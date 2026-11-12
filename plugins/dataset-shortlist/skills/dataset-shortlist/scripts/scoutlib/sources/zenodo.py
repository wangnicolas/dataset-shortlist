"""Zenodo adapter: general-purpose research repository (any field).

Metadata comes from the public records API; no key is needed. The explicit
`access_right` field (open, restricted, embargoed, closed) is the access
ground truth. Search terms are combined with AND because the default
matching is loose and floods the results with off-topic records.
"""
from __future__ import annotations

import re

from scoutlib import common

NAME = "zenodo"
DESCRIPTION = ("General-purpose research repository; any field; explicit access flag "
               "(open/restricted/embargoed/closed), licence id and file sizes.")
HOSTS = ("zenodo.org",)

API = "https://zenodo.org/api/records"
PAGE_MAX = 25  # anonymous page size limit

_STOP = set("""a an and are as at be by can do does for from has have how i in into is it its
of on or our that the their this to using use used via was were what when where which who
will with within without about across among between over under data dataset datasets
looking find need want study studying research""".split())
# Words that describe a kind of data rather than the subject; dropped in the looser passes.
_GENERIC = set("""time series prediction predict predicting recording recordings imagery image images
analysis model models learning classification detection forecasting forecast sample samples
collection database set open public""".split())

# Zenodo licence ids that the shared normaliser would not recognise.
_LICENCE_ALIASES = {"cc-zero": "CC0-1.0", "cc0-1.0": "CC0-1.0"}

_ACCESS = {
    "open": "open",
    "restricted": "gated",
    "embargoed": "closed",
    "closed": "closed",
}


def _terms(query):
    out = []
    for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9\-]*(?:'[a-z]+)?", query or ""):
        tok = re.sub(r"'s$", "", tok, flags=re.I).strip("-")
        if tok and tok.lower() not in _STOP and tok.lower() not in [t.lower() for t in out]:
            out.append(tok)
    return out


def _is_acronym(term):
    return 2 <= len(term) <= 6 and term.isupper() and any(c.isalpha() for c in term)


def build_queries(query):
    """Up to three query strings, strictest first (all AND-combined)."""
    terms = _terms(query)
    if not terms:
        return [query or ""]
    specific = [t for t in terms if t.lower() not in _GENERIC] or terms
    # The loosest pass keeps two words: acronyms typed in capitals ("ICU", "EEG") first,
    # because a short specific term says more than a long common one; then the longest.
    top2 = sorted(specific, key=lambda t: (not _is_acronym(t), -len(t)))[:2]
    top2 = [t for t in specific if t in top2]
    queries = []
    for group in (terms, specific, top2):
        q = " AND ".join(group)
        if q not in queries:
            queries.append(q)
    return queries[:3]


def _access(meta):
    raw = meta.get("access_right")
    if not raw:
        return "unknown", "access_right missing"
    tier = _ACCESS.get(str(raw).lower())
    if tier is None:
        return "unknown", "access_right=%s (unrecognised value)" % raw
    evidence = "access_right=%s" % raw
    if raw == "embargoed" and meta.get("embargo_date"):
        evidence += " (until %s)" % meta["embargo_date"]
    return tier, evidence


def _licence(meta):
    lic = meta.get("license")
    lic_id = lic.get("id") if isinstance(lic, dict) else (lic or None)
    if not lic_id:
        return None
    mapped = _LICENCE_ALIASES.get(str(lic_id).lower())
    result = common.normalise_licence(mapped or lic_id)
    if result and mapped is None and result.get("id") is None:
        result["name"] = str(lic_id)
    elif result and mapped:
        result["name"] = str(lic_id)
    return result


def _size(files):
    if not files:
        return None
    total = 0
    files = [f for f in files if isinstance(f, dict)]
    for f in files:
        try:
            total += int(f.get("size") or 0)
        except (TypeError, ValueError):
            pass
    return {"bytes": total, "files": len(files)}


def _formats(files):
    seen = []
    for f in files or []:
        if not isinstance(f, dict):
            continue
        key = str(f.get("key") or "")
        if "." in key:
            ext = key.rsplit(".", 1)[1].lower()
            if 0 < len(ext) <= 8 and ext not in seen:
                seen.append(ext)
    return seen


def _record(hit):
    meta = hit.get("metadata") or {}
    rid = hit.get("id") or hit.get("recid")
    links = hit.get("links") or {}
    url = links.get("self_html") or "https://zenodo.org/records/%s" % rid
    tier, evidence = _access(meta)
    stats = hit.get("stats") or {}
    usage = {}
    if "downloads" in stats:
        usage["downloads"] = stats["downloads"]
    if "views" in stats:
        usage["views"] = stats["views"]
    pub = meta.get("publication_date") or ""
    year = int(pub[:4]) if re.match(r"^\d{4}", pub) else None
    extra = {"access_right": meta.get("access_right"), "record_id": str(rid)}
    if hit.get("conceptrecid"):
        extra["concept_record_id"] = str(hit["conceptrecid"])
    if hit.get("conceptdoi"):
        extra["concept_doi"] = common.norm_doi(hit["conceptdoi"])
    if meta.get("embargo_date"):
        extra["embargo_date"] = meta["embargo_date"]
    rtype = (meta.get("resource_type") or {})
    if rtype.get("type"):
        extra["resource_type"] = rtype["type"]
    kw = [str(k) for k in meta.get("keywords") or [] if k]
    files = hit.get("files") or []
    return common.make_record(
        NAME, rid, meta.get("title") or hit.get("title") or "", url,
        access_tier=tier, access_evidence=evidence,
        description=meta.get("description") or "",
        doi=hit.get("doi") or meta.get("doi"),
        publisher="Zenodo",
        creators=[c.get("name") for c in (meta.get("creators") or []) if isinstance(c, dict) and c.get("name")],
        year=year,
        version=meta.get("version"),
        updated=(hit.get("updated") or hit.get("modified") or "")[:10] or None,
        licence=_licence(meta),
        size=_size(files),
        formats=_formats(files),
        subjects=kw,
        usage=usage,
        extra=extra,
    )


def search(query, limit=20):
    limit = max(1, int(limit))
    size = min(PAGE_MAX, max(limit, 10))
    merged, seen = common.Results(), set()
    for q in build_queries(query):
        data = common.get_json(API, params={"q": q, "type": "dataset", "size": size,
                                            "sort": "bestmatch"})
        hits = [h for h in ((data.get("hits") or {}).get("hits") or []) if isinstance(h, dict)]
        fresh = []
        for hit in hits:
            key = hit.get("conceptrecid") or hit.get("id")
            if key in seen:
                continue  # another version of a record already listed
            seen.add(key)
            fresh.append(hit)
        found = common.convert_items(fresh, _record, API)
        merged.skipped += found.skipped
        merged.extend(found)
        if len(merged) >= limit:
            break
    out = common.Results(merged[:limit])
    out.skipped = merged.skipped
    return out


def _record_id(url_or_id):
    text = str(url_or_id or "").strip()
    if re.fullmatch(r"\d+", text):
        return text
    m = re.search(r"zenodo\.org/(?:api/)?records?/(\d+)", text, re.I)
    if m:
        return m.group(1)
    m = re.search(r"10\.5281/zenodo\.(\d+)", text, re.I)
    if m:
        return m.group(1)
    m = re.search(r"zenodo\.org/doi/(10\.[^\s?#]+)", text, re.I)
    if m:
        return ("doi", m.group(1))
    return None


def lookup(url_or_id):
    """Fetch one record by URL, numeric id or Zenodo DOI; None if it is not Zenodo."""
    rid = _record_id(url_or_id)
    if rid is None:
        return None
    if isinstance(rid, tuple):
        # /doi/ links resolve to the latest version through the search endpoint.
        data = common.get_json(API, params={"q": 'doi:"%s"' % rid[1], "size": 1})
        hits = (data.get("hits") or {}).get("hits") or []
        return _record(hits[0]) if hits else None
    try:
        hit = common.get_json("%s/%s" % (API, rid))
    except common.FetchError as exc:
        if exc.status == 404:
            return None
        raise
    return _record(hit)
