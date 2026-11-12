"""DataCite adapter: DOI-level metadata for datasets from Zenodo, Dryad, figshare, university repositories and more.

DataCite has no access flag. The access tier is derived only from standard rights
statements in `rightsList` (COAR / eu-repo access-rights URIs or their labels);
without one the tier is "unknown".
"""
from __future__ import annotations

import re
import urllib.parse

from scoutlib import common

NAME = "datacite"
DESCRIPTION = ("DataCite DOI registry: datasets from most data repositories worldwide; "
               "licence from rightsList, no access flag (tier is unknown unless a standard rights statement exists).")
HOSTS = ("doi.org", "dx.doi.org")

API = "https://api.datacite.org/dois"

# (substring of rights URI / identifier / label, tier). Standard COAR and eu-repo access rights only.
_ACCESS_PATTERNS = [
    ("info:eu-repo/semantics/openaccess", "open"),
    ("c_abf2", "open"),
    ("info:eu-repo/semantics/restrictedaccess", "gated"),
    ("c_16ec", "gated"),
    ("info:eu-repo/semantics/embargoedaccess", "closed"),
    ("c_f1cf", "closed"),
    ("info:eu-repo/semantics/closedaccess", "closed"),
    ("c_14cb", "closed"),
]
_ACCESS_LABELS = {"open access": "open", "openaccess": "open", "restricted access": "gated",
                  "restrictedaccess": "gated", "embargoed access": "closed", "embargoedaccess": "closed",
                  "closed access": "closed", "closedaccess": "closed"}
_SEVERITY = {"open": 0, "gated": 1, "closed": 2}

_GENERIC = {"data", "dataset", "datasets", "database", "databases", "recordings", "recording",
            "prediction", "predicting", "analysis", "study", "studies", "using", "based",
            "imagery", "of", "for", "the", "and", "with", "in", "on", "a", "an", "to", "from", "by"}
_TOKEN_RE = re.compile(r"[\w']+", re.UNICODE)
_DOI_RE = re.compile(r"10\.\d{4,9}/\S+")


def _tokens(query):
    return [t.strip("'") for t in _TOKEN_RE.findall(query or "") if t.strip("'")]


def plain_query(query):
    """The query as plain words. DataCite reads `query` as Elasticsearch query_string
    syntax, where "mortality: adults" means the field "mortality" and returns nothing
    without an error (seen live on 2026-11-12), so punctuation is dropped."""
    return " ".join(_tokens(query))


def _relaxed_query(query):
    """AND of the content words. DataCite ANDs bare words anyway, so this only helps
    when generic words ("recordings", "imagery") block matches; None if nothing changes."""
    kept = [t for t in _tokens(query) if t.lower() not in _GENERIC]
    if not kept or len(kept) == len(_tokens(query)):
        return None
    return " AND ".join(kept)


def access_from_rights(rights_list):
    """Return (tier, evidence) from `rightsList`. Most restrictive standard statement wins."""
    found = []
    for entry in rights_list or []:
        if not isinstance(entry, dict):
            continue
        uri = (entry.get("rightsUri") or "").lower()
        ident = (entry.get("rightsIdentifier") or "").lower()
        label = (entry.get("rights") or "").strip().lower()
        tier = None
        for needle, t in _ACCESS_PATTERNS:
            if needle in uri or needle in ident or needle in label:
                tier = t
                break
        if tier is None and label in _ACCESS_LABELS:
            tier = _ACCESS_LABELS[label]
        if tier:
            found.append((tier, "rightsList=%s" % (entry.get("rightsUri") or entry.get("rights") or ident)))
    if not found:
        return "unknown", "no standard access statement in rightsList"
    found.sort(key=lambda f: -_SEVERITY[f[0]])
    return found[0]


def _is_access_statement(entry):
    probe = {"rightsList": [entry]}
    return access_from_rights(probe["rightsList"])[0] != "unknown"


def _licence(rights_list):
    for entry in rights_list or []:
        if not isinstance(entry, dict) or _is_access_statement(entry):
            continue
        name = entry.get("rights") or entry.get("rightsIdentifier")
        uri = entry.get("rightsUri")
        if not name and not uri:
            continue
        if entry.get("rightsIdentifier") and entry.get("rights") and \
                entry["rightsIdentifier"].lower() not in (name or "").lower():
            name = "%s (%s)" % (name, entry["rightsIdentifier"])
        return common.normalise_licence(common.truncate(name, 200) if name else None, uri)
    return None


def _related(attrs, *relation_types):
    out = []
    for rel in attrs.get("relatedIdentifiers") or []:
        rel = rel or {}
        if rel.get("relationType") in relation_types and (rel.get("relatedIdentifierType") or "").upper() == "DOI":
            doi = common.norm_doi(rel.get("relatedIdentifier"))
            if doi:
                out.append(doi)
    return out


def _description(attrs):
    descs = [d for d in attrs.get("descriptions") or [] if isinstance(d, dict)]
    for d in descs:
        if d.get("descriptionType") == "Abstract" and d.get("description"):
            return d["description"]
    for d in descs:
        if d.get("description"):
            return d["description"]
    return ""


def _size(attrs):
    sizes = [str(s) for s in attrs.get("sizes") or [] if s]
    return {"text": "; ".join(sizes)[:200]} if sizes else None


def _issued(attrs):
    for d in attrs.get("dates") or []:
        if isinstance(d, dict) and d.get("dateType") == "Issued" and d.get("date"):
            return str(d["date"])
    return ""


def record_from_item(item):
    attrs = item.get("attributes") or {}
    titles = [t.get("title") for t in attrs.get("titles") or [] if isinstance(t, dict) and t.get("title")]
    doi = common.norm_doi(attrs.get("doi") or item.get("id"))
    if not titles or not doi:
        return None
    tier, evidence = access_from_rights(attrs.get("rightsList"))
    usage = {}
    for src, dst in (("downloadCount", "downloads"), ("viewCount", "views"), ("citationCount", "citations")):
        if isinstance(attrs.get(src), int):
            usage[dst] = attrs[src]
    creators = [c.get("name") for c in attrs.get("creators") or [] if isinstance(c, dict) and c.get("name")]
    subjects = [s.get("subject") for s in attrs.get("subjects") or [] if isinstance(s, dict) and s.get("subject")]
    version = attrs.get("version")
    year = common.as_year(attrs.get("publicationYear"))
    client = (((item.get("relationships") or {}).get("client") or {}).get("data") or {}).get("id")
    record = common.make_record(
        NAME, doi, titles[0], "https://doi.org/" + doi,
        access_tier=tier, access_evidence=evidence,
        description=_description(attrs), doi=doi, publisher=attrs.get("publisher"),
        creators=creators, year=year,
        version=str(version) if version not in (None, "") else None,
        updated=(attrs.get("updated") or "")[:10] or None,
        licence=_licence(attrs.get("rightsList")), size=_size(attrs),
        formats=[str(f) for f in attrs.get("formats") or [] if f], subjects=subjects, usage=usage,
        extra={"landing_page": attrs.get("url"), "state": attrs.get("state"), "client": client})
    # Private grouping hints, removed again by collapse_versions().
    record["_version_of"] = _related(attrs, "IsVersionOf")
    record["_has_version"] = _related(attrs, "HasVersion")
    record["_sort"] = (year or 0, _issued(attrs), bool(_related(attrs, "IsVersionOf")),
                       str(attrs.get("registered") or attrs.get("created") or ""))
    return record


_VERSION_SUFFIX_RE = re.compile(r"^(?P<base>.+)\.v\d+$", re.I)                 # figshare, ICPSR, 4TU: ".v3"
_NUMBER_SUFFIX_RE = re.compile(r"^(?P<prefix>10\.\d+/)(?P<base>[^/]*\d[^/]*)\.\d{1,2}$")  # Mendeley Data: "<id>.2"


def doi_family(doi):
    """The DOI with a version suffix removed; the DOI itself when it has none.

    A bare ".N" counts only when what is left still holds an identifier with a digit,
    so "10.5281/zenodo.123" stays itself while "10.17632/hx4b2pcbxy.2" loses ".2".
    """
    doi = common.norm_doi(doi) or ""
    match = _VERSION_SUFFIX_RE.match(doi)
    if match:
        return match.group("base")
    match = _NUMBER_SUFFIX_RE.match(doi)
    if match:
        return match.group("prefix") + match.group("base")
    return doi


def collapse_versions(records):
    """Keep one record per dataset: the newest of a version family.

    Records are one family only when their DOIs say so: linked by IsVersionOf /
    HasVersion, or the same DOI apart from a version suffix (".v2", Mendeley ".2").
    A shared title is not enough: "Data" or "Dataset" on figshare names many
    unrelated records. The family keeps the position of its best-ranked member;
    `extra.versions_collapsed` counts the dropped records, `extra.other_dois` lists
    them, and `extra.all_dois` holds every DOI of the family so that `common.dedupe`
    can match a copy listed under any of them.
    """
    parent = list(range(len(records)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        parent[find(a)] = find(b)

    first_with = {}
    for i, rec in enumerate(records):
        keys = ["d:" + doi_family(d) for d in [rec["doi"]] + rec.get("_version_of", []) + rec.get("_has_version", []) if d]
        for key in keys:
            if key in first_with:
                union(i, first_with[key])
            else:
                first_with[key] = i
    families = {}
    for i in range(len(records)):
        families.setdefault(find(i), []).append(i)
    out = []
    for members in sorted(families.values(), key=min):
        newest = max(members, key=lambda i: records[i].get("_sort", ()))
        rec = records[newest]
        family = []
        for i in members:
            for doi in [records[i]["doi"]] + records[i].get("_version_of", []):
                for value in (doi, doi_family(doi)):
                    if value and value not in family:
                        family.append(value)
        if len(members) > 1:
            rec["extra"]["versions_collapsed"] = len(members) - 1
            rec["extra"]["other_dois"] = [records[i]["doi"] for i in members if i != newest][:5]
        if len(family) > 1:
            rec["extra"]["all_dois"] = family[:8]
        out.append(rec)
    for rec in out:
        for hidden in ("_version_of", "_has_version", "_sort"):
            rec.pop(hidden, None)
    return out


def _query(text, size):
    data = common.get_json(API, params={"query": text, "resource-type-id": "dataset",
                                        "page[size]": size})
    if not isinstance(data, dict) or not isinstance(data.get("data"), list):
        raise common.FetchError(API, None, "unexpected response shape")
    return common.convert_items(data["data"], record_from_item, API)


def _rank(records, query):
    """Stable re-rank: records whose title/subjects/description mention more query words first.
    DataCite's own order is kept for ties."""
    words = {t.lower() for t in _tokens(query) if t.lower() not in _GENERIC and len(t) > 2}
    if not words:
        return records

    def score(rec):
        title = " ".join(_tokens(rec["title"])).lower()
        body = " ".join(_tokens(" ".join(rec.get("subjects", [])) + " " + rec.get("description", ""))).lower()
        return -(2 * sum(w in title for w in words) + sum(w in body for w in words))

    return sorted(records, key=score)  # sorted() is stable


def search(query, limit=20):
    """Best-match DataCite datasets, versions collapsed. At most 2 HTTP requests."""
    size = max(10, min(int(limit) * 3, 100))  # versions duplicate records, so over-fetch
    first = _query(plain_query(query) or query, size)
    skipped = first.skipped
    records = collapse_versions(list(first))
    if len(records) < limit:
        relaxed = _relaxed_query(query)
        if relaxed:
            more = _query(relaxed, size)
            skipped += more.skipped
            records = collapse_versions(records + list(more))
    out = common.Results(_rank(records, query)[:limit])
    out.skipped = skipped
    return out


def lookup(url_or_id):
    """Fetch one DOI from the DataCite single-DOI endpoint. Returns a record, or None when DataCite does not know it."""
    text = urllib.parse.unquote(str(url_or_id or "").strip())
    match = _DOI_RE.search(text)
    if not match:
        return None
    doi = common.norm_doi(re.sub(r"[?#].*$", "", match.group(0)).rstrip(".,;)"))
    try:
        data = common.get_json(API + "/" + urllib.parse.quote(doi, safe="/"))
    except common.FetchError as exc:
        if exc.status == 404:
            return None
        raise
    item = (data or {}).get("data")
    rec = record_from_item(item) if isinstance(item, dict) else None
    if rec:
        for hidden in ("_version_of", "_has_version", "_sort"):
            rec.pop(hidden, None)
    return rec
