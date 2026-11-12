from __future__ import annotations

import pytest

from scoutlib import common


@pytest.fixture(autouse=True)
def _fresh_host_state():
    common._host_failures.clear()
    common._last_call.clear()
    yield
    common._host_failures.clear()


LICENCE_CASES = [
    ("CC BY NC 4.0", "CC-BY-NC-4.0", False),
    ("CC BY NC-SA 4.0", "CC-BY-NC-SA-4.0", False),
    ("CC BY ND 4.0", "CC-BY-ND-4.0", True),
    ("cc-by-4.0", "CC-BY-4.0", True),
    ("CC-BY-SA 3.0", "CC-BY-SA-3.0", True),
    ("Creative Commons Attribution 4.0 International", "CC-BY-4.0", True),
    ("Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International", "CC-BY-NC-SA-4.0", False),
    # an open licence plus a restriction in the same text is custom terms, not the open licence
    ("Creative Commons Attribution 4.0 International; non-commercial research use only", None, False),
    # an institution's name is not a licence
    ("Use of the data requires a signed agreement; see the Database Use Policy (MIT)", None, None),
    ("MIT", "MIT", True),
    ("MIT License", "MIT", True),
    # two licences in one statement: do not pick one
    ("Apache License 2.0 for code; data under CC BY-NC 4.0", None, False),
    ("BSD 2-Clause", "BSD-2-Clause", True),
    ("GNU General Public License v2.0", "GPL-2.0", True),
    ("Public Domain Mark", "PDM-1.0", True),
    ("CC0", "CC0-1.0", True),
    ("Creative Commons Zero v1.0 Universal", "CC0-1.0", True),
    ("Open Data Commons Open Database License v1.0", "ODbL-1.0", True),
    ("ODC-By-1.0", "ODC-By-1.0", True),
    ("A Credentialed Health Data License 1.5.0", None, None),
    ("other", None, None),
    ("cdla-permissive-2.0", "CDLA-Permissive-2.0", True),
    ("apache-2.0", "Apache-2.0", True),
    ("agpl-3.0", "AGPL-3.0", True),
    ("CC-BY-NC-ND 4.0", "CC-BY-NC-ND-4.0", False),
]


@pytest.mark.parametrize("text,lic_id,commercial", LICENCE_CASES)
def test_licence_names(text, lic_id, commercial):
    got = common.normalise_licence(text)
    assert got["id"] == lic_id
    assert got["commercial_use"] == commercial
    assert got["name"] == text      # the original wording is always kept


@pytest.mark.parametrize("url,lic_id", [
    ("https://creativecommons.org/licenses/by-nc-sa/3.0/", "CC-BY-NC-SA-3.0"),
    ("https://creativecommons.org/publicdomain/zero/1.0/", "CC0-1.0"),
    ("https://opensource.org/licenses/MIT", "MIT"),
])
def test_licence_urls(url, lic_id):
    assert common.normalise_licence(url=url)["id"] == lic_id


def test_no_licence_given_is_none():
    assert common.normalise_licence() is None


def test_records_do_not_share_default_objects():
    a = common.make_record("s", "1", "First", "https://example.org/1")
    b = common.make_record("s", "2", "Second", "https://example.org/2")
    a["extra"]["slug"] = "first"
    a["usage"]["downloads"] = 61
    a["creators"].append("someone")
    assert b["extra"] == {} and b["usage"] == {} and b["creators"] == []
    assert common._RECORD_DEFAULTS["extra"] == {} and common._RECORD_DEFAULTS["usage"] == {}


def _rec(source, rid, title, doi=None, tier="unknown", publisher=None, extra=None):
    return common.make_record(source, rid, title, "https://example.org/%s" % rid, tier, "%s says %s" % (source, tier),
                              doi=doi, publisher=publisher, extra=extra or {})


def test_dedupe_keeps_different_dois_apart_even_with_the_same_generic_title():
    out = common.dedupe([_rec("zenodo", 111, "Dataset", "10.1/a", "open"), _rec("zenodo", 222, "Dataset", "10.1/b", "gated")])
    assert len(out) == 2


def test_dedupe_prefers_the_hosting_registry_and_records_the_conflict():
    out = common.dedupe([_rec("openaire", "x", "A long and specific dataset title", "10.1/a", "open"),
                         _rec("physionet", "y", "A long and specific dataset title", "10.1/a", "gated")])
    assert len(out) == 1
    assert out[0]["source"] == "physionet" and out[0]["access"]["tier"] == "gated"
    assert out[0]["extra"]["access_conflicts"][0]["tier"] == "open"
    assert out[0]["also_found_in"][0]["source"] == "openaire"


def test_dedupe_matches_a_concept_doi_against_a_version_doi():
    out = common.dedupe([_rec("openaire", "x", "Some critical care database", "10.1/concept", "open"),
                         _rec("physionet", "y", "Some critical care database", "10.1/v3", "gated",
                              extra={"project_doi": "10.1/concept"})])
    assert len(out) == 1 and out[0]["access"]["tier"] == "gated"


def test_dedupe_without_a_host_keeps_the_more_restrictive_claim():
    out = common.dedupe([_rec("openaire", "x", "A long and specific dataset title", None, "open"),
                         _rec("datacite", "y", "A long and specific dataset title", None, "closed")])
    assert len(out) == 1 and out[0]["access"]["tier"] == "closed"


def test_dedupe_does_not_merge_on_title_when_both_have_different_dois():
    out = common.dedupe([_rec("datacite", "x", "A long and specific dataset title", "10.1/a"),
                         _rec("datacite", "y", "A long and specific dataset title", "10.1/b")])
    assert len(out) == 2


def test_dedupe_does_not_change_its_input():
    first = _rec("openaire", "x", "A long and specific dataset title", "10.1/a", "open")
    second = _rec("zenodo", "y", "A long and specific dataset title", "10.1/a", "gated")
    common.dedupe([first, second])
    assert first["access"]["tier"] == "open" and "also_found_in" not in first


def test_get_json_retries_once_on_a_garbled_body(monkeypatch):
    monkeypatch.setattr(common.time, "sleep", lambda seconds: None)
    bodies = [b'{"hits": [1, 2', b'{"hits": [1, 2]}']
    calls = []

    def fake(url, **kwargs):
        calls.append(url)
        return common.HttpResponse(200, url, {"Content-Type": "application/json"}, bodies[len(calls) - 1])

    monkeypatch.setattr(common, "http_request", fake)
    assert common.get_json("https://api.example.org/x") == {"hits": [1, 2]}
    assert len(calls) == 2


def test_get_json_gives_up_after_three_garbled_bodies(monkeypatch):
    calls = []
    monkeypatch.setattr(common.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(common, "http_request",
                        lambda url, **kw: calls.append(url) or common.HttpResponse(200, url, {}, b"{not json"))
    with pytest.raises(common.FetchError) as info:
        common.get_json("https://api.example.org/x")
    assert len(calls) == common.JSON_TRIES == 3 and "after 3 tries" in str(info.value)


def test_a_host_that_keeps_failing_is_skipped_for_the_rest_of_the_process(monkeypatch):
    import urllib.error
    import urllib.request

    attempts = []

    def boom(request, timeout=None):
        attempts.append(request.full_url)
        raise urllib.error.URLError("timed out")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    monkeypatch.setattr(common.time, "sleep", lambda seconds: None)
    for _ in range(common.HOST_FAILURE_LIMIT):
        with pytest.raises(common.FetchError):
            common.http_request("https://dead.example.org/a")
    made = len(attempts)
    with pytest.raises(common.FetchError) as info:
        common.http_request("https://dead.example.org/b")
    assert len(attempts) == made                      # no new request was made
    assert "skipped" in str(info.value)
    assert made == 2 * common.HOST_FAILURE_LIMIT      # each failing call tried twice, not three times


def test_throttle_spaces_out_threads_on_one_host(monkeypatch):
    import threading
    import time

    times = []
    lock = threading.Lock()

    def call():
        common._throttle("https://same.example/x")
        with lock:
            times.append(time.monotonic())

    threads = [threading.Thread(target=call) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    times.sort()
    gaps = [b - a for a, b in zip(times, times[1:])]
    assert all(gap >= common.MIN_INTERVAL_SECONDS / 2 for gap in gaps), gaps   # unsafe throttle gave ~0


def test_emit_creates_the_output_folder(tmp_path):
    target = tmp_path / "dataset-shortlist" / "nested" / "candidates.json"
    common.emit({"records": []}, str(target))
    assert target.exists()


# ------------------------------------------- transfers cut short, invalid addresses (P1, S9, X2)

class _FakeResponse(object):
    """Enough of http.client.HTTPResponse for http_request."""

    def __init__(self, body, length=None, raise_on_read=None, status=200, url="https://api.example.org/x"):
        self._body = body
        self._raise = raise_on_read
        self.status = status
        self._url = url
        self.headers = _Headers({"Content-Type": "application/json"})
        if length is not None:
            self.headers["Content-Length"] = str(length)

    def geturl(self):
        return self._url

    def read(self, amount=None):
        if self._raise is not None:
            raise self._raise
        chunk, self._body = self._body[:amount], self._body[amount:]
        return chunk

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _Headers(dict):
    def items(self):
        return list(dict.items(self))


def _urlopen_serving(monkeypatch, responses):
    import urllib.request

    seen = []

    def fake(request, timeout=None):
        seen.append(request.full_url)
        item = responses[min(len(seen) - 1, len(responses) - 1)]
        if isinstance(item, Exception):
            raise item
        return item

    monkeypatch.setattr(urllib.request, "urlopen", fake)
    monkeypatch.setattr(common.time, "sleep", lambda seconds: None)
    return seen


def test_a_body_cut_short_twice_is_fetched_the_third_time_without_blaming_the_host(monkeypatch):
    full = b'{"hits": [1, 2, 3]}'
    seen = _urlopen_serving(monkeypatch, [_FakeResponse(full[:7], length=len(full)),
                                          _FakeResponse(full[:12], length=len(full)),
                                          _FakeResponse(full, length=len(full))])
    assert common.get_json("https://api.example.org/x") == {"hits": [1, 2, 3]}
    assert len(seen) == 3
    assert common._host_failures == {}


def test_incomplete_read_and_read_timeouts_are_retried_then_reported_as_cut(monkeypatch):
    import http.client
    import socket

    seen = _urlopen_serving(monkeypatch, [_FakeResponse(b"", raise_on_read=http.client.IncompleteRead(b'{"a"')),
                                          _FakeResponse(b"", raise_on_read=socket.timeout("timed out")),
                                          _FakeResponse(b"", raise_on_read=http.client.IncompleteRead(b""))])
    with pytest.raises(common.FetchError) as info:
        common.http_request("https://api.example.org/x")
    assert len(seen) == 1 + common.CUT_BODY_RETRIES == 3
    assert info.value.kind == "cut_body" and info.value.status == 200 and "cut short 3 times" in str(info.value)
    assert common._host_failures == {}           # the host answered every time


def test_a_host_that_never_answers_still_fails_fast(monkeypatch):
    import urllib.error

    seen = _urlopen_serving(monkeypatch, [urllib.error.URLError("timed out")])
    with pytest.raises(common.FetchError) as info:
        common.http_request("https://dead.example.org/x")
    assert len(seen) == 2 and info.value.kind == "network"
    assert common._host_failures == {"dead.example.org": 1}


def test_an_invalid_address_is_not_retried_and_not_held_against_the_host(monkeypatch):
    import http.client

    seen = _urlopen_serving(monkeypatch, [http.client.InvalidURL("nonnumeric port: 'abc'")])
    with pytest.raises(common.FetchError) as info:
        common.http_request("https://api.example.org:abc/x")
    assert len(seen) == 1 and info.value.kind == "invalid_url"
    assert common._host_failures == {}


def test_spaces_and_non_ascii_are_percent_encoded_before_the_request(monkeypatch):
    seen = _urlopen_serving(monkeypatch, [_FakeResponse(b"ok")])
    common.http_request("https://repo.example/set/1 x?q=a b&t=ü%20already")
    assert seen == ["https://repo.example/set/1%20x?q=a%20b&t=%C3%BC%20already"]


def test_a_body_longer_than_the_cap_is_marked_truncated_and_get_json_says_so(monkeypatch):
    _urlopen_serving(monkeypatch, [_FakeResponse(b"x" * 50)])
    resp = common.http_request("https://api.example.org/x", max_bytes=10)
    assert resp.truncated is True and len(resp.body) == 10 and resp.ok
    monkeypatch.setattr(common, "http_request", lambda url, **kw: common.HttpResponse(
        200, url, {}, b'{"a": ', truncated=True))
    with pytest.raises(common.FetchError) as info:
        common.get_json("https://api.example.org/x")
    assert "larger than" in str(info.value)


def test_credentials_never_appear_in_an_error():
    err = common.FetchError("https://api.example.org/works?search=x&api_key=SECRET-1&per-page=5", 503,
                            "see https://api.example.org/works?token=SECRET-2")
    assert "SECRET" not in str(err) and "SECRET" not in err.url and "api_key=REDACTED" in str(err)
    assert "search=x" in str(err) and "per-page=5" in str(err)


@pytest.mark.parametrize("env,expected", [
    ({}, True), ({"HTTPS_PROXY": "http://127.0.0.1:3128"}, False), ({"all_proxy": "socks5://127.0.0.1:1080"}, False),
    ({"HTTPS_PROXY": "http://127.0.0.1:3128", "DATASET_SCOUT_PARALLEL": "1"}, True),
    ({"DATASET_SCOUT_PARALLEL": "0"}, False),
])
def test_parallel_requests_only_without_a_proxy_unless_forced(monkeypatch, env, expected):
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    assert common.parallel_allowed() is expected


# ------------------------------------------------- dedupe: re-finds and landing pages (M3, S5)

def test_a_record_found_again_is_not_its_own_copy():
    first = _rec("huggingface", "a/b", "A long and specific dataset title", None, "open")
    out = common.dedupe([first, copy_of(first)])
    assert len(out) == 1 and out[0]["also_found_in"] == []
    # a later search finds both copies again: nothing is appended twice
    again = common.dedupe(out + [copy_of(first), _rec("openaire", "x", "A long and specific dataset title", None, "open")])
    again = common.dedupe(again + [_rec("openaire", "x", "A long and specific dataset title", None, "open")])
    assert len(again) == 1 and [c["id"] for c in again[0]["also_found_in"]] == ["openaire:x"]


def copy_of(rec):
    import copy
    return copy.deepcopy(rec)


def test_a_manual_record_with_the_same_landing_page_merges_into_the_registry_record():
    host = common.make_record("zenodo", "22036480", "Arabic speech recordings", "https://zenodo.org/records/22036480",
                              "open", "access_right=open")
    manual = common.make_record("manual", "arabic-speech", "Arabic speech", "https://zenodo.org/records/22036480/")
    out = common.dedupe([manual, host])
    assert len(out) == 1 and out[0]["source"] == "zenodo" and out[0]["also_found_in"][0]["source"] == "manual"


def test_a_shared_home_page_does_not_merge_different_datasets():
    a = common.make_record("manual", "a", "First thing", "https://lab.example/")
    b = common.make_record("manual", "b", "Second thing", "https://lab.example")
    assert len(common.dedupe([a, b])) == 2


def test_a_host_that_states_no_tier_is_not_overruled_by_an_aggregator_open():
    host = _rec("physionet", "p", "A long and specific dataset title", "10.1/a", "unknown")
    agg = _rec("openaire", "x", "A long and specific dataset title", "10.1/a", "open")
    out = common.dedupe([agg, host])
    assert out[0]["source"] == "physionet" and out[0]["access"]["tier"] == "unknown"
    assert out[0]["extra"]["access_conflicts"] == [{"source": "openaire", "tier": "open", "evidence": "openaire says open"}]


def test_retry_on_limits_which_statuses_are_retried(monkeypatch):
    import io
    import urllib.error

    seen = _urlopen_serving(monkeypatch, [urllib.error.HTTPError("https://api.example.org/x", 429, "Too Many", {},
                                                                 io.BytesIO(b"{}"))])
    resp = common.http_request("https://api.example.org/x", retry_on=(500, 502, 503, 504))
    assert resp.status == 429 and len(seen) == 1


# ------------------------------------------------------------------ access words

@pytest.mark.parametrize("word, tier, how", [
    ("open", "open", "exact"), (" Gated", "gated", "exact"), ("CONTROLLED", "controlled", "exact"),
    ("application", "gated", "word"), ("Application required", "gated", "word"), ("restricted", "gated", "word"),
    ("registered", "account", "word"), ("free account", "account", "word"), ("free_account", "account", "word"),
    ("click-through", "account", "word"), ("fee", "controlled", "word"), ("secure environment", "controlled", "word"),
    ("embargoed", "closed", "word"),
    # nothing but the exact word "open" is read as open
    ("public", "unknown", "unrecognised"), ("free", "unknown", "unrecognised"), ("Open access", "unknown", "unrecognised"),
    ("downloadable", "unknown", "unrecognised"), ("open download, no account", "unknown", "unrecognised"),
    ("by arrangement with the authors", "unknown", "unrecognised"),
    ("", "unknown", "missing"), ("   ", "unknown", "missing"), (None, "unknown", "missing"), (3, "unknown", "missing"),
    (["open"], "unknown", "missing"),
])
def test_canonical_tier(word, tier, how):
    assert common.canonical_tier(word) == (tier, how)


def test_no_listed_word_maps_to_open_and_every_target_is_a_tier():
    assert "open" not in common._TIER_WORDS
    assert set(common._TIER_WORDS) <= set(common.ACCESS_TIERS)
    for word, tier in common._TIER_BY_WORD.items():
        assert tier != "open" and word not in common.ACCESS_TIERS, word
