"""Tests for scoutlib.render: shortlist JSON -> one self-contained, interactive HTML page.

Offline. The Python side only embeds the shortlist in a template, so string
checks on the output cannot prove that the page works. Two further layers do:

* when a ``node`` binary is on PATH, the page's own script is extracted from a
  rendered file, syntax-checked and its pure functions (normalisation, link
  safety, filtering, the Markdown plan) are exercised;
* with ``SCOUT_BROWSER=1`` and Chrome or Chromium installed, a hostile shortlist
  is rendered, opened headless and the resulting DOM is inspected.

The datasets in tests/fixtures/render/ are invented.
"""
from __future__ import annotations

import base64
import collections
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser

import pytest

from scoutlib import common, render

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOUT = os.path.join(REPO, "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts", "scout.py")
FIXTURES = os.path.join(REPO, "tests", "fixtures", "render")
SAMPLE = os.path.join(REPO, "docs", "examples", "sample-report.html")

DATA_OPEN = '<script type="application/json" id="scout-data">'
XSS_SCRIPT = "</script><script>alert(1)</script>"
XSS_IMG = "<img onerror=alert(1) src=x>"
XSS = "Evil %s %s dataset" % (XSS_SCRIPT, XSS_IMG)
BAD_URLS = ["javascript:alert(1)", "JaVaScRiPt:alert(1)", " javascript:alert(1)",
            "data:text/html,<script>alert(1)</script>", "vbscript:msgbox(1)"]


# ------------------------------------------------------------------ helpers

class Page(HTMLParser):
    """The parts of a rendered page the tests look at."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.tags = []        # (tag, {attribute: value})
        self.scripts = []     # ({attribute: value}, text)
        self.styles = []      # text of every <style>
        self.title = ""
        self._open = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script":
            self.scripts.append((attrs, ""))
        elif tag == "style":
            self.styles.append("")
        if tag in ("script", "style", "title"):
            self._open = tag

    def handle_endtag(self, tag):
        if tag == self._open:
            self._open = None

    def handle_data(self, data):
        if self._open == "script":
            attrs, text = self.scripts[-1]
            self.scripts[-1] = (attrs, text + data)
        elif self._open == "style":
            self.styles[-1] += data
        elif self._open == "title":
            self.title += data

    def named(self, name):
        return [attrs for tag, attrs in self.tags if tag == name]

    @property
    def code(self):
        """Text of the executable scripts (the data block has a type)."""
        return [text for attrs, text in self.scripts if "type" not in attrs]


def parse(text):
    page = Page()
    page.feed(text)
    page.close()
    return page


def split_data(text):
    """(page without the data block, text of the data block)."""
    start = text.index(DATA_OPEN) + len(DATA_OPEN)
    end = text.index("</script>", start)
    return text[:start] + text[end:], text[start:end]


def embedded(text):
    return json.loads(split_data(text)[1])


def load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as handle:
        return json.load(handle)


def hostile():
    """The full fixture with markup in every text field and a script URL in every link."""
    data = load("shortlist_full.json")
    data["question"] = "Why %s?" % XSS
    data["notes"] = XSS
    data["gaps"] = [XSS]
    data["requirements"][0]["text"] = XSS
    data["requirements"].append({"id": XSS, "text": "id made of markup", "must": True})
    data["searched"]["sources"] = [XSS]
    data["searched"]["queries"] = [XSS]
    data["not_recommended"] = [{"name": XSS, "url": BAD_URLS[1], "reason": XSS}]
    for index, entry in enumerate(data["datasets"]):
        record = entry["record"]
        record["title"] = XSS
        record["url"] = BAD_URLS[index % len(BAD_URLS)]
        record["description"] = XSS
        record["publisher"] = XSS
        record["creators"] = [XSS]
        record["version"] = XSS
        record["doi"] = "10.5555/%s" % XSS
        record["formats"] = [XSS]
        record["subjects"] = [XSS]
        record["access"]["evidence"] = XSS
        record["licence"] = {"id": None, "name": XSS, "url": BAD_URLS[0], "commercial_use": True}
        record["size"] = {"text": XSS}
        record["also_found_in"] = [{"source": XSS, "url": BAD_URLS[3]}]
        record["verification"]["method"] = XSS
        record["verification"]["final_url"] = BAD_URLS[2]
        record["verification"]["problems"] = [XSS]
        record["verification"]["notes"] = [XSS]
        entry["why"] = XSS
        entry["access_steps"] = [XSS, "two\nlines [x](javascript:alert(1))"]
        entry["caveats"] = [XSS]
        entry["requirements"] = {"R1": {"status": "met", "evidence": XSS, "url": BAD_URLS[0]},
                                 XSS: {"status": "partial", "evidence": XSS, "url": BAD_URLS[4]}}
        entry["papers"] = [{"title": XSS, "year": XSS, "doi": XSS, "url": BAD_URLS[0], "note": XSS}]
    return data


# ------------------------------------------------------- rendering both fixtures

@pytest.mark.parametrize("name, n_datasets", [("shortlist_full.json", 6), ("shortlist_minimal.json", 1)])
def test_fixture_renders(tmp_path, name, n_datasets):
    shortlist = load(name)
    out = tmp_path / "report.html"
    path = render.render_report(shortlist, str(out))

    assert path == str(out) and os.path.isabs(path) and os.path.isfile(path)
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    assert text.startswith("<!DOCTYPE html>") and text.rstrip().endswith("</html>")
    assert "__SCOUT_" not in split_data(text)[0], "a placeholder was left in the page"
    assert embedded(text) == shortlist, "the page must carry the shortlist unchanged"
    assert len(embedded(text)["datasets"]) == n_datasets

    page = parse(text)
    assert page.title.startswith("Dataset shortlist")
    assert len(page.scripts) == 2 and len(page.code) == 1
    assert [attrs.get("lang") for attrs in page.named("html")] == ["en"]
    assert any(attrs.get("name") == "viewport" for attrs in page.named("meta"))


def test_full_fixture_title_is_the_shortened_question():
    page = parse(render.render_html(load("shortlist_full.json")))
    assert page.title == ("Dataset shortlist: I want to study how the shift to remote work "
                          "changed commuting patterns\u2026")


def test_title_without_a_question_and_with_a_long_one():
    assert parse(render.render_html({})).title == "Dataset shortlist"
    assert parse(render.render_html({"question": "  Tides \n and   eels?  "})).title == \
        "Dataset shortlist: Tides and eels?"
    title = parse(render.render_html({"question": "word " * 200})).title
    assert title.endswith("word\u2026") and len(title) <= len("Dataset shortlist: ") + 73


def test_returned_path_is_absolute_and_template_is_found_from_any_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)                       # not the repository, not the skill
    path = render.render_report(load("shortlist_minimal.json"), os.path.join("deep", "er", "report.html"))
    assert os.path.isabs(path) and os.path.isfile(path)
    assert os.path.realpath(path) == os.path.realpath(str(tmp_path / "deep" / "er" / "report.html"))
    assert os.path.isfile(render.TEMPLATE_PATH) and os.path.isabs(render.TEMPLATE_PATH)


def test_rendering_is_deterministic_and_does_not_change_its_input():
    shortlist = load("shortlist_full.json")
    before = copy.deepcopy(shortlist)
    assert render.render_html(shortlist) == render.render_html(shortlist)
    assert shortlist == before


def test_rejects_something_that_is_not_a_shortlist_object(tmp_path):
    for bad in (None, [], "text", 3):
        with pytest.raises(TypeError):
            render.render_html(bad)
    with pytest.raises(ValueError):
        render.render_report({}, "")


# ------------------------------------------------------------- self-contained

def test_page_loads_nothing_from_outside():
    text = render.render_html(load("shortlist_full.json"))
    page = parse(text)

    for tag, attrs in page.tags:
        assert "src" not in attrs, "<%s src=...> would load a resource" % tag
        assert "srcset" not in attrs and "background" not in attrs and "poster" not in attrs
        if tag != "a":
            assert not re.match(r"\s*(https?:)?//", attrs.get("href", "")), (tag, attrs)
        assert "url(" not in attrs.get("style", "")
    for banned in ("link", "img", "iframe", "frame", "object", "embed", "video", "audio",
                   "source", "track", "base", "applet"):
        assert not page.named(banned), "<%s> is not allowed in the page" % banned
    assert not [attrs for attrs in page.named("form") if "action" in attrs]
    assert not [attrs for attrs in page.named("meta") if attrs.get("http-equiv", "").lower() == "refresh"]

    assert page.styles, "the stylesheet must be inline"
    for css in page.styles:
        assert "url(" not in css.lower() and "@import" not in css.lower()
        assert "http://" not in css and "https://" not in css

    assert len(page.code) == 1
    script = page.code[0]
    for call in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon",
                 "importScripts", "import(", "new Image", "serviceWorker", ".src ="):
        assert call not in script, "%s could reach the network" % call

    # Every link that is in the markup itself leads to a web page or to this page.
    for attrs in page.named("a"):
        assert re.match(r"(https?://|#)", attrs["href"]), attrs


def test_template_names_no_web_address_except_the_doi_resolver():
    with open(render.TEMPLATE_PATH, encoding="utf-8") as handle:
        template = handle.read()
    assert set(re.findall(r"https?://[^\s'\"<>)]*", template)) == {"https://doi.org/"}
    assert not re.search(r"""(src|href)\s*=\s*["']?\s*(https?:)?//""", template)


def test_policy_allows_only_the_page_script_by_hash():
    text = render.render_html(load("shortlist_full.json"))
    page = parse(text)
    policies = [attrs["content"] for attrs in page.named("meta")
                if attrs.get("http-equiv") == "Content-Security-Policy"]
    assert len(policies) == 1
    directives = dict(part.strip().split(" ", 1) for part in policies[0].split(";"))
    assert directives["default-src"] == "'none'"
    assert directives["base-uri"] == "'none'" and directives["form-action"] == "'none'"

    digest = hashlib.sha256(page.code[0].encode("utf-8")).digest()
    assert directives["script-src"] == "'sha256-%s'" % base64.b64encode(digest).decode("ascii")
    # The policy must come before anything it governs.
    assert text.index("Content-Security-Policy") < text.index("<style") < text.index("<script")


def test_page_script_can_be_inlined_and_never_parses_text_as_markup():
    script = parse(render.render_html(load("shortlist_full.json"))).code[0]
    script.encode("ascii")                     # the hash must not depend on an encoding
    assert "\r" not in script
    for sequence in ("</script", "<!--", "<script"):
        assert sequence not in script.lower()
    for sink in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(",
                 "new Function", "srcdoc", "DOMParser", "createContextualFragment", "setTimeout('",
                 "javascript:"):
        assert sink not in script, "%s must not be used in the page script" % sink
    assert "textContent" in script and "createElement" in script and "createTextNode" in script
    # The only values ever written to an href: a checked http(s) address, an
    # in-page anchor and the blob of the plan download.
    assert sorted({value.strip() for value in re.findall(r"\bhref: ([^,}]+)", script)}) == [
        "'#' + cardId(ds)", "address", "href"]
    assert ".href =" not in script and "['href']" not in script
    # Attribute names are fixed words of the script, except inside el(), whose
    # callers pass literal names only.
    assert set(re.findall(r"setAttribute\(([^,]+),", script)) == {
        "name", "'datetime'", "'aria-expanded'", "'data-scout'"}


# -------------------------------------------------------------- untrusted text

def test_markup_in_dataset_text_appears_only_in_escaped_form():
    shortlist = hostile()
    text = render.render_html(shortlist)
    outside, block = split_data(text)

    # In the data block: no character that could end or open an element.
    assert not set("<>&") & set(block)
    assert "\\u003c/script\\u003e\\u003cscript\\u003ealert(1)\\u003c/script\\u003e" in block
    assert "\\u003cimg onerror=alert(1) src=x\\u003e" in block
    assert json.loads(block) == shortlist

    # Outside it (title and the no-JavaScript list): entity-escaped, never raw.
    assert XSS_SCRIPT not in text and XSS_IMG not in text
    assert "<script>alert" not in text and "<img" not in text.lower()
    assert "&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;" in outside
    assert "&lt;img onerror=alert(1) src=x&gt;" in outside

    page = parse(text)
    assert len(page.scripts) == 2 and len(page.code) == 1, "the payload created a script element"
    assert not page.named("img")
    assert all(not name.startswith("on") for _, attrs in page.tags for name in attrs)
    # The payload added no element at all: the page has exactly the elements of
    # the same shortlist with harmless text (links aside: unsafe ones are dropped).
    harmless = json.loads(json.dumps(shortlist).replace(json.dumps(XSS)[1:-1], "Plain"))
    assert XSS not in json.dumps(harmless)
    expected = collections.Counter(tag for tag, _ in parse(render.render_html(harmless)).tags if tag != "a")
    assert collections.Counter(tag for tag, _ in page.tags if tag != "a") == expected
    assert page.title.startswith("Dataset shortlist: Why Evil </script><script>alert(1)</script>")
    # The script that runs is the template's, byte for byte.
    assert page.code == parse(render.render_html({})).code


def test_hostile_question_cannot_leave_the_title():
    text = render.render_html({"question": "</title><script>alert(1)</script><title>"})
    page = parse(text)
    assert len(page.scripts) == 2 and len(page.named("title")) == 1
    assert page.title == "Dataset shortlist: </title><script>alert(1)</script><title>"
    assert "<title>Dataset shortlist: &lt;/title&gt;&lt;script&gt;" in text


def test_placeholder_text_in_a_shortlist_is_not_substituted_again():
    shortlist = {"question": "__SCOUT_DATA__ and __SCOUT_TITLE__",
                 "datasets": [{"record": {"title": "__SCOUT_FALLBACK__ __SCOUT_CSP_SCRIPT__"}}]}
    text = render.render_html(shortlist)
    assert embedded(text) == shortlist
    assert parse(text).title == "Dataset shortlist: __SCOUT_DATA__ and __SCOUT_TITLE__"
    assert text.count(DATA_OPEN) == 1


def test_javascript_url_is_not_turned_into_a_link():
    shortlist = hostile()
    text = render.render_html(shortlist)
    outside, _ = split_data(text)
    page = parse(text)

    assert page.named("a"), "the page has links of its own to check"
    for attrs in page.named("a"):
        assert re.match(r"(https?://|#)", attrs["href"]), "unsafe link in the markup: %r" % attrs
    for scheme in ("javascript:", "vbscript:", "data:text"):
        assert scheme not in outside.lower(), "%s must stay inside the data block" % scheme
    # The names are still listed for readers without JavaScript, as plain text.
    assert outside.count("<li><strong>Evil &lt;/script&gt;") == len(shortlist["datasets"])

    # A real address in the same position does become a link there.
    good = render.render_html({"datasets": [{"record": {"title": "T", "url": "https://data.example.org/t?a=1&b=2"}}]})
    assert '<a href="https://data.example.org/t?a=1&amp;b=2" rel="noopener noreferrer">T</a>' in good


@pytest.mark.parametrize("url", BAD_URLS + ["//example.org/x", "ftp://example.org/x", "/local/path", "example.org",
                                            "https://exa mple.org/", "https://example.org/\"onmouseover=\"alert(1)",
                                            "", None, 7, ["https://example.org/"], {"href": "https://example.org/"}])
def test_python_side_link_check(url):
    assert render._safe_url(url) == ""


def test_python_side_link_check_accepts_plain_web_addresses():
    for url in ("https://example.org/a?b=1&c=2#d", "http://example.org", " HTTPS://Example.org/x "):
        assert render._safe_url(url) == url.strip()


# ------------------------------------------------------------ missing and odd input

ODD_SHORTLISTS = [
    {},
    {"datasets": []},
    {"datasets": [{}]},
    {"datasets": [{"record": None}]},
    {"datasets": [{"record": {}}]},
    {"datasets": [{"record": {"title": "Only a title"}}]},
    {"datasets": [None, "Just a name", 3, True, [], {"record": "text"}]},
    {"datasets": {"record": {"title": "One entry, not in a list"}}},
    {"datasets": "A name instead of a list"},
    {"question": None, "generated_at": None, "requirements": None, "searched": None, "datasets": None,
     "not_recommended": None, "gaps": None, "notes": None},
    {"question": ["a", "list"], "generated_at": 20261111, "requirements": "one requirement",
     "searched": "everything", "datasets": [{"rank": "first", "record": {"title": 12, "url": 34,
                                                                       "access": "open", "licence": "CC",
                                                                       "size": "big", "creators": "one person",
                                                                       "verification": "yes", "year": "2020s"},
                                              "fit": 1, "why": {"text": "x"}, "requirements": ["R1"],
                                              "access_steps": "one step", "time_to_access": 3,
                                              "caveats": {"a": 1}, "papers": "a paper"}],
     "not_recommended": "a name", "gaps": "one gap", "notes": ["a", "b"]},
    {"requirements": {"R1": {"text": "as a map", "must": False}, "R2": "plain text"},
     "datasets": [{"record": {"title": "T", "access": {}, "licence": {}, "size": {}, "usage": None,
                              "verification": {}}, "requirements": [{"id": "R1", "status": "met"}],
                   "papers": [{}, None, {"title": None}]}]},
    {"generated_at": "not a date", "searched": {"sources": None, "queries": [None, 3], "n_candidates": "many"},
     "datasets": [{"rank": float("nan"), "record": {"title": "NaN rank", "size": {"bytes": float("inf")},
                                                    "year": float("-inf")}}]},
    {"datasets": [{"record": {"title": "Lone \ud83d surrogate and \u2028 separators \x00 \x1b"}}],
     "question": "Caf\u00e9 \u00fc\u00f1\u00ed\u00e7\u00f8d\u00e9 \u65e5\u672c\u8a9e \U0001f9ea? \ud800"},
    {"datasets": [{"record": {"title": "T", "extra": {"when": {1, 2, 3}, "who": ("a", "b"), 5: object}}}]},
]


@pytest.mark.parametrize("index", range(len(ODD_SHORTLISTS)))
def test_missing_optional_keys_and_odd_values_do_not_raise(tmp_path, index):
    shortlist = ODD_SHORTLISTS[index]
    path = render.render_report(shortlist, str(tmp_path / "odd.html"))
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    def not_json(name):
        raise AssertionError("%s is not JSON; the browser could not read the data block" % name)

    data = json.loads(split_data(text)[1], parse_constant=not_json)
    assert isinstance(data, dict)
    page = parse(text)
    assert page.title.startswith("Dataset shortlist") and len(page.scripts) == 2


def test_non_finite_numbers_become_null():
    data = embedded(render.render_html(ODD_SHORTLISTS[12]))
    entry = data["datasets"][0]
    assert entry["rank"] is None and entry["record"]["size"]["bytes"] is None and entry["record"]["year"] is None


def test_non_ascii_text_survives_the_round_trip():
    shortlist = load("shortlist_full.json")
    text = render.render_html(shortlist)
    block = split_data(text)[1]
    block.encode("ascii")                              # the data block never depends on the file encoding
    assert embedded(text)["datasets"][0]["record"]["creators"] == ["Institut f\u00fcr Raumstatistik Quillhaven",
                                                                  "Zo\u00eb Lindqvist-\u00dcnsal"]
    assert "Quillhaven Mobile Network Commuting Matrices, 2018\u20132023" in split_data(text)[0]  # fallback list


# ----------------------------------------------------- list for viewers without JavaScript

def test_fallback_list_is_ranked_and_states_access_licence_and_verification():
    shortlist = load("shortlist_full.json")
    shortlist["datasets"].reverse()                   # written worst first: the page still sorts by rank
    text = render.render_html(shortlist)
    start, end = text.index('<div class="noscript">'), text.index("</noscript>", text.index('<div class="noscript">'))
    fallback = text[start:end]
    items = re.findall(r"<li>(.*?)</li>", fallback, re.S)
    assert len(items) == 6
    assert [re.search(r">([^<]+)</a>", item).group(1).split(" ")[0] for item in items] == [
        "Quillhaven", "Brackenmoor", "Vantry", "Estermere", "Pellwater", "Solvane"]
    assert "Access: Free account. Licence: CC-BY-NC-SA-4.0. Verified on 11 November 2026." in items[0]
    assert "Access: Open. Licence: CC-BY-4.0." in items[1]
    assert "Access: Institutional agreement. Licence: not stated." in items[2]
    assert "Access: Application required. Licence: Estermere Archive End User Licence." in items[3]
    assert "Access: Not obtainable." in items[4]
    assert "Access: Unknown. Licence: not stated. Not verified." in items[5]
    assert "Research question:" in fallback and "checked on 11 November 2026" in fallback
    assert ".needs-js { display: none !important; }" in text


def test_fallback_shows_problems_of_verified_records_and_needs_a_real_check():
    checked = {"verified": True, "method": "registry-api", "checked_at": "2026-11-11T13:41:00Z"}
    text = render.render_html({"datasets": [
        {"rank": 1, "record": {"title": "A", "access": {"tier": "gated"},
                               "verification": dict(checked, problems=["access tier conflict: open versus gated"])}},
        {"rank": 2, "record": {"title": "B", "verification": {"verified": True}}},
        {"rank": 3, "record": {"title": "C", "verification": checked}}]})
    items = re.findall(r"<li>(.*?)</li>", text, re.S)
    assert "Verified on 11 November 2026, with problems to check: access tier conflict: open versus gated." in items[0]
    assert "Not verified (the record gives no method or date of the check)." in items[1]
    assert items[2].endswith("Verified on 11 November 2026.")


def test_fallback_never_calls_an_unknown_tier_open():
    text = render.render_html({"datasets": [{"record": {"title": "A", "access": {"tier": "public"}}},
                                            {"record": {"title": "B", "access": "OPEN "}},
                                            {"record": {"title": "C", "verification": {"verified": "true"}}}]})
    items = re.findall(r"<li>(.*?)</li>", text, re.S)
    assert "Access: Unknown." in items[0] and "Access: Open." in items[1]
    assert all("Not verified" in item for item in items)


def test_access_words_written_by_hand_are_shown_as_their_tier():
    shortlist = {"datasets": [
        {"record": {"title": "A", "access": {"tier": "application", "evidence": "access page: 'submit a proposal'"}}},
        {"record": {"title": "B", "access": "registered"}},
        {"record": {"title": "C", "access": {"tier": "fee"}}},
        {"record": {"title": "D", "access": {"tier": "Restricted"}}},
        {"record": {"title": "E", "access": {"tier": "by arrangement"}}},
        {"title": "F", "access": "application"},
    ]}
    before = json.dumps(shortlist, sort_keys=True)
    text = render.render_html(shortlist)
    assert json.dumps(shortlist, sort_keys=True) == before, "rendering must not change its input"
    items = re.findall(r"<li>(.*?)</li>", text, re.S)
    assert ["Access: %s." % word in item for word, item in zip(
        ["Application required", "Free account", "Institutional agreement", "Application required", "Unknown",
         "Application required"], items)] == [True] * 6
    start = text.index(DATA_OPEN) + len(DATA_OPEN)
    embedded = json.loads(text[start:text.index("</script>", start)])
    access = [entry.get("record", entry)["access"] for entry in embedded["datasets"]]
    assert [a["tier"] for a in access[:4]] == ["gated", "account", "controlled", "gated"]
    assert access[0]["evidence"] == "access page: 'submit a proposal'", "evidence that was given is kept"
    assert access[1]["evidence"] == 'the shortlist says "registered"'
    assert access[4] == {"tier": "by arrangement"}, "an unrecognised word is left for the page to show as Unknown"
    assert access[5]["tier"] == "gated"


def test_access_notes_say_what_was_mapped_and_what_was_not():
    notes = render.access_notes({"datasets": [
        {"record": {"title": "A", "access": {"tier": "application"}}},
        {"record": {"title": "B", "access": {"tier": "open"}}},
        {"record": {"title": "C", "access": {"tier": "by arrangement"}}},
        {"record": {"title": "D"}},
    ]})
    assert notes[0] == 'note: access "application" on "A" is shown as "Application required"'
    assert notes[1].startswith('warning: access "by arrangement" on "C" is not a tier the page knows')
    assert "open, account, gated, controlled, closed, unknown" in notes[1]
    assert len(notes) == 2
    assert render.access_notes({}) == [] and render.access_notes(None) == []


def test_render_command_prints_the_access_notes(tmp_path):
    source = tmp_path / "shortlist.json"
    source.write_text(json.dumps({"question": "q", "datasets": [
        {"record": {"title": "A", "access": {"tier": "application"}}},
        {"record": {"title": "B", "access": {"tier": "who knows"}}}]}), encoding="utf-8")
    done = subprocess.run([sys.executable, SCOUT, "render", str(source), "--out", str(tmp_path / "out.html")],
                          capture_output=True, text=True, timeout=60, cwd=str(tmp_path))
    assert done.returncode == 0, done.stderr
    assert 'note: access "application" on "A" is shown as "Application required"' in done.stdout
    assert 'warning: access "who knows" on "B"' in done.stdout


def test_tier_words_match_the_shared_tiers_and_the_page():
    assert set(render._TIER_LABELS) == set(common.ACCESS_TIERS)
    assert list(render._TIER_LABELS.values()) == ["Open", "Free account", "Application required",
                                                 "Institutional agreement", "Not obtainable", "Unknown"]
    with open(render.TEMPLATE_PATH, encoding="utf-8") as handle:
        template = handle.read()
    for tier, label in render._TIER_LABELS.items():
        assert re.search(r"\b%s: \{ label: '%s'" % (tier, re.escape(label)), template), tier


# -------------------------------------------------------------- page structure

def test_page_has_the_promised_structure_and_controls():
    with open(render.TEMPLATE_PATH, encoding="utf-8") as handle:
        template = handle.read()
    page = parse(template)
    css = "\n".join(page.styles)

    assert re.search(r":root\s*\{[^}]*--paper:[^}]*--ink:[^}]*--accent:", css, re.S)
    assert re.search(r"@media[^{]*\(prefers-color-scheme: dark\)\s*\{\s*:root\s*\{[^}]*--paper:", css)
    assert "@media print" in css and ".card.is-collapsed .card-body { display: grid !important; }" in css
    assert "gradient" not in css
    assert not re.findall(r"#[0-9a-fA-F]{3,8}\b", re.sub(r":root\s*\{.*?\}|@media print\s*\{.*", "", css, flags=re.S)), \
        "colours are defined once, as custom properties"
    assert "overflow-x: auto" in css and "max(var(--gutter), env(safe-area-inset-left, 0px))" in css
    assert ":focus-visible" in css and "outline: none" not in css and "outline: 0" not in css

    assert len(page.named("h1")) == 1 and len(page.named("main")) == 1 and len(page.named("table")) == 1
    headers = [attrs for attrs in page.named("th")]
    assert len(headers) == 8 and all(attrs.get("scope") == "col" for attrs in headers)
    ids = [attrs["id"] for _, attrs in page.tags if "id" in attrs]
    assert len(ids) == len(set(ids)), "duplicate id in the template"
    live = {attrs.get("id") for _, attrs in page.tags if attrs.get("aria-live") == "polite"}
    assert {"plan-count", "plan-message", "filter-status"} <= live
    labelled = {attrs["for"] for attrs in page.named("label")}
    for control in page.named("input") + page.named("textarea"):
        assert control["id"] in labelled, "control without a label: %r" % control
    assert all(attrs.get("type") == "button" for attrs in page.named("button"))

    script = page.code[0]
    for label in ("Copy plan as Markdown", "Download plan (.md)", "Allows commercial use"):
        assert label in template
    for word in ("'Open'", "'Free account'", "'Application required'", "'Institutional agreement'",
                 "'Not obtainable'", "'Unknown'", "'Not verified'", "scope: 'row'"):
        assert word in script
    assert not re.search("[\U0001F000-\U0001FAFF\u2600-\u27BF]", template), "no emoji"


# ------------------------------------------------------------------ the command

def test_scout_render_command_writes_the_report(tmp_path):
    out = tmp_path / "from-cli.html"
    done = subprocess.run([sys.executable, SCOUT, "render", os.path.join(FIXTURES, "shortlist_full.json"),
                           "--out", str(out)], capture_output=True, text=True, timeout=60, cwd=str(tmp_path))
    assert done.returncode == 0, done.stderr
    assert out.name in done.stdout + done.stderr, "the command should say where the page is"
    with open(str(out), encoding="utf-8") as handle:
        assert handle.read() == render.render_html(load("shortlist_full.json"))


def test_sample_report_is_the_rendered_full_fixture():
    with open(SAMPLE, encoding="utf-8") as handle:
        sample = handle.read()
    assert sample == render.render_html(load("shortlist_full.json")), (
        "docs/examples/sample-report.html is stale; render tests/fixtures/render/shortlist_full.json again")


# ----------------------------------------------------- the page script, run by Node

NODE_HARNESS = r"""
'use strict';
// Usage: node check_report_js.js <rendered.html> [<rendered.html> ...]
// For each rendered report: take out the page's inline script, syntax-check it
// with `node --check`, load it (without a document it only exports its pure
// functions) and run it over the shortlist embedded in the same file. Then
// exercise normalisation, link safety, filtering and the Markdown plan on
// edge cases. Prints a JSON summary; exits 1 on the first failed check.
const assert = require('assert');
const childProcess = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

let checks = 0;
function ok(value, message) { checks += 1; assert.ok(value, message); }
function eq(actual, expected, message) { checks += 1; assert.deepStrictEqual(actual, expected, message); }

function extract(html) {
  const blocks = [];
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/g;
  let m;
  while ((m = re.exec(html)) !== null) { blocks.push({ attrs: m[1], body: m[2] }); }
  return {
    code: blocks.filter((b) => !/\btype\s*=/.test(b.attrs)),
    data: blocks.filter((b) => /application\/json/.test(b.attrs)),
  };
}

function load(file, workdir, index) {
  const found = extract(fs.readFileSync(file, 'utf8'));
  eq(found.code.length, 1, 'exactly one executable script in ' + file);
  eq(found.data.length, 1, 'exactly one data block in ' + file);
  const jsFile = path.join(workdir, 'page-script-' + index + '.js');
  fs.writeFileSync(jsFile, found.code[0].body);
  childProcess.execFileSync(process.execPath, ['--check', jsFile], { stdio: 'pipe' });
  checks += 1;
  const api = require(jsFile);
  ok(api && typeof api.normalise === 'function', 'without a document the script exports its functions');
  return { api: api, raw: JSON.parse(found.data[0].body) };
}

function urlFields(value, out) {
  if (Array.isArray(value)) { value.forEach((v) => urlFields(v, out)); return out; }
  if (value && typeof value === 'object') {
    Object.keys(value).forEach((key) => {
      if (/url$/i.test(key) && typeof value[key] === 'string') { out.push(value[key]); }
      else { urlFields(value[key], out); }
    });
  }
  return out;
}

function keysOf(api, model, filters) {
  return model.datasets.filter((d) => api.matchesFilters(d, filters)).map((d) => d.key);
}

// Checks that must hold for any shortlist, however odd.
function inspect(file, workdir, index) {
  const loaded = load(file, workdir, index);
  const api = loaded.api;
  const model = api.normalise(loaded.raw);
  const keys = model.datasets.map((d) => d.key);

  eq(new Set(keys).size, keys.length, 'dataset keys are unique');
  urlFields(model, []).forEach((u) => ok(u === '' || /^https?:\/\/\S+$/.test(u), 'only web addresses survive: ' + u));
  model.datasets.forEach((d, i) => {
    eq(d.key, 'd' + (i + 1), 'keys come from the position');
    ok(Object.prototype.hasOwnProperty.call(api.TIERS, d.tier), 'known tier');
    ok(Object.prototype.hasOwnProperty.call(api.FITS, d.fit), 'known fit');
    ok(Object.prototype.hasOwnProperty.call(api.TIMES, d.time), 'known time');
    ok(d.title.length > 0 && d.tierLabel.length > 0 && d.licence.label.length > 0, 'nothing is shown blank');
    ok(typeof d.verification.verified === 'boolean');
    ok(d.verification.verified || d.verification.problems.length > 0, 'an unverified dataset says why');
    d.requirements.forEach((r) => ok(Object.prototype.hasOwnProperty.call(api.STATUSES, r.status), 'known status'));
  });

  const plan = api.buildPlanMarkdown(model, keys);
  ok(plan.indexOf('# Data access plan\n') === 0, 'plan has its heading');
  eq((plan.match(/^## /gm) || []).length, keys.length, 'one section per chosen dataset');
  (plan.match(/(?<!\\)<[^>\s]*>?/g) || []).forEach((link) =>
    ok(/^<https?:\/\/[^<>\s]+>$/.test(link), 'every unescaped < in the plan opens a web link: ' + link));
  ok(!/(?<!\\)\]\(/.test(plan), 'shortlist text cannot form a Markdown link');
  ok(!/(?<!\\)[`*]/.test(plan.replace(/\*\*[A-Z][A-Za-z ]+:\*\*/g, '')), 'markup characters from the shortlist are escaped');
  model.datasets.forEach((d) => d.steps.forEach((s) => ok(s.indexOf('\n') === -1)));

  return {
    file: file,
    question: model.question,
    datasets: model.datasets.map((d) => ({
      key: d.key, rank: d.rankLabel, title: d.title, url: d.url, host: d.host, tier: d.tier, tierLabel: d.tierLabel,
      fit: d.fit, time: d.time, verified: d.verification.verified, tone: d.verification.tone,
      commercial: d.licence.commercial, licence: d.licence.label, size: d.sizeText, must: d.mustSummary,
      papers: d.papers.length, statuses: d.requirements.map((r) => r.id + ':' + r.status + (r.assessed ? '' : ':unassessed')),
    })),
    requirements: model.requirements,
    notRecommended: model.notRecommended,
    searched: api.searchedSentence(model),
    checked: api.checkedSentence(model),
    tally: api.tally(model).map((t) => t.count + ' ' + t.label),
    options: api.filterOptions(model),
    filters: {
      none: keysOf(api, model, {}),
      commercial: keysOf(api, model, { commercial: true }),
      open: keysOf(api, model, { tiers: ['open'] }),
      free: keysOf(api, model, { tiers: ['open', 'account'] }),
      strong: keysOf(api, model, { fits: ['strong'] }),
      tram: keysOf(api, model, { query: '  TRAM ' }),
      two_terms: keysOf(api, model, { query: 'smart-card vantry' }),
      combined: keysOf(api, model, { tiers: ['gated', 'controlled'], fits: ['strong'], query: 'journey' }),
      nothing: keysOf(api, model, { query: 'zzz-no-such-word' }),
    },
    plan_all: plan,
    plan_first: api.buildPlanMarkdown(model, keys.slice(0, 1)),
  };
}

// Edge cases that do not depend on a fixture.
function unitTests(api) {
  // --- links: only http and https ---
  const kept = {
    'https://example.org/a': 'https://example.org/a',
    'http://example.org': 'http://example.org/',
    '  https://example.org/x  ': 'https://example.org/x',
    'HTTPS://EXAMPLE.ORG/Path': 'https://example.org/Path',
    'https://example.org/a b': 'https://example.org/a%20b',
    'http://example.org/?next=javascript:alert(1)': 'http://example.org/?next=javascript:alert(1)',
  };
  Object.keys(kept).forEach((input) => eq(api.safeUrl(input), kept[input], 'safeUrl keeps ' + input));
  ['javascript:alert(1)', 'JaVaScRiPt:alert(1)', ' javascript:alert(1)', 'java\nscript:alert(1)', '\tjavascript:alert(1)',
    'javascript://example.org/%0Aalert(1)', 'data:text/html,<b>x</b>', 'vbscript:msgbox(1)', 'file:///etc/passwd',
    'ftp://example.org/x', '//example.org/x', '/relative/path', 'example.org', 'https://', 'https:// example.org',
    'https://exa mple.org/', 'blob:https://example.org/1', 'mailto:a@example.org', 'x-https://example.org', '',
    null, undefined, 5, {}, [], true, ['https://example.org/'], { href: 'https://example.org/' },
  ].forEach((bad) => eq(api.safeUrl(bad), '', 'safeUrl rejects ' + JSON.stringify(bad)));
  ok(!/[<>"\s]/.test(api.safeUrl('https://example.org/<a b="c">')), 'angle brackets and quotes are percent-encoded');
  eq(api.hostOf('https://www.example.org/x'), 'example.org');
  eq(api.hostOf('https://user:pw@data.example.org:8443/x?y#z'), 'data.example.org');
  eq(api.hostOf(''), '');
  eq(api.hostOf(undefined), '');
  eq(api.cleanDoi('https://doi.org/10.5555/abc.1'), '10.5555/abc.1');
  eq(api.cleanDoi('doi: 10.5555/ABC'), '10.5555/ABC');
  eq(api.cleanDoi('not a doi'), '');
  eq(api.doiLink('10.5555/a<b>'), 'https://doi.org/10.5555/a%3Cb%3E');
  eq(api.doiLink(''), '');

  // --- text, dates, sizes ---
  eq(api.str('  a \n\t b  '), 'a b');
  eq(api.str('a\u0000b\u202Ec\u2066d'), 'abcd');
  eq(api.str(12), '12');
  [null, undefined, {}, [], true, NaN, Infinity].forEach((v) => eq(api.str(v), ''));
  eq(api.num('42'), 42);
  [null, '', 'x', NaN, Infinity, true, [], {}].forEach((v) => eq(api.num(v), null));
  eq(api.longDate('2026-11-11T14:00:00Z'), '11 November 2026');
  eq(api.longDate('2026-01-05'), '5 January 2026');
  eq(api.shortDate('2026-11-11 14:00'), '11 Nov 2026');
  ['', 'garbage', '2026-13-01', '2026-00-10', '2026-02-40', '20261111', null, 5].forEach((v) => eq(api.longDate(v), ''));
  eq(api.sizeText({ bytes: 6200000000, files: 72, records: 41800000 }), '41.8 million records \u00B7 72 files \u00B7 6.2 GB');
  eq(api.sizeText({ text: 'about 5 GB', bytes: 1 }), 'about 5 GB');
  eq(api.sizeText({ records: 2900000000 }), '2.9 billion records');
  eq(api.sizeText({ records: 1260000, files: 1 }), '1.26 million records \u00B7 1 file');
  eq(api.sizeText({ records: 1 }), '1 record');
  eq(api.sizeText({ records: 12345 }), '12,345 records');
  eq(api.sizeText({ records: 999999 }), '1 million records');
  eq(api.sizeText({ bytes: -5, files: 'x', records: null }), '');
  [null, undefined, {}, [], 7, true].forEach((v) => eq(api.sizeText(v), ''));
  eq(api.formatBytes(0), '0 bytes');
  eq(api.formatBytes(1), '1 byte');
  eq(api.formatBytes(999), '999 bytes');
  eq(api.formatBytes(1000), '1 kB');
  eq(api.formatBytes(1500), '1.5 kB');
  eq(api.formatBytes(999999), '1 MB');
  eq(api.formatBytes(918000000), '918 MB');
  eq(api.formatBytes(2.5e15), '2.5 PB');

  // --- no shortlist at all ---
  [null, undefined, [], 'text', 7, {}].forEach((input) => {
    const m = api.normalise(input);
    eq([m.datasets, m.requirements, m.gaps, m.notRecommended, m.notes, m.question], [[], [], [], [], [], '']);
    eq(api.searchedSentence(m), 'The sources searched were not recorded. 0 datasets made the shortlist.');
    eq(api.tally(m), []);
    ok(api.checkedSentence(m).indexOf('The date of this check was not recorded.') > 0);
    ok(api.buildPlanMarkdown(m, ['d1']).indexOf('0 datasets chosen') > 0);
  });

  // --- a dataset with almost nothing: every default is the cautious one ---
  const bare = api.normalise({ datasets: [{ record: null }, {}, 'Only a name', null, 42, true,
    { record: { title: 'T', access: 'OPEN ', licence: 'Custom terms' } }] });
  eq(bare.datasets.map((d) => d.title), ['Untitled dataset', 'Untitled dataset', 'Only a name', '42', 'T']);
  bare.datasets.slice(0, 4).forEach((d) => {
    eq([d.tier, d.tierLabel, d.fit, d.time, d.url, d.host], ['unknown', 'Unknown', 'unrated', 'unknown', '', '']);
    eq([d.verification.verified, d.verification.recorded, d.verification.tone], [false, false, 'stop']);
    eq(d.verification.problems, ['No verification was recorded for this dataset.']);
    eq([d.licence.stated, d.licence.label, d.licence.commercial, d.licence.commercialLabel],
      [false, 'Not stated', null, 'Reuse rights unclear']);
    eq([d.steps, d.caveats, d.papers, d.requirements, d.mustSummary, d.sizeText], [[], [], [], [], '', '']);
  });
  eq([bare.datasets[4].tier, bare.datasets[4].licence.label, bare.datasets[4].licence.commercial], ['open', 'Custom terms', null]);
  eq(bare.datasets.map((d) => d.rankLabel), ['1', '2', '3', '4', '5']);

  // --- the access tier is never guessed ---
  ['public', 'free', 'Open access', '', null, true, 3, ['open'], { tier: 'downloadable' }, { tier: null }, {}].forEach((access) => {
    eq(api.normalise({ datasets: [{ record: { title: 'x', access: access } }] }).datasets[0].tier, 'unknown',
      'tier for ' + JSON.stringify(access));
  });
  eq(api.normalise({ datasets: [{ record: { title: 'x', access: { tier: ' Gated' } } }] }).datasets[0].tierLabel, 'Application required');
  eq(api.TIER_ORDER.map((t) => api.TIERS[t].label),
    ['Open', 'Free account', 'Application required', 'Institutional agreement', 'Not obtainable', 'Unknown']);

  // --- verified only when the block says exactly true ---
  ['true', 1, 'yes', null, undefined, {}, [true]].forEach((value) => {
    const v = api.normalise({ datasets: [{ record: { title: 'x', verification: { verified: value } } }] }).datasets[0].verification;
    eq([v.verified, v.recorded, v.tone], [false, true, 'stop'], 'verified=' + JSON.stringify(value));
    eq(v.problems, ['The check did not confirm this dataset, and it gave no reason.']);
  });
  ['yes', true, [], 'verified', 1].forEach((block) => {
    eq(api.normalise({ datasets: [{ record: { title: 'x', verification: block } }] }).datasets[0].verification.verified, false);
  });
  const seen = api.normalise({ datasets: [{ record: { title: 'x', verification: {
    verified: true, method: 'registry-api', checked_at: '2026-11-11T13:41:00Z', final_url: 'javascript:alert(1)' } } }] }).datasets[0].verification;
  eq([seen.verified, seen.tone, seen.methodLabel, seen.checkedLong, seen.checkedShort, seen.finalUrl, seen.problems],
    [true, 'go', 'Registry record', '11 November 2026', '11 Nov 2026', '', []]);
  // --- a verified dataset keeps its problems, and they count in the tally (S2) ---
  const warnedModel = api.normalise({ datasets: [{ record: { title: 'x', verification: {
    verified: true, method: 'registry-api', checked_at: '2026-11-11T13:41:00Z',
    problems: ['access tier conflict: the record says open but the host says gated'] } } }] });
  const warned = warnedModel.datasets[0].verification;
  eq([warned.verified, warned.warned, warned.problems.length], [true, true, 1]);
  ok(api.tally(warnedModel).some((t) => t.label === 'was verified with problems to check'), 'tally names the warning');
  ok(api.buildPlanMarkdown(warnedModel, [warnedModel.datasets[0].key]).indexOf('problems to check: access tier conflict') >= 0,
    'the access plan repeats the problem');
  // --- "verified" needs the method and the date of the check (M8) ---
  [{ verified: true }, { verified: true, method: 'http' }, { verified: true, checked_at: '2026-11-11T13:41:00Z' }].forEach((block) => {
    const v = api.normalise({ datasets: [{ record: { title: 'x', verification: block } }] }).datasets[0].verification;
    eq([v.verified, v.recorded, v.reason, v.tone], [false, true, 'Check not recorded', 'wait'], JSON.stringify(block));
    ok(/no method or no date/.test(v.problems[0]), 'says why the claim is not shown');
  });
  // --- the registry's title and the name given are kept for display (B3) ---
  const renamed = api.normalise({ datasets: [{ record: { title: 'Registry Title', extra: { given_title: 'Given name' },
    verification: { verified: true, method: 'registry-api', checked_at: '2026-11-11T13:41:00Z', found_title: 'Registry Title' } } }] }).datasets[0];
  eq([renamed.givenTitle, renamed.verification.foundTitle], ['Given name', 'Registry Title']);
  const blocked = api.normalise({ datasets: [{ record: { title: 'x', verification: {
    verified: false, outcome: 'could_not_check', problems: ['login wall'] } } }] }).datasets[0].verification;
  eq([blocked.verified, blocked.tone, blocked.reason, blocked.problems], [false, 'wait', 'Could not be checked', ['login wall']]);
  const gone = api.normalise({ datasets: [{ record: { title: 'x', verification: { verified: false, outcome: 'not_found' } } }] }).datasets[0].verification;
  eq([gone.tone, gone.reason], ['stop', 'Not found']);

  // --- "allows commercial use" needs a named licence that says so ---
  const lic = api.normalise({ datasets: [
    { record: { title: 'a', licence: { id: 'X', commercial_use: true } } },
    { record: { title: 'b', licence: { id: 'Y', commercial_use: 'true' } } },
    { record: { title: 'c', licence: { id: 'Z', commercial_use: null } } },
    { record: { title: 'd', licence: { id: 'W', commercial_use: false } } },
    { record: { title: 'e' } },
    { record: { title: 'f', licence: { commercial_use: true } } },
    { record: { title: 'g', license: { name: 'American spelling', commercial_use: true, share_alike: true } } },
  ] });
  eq(lic.datasets.filter((d) => api.matchesFilters(d, { commercial: true })).map((d) => d.title), ['a', 'g']);
  eq(lic.datasets.map((d) => d.licence.commercialLabel), ['Commercial use allowed', 'Commercial use not determined',
    'Commercial use not determined', 'Non-commercial use only', 'Reuse rights unclear', 'Reuse rights unclear', 'Commercial use allowed']);
  eq(api.filterOptions(lic).commercial, 2);

  // --- requirement grid ---
  const reqs = api.normalise({
    requirements: [{ id: 'R1', text: 'one', must: true }, { id: 'R2', text: 'two', must: false }, 'three', { id: 'R1', text: 'again' }],
    datasets: [{ record: { title: 'x' }, requirements: {
      R1: { status: 'MET', evidence: ' e ', url: 'javascript:alert(1)' }, R9: { status: 'partial', url: 'https://example.org/r9' }, R2: 'unmet' } }],
  });
  eq(reqs.requirements, [{ id: 'R1', text: 'one', must: true }, { id: 'R2', text: 'two', must: false }, { id: 'R3', text: 'three', must: true }]);
  eq(reqs.datasets[0].requirements.map((r) => [r.id, r.status, r.must, r.assessed, r.evidence, r.url]), [
    ['R1', 'met', true, true, 'e', ''], ['R2', 'unmet', false, true, '', ''], ['R3', 'unknown', true, false, '', ''],
    ['R9', 'partial', null, true, '', 'https://example.org/r9']]);
  eq(reqs.datasets[0].mustSummary, '1 of 2 must-haves met (1 unknown)');
  ['yes', 'ok', '', null, true, 1, { status: 'met' }].forEach((status) => {
    const row = api.normalise({ requirements: [{ id: 'R1', text: 't' }], datasets: [{ record: {}, requirements: { R1: { status: status } } }] })
      .datasets[0].requirements[0];
    eq(row.status, 'unknown', 'status ' + JSON.stringify(status) + ' is not read as met');
  });
  const listForm = api.normalise({ requirements: [{ id: 'R1', text: 't' }], datasets: [{ record: {}, requirements: [{ id: 'R1', status: 'partial' }] }] });
  eq(listForm.datasets[0].requirements[0].status, 'partial');

  // --- names that exist on every object are just names ---
  const proto = api.normalise({
    requirements: [{ id: '__proto__', text: 'p' }, { id: 'constructor', text: 'c' }, { id: 'toString', text: 't' }],
    datasets: [{ record: { title: 'x', access: { tier: 'constructor' } }, fit: '__proto__', time_to_access: 'toString',
      requirements: JSON.parse('{"__proto__": {"status": "met"}, "constructor": {"status": "hasOwnProperty"}}') }],
  });
  eq([proto.datasets[0].tier, proto.datasets[0].fit, proto.datasets[0].time], ['unknown', 'unrated', 'unknown']);
  eq(proto.datasets[0].requirements.map((r) => r.id + ':' + r.status + ':' + r.assessed),
    ['__proto__:met:true', 'constructor:unknown:true', 'toString:unknown:false']);
  eq([({}).status, ({}).text, Object.keys(Object.prototype).length], [undefined, undefined, 0]);

  // --- order: by rank, then as written ---
  const ranked = api.normalise({ datasets: [{ rank: 3, record: { title: 'c' } }, { rank: 1, record: { title: 'a' } },
    { record: { title: 'z' } }, { rank: '2', record: { title: 'b' } }, { rank: 1, record: { title: 'a2', id: 'same' } },
    { rank: 'first', record: { title: 'y', id: 'same' } }] });
  eq(ranked.datasets.map((d) => d.title), ['a', 'a2', 'b', 'c', 'z', 'y']);
  eq(ranked.datasets.map((d) => d.key), ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']);
  eq(ranked.datasets.map((d) => d.rankLabel), ['1', '1', '2', '3', '5', '6']);

  // --- filtering ---
  const shelf = api.normalise({ datasets: [
    { record: { title: 'River gauges', access: { tier: 'open' }, licence: { id: 'CC0-1.0', commercial_use: true }, publisher: 'Water Board' }, fit: 'strong' },
    { record: { title: 'Rain radar', access: { tier: 'gated' }, licence: { id: 'CC-BY-NC-4.0', commercial_use: false }, subjects: ['Precipitation'] }, fit: 'partial', caveats: ['Radar gaps in winter'] },
    { record: { title: 'Flood claims', access: { tier: 'controlled' } }, fit: 'strong', why: 'Insurance claims by postcode' },
    { record: { title: 'Soil moisture' }, papers: [{ title: 'A gauges comparison' }] },
  ] });
  const pick = (filters) => shelf.datasets.filter((d) => api.matchesFilters(d, filters)).map((d) => d.title);
  eq(pick(undefined), ['River gauges', 'Rain radar', 'Flood claims', 'Soil moisture']);
  eq(pick({ tiers: [], fits: [], commercial: false, query: '   ' }), ['River gauges', 'Rain radar', 'Flood claims', 'Soil moisture']);
  eq(pick({ tiers: ['open'] }), ['River gauges']);
  eq(pick({ tiers: ['open', 'gated'] }), ['River gauges', 'Rain radar']);
  eq(pick({ tiers: ['unknown'] }), ['Soil moisture']);
  eq(pick({ fits: ['strong'] }), ['River gauges', 'Flood claims']);
  eq(pick({ fits: ['unrated'] }), ['Soil moisture']);
  eq(pick({ commercial: true }), ['River gauges']);
  eq(pick({ query: 'GAUGES' }), ['River gauges', 'Soil moisture']);
  eq(pick({ query: 'gauges water' }), ['River gauges']);
  eq(pick({ query: 'precipitation' }), ['Rain radar']);
  eq(pick({ query: 'winter radar' }), ['Rain radar']);
  eq(pick({ query: 'postcode' }), ['Flood claims']);
  eq(pick({ tiers: ['controlled', 'gated'], fits: ['strong'] }), ['Flood claims']);
  eq(pick({ tiers: ['open'], commercial: true, query: 'rain' }), []);
  eq(api.filtersActive({ tiers: [], fits: [], commercial: false, query: ' ' }), false);
  eq([api.filtersActive({ tiers: ['open'] }), api.filtersActive({ commercial: true }), api.filtersActive({ query: 'x' })], [true, true, true]);
  eq(api.filterOptions(shelf), {
    tiers: [{ value: 'open', label: 'Open', count: 1 }, { value: 'gated', label: 'Application required', count: 1 },
      { value: 'controlled', label: 'Institutional agreement', count: 1 }, { value: 'unknown', label: 'Unknown', count: 1 }],
    fits: [{ value: 'strong', label: 'Strong', count: 2 }, { value: 'partial', label: 'Partial', count: 1 }, { value: 'unrated', label: 'Not rated', count: 1 }],
    commercial: 1,
  });
  eq(api.tally(shelf).map((t) => t.count + ' ' + t.label),
    ['1 needs no approval', '2 need an application or agreement', '1 has unknown access', '4 could not be verified']);

  // --- Markdown: text from the shortlist cannot become markup ---
  eq(api.mdText('access_right=open'), 'access_right=open');
  eq(api.mdText('_emphasis_ and __init__'), '\\_emphasis\\_ and \\_\\_init\\_\\_');
  eq(api.mdText('*x* `y` [z](w) <b> \\'), '\\*x\\* \\`y\\` \\[z\\](w) \\<b\\> \\\\');
  eq(api.mdText('# heading'), '\\# heading');
  eq(api.mdText('- item'), '\\- item');
  eq(api.mdText('+ item'), '\\+ item');
  eq(api.mdText('1. first'), '1\\. first');
  eq(api.mdText('12) twelfth'), '12\\) twelfth');
  eq(api.mdText('a\n\n# b\n- c'), 'a # b - c');
  eq(api.mdText(null), '');

  const evil = '</script><script>alert(1)</script> <img onerror=alert(1) src=x> [click](javascript:alert(1))';
  const plan = api.buildPlanMarkdown(api.normalise({
    question: evil,
    generated_at: '2026-11-11T14:00:00Z',
    datasets: [
      { rank: 2, record: { title: 'Second', url: 'https://example.org/second' } },
      { rank: 1, record: { title: evil, url: 'javascript:alert(1)', access: { tier: 'gated', evidence: evil },
        licence: { name: evil, url: 'data:text/html,x', commercial_use: false, share_alike: true },
        verification: { verified: false, problems: [evil] } },
        access_steps: [evil, 'line one\nline two\n\n## not a heading', '   '], time_to_access: 'weeks', caveats: [evil],
        papers: [{ title: evil, year: evil, url: 'javascript:alert(1)', doi: '10.5555/x<y>', note: evil }] },
      { rank: 3, record: { title: 'Third' } },
    ],
  }), ['d2', 'd1', 'nope']);
  const lines = plan.split('\n');
  eq(lines[0], '# Data access plan');
  ok(lines[2].indexOf('**Research question:** \\</script\\>\\<script\\>alert(1)\\</script\\> \\<img onerror=alert(1) src=x\\> \\[click\\](javascript:alert(1))') === 0);
  eq(lines[4], '2 datasets chosen from the dataset-shortlist shortlist of 11 November 2026.');
  eq(lines.filter((l) => /^## /.test(l)), ['## 1. \\</script\\>\\<script\\>alert(1)\\</script\\> \\<img onerror=alert(1) src=x\\> \\[click\\](javascript:alert(1))', '## 2. Second']);
  ok(plan.indexOf('- **URL:** the address in the record is not a web address') > 0);
  ok(plan.indexOf('- **URL:** <https://example.org/second>') > 0);
  ok(plan.indexOf('- **Access:** Application required (evidence: \\</script\\>') > 0);
  ok(plan.indexOf('(non-commercial use only, share-alike)\n') > 0, 'an unsafe licence address is left out');
  ok(plan.indexOf('- **Time to access:** weeks') > 0);
  ok(plan.indexOf('- **Verification:** NOT VERIFIED: \\</script\\>') > 0);
  ok(plan.indexOf('\n2. line one line two ## not a heading\n') > 0, 'a step stays on one line');
  eq(lines.filter((l) => /^\d+\. /.test(l)).length, 2, 'the blank step is dropped');
  ok(plan.indexOf('<https://doi.org/10.5555/x%3Cy%3E>') > 0, 'a paper falls back to its DOI link');
  ok(plan.indexOf('Third') === -1, 'unselected datasets stay out');
  ok(plan.indexOf('No access steps were recorded.') > 0 && plan.indexOf('No caveats were recorded.') > 0 && plan.indexOf('No papers were recorded.') > 0);
  ok(!/(?<!\\)<(?!https?:\/\/)/.test(plan), 'no unescaped < except web links');
  ok(!/(?<!\\)\]\(/.test(plan));
  ok(/\n---\n\nAccess conditions and licences change\. Everything on this page was checked on 11 November 2026\./.test(plan));
  ok(plan.charAt(plan.length - 1) === '\n');
}

function main(files) {
  if (!files.length) { throw new Error('give at least one rendered report'); }
  const workdir = fs.mkdtempSync(path.join(os.tmpdir(), 'scout-report-'));
  try {
    const reports = files.map((file, index) => inspect(file, workdir, index));
    unitTests(load(files[0], workdir, 'unit').api);
    process.stdout.write(JSON.stringify({ ok: true, node: process.version, checks: checks, reports: reports }) + '\n');
  } finally {
    fs.rmSync(workdir, { recursive: true, force: true });
  }
}

try {
  main(process.argv.slice(2));
} catch (error) {
  process.stderr.write('FAILED after ' + checks + ' checks: ' + (error && error.stack ? error.stack : error) + '\n');
  process.exit(1);
}
"""

NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="no node binary on PATH; the page script is not exercised")


def run_node_harness(tmp_path, shortlists):
    files = []
    for name, shortlist in shortlists:
        files.append(render.render_report(shortlist, str(tmp_path / (name + ".html"))))
    harness = tmp_path / "check_report_js.js"
    harness.write_text(NODE_HARNESS, encoding="utf-8")
    done = subprocess.run([NODE, str(harness)] + files, capture_output=True, text=True, timeout=120)
    assert done.returncode == 0, done.stderr[-4000:]
    summary = json.loads(done.stdout)
    assert summary["ok"] is True and summary["checks"] > 300
    return summary["reports"]


@needs_node
def test_page_script_on_the_full_fixture(tmp_path):
    report = run_node_harness(tmp_path, [("full", load("shortlist_full.json"))])[0]
    datasets = report["datasets"]

    assert [d["key"] for d in datasets] == ["d1", "d2", "d3", "d4", "d5", "d6"]
    assert [d["rank"] for d in datasets] == ["1", "2", "3", "4", "5", "6"]
    assert [d["title"].split(" ")[0] for d in datasets] == [
        "Quillhaven", "Brackenmoor", "Vantry", "Estermere", "Pellwater", "Solvane"]
    assert [d["tierLabel"] for d in datasets] == ["Free account", "Open", "Institutional agreement",
                                                 "Application required", "Not obtainable", "Unknown"]
    assert [d["fit"] for d in datasets] == ["strong", "partial", "strong", "partial", "weak", "weak"]
    assert [d["time"] for d in datasets] == ["days", "minutes", "months", "weeks", "unknown", "unknown"]
    assert [d["verified"] for d in datasets] == [True, True, True, True, True, False]
    assert [d["commercial"] for d in datasets] == [False, True, None, None, True, None]
    assert [d["licence"] for d in datasets] == ["CC-BY-NC-SA-4.0", "CC-BY-4.0", "Not stated",
                                               "Estermere Archive End User Licence", "ODbL-1.0", "Not stated"]
    assert [d["size"] for d in datasets] == [
        "41.8 million records \u00b7 72 files \u00b7 6.2 GB", "118 files \u00b7 918 MB", "2.9 billion records",
        "about 1.26 million trips by 63,000 respondents", "", ""]
    assert [d["must"] for d in datasets] == [
        "4 of 4 must-haves met", "3 of 4 must-haves met (1 partly)", "3 of 4 must-haves met (1 partly)",
        "2 of 4 must-haves met (2 partly)", "0 of 4 must-haves met (2 partly, 1 unmet, 1 unknown)",
        "1 of 4 must-haves met (1 unmet, 2 unknown)"]
    assert [d["papers"] for d in datasets] == [2, 1, 1, 3, 0, 1]
    assert datasets[2]["statuses"][-1] == "R7:unknown:unassessed"          # in the search, absent from the entry
    assert datasets[5]["statuses"] == ["R1:unmet", "R2:unknown:unassessed", "R3:met", "R4:unknown:unassessed",
                                       "R5:unknown:unassessed", "R6:unknown:unassessed", "R7:unknown:unassessed"]
    assert datasets[2]["host"] == "researchdata.example.org"

    assert report["searched"] == ("Searched 3 sources (coppice, lanternfish, quayside) on 11 November 2026. "
                                  "Of 87 candidates, 6 datasets made the shortlist and 3 were set aside.")
    assert report["tally"] == ["2 need no approval", "2 need an application or agreement", "1 is not obtainable",
                               "1 has unknown access", "1 could not be verified"]
    assert "checked on 11 November 2026" in report["checked"]
    assert [o["label"] for o in report["options"]["tiers"]] == [
        "Open", "Free account", "Application required", "Institutional agreement", "Not obtainable", "Unknown"]
    assert report["options"]["commercial"] == 2
    assert [r["must"] for r in report["requirements"]] == [True, True, True, True, False, False, False]
    assert report["notRecommended"][2] == {"name": "Tidewell Ride-Hailing Sample", "url": "",
                                           "reason": report["notRecommended"][2]["reason"]}

    filters = report["filters"]
    assert filters["none"] == ["d1", "d2", "d3", "d4", "d5", "d6"]
    assert filters["commercial"] == ["d2", "d5"]
    assert filters["open"] == ["d2"] and filters["free"] == ["d1", "d2"]
    assert filters["strong"] == ["d1", "d3"]
    assert filters["tram"] == ["d1", "d2"]
    assert filters["two_terms"] == ["d3"] and filters["combined"] == ["d3"] and filters["nothing"] == []

    plan = report["plan_first"]
    for expected in (
            "# Data access plan\n",
            "**Research question:** I want to study how the shift to remote work",
            "1 dataset chosen from the dataset-shortlist shortlist of 11 November 2026.",
            "## 1. Quillhaven Mobile Network Commuting Matrices, 2018\u20132023\n",
            "- **URL:** <https://coppice.example.org/records/48213>\n",
            "- **Access:** Free account (evidence: access_right=registered; terms=click-through)\n",
            "- **Licence:** CC-BY-NC-SA-4.0 (non-commercial use only, share-alike) <https://licences.example.org/by-nc-sa/4.0/>\n",
            "- **Time to access:** days\n",
            "- **Verification:** verified on 11 November 2026 (registry record)\n",
            "### Access steps\n\n1. Create a free account on the Coppice repository\n",
            "4. Download the monthly tables, or request the link to the full archive\n",
            "### Caveats\n\n- Flows under 15 commuters are suppressed",
            "### Papers that used it\n\n- Fewer trips, longer trips: commuting after the remote-work shift in 214 "
            "municipalities (2025). <https://journals.example.org/jtg/2025/0142> Used the monthly matrices",
            "Access conditions and licences change. Everything on this page was checked on 11 November 2026."):
        assert expected in plan, expected
    assert "Brackenmoor" not in plan and plan.count("\n## ") == 1

    everything = report["plan_all"]
    assert everything.count("\n## ") == 6
    assert "- **Verification:** NOT VERIFIED when checked on 11 November 2026: the landing page answered HTTP 404; " \
           "no registry searched lists a dataset with this title" in everything
    assert "- **Licence:** Not stated (reuse rights unclear)\n" in everything
    assert "- **Licence:** ODbL-1.0 (commercial use allowed, share-alike)" in everything
    assert "- **Access:** Unknown\n" in everything
    assert "No access steps were recorded." in everything and "No papers were recorded." in everything
    # A paper with a DOI but no address links to the DOI; one with neither is listed without a link.
    assert "(2024). <https://doi.org/10.5555/trb.2024.3391> Compared commuting days" in everything
    assert "- Sample design and weighting of the Estermere travel diary (2019). Method report." in everything


@needs_node
def test_page_script_on_minimal_empty_and_hostile_shortlists(tmp_path):
    minimal, empty, bad, odd = run_node_harness(tmp_path, [
        ("minimal", load("shortlist_minimal.json")), ("empty", {}), ("hostile", hostile()),
        ("odd", ODD_SHORTLISTS[10])])

    assert len(minimal["datasets"]) == 1
    only = minimal["datasets"][0]
    assert only["title"] == "Estermere Regional Travel Diary Microdata"
    assert only["url"] == "https://quayside.example.org/catalogue/ETD-2017-2023"
    assert (only["tierLabel"], only["verified"], only["licence"], only["fit"], only["time"]) == (
        "Unknown", False, "Not stated", "unrated", "unknown")
    assert minimal["tally"] == ["1 has unknown access", "1 could not be verified"]
    assert minimal["searched"] == "The sources searched were not recorded. 1 dataset made the shortlist."
    assert "- **URL:** <https://quayside.example.org/catalogue/ETD-2017-2023>" in minimal["plan_all"]
    assert "- **Access:** Unknown\n- **Licence:** Not stated (reuse rights unclear)" in minimal["plan_all"]
    assert "NOT VERIFIED: No verification was recorded for this dataset." in minimal["plan_all"]

    assert empty["datasets"] == [] and empty["filters"]["none"] == [] and empty["question"] == ""

    assert len(bad["datasets"]) == 6
    assert all(d["url"] == "" and d["host"] == "" for d in bad["datasets"]), "a script address became a link"
    assert bad["notRecommended"][0]["url"] == ""
    assert all(d["title"] == XSS for d in bad["datasets"])           # kept as text, to be shown as text
    plan = bad["plan_all"]
    assert not re.search(r"(?<!\\)<(?!https?://)", plan) and not re.search(r"(?<!\\)\]\(", plan)
    assert "<https://" not in plan and "javascript:alert(1)>" not in plan
    assert plan.count("- **URL:** the address in the record is not a web address") == 6
    assert "\n2. two lines \\[x\\](javascript:alert(1))\n" in plan

    assert [d["title"] for d in odd["datasets"]] == ["12"]
    assert (odd["datasets"][0]["tierLabel"], odd["datasets"][0]["licence"], odd["datasets"][0]["verified"]) == (
        "Open", "CC", False)


# ------------------------------------------------------- the page in a real browser

def warned_shortlist():
    return {"question": "q", "datasets": [{"rank": 1, "record": {
        "title": "Record Title", "url": "https://repo.example/r/1", "access": {"tier": "gated", "evidence": "host: flag"},
        "extra": {"given_title": "Given name"},
        "verification": {"verified": True, "method": "registry-api", "checked_at": "2026-11-11T13:41:00Z",
                         "found_title": "Host Title",
                         "problems": ["access tier conflict: the record says open but the host says gated"]}}}]}


def find_chrome():
    candidates = [os.environ.get("SCOUT_CHROME"),
                  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Chromium.app/Contents/MacOS/Chromium",
                  shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser")]
    return next((c for c in candidates if c and os.path.exists(c)), None)


def dump_dom(tmp_path, name, shortlist):
    path = render.render_report(shortlist, str(tmp_path / (name + ".html")))
    done = subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--no-first-run", "--disable-extensions",
                           "--user-data-dir=%s" % (tmp_path / ("profile-" + name)), "--virtual-time-budget=5000",
                           "--dump-dom", "file://" + path], capture_output=True, text=True, timeout=180)
    assert done.returncode == 0 and "<html" in done.stdout, done.stderr[-2000:]
    return done.stdout


@pytest.mark.skipif(os.environ.get("SCOUT_BROWSER") != "1", reason="browser test; set SCOUT_BROWSER=1 to run")
def test_page_builds_in_headless_chrome(tmp_path):
    if not find_chrome():
        pytest.skip("no Chrome or Chromium found (set SCOUT_CHROME to its path)")

    for name, shortlist, n_cards in (("full", load("shortlist_full.json"), 6),
                                     ("minimal", load("shortlist_minimal.json"), 1),
                                     ("hostile", hostile(), 6), ("empty", {}, 0), ("warned", warned_shortlist(), 1)):
        dom = dump_dom(tmp_path, name, shortlist)
        page = parse(dom)
        html_attrs = page.named("html")[0]
        assert html_attrs.get("data-scout") == "ready", "the page script did not finish for %s" % name
        cards = [attrs for attrs in page.named("article") if "card" in attrs.get("class", "").split()]
        assert len(cards) == n_cards
        rows = [attrs for attrs in page.named("tr") if attrs.get("id", "").startswith("row-")]
        assert len(rows) == n_cards
        assert len(page.scripts) == 2 and not page.named("img") and not page.named("iframe")
        for attrs in page.named("a"):
            assert re.match(r"(https?://|#)", attrs.get("href", "")), "%s: unsafe link %r" % (name, attrs)
        assert all(not key.startswith("on") for _, attrs in page.tags for key in attrs)
        if name == "full":
            assert sum(1 for attrs in cards if "is-unverified" in attrs["class"]) == 1
            assert dom.count("Not verified") >= 3 and "Institutional agreement" in dom
        if name == "warned":
            assert "Verified, with problems to check" in dom and "Problems to check" in dom
            assert "access tier conflict: the record says open but the host says gated" in dom
            assert "The registry record is titled \u201cHost Title\u201d." in dom
            assert "It was given as \u201cGiven name\u201d." in dom
        if name == "hostile":
            assert "&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;" in dom
            assert "javascript:" not in " ".join(attrs.get("href", "") for attrs in page.named("a"))
