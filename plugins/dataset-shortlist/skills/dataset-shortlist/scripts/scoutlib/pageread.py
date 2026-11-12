"""Read a landing page and pull out what it says about access and licence.

An agent's own fetch tool sometimes cannot read a repository's page, or returns
a summary that leaves out the one sentence that matters: who may download the
data and on what terms. This module fetches the page with the same HTTP layer as
the rest of the skill and prints the sentences that talk about access, so they
can be quoted. It reads; it never decides the access condition by itself.

Standard library only.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser

from scoutlib import common

ACCESS_WORDS = (r"access|licen[cs]e|agreement|\bDUA\b|appl(?:y|ication)|request|credential|regist|sign(?:ed|ing)?\b|"
                r"permission|terms of use|conditions of use|commercial|download|restrict|embargo|approv|"
                r"\bfee\b|\bcost\b|\bpaid\b|subscription|eligib|ethic|\bIRB\b|committee|enclave|training|"
                r"open data|public domain|free of charge|login|log in|account")

_SKIP = {"script", "style", "noscript", "svg", "template", "head"}
_BLOCK = {"p", "div", "li", "tr", "br", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "dd", "dt",
          "td", "th", "blockquote", "pre", "header", "footer", "nav", "ul", "ol", "table"}


class _Text(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.parts = []
        self.title = ""
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag in _SKIP and tag != "head":
            self._skip += 1
        if tag in _BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in _SKIP and tag != "head" and self._skip:
            self._skip -= 1
        if tag in _BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.parts.append(data)


def page_text(html_text):
    """Return (title, visible text with one block per line)."""
    parser = _Text()
    try:
        parser.feed(html_text)
        parser.close()
    except Exception:
        pass   # a malformed page still yields whatever was parsed so far
    lines = []
    for line in "".join(parser.parts).split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return re.sub(r"\s+", " ", parser.title).strip(), lines


def _sentences(line):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", line) if s.strip()]


def read_page(url, find=None, max_matches=24, start_chars=1200):
    """Fetch `url` and return a dict describing what was read.

    `find` is an extra regular expression; sentences matching it are listed
    together with those about access and licence.
    """
    result = {"url": url, "final_url": None, "status": None, "title": "", "matches": [], "start": "",
              "problem": None, "characters": 0}
    try:
        resp = common.http_request(url, timeout=15.0, retries=1,
                                   headers={"Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5"})
    except common.FetchError as exc:
        result["problem"] = "no answer from the site (%s); this is not evidence that the page does not exist" % exc.reason
        return result
    result["status"] = resp.status
    result["final_url"] = resp.url
    if resp.status in (401, 403, 429):
        result["problem"] = ("the site refused an automated client (HTTP %d); the page may exist. Try your own fetch tool, "
                             "the repository's API record, or a web search for the access terms" % resp.status)
        return result
    if not resp.ok:
        result["problem"] = "HTTP %d" % resp.status
        return result
    body = resp.text()
    ctype = resp.header("content-type").lower()
    if "html" in ctype or body.lstrip()[:1] == "<":
        title, lines = page_text(body)
    else:
        title, lines = "", [re.sub(r"\s+", " ", line).strip() for line in body.splitlines() if line.strip()]
    result["title"] = title
    text = " ".join(lines)
    result["characters"] = len(text)
    pattern = re.compile("(?:%s)%s" % (ACCESS_WORDS, ("|(?:%s)" % find) if find else ""), re.I)
    seen = set()
    for line in lines:
        for sentence in _sentences(line):
            if len(sentence) < 25 or len(sentence) > 600:
                continue
            if pattern.search(sentence):
                key = sentence.lower()
                if key not in seen:
                    seen.add(key)
                    result["matches"].append(sentence)
                    if len(result["matches"]) >= max_matches:
                        break
        if len(result["matches"]) >= max_matches:
            break
    result["start"] = common.truncate(text, start_chars)
    if len(text) < 400 and not result["matches"]:
        result["problem"] = ("the page has very little text (%d characters); it is probably drawn by JavaScript, so the "
                             "access terms may not be in what was fetched" % len(text))
    return result


def format_page(result):
    lines = ["page: %s" % result["url"]]
    if result.get("final_url") and result["final_url"] != result["url"]:
        lines.append("redirected to: %s" % result["final_url"])
    if result.get("status"):
        lines.append("status: HTTP %s" % result["status"])
    if result.get("title"):
        lines.append("title: %s" % result["title"])
    if result.get("problem"):
        lines.append("PROBLEM: %s" % result["problem"])
    if result.get("matches"):
        lines.append("")
        lines.append("Sentences about access, licence and terms (quote these, do not paraphrase from memory):")
        for sentence in result["matches"]:
            lines.append("  - %s" % common.truncate(sentence, 420))
    elif not result.get("problem"):
        lines.append("")
        lines.append("No sentence about access or licence was found on this page. Look for a separate access, terms or "
                     "licence page linked from it.")
    if result.get("start"):
        lines.append("")
        lines.append("Start of the page: %s" % result["start"])
    return "\n".join(lines)
