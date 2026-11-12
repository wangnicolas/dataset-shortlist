"""Shared pytest setup: make the skill's scripts importable and gate live tests."""
from __future__ import annotations

import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts")
FIXTURES = os.path.join(REPO, "tests", "fixtures")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)


def pytest_configure(config):
    config.addinivalue_line("markers", "live: needs network; runs only when SCOUT_LIVE=1")


def pytest_collection_modifyitems(config, items):
    if os.environ.get("SCOUT_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="live test; set SCOUT_LIVE=1 to run")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


_ENV_TO_CLEAR = ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy",
                 "DATASET_SCOUT_PARALLEL", "SCOUT_VERIFY_BUDGET", "DATASET_SCOUT_SEARCH_BUDGET")


@pytest.fixture(autouse=True)
def _hermetic(tmp_path, monkeypatch):
    """Every test starts from the same state, whatever the machine or sandbox it runs in.

    The PhysioNet catalogue cache goes to a private folder (never the shared temp
    cache a real run uses), the per-process host state is cleared, and proxy
    variables are removed, so a proxied sandbox does not change which code path runs.
    """
    if os.environ.get("SCOUT_LIVE") != "1":
        for name in _ENV_TO_CLEAR:
            monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("DATASET_SCOUT_CACHE", str(tmp_path / "scout-cache"))
    if os.environ.get("SCOUT_LIVE") != "1":
        # Offline tests replace urllib; they must never fall through to the real curl program.
        monkeypatch.setenv("DATASET_SCOUT_TRANSPORT", "urllib")
    from scoutlib import common, literature
    from scoutlib.sources import physionet

    physionet._CACHE.clear()
    literature._OPENALEX.clear()
    common._host_failures.clear()
    common._last_call.clear()
    yield
    physionet._CACHE.clear()
    common._host_failures.clear()


@pytest.fixture
def fixture_json():
    """Load tests/fixtures/<module>/<name> as JSON."""
    def _load(module, name):
        with open(os.path.join(FIXTURES, module, name), encoding="utf-8") as handle:
            return json.load(handle)
    return _load


@pytest.fixture
def fake_http(monkeypatch):
    """Replace scoutlib.common.http_request with canned responses.

    Usage:
        fake_http({"api.example.org/search": (200, {"hits": []})})
    Keys are substrings of the requested URL (query string included); values are
    (status, body) where body is a dict/list (served as JSON), str or bytes.
    Unmatched URLs raise FetchError, so an offline test can never reach the network.
    """
    from scoutlib import common

    calls = []

    def install(routes):
        def _request(url, params=None, headers=None, timeout=20.0, retries=2,
                     method="GET", data=None, max_bytes=4000000, **ignored):
            import urllib.parse
            full = url
            if params:
                full = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
            calls.append((method, full))
            for needle, (status, body) in routes.items():
                if needle in full:
                    if isinstance(body, (dict, list)):
                        raw = json.dumps(body).encode("utf-8")
                        ctype = "application/json"
                    elif isinstance(body, str):
                        raw = body.encode("utf-8")
                        ctype = "text/html; charset=utf-8"
                    else:
                        raw = body
                        ctype = "application/octet-stream"
                    return common.HttpResponse(status, full, {"Content-Type": ctype}, b"" if method == "HEAD" else raw)
            raise common.FetchError(full, None, "offline test: no canned response")

        monkeypatch.setattr(common, "http_request", _request)
        return calls

    return install
