"""Existence checks and cautious enrichment for dataset records.

The verifier is the mechanical gate between "a model says this dataset exists"
and "show it to a researcher". For every input item it tries, in order:

1. ``registry-api``: an adapter whose HOSTS cover the landing page confirms the
   record with its own ``lookup``; empty fields are filled from that record.
2. ``doi``: the DOI is looked up (the DataCite adapter first, then the doi.org
   handle service, which knows every registration agency), the landing page is
   checked, and an adapter for the landing host is asked for its metadata.
3. ``http``: the link itself is fetched (HEAD, then GET) and judged. Hard 404s,
   soft 404s, redirects to a home or search page, login walls, bot blocks and
   JavaScript shells that answer every address are told apart.

Anything that is not confirmed comes back with ``verified: false`` and the reason
in ``problems``. ``verification.outcome`` keeps "does not exist" (``not_found``),
"the link leads somewhere else" (``wrong_page``) and "could not check"
(``could_not_check``: blocked, login, timeout) apart, because calling a real
dataset fake is also a failure.

Page text never sets an access tier or a licence. It only adds quoted hints to
``verification.notes`` so the agent knows what to read on the landing page.
"""
from __future__ import annotations

import copy
import os
import re
import threading
import time
import urllib.parse
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from html.parser import HTMLParser

from scoutlib import common
from scoutlib import sources as _sources

__all__ = ["verify_records", "CONFIRMED", "NOT_FOUND", "WRONG_PAGE", "UNCHECKED"]

TIMEOUT = 10.0          # seconds per request; the shared default (20 s, 2 retries) is too slow here
MAX_WORKERS = 8         # different hosts run side by side; one host is never hit in parallel
PROXY_WORKERS = 2       # behind a proxy (see common.parallel_allowed): fewer transfers at once
RUN_BUDGET = 90.0       # seconds for a whole run (override: env SCOUT_VERIFY_BUDGET); then "could not check"
ADAPTER_BUDGET = 25.0   # seconds one registry lookup may take (adapters use the slower shared defaults)
LOCK_WAIT = 30.0        # seconds to wait for a host that another check is using
PAGE_BYTES = 400000     # enough for the head, title and the first screens of text
THIN_TEXT = 400         # fewer visible characters than this: the page may be a JavaScript shell
HTML_ACCEPT = "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5"
CSL_ACCEPT = "application/vnd.citationstyles.csl+json"
HANDLE_API = "https://doi.org/api/handles/"
DOI_RESOLVER = "https://doi.org/"

CONFIRMED = "confirmed"
NOT_FOUND = "not_found"
WRONG_PAGE = "wrong_page"
UNCHECKED = "could_not_check"

_RECORD_DEFAULTS = {
    "description": "", "doi": None, "publisher": None, "creators": [], "year": None,
    "version": None, "updated": None, "licence": None, "size": None, "formats": [],
    "subjects": [], "usage": {}, "extra": {},
}
_FILLABLE = ("title", "url", "description", "doi", "publisher", "creators", "year", "version",
             "updated", "licence", "size", "formats", "subjects")


# --------------------------------------------------------------------- run state

class _Locks(object):
    """One lock per host or adapter, so a service never sees two requests at once."""

    def __init__(self):
        self._guard = threading.Lock()
        self._locks = {}

    def _get(self, key):
        with self._guard:
            lock = self._locks.get(key)
            if lock is None:
                lock = self._locks[key] = threading.Lock()
            return lock

    @contextmanager
    def hold(self, keys, timeout=None):
        # Sorted acquisition, and never nested, so two threads cannot deadlock. A bounded
        # wait keeps a host held by an abandoned (still running) registry call from stalling us.
        names = sorted(set(k for k in keys if k))
        held = []
        try:
            for key in names:
                lock = self._get(key)
                if not lock.acquire(True, -1 if timeout is None else max(0.0, timeout)):
                    raise common.FetchError(key, None, "skipped: %s is still busy with an earlier request" % key)
                held.append(lock)
            yield
        finally:
            for lock in reversed(held):
                lock.release()


class _Context(object):
    def __init__(self, sources, timeout, budget):
        self.sources = dict(sources or {})
        self.import_errors = self.sources.pop("_errors", {}) or {}
        self.timeout = timeout
        self.budget = budget
        self.deadline = time.monotonic() + budget
        self.abandoned = set()   # lock keys still held by a registry call we stopped waiting for
        self.guard = threading.Lock()
        self.locks = _Locks()
        self.page_cache = {}
        self.doi_cache = {}
        self.lookup_cache = {}
        self.any_response = False
        self.adapter_down = {}   # adapter NAME -> reason; it gave no response once, skip it for this run
        self.host_failures = {}  # host -> consecutive network failures (timeouts, TLS errors)
        self.registry_hosts = set()
        for module in self.sources.values():
            for host in getattr(module, "HOSTS", ()) or ():
                self.registry_hosts.add(_host_key(host))

    def remaining(self):
        return self.deadline - time.monotonic()

    def out_of_time(self, what):
        return common.FetchError(what, None, "skipped: the time budget for this run (%d s) was used up; verify the "
                                             "unchecked items again in a smaller batch" % self.budget)


class _Verdict(object):
    def __init__(self):
        self.verified = False
        self.method = None
        self.http_status = None
        self.final_url = None
        self.problems = []
        self.codes = []
        self.notes = []
        self.outcome = None
        self.registry = None
        self.found_title = None
        self.registry_miss = None
        self.host_decided = False   # the registry that hosts the data has set the access tier

    def problem(self, code, message):
        if message not in self.problems:
            self.problems.append(message)
        if code not in self.codes:
            self.codes.append(code)

    def fail(self, code, message, outcome):
        self.verified = False
        self.outcome = outcome
        self.problem(code, message)

    def confirm(self, method):
        self.verified = True
        self.method = method
        self.outcome = CONFIRMED

    def note(self, text):
        if text and text not in self.notes:
            self.notes.append(text)

    def block(self):
        outcome = self.outcome or (CONFIRMED if self.verified else UNCHECKED)
        return {
            "verified": bool(self.verified),
            "method": self.method,
            "http_status": self.http_status,
            "final_url": self.final_url,
            "checked_at": common.now_iso(),
            "problems": list(self.problems),
            "notes": list(self.notes),
            "outcome": outcome,
            "problem_types": list(self.codes),
            "registry": self.registry,
            "found_title": self.found_title,
        }


# ------------------------------------------------------------------ small helpers

def _host_key(url_or_host):
    text = str(url_or_host or "").strip().lower()
    host = urllib.parse.urlsplit(text).netloc if "//" in text else text.split("/")[0]
    host = host.split("@")[-1]
    return host[4:] if host.startswith("www.") else host


def _short(text, limit=160):
    return common.truncate(str(text or ""), limit)


def _empty(value):
    return value is None or value == "" or value == [] or value == {}


_DOI_URL_RE = re.compile(r"^https?://(?:dx\.)?doi\.org/", re.I)
_DOI_BODY_RE = re.compile(r"^10\.\d{4,9}/\S+$")
_DOI_IN_TEXT_RE = re.compile(r"(10\.\d{4,9}/[^\s?#&\"'<>]+)")
_DOI_PATH_SUFFIX_RE = re.compile(
    r"/(full|abstract|pdf|epdf|epub|html|summary|references|figures|tables|download|metrics|citations?|meta)/?$",
    re.I)


def _is_doi_url(url):
    return bool(url) and bool(_DOI_URL_RE.match(str(url).strip()))


def _clean_doi(value):
    """Return (doi, problem) for a DOI string from the input; doi is None when absent or malformed."""
    if value is None or str(value).strip() == "":
        return None, None
    text = urllib.parse.unquote(str(value).strip())
    doi = common.norm_doi(text) or ""
    doi = re.sub(r"[?#].*$", "", doi).strip().rstrip(".,;)]>")
    if not _DOI_BODY_RE.match(doi):
        return None, "%r is not a well-formed DOI (expected 10.<prefix>/<suffix>)" % (str(value)[:80],)
    return doi, None


def _doi_from_doi_url(url):
    path = urllib.parse.unquote(_DOI_URL_RE.sub("", str(url).strip(), count=1))
    return _clean_doi(path)[0]


def _doi_in_url(url):
    """A DOI embedded in a landing-page address (repository or publisher pattern), or None."""
    if not url or _is_doi_url(url):
        return None
    match = _DOI_IN_TEXT_RE.search(urllib.parse.unquote(str(url)))
    if not match:
        return None
    doi = match.group(1)
    for _ in range(2):
        doi = _DOI_PATH_SUFFIX_RE.sub("", doi)
    return _clean_doi(doi)[0]


def _quote_doi(doi):
    return urllib.parse.quote(doi, safe="/()._-;:")


_LANG = r"(en|de|fr|es|it|ja|jp|zh|ko|pt|ru|nl|sv|fi|da|no|nb|pl|cs|tr|ar|he|el|hu|ro|uk|id|th|vi)"
_ROOT_PATH_RE = re.compile(
    r"^/?$|^/(index|home|default|start|welcome|main)(\.[a-z0-9]+)?/?$|^/" + _LANG + r"([-_][a-z]{2})?/?(index\.[a-z]+)?$",
    re.I)
_SEARCH_PATH_RE = re.compile(r"/(search|find|results|browse|discover)/?$|^/search(/|$)", re.I)
_SEARCH_KEYS = {"q", "query", "search", "term", "terms", "keyword", "keywords", "s", "text", "search_query"}
_LOGIN_PATH_RE = re.compile(
    r"/(login|log-in|log_in|signin|sign-in|sign_in|logon|sso|cas/login|oauth2?|saml2?|authorize|"
    r"accounts?/login|users?/sign_in|users?/login|session/new|idp)(/|\.|\?|$)", re.I)
_LOGIN_HOST_RE = re.compile(r"^(login|auth|sso|idp|signin|accounts|account|cas)\.", re.I)


def _is_root(url):
    parts = urllib.parse.urlsplit(url)
    return bool(_ROOT_PATH_RE.match(parts.path or "")) and not parts.query


def _is_search(url):
    parts = urllib.parse.urlsplit(url)
    if _SEARCH_PATH_RE.search(parts.path or ""):
        return True
    keys = {k.lower() for k, _ in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)}
    return bool(keys & _SEARCH_KEYS)


def _is_login_url(url):
    parts = urllib.parse.urlsplit(url)
    return bool(_LOGIN_PATH_RE.search(parts.path or "")) or bool(_LOGIN_HOST_RE.match(parts.netloc or ""))


def _same_page(a, b):
    def key(u):
        parts = urllib.parse.urlsplit(str(u or "").strip())
        return (_host_key(parts.netloc), (parts.path or "/").rstrip("/") or "/", parts.query)
    return bool(a) and bool(b) and key(a) == key(b)


_DNS_RE = re.compile(r"nodename nor servname|name or service not known|getaddrinfo failed|"
                     r"no address associated|name does not resolve|errno -2\b|errno 8\b|errno 11001", re.I)


def _is_dns_error(exc):
    return bool(_DNS_RE.search(str(exc)))


# ------------------------------------------------------------------- HTML parsing

class _PageParser(HTMLParser):
    _SKIP = {"script", "style", "noscript", "template", "svg"}

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.title = None
        self._title = None
        self.meta = {}
        self.headings = []
        self._heading = None
        self._skip = 0
        self.chunks = []
        self.size = 0
        self.has_password = False
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attrs = dict((k.lower(), v or "") for k, v in attrs if k)
        if tag == "title" and self.title is None and self._title is None:
            self._title = []
        elif tag == "meta":
            key = (attrs.get("name") or attrs.get("property") or attrs.get("itemprop") or "").lower()
            if key and "content" in attrs and key not in self.meta:
                self.meta[key] = attrs["content"]
        elif tag == "link" and "canonical" in attrs.get("rel", "").lower():
            self.canonical = attrs.get("href")
        elif tag == "input" and attrs.get("type", "").lower() == "password":
            self.has_password = True
        elif tag in ("h1", "h2") and self._heading is None and len(self.headings) < 4:
            self._heading = []
        if tag in self._SKIP:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title" and self._title is not None:
            self.title = " ".join("".join(self._title).split())
            self._title = None
        elif tag in ("h1", "h2") and self._heading is not None:
            text = " ".join("".join(self._heading).split())
            if text:
                self.headings.append(text)
            self._heading = None
        if tag in self._SKIP and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._title is not None:
            self._title.append(data)
            return
        if self._skip:
            return
        if self._heading is not None:
            self._heading.append(data)
        if self.size < 40000 and data.strip():
            self.chunks.append(data)
            self.size += len(data)


def _parse_html(text):
    parser = _PageParser()
    try:
        parser.feed(text[:PAGE_BYTES])
        parser.close()
    except Exception:  # a malformed page still yields whatever was parsed before the error
        pass
    if parser._title is not None and parser.title is None:
        parser.title = " ".join("".join(parser._title).split())
    meta = parser.meta
    visible = " ".join(" ".join(parser.chunks).split())
    doi = None
    for key in ("citation_doi", "dc.identifier", "dcterms.identifier", "prism.doi", "bepress_citation_doi"):
        value = meta.get(key)
        if value and _DOI_IN_TEXT_RE.search(value):
            doi = _clean_doi(_DOI_IN_TEXT_RE.search(value).group(1))[0]
            if doi:
                break
    return {
        "title": parser.title or "",
        "og_title": meta.get("og:title") or meta.get("twitter:title") or "",
        "citation_title": meta.get("citation_title") or meta.get("dc.title") or meta.get("dcterms.title") or "",
        "headings": parser.headings,
        "description": meta.get("description") or meta.get("og:description") or meta.get("dc.description") or "",
        "site_name": meta.get("og:site_name") or meta.get("citation_publisher") or meta.get("dc.publisher") or "",
        "doi": doi,
        "text": visible,
        "has_password": parser.has_password,
        "canonical": parser.canonical,
    }


def _heads(page):
    if not page:
        return []
    return [t for t in [page["title"], page["og_title"], page["citation_title"]] + page["headings"][:2] if t]


# ----------------------------------------------------------------- page judgement

_NF_STRONG = re.compile(
    r"\b(page|record|dataset|data\s*set|item|resource|file|url|link|project|repository|study|entry|document|content)s?\s+"
    r"(you\s+(requested|are\s+looking\s+for|were\s+looking\s+for)\s+)?"
    r"(was\s+|is\s+|has\s+been\s+)?"
    r"(not\s+found|does\s*n[o']t\s+exist|does\s+not\s+exist|no\s+longer\s+(exists|available)|"
    r"(removed|deleted|withdrawn|taken\s+down)\b|could\s*n[o']t\s+be\s+found|cannot\s+be\s+found|can't\s+be\s+found|"
    r"unavailable\b)"
    r"|\b(error|http)\s*(404|410)\b"
    r"|\b(404|410)\s*[-:|–—]?\s*(error|not\s+found|page\s+not\s+found|gone)\b"
    r"|\bno\s+such\s+(page|record|dataset|file|item|resource|project|entry)\b"
    r"|\b(sorry|oops)\b[^.!]{0,60}\b(could\s*n[o']t|can\s*n[o']?t|unable\s+to)\s+find\b"
    r"|\bthis\s+(record|dataset|page|item|entry)\s+(has\s+been|was|is)\s+(removed|deleted|withdrawn|retracted)\b",
    re.I)
_NF_HEAD_ONLY = re.compile(r"^\W*(error\W*)?(404|410)\b|\bnot\s+found\b|\bpage\s+not\s+available\b", re.I)

_CHALLENGE_TITLE = re.compile(
    r"just a moment|attention required|access denied|are you a (human|robot)|verify(ing)? (that )?you are (a )?human|"
    r"security check|captcha|request blocked|ddos protection|bot (check|detection|protection)|"
    r"pardon our interruption|checking your browser|please enable (javascript and )?cookies", re.I)
_CHALLENGE_BODY = re.compile(
    r"cf-chl|challenge-platform|g-recaptcha|h-captcha|hcaptcha|_incapsula_|px-captcha|perimeterx|"
    r"datadome|captcha-delivery", re.I)
_LOGIN_TITLE = re.compile(
    r"\b(log\s*in|sign\s*in|login|sign\s*on|single\s+sign|authentication\s+required|authenticate)\b", re.I)


def _soft_404(page):
    """The phrase that marks this page as an error page, or None."""
    if not page:
        return None
    for head in _heads(page):
        if _NF_HEAD_ONLY.search(head) or _NF_STRONG.search(head):
            return head
    start = page["text"][:400]
    match = _NF_STRONG.search(start)
    if match:
        return match.group(0)
    return None


def _challenge(resp, page, body=None):
    """Strong signs of a bot wall: a WAF header or a challenge title. With `body`, also a
    challenge script on a page that has almost no text (many normal pages embed such scripts)."""
    headers = {k.lower(): v for k, v in (resp.headers or {}).items()}
    if "x-amzn-waf-action" in headers or headers.get("cf-mitigated") or "x-datadome" in headers:
        return True
    if page and _CHALLENGE_TITLE.search(page["title"] or ""):
        return True
    if body is not None:
        thin = page is None or len(page["text"]) < THIN_TEXT
        return thin and bool(_CHALLENGE_BODY.search(body[:6000]))
    return False


def _login_page(page, final_url):
    if not page:
        return False
    title_hit = bool(_LOGIN_TITLE.search(page["title"] or "")) or any(
        _LOGIN_TITLE.search(h) for h in page["headings"][:1])
    if title_hit and (page["has_password"] or _is_login_url(final_url) or len(page["text"]) < 1500):
        return True
    return page["has_password"] and _is_login_url(final_url)


def _htmlish(ctype, body):
    ctype = (ctype or "").lower()
    if "html" in ctype or "xml" in ctype:
        return True
    if not ctype:
        return body[:200].lstrip().startswith(b"<")
    return False


def _page_result(url, **kw):
    res = {"url": url, "status": None, "final_url": None, "outcome": None, "code": None, "message": "",
           "page": None, "length": None, "content_length": None, "thin": False, "catch_all": None}
    res.update(kw)
    return res


HOST_FAILURE_LIMIT = 2   # after this many network failures in a row, a host is skipped for the run


def _request(ctx, url, method="GET", accept=HTML_ACCEPT, retries=0, max_bytes=PAGE_BYTES):
    host = _host_key(url)
    remaining = ctx.remaining()
    if remaining <= 0:
        raise ctx.out_of_time(url)
    wait = 0.0 if host in ctx.abandoned else min(LOCK_WAIT, remaining)
    with ctx.locks.hold([host], timeout=wait):
        if ctx.host_failures.get(host, 0) >= HOST_FAILURE_LIMIT:
            raise common.FetchError(url, None, "skipped: %s did not respond to %d earlier requests in this run"
                                    % (host, HOST_FAILURE_LIMIT))
        if ctx.remaining() <= 0:
            raise ctx.out_of_time(url)
        try:
            resp = common.http_request(url, headers={"Accept": accept},
                                       timeout=max(2.0, min(ctx.timeout, ctx.remaining())),
                                       retries=retries if ctx.remaining() > 3 * ctx.timeout else 0,
                                       method=method, max_bytes=max_bytes)
        except common.FetchError as exc:
            # A cut body means the host answered; an invalid address is our input's fault. Neither
            # says the host is down, so neither may cost the other datasets on that host their check.
            if not _is_dns_error(exc) and getattr(exc, "kind", None) not in ("cut_body", "invalid_url"):
                ctx.host_failures[host] = ctx.host_failures.get(host, 0) + 1
            raise
    ctx.host_failures[host] = 0
    ctx.any_response = True
    return resp


def _fetch_page(ctx, url):
    cached = ctx.page_cache.get(url)
    if cached is None:
        cached = _fetch_page_uncached(ctx, url)
        ctx.page_cache[url] = cached
    return cached


def _network_failure(url, exc):
    host = urllib.parse.urlsplit(url).netloc
    if getattr(exc, "kind", None) == "invalid_url":
        return _page_result(url, outcome=NOT_FOUND, code="invalid_url",
                            message="%r is not a valid web address (%s)" % (_short(url, 100), _short(exc.reason, 100)))
    if _is_dns_error(exc):
        return _page_result(url, outcome=NOT_FOUND, code="host_not_found",
                            message="the host %s does not resolve (DNS lookup failed), so the link is invalid" % host)
    reason = str(exc.reason or exc)
    if reason.startswith("skipped:"):
        # Not asked at all (a registry call on this host has not returned, the host failed
        # twice, or the time budget is spent): say so, rather than "no response".
        return _page_result(url, outcome=UNCHECKED, code="unreachable",
                            message="could not check: %s; verify this item again later" % _short(reason, 160))
    return _page_result(url, outcome=UNCHECKED, code="unreachable",
                        message="could not check: no response from %s (%s)" % (host, _short(reason, 120)))


def _fetch_page_uncached(ctx, url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme.lower() not in ("http", "https") or not parts.netloc:
        return _page_result(url, outcome=NOT_FOUND, code="invalid_url",
                            message="%r is not a web address (http or https)" % (_short(url, 100),))
    head = None
    head_error = None
    try:
        head = _request(ctx, url, "HEAD")
    except common.FetchError as exc:
        if _is_dns_error(exc) or getattr(exc, "kind", None) == "invalid_url":
            return _network_failure(url, exc)
        head_error = exc
    if head is not None and head.ok and head.status != 202 and not _challenge(head, None):
        ctype = head.header("content-type")
        if ctype and not _htmlish(ctype, b""):
            # A file (data download, JSON, PDF): HEAD is enough and avoids downloading it.
            length = head.header("content-length")
            return _page_result(url, status=head.status, final_url=head.url or url, outcome=CONFIRMED,
                                content_length=int(length) if length.isdigit() else None,
                                message="the link serves a file (%s)" % ctype.split(";")[0])
    # HEAD is never trusted for a negative answer: some sites answer HEAD 404 and GET 200.
    try:
        resp = _request(ctx, url, "GET", retries=0 if head_error is not None else 1)
    except common.FetchError as exc:
        return _network_failure(url, exc)
    return _classify(url, resp)


def _classify(url, resp):
    status = resp.status
    final = resp.url or url
    body = resp.body or b""
    ctype = resp.header("content-type")
    text = resp.text() if body else ""
    page = _parse_html(text) if body and _htmlish(ctype, body) else None
    res = _page_result(url, status=status, final_url=final, page=page, length=len(body))
    host = urllib.parse.urlsplit(final).netloc

    def done(outcome, code, message):
        res.update(outcome=outcome, code=code, message=message)
        return res

    challenge = ("could not check: %s answered with a bot challenge (HTTP %d); the page may exist, open it in a "
                 "browser" % (host, status))
    if _challenge(resp, page):
        return done(UNCHECKED, "blocked", challenge)
    if status in (404, 410):
        return done(NOT_FOUND, "not_found", "does not exist at this address: HTTP %d%s from %s" % (
            status, " (gone)" if status == 410 else "", final))
    error_phrase = _soft_404(page)
    if error_phrase and status >= 400:
        return done(NOT_FOUND, "not_found", 'does not exist at this address: HTTP %d and the page says "%s"'
                    % (status, _short(error_phrase, 80)))
    if status == 429:
        return done(UNCHECKED, "rate_limited",
                    "could not check: %s is rate-limiting automated requests (HTTP 429); this says nothing about existence"
                    % host)
    if not error_phrase and _challenge(resp, page, text):
        return done(UNCHECKED, "blocked", challenge)
    if status in (400, 422):
        return done(NOT_FOUND, "not_found", "the server rejected this address as invalid (HTTP %d)" % status)
    if status == 401:
        return done(UNCHECKED, "login_required",
                    "requires login to view (HTTP 401); existence not confirmed")
    if status == 403:
        if _login_page(page, final):
            return done(UNCHECKED, "login_required", "requires login to view (HTTP 403, login page); existence not confirmed")
        return done(UNCHECKED, "blocked",
                    "could not check: %s refused the automated request (HTTP 403); many sites block non-browser "
                    "clients, so this does not mean the dataset is missing" % host)
    if status >= 500:
        return done(UNCHECKED, "server_error", "could not check: %s returned a server error (HTTP %d)" % (host, status))
    if status >= 300:
        return done(UNCHECKED, "unexpected_status", "could not check: HTTP %d from %s" % (status, final))
    if status >= 400:
        return done(UNCHECKED, "unexpected_status", "could not check: HTTP %d from %s" % (status, final))

    # 2xx from here on.
    if not body.strip():
        return done(UNCHECKED, "empty_response",
                    "could not check: HTTP %d with an empty page from %s (typically a bot challenge)" % (status, host))
    if page is None:
        return done(CONFIRMED, None, "the link serves a file (%s)" % (ctype.split(";")[0] or "unknown type"))
    if _is_login_url(final) and not _is_login_url(url):
        return done(UNCHECKED, "login_required",
                    "requires login to view: the link redirects to a sign-in page (%s); existence not confirmed" % final)
    if not _is_root(url) and _is_root(final):
        return done(WRONG_PAGE, "redirected_home",
                    "the link redirects to the home page of %s (%s) instead of a record; the record is probably gone "
                    "or the link is wrong" % (host, final))
    if _is_search(final) and not _is_search(url):
        return done(WRONG_PAGE, "redirected_search",
                    "the link redirects to a search page (%s) instead of a record" % final)
    if error_phrase:
        return done(NOT_FOUND, "soft_404", 'does not exist: the page answers HTTP %d but says "%s"'
                    % (status, _short(error_phrase, 80)))
    if _login_page(page, final):
        return done(UNCHECKED, "login_required", "requires login to view (sign-in page); existence not confirmed")
    res["thin"] = len(page["text"]) < THIN_TEXT
    return done(CONFIRMED, None, "HTTP %d" % status)


def _probe_url(url):
    """A sibling address that should not exist, to see whether the site answers everything alike.

    Many sites route by a numeric id and ignore the words after it (/dataset/174/<anything>),
    so when the path has a numeric segment, that id is changed rather than the slug.
    """
    parts = urllib.parse.urlsplit(url)
    token = "zz-scout-probe-" + uuid.uuid4().hex[:8]
    path = parts.path or ""
    segments = path.split("/")
    numeric = [i for i, seg in enumerate(segments) if seg.isdigit() and len(seg) <= 12]
    if numeric:
        segments[numeric[-1]] = "9" + "".join(str(int(c, 16) % 10) for c in uuid.uuid4().hex[:9])
        return urllib.parse.urlunsplit((parts.scheme, parts.netloc, "/".join(segments), parts.query, ""))
    last = path.rstrip("/").rsplit("/", 1)[-1]
    pairs = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    if pairs and (not path.strip("/") or "." in last):
        key, value = pairs[-1]
        pairs[-1] = (key, value + token)
        return urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, urllib.parse.urlencode(pairs), ""))
    if not path.strip("/"):
        return None
    new_path = path.rstrip("/") + "-" + token + ("/" if path.endswith("/") else "")
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, new_path, "", ""))


def _catch_all(ctx, res):
    """True when the site serves the same page for an address that cannot exist (a JavaScript shell)."""
    if res.get("catch_all") is not None:
        return res["catch_all"]
    verdict = False
    probe = _probe_url(res.get("final_url") or res["url"])
    if probe and res.get("page"):
        try:
            resp = _request(ctx, probe, "GET")
        except common.FetchError:
            resp = None
        if resp is not None and resp.ok and resp.body:
            other = _parse_html(resp.text())
            same_title = " ".join(other["title"].lower().split()) == " ".join(res["page"]["title"].lower().split())
            similar = abs(len(resp.body) - (res.get("length") or 0)) <= max(300, 0.1 * (res.get("length") or 0))
            # The probe was served this very record (its canonical link names the original page):
            # the site ignored the changed part of the address, which is not a catch-all.
            original = res.get("final_url") or res["url"]
            same_record = bool(other.get("canonical")) and not _is_root(urllib.parse.urljoin(original, other["canonical"])) \
                and _same_page(urllib.parse.urljoin(original, other["canonical"]), original)
            verdict = bool(same_title and (similar or res.get("thin")) and not _soft_404(other) and not same_record)
    res["catch_all"] = verdict
    return verdict


# ---------------------------------------------------------------- title matching

_STOP = frozenset("""
a an the of for and or in on at to from with by via into over under about as is are be its it this that
de la le les el et und der die das du des del y e o
data dataset datasets database databases db set sets corpus corpora collection collections repository
file files version versions release edition v vol volume new open public home page record records site
website official project available download index
""".split())
_SLUG_STOP = frozenset("""
http https www com org net edu gov html htm php aspx jsp content contents dataset datasets data record records
article articles details detail view views doi abs files file item items entry entries resource resources
""".split())


def _words(text):
    text = common.strip_html(text or "").lower().replace("’", "'")
    text = re.sub(r"'s\b", "", text)
    return re.findall(r"[^\W_]+", text)


def _stem(word):
    if len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _content(words):
    out = []
    for word in words:
        if word in _STOP or len(word) < 2:
            continue
        if word.isdigit() and len(word) < 4:
            continue
        if re.match(r"^v\d+$", word):
            continue
        out.append(word)
    return out


def _coverage(expected, texts):
    """Share of the expected title's distinctive words that the found texts contain (0..1), or None."""
    ewords = _words(expected)
    econtent = _content(ewords)
    etoks = []
    for word in econtent:
        stem = _stem(word)
        if stem not in etoks:
            etoks.append(stem)
    if not etoks:
        return None
    word_lists = [_words(t) for t in texts if t]
    fwords = [w for ws in word_lists for w in ws]
    if not fwords:
        return None
    fset = set(_stem(w) for w in fwords)
    joined = set()
    for ws in word_lists:
        for a, b in zip(ws, ws[1:]):
            joined.add(a + b)
    initials = []
    for ws in word_lists:
        if len(ws) <= 40:  # titles only: initials of a long text match short tokens by chance
            initials.append("".join(w[0] for w in ws))
            initials.append("".join(w[0] for w in _content(ws)))

    def found(tok):
        if tok in fset or tok in joined:
            return True
        if len(tok) >= 5:
            for f in fset:
                if len(f) >= 5 and (f.startswith(tok) or tok.startswith(f) or tok in f or f in tok):
                    return True
        if 3 <= len(tok) <= 10 and tok.isalpha():
            return any(tok in ini for ini in initials if len(ini) >= len(tok))
        return False

    matched = set(t for t in etoks if found(t))
    # A found acronym that spells a run of the expected words covers those words.
    for f in fset:
        if not (3 <= len(f) <= 10 and f.isalpha()):
            continue
        for i in range(len(econtent)):
            for j in range(i + 2, min(len(econtent), i + 10) + 1):
                if "".join(w[0] for w in econtent[i:j]) == f:
                    matched.update(_stem(w) for w in econtent[i:j])
    return len(matched & set(etoks)) / float(len(etoks))


_URLISH_RE = re.compile(r"^\s*(https?://|www\.|doi:|10\.\d{4,9}/)", re.I)


def _usable_title(expected):
    """False for an empty title, or one that is only a web address or a DOI (nothing to compare)."""
    text = str(expected or "").strip()
    if not text or _URLISH_RE.match(text) or (" " not in text and "://" in text):
        return False
    return bool(_content(_words(text)))


def _title_verdict(expected, primary, secondary=(), strict=False):
    """True (consistent), False (clearly a different resource) or None (nothing to compare)."""
    if not _usable_title(expected):
        return None
    primary = [t for t in primary if t]
    secondary = [t for t in secondary if t]
    if not primary and not secondary:
        return None
    first = _coverage(expected, primary) if primary else None
    if strict:
        return bool(first is not None and first >= 0.6)
    if first is not None and first >= 0.3:
        return True
    both = _coverage(expected, primary + secondary)
    if both is None:
        return None
    return both >= 0.5


SAME_NAME = 0.6       # share of the given name's distinctive words a registry title must contain
PARTLY_SAME = 0.3     # below this the registry title names something else


def _without_registry_words(expected, names):
    """The expected title without words that only name the registry (one-word names such as the
    adapter's NAME or a one-word publisher), or None when nothing else is left."""
    drop = set()
    for name in names:
        words = _words(name)
        if len(words) == 1:
            drop.add(_stem(words[0]))
    if not drop:
        return expected
    kept = [w for w in _words(expected) if _stem(w) not in drop]
    return " ".join(kept) if _content(kept) else None


def _name_check(expected, titles, registry_names=(), identifiers=()):
    """Compare a given name with a title a registry states itself.

    Returns "same", "differs" (the registry title contains only some of the given
    name's distinctive words), "mismatch" (it names something else) or None
    (nothing to compare). A registry's description never rescues a title that
    does not match: words such as "sleep" or "apnea" in an abstract are no
    evidence that an invented name belongs to the record. Only identifiers (the
    record's address slug) and acronyms count besides the title.
    """
    titles = [t for t in titles if t]
    if not _usable_title(expected) or not titles:
        return None
    wanted = _without_registry_words(expected, registry_names)
    if wanted is None:
        return None
    cover = _coverage(wanted, titles)
    if cover is None:
        return None
    ids = [t for t in identifiers if t]
    by_id = _coverage(wanted, ids) if ids else None
    best = max(cover, by_id or 0.0)
    if best >= SAME_NAME:
        return "same"
    if best >= PARTLY_SAME:
        return "differs"
    return "mismatch"


def _extra(rec):
    if not isinstance(rec.get("extra"), dict):
        rec["extra"] = {}
    return rec["extra"]


def _adopt_title(rec, found, check, where, v):
    """A record confirmed by a registry carries the registry's own title; the given one is kept."""
    if not found:
        return
    given = rec.get("title")
    if _empty(given):
        rec["title"] = common.truncate(common.strip_html(found), 300)
        return
    if common.norm_title(given) == common.norm_title(found):
        return
    _extra(rec).setdefault("given_title", given)
    rec["title"] = common.truncate(common.strip_html(found), 300)
    if check == "differs":
        v.problem("title_differs",
                  'the name given, "%s", only partly matches %s, "%s"; the record is listed under that title. Check '
                  'that it is the dataset you meant' % (_short(given, 120), where, _short(found, 120)))
    else:
        v.note('title set to %s, "%s" (given as "%s")' % (where, _short(found, 120), _short(given, 120)))


def _slug_text(url):
    if not url:
        return ""
    parts = urllib.parse.urlsplit(str(url))
    words = re.split(r"[/\-_.+=&?%]+", urllib.parse.unquote(parts.path or ""))
    return " ".join(w for w in words if len(w) >= 3 and w.lower() not in _SLUG_STOP and not w.isdigit())


# ------------------------------------------------------------- hints & enrichment

_HINTS = [
    r"data\s+(use|usage|sharing|access|transfer|processing)\s+agreements?",
    r"credentialed\s+(access|users?|researchers?|data)|credentialing",
    r"request(ing)?\s+access|access\s+requests?|apply\s+for\s+access|application\s+for\s+access|access\s+application",
    r"application\s+form",
    r"(restricted|controlled|managed)\s+access",
    r"access\s+is\s+(restricted|limited|controlled)",
    r"(data\s+)?access\s+committee",
    r"ethics\s+(approval|committee)|institutional\s+review\s+board",
    r"(log\s*in|sign\s*in|registration|an\s+account)\s+(is\s+)?(required|needed)|must\s+(be\s+)?(registered|logged\s+in)|"
    r"(log|sign)\s*in\s+to\s+(download|access|view)",
    r"human\s+(subjects?\s+)?research\s+training",
    r"\bembargo(ed)?\b",
    r"available\s+(up)?on\s+(reasonable\s+)?request",
    r"not\s+(publicly|openly)\s+available",
    r"(agree|accept)\s+(to\s+)?(the\s+)?(terms|conditions)[^.]{0,40}\s+to\s+access",
    r"to\s+access\s+this\s+(dataset|data|database|repository)",
]
_HINT_RE = re.compile("|".join("(?:%s)" % p for p in _HINTS), re.I)


def _access_hints(page, limit=4):
    if not page:
        return []
    text = (page["description"] + " " + page["text"])[:30000]
    notes, seen = [], set()
    for match in _HINT_RE.finditer(text):
        phrase = " ".join(match.group(0).split())
        key = phrase.lower()[:30]
        if key in seen:
            continue
        seen.add(key)
        start, end = max(0, match.start() - 60), min(len(text), match.end() + 60)
        context = " ".join(text[start:end].split())
        notes.append('the landing page mentions "%s" ("...%s..."); confirm the access route on that page before '
                     'calling the data open' % (phrase, context))
        if len(notes) >= limit:
            break
    return notes


_RESTRICTIVENESS = {"open": 0, "account": 1, "gated": 2, "controlled": 3, "closed": 4}


def _note_conflict(rec, source, tier, evidence):
    conflicts = _extra(rec).setdefault("access_conflicts", [])
    entry = {"source": source, "tier": tier, "evidence": evidence or ""}
    if entry not in conflicts:
        conflicts.append(entry)


def _merge_access(rec, reg, name, v, host):
    """Decide the access tier when the record and a registry record disagree.

    The registry that hosts the data (`host`) is the authority on its own access
    rules, so its statement wins, also over a more permissive claim copied from an
    aggregator. When the host does not state a tier, a permissive claim from
    elsewhere is not confirmed and becomes `unknown`. Between two registries that do
    not host the data, the more restrictive statement is kept. The losing claim is
    kept in `extra.access_conflicts` and every disagreement is a problem, so it shows.
    """
    current = rec.get("access") if isinstance(rec.get("access"), dict) else {"tier": "unknown", "evidence": ""}
    incoming = reg.get("access") if isinstance(reg.get("access"), dict) else {}
    cur_tier = current.get("tier") if current.get("tier") in common.ACCESS_TIERS else "unknown"
    new_tier = incoming.get("tier") if incoming.get("tier") in common.ACCESS_TIERS else "unknown"
    cur_ev = current.get("evidence") or ""
    new_ev = incoming.get("evidence") or ""
    label = "%s: %s" % (name, new_ev) if new_ev else name
    source = rec.get("source") or "the input"
    if new_tier == cur_tier:
        if host and new_tier != "unknown":
            v.host_decided = True
        if new_tier == "unknown" and new_ev and (host or not cur_ev):
            # Neither states a tier, but the registry says why (a loading script only, an agreement on
            # an "Open" record): keep that reason. The hosting registry's reason replaces an older
            # one, such as a search listing's "look the repository up", which this lookup just did.
            rec["access"] = {"tier": "unknown", "evidence": label}
        return
    if cur_tier == "unknown":
        if new_tier != "unknown":
            rec["access"] = {"tier": new_tier, "evidence": label}
            v.host_decided = v.host_decided or host
            v.note("access tier '%s' taken from the %s registry record (%s)" % (new_tier, name, new_ev or "no evidence given"))
        return
    if new_tier == "unknown":
        if host and cur_tier in ("open", "account"):
            _note_conflict(rec, source, cur_tier, cur_ev)
            _note_conflict(rec, name, "unknown", new_ev)
            rec["access"] = {"tier": "unknown", "evidence": "%s does not confirm '%s' (%s); the record claimed it from "
                                                            "%s (%s)" % (name, cur_tier, new_ev or "no access statement",
                                                                         source, cur_ev or "no evidence")}
            v.host_decided = True
            v.problem("access_conflict",
                      "access tier conflict: the record says '%s' (%s) but the %s registry record, which hosts the data, "
                      "does not confirm it (%s); the tier was set to unknown, check the landing page"
                      % (cur_tier, cur_ev or "no evidence", name, new_ev or "no access statement"))
        return
    if host:
        winner, why = new_tier, "the %s registry hosts the data, so its statement was used" % name
        v.host_decided = True
    elif v.host_decided:
        winner, why = cur_tier, "the hosting registry's statement was kept"
    else:
        winner = max((cur_tier, new_tier), key=lambda t: _RESTRICTIVENESS.get(t, -1))
        why = "the more restrictive statement was kept"
    if winner == new_tier:
        _note_conflict(rec, source, cur_tier, cur_ev)
        rec["access"] = {"tier": new_tier, "evidence": label}
    else:
        _note_conflict(rec, name, new_tier, new_ev)
    v.problem("access_conflict",
              "access tier conflict: the record says '%s' (%s) but the %s registry record says '%s' (%s); %s, check the "
              "landing page" % (cur_tier, cur_ev or "no evidence", name, new_tier, new_ev or "no evidence", why))


def _merge(rec, reg, name, v, host=False):
    """Fill EMPTY fields of `rec` from a registry record and settle the access tier (see _merge_access).

    `host` is True when `reg` comes from the registry that holds the data: the adapter
    chosen for the given landing page, or for the landing page a DOI resolves to.
    """
    filled = []
    for field in _FILLABLE:
        if _empty(rec.get(field)) and not _empty(reg.get(field)):
            rec[field] = copy.deepcopy(reg[field])
            filled.append(field)
    for field in ("usage", "extra"):
        incoming = reg.get(field) or {}
        if isinstance(incoming, dict) and incoming:
            target = rec.get(field)
            if not isinstance(target, dict):
                target = rec[field] = {}
            added = [k for k in incoming if k not in target]
            for k in added:
                target[k] = copy.deepcopy(incoming[k])
            if added:
                filled.append(field)
    _merge_access(rec, reg, name, v, host)
    if filled:
        v.note("%s filled from the %s registry record" % (", ".join(filled), name))


def _fill_from_page(rec, page, v):
    if not page:
        return
    filled = []
    if _empty(rec.get("title")):
        title = page["citation_title"] or page["og_title"] or page["title"]
        if title:
            rec["title"] = common.truncate(common.strip_html(title), 300)
            filled.append("title")
    if _empty(rec.get("description")) and page["description"]:
        rec["description"] = common.truncate(common.strip_html(page["description"]), 700)
        filled.append("description")
    if _empty(rec.get("doi")) and page["doi"]:
        rec["doi"] = page["doi"]
        filled.append("doi")
    if _empty(rec.get("publisher")) and page["site_name"]:
        rec["publisher"] = common.truncate(common.strip_html(page["site_name"]), 200)
        filled.append("publisher")
    if filled:
        v.note("%s read from the landing page's own metadata" % ", ".join(filled))


# --------------------------------------------------------------- registry lookups

def _adapter_for(ctx, url):
    if not url or not ctx.sources:
        return None
    try:
        return _sources.source_for_url(url, ctx.sources)
    except Exception:
        return None


def _bounded_lookup(ctx, module, name, keys, arg):
    """Run an adapter's lookup in a helper thread and stop waiting after ADAPTER_BUDGET seconds.

    Adapters call the shared HTTP helper with its slower defaults (20 s, 2 retries), so one
    unreachable registry could otherwise hold a whole run for minutes. The helper thread keeps
    the registry's locks until it really returns, so the host still never sees two requests.
    """
    if name in ctx.adapter_down:
        raise common.FetchError(name, None, "skipped: %s" % ctx.adapter_down[name])
    remaining = ctx.remaining()
    if remaining <= 0:
        raise ctx.out_of_time(name)
    if any(k in ctx.abandoned for k in keys):
        raise common.FetchError(name, None, "skipped: an earlier %s lookup has not returned" % name)
    box = {"done": False, "abandoned": False}

    def run():
        try:
            with ctx.locks.hold(keys, timeout=LOCK_WAIT):
                box["result"] = module.lookup(arg)
        except BaseException as exc:  # handed to the waiting thread below
            box["error"] = exc
        finally:
            with ctx.guard:
                box["done"] = True
                if box["abandoned"]:
                    ctx.abandoned.difference_update(keys)

    worker = threading.Thread(target=run, name="scout-lookup-%s" % name)
    worker.daemon = True
    worker.start()
    budget = min(ADAPTER_BUDGET, remaining)
    worker.join(budget)
    with ctx.guard:
        late = not box["done"]
        if late:
            box["abandoned"] = True
            ctx.abandoned.update(keys)
    if late:
        ctx.adapter_down[name] = "the registry did not answer within %g s earlier in this run" % budget
        raise common.FetchError(name, None, "no answer within %g s" % budget)
    if "error" in box:
        raise box["error"]
    return box.get("result")


def _lookup(ctx, module, arg, v):
    name = getattr(module, "NAME", None) or getattr(module, "__name__", "adapter")
    key = (name, arg)
    if key in ctx.lookup_cache:
        result, error = ctx.lookup_cache[key]
    else:
        keys = ["adapter:%s" % name] + [_host_key(h) for h in (getattr(module, "HOSTS", ()) or ())]
        result, error = None, None
        try:
            result = _bounded_lookup(ctx, module, name, keys, arg)
        except Exception as exc:  # an adapter bug or outage must not stop the other checks
            error = "%s: %s" % (type(exc).__name__, _short(exc, 160))
            if isinstance(exc, common.FetchError) and exc.status is None and name not in ctx.adapter_down:
                ctx.adapter_down[name] = "the registry did not respond earlier in this run"
        if result is not None and not (isinstance(result, dict) and (result.get("title") or result.get("id"))):
            error, result = "returned something that is not a record", None
        ctx.lookup_cache[key] = (result, error)
    if error:
        v.note("the %s registry lookup failed (%s); fell back to other checks" % (name, error))
        return None
    return copy.deepcopy(result) if result is not None else None


def _handle(ctx, doi):
    """Ask the doi.org handle service: ("registered" | "not_registered" | "unknown", landing url, error)."""
    try:
        resp = _request(ctx, HANDLE_API + _quote_doi(doi), "GET", accept="application/json", retries=1)
    except common.FetchError as exc:
        return "unknown", None, "doi.org did not answer (%s)" % _short(exc.reason or exc, 100)
    try:
        data = resp.json()
    except ValueError:
        data = {}
    code = data.get("responseCode") if isinstance(data, dict) else None
    if code == 1:
        landing = None
        for value in data.get("values") or []:
            if value.get("type") == "URL":
                landing = (value.get("data") or {}).get("value")
                break
        return "registered", landing, ""
    if code == 200:  # handle exists, no URL value
        return "registered", None, ""
    if code == 100:
        return "not_registered", None, ""
    return "unknown", None, "doi.org answered HTTP %d (responseCode %s)" % (resp.status, code)


def _csl(ctx, doi):
    """Citation metadata through DOI content negotiation (Crossref, DataCite and others), or None."""
    try:
        resp = _request(ctx, DOI_RESOLVER + _quote_doi(doi), "GET", accept=CSL_ACCEPT, retries=0, max_bytes=2000000)
        if not resp.ok:
            return None
        data = resp.json()
    except (common.FetchError, ValueError):
        return None
    if not isinstance(data, dict):
        return None

    def first(value):
        if isinstance(value, list):
            value = value[0] if value else None
        return common.strip_html(value) if value else None

    year = None
    try:
        year = int(((data.get("issued") or {}).get("date-parts") or [[None]])[0][0])
    except (TypeError, ValueError, IndexError):
        year = None
    return {"title": first(data.get("title")), "type": data.get("type"), "publisher": first(data.get("publisher")),
            "year": year, "container": first(data.get("container-title"))}


def _resolve_doi(ctx, doi, v):
    """Registration state of a DOI plus whatever registries say about it."""
    cached = ctx.doi_cache.get(doi)
    if cached is not None:
        return copy.deepcopy(cached)
    res = {"state": "unknown", "landing": None, "records": [], "csl": None, "error": "", "host": None}
    datacite = ctx.sources.get("datacite")
    if datacite is not None and not callable(getattr(datacite, "lookup", None)):
        datacite = None
    reg = _lookup(ctx, datacite, doi, v) if datacite is not None else None
    if reg is not None:
        res["state"] = "registered"
        res["records"].append((getattr(datacite, "NAME", "datacite"), reg))
        landing = reg.get("url")
        if landing and not _is_doi_url(landing):
            res["landing"] = landing
        else:
            state, landing, _ = _handle(ctx, doi)
            res["landing"] = landing if state == "registered" else None
    else:
        state, landing, error = _handle(ctx, doi)
        res.update(state=state, landing=landing, error=error)
        if state == "registered":
            res["csl"] = _csl(ctx, doi)
    if res["state"] == "registered" and res["landing"] and not _is_doi_url(res["landing"]):
        adapter = _adapter_for(ctx, res["landing"])
        if adapter is not None and adapter is not datacite:
            more = _lookup(ctx, adapter, res["landing"], v)
            if more is not None:
                res["records"].insert(0, (getattr(adapter, "NAME", "registry"), more))
                res["host"] = getattr(adapter, "NAME", "registry")
    ctx.doi_cache[doi] = copy.deepcopy(res)
    return res


# ------------------------------------------------------------------- the checks

def _accept_registry(rec, reg, name, v):
    v.method = "registry-api"
    v.registry = name
    v.final_url = reg.get("url") or rec.get("url")
    v.found_title = reg.get("title") or None
    check = _name_check(rec.get("title"), [reg.get("title")], [name, reg.get("publisher")],
                        [_slug_text(reg.get("url")), _slug_text(rec.get("url"))])
    if check == "mismatch":
        v.fail("title_mismatch",
               'the link exists but describes a different resource: the %s record is titled "%s", not "%s"'
               % (name, _short(reg.get("title"), 120), _short(rec.get("title"), 120)), WRONG_PAGE)
        return
    v.confirm("registry-api")
    _adopt_title(rec, reg.get("title"), check, "the %s record's title" % name, v)
    reg_extra = reg.get("extra") if isinstance(reg.get("extra"), dict) else {}
    if reg_extra.get("version_not_listed") and reg.get("url"):
        # The link names a version the registry does not have: the facts below describe another
        # version, so the record must point at that version's address, not at the broken one.
        if rec.get("url") and not _same_page(rec.get("url"), reg["url"]):
            _extra(rec).setdefault("given_url", rec.get("url"))
            rec["url"] = reg["url"]
        v.problem("version_not_listed", "%s; the record now points at %s" % (reg_extra.get("version_note") or
                  "the %s registry does not list the version this link names" % name, reg["url"]))
    elif reg_extra.get("version_note"):
        v.note(reg_extra["version_note"])
    _merge(rec, reg, name, v, host=True)
    v.note("confirmed by the %s registry record %s" % (name, reg.get("id") or ""))
    if (rec.get("access") or {}).get("tier") == "closed":
        v.note("the registry marks this record as closed (withdrawn, embargoed or metadata only)")


def _confirm_by_doi(ctx, rec, doi, res, v, given_url):
    records = res["records"]
    csl = res.get("csl") or {}
    landing = res.get("landing")
    landing_adapter = any(name != "datacite" for name, _ in records)
    v.method = "registry-api" if records else "doi"
    v.registry = records[0][0] if records else None
    v.final_url = landing or (records[0][1].get("url") if records else None) or DOI_RESOLVER + doi
    page_res = None
    if landing and not landing_adapter:
        page_res = _fetch_page(ctx, landing)
        v.http_status = page_res["status"]
        v.final_url = page_res["final_url"] or landing
        if page_res["outcome"] == NOT_FOUND:
            v.method = "doi" if not records else v.method
            v.fail("doi_landing_broken", "the DOI %s is registered, but its landing page %s: %s; the record may have "
                   "been withdrawn or moved" % (doi, landing, page_res["message"]), NOT_FOUND)
            return
        if page_res["outcome"] == WRONG_PAGE:
            v.note("the DOI's landing page looks odd: %s" % page_res["message"])
        elif page_res["outcome"] == UNCHECKED:
            v.note("the DOI is registered; its landing page could not be checked (%s)" % page_res["message"])
    page = page_res["page"] if page_res and page_res["outcome"] == CONFIRMED else None
    stated = [r.get("title") for _, r in records] + [csl.get("title")]
    names = [n for n, _ in records] + [r.get("publisher") for _, r in records]
    ids = [_slug_text(landing), _slug_text(v.final_url)]
    if any(stated):
        # A registry or the DOI's own metadata states the title: its description cannot rescue another name.
        v.found_title = next((t for t in stated if t), None)
        check = _name_check(rec.get("title"), stated, names, ids)
        mismatch = check == "mismatch"
    else:
        primary = _heads(page) if page else []
        secondary = [r.get("description") for _, r in records] + [csl.get("container")]
        if page:
            secondary = secondary + [page["description"], page["text"][:3000]]
        v.found_title = next((t for t in primary if t), None)
        check = None
        mismatch = _title_verdict(rec.get("title"), primary, secondary) is False
    if mismatch:
        v.fail("title_mismatch",
               'the DOI %s exists but describes a different resource: it is registered as "%s", not "%s"'
               % (doi, _short(v.found_title, 120), _short(rec.get("title"), 120)), WRONG_PAGE)
        return
    v.confirm(v.method)
    if any(stated):
        if records or (csl.get("type") or "").lower() == "dataset":
            _adopt_title(rec, v.found_title, check, "the title registered for the DOI", v)
        elif check == "differs":
            # The DOI is probably the paper that describes the data: keep the dataset's name, but say so.
            v.problem("title_differs", 'the name given, "%s", only partly matches the title registered for the DOI, '
                      '"%s"; check that the DOI belongs to this dataset' % (_short(rec.get("title"), 120),
                                                                          _short(v.found_title, 120)))
    for name, reg in records:
        _merge(rec, reg, name, v, host=name == res.get("host"))
    if csl:
        filled = []
        for field, value in (("title", csl.get("title")), ("publisher", csl.get("publisher")), ("year", csl.get("year"))):
            if _empty(rec.get(field)) and value:
                rec[field] = value
                filled.append(field)
        if filled:
            v.note("%s filled from the DOI's citation metadata" % ", ".join(filled))
        if csl.get("type") and csl.get("type") != "dataset":
            v.note("the DOI is registered as type '%s', not 'dataset': it may be the paper that describes the data "
                   "rather than the data itself" % csl.get("type"))
    v.note("the DOI %s is registered%s" % (doi, " and resolves to %s" % landing if landing else ""))
    if page:
        for hint in _access_hints(page):
            v.note(hint)
        _fill_from_page(rec, page, v)
    if _empty(rec.get("doi")):
        rec["doi"] = doi
        v.note("doi filled from the link")
    if _empty(rec.get("url")):
        rec["url"] = DOI_RESOLVER + doi
    # The link the agent gave may be broken even though the DOI is fine.
    if given_url and not _is_doi_url(given_url) and not _same_page(given_url, landing) \
            and not _same_page(given_url, v.final_url):
        other = _fetch_page(ctx, given_url)
        if other["outcome"] in (NOT_FOUND, WRONG_PAGE) and other["code"] != "title_mismatch":
            v.problem("broken_link", "the link given does not work (%s); use the DOI landing page %s instead"
                      % (other["message"], v.final_url))


def _enrich_from_doi(ctx, rec, doi, v):
    """After the page itself was confirmed: fill empty fields from the registries that know its DOI."""
    res = _resolve_doi(ctx, doi, v)
    if res["state"] == "not_registered":
        if rec.get("doi") == doi:
            rec["doi"] = None
        v.note("the DOI %s found in the link or page metadata is not registered; it was not used" % doi)
        return
    if res["state"] != "registered":
        return
    merged = []
    for name, reg in res["records"]:
        if _name_check(rec.get("title"), [reg.get("title")], [name, reg.get("publisher")],
                       [_slug_text(reg.get("url"))]) == "mismatch":
            v.note('the DOI %s in the link belongs to "%s", which does not match this record; its metadata was not used'
                   % (doi, _short(reg.get("title"), 100)))
            continue
        _merge(rec, reg, name, v, host=name == res.get("host"))
        merged.append(name)
    if merged and not v.registry:
        v.registry = merged[0]
    if _empty(rec.get("doi")) and (merged or not res["records"]):
        rec["doi"] = doi
        v.note("doi %s read from the link and confirmed as registered" % doi)


def _verify_http(ctx, rec, url, v):
    res = _fetch_page(ctx, url)
    v.method = "http"
    v.http_status = res["status"]
    v.final_url = res["final_url"]
    if res["outcome"] != CONFIRMED:
        v.fail(res["code"], res["message"], res["outcome"])
        if res["page"]:
            v.found_title = res["page"]["title"] or None
        return
    page = res["page"]
    host = _host_key(url)
    if page:
        v.found_title = next(iter(_heads(page)), None)
    if _is_root(url):
        if host in ctx.registry_hosts or _adapter_for(ctx, url) is not None:
            v.fail("home_page", "the link is the home page of the %s repository, not a dataset record" % host, WRONG_PAGE)
            return
        if _title_verdict(rec.get("title"), _heads(page), strict=True) is not True:
            v.fail("home_page", 'the link is the home page of %s%s, not a page for this dataset' % (
                host, ' ("%s")' % _short(v.found_title, 80) if v.found_title else ""), WRONG_PAGE)
            return
        v.note("the link is the home page of %s; its title names the dataset, so the dataset seems to have its own "
               "site" % host)
    elif _is_search(url):
        v.fail("search_page", "the link is a search or listing page, not a dataset record", WRONG_PAGE)
        return
    if page and res["thin"] and _catch_all(ctx, res):
        v.fail("js_shell", "could not check: %s answers any address with the same page (a JavaScript app), so HTTP %d "
               "does not prove that the record exists; open the link in a browser" % (host, res["status"]), UNCHECKED)
        return
    if page and not _is_root(url):
        verdict = _title_verdict(rec.get("title"), _heads(page),
                                 [page["description"], _slug_text(res["final_url"] or url), page["text"][:3000]])
        if verdict is False:
            if _catch_all(ctx, res):
                v.fail("js_shell", "could not check: %s answers any address with the same page, so its title says "
                       "nothing about this record; open the link in a browser" % host, UNCHECKED)
            else:
                v.fail("title_mismatch", 'the URL exists but describes a different resource: the page is titled "%s", '
                       'not "%s"' % (_short(v.found_title, 120), _short(rec.get("title"), 120)), WRONG_PAGE)
            return
        if verdict is None and rec.get("title"):
            v.note("the page gives no usable title, so only its existence was checked")
        elif verdict and _usable_title(rec.get("title")) and _heads(page):
            # Consistent only through the page text or address: the page does not call itself that.
            named = _coverage(rec.get("title"), _heads(page))
            by_id = _coverage(rec.get("title"), [_slug_text(res["final_url"] or url)])
            if named is not None and named < PARTLY_SAME and (by_id or 0.0) < SAME_NAME:
                v.problem("title_differs",
                          'the page is titled "%s", which does not name "%s"; only words in its text or address '
                          'match, so check that this page is the dataset you meant'
                          % (_short(v.found_title, 120), _short(rec.get("title"), 120)))
    v.confirm("http")
    if not _same_page(url, res["final_url"]):
        v.note("the link redirects to %s" % res["final_url"])
    if page:
        for hint in _access_hints(page):
            v.note(hint)
        _fill_from_page(rec, page, v)
    elif res.get("content_length") and _empty(rec.get("size")):
        rec["size"] = {"bytes": res["content_length"]}
        v.note("size read from the Content-Length header of the file")


def _normalise(item):
    """(record, notes, input problem) for a full record or a minimal {title, url | doi} dict."""
    notes = []
    if not isinstance(item, dict):
        rec = common.make_record("manual", "invalid-input", _short(item, 200) if item is not None else "", "")
        return rec, notes, "the input item is not an object with a title and a URL or DOI"
    full = isinstance(item.get("access"), dict) and item.get("source") and item.get("id")
    if full:
        rec = copy.deepcopy(item)
        rec.pop("verification", None)
        for key, default in _RECORD_DEFAULTS.items():
            if key not in rec:
                rec[key] = copy.deepcopy(default)
        rec.setdefault("title", "")
        rec.setdefault("url", "")
        tier = rec["access"].get("tier")
        if tier not in common.ACCESS_TIERS:
            notes.append("the input access tier %r is not a known tier; set to unknown" % (tier,))
            rec["access"] = {"tier": "unknown", "evidence": ""}
        doi, bad = _clean_doi(rec.get("doi"))
        rec["doi"] = doi
        return rec, notes, bad
    title = item.get("title") or item.get("name") or ""
    url = ""
    for key in ("url", "link", "landing_page", "homepage", "href"):
        if isinstance(item.get(key), str) and item[key].strip():
            url = item[key].strip()
            break
    doi, bad = _clean_doi(item.get("doi"))
    if not doi and _is_doi_url(url):
        doi = _doi_from_doi_url(url)
    if not url and doi:
        url = DOI_RESOLVER + doi
    fields = {}
    for key in ("description", "publisher", "version", "updated"):
        if isinstance(item.get(key), str) and item[key].strip():
            fields[key] = item[key].strip()
    for key in ("creators", "formats", "subjects"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            fields[key] = [value.strip()]
        elif isinstance(value, list):
            fields[key] = [str(x) for x in value if x]
    try:
        if item.get("year") is not None:
            fields["year"] = int(str(item["year"]).strip()[:4])
    except ValueError:
        pass
    rec = common.make_record("manual", doi or url or common.norm_title(title) or "unnamed", str(title), url,
                             doi=doi, **fields)
    claimed = item.get("access") or item.get("access_tier") or item.get("tier")
    if claimed:
        tier = claimed.get("tier") if isinstance(claimed, dict) else claimed
        rec["extra"]["claimed_access"] = str(tier)
        notes.append("the input claimed access %r; that is not evidence, so the tier starts as unknown" % (str(tier),))
    licence = item.get("licence") or item.get("license")
    if licence:
        rec["extra"]["claimed_licence"] = licence if isinstance(licence, str) else (
            licence.get("name") or licence.get("id") if isinstance(licence, dict) else str(licence))
        notes.append("the input claimed a licence; it is kept under extra.claimed_licence until a registry confirms it")
    return rec, notes, bad


def _verify_one(ctx, item):
    rec, input_notes, input_problem = _normalise(item)
    v = _Verdict()
    for note in input_notes:
        v.note(note)
    if not isinstance(item, dict):
        v.fail("invalid_input", input_problem, UNCHECKED)
        return _finish(rec, v)
    url = (rec.get("url") or "").strip()
    doi = rec.get("doi")
    if input_problem:
        v.problem("doi_malformed", "the DOI given is not usable: %s" % input_problem)
    if not doi and _is_doi_url(url):
        doi = _doi_from_doi_url(url)
    if _is_doi_url(url) and not doi:
        v.fail("doi_malformed", "the link %s does not contain a well-formed DOI" % _short(url, 120), NOT_FOUND)
        return _finish(rec, v)
    if not url and not doi:
        if input_problem:
            v.fail("doi_malformed", "the DOI given is not usable: %s" % input_problem, NOT_FOUND)
        else:
            v.fail("no_link", "nothing to check: no URL or DOI was given; find the dataset's landing page first",
                   UNCHECKED)
        return _finish(rec, v)
    given_url = url if url and not _is_doi_url(url) else None

    # 1. A registry that understands the landing page confirms it from its own metadata.
    if given_url:
        adapter = _adapter_for(ctx, given_url)
        if adapter is not None:
            name = getattr(adapter, "NAME", "registry")
            reg = _lookup(ctx, adapter, given_url, v)
            if reg is not None:
                _accept_registry(rec, reg, name, v)
                return _finish(rec, v)
            if not any(n.startswith("the %s registry lookup failed" % name) for n in v.notes):
                v.registry_miss = name
                v.note("the %s registry returned no record for this link; checked the page itself" % name)

    # 2. A DOI: registered or not is decisive evidence.
    if doi:
        res = _resolve_doi(ctx, doi, v)
        if res["state"] == "registered":
            _confirm_by_doi(ctx, rec, doi, res, v, given_url)
            return _finish(rec, v)
        if res["state"] == "not_registered":
            message = ("the DOI %s is not registered at doi.org; a DOI that does not resolve is a strong sign that the "
                       "reference is fabricated or mistyped" % doi)
            if given_url:
                _verify_http(ctx, rec, given_url, v)
                v.problem("doi_not_registered", message)
                if v.verified:
                    rec.setdefault("extra", {})["unregistered_doi"] = doi
                    rec["doi"] = None
                    v.note("the unregistered DOI was moved to extra.unregistered_doi; the dataset itself was "
                           "confirmed at its link")
                else:
                    v.outcome = NOT_FOUND
            else:
                v.method = "doi"
                v.final_url = DOI_RESOLVER + doi
                v.fail("doi_not_registered", message, NOT_FOUND)
            return _finish(rec, v)
        v.note("could not check the DOI: %s" % (res.get("error") or "no answer"))
        if not given_url:
            v.method = "doi"
            v.fail("unreachable", "could not check: doi.org did not confirm or deny the DOI %s (%s)"
                   % (doi, res.get("error") or "no answer"), UNCHECKED)
            return _finish(rec, v)

    # 3. The link itself.
    _verify_http(ctx, rec, given_url, v)
    if v.verified:
        # A DOI in the address or in the page's own metadata can bring registry metadata in.
        candidate = _doi_in_url(given_url) or rec.get("doi")
        if candidate and candidate != doi:
            _enrich_from_doi(ctx, rec, candidate, v)
    elif v.outcome == UNCHECKED:
        embedded = _doi_in_url(given_url)
        if embedded and embedded != doi:
            res = _resolve_doi(ctx, embedded, v)
            if res["state"] == "registered":
                for message in v.problems:
                    v.note("%s; but the DOI in the address is registered" % message)
                v.problems, v.codes, v.outcome = [], [], None
                _confirm_by_doi(ctx, rec, embedded, res, v, None)
    return _finish(rec, v)


def _finish(rec, v):
    if not v.verified and v.registry_miss:
        v.problem("registry_no_record", "the %s registry has no record for this link" % v.registry_miss)
    if v.verified and (rec.get("access") or {}).get("tier", "unknown") == "unknown":
        evidence = (rec.get("access") or {}).get("evidence") or ""
        if evidence:   # a registry gave a reason (a loading script only, an agreement on an "Open" record, ...)
            v.note("access tier unknown (%s); read the landing page before calling the data open" % _short(evidence, 240))
        else:
            v.note("access tier unknown: no registry metadata states it; read the landing page before calling the data open")
    rec["verification"] = v.block()
    return rec


def _verify_safe(ctx, item):
    try:
        return _verify_one(ctx, item)
    except Exception as exc:  # one bad item must not sink the batch; the reason is reported, not hidden
        try:
            rec, _, _ = _normalise(item)
        except Exception:
            rec = common.make_record("manual", "invalid-input", "", "")
        v = _Verdict()
        v.fail("internal_error", "could not check: the verifier failed on this item (%s: %s)"
               % (type(exc).__name__, _short(exc, 160)), UNCHECKED)
        rec["verification"] = v.block()
        return rec


def _interleave(items):
    """Order item indices round-robin across hosts so workers do not queue on one host."""
    queues, order = {}, []
    for i, item in enumerate(items):
        key = "?"
        if isinstance(item, dict):
            url = item.get("url") or item.get("link") or ""
            key = _host_key(url) if isinstance(url, str) and url else ("doi.org" if item.get("doi") else "?")
        if key not in queues:
            queues[key] = []
            order.append(key)
        queues[key].append(i)
    out = []
    while any(queues.values()):
        for key in order:
            if queues[key]:
                out.append(queues[key].pop(0))
    return out


def _summary(records, ctx, seconds):
    by_method, verified_by_method, by_outcome, by_problem = {}, {}, {}, {}
    verified = 0
    for rec in records:
        ver = rec.get("verification") or {}
        method = ver.get("method") or "none"
        by_method[method] = by_method.get(method, 0) + 1
        by_outcome[ver.get("outcome")] = by_outcome.get(ver.get("outcome"), 0) + 1
        if ver.get("verified"):
            verified += 1
            verified_by_method[method] = verified_by_method.get(method, 0) + 1
        for code in ver.get("problem_types") or []:
            by_problem[code] = by_problem.get(code, 0) + 1
    summary = {"total": len(records), "verified": verified, "unverified": len(records) - verified,
               "by_method": by_method, "verified_by_method": verified_by_method, "by_outcome": by_outcome,
               "by_problem": by_problem, "registries": sorted(ctx.sources), "seconds": round(seconds, 1)}
    if ctx.import_errors:
        summary["adapter_import_errors"] = ctx.import_errors
    return summary


def _offline_fix(records):
    """If no site answered at all, DNS failures mean "no network", not "invented host"."""
    for rec in records:
        ver = rec["verification"]
        if "host_not_found" in ver["problem_types"]:
            ver["problem_types"] = ["unreachable" if c == "host_not_found" else c for c in ver["problem_types"]]
            ver["problems"] = ["could not check: no site answered during this run (no network?)"
                               if "does not resolve" in p else p for p in ver["problems"]]
            ver["outcome"] = UNCHECKED


def _worker_count(max_workers):
    """Threads for one run: the caller's number, else MAX_WORKERS, or PROXY_WORKERS behind a proxy
    (DATASET_SCOUT_PARALLEL=1 or =0 overrides, see common.parallel_allowed)."""
    if max_workers:
        return int(max_workers)
    flag = (os.environ.get("DATASET_SCOUT_PARALLEL") or "").strip().lower()
    if flag in ("0", "false", "no", "off"):
        return 1
    return MAX_WORKERS if common.parallel_allowed() else PROXY_WORKERS


def verify_records(records, sources=None, max_workers=None, timeout=TIMEOUT, budget=None):
    """Check that each dataset exists; return {"checked_at", "records", "summary"}.

    `records` are full records (from the adapters) or minimal dicts such as
    {"title": ..., "url": ...} or {"title": ..., "doi": ...}. Each output record
    carries a `verification` block (see docs/SPEC.md). `sources` maps adapter
    NAME to module; it defaults to every adapter that imports cleanly. `budget`
    caps the whole run in seconds (default RUN_BUDGET, or env SCOUT_VERIFY_BUDGET);
    items not reached in time come back as "could not check", never as missing.
    """
    started = time.monotonic()
    if isinstance(records, dict):
        records = records.get("records") or []
    items = list(records or [])
    if sources is None:
        try:
            sources = _sources.load_sources()
        except Exception:  # no adapters at all still leaves the DOI and HTTP checks
            sources = {}
    if budget is None:
        try:
            budget = float(os.environ.get("SCOUT_VERIFY_BUDGET") or RUN_BUDGET)
        except ValueError:
            budget = RUN_BUDGET
    ctx = _Context(sources, timeout, budget)
    results = [None] * len(items)
    if items:
        with ThreadPoolExecutor(max_workers=max(1, min(_worker_count(max_workers), len(items)))) as pool:
            futures = [(i, pool.submit(_verify_safe, ctx, items[i])) for i in _interleave(items)]
            for i, future in futures:
                results[i] = future.result()
    if results and not ctx.any_response:
        _offline_fix(results)
    return {"checked_at": common.now_iso(), "records": results,
            "summary": _summary(results, ctx, time.monotonic() - started)}
