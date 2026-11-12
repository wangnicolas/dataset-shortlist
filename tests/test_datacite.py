from __future__ import annotations

import pytest

from scoutlib import common
from scoutlib.sources import datacite


def test_field_mapping(fake_http, fixture_json):
    calls = fake_http({"api.datacite.org/dois": (200, fixture_json("datacite", "search_parkinson.json"))})
    recs = datacite.search("voice recordings Parkinson's disease", limit=5)
    assert 1 <= len(recs) <= 5 and len(calls) <= 3
    rec = next(r for r in recs if r["title"].startswith("VOC-PD"))
    assert rec["doi"] == "10.5281/zenodo.21775027"
    assert rec["url"] == "https://doi.org/10.5281/zenodo.21775027"
    assert rec["publisher"] == "Zenodo" and rec["year"] == 2026
    assert rec["licence"]["id"] == "CC-BY-4.0"
    assert rec["creators"][0] == "Chen, Min"
    assert rec["access"]["tier"] == "unknown"  # no standard access statement in this record
    assert rec["updated"] == "2026-10-09"
    assert "_sort" not in rec and "_version_of" not in rec


def test_versions_collapsed(fake_http, fixture_json):
    raw = fixture_json("datacite", "search_parkinson.json")
    fake_http({"api.datacite.org/dois": (200, raw)})
    recs = datacite.search("voice recordings Parkinson's disease", limit=20)
    titles = [common.norm_title(r["title"]) for r in recs]
    assert len(titles) == len(set(titles))
    assert len(recs) < len(raw["data"])
    assert any(r["extra"].get("versions_collapsed") for r in recs)


def _item(doi, title, year, rel=None, rights=None, issued="2020-01-01"):
    return {"id": doi, "attributes": {
        "doi": doi, "titles": [{"title": title}], "publisher": "Pub", "publicationYear": year,
        "dates": [{"date": issued, "dateType": "Issued"}], "relatedIdentifiers": rel or [],
        "rightsList": rights or [], "creators": []}}


def test_collapse_keeps_newest_and_links_by_relation():
    items = [_item("10.1/a.v1", "Same", 2020), _item("10.1/a.v3", "Same", 2022),
             _item("10.1/b.v1", "Renamed v1", 2019, [{"relationType": "IsVersionOf", "relatedIdentifier": "10.1/b", "relatedIdentifierType": "DOI"}]),
             _item("10.1/b.v2", "Renamed v2", 2021, [{"relationType": "IsVersionOf", "relatedIdentifier": "10.1/b", "relatedIdentifierType": "DOI"}]),
             _item("10.1/c", "Other", 2018)]
    out = datacite.collapse_versions([datacite.record_from_item(i) for i in items])
    assert [r["doi"] for r in out] == ["10.1/a.v3", "10.1/b.v2", "10.1/c"]


@pytest.mark.parametrize("rights,tier", [
    ([{"rightsUri": "info:eu-repo/semantics/openAccess"}], "open"),
    ([{"rights": "Open Access"}], "open"),
    ([{"rightsUri": "http://purl.org/coar/access_right/c_16ec"}], "gated"),
    ([{"rightsUri": "info:eu-repo/semantics/restrictedAccess"}], "gated"),
    ([{"rightsUri": "info:eu-repo/semantics/embargoedAccess"}], "closed"),
    ([{"rightsUri": "info:eu-repo/semantics/closedAccess"}], "closed"),
    ([{"rights": "Creative Commons Attribution 4.0", "rightsIdentifier": "cc-by-4.0"}], "unknown"),
    ([], "unknown"),
    ([{"rightsUri": "info:eu-repo/semantics/openAccess"}, {"rights": "Restricted Access"}], "gated"),
])
def test_access_tier(rights, tier):
    assert datacite.access_from_rights(rights)[0] == tier


def test_licence_skips_access_statement():
    rec = datacite.record_from_item(_item("10.1/x", "T", 2020, rights=[
        {"rights": "Open Access", "rightsUri": "info:eu-repo/semantics/openAccess"},
        {"rights": "Creative Commons Zero", "rightsUri": "https://creativecommons.org/publicdomain/zero/1.0/"}]))
    assert rec["licence"]["id"] == "CC0-1.0" and rec["access"]["tier"] == "open"
    assert "openAccess" in rec["access"]["evidence"]


def test_api_error_raises(fake_http):
    fake_http({"api.datacite.org": (503, {"errors": []})})
    with pytest.raises(common.FetchError):
        datacite.search("anything")


def test_lookup(fake_http, fixture_json):
    calls = fake_http({"api.datacite.org/dois/10.5281/zenodo.5330729": (200, fixture_json("datacite", "doi_single.json"))})
    rec = datacite.lookup("https://doi.org/10.5281/zenodo.5330729")
    assert rec["doi"] == "10.5281/zenodo.5330729" and rec["publisher"] == "Zenodo"
    assert rec["licence"]["id"] == "CC-BY-4.0" and rec["access"]["tier"] == "open"
    assert len(calls) == 1
    assert datacite.lookup("doi:10.5281/zenodo.5330729")["doi"] == rec["doi"]
    assert datacite.lookup("no doi here") is None


def test_lookup_not_found_returns_none_other_errors_raise(fake_http):
    fake_http({"10.1234/missing": (404, {"errors": [{"status": "404"}]})})
    assert datacite.lookup("10.1234/missing") is None
    fake_http({"10.1234/boom": (500, {})})
    with pytest.raises(common.FetchError):
        datacite.lookup("10.1234/boom")


@pytest.mark.live
def test_live():
    assert datacite.lookup("10.5281/zenodo.5330729")


# ---------------------------------------------- S4: versions are DOI families, not titles

def test_records_that_only_share_a_generic_title_are_not_collapsed():
    items = [_item("10.1234/aaa", "Data", 2020), _item("10.9999/bbb", "Data", 2021)]
    out = datacite.collapse_versions([datacite.record_from_item(i) for i in items])
    assert [r["doi"] for r in out] == ["10.1234/aaa", "10.9999/bbb"]
    assert all("other_dois" not in r["extra"] for r in out)


@pytest.mark.parametrize("dois,families", [
    (["10.17632/hx4b2pcbxy.1", "10.17632/hx4b2pcbxy.2"], 1),        # Mendeley Data versions
    (["10.6084/m9.figshare.20022192", "10.6084/m9.figshare.20022192.v1"], 1),
    (["10.5281/zenodo.123", "10.5281/zenodo.124"], 2),               # two Zenodo records, no relation
    (["10.1594/pangaea.912", "10.1594/pangaea.913"], 2),
])
def test_version_suffixes_form_families(dois, families):
    out = datacite.collapse_versions([datacite.record_from_item(_item(d, "Title %d" % i, 2020 + i))
                                      for i, d in enumerate(dois)])
    assert len(out) == families


def test_family_dois_let_dedupe_match_a_concept_doi_copy():
    # Live 2026-11-12: one figshare item listed twice, once per DOI (DataCite .v1, OpenAIRE concept).
    dc = datacite.collapse_versions([datacite.record_from_item(_item("10.6084/m9.figshare.20022192.v1", "Gait set", 2022))])
    assert "10.6084/m9.figshare.20022192" in dc[0]["extra"]["all_dois"]
    oa = common.make_record("openaire", "x", "Gait set", "https://doi.org/10.6084/m9.figshare.20022192", "open",
                            "bestAccessRight=OPEN", doi="10.6084/m9.figshare.20022192")
    assert len(common.dedupe(dc + [oa])) == 1


def test_null_entries_and_string_years_do_not_lose_the_results(fake_http, fixture_json):
    # M2: the review's cases, each of which used to lose every DataCite result.
    raw = fixture_json("datacite", "search_parkinson.json")
    raw["data"][0]["relationships"] = {"client": {"data": None}}
    raw["data"][1]["attributes"]["creators"] = [None, {"name": "Someone"}]
    raw["data"][2]["attributes"]["publicationYear"] = "2024"
    raw["data"][3]["attributes"]["publicationYear"] = 2023
    raw["data"].append(None)
    fake_http({"api.datacite.org/dois": (200, raw)})
    recs = datacite.search("voice recordings Parkinson's disease", limit=20)
    assert recs and recs.skipped >= 1          # the null item (once per request made)
    assert all(isinstance(r["year"], int) for r in recs if r["year"] is not None)


def test_every_item_malformed_is_an_error_not_an_empty_list(fake_http):
    fake_http({"api.datacite.org/dois": (200, {"data": [None, 3]})})
    with pytest.raises(common.FetchError):
        datacite.search("anything")


def test_query_punctuation_is_not_sent_as_query_syntax(fake_http):
    # X1, reproduced live 2026-11-12: "sepsis mortality: ICU" -> 0 results, "sepsis mortality ICU" -> 149.
    calls = fake_http({"api.datacite.org/dois": (200, {"data": []})})
    datacite.search("sepsis mortality: ICU/ward", limit=5)
    assert "query=sepsis+mortality+ICU+ward&" in calls[0][1]
