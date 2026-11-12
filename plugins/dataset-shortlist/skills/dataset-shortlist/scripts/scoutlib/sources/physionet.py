"""PhysioNet adapter.

PhysioNet publishes its whole catalogue as one JSON list at
/api/v1/project/published/ (every published version of every project, no paging;
a `search` parameter is accepted but ignored). So `search` fetches that list once
per process and ranks it locally; `lookup` reads the same list.

Access is stated per project in `access_policy`: Open, Restricted, Credentialed
or Contributor Review. Anything else maps to `unknown`.
"""
from __future__ import annotations

import re

from scoutlib import common

NAME = "physionet"
DESCRIPTION = ("PhysioNet: physiological signals and clinical research data (databases, challenges, models); "
               "explicit access policy per project (open, registered, credentialed, contributor review).")
HOSTS = ("physionet.org",)

API_URL = "https://physionet.org/api/v1/project/published/"
BASE = "https://physionet.org"

# registry value (lower case) -> (tier, plain-language meaning)
_POLICY_TIERS = {
    "open": ("open", "anyone can download"),
    "restricted": ("account", "logged-in users who sign the data use agreement"),
    "credentialed": ("gated", "credentialed users who complete training and sign the agreement"),
    "contributor review": ("gated", "approval by the data contributor"),
}

_STOP = set("""a an and are as at be by for from in into is it of on or that the this to with using use via
based data dataset datasets database databases study studies analysis new set sets""".split())

_CACHE = {}
_DISK_TTL_SECONDS = 6 * 3600


def _disk_cache_path():
    """A file in the system temp directory, never inside the skill directory.

    The catalogue is one request, but every command line call is a new process,
    and the registry's source code describes a low hourly limit for anonymous
    clients. Reusing the list for a few hours keeps a whole session to one request.
    """
    import os
    import tempfile

    folder = os.environ.get("DATASET_SCOUT_CACHE") or os.path.join(tempfile.gettempdir(), "dataset-shortlist-cache")
    return os.path.join(folder, "physionet_published.json")


def _read_disk_cache():
    import json
    import os
    import time

    try:
        path = _disk_cache_path()
        if time.time() - os.path.getmtime(path) > _DISK_TTL_SECONDS:
            return None
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload if isinstance(payload, list) and payload else None
    except (OSError, ValueError):
        return None


def _write_disk_cache(payload):
    import json
    import os

    try:
        path = _disk_cache_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path + ".part", "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        os.replace(path + ".part", path)
    except OSError:
        pass  # a read-only or sandboxed temp directory must not break the search


def _fetch_all():
    if "all" not in _CACHE:
        payload = _read_disk_cache()
        if payload is None:
            payload = common.get_json(API_URL)
            if not isinstance(payload, list):
                raise common.FetchError(API_URL, None, "unexpected response shape (not a list)")
            _write_disk_cache(payload)
        _CACHE["all"] = payload
    return _CACHE["all"]


def _latest(entries):
    """One entry per slug: the one flagged is_latest_version (else the highest listed)."""
    latest = {}
    for entry in entries:
        slug = entry.get("slug")
        if not slug:
            continue
        if entry.get("is_latest_version") or slug not in latest:
            latest[slug] = entry
    return latest


def _tier(policy):
    raw = (policy or "").strip()
    tier, meaning = _POLICY_TIERS.get(raw.lower(), ("unknown", None))
    if meaning:
        evidence = "access_policy=%s (%s)" % (raw, meaning)
    elif raw:
        evidence = "access_policy=%s (value not recognised; check the landing page)" % raw
    else:
        evidence = "access_policy missing in the registry record"
    return tier, evidence


def _record(entry):
    tier, evidence = _tier(entry.get("access_policy"))
    lic = entry.get("license") or {}
    dua = entry.get("dua") or {}
    if tier == "open" and dua.get("name"):
        # A few records are listed as Open and still carry a data use agreement.
        # Open means no agreement, so do not call these open on the policy field alone.
        tier = "unknown"
        evidence = ("access_policy=%s but the record carries a data use agreement (%s); "
                    "read the landing page before calling it open" % (entry.get("access_policy"), dua["name"]))
    url = entry.get("source_url") or "%s/content/%s/%s/" % (BASE, entry.get("slug"), entry.get("version"))
    date = entry.get("publish_date") or (entry.get("publish_datetime") or "")[:10] or None
    size = entry.get("main_storage_size")
    size_obj = {"bytes": size, "text": _human_bytes(size)} if isinstance(size, int) and size > 0 else None
    extra = {"access_policy": entry.get("access_policy"), "resource_type": entry.get("resource_type"),
             "slug": entry.get("slug")}
    if dua.get("name"):
        extra["data_use_agreement"] = dua["name"]
    if entry.get("core_doi"):
        extra["project_doi"] = entry["core_doi"]
    return common.make_record(
        NAME, entry.get("slug"), entry.get("title") or entry.get("slug"), url, tier, evidence,
        description=entry.get("abstract") or entry.get("short_description") or "",
        doi=entry.get("version_doi") or entry.get("core_doi") or entry.get("doi"),
        publisher="PhysioNet",
        year=int(date[:4]) if date and date[:4].isdigit() else None,
        version=entry.get("version"), updated=date,
        licence=common.normalise_licence(lic.get("name"), lic.get("url")) if lic.get("name") or lic.get("url") else None,
        size=size_obj, subjects=list(entry.get("topics") or []), extra=extra)


def _human_bytes(n):
    value = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1000 or unit == "TB":
            return ("%.0f %s" % (value, unit)) if unit == "B" else ("%.1f %s" % (value, unit))
        value /= 1000.0


def _terms(text):
    out = []
    for tok in re.findall(r"[a-z0-9]+", (text or "").lower()):
        if tok in _STOP or len(tok) < 2:
            continue
        out.append(_stem(tok))
    return out


def _stem(tok):
    for suffix in ("ing", "ed", "es", "s"):
        if len(tok) > len(suffix) + 3 and tok.endswith(suffix):
            return tok[: -len(suffix)]
    return tok


def _rank(entries, query):
    q_terms = list(dict.fromkeys(_terms(query)))
    if not q_terms:
        return []
    docs = []
    for e in entries:
        docs.append((e,
                     set(_terms(e.get("title"))),
                     set(_terms(" ".join(e.get("topics") or []))),
                     set(_terms(e.get("short_description"))),
                     set(_terms(common.strip_html(e.get("abstract"))))))
    n = float(len(docs)) or 1.0
    scored = []
    idf = {}
    for t in q_terms:
        df = sum(1 for d in docs if t in d[1] or t in d[2] or t in d[3] or t in d[4])
        idf[t] = 1.0 + (n / (1.0 + df)) ** 0.5 if df else 0.0
    # A project must cover at least half of the query's words, and at least one of
    # them outside the long abstract. Without this floor a query from another field
    # ("smart meter household electricity") returns projects that share one common
    # word, which wastes the reader's attention and looks like a finding.
    needed = (len(q_terms) + 1) // 2
    for e, title, topics, short, abstract in docs:
        score = 0.0
        matched = 0
        anchored = False
        for t in q_terms:
            s = (3.0 if t in title else 0.0) + (2.0 if t in topics else 0.0) + (1.5 if t in short else 0.0) \
                + (1.0 if t in abstract else 0.0)
            if s:
                matched += 1
                anchored = anchored or t in title or t in topics or t in short
            score += s * idf[t]
        if matched >= needed and anchored:
            score *= 0.5 + 0.5 * matched / len(q_terms)  # reward covering more of the query
            scored.append((score, e))
    scored.sort(key=lambda pair: (-pair[0], pair[1].get("title") or ""))
    return [e for _, e in scored]


def search(query, limit=20, include_software=False):
    """Rank the latest version of every published project against the query (one HTTP request)."""
    latest = _latest(_fetch_all())
    pool = [e for e in latest.values()
            if include_software or (e.get("resource_type") or "").lower() != "software"]
    return [_record(e) for e in _rank(pool, query)[: max(0, int(limit))]]


_VERSION_RE = re.compile(r"^\d+(?:\.\d+)*$")


def _parse(url_or_slug):
    """(slug, version or None). The version is the first of the next two path segments that looks
    like one, so /content/<slug>/metrics/3.1/ or /view-license/3.1/ read as version 3.1, and a
    page such as /content/<slug>/metrics/ names no version."""
    text = (url_or_slug or "").strip()
    match = re.search(r"physionet\.org/(?:content|files)/([^/?#\s]+)((?:/[^/?#\s]+){0,2})", text)
    if match:
        version = next((seg for seg in match.group(2).split("/") if _VERSION_RE.match(seg)), None)
        return match.group(1), version
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", text):
        return text, None
    return None, None


def _licence_word(rec):
    lic = rec.get("licence") or {}
    return lic.get("id") or lic.get("name") or "none stated"


def lookup(url_or_slug):
    """Record for the version a URL names, or for the latest version; None if PhysioNet has no such slug.

    Access policy and licence can change between versions (a project may move from
    Restricted to Open, or the reverse), so a link to an old version is answered with
    that version's own policy, licence, DOI and address. The latest version is named
    in `extra.latest_version` and `extra.version_note`. A version the catalogue does
    not list gives the latest version's record with `extra.version_not_listed`.
    """
    slug, version = _parse(url_or_slug)
    if not slug:
        return None
    entries = [e for e in _fetch_all() if e.get("slug") == slug]
    if not entries:
        return None
    latest = _latest(entries)[slug]
    latest_version = str(latest.get("version") or "")
    if not version or version == latest_version:
        return _record(latest)
    match = next((e for e in entries if str(e.get("version") or "") == version), None)
    if match is None:
        rec = _record(latest)
        rec["extra"].update({
            "requested_version": version, "version_not_listed": True,
            "version_note": "PhysioNet lists no version %s of this project (listed: %s); this record is the latest "
                            "version %s" % (version, ", ".join(str(e.get("version")) for e in entries), latest_version)})
        return rec
    rec = _record(match)
    newest = _record(latest)
    rec["extra"].update({
        "latest_version": latest_version,
        "latest_url": newest["url"],
        "latest_access": dict(newest["access"]),
        "latest_licence": _licence_word(newest),
        "version_note": "this record describes version %s, as the link asks; the latest version is %s (access %s, "
                        "licence %s) at %s" % (version, latest_version, newest["access"]["tier"],
                                              _licence_word(newest), newest["url"])})
    return rec
