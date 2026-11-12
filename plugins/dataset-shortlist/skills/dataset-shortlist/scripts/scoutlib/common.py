"""Shared helpers for dataset-shortlist.

Standard library only, Python 3.8+. Every source adapter, the verifier, the
literature module and the report renderer import from here so that records,
HTTP behaviour and error handling stay identical across the skill.
"""
from __future__ import annotations

import copy
import html
import http.client
import json
import os
import re
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

__all__ = [
    "USER_AGENT", "ACCESS_TIERS", "canonical_tier", "FetchError", "HttpResponse", "http_request", "transport", "curl_path",
    "get_json", "get_text", "make_record", "normalise_licence", "strip_html",
    "truncate", "norm_title", "norm_doi", "dedupe", "today_iso", "now_iso", "emit",
    "behind_proxy", "parallel_allowed", "Results", "convert_items", "as_year",
]

# A generic client name on purpose: no personal contact details are ever sent.
USER_AGENT = "dataset-shortlist/0.1 (dataset metadata client; python-urllib)"

# How a researcher can actually get the data. Adapters must justify the tier
# they assign with an `evidence` string naming the metadata field they read.
ACCESS_TIERS = {
    "open": "Direct download, no account and no approval.",
    "account": "Free account, login or click-through terms; no human approval.",
    "gated": "Application, credentialing, training or owner approval before access.",
    "controlled": "Institutional agreement, ethics approval, access committee, fee or secure enclave.",
    "closed": "Not obtainable (withdrawn, embargoed without date, metadata only).",
    "unknown": "The registry metadata does not say; must be checked on the landing page.",
}

# Words people write for a tier when they fill in a record by hand, after reading
# a landing page. Only words that state a restriction are listed: nothing here
# maps to "open", so a loose word can never turn a dataset into a free download.
_TIER_WORDS = {
    "account": ("free account", "account required", "registration", "registration required", "registered",
                "register", "login", "log in", "login required", "sign in", "click through", "clickthrough"),
    "gated": ("application", "application required", "apply", "request", "on request", "by request",
              "access request", "restricted", "restricted access", "credentialed", "credentialing",
              "approval", "approval required", "dua", "data use agreement", "agreement"),
    "controlled": ("institutional", "institutional agreement", "institution", "fee", "paid", "licence fee",
                   "license fee", "purchase", "commercial licence", "commercial license", "secure environment",
                   "secure enclave", "enclave", "on site", "onsite", "access committee", "committee",
                   "ethics approval"),
    "closed": ("not obtainable", "unavailable", "not available", "withdrawn", "embargoed", "embargo",
               "metadata only"),
}
_TIER_BY_WORD = {word: tier for tier, words in _TIER_WORDS.items() for word in words}


def canonical_tier(word):
    """Map what a record says about access onto a key of ACCESS_TIERS.

    Returns ``(tier, how)``. ``how`` is "exact" for one of the six keys, "word"
    for a listed word that states a restriction ("application", "registered",
    "fee", ...), "unrecognised" for any other text and "missing" for no text.
    Unrecognised and missing give "unknown"; nothing but the exact word "open"
    gives "open".
    """
    if not isinstance(word, str) or not word.strip():
        return "unknown", "missing"
    text = " ".join(word.strip().lower().replace("_", " ").replace("-", " ").split())
    if text in ACCESS_TIERS:
        return text, "exact"
    if text in _TIER_BY_WORD:
        return _TIER_BY_WORD[text], "word"
    return "unknown", "unrecognised"


MIN_INTERVAL_SECONDS = 0.34  # politeness delay between two calls to one host
_last_call = {}


# Query parameters that carry credentials. They are never echoed into an error message,
# because error messages are printed, written to --out files and read by agents.
_SECRET_RE = re.compile(r"((?<![A-Za-z0-9_])(?:api[_-]?key|apikey|access[_-]?token|token|key)=)[^&\s#\"'<>]+", re.I)


def redact(text):
    """`text` with the values of credential parameters (api_key=..., token=...) replaced."""
    return _SECRET_RE.sub(r"\1REDACTED", str(text)) if text else text


class FetchError(Exception):
    """A request failed (network error, non-2xx where JSON was required, bad JSON).

    `kind` says what went wrong when http_request raised it: "network" (no answer),
    "cut_body" (the host answered but the body was cut short), "invalid_url" (the
    address cannot be requested) or "skipped" (the host failed earlier in this run);
    None otherwise. Credential parameters in the URL and reason are redacted.
    """

    def __init__(self, url, status=None, reason="", kind=None):
        self.url = redact(url)
        self.status = status
        self.reason = redact(reason)
        self.kind = kind
        super().__init__("%s -> %s %s" % (self.url, status if status is not None else "no response", self.reason))


class HttpResponse(object):
    __slots__ = ("status", "url", "headers", "body", "truncated")

    def __init__(self, status, url, headers, body, truncated=False):
        self.status = status
        self.url = url          # final URL after redirects
        self.headers = headers  # dict, keys as sent by the server
        self.body = body        # bytes (possibly truncated at max_bytes)
        self.truncated = truncated  # True when the body was longer than max_bytes and was cut there on purpose

    def header(self, name, default=""):
        lname = name.lower()
        for key, value in self.headers.items():
            if key.lower() == lname:
                return value
        return default

    def text(self):
        ctype = self.header("content-type")
        match = re.search(r"charset=([\w-]+)", ctype or "")
        encoding = match.group(1) if match else "utf-8"
        try:
            return self.body.decode(encoding, errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")

    def json(self):
        return json.loads(self.text())

    @property
    def ok(self):
        return 200 <= self.status < 300


_throttle_lock = threading.Lock()
_host_failures = {}
HOST_FAILURE_LIMIT = 2   # after this many network failures in a row, a host is skipped for the rest of the process
CUT_BODY_RETRIES = 2     # extra tries when a host answers but the body arrives cut short

PROXY_VARIABLES = ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy")


def behind_proxy():
    """True when a proxy environment variable is set (urllib then sends every request through it)."""
    return any(os.environ.get(name) for name in PROXY_VARIABLES)


def parallel_allowed():
    """Whether independent requests may run side by side.

    Some local proxies cut response bodies when several transfers go through them
    at once, so behind a proxy requests run one after another. The environment
    variable DATASET_SCOUT_PARALLEL=1 forces parallel requests, =0 forces sequential.
    """
    flag = (os.environ.get("DATASET_SCOUT_PARALLEL") or "").strip().lower()
    if flag in ("1", "true", "yes", "on"):
        return True
    if flag in ("0", "false", "no", "off"):
        return False
    return not behind_proxy()


def _clean_url(url):
    """Percent-encode what a request line may not carry (spaces, control and non-ASCII characters).

    Existing %-escapes are kept. A typo such as a space then gives an ordinary answer
    from the server (often a 404) instead of a client-side error.
    """
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return url
    netloc = parts.netloc
    if netloc and any(ord(ch) > 127 for ch in netloc):
        try:
            netloc = netloc.encode("idna").decode("ascii")
        except UnicodeError:
            pass
    path = urllib.parse.quote(parts.path, safe="/%:@!$&'()*+,;=~")
    query = urllib.parse.quote(parts.query, safe="=&%:/?@!$'()*+,;~")
    fragment = urllib.parse.quote(parts.fragment, safe="=&%:/?@!$'()*+,;~#")
    return urllib.parse.urlunsplit((parts.scheme, netloc, path, query, fragment))


def _content_length(headers):
    for key, value in headers.items():
        if key.lower() == "content-length":
            value = str(value).strip()
            return int(value) if value.isdigit() else None
    return None


def _throttle(url):
    """Space out calls to one host. Safe when adapters run in threads."""
    host = urllib.parse.urlsplit(url).netloc
    with _throttle_lock:
        now = time.monotonic()
        ready = max(now, _last_call.get(host, 0.0) + MIN_INTERVAL_SECONDS)
        _last_call[host] = ready
    wait = ready - time.monotonic()
    if wait > 0:
        time.sleep(wait)


RETRY_STATUSES = (429, 500, 502, 503, 504)

# ------------------------------------------------------------------ curl transport
#
# Some HTTP proxies hand Python's own client bodies that stop part-way, at random,
# while the same request through curl arrives whole (measured inside a sandboxed
# agent run: 5 of 12 urllib transfers cut, 0 of 5 with curl). So when a proxy is
# configured the tool sends its requests through the curl program if there is
# one, and it falls back to curl whenever urllib receives a cut body. curl is a
# program that ships with macOS, Linux and Windows; no Python package is involved.

_CURL = {}
_CURL_CUT_EXITS = (18, 56, 92)    # partial file, receive failure, stream error: the body did not arrive whole
_CURL_BAD_URL_EXITS = (1, 3)      # unsupported protocol, malformed URL


def curl_path():
    if "path" not in _CURL:
        _CURL["path"] = shutil.which("curl")
    return _CURL["path"]


def transport():
    """'curl' or 'urllib'. DATASET_SCOUT_TRANSPORT=curl|urllib overrides the automatic choice."""
    choice = (os.environ.get("DATASET_SCOUT_TRANSPORT") or "auto").strip().lower()
    if choice == "urllib" or not curl_path():
        return "urllib"
    if choice == "curl":
        return "curl"
    return "curl" if behind_proxy() else "urllib"


def _run_curl(url, hdrs, timeout, method, data, max_bytes):
    """Run curl once. Returns (exit_code, status, final_url, headers, body, truncated, message)."""
    folder = tempfile.mkdtemp(prefix="scout-curl-")
    head_file, body_file = os.path.join(folder, "headers"), os.path.join(folder, "body")
    cmd = [curl_path(), "-sS", "-L", "--compressed", "--max-time", str(max(2, int(timeout + 0.999))),
           "--connect-timeout", str(max(2, min(15, int(timeout)))), "-D", head_file, "-o", body_file,
           "-w", "%{http_code}\n%{url_effective}"]
    if method == "HEAD":
        cmd.append("-I")
    elif method != "GET":
        cmd += ["-X", method]
    for key, value in hdrs.items():
        if key.lower() == "user-agent":
            cmd += ["-A", value]
        else:
            cmd += ["-H", "%s: %s" % (key, value)]
    try:
        if data is not None:
            data_file = os.path.join(folder, "data")
            with open(data_file, "wb") as handle:
                handle.write(data)
            cmd += ["--data-binary", "@" + data_file]
        cmd.append(url)
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout + 15)
            code = proc.returncode
            out = proc.stdout.decode("utf-8", "replace")
            message = proc.stderr.decode("utf-8", "replace").strip()
        except subprocess.TimeoutExpired:
            code, out, message = 28, "000\n" + url, "curl did not finish within %g s" % (timeout + 15)
        lines = out.split("\n")
        try:
            status = int(lines[0].strip() or 0)
        except ValueError:
            status = 0
        final = lines[1].strip() if len(lines) > 1 and lines[1].strip() else url
        headers = {}
        try:
            with open(head_file, encoding="iso-8859-1") as handle:
                block = {}
                for line in handle.read().replace("\r\n", "\n").split("\n"):
                    if line.startswith("HTTP/"):
                        block = {}                     # a redirect or the proxy's own answer came first
                        headers = block
                    elif ":" in line:
                        key, value = line.split(":", 1)
                        block[key.strip()] = value.strip()
        except OSError:
            pass
        body, truncated = b"", False
        if method != "HEAD":
            try:
                with open(body_file, "rb") as handle:
                    body = handle.read(max_bytes)
                    truncated = len(body) >= max_bytes and bool(handle.read(1))
            except OSError:
                pass
        # curl has already undone any compression, so these two headers no longer describe the body
        for name in list(headers):
            if name.lower() in ("content-encoding", "content-length"):
                del headers[name]
        return code, status, final, headers, body, truncated, message
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def _curl_http_request(url, hdrs, timeout, retries, method, data, max_bytes, retry_on, host):
    """The same contract as http_request, with curl doing the transfer."""
    network_tries = status_tries = cut_tries = 0
    cut_limit = CUT_BODY_RETRIES if retries else 0
    while True:
        _throttle(url)
        code, status, final, rheaders, body, truncated, message = _run_curl(url, hdrs, timeout, method, data, max_bytes)
        if code in _CURL_BAD_URL_EXITS:
            raise FetchError(url, None, "invalid address, not requested (curl: %s)" % (message or code), kind="invalid_url")
        if not status:                                   # no HTTP answer at all
            network_tries += 1
            if network_tries <= min(1, retries):
                time.sleep(1.0)
                continue
            _host_failures[host] = _host_failures.get(host, 0) + 1
            raise FetchError(url, None, "no answer (curl exit %s: %s)" % (code, truncate(message, 120)), kind="network")
        _host_failures.pop(host, None)                   # the host answered
        if code != 0:                                    # headers arrived, the body did not arrive whole
            cut_tries += 1
            if cut_tries <= cut_limit:
                time.sleep(0.5 * cut_tries)
                continue
            raise FetchError(url, status, "the answer was cut short %d time%s (curl exit %s); the host did answer, so "
                                          "this is a transfer problem (a busy proxy or network), not a missing record"
                             % (cut_tries, "" if cut_tries == 1 else "s", code), kind="cut_body")
        if status in retry_on and status_tries < retries:
            status_tries += 1
            try:
                delay = float(rheaders.get("Retry-After") or rheaders.get("retry-after") or 1.5 * status_tries)
            except ValueError:
                delay = 1.5 * status_tries
            time.sleep(min(delay, 10.0))
            continue
        return HttpResponse(status, final, rheaders, body, truncated=truncated)



def http_request(url, params=None, headers=None, timeout=20.0, retries=2,
                 method="GET", data=None, max_bytes=4000000, retry_on=RETRY_STATUSES):
    """Fetch a URL and return an HttpResponse for ANY HTTP status.

    Three kinds of trouble are told apart:

    * an HTTP 429 or 5xx answer (the statuses in `retry_on`) is retried up to
      `retries` times with backoff;
    * no answer at all (DNS, connection, TLS, a timeout before the headers) is
      retried once; a host that fails like this twice in a row is skipped for the
      rest of the process, because a host that hangs costs every later call;
    * an answer whose body is cut short (IncompleteRead, fewer bytes than
      Content-Length, a read timeout after the headers) is retried up to
      CUT_BODY_RETRIES more times and never counts against the host, which did
      answer. Busy proxies do this when several transfers run at once.

    An address that cannot be requested (an invalid host or port) raises at once,
    without a retry. Raises FetchError only when no complete answer was obtained.
    """
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        url = url + ("&" if "?" in url else "?") + query
    url = _clean_url(url)
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json, text/html;q=0.8, */*;q=0.5"}
    if headers:
        hdrs.update(headers)
    host = urllib.parse.urlsplit(url).netloc
    if _host_failures.get(host, 0) >= HOST_FAILURE_LIMIT:
        raise FetchError(url, None, "skipped: %s did not answer %d times in a row earlier in this run" % (
            host, _host_failures[host]), kind="skipped")
    if transport() == "curl":
        return _curl_http_request(url, hdrs, timeout, retries, method, data, max_bytes, retry_on, host)
    network_tries = 0
    status_tries = 0
    cut_tries = 0
    cut_limit = CUT_BODY_RETRIES if retries else 0
    while True:
        _throttle(url)
        try:
            request = urllib.request.Request(url, data=data, headers=hdrs, method=method)
            resp = urllib.request.urlopen(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            if exc.code in retry_on and status_tries < retries:
                status_tries += 1
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    delay = float(retry_after) if retry_after else 1.5 * status_tries
                except ValueError:
                    delay = 1.5 * status_tries
                time.sleep(min(delay, 10.0))
                continue
            try:
                body = exc.read(max_bytes) if method != "HEAD" else b""
            except Exception:
                body = b""
            hdr = dict(exc.headers.items()) if exc.headers else {}
            _host_failures.pop(host, None)       # the host answered, even if with an error status
            return HttpResponse(exc.code, exc.geturl() or url, hdr, body)
        except (ValueError, http.client.InvalidURL) as exc:
            # Deterministic: asking again cannot help, and the host is not to blame.
            raise FetchError(url, None, "invalid address, not requested (%s: %s)" % (type(exc).__name__, exc),
                             kind="invalid_url")
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError,
                http.client.HTTPException, ssl.SSLError) as exc:
            network_tries += 1
            if network_tries <= min(1, retries):   # one retry: a host that hangs twice is not coming back soon
                time.sleep(1.0)
                continue
            _host_failures[host] = _host_failures.get(host, 0) + 1
            raise FetchError(url, None, "%s: %s" % (type(exc).__name__, exc), kind="network")
        # The headers arrived, so the host answered; what follows is about the transfer of the body.
        _host_failures.pop(host, None)
        status, final, rheaders = resp.status, resp.geturl(), dict(resp.headers.items())
        cut = None
        body, truncated = b"", False
        try:
            with resp:
                if method != "HEAD":
                    body = resp.read(max_bytes)
                    truncated = len(body) >= max_bytes and bool(resp.read(1))
        except http.client.IncompleteRead as exc:
            cut = "IncompleteRead, %d bytes received" % len(exc.partial or b"")
        except (socket.timeout, TimeoutError):
            cut = "no more data within %g s after the headers" % timeout
        except (ConnectionError, http.client.HTTPException, ssl.SSLError, OSError) as exc:
            cut = "%s: %s" % (type(exc).__name__, exc)
        else:
            length = _content_length(rheaders)
            if method != "HEAD" and not truncated and length is not None and len(body) < length:
                cut = "%d of %d bytes received" % (len(body), length)
        if cut is None:
            return HttpResponse(status, final, rheaders, body, truncated=truncated)
        cut_tries += 1
        if cut_tries <= cut_limit:
            time.sleep(0.5 * cut_tries)
            continue
        if curl_path() and (os.environ.get("DATASET_SCOUT_TRANSPORT") or "auto").strip().lower() != "urllib":
            # Python's client keeps getting a cut body; curl often gets the same answer whole.
            return _curl_http_request(url, hdrs, timeout, min(retries, 1), method, data, max_bytes, retry_on, host)
        raise FetchError(url, status, "the answer was cut short %d time%s (%s); the host did answer, so this is a "
                                      "transfer problem (a busy proxy or network), not a missing record"
                         % (cut_tries, "" if cut_tries == 1 else "s", cut), kind="cut_body")


JSON_TRIES = 3          # a 2xx body that does not parse is usually a transfer cut short
JSON_MAX_BYTES = 4000000


def get_json(url, params=None, headers=None, timeout=20.0, retries=2, method="GET", data=None):
    """GET (or POST) a JSON document. Raises FetchError on non-2xx or invalid JSON.

    A 2xx answer whose body does not parse (a transfer cut short that the HTTP
    layer could not detect) is requested again, up to JSON_TRIES times in all, with
    a short growing pause. A body larger than JSON_MAX_BYTES is reported as such.
    """
    problem = None
    for attempt in range(JSON_TRIES):
        if attempt:
            time.sleep(0.5 * attempt)
        resp = http_request(url, params=params, headers=headers, timeout=timeout,
                            retries=retries, method=method, data=data, max_bytes=JSON_MAX_BYTES)
        if not resp.ok:
            raise FetchError(resp.url, resp.status, truncate(resp.text(), 200))
        if getattr(resp, "truncated", False):
            raise FetchError(resp.url, resp.status, "the response is larger than %d bytes, the most this client reads; "
                                                    "it was not parsed" % JSON_MAX_BYTES)
        try:
            return resp.json()
        except ValueError as exc:
            problem = FetchError(resp.url, resp.status, "invalid JSON after %d tries: %s" % (attempt + 1, exc))
    raise problem


def get_text(url, params=None, headers=None, timeout=20.0, retries=2):
    """GET a text document. Raises FetchError on non-2xx."""
    resp = http_request(url, params=params, headers=headers, timeout=timeout, retries=retries)
    if not resp.ok:
        raise FetchError(resp.url, resp.status, truncate(resp.text(), 200))
    return resp.text()


# --------------------------------------------------------------------------- text

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def strip_html(text):
    if not text:
        return ""
    return _WS_RE.sub(" ", html.unescape(_TAG_RE.sub(" ", str(text)))).strip()


def truncate(text, limit=700):
    text = _WS_RE.sub(" ", str(text or "")).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def norm_title(title):
    """Lower-case alphanumeric key used to spot the same dataset in two registries."""
    return re.sub(r"[^a-z0-9]+", " ", str(title or "").lower()).strip()


def norm_doi(doi):
    if not doi:
        return None
    doi = str(doi).strip()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi, flags=re.I)
    return doi.lower() or None


def today_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ----------------------------------------------------------------------- licences

_NC_RE = re.compile(r"non[-\s]?commercial|research[-\s]use[-\s]only|academic[-\s]use[-\s]only|"
                    r"not[-\s]for[-\s]commercial|no[-\s]commercial", re.I)
_CC_URL_RE = re.compile(r"creativecommons\.org/licen[cs]es/(by(?:-nc)?(?:-nd|-sa)?)/(\d\.\d)")
_CC_CODE_RE = re.compile(r"(?<![a-z])cc-?(by(?:-nc)?(?:-nd|-sa)?)(?:-(\d\.\d))?(?![a-z])")
_VERSION_RE = re.compile(r"(\d\.\d)")


def _cc(code, version, name, url):
    lic_id = "CC-%s-%s" % (code.upper(), version or "4.0")
    return {"id": lic_id, "name": name or lic_id, "url": url,
            "commercial_use": "nc" not in code.split("-"), "share_alike": "sa" in code.split("-")}


def _candidates(text, compact):
    """Every licence the text names: (id, commercial_use, share_alike)."""
    found = []

    def add(lic_id, commercial, share_alike):
        if lic_id not in [f[0] for f in found]:
            found.append((lic_id, commercial, share_alike))

    if re.search(r"(?<![a-z])cc-?0(?![0-9a-z])|cc-zero|creative-?commons-zero|publicdomain/zero|public-domain-dedication", compact):
        add("CC0-1.0", True, False)
    for match in _CC_URL_RE.finditer(text):
        code = match.group(1)
        add("CC-%s-%s" % (code.upper(), match.group(2)), "nc" not in code.split("-"), "sa" in code.split("-"))
    for match in _CC_CODE_RE.finditer(compact):
        code = match.group(1)
        version = match.group(2)
        if not version:
            after = _VERSION_RE.match(compact[match.end():].lstrip("-v"))
            version = after.group(1) if after else "4.0"
        add("CC-%s-%s" % (code.upper(), version), "nc" not in code.split("-"), "sa" in code.split("-"))
    if not any(f[0].startswith("CC-BY") for f in found) and "attribution" in compact and (
            "creative-commons" in compact or "creativecommons" in compact or compact.startswith("attribution")):
        parts = ["by"]
        if re.search(r"attribution-non-?commercial", compact):      # part of the licence name, not a separate clause
            parts.append("nc")
        if "noderiv" in compact or "no-deriv" in compact:
            parts.append("nd")
        elif "sharealike" in compact or "share-alike" in compact:
            parts.append("sa")
        after = _VERSION_RE.search(compact[compact.index("attribution"):])
        add("CC-%s-%s" % ("-".join(parts).upper(), after.group(1) if after else "4.0"), "nc" not in parts, "sa" in parts)
    if re.search(r"odbl|open-database-licen[cs]e", compact):
        add("ODbL-1.0", True, True)
    if re.search(r"odc-by|open-data-commons-attribution", compact):
        add("ODC-By-1.0", True, False)
    if re.search(r"pddl|open-data-commons-public-domain", compact):
        add("PDDL-1.0", True, False)
    if "public-domain-mark" in compact:
        add("PDM-1.0", True, False)
    if re.search(r"cdla-permissive", compact):
        add("CDLA-Permissive-2.0" if "2.0" in compact else "CDLA-Permissive-1.0", True, False)
    if re.search(r"cdla-sharing", compact):
        add("CDLA-Sharing-1.0", True, True)
    if re.search(r"(?<![a-z])apache(-licen[cs]e)?(-version)?-?2|(?<![a-z])apache-?2|^apache(-licen[cs]e)?$", compact):
        add("Apache-2.0", True, False)
    # "MIT" only as a licence name, never as a word inside other terms (it is also an institution).
    if re.search(r"^mit$|^mit-licen[cs]e|(?<![a-z])mit-licen[cs]e(?![a-z])|licenses/mit(?![a-z])|^mit-(?:0|no-attribution)$", compact):
        add("MIT", True, False)
    match = re.search(r"(?<![a-z])bsd-?([23])", compact)
    if match:
        add("BSD-%s-Clause" % match.group(1), True, False)
    elif re.search(r"^bsd(-licen[cs]e)?$", compact):
        add("BSD-3-Clause", True, False)
    match = re.search(r"(?<![a-z])(a|l)?gpl-?v?-?([23])|gnu-(affero-|lesser-)?general-public-licen[cs]e-?v?-?([23])?", compact)
    if match:
        prefix = (match.group(1) or "").upper()
        if not prefix and match.group(3):
            prefix = "A" if match.group(3).startswith("affero") else "L"
        version = match.group(2) or match.group(4) or "3"
        add("%sGPL-%s.0" % (prefix, version), True, True)
    return found


def normalise_licence(name=None, url=None):
    """Map a free-text licence name or URL to a small structured description.

    Returns None when nothing was given. `id` is None when the text is not one
    recognisable open licence: a custom agreement, an uploader's "other", or text
    that names more than one licence. In that case the original text stays in
    `name` and has to be read by a person. `commercial_use` is True only when the
    licence allows it and nothing in the text restricts it; any mention of
    non-commercial or research-only use makes it False.
    """
    if not name and not url:
        return None
    text = ("%s %s" % (name or "", url or "")).strip().lower()
    compact = re.sub(r"[\s_]+", "-", text)
    found = _candidates(text, compact)
    restricted = bool(_NC_RE.search(text))
    if len(found) == 1:
        lic_id, commercial, share_alike = found[0]
        if restricted and commercial:
            # an open licence plus a restriction in the same text: custom terms, not the open licence
            return {"id": None, "name": name or url, "url": url, "commercial_use": False, "share_alike": None}
        return {"id": lic_id, "name": name or lic_id, "url": url, "commercial_use": commercial, "share_alike": share_alike}
    if len(found) > 1:
        # several licences in one statement (code under one, data under another): do not pick
        commercial = False if (restricted or any(f[1] is False for f in found)) else None
        return {"id": None, "name": name or url, "url": url, "commercial_use": commercial, "share_alike": None}
    return {"id": None, "name": name or url, "url": url, "commercial_use": False if restricted else None,
            "share_alike": None}


# ------------------------------------------------------------------------ records

class Results(list):
    """A list of records that also says how many raw items had to be skipped."""
    skipped = 0


def convert_items(items, convert, where):
    """Turn raw registry items into records, skipping malformed ones.

    One item with an unexpected null must not lose every result of a registry, so
    items that raise TypeError, AttributeError, KeyError or ValueError are skipped
    and counted in `Results.skipped`. `convert` may return None for an item that is
    not a record (no title, say). When every item is malformed, FetchError is raised:
    an empty list would hide the failure.
    """
    out = Results()
    items = list(items or [])
    for item in items:
        try:
            if not isinstance(item, dict):
                raise TypeError("not an object")
            rec = convert(item)
        except (TypeError, AttributeError, KeyError, ValueError):
            out.skipped += 1
            continue
        if rec:
            out.append(rec)
    if items and out.skipped == len(items):
        raise FetchError(where, None, "all %d items in the response were malformed" % len(items))
    return out


def as_year(value):
    """An int year from 2021, "2021" or "2021-05-03"; None otherwise."""
    text = str(value or "").strip()
    return int(text[:4]) if re.match(r"^\d{4}", text) else None


_RECORD_DEFAULTS = {
    "description": "", "doi": None, "publisher": None, "creators": [], "year": None,
    "version": None, "updated": None, "licence": None, "size": None, "formats": [],
    "subjects": [], "usage": {}, "extra": {},
}


def make_record(source, id, title, url, access_tier="unknown", access_evidence="", **fields):
    """Build one dataset record in the common schema (see docs/SPEC.md).

    `access_tier` must be a key of ACCESS_TIERS and `access_evidence` must name
    the metadata field or page text that justifies it. Use "unknown" rather
    than guessing: a wrong "open" sends a researcher down a dead end.
    """
    if access_tier not in ACCESS_TIERS:
        raise ValueError("unknown access tier %r" % (access_tier,))
    unknown = set(fields) - set(_RECORD_DEFAULTS)
    if unknown:
        raise ValueError("unknown record fields: %s" % ", ".join(sorted(unknown)))
    record = {
        "id": "%s:%s" % (source, id),
        "source": source,
        "title": truncate(strip_html(title), 300),
        "url": url,
        "access": {"tier": access_tier, "evidence": str(access_evidence or "")},
        "retrieved_at": today_iso(),
    }
    for key, default in _RECORD_DEFAULTS.items():
        value = fields.get(key)
        if value is None:
            value = copy.deepcopy(default)   # a fresh list or dict for every record, never the shared default
        if key == "description":
            value = truncate(strip_html(value), 700)
        elif key == "doi":
            value = norm_doi(value)
        elif key == "creators":
            value = [str(c) for c in (value or [])][:5]
        elif key in ("formats", "subjects"):
            value = [str(v) for v in (value or [])][:12]
        record[key] = value
    return record


# ------------------------------------------------------------------------- dedupe

HOST_SOURCES = ("zenodo", "physionet", "huggingface")   # registries that hold the files themselves
_TIER_ORDER = {"open": 0, "account": 1, "gated": 2, "controlled": 3, "closed": 4}
_GENERIC_TITLE = re.compile(r"^(data|dataset|datasets|data set|supplementary (data|material|materials|information)|"
                            r"additional file \d+.*|data sheet \d+.*|table \d+.*|raw data|source data|untitled)$")


def _all_dois(rec):
    extra = rec.get("extra") or {}
    values = [rec.get("doi"), extra.get("project_doi"), extra.get("concept_doi"), extra.get("version_doi")]
    values.extend(extra.get("all_dois") or [])
    return {d for d in (norm_doi(v) for v in values) if d}


def _url_key(rec):
    """The landing page without scheme, "www.", fragment or trailing slash; None for a home page or a DOI link."""
    url = str(rec.get("url") or "").strip()
    if not url:
        return None
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return None
    host = parts.netloc.lower()
    host = host[4:] if host.startswith("www.") else host
    path = (parts.path or "").rstrip("/")
    if not host or not path or host in ("doi.org", "dx.doi.org"):
        return None      # a home page names no dataset; DOI links are matched by DOI
    return "%s%s%s" % (host, path, "?" + parts.query if parts.query else "")


def _title_key(rec):
    key = norm_title(rec.get("title"))
    if len(key) < 15 or _GENERIC_TITLE.match(key):
        return None      # "Dataset", "Supplementary data": too generic to mean the same thing twice
    return "%s|%s" % (key, norm_title(rec.get("publisher")))


def dedupe(records):
    """Merge records that describe the same dataset.

    Two records are the same when they share any DOI (version, concept or project
    DOI), or when neither carries a DOI that contradicts the other and they have
    the same landing page, or the same specific title and publisher. A record met
    again under its own id (a later search, a second `add`) is not listed as a copy
    of itself; its empty fields are filled from the newer copy. The record from the
    registry that hosts the files is kept as the main one; the others are listed
    in `also_found_in`. When the copies disagree about access, the host's
    statement wins, otherwise the more restrictive one, and the disagreement is
    kept in `extra.access_conflicts`.
    """
    out = []
    by_doi = {}
    by_title = {}
    by_url = {}
    by_id = {}
    for rec in records:
        rec = copy.deepcopy(rec)
        rec.setdefault("also_found_in", [])
        dois = _all_dois(rec)
        title_key = _title_key(rec)
        url_key = _url_key(rec)
        same = by_id.get(rec.get("id")) if rec.get("id") else None
        if same is not None:
            # The same record again (a later search found it, or it was added twice): not a copy of itself.
            for key, value in rec.items():
                if key != "also_found_in" and value not in (None, "", [], {}) and same.get(key) in (None, "", [], {}):
                    same[key] = value
            continue
        hit = next((by_doi[d] for d in dois if d in by_doi), None)
        for index, key in ((by_url, url_key), (by_title, title_key)):
            if hit is None and key and key in index:
                other = index[key]
                if not (dois and _all_dois(other)):      # two different DOIs: different datasets
                    hit = other
        if hit is None:
            out.append(rec)
        else:
            main, extra_rec = hit, rec
            if hit.get("source") not in HOST_SOURCES and rec.get("source") in HOST_SOURCES:
                position = next(i for i, item in enumerate(out) if item is hit)
                rec["also_found_in"] = hit.get("also_found_in", [])
                out[position] = rec
                for key, value in list(by_doi.items()):
                    if value is hit:
                        by_doi[key] = rec
                for index in (by_title, by_url, by_id):
                    for key, value in list(index.items()):
                        if value is hit:
                            index[key] = rec
                main, extra_rec = rec, hit
            main["also_found_in"].append({"source": extra_rec.get("source"), "id": extra_rec.get("id"),
                                          "url": extra_rec.get("url")})
            a, b = (main.get("access") or {}), (extra_rec.get("access") or {})
            ta, tb = a.get("tier", "unknown"), b.get("tier", "unknown")
            if not isinstance(main.get("extra"), dict):
                main["extra"] = {}
            conflicts = main["extra"].setdefault("access_conflicts", [])
            if ta == "unknown" and tb != "unknown":
                if main.get("source") in HOST_SOURCES and tb in ("open", "account"):
                    # the host holds the data and does not say this; a permissive claim from elsewhere is not enough
                    conflicts.append({"source": extra_rec.get("source"), "tier": tb, "evidence": b.get("evidence", "")})
                else:
                    main["access"] = dict(b)
            elif tb != "unknown" and ta != tb:
                conflicts.append({"source": extra_rec.get("source"), "tier": tb, "evidence": b.get("evidence", "")})
                if main.get("source") not in HOST_SOURCES and _TIER_ORDER.get(tb, -1) > _TIER_ORDER.get(ta, -1):
                    conflicts.append({"source": main.get("source"), "tier": ta, "evidence": a.get("evidence", "")})
                    main["access"] = dict(b)       # no host among them: keep the more restrictive claim
            if not conflicts:
                main["extra"].pop("access_conflicts")
            if not main.get("licence") and extra_rec.get("licence"):
                main["licence"] = extra_rec["licence"]
            rec = main
        for doi in _all_dois(rec) | dois:
            by_doi.setdefault(doi, rec)
        if title_key:
            by_title.setdefault(title_key, rec)
        if url_key:
            by_url.setdefault(url_key, rec)
        by_id.setdefault(rec.get("id"), rec)
        for other in rec.get("also_found_in") or []:
            if other.get("id"):
                by_id.setdefault(other["id"], rec)
    return out


def emit(obj, out=None):
    """Write JSON to a file, or to stdout when `out` is None."""
    text = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False)
    if out:
        import os

        folder = os.path.dirname(os.path.abspath(out))
        os.makedirs(folder, exist_ok=True)  # e.g. dataset-shortlist/ on the first search of a session
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    else:
        sys.stdout.write(text + "\n")
