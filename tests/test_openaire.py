from __future__ import annotations

import os

import pytest

from scoutlib import common
from scoutlib.sources import openaire


def test_field_mapping(fake_http, fixture_json):
    calls = fake_http({"api.openaire.eu/graph/v1/researchProducts": (200, fixture_json("openaire", "search_parkinson.json"))})
    recs = openaire.search("voice recordings Parkinson's disease", limit=5)
    assert 1 <= len(recs) <= 5 and len(calls) <= 3
    first = recs[0]
    assert first["id"].startswith("openaire:") and first["source"] == "openaire"
    assert first["title"] == "Dataset for Parkinson Disease"
    assert first["doi"] == "10.6084/m9.figshare.33212514.v1"
    assert first["url"] == "https://doi.org/10.6084/m9.figshare.33212514.v1"
    assert first["publisher"] == "figshare" and first["year"] == 2026
    assert first["licence"]["id"] == "CC-BY-4.0"
    assert first["access"] == {"tier": "open", "evidence": "bestAccessRight=OPEN"}
    assert first["creators"] and first["usage"].get("citations") == 0
    assert "voice measurements" in first["description"]


def test_unknown_when_access_missing(fake_http, fixture_json):
    fake_http({"researchProducts": (200, fixture_json("openaire", "search_parkinson.json"))})
    recs = openaire.search("voice recordings Parkinson's disease", limit=5)
    missing = [r for r in recs if r["access"]["evidence"] == "bestAccessRight=null"]
    assert missing and all(r["access"]["tier"] == "unknown" for r in missing)


@pytest.mark.parametrize("label,tier", [("OPEN", "open"), ("RESTRICTED", "gated"), ("EMBARGO", "closed"),
                                         ("CLOSED", "closed"), ("OPEN SOURCE", "unknown"),
                                         ("something new", "unknown")])
def test_access_mapping(label, tier):
    got, evidence = openaire.access_from_best_access_right({"label": label})
    assert got == tier and label in evidence


def test_access_null():
    assert openaire.access_from_best_access_right(None)[0] == "unknown"


def test_embargo_date_kept_in_evidence():
    rec = openaire.record_from_item({"id": "x::1", "mainTitle": "T", "embargoEndDate": "2030-01-01",
                                     "bestAccessRight": {"label": "EMBARGO"}})
    assert rec["access"]["tier"] == "closed" and "2030-01-01" in rec["access"]["evidence"]
    assert rec["url"].startswith("https://explore.openaire.eu/")


def test_second_query_when_few_results(fake_http):
    calls = fake_http({"researchProducts": (200, {"results": []})})
    assert openaire.search("voice recordings Parkinson's disease", limit=5) == []
    assert len(calls) == 2 and "recordings" not in calls[1][1]


def test_api_error_raises(fake_http):
    fake_http({"researchProducts": (500, {"message": "boom"})})
    with pytest.raises(common.FetchError):
        openaire.search("anything")


def test_no_lookup_route_through_an_aggregator():
    # M10: the old lookup was unreachable, and OpenAIRE's label for a paper DOI describes the paper.
    from scoutlib.sources import source_for_url

    assert not hasattr(openaire, "lookup") and openaire.HOSTS == ()
    assert source_for_url("https://explore.openaire.eu/search/result?id=x", {"openaire": openaire}) is None


def test_trial_registration_is_not_called_open():
    # S6, the review's live record (2026-11-12) reduced to the fields that matter.
    item = {"id": "opentrials__::52c2a1b3", "mainTitle": "Efficacy of Voice Treatment for Parkinson's Disease",
            "publisher": "nct", "bestAccessRight": {"label": "OPEN"},
            "instances": [{"urls": ["http://apps.who.int/trialsearch/Trial3.aspx?trialid=NCT00123084"]}]}
    rec = openaire.record_from_item(item)
    assert rec["access"]["tier"] == "unknown"
    assert "bestAccessRight=OPEN describes the metadata record of a clinical-trial registration" in rec["access"]["evidence"]
    assert rec["extra"]["metadata_only"]
    for variant in ({"id": "x::1", "publisher": "ISRCTN"},
                    {"id": "x::2", "instances": [{"urls": ["https://clinicaltrials.gov/study/NCT01"]}]}):
        assert openaire.record_from_item(dict(item, **variant))["access"]["tier"] == "unknown"
    data = dict(item, id="r3data::9", publisher="Zenodo", instances=[{"urls": ["https://zenodo.org/records/1"]}])
    assert openaire.record_from_item(data)["access"]["tier"] == "open"


def test_query_punctuation_is_not_sent_as_syntax(fake_http):
    calls = fake_http({"researchProducts": (200, {"results": []})})
    openaire.search("ICU/ward mortality: adults", limit=5)
    assert "search=ICU+ward+mortality+adults" in calls[0][1]


def test_one_malformed_item_does_not_lose_the_others(fake_http, fixture_json):
    data = fixture_json("openaire", "search_parkinson.json")
    data["results"][0]["authors"] = [None]
    data["results"][1]["pids"] = [None, {"scheme": "doi", "value": "10.1/x"}]
    data["results"].insert(2, None)
    fake_http({"researchProducts": (200, data)})
    recs = openaire.search("voice recordings Parkinson's disease", limit=5)
    assert len(recs) == 5 and recs.skipped == 1


@pytest.mark.live
def test_live():
    assert openaire.search("satellite imagery crop yield", limit=3)
