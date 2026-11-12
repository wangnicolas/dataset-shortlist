"""Tests for scoutlib.verify: offline, with recorded pages from tests/fixtures/verify/.

The recorded pages (see tests/fixtures/verify/SOURCES.json for where each came
from) reproduce behaviours observed live on 2026-11-11: a site that answers HEAD
404 but GET 200, a 401 whose page says 404, a JavaScript shell that answers any
address with HTTP 200, and a WAF challenge served as HTTP 202 with an empty body.
Titles used in the synthetic cases are invented on purpose.
"""
from __future__ import annotations

import json
import os
import threading
import time
import types
import urllib.parse

import pytest

from scoutlib import common, verify

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "verify")


def fixture_text(name):
    with open(os.path.join(FIX, name), encoding="utf-8", errors="replace") as handle:
        return handle.read()


def fixture_obj(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as handle:
        return json.load(handle)


def page(title, text="", extra_head=""):
    filler = " ".join(["Measurements were collected at regular intervals and quality controlled."] * 12)
    return ("<html><head><title>%s</title>%s</head><body><h1>%s</h1><p>%s</p><p>%s</p></body></html>"
            % (title, extra_head, title, text, filler))


class Web(object):
    """A fake web behind common.http_request.

    routes: {url substring: spec}; the first matching substring wins. A spec is a
    dict with status, body, final (URL after redirects), headers, ctype and
    head_status (status for HEAD only), an Exception to raise, or a callable
    (method, url, headers) -> spec.
    """

    def __init__(self, monkeypatch, routes, delay=0.0):
        self.routes = routes
        self.delay = delay
        self.calls = []
        self.active = {}
        self.max_active = {}
        self.overall = 0
        self.max_overall = 0
        self.lock = threading.Lock()
        monkeypatch.setattr(common, "http_request", self.request)

    def request(self, url, params=None, headers=None, timeout=20.0, retries=2, method="GET", data=None,
                max_bytes=4000000, **ignored):
        host = urllib.parse.urlsplit(url).netloc
        with self.lock:
            self.calls.append((method, url, dict(headers or {})))
            self.active[host] = self.active.get(host, 0) + 1
            self.max_active[host] = max(self.max_active.get(host, 0), self.active[host])
            self.overall += 1
            self.max_overall = max(self.max_overall, self.overall)
        try:
            if self.delay:
                time.sleep(self.delay)
            for needle, spec in self.routes.items():
                if needle not in url:
                    continue
                if callable(spec):
                    spec = spec(method, url, headers or {})
                if isinstance(spec, Exception):
                    raise spec
                status = spec.get("status", 200)
                if method == "HEAD":
                    status = spec.get("head_status", status)
                body = spec.get("body", "")
                ctype = spec.get("ctype")
                if isinstance(body, (dict, list)):
                    raw, ctype = json.dumps(body).encode("utf-8"), ctype or "application/json"
                elif isinstance(body, str):
                    raw, ctype = body.encode("utf-8"), ctype or "text/html; charset=utf-8"
                else:
                    raw, ctype = body, ctype or "application/octet-stream"
                hdrs = {"Content-Type": ctype}
                hdrs.update(spec.get("headers") or {})
                return common.HttpResponse(status, spec.get("final", url), hdrs, b"" if method == "HEAD" else raw)
            raise common.FetchError(url, None, "offline test: no route")
        finally:
            with self.lock:
                self.active[host] -= 1
                self.overall -= 1

    def urls(self, method=None):
        return [u for m, u, _ in self.calls if method is None or m == method]


def fake_adapter(name, hosts, lookup):
    module = types.ModuleType("fake_%s" % name)
    module.NAME = name
    module.DESCRIPTION = "fake adapter for tests"
    module.HOSTS = tuple(hosts)
    module.search = lambda query, limit=20: []
    module.lookup = lookup
    return module


def registry_record(source="repo", rid="42", title="Coastal Buoy Temperature Records", url="https://repo.example/records/42",
                    tier="gated", evidence="access_flag=application", **fields):
    defaults = dict(licence=common.normalise_licence("CC-BY-4.0"), version="2.0", size={"bytes": 123456},
                    doi="10.5555/repo.42", description="Hourly sea temperature from coastal buoys.")
    defaults.update(fields)
    return common.make_record(source, rid, title, url, access_tier=tier, access_evidence=evidence, **defaults)


def one(result):
    assert len(result["records"]) == 1
    return result["records"][0]


def ver(rec):
    return rec["verification"]


# ------------------------------------------------------------------- registry

def test_registry_confirmation_fills_empty_fields_from_adapter(monkeypatch):
    web = Web(monkeypatch, {})
    seen = []

    def lookup(url):
        seen.append(url)
        return registry_record()

    sources = {"repo": fake_adapter("repo", ["repo.example"], lookup)}
    rec = one(verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://repo.example/records/42"}],
                                    sources=sources))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "registry-api" and v["registry"] == "repo"
    assert v["outcome"] == "confirmed" and v["problems"] == []
    assert seen == ["https://repo.example/records/42"]
    assert web.calls == []  # the registry confirmed it; the landing page was not fetched
    assert rec["source"] == "manual" and rec["title"] == "Coastal buoy temperature records"
    assert rec["access"]["tier"] == "gated" and "access_flag=application" in rec["access"]["evidence"]
    assert rec["licence"]["id"] == "CC-BY-4.0" and rec["version"] == "2.0" and rec["size"] == {"bytes": 123456}
    assert rec["doi"] == "10.5555/repo.42"
    assert any("filled from the repo registry record" in n for n in v["notes"])
    assert set(v) >= {"verified", "method", "http_status", "final_url", "checked_at", "problems", "notes"}


def test_hosting_registry_settles_a_tier_conflict_and_both_claims_are_kept(monkeypatch):
    # S2: the registry that holds the data is the authority on its access rules; the
    # other claim is kept, and the conflict is a problem (shown on the page too).
    Web(monkeypatch, {})
    found = registry_record(source="search", rid="7", tier="gated", evidence="flag=manual", licence=None, version=None)
    sources = {"repo": fake_adapter("repo", ["repo.example"],
                                    lambda url: registry_record(tier="open", evidence="flag=false", version="3.1"))}
    rec = one(verify.verify_records([found], sources=sources))
    v = ver(rec)
    assert v["verified"] is True
    assert rec["access"] == {"tier": "open", "evidence": "repo: flag=false"}
    assert rec["extra"]["access_conflicts"] == [{"source": "search", "tier": "gated", "evidence": "flag=manual"}]
    assert "access_conflict" in v["problem_types"] and "hosts the data" in v["problems"][0]
    assert rec["version"] == "3.1" and rec["licence"]["id"] == "CC-BY-4.0"  # empty fields are filled
    assert rec["source"] == "search" and rec["id"] == "search:7"


def test_aggregator_open_claim_loses_to_the_host(monkeypatch, fake_http, fixture_json):
    # The review's case: an aggregator says OPEN for a record whose host says Credentialed.
    from scoutlib.sources import physionet

    data = fixture_json("physionet", "published_list.json")
    entry = next(e for e in data if e["access_policy"] == "Credentialed" and e["is_latest_version"])
    fake_http({"physionet.org/api/v1/project/published/": (200, data)})
    claim = common.make_record("openaire", "x", entry["title"], entry["source_url"], "open", "bestAccessRight=OPEN")
    rec = one(verify.verify_records([claim], sources={"physionet": physionet}))
    v = ver(rec)
    assert v["verified"] is True and rec["access"]["tier"] == "gated"
    assert {"source": "openaire", "tier": "open", "evidence": "bestAccessRight=OPEN"} in rec["extra"]["access_conflicts"]
    assert "access_conflict" in v["problem_types"]


def test_host_that_does_not_confirm_an_open_claim_makes_it_unknown(monkeypatch):
    Web(monkeypatch, {})
    found = registry_record(source="aggregator", rid="7", tier="open", evidence="best=OPEN")
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record(
        tier="unknown", evidence="flag=open, but the record carries a data use agreement"))}
    rec = one(verify.verify_records([found], sources=sources))
    v = ver(rec)
    assert v["verified"] is True and rec["access"]["tier"] == "unknown"
    assert "best=OPEN" in rec["access"]["evidence"] and "data use agreement" in rec["access"]["evidence"]
    assert "access_conflict" in v["problem_types"]


def test_host_silence_keeps_a_restrictive_claim(monkeypatch):
    Web(monkeypatch, {})
    found = registry_record(source="aggregator", rid="7", tier="gated", evidence="best=RESTRICTED")
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record(tier="unknown", evidence=""))}
    rec = one(verify.verify_records([found], sources=sources))
    assert rec["access"] == {"tier": "gated", "evidence": "best=RESTRICTED"} and ver(rec)["problems"] == []


def test_doi_path_host_wins_over_datacite_and_the_input(monkeypatch):
    Web(monkeypatch, {"doi.org/api/handles/": {"body": {"responseCode": 100}}})
    dc = registry_record(source="datacite", rid="10.5555/repo.42", url="https://repo.example/records/42",
                         tier="open", evidence="rightsList=openAccess")
    sources = {"datacite": fake_adapter("datacite", ["doi.org"], lambda doi: dc),
               "repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record(tier="gated", evidence="flag=manual"))}
    found = registry_record(source="aggregator", rid="9", url="https://doi.org/10.5555/repo.42", tier="open",
                            evidence="best=OPEN")
    rec = one(verify.verify_records([found], sources=sources))
    v = ver(rec)
    assert v["verified"] is True and rec["access"]["tier"] == "gated" and v["registry"] == "repo"
    claims = {(c["source"], c["tier"]) for c in rec["extra"]["access_conflicts"]}
    assert claims == {("aggregator", "open"), ("datacite", "open")}


def test_without_a_host_the_more_restrictive_claim_is_kept(monkeypatch):
    Web(monkeypatch, {"doi.org/api/handles/": {"body": {"responseCode": 100}}})
    dc = registry_record(source="datacite", rid="10.5555/x.1", url="https://doi.org/10.5555/x.1",
                         tier="closed", evidence="rightsList=closedAccess")
    sources = {"datacite": fake_adapter("datacite", ["doi.org"], lambda doi: dc)}
    found = registry_record(source="aggregator", rid="9", url="https://doi.org/10.5555/x.1", tier="open",
                            evidence="best=OPEN")
    rec = one(verify.verify_records([found], sources=sources))
    assert rec["access"]["tier"] == "closed" and "access_conflict" in ver(rec)["problem_types"]


def test_page_text_never_sets_tier_or_licence(monkeypatch):
    body = page("Coastal buoy temperature records",
                "Freely available open access data, no registration. Use is governed by a data use agreement. "
                "Licensed under CC BY 4.0.")
    Web(monkeypatch, {"buoys.example": {"body": body}})
    rec = one(verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://buoys.example/set/9"}],
                                    sources={}))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "http"
    assert rec["access"]["tier"] == "unknown" and rec["licence"] is None
    assert any('"data use agreement"' in n for n in v["notes"])
    assert any(n.startswith("access tier unknown") for n in v["notes"])


def test_recorded_credentialed_page_gives_access_hints_only(monkeypatch):
    url = "https://archive.example/content/project-a/3.1/"
    Web(monkeypatch, {url: {"body": fixture_text("physionet_credentialed.html")}})
    rec = one(verify.verify_records([{"title": None, "url": url}], sources={}))
    v = ver(rec)
    assert v["verified"] is True and rec["access"]["tier"] == "unknown"
    assert any('mentions "request access"' in n for n in v["notes"])
    assert rec["title"]  # filled from the page because the input had none


def test_adapter_that_raises_falls_back_to_http(monkeypatch):
    def broken(url):
        raise RuntimeError("adapter bug")

    Web(monkeypatch, {"repo.example/records/5": {"body": page("Glacier melt stakes 1990-2020")}})
    sources = {"repo": fake_adapter("repo", ["repo.example"], broken)}
    rec = one(verify.verify_records([{"title": "Glacier melt stakes", "url": "https://repo.example/records/5"}], sources=sources))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "http"
    assert any("repo registry lookup failed (RuntimeError: adapter bug)" in n for n in v["notes"])


def test_adapter_fetcherror_and_missing_page_is_not_found(monkeypatch):
    def unauthorised(url):
        raise common.FetchError(url, 401, "Repository not found")

    url = "https://hub.example/datasets/nobody/nothing"
    Web(monkeypatch, {url: {"status": 401, "body": fixture_text("huggingface_missing_401.html")}})
    sources = {"hub": fake_adapter("hub", ["hub.example"], unauthorised)}
    v = ver(one(verify.verify_records([{"title": "Imaginary speech corpus", "url": url}], sources=sources)))
    # HTTP 401 alone would read as a login wall; the page itself says 404.
    assert v["verified"] is False and v["outcome"] == "not_found" and v["problem_types"] == ["not_found"]
    assert "404" in v["problems"][0]


def test_registry_without_record_then_404(monkeypatch, fake_http):
    fake_http({"repo.example/records/999": (404, fixture_text("zenodo_404.html"))})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: None)}
    v = ver(one(verify.verify_records([{"title": "Invented gait set", "url": "https://repo.example/records/999"}],
                                      sources=sources)))
    assert v["verified"] is False and v["outcome"] == "not_found"
    assert set(v["problem_types"]) == {"not_found", "registry_no_record"}


def test_registry_title_mismatch_is_not_merged(monkeypatch):
    Web(monkeypatch, {})
    sources = {"repo": fake_adapter("repo", ["repo.example"],
                                    lambda url: registry_record(title="Annual rainfall station records",
                                                                description="Daily precipitation totals."))}
    rec = one(verify.verify_records([{"title": "Pediatric sleep EEG recordings", "url": "https://repo.example/records/42"}],
                                    sources=sources))
    v = ver(rec)
    assert v["verified"] is False and v["outcome"] == "wrong_page" and v["problem_types"] == ["title_mismatch"]
    assert "describes a different resource" in v["problems"][0]
    assert rec["licence"] is None and rec["access"]["tier"] == "unknown"  # nothing merged from the wrong record


# ---------------------------------------------- B3: an invented name on a real record

def test_invented_name_on_a_real_registry_record_is_not_verified(fake_http, fixture_json):
    # The review's case, offline: a real PhysioNet project whose abstract mentions sleep and
    # apnea, given under an invented name with an invented modality.
    from scoutlib.sources import physionet

    fake_http({"physionet.org/api/v1/project/published/": (200, fixture_json("physionet", "published_list.json"))})
    rec = one(verify.verify_records([{"title": "Sleep Apnea Smartwatch Dataset",
                                      "url": "https://physionet.org/content/slpdb/1.0.0/"}],
                                    sources={"physionet": physionet}))
    v = ver(rec)
    assert v["verified"] is False and v["outcome"] == "wrong_page" and v["problem_types"] == ["title_mismatch"]
    assert v["found_title"] == "MIT-BIH Polysomnographic Database"
    assert "MIT-BIH Polysomnographic Database" in v["problems"][0] and "different resource" in v["problems"][0]
    assert rec["licence"] is None and rec["access"]["tier"] == "unknown"   # nothing merged from the record


def test_registry_description_does_not_rescue_a_different_title(monkeypatch):
    Web(monkeypatch, {})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record(
        title="Annual rainfall station records", description="Sleep EEG of children recorded in a pediatric clinic."))}
    v = ver(one(verify.verify_records([{"title": "Pediatric sleep EEG", "url": "https://repo.example/records/42"}],
                                      sources=sources)))
    assert v["verified"] is False and v["problem_types"] == ["title_mismatch"]


@pytest.mark.parametrize("given", [
    "GOTA",                                    # an acronym of the registry title
    "oceanarch",                               # the record's address slug
    None,                                      # verify --url: no name given
    "https://repo.example/records/oceanarch",  # a link stored as the title
    "Global ocean temperature archive",        # the same name in other letters
])
def test_aliases_and_missing_names_stay_verified(monkeypatch, given):
    Web(monkeypatch, {})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record(
        title="Global Ocean Temperature Archive", url="https://repo.example/records/oceanarch"))}
    rec = one(verify.verify_records([{"title": given, "url": "https://repo.example/records/oceanarch"}], sources=sources))
    v = ver(rec)
    assert v["verified"] is True and v["problems"] == []
    same_letters = given == "Global ocean temperature archive"
    assert rec["title"] == (given if same_letters else "Global Ocean Temperature Archive")
    if given and not same_letters:
        assert rec["extra"]["given_title"] == given


def test_real_record_under_its_slug_stays_verified(fake_http, fixture_json):
    from scoutlib.sources import physionet

    fake_http({"physionet.org/api/v1/project/published/": (200, fixture_json("physionet", "published_list.json"))})
    rec = one(verify.verify_records([{"title": "SLPDB", "url": "https://physionet.org/content/slpdb/1.0.0/"}],
                                    sources={"physionet": physionet}))
    assert ver(rec)["verified"] is True and rec["title"] == "MIT-BIH Polysomnographic Database"


def test_partly_matching_name_is_verified_under_the_registry_title(monkeypatch):
    Web(monkeypatch, {})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record())}
    rec = one(verify.verify_records([{"title": "Coastal buoy salinity drifters", "url": "https://repo.example/records/42"}],
                                    sources=sources))
    v = ver(rec)
    assert v["verified"] is True and v["problem_types"] == ["title_differs"]
    assert rec["title"] == "Coastal Buoy Temperature Records"
    assert rec["extra"]["given_title"] == "Coastal buoy salinity drifters"
    assert "Coastal Buoy Temperature Records" in v["problems"][0]


def test_registry_name_in_the_given_title_does_not_count_against_it(monkeypatch):
    Web(monkeypatch, {})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record(publisher="Repo"))}
    v = ver(one(verify.verify_records([{"title": "Repo coastal buoy temperature", "url": "https://repo.example/records/42"}],
                                      sources=sources)))
    assert v["verified"] is True and v["problems"] == []


def test_doi_title_stated_by_datacite_is_not_rescued_by_its_description(monkeypatch):
    Web(monkeypatch, {"landing.example/rec/1": {"body": page("Lake sediment cores from the Andes")}})
    rec_dc = registry_record(source="datacite", rid="10.5555/lake.1", title="Lake sediment cores from the Andes",
                             url="https://landing.example/rec/1", tier="unknown", evidence="", doi="10.5555/lake.1",
                             description="Glacier melt and alpine lakes; pollen and diatom counts.")
    sources = {"datacite": fake_adapter("datacite", ["doi.org", "dx.doi.org"], lambda doi: rec_dc)}
    v = ver(one(verify.verify_records([{"title": "Alpine glacier pollen diatoms", "doi": "10.5555/lake.1"}],
                                      sources=sources)))
    assert v["verified"] is False and v["problem_types"] == ["title_mismatch"]
    assert v["found_title"] == "Lake sediment cores from the Andes"


def test_page_that_does_not_name_the_dataset_is_flagged(monkeypatch):
    body = page("Data portal", "This collection holds pediatric sleep EEG recordings from two clinics.")
    Web(monkeypatch, {"portal.example/c/7": {"body": body}})
    rec = one(verify.verify_records([{"title": "Pediatric sleep EEG recordings", "url": "https://portal.example/c/7"}],
                                    sources={}))
    v = ver(rec)
    assert v["verified"] is True and v["problem_types"] == ["title_differs"]
    assert '"Data portal"' in v["problems"][0]
    assert rec["title"] == "Pediatric sleep EEG recordings"     # a page title can be generic: the name is kept


# ------------------------------------------------------------------------ DOI

def test_doi_resolves_through_handle_service(monkeypatch):
    csl = fixture_obj("csl_dataset.json")
    handle = fixture_obj("handle_registered.json")
    landing = [v["data"]["value"] for v in handle["values"] if v["type"] == "URL"][0]
    web = Web(monkeypatch, {
        "doi.org/api/handles/": {"body": handle},
        "doi.org/10.13026/": {"body": csl, "final": "https://data.crosscite.org/10.13026%2Fkpb9-mt58"},
        landing: {"body": fixture_text("physionet_credentialed.html")},
    })
    rec = one(verify.verify_records([{"title": csl["title"], "doi": "10.13026/KPB9-MT58"}], sources={}))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "doi" and v["outcome"] == "confirmed"
    assert v["final_url"] == landing and v["http_status"] == 200
    assert rec["doi"] == "10.13026/kpb9-mt58" and rec["url"] == "https://doi.org/10.13026/kpb9-mt58"
    assert rec["access"]["tier"] == "unknown"  # landing-page wording is a hint, never a tier
    assert any('mentions "request access"' in n for n in v["notes"])
    accepts = {u: h.get("Accept", "") for _, u, h in web.calls}
    assert "csl+json" in accepts["https://doi.org/10.13026/kpb9-mt58"]
    assert accepts[landing].startswith("text/html")  # never the JSON default, which doi.org negotiates


def test_unregistered_doi_is_flagged_as_likely_fabricated(monkeypatch, fake_http):
    fake_http({"doi.org/api/handles/": (404, fixture_obj("handle_missing.json"))})
    v = ver(one(verify.verify_records([{"title": "Global soil moisture benchmark", "doi": "10.5281/zenodo.99999999999"}],
                                      sources={})))
    assert v["verified"] is False and v["method"] == "doi" and v["outcome"] == "not_found"
    assert v["problem_types"] == ["doi_not_registered"]
    assert "not registered" in v["problems"][0] and "fabricated" in v["problems"][0]


def test_doi_prefers_datacite_adapter(monkeypatch):
    web = Web(monkeypatch, {"landing.example/rec/1": {"body": page("Lake sediment cores from the Andes")}})
    rec_dc = registry_record(source="datacite", rid="10.5555/lake.1", title="Lake sediment cores from the Andes",
                             url="https://landing.example/rec/1", tier="unknown", evidence="", doi="10.5555/lake.1")
    sources = {"datacite": fake_adapter("datacite", ["doi.org", "dx.doi.org"], lambda doi: rec_dc)}
    rec = one(verify.verify_records([{"title": "Andes lake sediment cores", "doi": "10.5555/LAKE.1"}], sources=sources))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "registry-api" and v["registry"] == "datacite"
    assert not any("api/handles" in u for u in web.urls())
    assert rec["licence"]["id"] == "CC-BY-4.0" and v["final_url"] == "https://landing.example/rec/1"


def test_datacite_none_falls_back_to_handle(monkeypatch):
    web = Web(monkeypatch, {
        "doi.org/api/handles/": {"body": {"responseCode": 1, "values": [
            {"type": "URL", "data": {"format": "string", "value": "https://journal.example/article/77"}}]}},
        "doi.org/10.6666/": {"body": {"type": "journal-article", "title": "Lake sediment cores from the Andes"}},
        "journal.example/article/77": {"body": page("Lake sediment cores from the Andes")},
    })
    sources = {"datacite": fake_adapter("datacite", ["doi.org"], lambda doi: None)}
    v = ver(one(verify.verify_records([{"title": "Lake sediment cores from the Andes", "doi": "10.6666/xyz.77"}],
                                      sources=sources)))
    assert v["verified"] is True and v["method"] == "doi"
    assert any("api/handles" in u for u in web.urls())
    assert any("registered as type 'journal-article'" in n for n in v["notes"])


def test_doi_landing_adapter_supplies_access_tier(monkeypatch):
    Web(monkeypatch, {"doi.org/api/handles/": {"body": {"responseCode": 1, "values": [
        {"type": "URL", "data": {"value": "https://repo.example/records/42"}}]}},
        "doi.org/10.5555/": {"body": {"type": "dataset", "title": "Coastal Buoy Temperature Records"}}})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record())}
    rec = one(verify.verify_records([{"title": "Coastal buoy temperature records", "doi": "10.5555/repo.42"}], sources=sources))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "registry-api" and v["registry"] == "repo"
    assert rec["access"]["tier"] == "gated"


def test_doi_title_mismatch(monkeypatch):
    Web(monkeypatch, {
        "doi.org/api/handles/": {"body": {"responseCode": 1, "values": [
            {"type": "URL", "data": {"value": "https://journal.example/a/1"}}]}},
        "doi.org/10.7777/": {"body": {"type": "journal-article", "title": "Annual rainfall station records"}},
        "journal.example/a/1": {"body": page("Annual rainfall station records")},
    })
    v = ver(one(verify.verify_records([{"title": "Pediatric sleep EEG recordings", "doi": "10.7777/abc"}], sources={})))
    assert v["verified"] is False and v["outcome"] == "wrong_page" and v["problem_types"] == ["title_mismatch"]
    assert "DOI 10.7777/abc exists but describes a different resource" in v["problems"][0]


def test_doi_registered_but_landing_gone(monkeypatch):
    Web(monkeypatch, {
        "doi.org/api/handles/": {"body": {"responseCode": 1, "values": [
            {"type": "URL", "data": {"value": "https://old.example/data/1"}}]}},
        "doi.org/10.8888/": {"status": 404, "body": ""},
        "old.example/data/1": {"status": 404, "body": fixture_text("physionet_404.html")},
    })
    v = ver(one(verify.verify_records([{"title": "Old survey", "doi": "10.8888/old.1"}], sources={})))
    assert v["verified"] is False and v["outcome"] == "not_found" and v["problem_types"] == ["doi_landing_broken"]


def test_doi_registered_landing_blocked_is_still_verified(monkeypatch):
    Web(monkeypatch, {
        "doi.org/api/handles/": {"body": {"responseCode": 1, "values": [
            {"type": "URL", "data": {"value": "https://walled.example/dataset?id=1"}}]}},
        "doi.org/10.9999/": {"body": {"type": "dataset", "title": "Household survey wave 3"}},
        "walled.example": {"status": 403, "body": "<html><head><title>403 Forbidden</title></head><body>403 Forbidden</body></html>"},
    })
    v = ver(one(verify.verify_records([{"title": "Household survey wave 3", "doi": "10.9999/hs.3"}], sources={})))
    assert v["verified"] is True and v["method"] == "doi" and v["http_status"] == 403
    assert any("landing page could not be checked" in n for n in v["notes"])


def test_working_doi_with_broken_given_link(monkeypatch):
    Web(monkeypatch, {
        "doi.org/api/handles/": {"body": {"responseCode": 1, "values": [
            {"type": "URL", "data": {"value": "https://repo3.example/record/8"}}]}},
        "doi.org/10.4444/": {"body": {"type": "dataset", "title": "Urban noise sensor network"}},
        "repo3.example/record/8": {"body": page("Urban noise sensor network")},
        "elsewhere.example": {"status": 404, "body": "gone"},
    })
    rec = one(verify.verify_records([{"title": "Urban noise sensor network", "doi": "10.4444/noise.8",
                                      "url": "https://elsewhere.example/noise"}], sources={}))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "doi"
    assert "broken_link" in v["problem_types"]
    assert rec["url"] == "https://elsewhere.example/noise"  # never overwritten; final_url shows the working page
    assert v["final_url"] == "https://repo3.example/record/8"


def test_unregistered_doi_with_working_link(monkeypatch):
    Web(monkeypatch, {
        "doi.org/api/handles/": {"status": 404, "body": {"responseCode": 100, "handle": "10.1111/fake"}},
        "repo4.example/r/2": {"body": page("Urban noise sensor network")},
    })
    rec = one(verify.verify_records([{"title": "Urban noise sensor network", "doi": "10.1111/fake",
                                      "url": "https://repo4.example/r/2"}], sources={}))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "http"
    assert "doi_not_registered" in v["problem_types"]
    assert rec["doi"] is None and rec["extra"]["unregistered_doi"] == "10.1111/fake"


def test_blocked_page_with_doi_in_address_is_confirmed_by_doi(monkeypatch):
    url = "https://dv.example/dataset.xhtml?persistentId=doi:10.5072/FK2/ABC123"
    Web(monkeypatch, {
        "doi.org/api/handles/10.5072/fk2/abc123": {"body": {"responseCode": 1, "values": [
            {"type": "URL", "data": {"value": url}}]}},
        "doi.org/10.5072/": {"body": {"type": "dataset", "title": "Replication data for a voting study"}},
        "dv.example": {"status": 403, "body": "<html><head><title>403 Forbidden</title></head><body>403 Forbidden</body></html>"},
    })
    rec = one(verify.verify_records([{"title": "Replication data for a voting study", "url": url}], sources={}))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "doi" and v["problems"] == []
    assert rec["doi"] == "10.5072/fk2/abc123"
    assert any("refused the automated request" in n for n in v["notes"])


# ----------------------------------------------------------------------- HTTP

def test_plain_http_success(monkeypatch):
    Web(monkeypatch, {"buoys.example/set/9": {"body": page("Coastal Buoy Temperature Records 2001-2020 | Example Repository")}})
    rec = one(verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://buoys.example/set/9"}],
                                    sources={}))
    v = ver(rec)
    assert v["verified"] is True and v["method"] == "http" and v["http_status"] == 200
    assert v["final_url"] == "https://buoys.example/set/9" and v["problems"] == []


def test_recorded_thin_page_checked_with_probe(monkeypatch):
    url = "https://www.hub2.example/datasets/owner/some-slug"
    title = verify._parse_html(fixture_text("kaggle_dataset.html"))["title"].split("|")[0].strip()
    web = Web(monkeypatch, {
        "zz-scout-probe": {"status": 404, "body": "<html><head><title>Not here</title></head></html>"},
        url: {"head_status": 404, "body": fixture_text("kaggle_dataset.html")},  # HEAD 404, GET 200, as observed live
    })
    v = ver(one(verify.verify_records([{"title": title, "url": url}], sources={})))
    assert v["verified"] is True and v["method"] == "http"
    assert [m for m, _, _ in web.calls][:2] == ["HEAD", "GET"]
    assert any("zz-scout-probe" in u for u in web.urls())


def test_head_refused_then_get(monkeypatch):
    web = Web(monkeypatch, {"buoys.example/set/9": {"head_status": 405, "body": page("Coastal buoy temperature records")}})
    v = ver(one(verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://buoys.example/set/9"}],
                                      sources={})))
    assert v["verified"] is True and v["http_status"] == 200
    assert [m for m, _, _ in web.calls] == ["HEAD", "GET"]


def test_file_link_is_checked_with_head_only(monkeypatch):
    web = Web(monkeypatch, {"files.example/a.zip": {"ctype": "application/zip", "body": b"PK",
                                                    "headers": {"Content-Length": "987654"}}})
    rec = one(verify.verify_records([{"title": "Archive", "url": "https://files.example/a.zip"}], sources={}))
    assert ver(rec)["verified"] is True and [m for m, _, _ in web.calls] == ["HEAD"]
    assert rec["size"] == {"bytes": 987654}


def test_hard_404(monkeypatch, fake_http):
    fake_http({"repo2.example/records/1": (404, fixture_text("zenodo_404.html"))})
    v = ver(one(verify.verify_records([{"title": "Invented gait set", "url": "https://repo2.example/records/1"}], sources={})))
    assert v["verified"] is False and v["outcome"] == "not_found" and v["http_status"] == 404
    assert v["problem_types"] == ["not_found"] and "HTTP 404" in v["problems"][0]


def test_soft_404(monkeypatch):
    Web(monkeypatch, {"repo2.example/records/1": {"status": 200, "body": fixture_text("zenodo_404.html")}})
    v = ver(one(verify.verify_records([{"title": "Invented gait set", "url": "https://repo2.example/records/1"}], sources={})))
    assert v["verified"] is False and v["outcome"] == "not_found" and v["problem_types"] == ["soft_404"]
    assert "Page not found" in v["problems"][0]


def test_redirect_to_home_page(monkeypatch):
    Web(monkeypatch, {"repo2.example/records/123": {"final": "https://repo2.example/",
                                                    "body": fixture_text("zenodo_home.html")}})
    v = ver(one(verify.verify_records([{"title": "Invented gait set", "url": "https://repo2.example/records/123"}],
                                      sources={})))
    assert v["verified"] is False and v["outcome"] == "wrong_page" and v["problem_types"] == ["redirected_home"]
    assert v["final_url"] == "https://repo2.example/"


def test_redirect_to_search_page(monkeypatch):
    Web(monkeypatch, {"repo2.example/records/123": {"final": "https://repo2.example/search?q=gait",
                                                    "body": page("Search results")}})
    v = ver(one(verify.verify_records([{"title": "Invented gait set", "url": "https://repo2.example/records/123"}],
                                      sources={})))
    assert v["verified"] is False and v["problem_types"] == ["redirected_search"]


def test_repository_home_page_given_as_dataset(monkeypatch):
    Web(monkeypatch, {"repo.example": {"body": fixture_text("zenodo_home.html")}})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: None)}
    v = ver(one(verify.verify_records([{"title": "Arctic sea ice thickness dataset", "url": "https://repo.example/"}],
                                      sources=sources)))
    assert v["verified"] is False and v["outcome"] == "wrong_page" and "home_page" in v["problem_types"]


def test_home_page_of_other_site_needs_a_matching_title(monkeypatch):
    Web(monkeypatch, {"https://bigsite.example/": {"body": page("Bigsite: where data science happens")},
                      "https://oceanbuoys.example/": {"body": page("Ocean Buoy Archive - hourly sea temperature")}})
    result = verify.verify_records([
        {"title": "Arctic sea ice thickness dataset", "url": "https://bigsite.example/"},
        {"title": "Ocean Buoy Archive", "url": "https://oceanbuoys.example/"},
    ], sources={})
    wrong, own_site = result["records"]
    assert ver(wrong)["verified"] is False and ver(wrong)["problem_types"] == ["home_page"]
    assert ver(own_site)["verified"] is True and any("own site" in n for n in ver(own_site)["notes"])


def test_login_wall(monkeypatch):
    login = page("Sign in", extra_head="") .replace("</p></body>", "</p><form><input type='password'></form></body>")
    Web(monkeypatch, {
        "members.example/data/1": {"status": 401, "body": "<html><head><title>Unauthorized</title></head></html>"},
        "portal.example/data/2": {"final": "https://portal.example/accounts/login/?next=/data/2", "body": login},
    })
    result = verify.verify_records([{"title": "Clinic visits", "url": "https://members.example/data/1"},
                                    {"title": "Clinic visits", "url": "https://portal.example/data/2"}], sources={})
    for rec in result["records"]:
        v = ver(rec)
        assert v["verified"] is False and v["outcome"] == "could_not_check"
        assert v["problem_types"] == ["login_required"] and "requires login" in v["problems"][0]


def test_blocked_client_is_not_called_missing(monkeypatch):
    Web(monkeypatch, {
        "waf1.example": {"status": 403, "body": "<html><head><title>403 Forbidden</title></head><body>403 Forbidden</body></html>"},
        "waf2.example": {"status": 202, "body": "", "headers": {"x-amzn-waf-action": "challenge"}},
        "waf3.example": {"status": 429, "body": "slow down"},
        "waf4.example": {"status": 200, "body": "<html><head><title>Just a moment...</title></head><body></body></html>"},
    })
    result = verify.verify_records([{"title": "Survey", "url": "https://waf%d.example/item/1" % i} for i in range(1, 5)],
                                   sources={})
    codes = [ver(r)["problem_types"] for r in result["records"]]
    assert codes == [["blocked"], ["blocked"], ["rate_limited"], ["blocked"]]
    for rec in result["records"]:
        assert ver(rec)["verified"] is False and ver(rec)["outcome"] == "could_not_check"
    assert "does not mean the dataset is missing" in ver(result["records"][0])["problems"][0]


def test_javascript_shell_is_could_not_check(monkeypatch):
    shell = fixture_text("openneuro_shell.html")
    Web(monkeypatch, {"spa.example/datasets/": {"body": shell}})  # the probe address gets the same shell
    v = ver(one(verify.verify_records([{"title": "Emotion perception imaging", "url": "https://spa.example/datasets/ds1"}],
                                      sources={})))
    assert v["verified"] is False and v["outcome"] == "could_not_check" and v["problem_types"] == ["js_shell"]


def test_http_title_mismatch(monkeypatch):
    Web(monkeypatch, {"zz-scout-probe": {"status": 404, "body": "missing"},
                      "repo5.example/r/3": {"body": page("Annual rainfall station records")}})
    v = ver(one(verify.verify_records([{"title": "Pediatric sleep EEG recordings", "url": "https://repo5.example/r/3"}],
                                      sources={})))
    assert v["verified"] is False and v["outcome"] == "wrong_page" and v["problem_types"] == ["title_mismatch"]
    assert v["problems"][0].startswith("the URL exists but describes a different resource")


def test_dns_failure_vs_offline(monkeypatch):
    dns = common.FetchError("x", None, "URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known>")
    Web(monkeypatch, {"invented-host.example": dns, "real.example": {"body": page("Coastal buoy temperature records")}})
    result = verify.verify_records([{"title": "A", "url": "https://invented-host.example/a"},
                                    {"title": "Coastal buoy temperature records", "url": "https://real.example/b"}],
                                   sources={})
    assert ver(result["records"][0])["problem_types"] == ["host_not_found"]
    assert ver(result["records"][0])["outcome"] == "not_found"

    Web(monkeypatch, {"example": dns})  # nothing answers: the network is down, not every host invented
    v = ver(one(verify.verify_records([{"title": "A", "url": "https://invented-host.example/a"}], sources={})))
    assert v["outcome"] == "could_not_check" and v["problem_types"] == ["unreachable"]


def test_unresponsive_adapter_is_skipped_for_the_rest_of_the_run(monkeypatch):
    calls = []

    def slow(url):
        calls.append(url)
        raise common.FetchError(url, None, "timeout: The read operation timed out")

    Web(monkeypatch, {"repo.example": {"body": page("Coastal buoy temperature records")}})
    sources = {"repo": fake_adapter("repo", ["repo.example"], slow)}
    result = verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://repo.example/records/%d" % i}
                                    for i in range(3)], sources=sources, max_workers=1)
    assert len(calls) == 1  # one timeout, then the registry is not asked again in this run
    assert result["summary"]["verified"] == 3 and result["summary"]["by_method"] == {"http": 3}


def test_unresponsive_host_is_skipped_after_two_failures(monkeypatch):
    timeout = common.FetchError("x", None, "URLError: <urlopen error _ssl.c:1112: The handshake operation timed out>")
    web = Web(monkeypatch, {"slow.example": timeout})
    result = verify.verify_records([{"title": "Thing %d" % i, "url": "https://slow.example/r/%d" % i} for i in range(4)],
                                   sources={}, max_workers=1)
    assert len(web.calls) == 2  # HEAD and GET of the first item; the rest are skipped without waiting
    for rec in result["records"]:
        v = ver(rec)
        assert v["verified"] is False and v["outcome"] == "could_not_check" and v["problem_types"] == ["unreachable"]


def test_slow_adapter_is_abandoned_within_its_budget(monkeypatch):
    calls = []

    def slow(url):
        calls.append(url)
        time.sleep(1.0)
        return registry_record()

    monkeypatch.setattr(verify, "ADAPTER_BUDGET", 0.1)
    Web(monkeypatch, {"repo.example": {"body": page("Coastal buoy temperature records")}})
    sources = {"repo": fake_adapter("repo", ["repo.example"], slow)}
    started = time.monotonic()
    result = verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://repo.example/records/%d" % i}
                                    for i in range(2)], sources=sources, max_workers=1)
    assert time.monotonic() - started < 0.9 and len(calls) == 1
    for rec in result["records"]:
        v = ver(rec)
        assert v["verified"] is False and v["outcome"] == "could_not_check"  # never "missing"
    assert any("no answer within" in n for n in ver(result["records"][0])["notes"])


def test_run_budget_turns_leftovers_into_could_not_check(monkeypatch):
    web = Web(monkeypatch, {"example": {"body": page("Coastal buoy temperature records")}})
    result = verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://a.example/r"},
                                    {"title": "X", "doi": "10.5555/x.1"}], sources={}, budget=0)
    assert web.calls == []
    for rec in result["records"]:
        v = ver(rec)
        assert v["verified"] is False and v["outcome"] == "could_not_check"
        assert any("time budget" in text for text in v["problems"] + v["notes"])


def test_title_matching_is_loose_but_not_blind():
    tv = verify._title_verdict
    assert tv("GOTA", ["Global Ocean Temperature Archive"]) is True
    assert tv("Global Ocean Temperature Archive (GOTA)", ["GOTA v2 | Example Repository"]) is True
    assert tv("Coastal buoy temperature records", ["Coastal Buoy Temperature Records 2001-2020 | Repo"]) is True
    assert tv("Voice recordings of patients", ["Patient voice recording set"]) is True
    assert tv("Pediatric sleep EEG recordings", ["Annual rainfall station records"]) is False
    assert tv("Pediatric sleep EEG", ["Rainfall"], ["Sleep EEG of children, pediatric clinic"]) is True
    assert tv(None, ["Anything"]) is None and tv("Something", []) is None


# --------------------------------------------------------------- inputs & batch

def test_minimal_inputs_become_manual_records(monkeypatch):
    Web(monkeypatch, {
        "buoys.example/set/9": {"body": page("Coastal buoy temperature records",
                                             extra_head='<meta name="description" content="Hourly sea temperature.">')},
        "doi.org/api/handles/": {"status": 404, "body": {"responseCode": 100}},
    })
    result = verify.verify_records([
        {"title": None, "url": "https://buoys.example/set/9"},                     # scout.py verify --url
        {"name": "Coastal buoy temperature records", "link": "https://buoys.example/set/9",
         "access": "open", "license": "CC0"},
        {"title": "Some dataset", "doi": "https://doi.org/10.1234/ABC."},
        {"title": "Nothing to check"},
        "not a dict",
        {"title": "Bad DOI", "doi": "10.12/x"},
    ], sources={})
    first, alias, by_doi, nolink, junk, bad = result["records"]
    assert first["id"] == "manual:https://buoys.example/set/9" and first["source"] == "manual"
    assert first["title"] == "Coastal buoy temperature records" and first["description"] == "Hourly sea temperature."
    assert ver(first)["verified"] is True
    assert "claimed_access" not in first["extra"] and first["extra"] is not alias["extra"]   # B1: no shared defaults
    assert alias["access"]["tier"] == "unknown" and alias["extra"]["claimed_access"] == "open"
    assert alias["extra"]["claimed_licence"] == "CC0" and alias["licence"] is None
    assert by_doi["doi"] == "10.1234/abc" and by_doi["url"] == "https://doi.org/10.1234/abc"
    assert ver(by_doi)["problem_types"] == ["doi_not_registered"]
    assert ver(nolink)["problem_types"] == ["no_link"] and ver(nolink)["verified"] is False
    assert ver(junk)["problem_types"] == ["invalid_input"]
    assert ver(bad)["problem_types"] == ["doi_malformed"]
    for rec in result["records"]:
        assert set(rec) >= {"id", "source", "title", "url", "access", "doi", "licence", "retrieved_at", "verification"}


def test_summary_counts(monkeypatch):
    Web(monkeypatch, {
        "doi.org/api/handles/": {"status": 404, "body": {"responseCode": 100}},
        "ok.example/a": {"body": page("Coastal buoy temperature records")},
        "gone.example/b": {"status": 404, "body": "no"},
        "waf.example/c": {"status": 403, "body": "<html><head><title>403 Forbidden</title></head></html>"},
    })
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record())}
    result = verify.verify_records([
        {"title": "Coastal buoy temperature records", "url": "https://repo.example/records/42"},
        {"title": "Coastal buoy temperature records", "url": "https://ok.example/a"},
        {"title": "Lost", "url": "https://gone.example/b"},
        {"title": "Walled", "url": "https://waf.example/c"},
        {"title": "Invented", "doi": "10.5281/zenodo.99999999999"},
    ], sources=sources)
    s = result["summary"]
    assert (s["total"], s["verified"], s["unverified"]) == (5, 2, 3)
    assert s["by_method"] == {"registry-api": 1, "http": 3, "doi": 1}
    assert s["verified_by_method"] == {"registry-api": 1, "http": 1}
    assert s["by_outcome"] == {"confirmed": 2, "not_found": 2, "could_not_check": 1}
    assert s["by_problem"] == {"not_found": 1, "blocked": 1, "doi_not_registered": 1}
    assert result["checked_at"].endswith("Z") and s["registries"] == ["repo"]


def test_one_host_is_never_hit_in_parallel(monkeypatch):
    routes = {"same.example": {"body": page("Coastal buoy temperature records")}}
    for i in range(4):
        routes["other%d.example" % i] = {"body": page("Coastal buoy temperature records")}
    web = Web(monkeypatch, routes, delay=0.05)
    items = [{"title": "Coastal buoy temperature records", "url": "https://same.example/r/%d" % i} for i in range(6)]
    items += [{"title": "Coastal buoy temperature records", "url": "https://other%d.example/r" % i} for i in range(4)]
    result = verify.verify_records(items, sources={}, max_workers=6)
    assert result["summary"]["verified"] == 10
    assert max(web.max_active.values()) == 1
    assert web.max_overall > 1  # different hosts did run side by side


def test_imports_under_system_python():
    import subprocess
    import sys
    scripts = os.path.dirname(os.path.dirname(os.path.abspath(verify.__file__)))
    exe = "/usr/bin/python3"
    if not os.path.exists(exe) or os.path.realpath(exe) == os.path.realpath(sys.executable):
        pytest.skip("no separate system python")
    out = subprocess.run([exe, "-c", "import sys; sys.path.insert(0, %r); from scoutlib import verify; "
                          "print(verify.verify_records([], sources={})['summary']['total'])" % scripts],
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "0"


@pytest.mark.live
def test_live_real_and_invented():
    result = verify.verify_records([
        {"title": None, "url": "https://zenodo.org/records/99999999999"},
        {"title": "Invented", "doi": "10.5281/zenodo.99999999999"},
        {"title": None, "url": "https://zenodo.org/"},
    ])
    assert [ver(r)["verified"] for r in result["records"]] == [False, False, False]
    assert ver(result["records"][1])["problem_types"] == ["doi_not_registered"]


# ------------------------------------------- transfers and addresses (P1, S9)

def test_a_cut_body_does_not_make_the_host_look_dead(monkeypatch):
    cut = common.FetchError("x", 200, "the answer was cut short 3 times", kind="cut_body")
    web = Web(monkeypatch, {"busy.example/r/0": cut, "busy.example": {"body": page("Coastal buoy temperature records")}})
    result = verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://busy.example/r/%d" % i}
                                    for i in range(3)], sources={}, max_workers=1)
    assert [ver(r)["verified"] for r in result["records"]] == [False, True, True]
    assert ver(result["records"][0])["outcome"] == "could_not_check"
    assert len(web.calls) >= 4      # the later items were still fetched


def test_a_typo_in_one_address_does_not_cost_the_others_their_check(tmp_path):
    # The review's case on a local server that answers every page: one address with a space,
    # one without. Real HTTP layer, no fake.
    import http.server

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

        def do_GET(self):
            body = page("Coastal buoy temperature records").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % server.server_address[1]
    try:
        result = verify.verify_records([{"title": "Coastal buoy temperature records", "url": base + "/set/1 x"},
                                        {"title": "Coastal buoy temperature records", "url": base + "/set/2"}],
                                       sources={}, max_workers=1)
    finally:
        server.shutdown()
        server.server_close()
    assert [ver(r)["verified"] for r in result["records"]] == [True, True]


@pytest.mark.parametrize("env,given,expected", [
    ({}, None, 8), ({"HTTPS_PROXY": "http://127.0.0.1:3128"}, None, 2),
    ({"HTTPS_PROXY": "http://127.0.0.1:3128", "DATASET_SCOUT_PARALLEL": "1"}, None, 8),
    ({"DATASET_SCOUT_PARALLEL": "0"}, None, 1), ({"HTTPS_PROXY": "http://127.0.0.1:3128"}, 6, 6),
])
def test_fewer_page_checks_at_once_behind_a_proxy(monkeypatch, env, given, expected):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    seen = []
    real = verify.ThreadPoolExecutor
    monkeypatch.setattr(verify, "ThreadPoolExecutor", lambda max_workers: seen.append(max_workers) or real(max_workers))
    Web(monkeypatch, {"example": {"body": page("Coastal buoy temperature records")}})
    items = [{"title": "Coastal buoy temperature records", "url": "https://h%d.example/r" % i} for i in range(10)]
    verify.verify_records(items, sources={}, max_workers=given)
    assert seen == [expected]


# ------------------------------------------- M5: sites that route by id

def test_site_that_routes_by_id_is_not_mistaken_for_a_javascript_shell(monkeypatch):
    # The review's case: /dataset/174/<slug> serves record 174 whatever the slug, and an
    # unknown id is a clean 404, so the site is not a catch-all and a wrong title is a mismatch.
    shell = page("Parkinsons - Example Archive")[:380]

    def route(method, url, headers):
        if "/dataset/174/" in url:
            return {"body": shell}
        return {"status": 404, "body": "not found"}

    Web(monkeypatch, {"archive.example": route})
    v = ver(one(verify.verify_records([{"title": "Sleep Heart Health Study",
                                        "url": "https://archive.example/dataset/174/parkinsons"}], sources={})))
    assert v["verified"] is False and v["problem_types"] == ["title_mismatch"]


def test_probe_answered_with_the_same_record_is_not_a_catch_all(monkeypatch):
    original = "https://slugs.example/sets/coastal-buoys"
    body = page("Coastal buoys", extra_head='<link rel="canonical" href="%s">' % original)[:420]
    Web(monkeypatch, {"slugs.example": {"body": body}})
    v = ver(one(verify.verify_records([{"title": "Pediatric sleep EEG", "url": original}], sources={})))
    assert v["problem_types"] == ["title_mismatch"]


def test_numeric_id_is_changed_in_the_probe():
    probe = verify._probe_url("https://archive.example/dataset/174/parkinsons")
    assert "/dataset/174/" not in probe and probe.endswith("/parkinsons") and "/dataset/9" in probe


def test_items_on_a_host_held_by_an_abandoned_registry_call_are_could_not_check(monkeypatch):
    # X3 (confirmed, behaviour kept): while an abandoned registry call still holds the host,
    # later items on it are not fetched; they come back "could not check", never "missing",
    # and the message says they were not asked rather than "no response".
    def slow(url):
        time.sleep(1.0)
        return None

    monkeypatch.setattr(verify, "ADAPTER_BUDGET", 0.1)
    Web(monkeypatch, {"repo.example": {"body": page("Coastal buoy temperature records")}})
    sources = {"repo": fake_adapter("repo", ["repo.example"], slow)}
    result = verify.verify_records([{"title": "Coastal buoy temperature records", "url": "https://repo.example/r/%d" % i}
                                    for i in range(3)], sources=sources, max_workers=1)
    for rec in result["records"]:
        v = ver(rec)
        assert v["verified"] is False and v["outcome"] == "could_not_check"
        assert any("still busy" in p and "no response" not in p for p in v["problems"])


def test_a_paper_doi_does_not_rename_the_dataset(monkeypatch):
    Web(monkeypatch, {
        "doi.org/api/handles/": {"body": {"responseCode": 1, "values": [
            {"type": "URL", "data": {"value": "https://journal.example/a/1"}}]}},
        "doi.org/10.7777/": {"body": {"type": "journal-article",
                                      "title": "Coastal buoy temperature records: design and first results"}},
        "journal.example/a/1": {"body": page("Coastal buoy temperature records: design and first results")},
    })
    rec = one(verify.verify_records([{"title": "Coastal buoy temperature records", "doi": "10.7777/abc"}], sources={}))
    assert ver(rec)["verified"] is True and rec["title"] == "Coastal buoy temperature records"


def test_the_reason_for_an_unknown_tier_is_in_the_note(monkeypatch):
    Web(monkeypatch, {})
    sources = {"repo": fake_adapter("repo", ["repo.example"], lambda url: registry_record(
        tier="unknown", evidence="gated=false, but the repository holds only a loading script"))}
    v = ver(one(verify.verify_records([{"title": None, "url": "https://repo.example/records/42"}], sources=sources)))
    assert any(n.startswith("access tier unknown (repo: gated=false, but the repository holds only a loading script)")
               for n in v["notes"])
