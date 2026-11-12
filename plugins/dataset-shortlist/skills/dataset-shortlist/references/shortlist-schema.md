# Shortlist file format

The interactive page is rendered from one JSON file that you write at the end of
the workflow:

```bash
python3 <skill-dir>/scripts/scout.py render dataset-shortlist/shortlist.json --out dataset-shortlist.html
```

Only `question` and `datasets` are required. Leave out what you do not know
rather than inventing it; the page shows missing facts as "not stated".

## Fields

| Field | Type | Notes |
|---|---|---|
| `question` | string | The user's research question, in their words. |
| `generated_at` | string | ISO date and time of the check. |
| `requirements` | list | `{"id": "R1", "text": "...", "must": true}`; `must: false` for nice-to-have. |
| `searched` | object | `{"sources": [...], "queries": [...], "n_candidates": 42}`: what was actually searched. |
| `datasets` | list | The recommended datasets, best first. See below. |
| `not_recommended` | list | `{"name": "...", "url": "...", "reason": "..."}` for candidates the user might expect but that fail a must-have. |
| `gaps` | list of strings | What could not be found. |
| `notes` | string | Anything else the user should know, such as a registry that was down. |

Each entry of `datasets`:

| Field | Type | Notes |
|---|---|---|
| `rank` | integer | 1 is the best. |
| `record` | object | The record exactly as returned by `scout.py verify`, including its `verification` block. Do not retype it: the page shows "Verified" only when that block carries the method and the time of the check. |
| `fit` | string | `strong`, `partial` or `weak`. |
| `why` | string | One or two sentences: why it suits this question. |
| `requirements` | object | Keyed by requirement id: `{"status": "met", "evidence": "...", "url": "..."}`. Status is `met`, `partial`, `unmet` or `unknown`. Evidence is a short quote or a pointer to where you read it. |
| `access_steps` | list of strings | The concrete steps, in order. |
| `time_to_access` | string | `minutes`, `days`, `weeks`, `months` or `unknown`. |
| `caveats` | list of strings | Known limitations, licence restrictions, version notes. |
| `papers` | list | `{"title": "...", "year": 2024, "doi": "...", "url": "...", "note": "what they used it for"}`, only papers returned by the tool or fetched in this session. |

## Access tiers

`record.access.tier` is one of six words. The page shows any other text as
"Unknown", so use these and put the detail in `record.access.evidence`:

| Tier | Shown as | Use it when |
|---|---|---|
| `open` | Open | Direct download, no account and no approval. |
| `account` | Free account | A free account, a login or click-through terms; nobody has to approve you. |
| `gated` | Application required | An application, credentialing, training or the owner's approval comes first. |
| `controlled` | Institutional agreement | An agreement signed by your institution, ethics approval, an access committee, a fee or a secure environment. |
| `closed` | Not obtainable | Withdrawn, under embargo or metadata only. |
| `unknown` | Unknown | You could not establish the condition. |

Records that come out of `verify` already carry one of these. When you write or
correct a tier by hand, `render` accepts a few plain words that state a
restriction ("application", "registered", "fee", "restricted") and prints what
it showed them as; it never reads a word as `open` except `open` itself.

## Example

The names below are invented to show the shape.

```json
{
  "question": "I want to predict river flooding one day ahead for small catchments. What data can I use?",
  "generated_at": "2026-01-15T09:30:00Z",
  "requirements": [
    {"id": "R1", "text": "Daily or finer river discharge for many small catchments", "must": true},
    {"id": "R2", "text": "Matching rainfall for the same catchments", "must": true},
    {"id": "R3", "text": "Commercial use allowed", "must": false}
  ],
  "searched": {
    "sources": ["openaire", "zenodo", "datacite"],
    "queries": ["catchment discharge daily", "streamflow rainfall dataset", "flood forecasting benchmark"],
    "n_candidates": 37
  },
  "datasets": [
    {
      "rank": 1,
      "record": {
        "id": "zenodo:0000000",
        "source": "zenodo",
        "title": "Example Catchment Hydrology Collection",
        "url": "https://example.org/records/0000000",
        "access": {"tier": "open", "evidence": "access_right=open"},
        "licence": {"id": "CC-BY-4.0", "name": "Creative Commons Attribution 4.0", "url": null, "commercial_use": true, "share_alike": false},
        "size": {"bytes": 2400000000, "files": 12},
        "year": 2024,
        "verification": {"verified": true, "method": "registry-api", "http_status": 200, "final_url": "https://example.org/records/0000000", "checked_at": "2026-01-15T09:21:00Z", "problems": [], "notes": []}
      },
      "fit": "strong",
      "why": "Daily discharge and rainfall for 600 catchments under 500 square kilometres, 1990 to 2022.",
      "requirements": {
        "R1": {"status": "met", "evidence": "README: 'daily mean discharge, 612 gauges'", "url": "https://example.org/records/0000000"},
        "R2": {"status": "met", "evidence": "README: 'catchment-average daily precipitation'", "url": "https://example.org/records/0000000"},
        "R3": {"status": "met", "evidence": "licence CC BY 4.0"}
      },
      "access_steps": ["Open the record page", "Download the archive (2.4 GB)"],
      "time_to_access": "minutes",
      "caveats": ["Gauges are concentrated in two countries"],
      "papers": [{"title": "An example benchmark for flood forecasting", "year": 2025, "doi": "10.0000/example.1", "url": "https://doi.org/10.0000/example.1", "note": "one-day-ahead forecasting baseline"}]
    }
  ],
  "not_recommended": [
    {"name": "Example Global Runoff Archive", "url": "https://example.org/runoff", "reason": "Monthly values only, so it fails R1."}
  ],
  "gaps": ["No open dataset with sub-daily discharge for small catchments was found."],
  "notes": "One registry did not answer during the search, so coverage of institutional repositories may be incomplete."
}
```

## Checks before rendering

- Every dataset has a `record` that came out of `scout.py verify`, and you have
  read its `verification.problems`.
- The access condition in the record matches what you wrote in `access_steps`.
  If you corrected an `unknown` tier after reading the landing page, set
  `record.access` to the tier you found and put the quoted sentence in
  `record.access.evidence`.
- Each must-have requirement has a status for each dataset.
