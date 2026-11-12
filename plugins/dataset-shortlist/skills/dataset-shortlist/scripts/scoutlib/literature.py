"""Literature lookups: papers on a topic, papers that use a named dataset, works that cite a DOI.

OpenAlex is tried first (abstracts come back as an inverted index and are rebuilt
here). Without a key it gives one small daily budget per IP address; when that is
spent (HTTP 429, or the header x-ratelimit-remaining at 0) this is remembered for
the rest of the process and later calls go straight to the fallbacks. Europe PMC
is the second source: no key, abstracts included, strongest in life sciences and
medicine, with preprints and other fields too. Crossref comes last; it rarely has
abstracts. Every field comes from an API response. At most 3 HTTP requests per call
(retries aside), and no e-mail address or other personal detail is sent.
"""
from __future__ import annotations

import os
import re

from scoutlib import common

OPENALEX = "https://api.openalex.org/works"
EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF = "https://api.crossref.org/works"
DATACITE = "https://api.datacite.org/dois"
ABSTRACT_LIMIT = 1200
_SELECT = ("id,doi,title,publication_year,type,cited_by_count,"
           "primary_location,authorships,abstract_inverted_index")
_SURVEY_WORDS = re.compile(r"\b(review|survey|benchmark|systematic|meta-analysis|overview|scoping)\b", re.I)


def _openalex_params(extra):
    params = {"select": _SELECT}
    params.update(extra)
    # Optional, and only from an EVAL_*-style variable (SPEC rule 3). common.FetchError
    # redacts it, so it never appears in an error message or an --out file.
    key = os.environ.get("EVAL_OPENALEX_KEY")
    if key:
        params["api_key"] = key
    return params


_OPENALEX = {}   # "spent": why OpenAlex is skipped for the rest of this process


def _budget_left(resp):
    """False when OpenAlex says the free budget is used up."""
    if resp.status == 429:
        return False
    value = (resp.header("x-ratelimit-remaining") or "").strip()
    try:
        return not (value and float(value) <= 0)
    except ValueError:
        return True


def _openalex_json(url, params):
    """GET an OpenAlex document, remembering a spent budget for the rest of the process."""
    if _OPENALEX.get("spent"):
        raise common.FetchError(url, None, "skipped: %s" % _OPENALEX["spent"], kind="skipped")
    problem = None
    for attempt in range(common.JSON_TRIES):
        # 429 means the budget is spent: retrying would only wait; 5xx is still retried.
        resp = common.http_request(url, params=params, retry_on=(500, 502, 503, 504))
        if not _budget_left(resp):
            _OPENALEX["spent"] = ("the OpenAlex budget for this address is used up (HTTP %d, x-ratelimit-remaining=%s); "
                                  "later searches in this run use the other sources"
                                  % (resp.status, resp.header("x-ratelimit-remaining") or "not given"))
        if not resp.ok:
            raise common.FetchError(resp.url, resp.status, common.truncate(resp.text(), 200))
        try:
            return resp.json()
        except ValueError as exc:
            problem = common.FetchError(resp.url, resp.status, "invalid JSON after %d tries: %s" % (attempt + 1, exc))
    raise problem


def reconstruct_abstract(inverted, limit=ABSTRACT_LIMIT):
    """Rebuild plain text from an OpenAlex abstract_inverted_index ({word: [positions]})."""
    if not inverted or not isinstance(inverted, dict):
        return None
    slots = {}
    for word, positions in inverted.items():
        for pos in positions or []:
            if isinstance(pos, int):
                slots[pos] = word
    if not slots:
        return None
    text = " ".join(slots[i] for i in sorted(slots))
    return common.truncate(text, limit) or None


def _doi_url(doi):
    return "https://doi.org/" + doi if doi else None


def _work(title, year, venue, doi, url, authors, cited_by, abstract, wtype):
    doi = common.norm_doi(doi)
    return {
        "title": common.strip_html(title) or None,
        "year": year,
        "venue": venue or None,
        "doi": doi,
        "url": url or _doi_url(doi),
        "authors": [a for a in (authors or []) if a][:5],
        "cited_by": cited_by,
        "abstract": abstract,
        "type": wtype,
    }


def _map_openalex(item):
    loc = item.get("primary_location") or {}
    source = loc.get("source") or {}
    authors = [(a.get("author") or {}).get("display_name") for a in item.get("authorships") or []]
    doi = common.norm_doi(item.get("doi"))
    url = _doi_url(doi) or loc.get("landing_page_url") or item.get("id")
    return _work(item.get("title"), item.get("publication_year"), source.get("display_name"),
                 doi, url, authors, item.get("cited_by_count"),
                 reconstruct_abstract(item.get("abstract_inverted_index")), item.get("type"))


def _map_crossref(item):
    title = (item.get("title") or [None])[0]
    venue = (item.get("container-title") or [None])[0]
    parts = ((item.get("issued") or {}).get("date-parts") or [[None]])[0]
    year = parts[0] if parts else None
    authors = []
    for a in item.get("author") or []:
        name = " ".join(x for x in (a.get("given"), a.get("family")) if x) or a.get("name")
        authors.append(name)
    abstract = common.truncate(common.strip_html(item.get("abstract")), ABSTRACT_LIMIT) or None
    return _work(title, year, venue, item.get("DOI"), item.get("URL"), authors,
                 item.get("is-referenced-by-count"), abstract, item.get("type"))


def _boost(works):
    """Stable re-rank: review/survey/benchmark papers move up a few places, nothing is dropped."""
    def key(pair):
        idx, w = pair
        hit = w.get("type") == "review" or _SURVEY_WORDS.search(w.get("title") or "")
        return idx - (3 if hit else 0)
    return [w for _, w in sorted(enumerate(works), key=key)]


def _openalex_search(query, limit, year_from, phrase=False, sort=None):
    flt = []
    if phrase:
        flt.append('title_and_abstract.search:"%s"' % query.replace('"', " ").replace(",", " "))
    if year_from:
        flt.append("from_publication_date:%s-01-01" % int(year_from))
    extra = {"per-page": min(50, max(limit * 2, limit))}
    if phrase:
        extra["filter"] = ",".join(flt)
    else:
        extra["search"] = query
        if flt:
            extra["filter"] = ",".join(flt)
    if sort:
        extra["sort"] = sort
    data = _openalex_json(OPENALEX, _openalex_params(extra))
    return [_map_openalex(r) for r in data.get("results") or []]


_EPMC_TYPES = (("review", "review"), ("review-article", "review"), ("systematic review", "review"),
               ("preprint", "preprint"), ("journal article", "article"), ("research-article", "article"))


def _plain_words(text):
    """Words only: ":" and brackets are query syntax for Europe PMC, as for most search services."""
    return " ".join(re.findall(r"[^\W_][\w'\-]*", text or ""))


def _map_europepmc(item):
    authors = [(a or {}).get("fullName") for a in ((item.get("authorList") or {}).get("author") or [])
               if isinstance(a, dict)]
    if not any(authors) and item.get("authorString"):
        authors = [a.strip() for a in str(item["authorString"]).rstrip(".").split(",")]
    venue = (((item.get("journalInfo") or {}).get("journal") or {}).get("title")
             or (item.get("bookOrReportDetails") or {}).get("publisher"))
    kinds = [str(t).lower() for t in ((item.get("pubTypeList") or {}).get("pubType") or [])]
    wtype = next((name for key, name in _EPMC_TYPES if key in kinds), kinds[0] if kinds else None)
    year = None
    try:
        year = int(str(item.get("pubYear") or "")[:4])
    except ValueError:
        year = None
    url = None
    if not item.get("doi") and item.get("id") and item.get("source"):
        url = "https://europepmc.org/article/%s/%s" % (item["source"], item["id"])
    abstract = common.truncate(common.strip_html(item.get("abstractText")), ABSTRACT_LIMIT) or None
    cited = item.get("citedByCount")
    return _work(item.get("title"), year, venue, item.get("doi"), url, authors,
                 cited if isinstance(cited, int) else None, abstract, wtype)


def _europepmc_search(query, limit, year_from, sort=None):
    text = query
    if year_from:
        text = "(%s) AND PUB_YEAR:[%d TO 3000]" % (query, int(year_from))
    params = {"query": text, "format": "json", "resultType": "core", "pageSize": min(50, max(limit * 2, limit))}
    if sort:
        params["sort"] = sort
    data = common.get_json(EUROPEPMC, params=params)
    items = ((data or {}).get("resultList") or {}).get("result") or []
    return [_map_europepmc(r) for r in items if isinstance(r, dict) and r.get("title")]


def _crossref_search(query, limit, year_from, bibliographic=False):
    params = {
        "query.bibliographic" if bibliographic else "query": query,
        "rows": min(50, max(limit * 2, limit)),
        "select": "DOI,title,container-title,author,issued,URL,is-referenced-by-count,abstract,type",
    }
    if year_from:
        params["filter"] = "from-pub-date:%s" % int(year_from)
    data = common.get_json(CROSSREF, params=params)
    return [_map_crossref(r) for r in (data.get("message") or {}).get("items") or []]


def _result(query, source, works, errors):
    return {"query": query, "source": source, "works": works, "errors": errors}


def search_papers(query, limit=10, year_from=None):
    errors = {}
    try:
        works = _boost(_openalex_search(query, limit, year_from))[:limit]
        if works:
            return _result(query, "openalex", works, errors)
        errors["openalex"] = "no results"
    except common.FetchError as exc:
        errors["openalex"] = str(exc)
    try:
        words = _plain_words(query)
        works = _boost(_europepmc_search(words, limit, year_from))[:limit] if words else []
        if works:
            return _result(query, "europepmc", works, errors)
        errors["europepmc"] = "no results"
    except common.FetchError as exc:
        errors["europepmc"] = str(exc)
    try:
        works = _boost(_crossref_search(query, limit, year_from))[:limit]
        return _result(query, "crossref", works, errors)
    except common.FetchError as exc:
        errors["crossref"] = str(exc)
    return _result(query, None, [], errors)


def papers_mentioning(dataset_name, limit=10):
    errors = {}
    try:
        works = _openalex_search(dataset_name, limit, None, phrase=True, sort="cited_by_count:desc")[:limit]
        if works:
            return _result(dataset_name, "openalex", works, errors)
        errors["openalex"] = "no results"
    except common.FetchError as exc:
        errors["openalex"] = str(exc)
    try:
        phrase = " ".join(str(dataset_name or "").replace('"', " ").split())
        works = _europepmc_search('"%s"' % phrase, limit, None, sort="CITED desc")[:limit] if phrase else []
        if works:
            return _result(dataset_name, "europepmc", works, errors)
        errors["europepmc"] = "no results"
    except common.FetchError as exc:
        errors["europepmc"] = str(exc)
    try:
        works = _crossref_search('"%s"' % dataset_name, limit, None, bibliographic=False)
        works.sort(key=lambda w: -(w.get("cited_by") or 0))
        errors["crossref"] = "fallback: relevance match on metadata, not an exact phrase match"
        return _result(dataset_name, "crossref", works[:limit], errors)
    except common.FetchError as exc:
        errors["crossref"] = str(exc)
    return _result(dataset_name, None, [], errors)


# Relations by which a record says it used or cites the DOI. Version and part relations
# (IsVersionOf, HasVersion, IsPartOf, IsIdenticalTo, ...) link a dataset to itself.
_CITING_RELATIONS = {"cites", "references", "issupplementto", "isderivedfrom", "documents"}


def _family(doi):
    from scoutlib.sources.datacite import doi_family

    return doi_family(doi)


def _datacite_citing(doi, limit):
    """DataCite records that declare that they cite or use this DOI.

    The search matches any relation, so the dataset's own versions come back too (a
    concept DOI lists every version); only citation relations are kept, and records
    of the same DOI family are dropped.
    """
    data = common.get_json(DATACITE, params={
        "query": 'relatedIdentifiers.relatedIdentifier:"%s"' % doi,
        "page[size]": min(25, max(limit * 2, limit))})
    works = []
    family = _family(doi)
    for rec in data.get("data") or []:
        if not isinstance(rec, dict):
            continue
        a = rec.get("attributes") or {}
        own = common.norm_doi(a.get("doi") or rec.get("id"))
        if not own or own == doi or _family(own) == family:
            continue
        relations = {str((r or {}).get("relationType") or "").lower() for r in a.get("relatedIdentifiers") or []
                     if isinstance(r, dict) and common.norm_doi(r.get("relatedIdentifier")) in (doi, family)}
        if not relations & _CITING_RELATIONS:
            continue
        if len(works) >= limit:
            break
        titles = a.get("titles") or [{}]
        creators = [c.get("name") for c in a.get("creators") or [] if isinstance(c, dict)]
        types = a.get("types") or {}
        titles = [t for t in titles if isinstance(t, dict)] or [{}]
        works.append(_work(titles[0].get("title"), a.get("publicationYear"), a.get("publisher"),
                           a.get("doi"), a.get("url"), creators, a.get("citationCount"),
                           common.truncate(common.strip_html(next((d for d in a.get("descriptions") or []
                                                                   if isinstance(d, dict)), {}).get("description")),
                                           ABSTRACT_LIMIT) or None,
                           types.get("resourceTypeGeneral")))
    return works


def papers_citing(doi, limit=10):
    clean = common.norm_doi(doi)
    errors = {}
    if not clean:
        return _result(doi, None, [], {"input": "empty DOI"})
    try:
        meta = _openalex_json("%s/doi:%s" % (OPENALEX, clean), _openalex_params({"select": "id"}))
        wid = str(meta.get("id") or "").rsplit("/", 1)[-1]
        if not wid:
            raise common.FetchError(clean, None, "OpenAlex has no id for this DOI")
        works = _openalex_search_cites(wid, limit)
        if works:
            return _result(clean, "openalex", works, errors)
        errors["openalex"] = "DOI known to OpenAlex but no citing works recorded"
    except common.FetchError as exc:
        errors["openalex"] = str(exc)
    try:
        works = _datacite_citing(clean, limit)
        if works:
            errors["datacite"] = "fallback: DataCite records that declare they cite, reference or derive from this DOI"
            return _result(clean, "datacite", works, errors)
        errors["datacite"] = "no records that cite it (the dataset's own versions are not counted)"
    except common.FetchError as exc:
        errors["datacite"] = str(exc)
    errors["note"] = "no free route returned citing works for this DOI; no results invented"
    return _result(clean, None, [], errors)


def _openalex_search_cites(wid, limit):
    extra = {"filter": "cites:%s" % wid, "sort": "cited_by_count:desc", "per-page": min(50, limit)}
    data = _openalex_json(OPENALEX, _openalex_params(extra))
    return [_map_openalex(r) for r in data.get("results") or []][:limit]
