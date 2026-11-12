# dataset-shortlist: build specification (v0.1)

This file is the contract between the modules. Read it before writing any code.

## What the product is

An Agent Skill that answers "I want to study X: what data can I actually get?".
It searches dataset registries, verifies that every dataset really exists, states
how the data can be obtained and under which licence, checks the fit against the
research question, and renders one interactive HTML page.

The skill must be measurably better than the same model without it. The edge comes
from three things plain model answers get wrong: datasets or links that do not
exist, wrong access conditions (calling gated data "public"), and missing the
less famous datasets. Every module exists to serve one of those three.

## Layout

```
plugins/dataset-shortlist/skills/dataset-shortlist/
  SKILL.md
  scripts/scout.py                 CLI entry point (do not edit unless you own it)
  scripts/scoutlib/common.py       HTTP, record schema, licences, dedupe (shared; do not edit)
  scripts/scoutlib/sources/*.py    one adapter per registry
  scripts/scoutlib/verify.py       existence checks and enrichment
  scripts/scoutlib/literature.py   papers on a topic / papers using a dataset
  scripts/scoutlib/render.py       shortlist JSON -> interactive HTML
  assets/report_template.html
tests/test_<module>.py             pytest, offline by default
tests/fixtures/<module>/           recorded API responses (small, real)
```

## Hard rules for every module

1. Python standard library only, Python 3.8+ syntax. No `match`, no `X | Y` in
   runtime expressions (annotations are fine: every file starts with
   `from __future__ import annotations`). It must run under `/usr/bin/python3`
   (3.9, no third-party packages).
2. All HTTP goes through `scoutlib.common.http_request` / `get_json` / `get_text`.
   They honour proxy environment variables, throttle per host, retry 429 and 5xx,
   and send a generic User-Agent. Never send an e-mail address, API key or any
   personal detail. Never install your own `ProxyHandler` or open raw sockets.
3. No API key may be required. If a registry offers optional keys, read them from
   an `EVAL_*`-style environment variable only if present, and work without it.
4. Be polite: at most 3 requests per `search()` call, small page sizes, timeouts
   of 20 s or less.
5. Never guess. If the registry metadata does not state the access condition, the
   tier is `unknown`. A wrong `open` sends a researcher down a dead end, which is
   the exact failure this skill exists to prevent.
6. Do not hard-code dataset names, dataset lists or "recommended datasets"
   anywhere in code, docs, tests or examples of the skill directory. Adapters
   describe how a REGISTRY works, not which datasets are good. (Test fixtures
   recorded from live API responses are fine: they are data, and they live
   outside the skill directory.)
7. Functions return data; only `scout.py` prints. Errors: raise
   `common.FetchError` for network or API failures; never swallow an error into
   an empty list silently.
8. Do not run git commands. Do not edit files you do not own (see your brief).

## Record schema (one dataset)

Build records only with `common.make_record(...)`.

| Field | Type | Meaning |
|---|---|---|
| `id` | str | `"<source>:<registry id>"`, stable |
| `source` | str | adapter NAME |
| `title` | str | plain text |
| `url` | str | landing page a human can open |
| `access` | `{tier, evidence}` | tier is one of `open`, `account`, `gated`, `controlled`, `closed`, `unknown`; evidence names the metadata field and value, e.g. `access_right=restricted` |
| `description` | str | plain text, up to 700 characters |
| `doi` | str or null | bare DOI, lower case |
| `publisher` | str or null | the hosting repository or organisation |
| `creators` | list of str | up to 5 |
| `year` | int or null | publication year |
| `version` | str or null | |
| `updated` | str or null | ISO date of the last update |
| `licence` | object or null | from `common.normalise_licence(name, url)` |
| `size` | object or null | `{bytes, files, records, text}`; any key may be missing |
| `formats` | list of str | file formats or modalities |
| `subjects` | list of str | keywords |
| `usage` | object | `{downloads, citations, likes, views}`; only what the registry reports |
| `extra` | object | small registry-specific facts worth keeping (for example `gated: "manual"`) |
| `retrieved_at` | str | set automatically |

Access tiers:

| Tier | Meaning |
|---|---|
| `open` | direct download, no account, no approval |
| `account` | free account, login or click-through terms; no human approval |
| `gated` | application, credentialing, training or owner approval first |
| `controlled` | institutional agreement, ethics approval, access committee, fee or secure enclave |
| `closed` | not obtainable (withdrawn, embargoed, metadata only) |
| `unknown` | the registry does not say |

## Adapter interface (`scoutlib/sources/<name>.py`)

```python
NAME = "zenodo"
DESCRIPTION = "General-purpose research repository; any field; explicit access flag and licence."
HOSTS = ("zenodo.org",)            # landing-page hosts this adapter understands

def search(query, limit=20):       # -> list of records, best match first
def lookup(url_or_id):             # -> one record with full metadata, or None
```

`lookup` is what the verifier calls to confirm a landing page and to fill in
licence, access, version and size from the registry itself. Implement it whenever
the registry has a per-record endpoint.

## Verifier (`scoutlib/verify.py`)

`verify_records(records) -> {"checked_at": iso, "records": [...]}`. Input items are
full records or minimal `{"title": ..., "url": ...}` dicts (datasets the agent
found on the web or in a paper). Each output record gains:

```json
"verification": {
  "verified": true, "method": "registry-api", "http_status": 200,
  "final_url": "https://...", "checked_at": "2026-11-11T14:00:00Z",
  "problems": [], "notes": ["licence filled from the registry record"]
}
```

`method` is `registry-api` (an adapter's `lookup` confirmed it), `doi` (the DOI
resolved to a landing page) or `http` (the page answered 2xx and does not look
like an error page). `verified` is false when nothing confirmed the dataset; say
why in `problems`. Enrichment may fill empty fields but must never overwrite a
registry-derived access tier with a guess from page text.

## Literature (`scoutlib/literature.py`)

```python
search_papers(query, limit=10, year_from=None)   # papers on a topic
papers_mentioning(dataset_name, limit=10)        # papers that use a named dataset
papers_citing(doi, limit=10)                     # works that cite a dataset DOI
```

Each returns `{"query": ..., "source": ..., "works": [...], "errors": {...}}` with
works as `{title, year, venue, doi, url, authors (<=5), cited_by, abstract, type}`.
Missing values are null. Metadata comes from the API response only, never typed
from memory.

## Shortlist (input of `scoutlib/render.py`, written by the agent)

```json
{
  "question": "the user's research question, verbatim",
  "generated_at": "2026-11-11T14:00:00Z",
  "requirements": [{"id": "R1", "text": "adult ICU stays", "must": true}],
  "searched": {"sources": ["openaire", "zenodo"], "queries": ["..."], "n_candidates": 87},
  "datasets": [{
    "rank": 1,
    "record": {"...": "a verified record, including its verification block"},
    "fit": "strong",
    "why": "one or two sentences",
    "requirements": {"R1": {"status": "met", "evidence": "quote or pointer", "url": "https://..."}},
    "access_steps": ["Create an account", "Complete the required training", "Sign the agreement"],
    "time_to_access": "days",
    "caveats": ["..."],
    "papers": [{"title": "...", "year": 2024, "doi": "10.x/y", "url": "https://...", "note": "used it for ..."}]
  }],
  "not_recommended": [{"name": "...", "url": "https://...", "reason": "..."}],
  "gaps": ["..."],
  "notes": "free text"
}
```

`fit` is `strong`, `partial` or `weak`. Requirement `status` is `met`, `partial`,
`unmet` or `unknown`. `time_to_access` is `minutes`, `days`, `weeks`, `months` or
`unknown`. The renderer must tolerate missing optional keys.

## Tests

- `tests/test_<module>.py`, pytest style, offline: load recorded responses from
  `tests/fixtures/<module>/` and monkeypatch `scoutlib.common.http_request`.
- One live test per module, skipped unless the environment variable
  `SCOUT_LIVE=1` is set.
- Run with `/opt/anaconda3/bin/python3 -m pytest tests/test_<module>.py -q` from
  the repository root. Also prove the module imports and runs under
  `/usr/bin/python3`.
