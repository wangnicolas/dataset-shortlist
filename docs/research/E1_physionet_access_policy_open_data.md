# E1 — PhysioNet: programmatic catalogue access, LLM policy, open ICU data, reference results
Fetched 2026-11-11 (API snapshot: server `Date: Wed, 11 Nov 2026 13:51:29 GMT`). 33 requests to physionet.org in total. Everything else came from GitHub, arXiv, NCBI/Europe PMC and the AWS S3 mirror. Local tool runs (counts) used the 1.4 MB API JSON and label files ≤ 140 KB, saved under `dl_physionet/`. **UNVERIFIED** marks a claim not confirmed in this session.

## 1. Programmatic access to the catalogue
**Working endpoint (tested, anonymous, HTTP 200, `application/json`):** `https://physionet.org/api/v1/project/published/`. It returns one JSON array of **760 published versions** (1,368,019 bytes) with **no pagination**. The official client agrees: "The API returns all projects in a single response (no pagination)" (https://github.com/MIT-LCP/physionet/blob/main/physionet/api/endpoints.py). The server docstring says "paginated", but the source configures no pagination class (https://github.com/MIT-LCP/physionet-build/blob/dev/physionet-django/export/views.py).

**Fields in every list record:** `public_project_uuid, slug, version, core_doi, version_doi, is_latest_version, short_description, publish_date, title, abstract` (HTML), `license{name}, dua{name}` (null for open data), `main_storage_size, compressed_storage_size` (bytes), `resource_type, access_policy, topics[], source_url`. The detail endpoint adds `project_home_page, publish_datetime, doi, funding[]`. Caveat: the size fields are unreliable. challenge-2012 has `main_storage_size` = 0 and challenge-2019 has 335,112 bytes, although the 2019 `training/` folder holds the 40,336 patient files.

**Counts (local run on the snapshot):** 563 unique projects (`is_latest_version`), 760 versions.

| Latest version only (n=563) | Open | Credentialed | Restricted | Contributor Review | Total |
|---|---|---|---|---|---|
| Database | 242 | 155 | 48 | 13 | 458 |
| Software | 56 | 1 | 0 | 0 | 57 |
| Challenge | 26 | 9 | 1 | 0 | 36 |
| Model | 0 | 12 | 0 | 0 | 12 |
| **Total** | **324** | **177** | **49** | **13** | 563 |

**Caveat on "Open":** 7 of the 324 latest "Open" records still carry `dua` = "PhysioNet Contributor Review Health Data Use Agreement 1.5.0" and the Contributor Review licence: mental-fnirs, sleep-dep-hemo-cog, cardioresp-response-orthostat, eda-rest-sedation, propofol-anesthesia-dynamics, auditory-eeg and treadmill-exercise-cardioresp. Only **317** latest records have `dua` = null. A scout should therefore treat a project as open only when `access_policy == "Open"` **and** `dua == null`. Counting all 760 versions gives Open 395, Credentialed 263, Restricted 79 and Contributor Review 23 by access policy, and Database 628, Software 63, Challenge 54 and Model 15 by type. Publish dates run from 1999-08-03 to 2026-11-02. Cross-check: the HTML index `https://physionet.org/content/` shows 10 per page and its last page (`?page=50`) is full, so it lists about 500 entries, against 563 in the API. **Cause of the gap UNVERIFIED.**

**Other routes in the source** (`export/urls.py` on the dev branch, https://github.com/MIT-LCP/physionet-build/blob/dev/physionet-django/export/urls.py):

| Route | Status in this session |
|---|---|
| `/api/v1/project/published/search/?search_term=…&resource_type=…` | tested 200; `sepsis`+`challenge` returned 1 project (challenge-2019) |
| `/api/v1/project/published/<slug>/<version>/` | tested 200 (challenge-2012) |
| `/api/v1/projects/<slug>/versions/<version>/access/` | tested 200 (challenge-2019: `"status":"ready","can_download":true`) |
| `/api/v1/projects/published/`, `/api/v1/projects/search/`, `/api/v1/projects/<slug>/versions/`, `/api/v1/projects/<slug>/versions/<v>/` | in source, not tested |
| `/api/v1/projects/published/<slug>/<v>/sha256sums/` | in source; needs authentication |
| `/rest/database-list/` (legacy) | **404** |
| `/sitemap.xml` | **404** (no sitemap) |
| `/about/database/` | 200 HTML (173,664 bytes); not inspected |
| `/content/?topic=…&orderby=relevance-desc&types=0..3` | HTML search; tested 200 (`topic=sepsis` gave "7 results"); type codes 0=Data, 1=Software, 2=Challenge, 3=Model |
| `/rest/1/` (named only by a third-party listing) | not tested, **UNVERIFIED** |

**robots.txt** (https://physionet.org/robots.txt) is exactly 22 bytes: `User-Agent: *\Allow: /`. The `\` is a literal backslash, not a newline; the source has `HttpResponse("User-Agent: *\\Allow: /")` (`physionet/urls.py`). So the file is malformed but permissive: no Disallow rule, no Crawl-delay, no Sitemap.

**Rate limits and terms:** the dev-branch source sets `StandardAnonRateThrottle rate = '20/hour'` and `StandardRateThrottle rate = '100/hour'` (authenticated) on every API view (export/views.py, linked above). I did not observe these limits in production: 4 anonymous API calls drew no 429 and no rate-limit headers. The docstrings say "Session or Basic authentication required", yet anonymous GETs returned 200. I found no website terms of use for automated access (checked robots.txt, FAQ, physionet-build source, web search), so this is an **absence, UNVERIFIED**. The FAQ (https://physionet.org/about/faqs/, undated) says: "PhysioNet supports terabytes of downloads per day, for free. In order to support this volume, bandwidth is restricted for individual downloads." It points to AWS Open Data for large datasets.

**Copy-pasteable requests (tested ones are marked ✓):**
```bash
UA="Mozilla/5.0 (compatible; dataset-scout/0.1)"   # generic UA
curl -sS -A "$UA" https://physionet.org/api/v1/project/published/ -o published.json          # ✓ full catalogue, one array
jq '[.[]|select(.is_latest_version)]|group_by(.access_policy)|map({(.[0].access_policy):length})|add' published.json
jq -r '.[]|select(.is_latest_version and .access_policy=="Open" and .dua==null)|[.slug,.version,.resource_type,.license.name]|@tsv' published.json
curl -sS -A "$UA" "https://physionet.org/api/v1/project/published/search/?search_term=sepsis&resource_type=challenge"  # ✓
curl -sS -A "$UA" https://physionet.org/api/v1/project/published/challenge-2012/1.0.0/        # ✓ detail (+funding)
curl -sS -A "$UA" https://physionet.org/api/v1/projects/challenge-2019/versions/1.0.0/access/ # ✓ download readiness
curl -sS -A "$UA" https://physionet.org/api/v1/projects/mimic-iv-demo/versions/              # per source, untested
pip install physionet && physionet search "sepsis" --json      # official client (README: github.com/MIT-LCP/physionet), untested
```
Cache the 1.4 MB list once and filter it locally. If the 20/hour anonymous limit in the source applies in production, querying project by project is a poor fit.

## 2. Policy on LLMs and online AI services
**Current post: "Use of MIMIC Data with Large Language Models and Online Services", dated Sept. 24, 2025** (https://physionet.org/news/post/llm-responsible-use/). Verbatim quotes:
- "The PhysioNet Credentialed Data Use Agreement explicitly prohibits sharing access to the data with third parties, including sending it through APIs or using it on online platforms."
- "Zero Data Retention: MIMIC data must not be stored or retained by third-party LLM services."
- "Strongly Recommended: Use locally deployed LLMs to maintain full control over the data."
- "If Using Cloud Services or APIs: Verify that the service’s settings ensure zero data retention, no use of data for model training, and no human review."
- "Even when services claim "zero data retention," their requirements may be insufficient due to internal processing, logging, or caching practices."
- "If a service’s data handling practices are unclear or cannot be fully verified, do not use the service."
- "Important Disclaimer: PhysioNet cannot verify the data practices of external services and does not endorse or recommend specific platforms."

The scope stated in the post covers "credentialed and restricted data … including MIMIC-III, MIMIC-IV, MIMIC-CXR, and their derivatives".

**FAQ (https://physionet.org/about/faqs/, undated).** Q3 answers: "Current policy requires adherence to a zero data retention policy. Local LLM models can be used without restrictions, but there are limitations when using API services." Q3 links only to the 2025 post. Q2 answers: "For credentialed access data such as MIMIC and eICU, each user must obtain individual access rights. Sharing data within teams or classes is not permitted."

**Older post, still online: "Responsible use of MIMIC data with online services like GPT", displayed date April 18, 2023** (https://physionet.org/news/post/gpt-responsible-use/). It says: "The PhysioNet Credentialed Data Use Agreement explicitly prohibits sharing access to the data with third parties, including sending it through APIs provided by companies like OpenAI, or using it in online platforms like ChatGPT." It then names four routes:
- "Azure OpenAI service. You'll need to opt out of human review of the data via this form."
- "Amazon Bedrock. … After creating a copy of a base foundation model for exclusive use, data is not shared back to the base model for training."
- "Google's Gemini via Vertex AI on Google Cloud Platform. Gemini doesn't use your prompts or its responses as data to train its models." Under the Gemini Trusted Tester Program, users must get data-sharing opt-outs.
- "Anthropic Claude. Claude does not use your prompts or its responses as data to train its models by default, and routine human review of data is not performed."

The post must have been edited after its displayed date: Google's announcement of Gemini on Vertex AI is dated December 14, 2023 (https://cloud.google.com/blog/products/ai-machine-learning/gemini-support-on-vertex-ai). The post's **last-updated date is UNVERIFIED**. Neither post refers to the other, and nothing on the site says the 2023 post was superseded. Whether its named-platform list is still in force is **UNVERIFIED**. The 2025 post endorses no platform; read together, the posts make platform names insufficient by themselves, and the 2025 conditions (verified zero retention, no training, no human review) apply.

**Summary.** The 2025 post first states that the DUA prohibits sending the data through APIs or using it on online platforms. Its "Key Requirements" are zero data retention and the researcher's own responsibility for compliance. Under "Recommendations" it strongly recommends local LLMs, and for "If Using Cloud Services or APIs" it requires verified zero retention, no training use and no human review, with "do not use the service" if any of this is unclear. The FAQ says local LLMs "can be used without restrictions". Sharing within teams or classes is not permitted. **My reading of the stated scope** (credentialed and restricted data) is that searching public catalogue metadata (Part 1) and working with open-access datasets fall outside these rules; open datasets carry their own licences (ODbL, ODC-By, CC BY, etc.). PhysioNet does not say this explicitly.

**mimic.mit.edu:** I found no LLM statement on `/docs/faq/`, `/docs/faq/data.html` or `/docs/faq/how-to-get-access.html` (fetched today). This is an absence, **UNVERIFIED** for the rest of the site.

**PhysioNet Credentialed Health Data Use Agreement 1.5.0** (as shown for MIMIC-IV v3.1, https://physionet.org/content/mimiciv/view-dua/3.1/). The clauses on sharing and security:
- "I will not share access to PhysioNet restricted data with anyone else."
- "I will exercise all reasonable and prudent care to maintain the physical and electronic security of PhysioNet restricted data."
- "I have requested access to PhysioNet restricted data for the sole purpose of lawful use in scientific research, and I will use my privilege of access, if it is granted, for this purpose and no other."

The companion **PhysioNet Credentialed Health Data License 1.5.0** (https://physionet.org/content/mimiciv/view-license/3.1/; the page shows "Copyright (c) 2026 MIT Laboratory for Computational Physiology") says: "The LICENSEE will not share access to PhysioNet restricted data with anyone else." Neither text contains the words "third party", "API" or "LLM". The ban on API and online-platform use is **PhysioNet's interpretation in its news posts** of the "anyone else" clause. In the API catalogue, 173 latest-version projects carry `dua.name` = "PhysioNet Credentialed Health Data Use Agreement 1.5.0". Four more Credentialed projects use other agreements: medical-ai-research-foundation, inspire (Korea Credentialed Health Data Agreement), b2ai-voice and b2ai-voice-pediatric. The safe rule for a scout is "any non-null `dua` means gated: keep the data away from online LLMs" rather than matching one DUA name.

## 3. Open-access clinical datasets for a public demo
Every page below shows "Open Access" with the access policy "Anyone can access the files, as long as they conform to the terms of the specified license." The file pattern is `https://physionet.org/files/<slug>/<version>/<path>`. The demo files return 200 directly. The challenge files return **302 → `https://physionet-open.s3.amazonaws.com/<slug>/<version>/<path>`**, so use `curl -L`. Cohort counts marked (run) are my local counts on the small label files.

| Dataset (page) | Version · published · licence | Size | Reachability check | Labels; all subsets public? |
|---|---|---|---|---|
| [Challenge 2012](https://physionet.org/content/challenge-2012/1.0.0/) | 1.0.0 · Jan. 20, 2012 · Open Data Commons Attribution License v1.0 · no DOI in API | 12,000 ICU stays ≥48 h, 3 sets × 4,000; ZIP 1.8 GB; `set-{a,b,c}.tar.gz` ≈6.3 MB each | S3 HEAD 200: set-a 6,632,372 B, set-b 6,652,690 B, set-c 6,600,293 B; `Outcomes-{a,b,c}.txt` GET 200 (≈79 KB each) | RecordID, SAPS-I, SOFA, Length_of_stay, Survival, In-hospital_death. Deaths (run): A 554/4,000 (13.9%), B 568 (14.2%), C 585 (14.6%); RecordIDs disjoint (run). **Yes, all three are downloadable today**, but the page still says outcomes "are withheld for the test set records". Release date **UNVERIFIED**; a GitHub split script committed 2020-01-28 already reads Outcomes-b/-c |
| [Challenge 2019](https://physionet.org/content/challenge-2019/1.0.0/) | 1.0.0 · Aug. 5, 2019 · Creative Commons Attribution 4.0 International Public License · 10.13026/v64v-d857 | Training set A 20,336 + set B 20,000 = 40,336 patients, one hourly `.psv` per patient; page shows "Total uncompressed size: 327.3 KB" (excludes `training/`) and links a "42 MB" bundle via archive.physionet.org (not checked) | `…/training/training_setA/p000001.psv` 302→S3 200 (9,062 B); `training_setB/p100001.psv` 200 | Hourly `SepsisLabel` (1 if t ≥ t_sepsis − 6), 41 columns (run on 2 files). **No.** The hidden test set (24,819 patients from systems A, B, C) is not in today's file listing: `training/` holds only `training_setA/` and `training_setB/`; `hackathon/`, `sources/` and `papers/` were not inspected |
| [MIMIC-IV Clinical Database Demo](https://physionet.org/content/mimic-iv-demo/2.2/) | 2.2 · Jan. 31, 2023 · Open Data Commons Open Database License v1.0 · 10.13026/dp1f-ex47 | 100 patients; (run) 275 admissions, 140 ICU stays; "Total uncompressed size: 15.5 MB", ZIP 15.4 MB | `icu/icustays.csv.gz` 200 (5,667 B); `hosp/admissions.csv.gz` 200 | Derive labels from tables, e.g. `hospital_expire_flag` = 1 for 15 admissions (run). The page says the demo "excludes free-text clinical notes". No train/test split; the whole demo is public |
| [eICU-CRD Demo](https://physionet.org/content/eicu-crd-demo/2.0.1/) | 2.0.1 · May 6, 2021 · Open Data Commons Open Database License v1.0 · 10.13026/4mxk-na84 | Page: "over 2,500 unit stays selected from 20 of the larger hospitals". (run) 2,520 unit stays, 1,841 `uniquepid`, **186 distinct `hospitalid`**, which contradicts "20". 130.6 MB uncompressed, ZIP 130.4 MB | `patient.csv.gz` 200 (136,791 B) | `hospitaldischargestatus`: Expired 212, Alive 2,280, blank 28; `unitdischargestatus` Expired 126 (run); APACHE result table present. Whole demo public |
| [MIMIC-III Clinical Database Demo](https://physionet.org/content/mimiciii-demo/1.4/) | 1.4 · April 24, 2019 · Open Data Commons Open Database License v1.0 · 10.13026/C2HM2Q | 100 patients; (run) 129 admissions, 136 ICU stays; 103.0 MB uncompressed, ZIP 13.4 MB | `ICUSTAYS.csv` 200 (13,495 B); `ADMISSIONS.csv` 200 | `hospital_expire_flag` = 1 for 40 admissions (run). **Biased sample:** patients "were selected randomly from the subset of patients in the dataset who eventually die"; NOTEEVENTS rows removed |
| [I-CARE](https://physionet.org/content/i-care/2.1/) | 2.1 · Dec. 14, 2023 (page; API says 2023-12-15) · Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License · 10.13026/m33r-bj81 | 607 patients, EEG/ECG + clinical; API size ≈1.69 TB | page 200 shows "Open Access"; files not checked | CPC 1–5 / good vs poor outcome. **No:** "the remaining 413 patients" are kept as hidden validation and test sets |

Other open-access candidates come from API metadata only; their pages and files were not checked:
- `mimic2-iaccd` 1.0: 1,776 patients, summary rows with mortality outcomes, not time-stamped.
- `challenge-2009` 1.0.0: acute hypotensive episodes.
- MIMIC-IV demo derivatives: `mimic-iv-demo-omop` 0.9, `mimic-iv-demo-meds` 0.0.1, `mimic-iv-fhir-demo` 2.1.0, `mimic-iv-ed-demo` 2.2.
- `vtac` 1.1: labelled ICU VT alarm waveforms.

None of the six other projects returned by the HTML `topic=sepsis` search is open; all are Credentialed, Restricted or Contributor Review (API).

## 4. Human reference results: Challenge 2012 and 2019
**Challenge 2012** (page above; Silva et al., Comput Cardiol 2012;39:245–248, https://pmc.ncbi.nlm.nih.gov/articles/PMC3965265/, read via NCBI efetch).

Official metrics:
- Event 1 = min(Se, +P), the lower of sensitivity and positive predictivity.
- Event 2 = range-normalized Hosmer–Lemeshow H/D; lower is better.
- Official scorer: `score.c`. The page notes that `lemeshow.m` may differ "due to differences in rounding".

Official results, all on set C:
- Event 1: top **0.5353** (Johnson et al.), then 0.5345 (Citi & Barbieri). The page says "The top 10 (of 28) participants".
- Event 2: top **17.88** (Citi & Barbieri). The page says "The top 10 (of 23) participants".
- SAPS-I baseline (m-code): 0.3125 and 68.58.
- Silva 2012: "A total of 37 different teams across the world competed … submitting around 200 different entries". The two counts are at different granularity and are not reconciled.
- The challenge did not use AUROC. Silva says Event 1 was meant to make competitors "optimize the Precision-Recall (PR) curve of their classifiers, instead of the usual receiver operating curve (ROC)".

**Challenge 2019** (Reyna et al., Critical Care Medicine 48(2):210–217; the PhysioNet page gives the year as 2019; accepted manuscript at https://physionet-open.s3.amazonaws.com/challenge-2019/1.0.0/physionet_challenge_2019_ccm_manuscript.pdf, linked from the page).

The official metric is the normalized clinical utility U_norm: an optimal classifier scores 1 and one with no positive predictions scores 0. It rewards predictions from 12 h before to 3 h after t_sepsis.

Official results:
- "A total of 104 teams from academia and industry submitted a total of 853 entries during the official phase of the Challenge; of these, 88 distinct teams with a total of 430 entries were able to be scored."
- Table 3, full hidden test set:

| Entry | Full test set | System A | System B | System C |
|---|---|---|---|---|
| Rank 1 (Morrill et al.) | **0.360** | 0.433 | 0.434 | −0.123 |
| Rank 2 (Du, Sadr, de Chazal) | 0.345 | 0.409 | 0.396 | −0.042 |
| Rank 3 (Zabihi, Kiranyaz, Gabbouj) | 0.339 | 0.422 | 0.395 | −0.146 |
| Rank 4 (Li et al.) | 0.337 | 0.420 | 0.401 | −0.156 |
| Rank 5 (Singh et al.) | 0.337 | 0.401 | 0.407 | −0.094 |
| Best unofficial entry (Yang et al.) | 0.364 | 0.430 | 0.422 | −0.048 |

Data split: "Data and labels for 40,336 patients from hospital systems A and B were posted publicly for download and data and labels for 24,819 patients from hospital systems A, B, and C were sequestered as hidden test sets."

**Later papers. Read the label and split column before comparing any numbers.**

| Paper (PDF fetched) | Data · split | Label | Results (AUROC / AUPRC) |
|---|---|---|---|
| GRU-D, Che et al., Sci Rep 2018;8:6085 ([PMC5904216](https://pmc.ncbi.nlm.nih.gov/articles/PMC5904216/), read via NCBI efetch; Europe PMC citedBy 476) | Set A only, 5-fold CV. The paper gives 554 positives; set A = 4,000 records per the challenge page. Quote: "We used Training Set A subset in our experiments since outcomes (such as in-hospital mortality labels) are publicly available only for this subset." | in-hospital death | AUROC: GRU-D **0.8424 ± 0.012**. Classical baselines: SVM-Simple 0.8277 ± 0.012, RF-Forward 0.8219 ± 0.017, LR-Simple 0.7625 ± 0.004 |
| mTAND, Shukla & Marlin, ICLR 2021 ([arXiv 2101.10318](https://arxiv.org/abs/2101.10318)) | Set A, "4000 labeled instances and 4000 unlabeled instances"; random 80/20 split, 20% of train used for validation, 5 seeds | in-hospital death (13.8% positive) | AUROC: mTAND-Full **0.858 ± 0.004**, GRU-D 0.818 ± 0.008, SeFT 0.795 ± 0.015 |
| SeFT, Horn et al., ICML 2020 ([arXiv 1909.12064](https://arxiv.org/abs/1909.12064)) | A+B+C pooled, own stratified 80/20 split. The SeFT code README links to `ExpectationMax/medical_ts_datasets`, whose split script ([GitHub](https://github.com/ExpectationMax/medical_ts_datasets/blob/master/scripts/split_physionet2012_train_val_test.py); the same file exists in the `BorgwardtLab/` fork) produces test 2,400, val 1,920, train 7,680. The main text says "8,000 … 4,000", which is inconsistent with the script | in-hospital death | P12: GRU-D 86.3 ± 0.3 / 53.7 ± 0.9; Transformer 86.3 ± 0.8 / 52.8 ± 2.2; SeFT-Attn 85.1 ± 0.4 / 52.4 ± 1.1. P-Sepsis (own split of the 2019 training data, hourly): Transformer AUROC 97.3 but 65.8 with future masked, which the authors attribute to leakage; GRU-Simple 78.1 / 6.10, U_norm 26.9 |
| Raindrop, Zhang et al., ICLR 2022 ([arXiv 2110.05357 v1 & v2](https://arxiv.org/abs/2110.05357)) | "P12" = 11,988 patients (12 removed), random 80/10/10 split, 5 fixed splits. "P19" = 38,803 patients | **P12 label = LOS > 3 days** (~93% positive, both versions). P19 = per-patient sepsis label (~4% positive), not the hourly utility task | P12 (LOS): Raindrop 72.1 ± 1.3 / 97.0 ± 0.4. P19: Raindrop **87.0 ± 2.3 / 51.8 ± 5.5**, GRU-D 83.9 ± 1.7 / 46.9 ± 2.1 |
| ViTST, Li et al., NeurIPS 2023 ([arXiv 2303.12799](https://arxiv.org/abs/2303.12799)) | "We used the processed data provided by Raindrop" and the same 5 splits | P12 = "survival during hospitalization" | P12: ViTST **85.1 ± 0.8 / 51.1 ± 4.1**; Raindrop 82.8 ± 1.7 / 44.0 ± 3.0 (as re-reported here; not in Raindrop arXiv v1 or v2; OpenReview PDF returned 403, **UNVERIFIED**); GRU-D 81.9 ± 2.1 / 46.1 ± 4.7. P19: ViTST 89.2 ± 2.0 / 53.1 ± 3.4 |

Citation counts were checked only for GRU-D; the other papers are cited by venue. I found no paper dedicated to strong classical baselines (e.g. gradient boosting) on P12 or P19 in this session (**UNVERIFIED**). GRU-D's own LR/SVM/RF table is the classical reference above.

**Can an evaluation be exactly comparable to the official results?**
- **2012: yes, on one assumption.** Set C data and labels are now public. You can train on A (as the 2012 entrants did; B came without labels) and score C once with the official `score.c`, which gives numbers comparable to the 0.5353 / 17.88 leaderboard.

  The assumption: nothing fetched here proves that the posted `set-c.tar.gz` and `Outcomes-c.txt` are exactly the set the leaderboard was scored on (**UNVERIFIED**). To test it, run the SAPS-I sample entry on set C and score it with `score.c`; it should reproduce the published baseline of 0.3125 / 68.58 (m-code) or 0.3097 / 35.21 (C).

  Caveats:
  - C is no longer sequestered, so nothing prevents tuning on it.
  - The official metrics are not AUROC.
  - Entrants had at most 5 + 5 entries, scored on B, before a single run on C.
  - None of the ML papers above reports results on set C: they use set A with CV or 80/20 splits, or a pooled random split. Their AUROCs are therefore comparable neither to the leaderboard nor to each other.
  - "P12" means LOS > 3 days in Raindrop and mortality in ViTST and SeFT.
- **2019: no.** No held-out set with public labels exists, and hospital system C has no public data at all, so the official utility (0.360, and the negative system-C scores) cannot be reproduced. Every literature number on the 2019 data comes from authors' own splits of the 40,336 training patients, often with per-patient labels, and is not comparable to the challenge results.

---
*Housekeeping:* downloaded pages, JSON and small label files (all ≤ 1.9 MB; no executable content run) are in `dl_physionet/`. Five small helper scripts I wrote (HTML-to-text, counts) are in `research/scripts/`, outside that folder, so that data and code stay apart.
