# dataset-scout code review (2026-11-12)

Reviewer: an independent agent that did not write the code. This review only reports: no repository file was edited and no git command was run.

**Scope:** `scripts/scout.py`; `scoutlib/{common,literature,verify,render}.py`; `scoutlib/sources/{__init__,openaire,datacite,zenodo,huggingface,physionet}.py`; `assets/report_template.html` (script-injection safety and obvious breakage only); `tests/`. Paths below are relative to `plugins/dataset-scout/skills/dataset-scout/` unless they start with `tests/`. Line numbers refer to the files as they were on 2026-11-12.

**How the findings were checked:**
- "Live" means a real call made on 2026-11-12. "No network" means the step used recorded fixtures, the PhysioNet catalogue disk cache (`$TMPDIR/dataset-scout-cache`, fresh at the time) or local sockets.
- Network use, disclosed: I made 3 direct probes with curl (OpenAIRE `pid=`, DataCite `/dois/<doi>`, Hugging Face `/api/datasets/<id>`). The requested CLI flow (item 4 of the brief) and the verifier tests then made about 90 to 100 requests through the tool's own throttled client, spread over about 8 hosts and serialised per host. I read the "under 25 requests" limit as applying to my own direct probes.
- Working files are in `<scratch>/review/flow/`: `judge.json`, `conflict.json`, `invented.json`, `dataset-scout/candidates.json`, `verified.json`, `shortlist.json` and `dataset-shortlist.html`. Scripts: `hang_probe.py`, `nodecheck.js`.

**Totals:** 28 findings: 3 blockers, 13 should fix, 12 minor (25 confirmed, 3 suspected).

---

## CONFIRMED (reproduced)

### Blockers

**B1. blocker: `scoutlib/common.py:246-286` (`make_record`).** Records built in the same process share one `extra` dict and one `usage` dict, so registry facts leak from one record into another.
- **Cause:** `value = fields.get(key, default)` returns the single module-level `{}` from `_RECORD_DEFAULTS` whenever the caller does not pass `extra` or `usage`. The `value is None` branch only fires for an explicit None. `verify._merge` then writes registry facts into that shared dict, which also mutates `_RECORD_DEFAULTS` itself.
- **Who is affected:**
  - every minimal input in one verify batch (`verify --url A --url B ...`, or a file of `{title, url}` dicts, as the SPEC allows);
  - every PhysioNet record built in one process, because that adapter never passes `usage`.
  - Full records loaded from a candidates file are deep-copied, so they are not affected.
- **Repro (1 Zenodo request; PhysioNet from the disk cache):** `scout.py verify --url https://zenodo.org/records/17753641 --url https://physionet.org/content/kinecal/1.0.3/ --out leak.json`.
  - Both records get `usage = {"downloads": 61, "views": 314}`, which are Zenodo's counts. The page then says "The registry reports 61 downloads, 314 views" for the PhysioNet dataset.
  - Both get the same `extra`: `{"slug": "kinecal", "project_doi": "10.13026/8bsb-ch59", "record_id": "17753641", "concept_doi": "10.5281/zenodo.17753640", ...}`.
  - A batch of three PhysioNet URLs (`conflict.json`) gave the MIMIC-IV-ECG record KINECAL's slug, project DOI and version note. `_merge` only adds missing keys, so the second record's own values are never written.
  - The same leak carries `data_use_agreement`, `claimed_access`, `claimed_licence` and `unregistered_doi` onto unrelated records.
  - The scenario of `tests/test_verify.py::test_minimal_inputs_become_manual_records` already shows it: its first item, which claims nothing, comes back with `extra = {"claimed_access": "open", "claimed_licence": "CC0"}`, the same object as the second item's. The test simply never asserts on it.
- **Fix:** use `value = fields.get(key); if value is None: value = copy.deepcopy(default)`. Add a test that two default records do not share `extra` or `usage`.

**B2. blocker: `scoutlib/sources/huggingface.py:61-63` (`_access`).** `gated=false` becomes tier `open` ("direct download, no account, no approval") even when the repository holds no data, only a loading script that downloads the data from somewhere else.
- **Repro (live probe):** `GET https://huggingface.co/api/datasets/bigbio/n2c2_2018_track2` returns:
  - `gated: false`;
  - tags: only `license:other` (no `format:` or `modality:` tag);
  - siblings: `.gitattributes, README.md, bigbiohub.py, n2c2_2018_track2.py`, i.e. no data files.
  - `huggingface._record(<that JSON>)` gives `{"tier": "open", "evidence": "gated=false"}`.
  - Loader-only Hub repos of clinical and NLP corpora that are distributed elsewhere under agreements are common. This is the "gated data called public" failure the skill exists to prevent.
- **Fix:** treat `gated=false` as proof only that the Hub repo is not gated.
  - The single-record endpoint returns `siblings`. When they hold only `*.py`, `*.md` and `.gitattributes`, return `unknown` with evidence "gated=false, but the repository holds only a loading script", and set `extra.loader_only`.
  - Search listings carry no `siblings` (checked in all three recorded search fixtures). There, call a repo `open` only when the Hub's own `format:` tag is present (real data repos in the fixtures have `format:audiofolder` / `format:imagefolder`); otherwise return `unknown`.
  - Do this in `_record`, not only in `lookup`: `verify._merge` never downgrades a tier the search already set.

**B3. blocker: `scoutlib/verify.py:745-761` (`_title_verdict`), `1040-1054` (`_accept_registry`), `1183-1196` (`_verify_http`).** An invented dataset name attached to a real record URL comes back VERIFIED, and the record keeps the invented name.
- **Cause:** the title check passes when the given title's words appear in the registry description (the secondary texts, threshold 0.5). The registry's real title is stored only in `verification.found_title`. The page never shows it (`found_title` occurs 0 times in `report_template.html`), and no problem is raised.
- **Repro (no network; PhysioNet cache):** `verify invented.json`, with item `{"title": "Sleep Apnea Smartwatch Dataset", "url": "https://physionet.org/content/slpdb/1.0.0/"}`.
  - Result: `VERIFIED [manual | open | ODC-By-1.0 | 1999] Sleep Apnea Smartwatch Dataset`, `found_title = "MIT-BIH Polysomnographic Database"`, `problems = []`.
  - Two other invented names in the same batch were correctly caught as `title_mismatch`.
  - Impact: a misremembered or invented name, together with an invented modality ("smartwatch"), gets a green Verified stamp.
- **Fix:**
  - When the record is confirmed only through description or slug text (primary-title coverage below about 0.6), replace `title` with the registry or page title.
  - Keep the given title in `extra.given_title` and add a problem `title_differs` ("given as X; the registry calls it Y").
  - Show `found_title` on the page whenever it differs from the title.

### Should fix

**S1. should fix: `scoutlib/sources/physionet.py:237-245` (`lookup`) with `verify._accept_registry`.** A URL that names an old version is answered with the latest version's access tier, licence, DOI and version number, while the record keeps the old version's URL.
- **Scale:** the catalogue lists every version, and in the cached catalogue (760 entries) 9 projects change access policy between versions and 14 change licence. Examples:
  - `kinecal` 1.0.0: Restricted, with the PhysioNet Restricted licence; 1.0.3: Open, CC0.
  - `mimic-iv-ecg` 0.1 to 0.3: Credentialed; 1.0: Open.
  - `ct-ich` 1.3.0: Open, CC BY; 1.3.1: Restricted.
- **Repro (no network):** `{"title": "KINECAL", "url": "https://physionet.org/content/kinecal/1.0.0/"}` gives `VERIFIED [manual | open | CC0-1.0]`, version `1.0.3`, with the URL still `.../kinecal/1.0.0/`. The mismatch appears only in `extra.note`, not in `verification`.
- **Fix:** return the entry for the requested version when it is listed, and put the latest version and its tier in `extra.latest_version` plus a verification note. If the requested version is not listed, add a problem.
- **Test impact:** `tests/test_physionet.py::test_lookup_old_version_url_notes_it` pins the current behaviour and must change.

**S2. should fix: `scoutlib/verify.py:833-846` (`_merge`) and `assets/report_template.html:1805-1816, 1848-1853, 1412`.** When the input record and the registry that hosts the landing page disagree on access, the input tier is kept and the record stays `verified: true`. The conflict is written only to `verification.problems`, and the page shows `problems` only for unverified datasets: every use of `v.problems` in the template sits in a `!verified` branch.
- **Repro (no network; the trigger record is hand-built, because live OpenAIRE returned `bestAccessRight: null` for this DOI):** `{"source": "openaire", "id": "openaire:x", "title": "MIMIC-IV", "url": "https://physionet.org/content/mimiciv/3.1/", "access": {"tier": "open", "evidence": "bestAccessRight=OPEN"}}`.
  - It comes back `VERIFIED [openaire | open | custom: PhysioNet Credentialed Health Data Lice...]` with an "access tier conflict" problem.
  - Rendered into `dataset-shortlist.html`, the no-JavaScript list reads "MIMIC-IV. Access: Open. Licence: PhysioNet Credentialed Health Data License 1.5.0. Verified on 11 November 2026.". The interactive page normalises it as Open and verified (checked with `nodecheck.js`), with no warning.
  - Other problems a verified record can carry are hidden the same way: `broken_link` (the record's own `url` is dead, yet the page links to it), `doi_not_registered` and `doi_malformed`.
- **Fix:**
  - When the hosting registry (the adapter chosen for the given URL, or the landing adapter on the DOI path) disagrees, adopt the more restrictive tier, or set the tier to `unknown` and record both pieces of evidence. The SPEC forbids overwriting a registry tier with a guess from page text; it does not require keeping an aggregator's claim over the host's own record.
  - Render `v.problems` for verified records too, as a warning block.
- **Test impact:** `tests/test_verify.py::test_never_overwrite_a_registry_tier` pins "keep the input tier" and must change.

**S3. should fix: `scoutlib/common.py:203-241` (`normalise_licence`).** Several realistic spellings produce a wrong licence id with `commercial_use: true`. Calling the function directly:
- `"CC BY NC 4.0"`, `"CC BY NC-SA 4.0"`, `"CC BY ND 4.0"`: space-separated forms, as found in OpenAIRE instance licences (the recorded fixture has `"CC BY"`) and free-text DataCite rights, all give `CC-BY-4.0` with commercial=True. Only the hyphenated `by-nc` forms are recognised before the generic `cc[- ]by` rule fires.
- `"Use of the data requires a signed agreement; see the Database Use Policy (MIT)"` gives `MIT`, commercial=True. Any custom terms that mention the institution become the MIT licence.
- `"Creative Commons Attribution 4.0 International; non-commercial research use only"` gives `CC-BY-4.0`, commercial=True.
- `"Apache License 2.0 for code; data under CC BY-NC 4.0"` gives `CC-BY-NC-2.0`: the version is taken from the first `d.d` in the whole text.
- Smaller errors: `BSD 2-Clause` gives `BSD-3-Clause`; `GNU General Public License v2.0` gives `GPL-3.0`; `Public Domain Mark` gives `PDDL-1.0`.
- **Fix:**
  - Allow `[-_ ]` as the separator in every CC pattern.
  - Match MIT only as `^mit$`, `mit license` or an SPDX id.
  - Never return `commercial_use: true` when the text contains "non-commercial" or "noncommercial".
  - Take the version number from the matched token.
  - Add a table-driven test.

**S4. should fix: `scoutlib/common.py:289-316` (`dedupe`) and `scoutlib/sources/datacite.py:164-205` (`collapse_versions`).** Both merge on title plus publisher.
- **(a) Distinct datasets are merged.** Two records with different DOIs and no version relation become one:
  - `dedupe` of two `"Dataset"` records on Zenodo (DOIs `.111` open and `.222` restricted) keeps one; the other survives only as an `also_found_in` pointer.
  - `collapse_versions` of two DataCite records titled `"Data"` on figshare (DOIs `10.1234/aaa` and `10.9999/bbb`) keeps one, with the other listed in `extra.other_dois` as an "old version".
  - Generic titles ("Dataset", "Data", "Data_Sheet_1.docx") are common on Zenodo, figshare and Frontiers.
- **(b) A tier conflict is resolved silently.** When both copies have a known tier, the first record wins with no note. `scout.py search` orders sources alphabetically, so an `openaire` aggregated claim beats the hosting `physionet` or `zenodo` record (shown with constructed records).
- **(c) Copies of one dataset under a concept DOI and a version DOI are not merged.**
  - Live: the first search listed the same figshare item twice, as #6 (datacite, `10.6084/m9.figshare.20022192.v1`, access unknown) and #16 (openaire, `10.6084/m9.figshare.20022192`, open). The OpenAIRE copy even had the `.v1` DOI in `extra.all_dois`.
  - Live OpenAIRE also gives MIMIC-IV the concept DOI `10.13026/07hj-2a80` first, with `publisher: null`.
- **Fix:**
  - Never merge on title when both records carry DOIs that differ and are not version-linked.
  - Key on all known DOIs (`extra.all_dois`, `extra.concept_doi`, `extra.project_doi`).
  - On a tier conflict, record it (for example in `extra.access_conflicts`) and prefer the host's record, or the more restrictive tier.

**S5. should fix: `scripts/scout.py:169-192` (`cmd_add`).** Running `add` without `--title` stores the URL as the title (`args.title or url`). `verify` then compares that URL text with the registry title and marks a real dataset as a different resource.
- **Repro (live):** `add candidates.json --url https://zenodo.org/records/22036480`, then `verify --pick 26`, gives `NOT VERIFIED ... the zenodo record is titled "Arabic Parkinson's Disease Speech Dataset", not "https://zenodo.org/records/22036480"`. `add --doi X` without a title has the same root cause (the title becomes `https://doi.org/X`).
- **Two side problems in the same command:**
  - `--note` ("where you found it") is stored as the dataset `description`. That blocks the page description from being filled in, and the page shows the note as the dataset's description.
  - Records are never matched by URL: record 26 duplicated record 20 (`zenodo:22036480`, same URL).
- **Fix:**
  - Leave `title` empty when it is not given, or have `_title_verdict` treat a URL or DOI as no title.
  - Store the note in `extra.found_via`.
  - Add the normalised URL as a `dedupe` key.

**S6. should fix: `scoutlib/sources/openaire.py:44-50` (`access_from_best_access_right`).** `bestAccessRight=OPEN` on a metadata-only product becomes tier `open`.
- **Live:** the search "parkinson voice recordings" returned `openaire:opentrials__::52c2...`, a clinical-trial registration (publisher `nct`, url `http://apps.who.int/trialsearch/Trial3.aspx?trialid=NCT00123084`). It was listed as `[openaire | open | no licence stated] Efficacy of Voice Treatment for Parkinson's Disease`.
- A registration holds no data. The SPEC's tier for "metadata only" is `closed`, or at least `unknown`.
- **Fix:** use `unknown` for trial-registry products (`opentrials__` ids, publisher `nct` or ISRCTN) and for products whose only instance URL is a registry or search page. Use evidence such as "bestAccessRight=OPEN describes the metadata record".

**S7. should fix: `scoutlib/literature.py:171-187` (`_datacite_citing`, the fallback behind `papers --doi`).** It matches any `relatedIdentifiers` entry, so it returns the dataset's own versions as "works that cite it".
- **Repro (live):** `scout.py papers --doi 10.5281/zenodo.17753640` (a Zenodo concept DOI) gives `source: datacite`, and work 1 is `10.5281/zenodo.17753641`, the same dataset's version record. An agent filling `papers` in the shortlist would list the dataset as a paper that used it.
- **Fix:** keep only citation relations (Cites, References, IsSupplementTo, IsDerivedFrom, Documents), and drop records in the same DOI family and Dataset records that are linked only by version relations.

**S8. should fix: `scoutlib/common.py:97-139` (`http_request`) and `scripts/scout.py:133-140` (`cmd_search`).** One registry that accepts the connection but never answers holds the whole `search` command for about 65 s.
- **Cause:** each request makes 3 attempts of 20 s each plus 4.5 s of backoff, and `cmd_search` waits on every future with no deadline.
- **Measured (`hang_probe.py`):** a local socket that accepts and never replies, set as `zenodo.API`, gave `FetchError after 64.8 s`, with 3 connections opened.
- An agent runs 4 to 6 searches in a session, so one dead registry costs 4 to 6 minutes. Retrying a timeout twice is also the least polite choice towards a struggling host. `verify` already handles this well (10 s timeout, adapter and run budgets).
- **Fix:** do not retry socket timeouts (or retry once, briefly). Give `cmd_search` a per-source deadline (`future.result(timeout=...)` against a shared budget of about 30 s) that reports `SOURCE FAILED <name>: no answer within N s`.

**S9. should fix: `common.http_request` (lines 133-139) and `verify._request` (lines 490-493).** A deterministic `http.client.InvalidURL`, such as a URL containing a space, is retried as if it were a network error. In `verify`, it then counts as a host failure.
- **Repro (no network; a local HTTP server that answers every page):**
  - `common.http_request("http://127.0.0.1:9/a b")` raises `FetchError ... no response InvalidURL` after 4.8 s of retries.
  - Verifying `[".../set/1 x", ".../set/2"]` on that server returns the second, valid page as `could_not_check: skipped: 127.0.0.1:... did not respond to 2 earlier requests in this run`. One typo in one candidate makes every other dataset on the same portal unverifiable for the rest of the run.
- **Fix:** raise `FetchError` immediately for `ValueError` / `InvalidURL` with no retry, do not count it as a host failure, and percent-encode spaces before requesting.

**S10. should fix: `scripts/scout.py:88-95` (`_print_records`).** The digest prints only `notes[:2]`, and the notes it drops are the access warnings.
- Checked on my verify outputs:
  - For the MIMIC-III paper DOI, the hidden notes include "the landing page mentions 'data use agreement'", "...'restricted access'", "...'request access'" and "access tier unknown: ... read the landing page before calling the data open".
  - For the figshare record, the only hidden note is the "access tier unknown" warning.
- The SKILL tells the agent to work from this digest.
- **Fix:** always print access hints and the "access unknown" note, and cap only the routine "filled from" and "confirmed by" notes.

**S11. should fix: `scoutlib/sources/huggingface.py:171-181` (`lookup`) and `scripts/scout.py:205-222` (`cmd_lookup`).** For a missing repository the Hub answers 401 (`{"error":"Invalid username or password."}`), not 404. `lookup` raises on it, and `cmd_lookup` catches no `FetchError`.
- **Repro (live):** `scout.py lookup https://huggingface.co/datasets/nonexistent-user-xyz/nonexistent-dataset-abc` ends in a raw Python traceback that says "Invalid username or password.". An agent may conclude that it needs credentials.
- `verify` copes with this (it reaches `not_found` through the soft-404 text).
- **Fix:** have `huggingface.lookup` return None on 401/404 ("not a public repo"), and make `cmd_lookup` catch `FetchError` and print a one-line message.

**S12. should fix: `scoutlib/literature.py:23-29` (`_openalex_params`).** The OpenAlex key is sent as a URL parameter. When OpenAlex fails, `FetchError` embeds the full URL, `search_papers` copies it into `errors["openalex"]`, `_print_works` prints it, and `--out` writes it to disk.
- **Repro (no network; fake 503):** `EVAL_OPENALEX_KEY=SECRET-KEY-123` gives `"SECRET-KEY-123" in json.dumps(result["errors"]) == True`.
- The function also reads the non-`EVAL_*` name `OPENALEX_API_KEY`, while SPEC rule 3 asks for an `EVAL_*`-style variable.
- **Fix:** redact `api_key=` from error strings (for example in `FetchError.__init__`, or before storing the error), and read only `EVAL_OPENALEX_KEY`.

### Minor

**M1. minor: `scoutlib/common.py:89-94` (`_throttle`).** The throttle is not thread-safe. Four threads that called `_throttle("https://same.example/x")` together left at gaps of `[0.342, 0.0, 0.002]` s. Nothing triggers this today, because `cmd_search` runs adapters with distinct hosts and `verify` serialises hosts with its own `_Locks`. But any adapter that shares a host, or a threaded caller of `literature`, silently loses the politeness promised in SPEC rule 2. **Fix:** take a module lock and reserve the slot before sleeping.

**M2. minor: null list entries crash a whole adapter.** One bad item loses every result from that registry, which is then reported as `SOURCE FAILED <name>: AttributeError`. Each case below was tested offline on a fixture with one field nulled:
- `datacite.record_from_item`: `relationships.client.data = null` (line 156: `.get("data", {})` returns None), and `creators = [null]`;
- `datacite.collapse_versions`: a str `publicationYear` next to an int one raises TypeError in the `_sort` comparison;
- `openaire.record_from_item`: `authors = [null]` and `pids = [null]`;
- `zenodo._record`: `creators = [null]`.

None of these was seen in today's live data. **Fix:** guard with `(x or {})`, and skip and count bad items inside `search`.

**M3. minor: `common.dedupe` (line 311) / `cmd_add`.** Re-finding a record in a later search, or adding it twice, appends the record to its own `also_found_in`. After the second search, `huggingface:birgermoell/Italian_Parkinsons_Voice_and_Speech` listed itself; `manual:parkinsons` did the same after a repeated `add`. The page then shows "also found in" pointing at the record itself, and the digest counts these as "duplicates merged". **Fix:** skip the append when the `id` is the same.

**M4. minor: `scripts/scout.py:205-222` (`cmd_lookup`) with a bare DOI.**
- A DOI is routed only to DataCite. For a Crossref DOI (live: `lookup 10.1038/sdata.2016.35`) the tool prints "the datacite registry has no record for this" with exit 1, which reads as "the DOI does not exist".
- A PhysioNet DOI (`lookup doi:10.13026/kpb9-mt58`) returns DataCite's `unknown` tier, while the hosting adapter knows the data are Credentialed, because `lookup` never follows `extra.landing_page` to that adapter (`verify` does).
- **Fix:** say "DataCite has no record; the DOI may belong to another agency, run verify", and route through the landing page as `_resolve_doi` does.

**M5. minor: `scoutlib/verify.py:619-653` (`_probe_url` / `_catch_all`).** The probe changes only the trailing slug, so sites that route by id and ignore the slug are diagnosed as JavaScript shells.
- **Live:** `{"title": "Sleep Heart Health Study", "url": "https://archive.ics.uci.edu/dataset/174/parkinsons"}` comes back "could not check: archive.ics.uci.edu answers any address with the same page", when it should be `title_mismatch`. An invented id on the same site (`/dataset/987654/parkinsons`) is a clean 404, so the site is not a catch-all.
- **Fix:** compare the probe page's `canonical` link with the original's, or change an id-like segment as well.

**M6. minor: `scoutlib/sources/huggingface.py:125-133` (`_score`).** Popularity (`log10(downloads)`) outweighs matching both query words. In the live search "parkinson voice recordings", `saeedzou/kcl-parkinson-voice-dataset` (both words) ranked below `Hebrish/Hebrish-TTS-Voice-Recordings` and `omegalabsinc/omega-voice` (voice only).

**M7. minor: `scoutlib/sources/zenodo.py:51-64` (`build_queries`).** The third pass keeps the two longest words, which drops short specific terms. The live search "ICU/ward mortality: adults" fell back to `mortality AND adults` and returned stroke incidence in Denmark and tree seedlings.

**M8. minor: `assets/report_template.html:1163-1165` (`normVerification`) and `render._fallback_item`.** Any `verification: {"verified": true}` renders as "Verified", even without `method` or `checked_at`. A hand-built record in my `shortlist.json` (#4) rendered as Verified. Since the agent writes the shortlist by hand, consider requiring `method` and `checked_at` before showing the stamp.

**M9. minor: `scripts/scout.py:228-232` (`cmd_verify`).** When both a file and `--url` are given, the file is ignored silently.

**M10. minor: `scoutlib/sources/openaire.py:161-173`.** `lookup` is unreachable: `HOSTS = ()`, `verify` routes DOIs only to DataCite, and `cmd_lookup` uses `source_for_url`. Either wire it in as a DOI fallback for the access tier, or delete it.

---

## SUSPECTED (not reproduced to the end)

**X1. should fix (suspected): `scoutlib/sources/datacite.py:208-213` and `openaire.py:133-138`.** The raw user query goes straight into the registry's query language. DataCite uses Elasticsearch `query_string`, so `:` and `/` are field and regex syntax. Live, `search "ICU/ward mortality: adults" --source datacite` returned `datacite=0` with no error, and `_relaxed_query` returns None for it, so no second try is made. I did not compare it with a sanitised query, to stay within the request budget. **Fix:** build the query from `_tokens()` (escape reserved characters) for both requests.

**X2. minor (suspected): `common.http_request` `max_bytes=4000000`.** `get_json` silently truncates larger bodies and then reports "invalid JSON". The PhysioNet catalogue is 1.4 MB today (760 entries), so it is fine now, but `physionet._fetch_all` will break without a clear message if the catalogue grows past the cap. **Fix:** raise a clear `FetchError("response larger than N bytes")` when the read hits `max_bytes`.

**X3. minor (suspected): `verify._bounded_lookup`.** Abandoned helper threads keep their locks until the adapter's own 64 s worst case ends, and `ctx.adapter_down` then skips that registry for the rest of the run. This is by design, but combined with S8 one slow registry turns every later item on that host into "could not check" for up to about a minute. Seen only by reading the code; `test_slow_adapter_is_abandoned_within_its_budget` covers the happy path.

---

## SPEC compliance (checked, no violation unless listed above)

- **Standard library and Python 3.8:** every module parses with `ast.parse(..., feature_version=(3, 8))` and imports only stdlib modules. The CLI runs under `/usr/bin/python3` (3.9). Every file has `from __future__ import annotations` except the empty `scoutlib/__init__.py`.
- **HTTP routing:** no `urllib.request`, `http.client`, `socket` or `ProxyHandler` use outside `common.py`. All HTTP goes through `common.http_request` / `get_json` / `get_text`.
- **Requests per search:** at most 3 per `search()` (zenodo 3, huggingface 3, datacite 2, openaire 2, physionet 1 or 0 with the cache). Retries inside `http_request` can add more.
- **No personal data sent:** the User-Agent is generic and no `mailto` is sent. The only leak found is S12, an optional key echoed into output.
- **No hard-coded dataset names:** no dataset names or lists in the skill directory (searched for common clinical, ML and earth-observation dataset names across `.py`, `.md`, `.html` and `.json`). Registry names only.
- **Errors not swallowed:** errors are reported, with a few exceptions: `physionet._write_disk_cache` (documented), `verify._csl` (best-effort enrichment) and `verify._adapter_for`, which swallows adapter exceptions and returns None with no note. That last one is minor.
- **Template safety:** the template is sound against injection. Hostile titles, questions, reasons and `javascript:` URLs were tested in `shortlist.json`: the JSON block escapes `< > &`, the fallback list is `html.escape`d, `javascript:` links come out as plain text, the CSP allows only the hash of the page script, and the DOM is built from text nodes.

## CLI behaviour (item 4)

- **Help:** `--help` works for all 8 subcommands; `add` and `lookup` arguments have no help text.
- **Flow:**
  - `search` twice into one `--out`: 21 new and 4 merged, then 3 new and 3 "merged" (which were self re-finds, M3).
  - `add`, `show`, `show --pick`: all ran.
  - `verify --pick 1,2,7,13,14,17,20,25,26 --out`: **8.1 s** for 9 items. A 10-item judgement batch took 8.5 s; a 3-item PhysioNet batch, under 0.1 s from the cache.
  - `lookup` with a URL, a bare DOI and a `doi:` DOI; `papers --query` (1.3 s); `papers --doi`; `render`. All completed.
- **Problems found in the flow:** a raw traceback from `lookup` (S11), misleading "no record" for a Crossref DOI (M4), notes hidden by the digest (S10), and self-merges counted as duplicates (M3).
- **Verifier judgement on my own inputs** (`judge.json`, live):
  - Correct on 9 of 10: real UCI page verified; UCI home page and Zenodo home page rejected; invented PhysioNet slug and invented Zenodo id → 404; invented Hub repo → not_found (soft 404 under HTTP 401); invented DOI `10.13026/zz9q-k4x1` → "not registered"; real Zenodo DOI verified with the registry tier; a Crossref paper DOI verified with a "registered as journal-article, may be the paper" note.
  - Wrong on 1: the real UCI page with the wrong title came back "could not check" (M5).
  - Separately, invented names on real PhysioNet URLs were caught 2 times out of 3 (B3).

## Tests (item 5)

- **Result:** `/opt/anaconda3/bin/python3 -m pytest tests -q` gives **195 passed, 7 skipped** (the live tests) in 2.1 s.
- **Quality:** the verify and render tests mostly check behaviour. They use a fake web layer with realistic statuses and pages, recorded HTML, headless-JavaScript checks of the page, and CSP and escaping tests. The adapter tests are largely field-mapping tests against recorded fixtures. Some tests pin the behaviour flagged above and will need changing with the fixes:
  - `test_physionet.py::test_lookup_old_version_url_notes_it` (S1);
  - `test_verify.py::test_never_overwrite_a_registry_tier` (S2);
  - `test_huggingface.py::test_access_mapping` (`gated=False` → `open`, B2).
- **Most valuable missing tests:**
  1. A `tests/test_common.py`:
     - `make_record` does not share `extra` or `usage` between records (B1);
     - a `normalise_licence` table that includes space-separated CC forms, "MIT" inside custom terms and "non-commercial" riders (S3);
     - `dedupe` does not merge different DOIs with the same title, and does merge concept and version DOIs (S4);
     - `http_request` does not retry InvalidURL (S9), and its timeout and retry totals are bounded (S8);
     - `_throttle` under threads (M1).
  2. One assertion added to the existing `test_minimal_inputs_become_manual_records`: `"claimed_access" not in first["extra"]`. It fails today.
  3. A Hub fixture for a loader-only repo (only `*.py` siblings, no `format:` tag) that must not be `open` (B2).
  4. Invented title on a real registry URL whose description shares the words: the record must not stay verified under the invented name (B3).
  5. CLI tests for `search` (accumulation, self-merge, per-source deadline), `add` without `--title`, `lookup` error paths, and the digest printing access hints. Today only `render` is tested through the CLI.
  6. A template test that a verified record with `problems` shows them (S2).
