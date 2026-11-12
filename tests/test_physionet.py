from __future__ import annotations

import pytest

from scoutlib import common
from scoutlib.sources import physionet


@pytest.fixture(autouse=True)
def _clear_cache(tmp_path, monkeypatch):
    # Each test gets its own empty disk cache, so no test can read a catalogue
    # left behind by a real run or by another test.
    monkeypatch.setenv("DATASET_SCOUT_CACHE", str(tmp_path / "cache"))
    physionet._CACHE.clear()
    yield
    physionet._CACHE.clear()


def test_open_policy_with_agreement_is_not_called_open():
    entry = {"slug": "x", "title": "X", "version": "1.0", "access_policy": "Open",
             "dua": {"name": "Some Contributor Review Agreement"}, "is_latest_version": True}
    rec = physionet._record(entry)
    assert rec["access"]["tier"] == "unknown"
    assert "data use agreement" in rec["access"]["evidence"]
    entry["dua"] = None
    assert physionet._record(entry)["access"]["tier"] == "open"


def test_catalogue_is_reused_from_disk_between_processes(listing):
    _, calls = listing
    assert physionet.search("sleep", limit=3) is not None
    assert len(calls) == 1
    physionet._CACHE.clear()          # what a new process would start with
    assert physionet.search("heart", limit=3) is not None
    assert len(calls) == 1            # served from the disk cache, no second request


def test_unwritable_cache_folder_does_not_break_search(listing, monkeypatch):
    monkeypatch.setenv("DATASET_SCOUT_CACHE", "/nonexistent-root/definitely/not/writable")
    _, calls = listing
    assert physionet.search("sleep", limit=3) is not None
    assert len(calls) == 1


@pytest.fixture
def listing(fixture_json, fake_http):
    data = fixture_json("physionet", "published_list.json")
    calls = fake_http({"physionet.org/api/v1/project/published/": (200, data)})
    return data, calls


def _by_slug(data, slug, latest=True):
    return next(e for e in data if e["slug"] == slug and e["is_latest_version"] == latest)


def test_field_mapping(listing):
    data, _ = listing
    rec = physionet.lookup("slpdb")
    raw = _by_slug(data, "slpdb")
    assert rec["id"] == "physionet:slpdb"
    assert rec["source"] == "physionet"
    assert rec["title"] == raw["title"]
    assert rec["url"] == raw["source_url"]
    assert rec["version"] == raw["version"]
    assert rec["doi"] == raw["version_doi"].lower()
    assert rec["year"] == int(raw["publish_date"][:4])
    assert rec["updated"] == raw["publish_date"]
    assert rec["subjects"] == raw["topics"][:12]
    assert rec["licence"]["id"] == "ODC-By-1.0"
    assert rec["size"]["bytes"] == raw["main_storage_size"]
    assert rec["extra"]["access_policy"] == "Open"
    assert rec["extra"]["resource_type"] == "Database"
    assert "<" not in rec["description"]
    assert rec["access"]["tier"] == "open"
    assert "access_policy=Open" in rec["access"]["evidence"]


@pytest.mark.parametrize("policy,tier", [
    ("Open", "open"), ("Restricted", "account"), ("Credentialed", "gated"),
    ("Contributor Review", "gated"), ("Something New", "unknown"), (None, "unknown"),
])
def test_access_policy_tiers(policy, tier):
    got, evidence = physionet._tier(policy)
    assert got == tier
    if policy:
        assert "access_policy=%s" % policy in evidence


def test_every_policy_in_fixture_maps_to_expected_tier(listing):
    data, _ = listing
    expected = {"Open": "open", "Restricted": "account", "Credentialed": "gated", "Contributor Review": "gated"}
    for entry in data:
        assert physionet._record(entry)["access"]["tier"] == expected[entry["access_policy"]]


def test_unrecognised_policy_in_record(listing):
    data, _ = listing
    odd = dict(_by_slug(data, "slpdb"), access_policy="Members Only")
    rec = physionet._record(odd)
    assert rec["access"]["tier"] == "unknown"
    assert "Members Only" in rec["access"]["evidence"]
    assert rec["extra"]["access_policy"] == "Members Only"


def test_ranking_and_request_budget(listing):
    _, calls = listing
    results = physionet.search("sleep apnea polysomnography", limit=5)
    assert results
    assert results[0]["id"] in ("physionet:slpdb", "physionet:apnea-ecg")
    assert len(calls) == 1
    physionet.search("voice recordings", limit=5)
    assert len(calls) == 1  # list is cached for the process


def test_ranking_title_beats_abstract(listing):
    results = physionet.search("voice", limit=10)
    assert results
    assert "voice" in (results[0]["title"] + " ".join(results[0]["subjects"])).lower()


def test_search_skips_software_but_keeps_challenges(listing):
    data, _ = listing
    soft = _by_slug(data, "wfdb-swig-matlab")
    ids = [r["id"] for r in physionet.search(soft["title"], limit=30)]
    assert "physionet:wfdb-swig-matlab" not in ids
    assert any(r["extra"]["resource_type"] == "Challenge" for r in physionet.search("challenge", limit=30))


def test_search_only_latest_versions(listing):
    ids = [r["id"] for r in physionet.search("taichi", limit=30)]
    assert ids.count("physionet:taichidb") <= 1


def test_no_match_returns_empty_list(listing):
    assert physionet.search("zzzxqv", limit=5) == []


def test_lookup_from_latest_url(listing):
    rec = physionet.lookup("https://physionet.org/content/taichidb/1.0.2/")
    assert rec["version"] == "1.0.2"
    assert "requested_version" not in rec["extra"]


def test_lookup_old_version_url_describes_that_version(listing):
    rec = physionet.lookup("https://physionet.org/content/taichidb/1.0.0/")
    assert rec["version"] == "1.0.0" and rec["url"] == "https://physionet.org/content/taichidb/1.0.0/"
    assert rec["doi"] == "10.13026/c2w01j"
    assert rec["extra"]["latest_version"] == "1.0.2"
    assert "latest version is 1.0.2" in rec["extra"]["version_note"]


@pytest.fixture
def versions(fixture_json, fake_http):
    # Recorded catalogue entries (2026-11-11) of two projects whose access policy changed between versions.
    data = fixture_json("physionet", "version_policy_change.json")
    fake_http({"physionet.org/api/v1/project/published/": (200, data)})
    return data


def test_old_version_keeps_its_own_access_and_licence(versions):
    old = physionet.lookup("https://physionet.org/content/kinecal/1.0.0/")
    assert old["version"] == "1.0.0" and old["access"]["tier"] == "account"           # Restricted then
    assert "Restricted" in old["licence"]["name"] and old["doi"] == "10.13026/pq4z-4g10"
    assert old["extra"]["latest_version"] == "1.0.3"
    assert old["extra"]["latest_access"]["tier"] == "open" and old["extra"]["latest_licence"] == "CC0-1.0"
    newer = physionet.lookup("https://physionet.org/content/ct-ich/1.3.0/")           # Open then, Restricted now
    assert newer["access"]["tier"] == "open" and newer["extra"]["latest_access"]["tier"] == "account"


def test_unlisted_version_is_marked(versions):
    rec = physionet.lookup("https://physionet.org/content/kinecal/9.9/")
    assert rec["version"] == "1.0.3" and rec["extra"]["version_not_listed"] is True
    assert rec["extra"]["requested_version"] == "9.9" and "lists no version 9.9" in rec["extra"]["version_note"]


def test_verify_answers_an_old_version_link_with_that_version(versions):
    from scoutlib import verify

    rec = verify.verify_records([{"title": "KINECAL", "url": "https://physionet.org/content/kinecal/1.0.0/"}],
                                sources={"physionet": physionet})["records"][0]
    v = rec["verification"]
    assert v["verified"] is True and rec["access"]["tier"] == "account" and rec["version"] == "1.0.0"
    assert rec["url"] == "https://physionet.org/content/kinecal/1.0.0/"
    assert any("latest version is 1.0.3" in n for n in v["notes"])
    assert rec["extra"]["latest_access"]["tier"] == "open"


def test_verify_moves_an_unlisted_version_link_to_the_listed_record(versions):
    from scoutlib import verify

    rec = verify.verify_records([{"title": "KINECAL", "url": "https://physionet.org/content/kinecal/9.9/"}],
                                sources={"physionet": physionet})["records"][0]
    v = rec["verification"]
    assert "version_not_listed" in v["problem_types"]
    assert rec["url"] == "https://physionet.org/content/kinecal/1.0.3/" and rec["version"] == "1.0.3"
    assert rec["extra"]["given_url"] == "https://physionet.org/content/kinecal/9.9/"


def test_lookup_from_slug_and_unknown(listing):
    assert physionet.lookup("slpdb")["id"] == "physionet:slpdb"
    assert physionet.lookup("no-such-project") is None
    assert physionet.lookup("https://example.org/x") is None


def test_api_error_raises_fetcherror(fake_http):
    fake_http({"physionet.org/api/v1/project/published/": (500, {"detail": "boom"})})
    with pytest.raises(common.FetchError):
        physionet.search("anything")
    physionet._CACHE.clear()
    with pytest.raises(common.FetchError):
        physionet.lookup("slpdb")


def test_unexpected_shape_raises(fake_http):
    fake_http({"physionet.org/api/v1/project/published/": (200, {"detail": "nope"})})
    with pytest.raises(common.FetchError):
        physionet.search("anything")


@pytest.mark.live
def test_live_search():
    res = physionet.search("ECG arrhythmia", limit=3)
    assert res and all(r["url"].startswith("https://physionet.org/") for r in res)


def test_ranking_needs_half_of_the_query_and_a_match_outside_the_abstract():
    entries = [
        {"slug": "a", "title": "Smart wearable heart study", "topics": [], "short_description": "", "abstract": ""},
        {"slug": "b", "title": "Sleep staging with EEG", "topics": ["polysomnography"], "short_description": "",
         "abstract": "Overnight recordings."},
        {"slug": "c", "title": "Gait database", "topics": [], "short_description": "",
         "abstract": "Collected in a sleep laboratory with EEG caps for staging experiments."},
    ]
    # one shared word out of four is not a match
    assert physionet._rank(entries, "smart meter household electricity") == []
    # three of three words, anchored in the title: found; the abstract-only match is dropped
    assert [e["slug"] for e in physionet._rank(entries, "sleep staging EEG")] == ["b"]
    # a one-word query still works
    assert [e["slug"] for e in physionet._rank(entries, "gait")] == ["c"]


@pytest.mark.parametrize("url,version", [
    ("https://physionet.org/content/kinecal/1.0.0/", "1.0.0"),
    ("https://physionet.org/files/kinecal/1.0.0/data/file.csv", "1.0.0"),
    ("https://physionet.org/content/kinecal/metrics/1.0.0/", "1.0.0"),
    ("https://physionet.org/content/kinecal/view-license/1.0.3/", "1.0.3"),
    ("https://physionet.org/content/kinecal/", None),
    ("https://physionet.org/content/kinecal/metrics/", None),
])
def test_only_a_version_shaped_segment_is_read_as_the_version(url, version):
    assert physionet._parse(url) == ("kinecal", version)


def test_a_project_subpage_is_not_an_unlisted_version(versions):
    rec = physionet.lookup("https://physionet.org/content/kinecal/metrics/")
    assert rec["version"] == "1.0.3" and "version_not_listed" not in rec["extra"]
