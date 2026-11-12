from __future__ import annotations

import http.client

import pytest

from scoutlib import common


@pytest.fixture
def curl(monkeypatch):
    """Pretend curl is installed and script what it returns: a list of
    (exit_code, status, body) tuples, one per call."""
    calls = []
    script = []

    def fake_run(url, hdrs, timeout, method, data, max_bytes):
        calls.append((method, url))
        code, status, body = script.pop(0) if script else (0, 200, b"{}")
        return code, status, url, {"Content-Type": "application/json"}, body, False, "scripted"

    monkeypatch.setattr(common, "curl_path", lambda: "/usr/bin/curl")
    monkeypatch.setattr(common, "_run_curl", fake_run)
    monkeypatch.setattr(common.time, "sleep", lambda seconds: None)
    return script, calls


def test_transport_choice(monkeypatch):
    monkeypatch.setattr(common, "curl_path", lambda: "/usr/bin/curl")
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "auto")
    assert common.transport() == "urllib"                 # no proxy: Python's own client
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:9999")
    assert common.transport() == "curl"                   # a proxy is configured
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "urllib")
    assert common.transport() == "urllib"                 # explicit choice wins
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    monkeypatch.delenv("HTTPS_PROXY")
    assert common.transport() == "curl"
    monkeypatch.setattr(common, "curl_path", lambda: None)
    assert common.transport() == "urllib"                 # no curl program: nothing to choose


def test_curl_answer_is_returned(curl, monkeypatch):
    script, calls = curl
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    script.append((0, 200, b'{"hits": 3}'))
    resp = common.http_request("https://api.example.org/search")
    assert resp.status == 200 and resp.json() == {"hits": 3}
    assert calls == [("GET", "https://api.example.org/search")]


def test_cut_body_is_retried_and_never_blames_the_host(curl, monkeypatch):
    script, calls = curl
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    script.extend([(18, 200, b'{"hi'), (56, 200, b""), (0, 200, b'{"hits": 1}')])
    assert common.get_json("https://api.example.org/search") == {"hits": 1}
    assert len(calls) == 3
    assert "api.example.org" not in common._host_failures


def test_cut_body_that_never_arrives_is_reported_as_a_transfer_problem(curl, monkeypatch):
    script, calls = curl
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    script.extend([(18, 200, b"")] * 5)
    with pytest.raises(common.FetchError) as info:
        common.http_request("https://api.example.org/search")
    assert info.value.kind == "cut_body" and "not a missing record" in str(info.value)
    assert len(calls) == 1 + common.CUT_BODY_RETRIES


def test_no_answer_counts_against_the_host(curl, monkeypatch):
    script, calls = curl
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    script.extend([(7, 0, b"")] * 4)
    with pytest.raises(common.FetchError) as info:
        common.http_request("https://dead.example.org/x")
    assert info.value.kind == "network" and len(calls) == 2
    assert common._host_failures.get("dead.example.org") == 1


def test_error_status_is_returned_not_raised(curl, monkeypatch):
    script, calls = curl
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    script.append((0, 404, b"not here"))
    assert common.http_request("https://api.example.org/missing").status == 404


def test_bad_address_is_not_retried(curl, monkeypatch):
    script, calls = curl
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    script.append((3, 0, b""))
    with pytest.raises(common.FetchError) as info:
        common.http_request("https://api.example.org/a b")
    assert info.value.kind == "invalid_url" and len(calls) == 1


def test_python_client_falls_back_to_curl_when_its_body_keeps_arriving_cut(curl, monkeypatch):
    script, calls = curl
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "auto")       # no proxy, so urllib goes first

    class CutResponse(object):
        status = 200
        headers = {"Content-Type": "application/json"}

        def geturl(self):
            return "https://api.example.org/search"

        def read(self, n=None):
            raise http.client.IncompleteRead(b'{"hi')

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    attempts = []

    def fake_urlopen(request, timeout=None):
        attempts.append(request.full_url)
        return CutResponse()

    monkeypatch.setattr(common.urllib.request, "urlopen", fake_urlopen)
    script.append((0, 200, b'{"hits": 2}'))
    assert common.get_json("https://api.example.org/search") == {"hits": 2}
    assert len(attempts) == 1 + common.CUT_BODY_RETRIES and len(calls) == 1


@pytest.mark.live
def test_live_curl_fetch(monkeypatch):
    monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "curl")
    if not common.curl_path():
        pytest.skip("no curl on this machine")
    resp = common.http_request("https://api.datacite.org/heartbeat")
    assert resp.status == 200
