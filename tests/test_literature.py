from __future__ import annotations

import json

from scoutlib import common, literature

OA = "api.openalex.org/works"
EPMC = "ebi.ac.uk/europepmc/webservices/rest/search"


def test_reconstruct_abstract_orders_words_and_truncates():
    inv = {"world": [1], "Hello": [0], "again": [2, 3]}
    assert literature.reconstruct_abstract(inv) == "Hello world again again"
    assert literature.reconstruct_abstract(None) is None
    assert literature.reconstruct_abstract({}) is None
    long = {"w%d" % i: [i] for i in range(1000)}
    assert len(literature.reconstruct_abstract(long)) <= 1200


def test_openalex_field_mapping(fake_http, fixture_json):
    fake_http({OA: (200, fixture_json("literature", "openalex_search.json"))})
    res = literature.search_papers("early sepsis prediction intensive care", limit=3)
    assert res["source"] == "openalex" and res["errors"] == {}
    assert len(res["works"]) == 3
    w = res["works"][0]
    assert set(w) == {"title", "year", "venue", "doi", "url", "authors", "cited_by", "abstract", "type"}
    assert w["title"] and isinstance(w["year"], int) and len(w["authors"]) <= 5
    assert w["doi"] and not w["doi"].startswith("http")
    assert w["url"].startswith("http")
    assert any(x["abstract"] for x in res["works"])


def test_crossref_fallback_when_openalex_fails(fake_http, fixture_json):
    calls = fake_http({OA: (429, {"error": "budget"}),
                       "api.crossref.org/works": (200, fixture_json("literature", "crossref_search.json"))})
    res = literature.search_papers("early sepsis prediction intensive care", limit=3)
    assert res["source"] == "crossref"
    assert "openalex" in res["errors"]
    w = res["works"][0]
    assert w["title"] and w["doi"] and w["url"]
    assert isinstance(w["year"], int)
    assert len(calls) <= 3


def test_all_sources_fail(fake_http):
    fake_http({OA: (500, {}), EPMC: (503, {}), "api.crossref.org": (503, {})})
    res = literature.search_papers("x")
    assert res["works"] == [] and res["source"] is None
    assert set(res["errors"]) == {"openalex", "europepmc", "crossref"}


def test_year_filter_sent_to_both_sources(fake_http, fixture_json):
    calls = fake_http({OA: (500, {}),
                       "api.crossref.org/works": (200, fixture_json("literature", "crossref_search.json"))})
    literature.search_papers("topic", limit=3, year_from=2022)
    urls = [u for _, u in calls]
    assert any("from_publication_date%3A2022-01-01" in u or "from_publication_date:2022-01-01" in u for u in urls)
    assert any("from-pub-date%3A2022" in u or "from-pub-date:2022" in u for u in urls)


def test_review_papers_ranked_slightly_higher():
    plain = [{"title": "A %d" % i, "type": "article"} for i in range(5)]
    plain.append({"title": "A systematic review of things", "type": "article"})
    out = literature._boost(plain)
    assert [w["title"] for w in out].index("A systematic review of things") < 5
    assert len(out) == 6


def test_papers_mentioning_uses_phrase_filter_sorted_by_citations(fake_http, fixture_json):
    calls = fake_http({OA: (200, fixture_json("literature", "openalex_search.json"))})
    res = literature.papers_mentioning("Some Dataset", limit=2)
    assert len(res["works"]) == 2
    url = calls[0][1]
    assert "title_and_abstract.search" in url and "cited_by_count%3Adesc" in url


def test_papers_citing_resolves_doi_then_cites(fake_http, fixture_json):
    calls = fake_http({"works/doi:10.1/abc": (200, fixture_json("literature", "openalex_doi.json")),
                       "filter=cites%3AW6960102814": (200, fixture_json("literature", "openalex_cites.json"))})
    res = literature.papers_citing("https://doi.org/10.1/ABC", limit=2)
    assert res["source"] == "openalex" and len(res["works"]) == 2
    assert res["query"] == "10.1/abc"
    assert len(calls) == 2


def test_papers_citing_no_route_returns_empty_with_message(fake_http):
    fake_http({OA: (404, {}), "api.datacite.org": (200, {"data": []})})
    res = literature.papers_citing("10.1/none")
    assert res["works"] == [] and res["source"] is None
    assert "no free route" in res["errors"]["note"]
    assert "openalex" in res["errors"]


def test_key_env_is_used_without_mailto(fake_http, fixture_json, monkeypatch):
    monkeypatch.setenv("EVAL_OPENALEX_KEY", "k123")
    calls = fake_http({OA: (200, fixture_json("literature", "openalex_search.json"))})
    literature.search_papers("q", limit=1)
    assert "api_key=k123" in calls[0][1] and "mailto" not in calls[0][1]


def test_optional_key_is_never_echoed_and_only_the_eval_variable_is_read(fake_http, monkeypatch):
    import json

    monkeypatch.setenv("EVAL_OPENALEX_KEY", "SECRET-KEY-123")
    monkeypatch.setenv("OPENALEX_API_KEY", "OTHER-KEY-456")
    calls = fake_http({OA: (503, {"error": "down"}), "api.crossref.org/works": (503, {"error": "down"})})
    res = literature.search_papers("early sepsis prediction", limit=3)
    assert "SECRET-KEY-123" not in json.dumps(res) and "api_key=REDACTED" in json.dumps(res["errors"])
    assert any("api_key=SECRET-KEY-123" in url for _, url in calls)      # it is sent, just never shown
    monkeypatch.delenv("EVAL_OPENALEX_KEY")
    assert "api_key" not in literature._openalex_params({})            # OPENALEX_API_KEY is not read


def test_datacite_fallback_lists_works_that_cite_not_the_datasets_own_versions(fake_http):
    # S7: the review's case, a Zenodo concept DOI whose "citing works" were its own version record.
    concept = "10.5281/zenodo.17753640"

    def item(doi, title, relation, rtype="Dataset"):
        return {"id": doi, "attributes": {"doi": doi, "titles": [{"title": title}], "publicationYear": 2025,
                                          "types": {"resourceTypeGeneral": rtype},
                                          "relatedIdentifiers": [{"relationType": relation, "relatedIdentifier": concept,
                                                                  "relatedIdentifierType": "DOI"}]}}

    fake_http({OA: (404, {"error": "not found"}),
               "api.datacite.org/dois": (200, {"data": [
                   item("10.5281/zenodo.17753641", "The dataset, version 1", "IsVersionOf"),
                   item("10.5281/zenodo.99", "A model trained on it", "IsDerivedFrom", "Software"),
                   item("10.1234/paper.1", "A paper that uses it", "References", "Text"),
                   item("10.1234/other.2", "A collection that holds it", "HasPart", "Collection")]})})
    res = literature.papers_citing(concept, limit=5)
    assert res["source"] == "datacite"
    assert [w["doi"] for w in res["works"]] == ["10.5281/zenodo.99", "10.1234/paper.1"]


# ---------------------------------------------- Europe PMC, the second source (P2)

def test_europepmc_field_mapping(fake_http, fixture_json):
    # Recorded 2026-11-12 (resultType=core, pageSize=3; affiliations removed from the fixture).
    raw = fixture_json("literature", "europepmc_search.json")
    fake_http({OA: (429, {"error": "budget"}), EPMC: (200, raw)})
    res = literature.search_papers("early sepsis prediction intensive care", limit=3)
    assert res["source"] == "europepmc" and "openalex" in res["errors"]
    assert len(res["works"]) == 3
    for work, item in zip(sorted(res["works"], key=lambda w: w["doi"]),
                          sorted(raw["resultList"]["result"], key=lambda r: r["doi"].lower())):
        assert set(work) == {"title", "year", "venue", "doi", "url", "authors", "cited_by", "abstract", "type"}
        assert work["title"] == item["title"] and work["year"] == int(item["pubYear"])
        assert work["doi"] == item["doi"].lower() and work["url"] == "https://doi.org/" + work["doi"]
        assert work["authors"] and len(work["authors"]) <= 5 and work["authors"][0] == item["authorList"]["author"][0]["fullName"]
        assert work["cited_by"] == item["citedByCount"]
        assert work["abstract"] and "<h4>" not in work["abstract"]
    by_type = {w["type"]: w for w in res["works"]}
    assert set(by_type) == {"article", "review", "preprint"}
    assert by_type["preprint"]["venue"] == "medRxiv"
    assert by_type["article"]["venue"] == "World journal of clinical pediatrics"


def test_order_is_openalex_then_europepmc_then_crossref(fake_http, fixture_json):
    calls = fake_http({OA: (200, {"results": []}), EPMC: (200, {"resultList": {"result": []}}),
                       "api.crossref.org/works": (200, fixture_json("literature", "crossref_search.json"))})
    res = literature.search_papers("early sepsis prediction intensive care", limit=3)
    assert res["source"] == "crossref" and res["errors"]["openalex"] == "no results"
    assert res["errors"]["europepmc"] == "no results"
    assert [h for h in ("openalex", "europepmc", "crossref") for _, u in calls if h in u] == ["openalex", "europepmc", "crossref"]
    assert len(calls) == 3


def test_europepmc_gets_the_year_filter_and_plain_words(fake_http, fixture_json):
    calls = fake_http({OA: (500, {}), EPMC: (200, fixture_json("literature", "europepmc_search.json"))})
    literature.search_papers("ICU/ward mortality: adults", limit=3, year_from=2022)
    query = [u for _, u in calls if "europepmc" in u][0]
    assert "query=%28ICU+ward+mortality+adults%29+AND+PUB_YEAR%3A%5B2022+TO+3000%5D" in query
    assert "resultType=core" in query and "format=json" in query


def test_papers_mentioning_asks_europepmc_for_the_quoted_name(fake_http, fixture_json):
    calls = fake_http({OA: (429, {}), EPMC: (200, fixture_json("literature", "europepmc_phrase.json"))})
    res = literature.papers_mentioning("MIMIC-IV", limit=3)
    assert res["source"] == "europepmc" and len(res["works"]) == 3
    url = [u for _, u in calls if "europepmc" in u][0]
    assert "query=%22MIMIC-IV%22" in url and "sort=CITED+desc" in url


def test_a_spent_openalex_budget_is_remembered_for_the_rest_of_the_process(fake_http, fixture_json):
    calls = fake_http({OA: (429, {"error": "budget"}), EPMC: (200, fixture_json("literature", "europepmc_search.json"))})
    literature.search_papers("first topic", limit=3)
    assert sum(1 for _, u in calls if "openalex" in u) == 1          # a 429 is not retried
    second = literature.search_papers("second topic", limit=3)
    assert sum(1 for _, u in calls if "openalex" in u) == 1          # not asked again
    assert second["source"] == "europepmc" and "budget for this address is used up" in second["errors"]["openalex"]


def test_a_zero_remaining_header_uses_this_answer_and_skips_openalex_later(monkeypatch, fixture_json):
    seen = []
    oa = json.dumps(fixture_json("literature", "openalex_search.json")).encode()
    epmc = json.dumps(fixture_json("literature", "europepmc_search.json")).encode()

    def fake(url, params=None, **kw):
        seen.append(url)
        if "openalex" in url:
            return common.HttpResponse(200, url, {"Content-Type": "application/json", "x-ratelimit-remaining": "0"}, oa)
        return common.HttpResponse(200, url, {"Content-Type": "application/json"}, epmc)

    monkeypatch.setattr(common, "http_request", fake)
    assert literature.search_papers("first", limit=2)["source"] == "openalex"
    assert literature.search_papers("second", limit=2)["source"] == "europepmc"
    assert sum(1 for u in seen if "openalex" in u) == 1
