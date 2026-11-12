"""Render a shortlist as one self-contained, interactive HTML page.

The input is the shortlist object described in docs/SPEC.md ("Shortlist"). The
page is built in the browser from that object: this module embeds it as JSON in
``assets/report_template.html`` and writes the result. The page loads nothing
from the network, so it works offline and from a ``file://`` address.

Every string in a shortlist comes from a registry, a web page or a paper, so all
of it is treated as untrusted:

* the JSON block is written with ``<``, ``>`` and ``&`` as ``\\uXXXX`` escapes, so
  no value can close the ``<script>`` element that carries it;
* the two places where this module writes shortlist text into markup (the page
  title and the list shown when JavaScript is off) go through ``html.escape``,
  and only http and https addresses become links;
* the page builds its DOM with ``textContent`` and ``createElement``;
* a Content-Security-Policy allows the page's own script by its SHA-256 hash and
  nothing else, so injected markup could neither run nor load anything.

Rendering is deterministic: the same shortlist always gives the same bytes.
Standard library only.
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
import math
import os
import re

from .common import ACCESS_TIERS, canonical_tier

__all__ = ["render_report", "render_html", "access_notes", "TEMPLATE_PATH"]

_HERE = os.path.dirname(os.path.abspath(__file__))
# <skill>/scripts/scoutlib/render.py -> <skill>/assets/report_template.html
TEMPLATE_PATH = os.path.normpath(
    os.path.join(_HERE, os.pardir, os.pardir, "assets", "report_template.html"))

_PLACEHOLDERS = ("TITLE", "CSP_SCRIPT", "FALLBACK", "DATA")
_PLACEHOLDER_RE = re.compile(r"__SCOUT_(%s)__" % "|".join(_PLACEHOLDERS))
_INLINE_SCRIPT_RE = re.compile(r"<script>(.*?)</script>", re.S)
_HTTP_URL_RE = re.compile(r"^https?://[^\s<>\"'`\\\x00-\x1f\x7f]+$", re.I)
_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:$|[T\s])")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f‪-‮⁦-⁩]")
_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December")

# The words the page uses for each access tier (keys match common.ACCESS_TIERS).
# The template carries the same table for the interactive page; a test keeps
# the two in step.
_TIER_LABELS = {
    "open": "Open",
    "account": "Free account",
    "gated": "Application required",
    "controlled": "Institutional agreement",
    "closed": "Not obtainable",
    "unknown": "Unknown",
}

_TITLE_PREFIX = "Dataset shortlist"
_TITLE_LIMIT = 72


def render_report(shortlist, out_path):
    """Write the report for `shortlist` to `out_path` and return its absolute path.

    Missing optional keys are tolerated everywhere: a shortlist with a single
    dataset that has only a title still gives a complete page. Parent folders
    are created when they do not exist.
    """
    if out_path is None or str(out_path) == "":
        raise ValueError("out_path is required")
    page = render_html(shortlist)
    path = os.path.abspath(os.path.expanduser(os.fspath(out_path)))
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # "\n" on every platform: the script hash in the page is computed over
    # exactly these characters.
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(page)
    return path


def render_html(shortlist):
    """Return the complete HTML document for `shortlist` as a string."""
    if not isinstance(shortlist, dict):
        raise TypeError("the shortlist must be a JSON object (a dict), not %s"
                        % type(shortlist).__name__)
    template = _read_template()
    data = _clean(shortlist)
    _settle_access(data)
    values = {
        "TITLE": html.escape(_page_title(data), quote=True),
        "CSP_SCRIPT": _script_sources(template),
        "FALLBACK": _fallback_html(data),
        "DATA": _embed_json(data),
    }
    missing = [name for name in _PLACEHOLDERS if "__SCOUT_%s__" % name not in template]
    if missing:
        raise ValueError("report template %s has no placeholder for: %s"
                         % (TEMPLATE_PATH, ", ".join(missing)))
    # One pass with a callback: substituted text is never scanned again, and
    # backslashes in the JSON are not read as regex escapes.
    return _PLACEHOLDER_RE.sub(lambda match: values[match.group(1)], template)


# --------------------------------------------------------------------- access

def _records(data):
    """(entry, record) for every dataset; an entry without "record" is its own record."""
    datasets = data.get("datasets") if isinstance(data, dict) else None
    for entry in datasets if isinstance(datasets, list) else []:
        if isinstance(entry, dict):
            record = entry.get("record")
            yield entry, record if isinstance(record, dict) else entry


def _stated_tier(record):
    access = record.get("access")
    return access.get("tier") if isinstance(access, dict) else access


def _settle_access(data):
    """Write the page's own tier word into every record.

    A shortlist is partly written by hand: after reading a landing page people
    put "application" or "registered" where the page expects "gated" or
    "account", and the page would then show "Unknown" for a condition that had
    in fact been established. Words that state a restriction are mapped to their
    tier and the original word is kept as evidence when none was given. Any
    other text stays "unknown"; it is never read as "open".
    """
    for _, record in _records(data):
        stated = _stated_tier(record)
        tier, how = canonical_tier(stated)
        if how == "exact":
            access = record.get("access")
            if isinstance(access, dict):
                access["tier"] = tier
            else:
                record["access"] = {"tier": tier, "evidence": ""}
        elif how == "word":
            access = record.get("access")
            evidence = access.get("evidence") if isinstance(access, dict) else ""
            evidence = evidence if isinstance(evidence, str) and evidence.strip() else 'the shortlist says "%s"' % _plain(stated)
            if isinstance(access, dict):
                access["tier"], access["evidence"] = tier, evidence
            else:
                record["access"] = {"tier": tier, "evidence": evidence}


def access_notes(shortlist):
    """What `render` did with the access words of a shortlist, as lines to print.

    One line for each word that was mapped to a tier and one for each that the
    page cannot show, so that whoever wrote the shortlist can correct it.
    """
    notes = []
    for _, record in _records(shortlist if isinstance(shortlist, dict) else {}):
        stated = _stated_tier(record)
        tier, how = canonical_tier(stated)
        title = _shorten(_plain(record.get("title")) or "untitled dataset", 60)
        if how == "word":
            notes.append('note: access "%s" on "%s" is shown as "%s"' % (_plain(stated), title, _TIER_LABELS[tier]))
        elif how == "unrecognised":
            notes.append('warning: access "%s" on "%s" is not a tier the page knows and is shown as "Unknown"; '
                         'use one of: %s, and put the detail in access.evidence'
                         % (_shorten(_plain(stated), 40), title, ", ".join(ACCESS_TIERS)))
    return notes


# ------------------------------------------------------------------- template

def _read_template():
    # Text mode turns every line ending into "\n", whatever the checkout did.
    with open(TEMPLATE_PATH, encoding="utf-8") as handle:
        return handle.read()


def _script_sources(template):
    """CSP source list (``'sha256-...'``) for the executable inline scripts."""
    scripts = _INLINE_SCRIPT_RE.findall(template)
    if not scripts:
        raise ValueError("report template %s has no inline <script>" % TEMPLATE_PATH)
    sources = []
    for body in scripts:
        if "__SCOUT_" in body:
            raise ValueError("a placeholder inside the page script would break its hash")
        digest = hashlib.sha256(body.encode("utf-8")).digest()
        sources.append("'sha256-%s'" % base64.b64encode(digest).decode("ascii"))
    return " ".join(sources)


# ----------------------------------------------------------------------- data

def _clean(value):
    """Copy `value` into plain JSON types.

    Non-finite numbers become null (``NaN`` is not JSON and would stop the page
    from reading its data), keys become strings, and anything exotic becomes
    its string form instead of raising.
    """
    if value is None or isinstance(value, (bool, str, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(key): _clean(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return [_clean(item) for item in sorted(value, key=str)]
    return str(value)


def _embed_json(data):
    """JSON for a ``<script type="application/json">`` block.

    ``ensure_ascii`` keeps the block independent of the file encoding and
    escapes U+2028/U+2029 and lone surrogates. The three replacements are safe
    because ``<``, ``>`` and ``&`` can only occur inside JSON strings.
    """
    text = json.dumps(data, ensure_ascii=True, allow_nan=False, separators=(",", ":"))
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


# ----------------------------------------------------------------------- text

def _plain(value):
    """Any value as one line of text that is safe to encode as UTF-8."""
    if isinstance(value, bool) or value is None:
        return ""
    if isinstance(value, (int, float)):
        value = str(value)
    if not isinstance(value, str):
        return ""
    value = value.encode("utf-8", "replace").decode("utf-8")  # lone surrogates -> "?"
    return " ".join(_CONTROL_RE.sub("", value).split())


def _shorten(text, limit):
    if len(text) <= limit:
        return text
    head = text[:limit]
    if " " in head:
        head = head.rsplit(" ", 1)[0]
    return head.rstrip(" ,;:.!?-–—") + "…"


def _page_title(data):
    question = _plain(data.get("question"))
    if not question:
        return _TITLE_PREFIX
    return "%s: %s" % (_TITLE_PREFIX, _shorten(question, _TITLE_LIMIT))


def _safe_url(value):
    """The address if it is a plain http(s) URL, else an empty string."""
    if not isinstance(value, str):
        return ""
    value = value.strip()
    return value if _HTTP_URL_RE.match(value) else ""


def _number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value if math.isfinite(value) else None
    if isinstance(value, str) and re.match(r"^\s*-?\d+(\.\d+)?\s*$", value):
        return float(value)
    return None


def _long_date(value):
    match = _DATE_RE.match(_plain(value))
    if not match:
        return ""
    month, day = int(match.group(2)), int(match.group(3))
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return ""
    return "%d %s %s" % (day, _MONTHS[month - 1], match.group(1))


# ------------------------------------------------------- no-JavaScript fallback

def _ranked(datasets):
    """Dataset entries in the order the page shows them: by rank, unranked last."""
    if isinstance(datasets, dict) or _plain(datasets):
        datasets = [datasets]          # a single entry written without the list
    entries = []
    for item in datasets if isinstance(datasets, list) else []:
        if not isinstance(item, dict) and _plain(item):
            item = {"record": {"title": _plain(item)}}   # just a name
        if isinstance(item, dict):
            entries.append(item)

    def key(pair):
        index, entry = pair
        rank = _number(entry.get("rank"))
        return (1, 0, index) if rank is None else (0, rank, index)

    return [entry for _, entry in sorted(enumerate(entries), key=key)]


def _fallback_item(entry):
    record = entry.get("record") if isinstance(entry.get("record"), dict) else entry
    title = _plain(record.get("title")) or "Untitled dataset"
    url = _safe_url(record.get("url"))
    if url:
        name = '<a href="%s" rel="noopener noreferrer">%s</a>' % (
            html.escape(url, quote=True), html.escape(title))
    else:
        name = html.escape(title)

    label = _TIER_LABELS[canonical_tier(_stated_tier(record))[0]]

    licence = record.get("licence")
    if isinstance(licence, dict):
        licence_text = _plain(licence.get("id")) or _plain(licence.get("name"))
    else:
        licence_text = _plain(licence)

    verification = record.get("verification")
    verification = verification if isinstance(verification, dict) else {}
    checked = _long_date(verification.get("checked_at"))
    # "Verified" needs the method and the date the verifier writes; a bare
    # {"verified": true} is a claim, not a check. The page script applies the same rule.
    if verification.get("verified") is True and _plain(verification.get("method")) and checked:
        state = "Verified on %s" % checked
        problems = [_plain(p) for p in verification.get("problems") or [] if _plain(p)] \
            if isinstance(verification.get("problems"), list) else []
        if problems:
            state += ", with problems to check: %s" % "; ".join(problems)
    elif verification.get("verified") is True:
        state = "Not verified (the record gives no method or date of the check)"
    else:
        state = "Not verified"

    facts = "Access: %s. Licence: %s. %s." % (label, licence_text or "not stated", state)
    return "<li><strong>%s</strong><br>%s</li>" % (name, html.escape(facts))


def _fallback_html(data):
    """A plain list of the datasets for viewers that do not run JavaScript
    (file previews, some mail clients). Everything here is escaped."""
    parts = []
    question = _plain(data.get("question"))
    if question:
        parts.append("<p><strong>Research question:</strong> %s</p>" % html.escape(question))
    items = [_fallback_item(entry) for entry in _ranked(data.get("datasets"))]
    if items:
        parts.append("<ol>\n%s\n</ol>" % "\n".join(items))
    else:
        parts.append("<p>This shortlist contains no datasets.</p>")
    checked = _long_date(data.get("generated_at"))
    parts.append("<p>Access conditions and licences change. %s</p>" % html.escape(
        "These were checked on %s." % checked if checked
        else "The date of the check was not recorded."))
    return "\n".join(parts)
