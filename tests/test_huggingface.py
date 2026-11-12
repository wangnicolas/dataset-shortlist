"""Offline tests for the Hugging Face Hub adapter (recorded responses)."""
from __future__ import annotations

import copy

import pytest

from scoutlib import common
from scoutlib.sources import huggingface as hf


def test_field_mapping(fixture_json):
    item = fixture_json("huggingface", "search_parkinson.json")[1]
    rec = hf._record(item)
    assert rec["id"] == "huggingface:" + item["id"]
    assert rec["url"] == "https://huggingface.co/datasets/" + item["id"]
    assert rec["access"]["tier"] == "open"
    assert rec["access"]["evidence"] == "gated=false; the Hub detected data files (format:audiofolder)"
    assert rec["licence"]["id"] == "CC-BY-4.0"
    assert rec["extra"]["licence_declared_by"] == "uploader"
    assert rec["extra"]["gated"] is False
    assert rec["usage"] == {"downloads": item["downloads"], "likes": item["likes"]}
    assert "audio" in rec["formats"]
    assert rec["size"] == {"text": "1K<n<10K"}
    assert "See the full description" not in rec["description"]


@pytest.mark.parametrize("gated,tier", [(False, "open"), ("auto", "account"), ("manual", "gated")])
def test_access_mapping(fixture_json, gated, tier):
    item = copy.deepcopy(fixture_json("huggingface", "search_parkinson.json")[0])
    item["gated"] = gated
    rec = hf._record(item)
    assert rec["access"]["tier"] == tier
    assert rec["extra"]["gated"] == gated
    if gated:
        assert gated in rec["access"]["evidence"]


def test_missing_gated_is_unknown(fixture_json):
    item = copy.deepcopy(fixture_json("huggingface", "search_parkinson.json")[0])
    item.pop("gated")
    assert hf._record(item)["access"]["tier"] == "unknown"


def test_no_licence_is_noted(fixture_json):
    item = fixture_json("huggingface", "search_voice.json")[1]
    rec = hf._record(item)
    assert rec["licence"] is None
    assert "licence_note" in rec["extra"]


def test_keyword_derivation_long_query():
    qs = hf.build_queries("I need voice recordings from patients with Parkinson's disease for classification")
    assert 1 <= len(qs) <= 3
    assert qs[0] == "parkinson"
    assert all(" " not in q for q in qs)
    assert "the" not in qs and "with" not in qs


def test_keyword_generic_words_go_last():
    qs = hf.build_queries("ICU mortality prediction time series")
    assert qs[:2] == ["mortality", "icu"]
    assert len(qs) == 3


def test_search_merges_and_ranks(fake_http, fixture_json):
    park = fixture_json("huggingface", "search_parkinson.json")
    voice = fixture_json("huggingface", "search_voice.json")
    calls = fake_http({"search=parkinson": (200, park), "search=voice": (200, voice),
                       "search=recordings": (200, [])})
    recs = hf.search("voice recordings Parkinson's disease", limit=20)
    assert len(calls) <= 3
    ids = [r["id"] for r in recs]
    assert len(ids) == len(set(ids))
    assert recs[0]["title"].lower().count("parkinson") >= 1  # both terms in the id win
    assert any("voice" in r["title"].lower() for r in recs)


def test_search_respects_limit_and_request_cap(fake_http, fixture_json):
    park = fixture_json("huggingface", "search_parkinson.json")
    calls = fake_http({"huggingface.co/api/datasets": (200, park)})
    recs = hf.search("alpha beta gamma delta epsilon", limit=2)
    assert len(calls) == 3
    assert len(recs) <= 2


def test_api_error_raises(fake_http):
    fake_http({"huggingface.co/api/datasets": (503, {"error": "down"})})
    with pytest.raises(common.FetchError):
        hf.search("parkinson")


@pytest.mark.parametrize("ref", ["https://huggingface.co/datasets/birgermoell/Italian_Parkinsons_Voice_and_Speech",
                                 "birgermoell/Italian_Parkinsons_Voice_and_Speech"])
def test_lookup(fake_http, fixture_json, ref):
    calls = fake_http({"api/datasets/birgermoell/Italian": (200, fixture_json("huggingface", "dataset.json"))})
    rec = hf.lookup(ref)
    assert rec["id"] == "huggingface:birgermoell/Italian_Parkinsons_Voice_and_Speech"
    assert rec["access"]["tier"] == "open"
    assert len(calls) == 1


def test_lookup_404_and_foreign(fake_http):
    fake_http({"api/datasets/a/b": (404, {"error": "no"})})
    assert hf.lookup("a/b") is None
    assert hf.lookup("https://example.org/x y") is None


# ------------------------------------------------- B2: gated=false is not "open"

def test_loader_only_repository_is_not_called_open(fixture_json):
    # Recorded 2026-11-12 from /api/datasets/<id>: gated=false, no format: tag, and the
    # files are a card plus loading scripts; the data are distributed elsewhere.
    item = fixture_json("huggingface", "dataset_loader_only.json")
    rec = hf._record(item)
    assert item["gated"] is False
    assert rec["access"]["tier"] == "unknown"
    assert "gated=false" in rec["access"]["evidence"] and "loading script" in rec["access"]["evidence"]
    assert rec["extra"]["loader_only"] is True
    assert rec["extra"]["loading_script"] == item["id"].split("/")[1] + ".py"


def test_lookup_of_loader_only_repository_is_unknown(fake_http, fixture_json):
    item = fixture_json("huggingface", "dataset_loader_only.json")
    fake_http({"api/datasets/" + item["id"]: (200, item)})
    assert hf.lookup(item["id"])["access"]["tier"] == "unknown"


def test_search_listing_without_format_tag_is_unknown(fixture_json):
    # Search listings carry no file list; without the Hub's format: tag nothing shows the data are there.
    item = fixture_json("huggingface", "search_parkinson.json")[2]
    assert "siblings" not in item and not [t for t in item["tags"] if t.startswith("format:")]
    rec = hf._record(item)
    assert rec["access"]["tier"] == "unknown"
    assert "look the repository up" in rec["access"]["evidence"]


def _repo(gated, files, tags=(), stored=1000):
    return {"id": "someone/thing", "gated": gated, "tags": list(tags), "usedStorage": stored,
            "siblings": [{"rfilename": f} for f in files]}


@pytest.mark.parametrize("gated,files,stored,tier", [
    (False, [".gitattributes", "README.md", "data/part-0.zip"], 5000, "open"),         # data files, no format tag
    (False, [".gitattributes", "README.md"], 0, "unknown"),                              # an empty card
    (False, ["README.md", "thing.py", "dummy/0.0.0/dummy_data.zip"], 10, "unknown"),     # script plus test sample
    (False, ["README.md", "thing.py", "data/train.csv"], 5000, "unknown"),               # script: data may come from elsewhere
    ("auto", ["README.md", "thing.py"], 0, "unknown"),                                   # free account on the Hub, data elsewhere
    ("auto", ["README.md", "audio/a.wav"], 5000, "account"),
    ("manual", ["README.md", "thing.py"], 0, "gated"),                                   # an application either way
])
def test_hosting_evidence_from_the_file_list(gated, files, stored, tier):
    rec = hf._record(_repo(gated, files, stored=stored))
    assert rec["access"]["tier"] == tier
    if tier == "unknown":
        assert rec["access"]["evidence"].startswith("gated=")


def test_format_tag_is_positive_evidence_even_with_a_script():
    rec = hf._record(_repo(False, ["README.md", "thing.py", "data/x.parquet"], tags=["format:parquet"]))
    assert rec["access"]["tier"] == "open"


@pytest.mark.live
def test_live_search():
    recs = hf.search("parkinson voice", limit=3)
    assert recs


def test_missing_repository_answered_with_401_is_no_record(fake_http, fixture_json):
    # S11: the Hub answers 401 "Invalid username or password" for a repository that does not exist.
    fake_http({"api/datasets/nobody/nothing": (401, {"error": "Invalid username or password."})})
    assert hf.lookup("https://huggingface.co/datasets/nobody/nothing") is None


def test_a_malformed_search_item_is_skipped(fake_http, fixture_json):
    park = fixture_json("huggingface", "search_parkinson.json")
    fake_http({"huggingface.co/api/datasets": (200, park + [None, {"id": "x/y", "tags": "oops"}])})
    recs = hf.search("parkinson", limit=10)
    assert {r["id"] for r in recs} >= {"huggingface:" + park[0]["id"]}


def test_matching_more_query_words_beats_popularity(fake_http):
    # M6, the review's live ranking: a repository with both specific words ranked below two
    # very popular ones that match only "voice".
    def item(rid, downloads):
        return {"id": rid, "gated": False, "tags": ["format:parquet"], "downloads": downloads, "description": ""}

    listing = [item("omegalabsinc/omega-voice", 2000000), item("Hebrish/Hebrish-TTS-Voice-Recordings", 50000),
               item("someone/kcl-parkinson-voice-dataset", 12)]
    fake_http({"huggingface.co/api/datasets": (200, listing)})
    recs = hf.search("parkinson voice recordings", limit=3)
    assert recs[0]["title"] == "someone/kcl-parkinson-voice-dataset"


def test_verify_replaces_the_search_listing_reason_with_the_lookup_reason(fake_http, fixture_json):
    # A search hit without a format: tag says "look the repository up"; once verify has done that and
    # found only a loading script, the record must say so, not repeat the stale advice.
    from scoutlib import verify

    hit = copy.deepcopy(fixture_json("huggingface", "search_parkinson.json")[2])
    loader = fixture_json("huggingface", "dataset_loader_only.json")
    loader = dict(loader, id=hit["id"])
    listing_rec = hf._record(hit)
    assert "look the repository up" in listing_rec["access"]["evidence"]
    fake_http({"api/datasets/" + hit["id"]: (200, loader)})
    rec = verify.verify_records([listing_rec], sources={"huggingface": hf})["records"][0]
    assert rec["verification"]["verified"] is True and rec["access"]["tier"] == "unknown"
    assert "loading script" in rec["access"]["evidence"] and "look the repository up" not in rec["access"]["evidence"]
    assert any("loading script" in n for n in rec["verification"]["notes"] if n.startswith("access tier unknown"))
