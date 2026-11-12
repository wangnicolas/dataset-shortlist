"""Tests for scripts/scout.py: the digest an agent reads, and the commands' error paths. Offline."""
from __future__ import annotations

import importlib.util
import json
import os

import pytest

from scoutlib import common

SCOUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts", "scout.py")


@pytest.fixture
def scout():
    spec = importlib.util.spec_from_file_location("scout_cli", SCOUT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _verified(title, found_title, method="registry-api", notes=(), problems=(), extra=None, tier="unknown"):
    rec = common.make_record("manual", "x", title, "https://repo.example/r/1", tier, "", extra=extra or {})
    rec["verification"] = {"verified": True, "method": method, "checked_at": "2026-11-12T00:00:00Z",
                           "problems": list(problems), "notes": list(notes), "found_title": found_title}
    return rec


def test_digest_shows_the_name_given_and_the_registry_title(scout, capsys):
    rec = _verified("Coastal Buoy Temperature Records", "Coastal Buoy Temperature Records",
                    extra={"given_title": "Coastal buoy salinity drifters"})
    page = _verified("Pediatric sleep EEG recordings", "Data portal", method="http")
    scout._print_records([rec, page])
    out = capsys.readouterr().out
    assert "given as: Coastal buoy salinity drifters" in out
    assert "page title: Data portal" in out
    assert out.count("registry title:") == 0      # the registry title is already the record's title


# ------------------------------------------------ search: deadlines, proxy (S8, P1)

import threading  # noqa: E402
import time  # noqa: E402
import types  # noqa: E402


def _fake_source(name, delay=0.0, tracker=None):
    module = types.ModuleType("fake_" + name)
    module.NAME = name
    module.DESCRIPTION = "fake"

    def search(query, limit=20):
        if tracker is not None:
            with tracker["lock"]:
                tracker["now"] += 1
                tracker["max"] = max(tracker["max"], tracker["now"])
        try:
            time.sleep(delay)
            return [common.make_record(name, "1", "%s record about %s" % (name, query), "https://%s.example/1" % name)]
        finally:
            if tracker is not None:
                with tracker["lock"]:
                    tracker["now"] -= 1

    module.search = search
    return module


def _tracker():
    return {"lock": threading.Lock(), "now": 0, "max": 0}


@pytest.mark.parametrize("env,expected_max", [({}, 3), ({"HTTPS_PROXY": "http://127.0.0.1:3128"}, 1),
                                              ({"https_proxy": "http://p:1", "DATASET_SCOUT_PARALLEL": "1"}, 3),
                                              ({"DATASET_SCOUT_PARALLEL": "0"}, 1)])
def test_search_runs_registries_one_after_another_behind_a_proxy(scout, monkeypatch, capsys, env, expected_max):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    tracker = _tracker()
    monkeypatch.setattr(scout, "load_sources", lambda: {n: _fake_source(n, 0.15, tracker) for n in ("a", "b", "c")})
    assert scout.main(["search", "coastal buoys"]) == 0
    assert tracker["max"] == expected_max
    assert capsys.readouterr().out.count("record about coastal buoys") == 3


def test_a_registry_that_never_answers_costs_one_budget_not_the_whole_search(scout, monkeypatch, capsys):
    monkeypatch.setenv("DATASET_SCOUT_SEARCH_BUDGET", "0.3")
    monkeypatch.setattr(scout, "load_sources", lambda: {"fast": _fake_source("fast"), "stuck": _fake_source("stuck", 5.0)})
    started = time.monotonic()
    scout.main(["search", "coastal buoys"])
    assert time.monotonic() - started < 2.0
    out = capsys.readouterr().out
    assert "SOURCE FAILED stuck: no answer within 0.3 s" in out and "fast record about coastal buoys" in out


def test_the_cli_process_exits_on_time_when_a_registry_hangs(tmp_path):
    # The review's measurement, end to end: a socket that accepts and never replies, set as the
    # Zenodo API. The process (not just the function) must end soon after the search budget.
    import socket
    import subprocess
    import sys

    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    server.listen(5)
    held = []

    def accept():
        while True:
            try:
                conn, _ = server.accept()
            except OSError:
                return
            held.append(conn)

    threading.Thread(target=accept, daemon=True).start()
    port = server.getsockname()[1]
    code = ("import sys; sys.argv[0] = %r; sys.path.insert(0, %r); import scout; "
            "from scoutlib.sources import zenodo; zenodo.API = 'http://127.0.0.1:%d/api/records'; "
            "sys.exit(scout.main(['search', 'coastal buoys', '--source', 'zenodo']))"
            % (SCOUT, os.path.dirname(SCOUT), port))
    env = dict(os.environ, DATASET_SCOUT_SEARCH_BUDGET="1.5", DATASET_SCOUT_CACHE=str(tmp_path))
    started = time.monotonic()
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60, env=env)
    elapsed = time.monotonic() - started
    server.close()
    for conn in held:
        conn.close()
    assert "SOURCE FAILED zenodo: no answer within 1.5 s" in done.stdout, done.stdout + done.stderr
    assert elapsed < 10.0, elapsed


# ------------------------------------------------ add and search accumulation (S5, M3)

def test_add_keeps_the_note_out_of_the_description_and_knows_a_second_add(scout, tmp_path, capsys):
    path = str(tmp_path / "candidates.json")
    assert scout.main(["add", path, "--title", "Coastal buoys", "--url", "https://repo.example/r/1",
                       "--note", "table 2 of a 2024 paper"]) == 0
    rec = json.load(open(path))["records"][0]
    assert rec["description"] == "" and rec["extra"]["found_via"] == "table 2 of a 2024 paper"
    scout.main(["add", path, "--title", "Coastal buoys", "--url", "https://repo.example/r/1"])
    assert "already in" in capsys.readouterr().out
    data = json.load(open(path))
    assert len(data["records"]) == 1 and data["records"][0]["also_found_in"] == []


def test_a_second_search_counts_re_finds_as_already_in_the_file(scout, tmp_path, monkeypatch, capsys):
    path = str(tmp_path / "candidates.json")
    monkeypatch.setattr(scout, "load_sources", lambda: {"a": _fake_source("a")})
    scout.main(["search", "coastal buoys", "--out", path])
    capsys.readouterr()
    scout.main(["search", "coastal buoys", "--out", path])
    out = capsys.readouterr().out
    assert "0 new, 1 already in the file, 0 merged with another copy, 1 total" in out
    assert json.load(open(path))["records"][0]["also_found_in"] == []


# ------------------------------------------------ lookup error paths (S11, M4)

def _lookup_sources(datacite_lookup=None, host_lookup=None):
    dc = types.ModuleType("fake_datacite")
    dc.NAME, dc.HOSTS, dc.search = "datacite", ("doi.org",), (lambda q, limit=20: [])
    dc.lookup = datacite_lookup or (lambda target: None)
    host = types.ModuleType("fake_hub")
    host.NAME, host.HOSTS, host.search = "hub", ("hub.example",), (lambda q, limit=20: [])
    host.lookup = host_lookup or (lambda target: None)
    return {"datacite": dc, "hub": host}


def test_lookup_of_a_registry_error_prints_one_line_not_a_traceback(scout, monkeypatch, capsys):
    def refuses(target):
        raise common.FetchError(target, 401, "Invalid username or password.")

    monkeypatch.setattr(scout, "load_sources", lambda: _lookup_sources(host_lookup=refuses))
    assert scout.main(["lookup", "https://hub.example/datasets/nobody/nothing"]) == 1
    err = capsys.readouterr().err
    assert "could not ask the hub registry" in err and "says nothing about whether the record exists" in err


def test_lookup_of_a_doi_datacite_does_not_know_does_not_say_it_does_not_exist(scout, monkeypatch, capsys):
    monkeypatch.setattr(scout, "load_sources", lambda: _lookup_sources())
    assert scout.main(["lookup", "10.1038/sdata.2016.35"]) == 1
    err = capsys.readouterr().err
    assert "another agency" in err and "does not mean it does not exist" in err
    assert "verify --url https://doi.org/10.1038/sdata.2016.35" in err


def test_lookup_of_a_doi_follows_the_landing_page_to_the_hosting_registry(scout, monkeypatch, capsys):
    dc = common.make_record("datacite", "10.5555/x", "Gait set", "https://doi.org/10.5555/x", "unknown",
                            "no standard access statement", doi="10.5555/x",
                            licence=common.normalise_licence("CC-BY-4.0"), extra={"landing_page": "https://hub.example/r/1"})
    hub = common.make_record("hub", "r1", "Gait set", "https://hub.example/r/1", "gated", "flag=manual")
    monkeypatch.setattr(scout, "load_sources", lambda: _lookup_sources(lambda t: dc, lambda t: hub))
    assert scout.main(["lookup", "doi:10.5555/x"]) == 0
    captured = capsys.readouterr()
    record = json.loads(captured.out)
    assert record["source"] == "hub" and record["access"]["tier"] == "gated"
    assert record["doi"] == "10.5555/x" and record["licence"]["id"] == "CC-BY-4.0"
    assert "hosts the DOI's landing page" in captured.err


# ------------------------------------------------ the verify digest and inputs (S10, M9)

def test_digest_prints_every_access_note_and_caps_only_routine_ones(scout, capsys):
    notes = ["licence, version filled from the zenodo registry record", "confirmed by the zenodo registry record zenodo:1",
             "description read from the landing page's own metadata",
             'the landing page mentions "data use agreement" ("...")', 'the landing page mentions "request access" ("...")',
             "access tier unknown: no registry metadata states it; read the landing page before calling the data open"]
    scout._print_records([_verified("Coastal buoys", None, notes=notes)])
    out = capsys.readouterr().out
    assert '"data use agreement"' in out and '"request access"' in out and "access tier unknown" in out
    assert out.count("    note: ") == 5            # two routine notes, then the three that matter


def test_verify_with_a_file_and_urls_checks_both(scout, tmp_path, monkeypatch, capsys):
    from scoutlib import verify

    path = str(tmp_path / "candidates.json")
    json.dump({"records": [common.make_record("zenodo", "1", "Coastal buoys", "https://zenodo.org/records/1")]},
              open(path, "w"))
    seen = []
    monkeypatch.setattr(verify, "verify_records", lambda records: seen.extend(records) or {"records": [], "checked_at": ""})
    scout.main(["verify", path, "--url", "https://example.org/data/2"])
    assert [r.get("url") for r in seen] == ["https://zenodo.org/records/1", "https://example.org/data/2"]


def test_add_without_a_title_is_refused(scout, tmp_path, capsys):
    # S5 (already fixed): a URL stored as the title made verify call a real dataset a different resource.
    with pytest.raises(SystemExit) as info:
        scout.main(["add", str(tmp_path / "c.json"), "--url", "https://zenodo.org/records/1"])
    assert info.value.code == 2 and "--title" in capsys.readouterr().err
