"""OpenAIRE Graph adapter: research products of type dataset, aggregated across repositories.

The Graph API needs no key. Access is taken from `bestAccessRight`, which OpenAIRE
aggregates from the harvested repositories, so it is a metadata claim and not a
guarantee: the landing page remains the final authority.
"""
from __future__ import annotations

import re

from scoutlib import common

NAME = "openaire"
DESCRIPTION = ("OpenAIRE Graph: aggregated research datasets from thousands of repositories; "
               "best-match ranking, aggregated access flag, per-instance licence, citation counts.")
HOSTS = ()

API = "https://api.openaire.eu/graph/v1/researchProducts"

# bestAccessRight.label -> access tier. Anything not listed stays "unknown".
_ACCESS_MAP = {"OPEN": "open", "RESTRICTED": "gated", "EMBARGO": "closed", "CLOSED": "closed"}

# Words that describe the kind of thing wanted rather than its topic; dropped when
# the full query finds too few products and a looser second query is tried.
_GENERIC = {"data", "dataset", "datasets", "database", "databases", "recordings", "recording",
            "prediction", "predicting", "analysis", "study", "studies", "using", "based",
            "of", "for", "the", "and", "with", "in", "on", "a", "an", "to", "from", "by"}
_TOKEN_RE = re.compile(r"[\w']+", re.UNICODE)


def _tokens(query):
    return [t.strip("'") for t in _TOKEN_RE.findall(query or "") if t.strip("'")]


def plain_query(query):
    """The query as plain words: punctuation such as ":" or "/" can be read as query syntax."""
    return " ".join(_tokens(query))


def _relaxed_query(query):
    """Content words only (no stop or generic words); None if nothing would change."""
    kept = [t for t in _tokens(query) if t.lower() not in _GENERIC]
    relaxed = " ".join(kept)
    if not kept or relaxed.lower() == " ".join(_tokens(query)).lower():
        return None
    return relaxed


def access_from_best_access_right(best):
    """Return (tier, evidence) from the `bestAccessRight` object (may be None)."""
    label = (best or {}).get("label") if isinstance(best, dict) else None
    if not label:
        return "unknown", "bestAccessRight=null"
    tier = _ACCESS_MAP.get(str(label).strip().upper(), "unknown")
    return tier, "bestAccessRight=%s" % label


def _pids(item):
    return [p for p in item.get("pids") or [] if isinstance(p, dict)]


def _instances(item):
    return [i for i in item.get("instances") or [] if isinstance(i, dict)]


def _doi_of(item):
    for pid in _pids(item):
        if (pid.get("scheme") or "").lower() == "doi" and pid.get("value"):
            return common.norm_doi(pid["value"])
    return None


# Clinical-trial registries: their records describe a planned study, not data. OpenAIRE
# still labels many of them bestAccessRight=OPEN, which describes the metadata record.
_REGISTRATION_HOSTS = ("trialsearch", "clinicaltrials.gov", "isrctn.com", "clinicaltrialsregister.eu",
                       "anzctr.org.au", "drks.de", "chictr.org.cn", "ctri.nic.in", "trialregister.nl",
                       "umin.ac.jp", "jrct.niph.go.jp", "pactr.samrc.ac.za", "irct.ir", "ensaiosclinicos.gov.br",
                       "cris.nih.go.kr", "who.int/ictrp")
_REGISTRATION_PUBLISHERS = {"nct", "isrctn", "clinicaltrials.gov", "who ictrp", "who international clinical trials "
                            "registry platform", "eu clinical trials register", "anzctr", "drks", "chictr", "ctri"}


def _registration(item):
    """Why this product is a trial registration (a record without data), or None."""
    oid = str(item.get("id") or "")
    if oid.startswith("opentrials__"):
        return "a clinical-trial registration (OpenAIRE source opentrials)"
    publisher = str(item.get("publisher") or "").strip().lower()
    if publisher in _REGISTRATION_PUBLISHERS:
        return "a clinical-trial registration (publisher %s)" % item.get("publisher")
    urls = [str(u) for inst in _instances(item) for u in inst.get("urls") or [] if u]
    if urls and all(any(h in u.lower() for h in _REGISTRATION_HOSTS) for u in urls):
        return "a clinical-trial registration (%s)" % urls[0]
    return None


def _first_licence(item):
    for inst in _instances(item):
        lic = inst.get("license")
        if lic:
            return common.normalise_licence(str(lic)[:200], None)
    return None


def _usage(item):
    usage = {}
    ind = item.get("indicators") or {}
    cites = (ind.get("citationImpact") or {}).get("citationCount")
    if isinstance(cites, (int, float)):
        usage["citations"] = int(cites)
    counts = ind.get("usageCounts") or {}
    for src, dst in (("downloads", "downloads"), ("views", "views")):
        try:
            if counts.get(src) is not None:
                usage[dst] = int(counts[src])
        except (TypeError, ValueError):
            pass
    return usage


def _subjects(item):
    keywords, others = [], []
    for entry in item.get("subjects") or []:
        subj = (entry or {}).get("subject") or {}
        value = subj.get("value")
        if not value:
            continue
        (keywords if subj.get("scheme") == "keyword" else others).append(str(value))
    return keywords + others


def _url_of(item, doi):
    if doi:
        return "https://doi.org/" + doi
    for inst in _instances(item):
        for url in inst.get("urls") or []:
            if str(url).startswith("http"):
                return url
    return "https://explore.openaire.eu/search/result?id=%s" % item.get("id", "")


def record_from_item(item):
    title = item.get("mainTitle") or ""
    if not title:
        return None
    doi = _doi_of(item)
    tier, evidence = access_from_best_access_right(item.get("bestAccessRight"))
    extra = {"openaire_id": item.get("id")}
    registration = _registration(item)
    if registration:
        # The access label is about the registration's metadata; there are no data behind it.
        extra["metadata_only"] = registration
        evidence = "%s describes the metadata record of %s, not data" % (evidence, registration)
        tier = "unknown"
    if item.get("embargoEndDate"):
        extra["embargo_end_date"] = item["embargoEndDate"]
        evidence += "; embargoEndDate=%s" % item["embargoEndDate"]
    if len(_pids(item)) > 1:
        extra["all_dois"] = [common.norm_doi(p["value"]) for p in _pids(item)
                             if (p.get("scheme") or "").lower() == "doi" and p.get("value")][:5]
    date = item.get("publicationDate") or ""
    year = int(date[:4]) if re.match(r"\d{4}", date) else None
    size = {"text": str(item["size"])} if item.get("size") else None
    return common.make_record(
        NAME, item.get("id"), title, _url_of(item, doi),
        access_tier=tier, access_evidence=evidence,
        description=" ".join(str(d) for d in item.get("descriptions") or [] if d)[:3000],
        doi=doi, publisher=item.get("publisher"),
        creators=[a.get("fullName") for a in item.get("authors") or [] if isinstance(a, dict) and a.get("fullName")],
        year=year, version=item.get("version"), updated=date or None,
        licence=_first_licence(item), size=size,
        formats=[str(f) for f in item.get("formats") or [] if f],
        subjects=_subjects(item), usage=_usage(item), extra=extra)


def _query(text, page_size):
    data = common.get_json(API, params={"search": text, "type": "dataset", "pageSize": page_size,
                                        "sortBy": "relevance DESC"})
    if not isinstance(data, dict):
        raise common.FetchError(API, None, "unexpected response shape")
    return common.convert_items(data.get("results") or [], record_from_item, API)


def search(query, limit=20):
    """Best-match OpenAIRE datasets. At most 2 HTTP requests."""
    page = max(1, min(int(limit), 50))
    records, seen = common.Results(), set()

    def add(found):
        records.skipped += found.skipped
        for rec in found:
            if rec["id"] not in seen:
                seen.add(rec["id"])
                records.append(rec)

    add(_query(plain_query(query) or query, page))
    if len(records) < page:
        relaxed = _relaxed_query(query)
        if relaxed:
            add(_query(relaxed, page))
    out = common.Results(records[:limit])
    out.skipped = records.skipped
    return out


# No `lookup`: OpenAIRE hosts no landing pages (HOSTS is empty), and its access label is an
# aggregated claim that, for a DOI of a paper, describes the paper. The hosting registry or
# DataCite answers a lookup instead.
