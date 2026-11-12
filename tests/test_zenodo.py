"""Offline tests for the Zenodo adapter (recorded responses)."""
from __future__ import annotations

import copy
import os

import pytest

from scoutlib import common
from scoutlib.sources import zenodo


def test_field_mapping(fixture_json):
    hit = fixture_json("zenodo", "record.json")
    rec = zenodo._record(hit)
    assert rec["id"] == "zenodo:17753641"
    assert rec["source"] == "zenodo"
    assert rec["url"] == "https://zenodo.org/records/17753641"
    assert rec["access"] == {"tier": "open", "evidence": "access_right=open"}
    assert rec["doi"] == hit["doi"].lower()
    assert rec["extra"]["concept_doi"] == "10.5281/zenodo.17753640"
    assert rec["licence"]["id"] == "MIT"
    assert rec["size"]["files"] == len(hit["files"])
    assert rec["size"]["bytes"] == sum(f["size"] for f in hit["files"])
    assert rec["usage"]["downloads"] == hit["stats"]["downloads"]
    assert rec["usage"]["views"] == hit["stats"]["views"]
    assert rec["year"] == int(hit["metadata"]["publication_date"][:4])
    assert "<" not in rec["description"]


@pytest.mark.parametrize("raw,tier", [("open", "open"), ("restricted", "gated"),
                                      ("embargoed", "closed"), ("closed", "closed")])
def test_access_mapping(fixture_json, raw, tier):
    hit = copy.deepcopy(fixture_json("zenodo", "record.json"))
    hit["metadata"]["access_right"] = raw
    rec = zenodo._record(hit)
    assert rec["access"]["tier"] == tier
    assert "access_right=%s" % raw in rec["access"]["evidence"]


def test_missing_or_odd_access_is_unknown(fixture_json):
    hit = copy.deepcopy(fixture_json("zenodo", "record.json"))
    del hit["metadata"]["access_right"]
    assert zenodo._record(hit)["access"]["tier"] == "unknown"
    hit["metadata"]["access_right"] = "weird"
    assert zenodo._record(hit)["access"]["tier"] == "unknown"


def test_cc_zero_licence(fixture_json):
    hit = copy.deepcopy(fixture_json("zenodo", "record.json"))
    hit["metadata"]["license"] = {"id": "cc-zero"}
    assert zenodo._record(hit)["licence"]["id"] == "CC0-1.0"
    hit["metadata"].pop("license")
    assert zenodo._record(hit)["licence"] is None


def test_build_queries_and_combined():
    qs = zenodo.build_queries("voice recordings Parkinson's disease")
    assert qs[0] == "voice AND recordings AND Parkinson AND disease"
    assert len(qs) <= 3 and all(" OR " not in q for q in qs)
    assert "recordings" not in qs[1]


def test_search_collapses_versions_and_limits(fake_http, fixture_json):
    data = copy.deepcopy(fixture_json("zenodo", "search.json"))
    dup = copy.deepcopy(data["hits"]["hits"][0])
    dup["id"] = 99
    data["hits"]["hits"].append(dup)  # same conceptrecid: another version
    calls = fake_http({"zenodo.org/api/records": (200, data)})
    recs = zenodo.search("voice Parkinson", limit=10)
    ids = [r["id"] for r in recs]
    assert len(ids) == len(set(ids)) == len(data["hits"]["hits"]) - 1
    assert len(calls) <= 3
    tiers = {r["id"]: r["access"]["tier"] for r in recs}
    assert "gated" in tiers.values()  # the recorded restricted record


def test_search_never_more_than_three_requests(fake_http):
    calls = fake_http({"zenodo.org/api/records": (200, {"hits": {"hits": []}})})
    assert zenodo.search("satellite imagery crop yield", limit=5) == []
    assert 1 <= len(calls) <= 3


def test_api_error_raises(fake_http):
    fake_http({"zenodo.org/api/records": (500, {"message": "boom"})})
    # the fake serves the status through http_request; get_json must raise
    with pytest.raises(common.FetchError):
        zenodo.search("anything")


def test_offline_unmatched_raises(fake_http):
    fake_http({})
    with pytest.raises(common.FetchError):
        zenodo.search("anything")


@pytest.mark.parametrize("ref", ["https://zenodo.org/records/17753641", "17753641",
                                 "10.5281/zenodo.17753641", "https://doi.org/10.5281/zenodo.17753641",
                                 "https://zenodo.org/record/17753641"])
def test_lookup_forms(fake_http, fixture_json, ref):
    calls = fake_http({"zenodo.org/api/records/17753641": (200, fixture_json("zenodo", "record.json"))})
    rec = zenodo.lookup(ref)
    assert rec["id"] == "zenodo:17753641"
    assert calls[0][1].endswith("/17753641")


def test_lookup_404_and_foreign(fake_http):
    fake_http({"zenodo.org/api/records/1": (404, {"message": "gone"})})
    assert zenodo.lookup("1") is None
    assert zenodo.lookup("https://example.org/page") is None


def test_lookup_server_error_raises(fake_http):
    fake_http({"zenodo.org/api/records/2": (500, {})})
    with pytest.raises(common.FetchError):
        zenodo.lookup("2")


@pytest.mark.live
def test_live_search():
    recs = zenodo.search("voice Parkinson", limit=3)
    assert recs and recs[0]["url"].startswith("https://zenodo.org/")


def test_null_entries_do_not_lose_the_record(fixture_json):
    # M2: one null in a list used to raise AttributeError and lose every result of the registry.
    hit = copy.deepcopy(fixture_json("zenodo", "record.json"))
    hit["metadata"]["creators"] = [None] + hit["metadata"]["creators"]
    hit["files"] = [None] + hit["files"]
    hit["metadata"]["keywords"] = [None, "gait"]
    rec = zenodo._record(hit)
    assert rec["creators"] and "None" not in rec["creators"] and rec["subjects"] == ["gait"]
    assert rec["size"]["files"] == len(hit["files"]) - 1


def test_a_malformed_hit_is_skipped_not_fatal(fake_http, fixture_json):
    good = fixture_json("zenodo", "record.json")
    bad = {"id": 5, "metadata": "not an object"}
    fake_http({"zenodo.org/api/records": (200, {"hits": {"hits": [bad, good]}})})
    recs = zenodo.search("gait", limit=5)
    assert [r["id"] for r in recs] == ["zenodo:17753641"] and recs.skipped == 1


def test_loosest_pass_keeps_a_short_acronym():
    # M7: "ICU/ward mortality: adults" fell back to "mortality AND adults" and found stroke and seedlings.
    qs = zenodo.build_queries("ICU/ward mortality: adults")
    assert qs[-1] == "ICU AND mortality"
