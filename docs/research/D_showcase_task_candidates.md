# D. Showcase task candidates: agent (unattended) vs documented human results

Research date 2026-11-11. Read-only web research. Labels used below:
**[V]** = quoted from a page or official file fetched in this session (URL given);
**[computed]** = I computed it from an official file fetched in this session;
**[inference]** = derived by reasoning from [V] numbers;
**UNVERIFIED** = not confirmed in this session.
Background knowledge that I did not check today is tagged UNVERIFIED.
Every download URL marked "200" answered HTTP 200, directly or after a 302, to `curl -sI -L` today.

**Downloads.** I downloaded no dataset file larger than 5 MB.
- Saved under `dl_candidates/` and treated as untrusted data:
  - Data files: KDD98 `valtargt.txt` and `cup98doc.txt`; M4 `M4-info.csv`, Weekly train and test, and `Evaluation and Ranks.xlsx`.
  - FluSight files: README, git-tree JSON, and the first 2.5 MB of a report HTML.
  - Web pages: PhysioNet, KDnuggets and PMC HTML.
  - Tourism PDFs and text.
  - Higgs paper text.
- Disclosure: WebFetch auto-saved the 6.1 MB Higgs paper PDF (a paper, not data) in the session's tool-results directory, outside `dl_candidates/`.

## 1. Candidate table

| # | Task (domain) | Data size / download | Licence | Metric & locked test | Human reference (best / median / baseline) | Test labels public? | Contamination |
|---|---|---|---|---|---|---|---|
| C1 | PhysioNet/CinC Challenge 2012, in-hospital mortality (clinical) | 3 × 4,000 ICU stays; ~6.3 MB tar.gz per set; 200 | ODC-BY 1.0 [V] | Event 1 = min(Se, +P) on set C; train on set A | 0.5353 / median not published (top 10 of 28 only) / SAPS-I 0.3125 [V] | Yes: Outcomes-c.txt is downloadable (the page text still says withheld) | Moderate |
| C2 | Higgs Boson ML Challenge 2014 (tabular, physics) | 818,238 × 35; 65.6 MB gz; 200 | CC0 1.0 [V] | AMS (b_reg = 10) on KaggleSet = v (450K events); train on t (250K) | 3.80581 / ≈3.40–3.50 at rank ≈893 of 1,785 [inference] / MultiBoost 3.40488, TMVA 3.19956 [V] | Yes: labels and weights for all events | **High** |
| C3 | KDD Cup 1998 direct-mail profit (tabular) | 95,412 × 481 learn; 96,367 × 479 validation; ~36 MB zip each; 200 | CC BY 4.0 on the UCI page [V raw], plus legacy notification terms (§C3) | Net profit on the validation file, one returned file | $14,712 / $10,720 (11th of 21) [computed from V] / mail-all $10,560 [V; reproduced] | Yes: valtargt.txt | Moderate (UNVERIFIED judgement) |
| C4 | M4 Weekly (alternative: Hourly) (forecasting) | Weekly 359 series, h = 13 (4.0 MB train); Hourly 414 series, h = 48; 200 | Original UNVERIFIED (repo has no licence); Monash mirror CC BY 4.0 [V] | OWA (rel. sMAPE + rel. MASE vs Naive2) on the official test file | Weekly: 0.739 / 0.930 [computed] / Theta 0.971, Naive2 1.000. Hourly: 0.410 / 0.794 [computed] / sNaive 0.627 [V] | Yes | **High** |
| C5 | CDC FluSight 2025–26 retrospective, or 2026–27 prospective (public-health forecasting) | 52 jurisdictions + US, horizons 0–3, quantiles; vintage target file 95 MB; 200 | Repo MIT; per-model CC-BY-4.0 (checked 3); CDC asks for attribution contact [V] | WIS / relative WIS vs FluSight-baseline, forecasting from as_of data only | 2025–26: no published table found, so **recompute from the submitted files**: 68 model directories, of which 56 are not hub-generated, from 35 distinct team prefixes [computed]. Prior seasons [V raw]: best rel. WIS 0.74 (2021–22), 0.61 (2022–23); baseline 1.00 | Yes, retrospective; prospective truth arrives weekly until 2027-05 | **Lowest** |
| C6 | Tourism Forecasting Competition 2010, monthly (forecasting) | 366 monthly, 427 quarterly, 518 yearly series; 200 KB zip; 200 | CC BY 4.0 (Zenodo mirror), GPL-3 (CRAN Tcomp) [V] | MASE averaged over h = 1–24 (monthly) | Organiser-run expert methods: ARIMA 1.38, ForePro 1.40, ETS 1.49, SNaive 1.54 [V]; Kaggle teams UNVERIFIED | Likely; train/test split in the mirror UNVERIFIED | Moderate (UNVERIFIED) |
| C7 | TabArena-v0.1, one dataset, first split only (tabular, expert-tuned) | 51 datasets, 9–30 splits each; OpenML API works without a key [V] | Code Apache-2.0 [V]; per-dataset licences UNVERIFIED | Task metric on split 0 | Per-dataset numbers "not hosted"; they must be generated with TabArena scripts, so UNVERIFIED | Yes (OpenML) | Moderate–high (UNVERIFIED) |

Screened out (with evidence):
- **PhysioNet/CinC 2019 sepsis.** The test set is hidden ("the patients in the hidden test set"), so its scores cannot be replicated ([V] https://physionet.org/content/challenge-2019/1.0.0/).
- **Data Mining Cup archive.** `www.data-mining-cup.com/reviews/dmc-2019/` now 301-redirects to an unrelated gambling site.
- **BeyondArena** (HF `TabArena/BeyondArena`, created 2026-05-26, not gated). Its licence is "copyright-at-original-authors", which fails the licence constraint.
- **Kaggle, DrivenData and Zindi originals.** Login is required (UNVERIFIED background knowledge). The Kaggle Higgs leaderboard page rendered no data [V].
- **M5.** Not examined.

## 2. Per-candidate protocol notes

### C1 PhysioNet/CinC Challenge 2012: https://physionet.org/content/challenge-2012/1.0.0/
- **Download (200).** `https://physionet.org/files/challenge-2012/1.0.0/{set-a.tar.gz (6,632,372 B), set-c.tar.gz (6,600,293 B), Outcomes-a.txt (79,219 B), Outcomes-c.txt (79,191 B)}`. Set B and Outcomes-b.txt also exist; a ranged GET on Outcomes-b worked.
- **Data.** 12,000 adult ICU stays (stays under 48 h excluded), split into A, B and C of 4,000 each. "Up to 42 variables were recorded at least once during the first 48 hours… Six of these variables are general descriptors" [V].
- **Metric** [V, "Challenge Scoring"]. Event 1 = min(Se, +P), using a binary prediction per record. Event 2 = range-normalised Hosmer–Lemeshow H/D (lower is better).
- **Human protocol** [V]:
  - Only set A outcomes were available to participants.
  - "You may submit up to five Phase 1 entries" and "up to five Phase 2 entries". Each entry received set B scores (scores only, no labels).
  - One selected entry was then scored on set C: "Scores obtained in the set C evaluations determined the final ranks".
  - Entries ran per record and "may not store information for use in later runs".
- **Replication.**
  - Train on A only, fix the threshold on A, then predict C record by record. No transductive use of C, such as quantile thresholds computed on C.
  - Giving the agent B labels would hand it more than humans had. Either forbid that or disclose it.
  - Every specified element is reproducible: train on A, one shot on C, per-record inference. The B-score feedback loop is not reproduced, which makes the agent's run stricter than the humans'.
- **Human reference** [V, "Challenge Results" section, Event 1 table]:
  - 1. Johnson et al. 0.5353
  - 2. Citi & Barbieri 0.5345
  - 3. Vairavan et al. 0.5009
  - 10. Bera & Nayak 0.4513
  - Baselines: "SAPS-I (in m-code) 0.3125"; "86% randomly predicted to survive 0.1386"
  - "The top 10 (of 28) participants in event 1 are listed above." No median is published.
  - Event 2 best: 17.88 (Citi & Barbieri).
- **Leakage pitfalls.**
  - The Outcomes files contain `Length_of_stay` and `Survival`, which are outcome-derived. They also contain `SAPS-I` and `SOFA`, which were not inputs for B or C. The harness must strip all four.
  - The page text ("only those for set A are available") contradicts today's file listing. Labels are public now.
- **Noise.** The top two scores differ by 0.0008, and Event 1 is a thresholded metric on about 4,000 records. Report bootstrap CIs and the agent's rank band, not "beats #1".
- **Licence** [V raw]: "Open Data Commons Attribution License v1.0".
- **Contamination.** Set A is widely used in later ICU deep-learning papers, and the winning methods are published in the CinC 2012 proceedings (both UNVERIFIED background knowledge). The navigation lists a `sources/` folder; I did not inspect it, so entrants' code may be public, which is both a contamination vector and a route to paired re-runs.

### C2 Higgs Boson ML Challenge: https://opendata.cern.ch/record/328, paper https://proceedings.mlr.press/v42/cowa14.pdf
- **Download (200, not downloaded).** `curl -LO https://opendata.cern.ch/record/328/files/atlas-higgs-challenge-2014-v2.csv.gz` (65,630,848 B; 186.5 MiB unzipped).
- **Data and licence.** 818,238 events. Columns: EventId, 30 features (DER_*, PRI_*), Weight, Label, KaggleSet (t/b/v/u), KaggleWeight. CC0 [V].
- **Metric.** AMS = sqrt(2((s + b + b_r) ln(1 + s/(b + b_r)) − s)) with b_r = 10 [V record page; paper Eq. 7].
- **Exact replication** [V, paper Appendix C]. KaggleSet and KaggleWeight "allow to recover the original Kaggle training, public and private data sets… and to recompute the original exact public and private Kaggle leaderboard scores". Sizes: 250K train, 100K public, 450K private (§5.1).
- **Human protocol** [V, §5.3]. Participants had public-leaderboard feedback, and "the calculated metric is the best AMSc among two solutions formally submitted by each participant". The agent's single locked shot on `v` is therefore stricter. Exclude `u` events, and use `b` only to emulate the public leaderboard (or not at all).
- **Human reference** [V, Table 2, p. 20, "Excerpts of the private leaderboard"]:

  | Rank | Team | AMS | Method |
  |---|---|---|---|
  | 1 | Gábor Melis | 3.80581 | DNN |
  | 2 | Tim Salimans | 3.78913 | |
  | 3 | nhlx5haze | 3.78682 | |
  | 8 | Luboš Motl's team | 3.76050 | "XGboost and Intensive feature engineering" |
  | 31 | Mymo | 3.72594 | |
  | 45 | Crowwork | 3.71885 | "XGBoost Tuned" |
  | 782 | Eckhard | 3.49945 | "TMVA Tuned" |
  | 902 | Benchmark | 3.40488 | MultiBoost |
  | 991 | Benchmark | 3.19956 | TMVA |

  The field was "1785 teams (1942 people)" (§6.1). The median is not published; rank ≈893 lies between ranks 782 and 902 [inference]. The classical (GBDT) reference points are ranks 8 and 45.
- **Leakage pitfalls.**
  - Weight and KaggleWeight must never be features: the weight distribution would have "given away the label" (§5.1).
  - Internal CV needs weight renormalisation (Eq. 31).
- **Noise.** The paper bootstraps the ranks; ranks 2 and 3 are statistically indistinguishable (§6.2).
- **Licence.** "Creative Commons Zero v1.0 Universal" appears in the raw record HTML [V].
- **Contamination: highest.** This is reputedly XGBoost's breakthrough competition, the winners' write-ups are public, and feature tricks are widely blogged (UNVERIFIED background knowledge). The paper does cite a companion write-up of the winning method (Melis, 2015) [V].

### C3 KDD Cup 1998: https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html, UCI https://archive.ics.uci.edu/dataset/129/kdd+cup+1998+data
- **Download (200).** `…/kddcup98/epsilon_mirror/{cup98lrn.zip (36,468,735 B), cup98val.zip (36,763,018 B), valtargt.txt (1,104,529 B)}`. Combined archive: `https://archive.ics.uci.edu/static/public/129/kdd+cup+1998+data.zip`.
- **Data.** "<cup98LRN.txt> contains 95412 records and 481 fields"; validation "96367 records and 479 variables" (no targets) [V, cup98doc.txt].
- **Licence.** The UCI page says CC BY 4.0 [V]. The original page also asks users to notify the dataset donors of results and publications, and not to name the sponsoring charity to trainees in teaching [V]. The 1998 contacts may be defunct. Disclose both.
- **Metric** [V, cup98doc.txt "EVALUATION RULES"]: "Sum (the actual donation amount − $0.68) over all records for which the expected revenue (or predicted value of the donation) is over $0.68… rounded to the nearest 10 dollars."
- **Human protocol.** Each participant returned one file of predictions by email by the deadline. There was no leaderboard; this is implied by the rules, not stated as "single submission". That is essentially our locked, score-once design.
- **Human reference** [V, KDnuggets 98:19 item 1, https://kdnuggets.com/news/98/n19.html, "TABLE 2: … Total Profits"]:
  - GainSmarts $14,712; SAS $14,662; Quadstone $13,954; CARRL $13,825; Amdocs $13,794; #6 $13,598; … #21 −$54.
  - Median, 11th of 21: $10,720 [computed].
  - TABLE 1 row "Profit Damt-.68 96,367 … $10,560" is the mail-everyone profit. The page does not call it a baseline. I reproduced $10,560.08 from valtargt.txt (4,873 donors) [computed].
- **Noise and evidence strength.**
  - One gift contributes up to $499.32, and the top three are within $758. Use a bootstrap.
  - Only 12 of 21 entries beat mail-everyone's $10,560 [computed], and the median beats it by just $160.
  - The humans used 1998 tools, so beating them with 2026 GBDTs is weak evidence by itself. Post-1998 expert results exist in the literature but are UNVERIFIED here.
- **Contamination: moderate.** This is a classic textbook dataset, and the two-stage approach (P(respond) × E[amount | respond]) is widely taught (UNVERIFIED background knowledge).

### C4 M4 Weekly / Hourly: https://github.com/Mcompetitions/M4-methods
- **Download (200).**
  - `raw.githubusercontent.com/Mcompetitions/M4-methods/master/Dataset/{Train/Weekly-train.csv (4,015,067 B), Test/Weekly-test.csv (44,247 B), Train/Hourly-train.csv (2,347,115 B), Test/Hourly-test.csv (132,820 B), M4-info.csv}`.
  - Mirror: `https://zenodo.org/api/records/4656522/files/m4_weekly_dataset.zip/content` (CC BY 4.0, "359 weekly time series used in the M4 forecasting competition") [V].
- **Sizes** [computed from M4-info.csv]. Weekly 359 series, h = 13. Hourly 414 series, h = 48 (SP 24). Daily 4,227 series, h = 14.
- **Licence.** The GitHub API reports `license: null`, so the original licence is UNVERIFIED.
- **Metric and protocol.** OWA is "overall weighted average of the relative sMAPE and the relative MASE" (footnote in the xlsx [V]). The scoring code is `Benchmarks and Evaluation.R`. The test file is fixed.
- **Exactness check** [computed]. Naive2 (last value, m = 1) on the official Weekly files gives sMAPE 9.161 and MASE 2.777, identical to the xlsx Naive2 Weekly row.
- **Human reference** [V, `Evaluation and Ranks.xlsx`, sheet "Point Forecasts-Frequency", OWA columns; medians computed over the 49 valid submissions]:
  - Weekly: best 0.739 (ID 235, Darin & Stellwagen / Forecast Pro); 0.751 (ID 36); 0.766 (ID 237). Median 0.930. Benchmarks: Damped 0.917, Comb 0.926, Theta 0.971, Naive2 1.000.
  - Hourly: best 0.410 (ID 238, Doornik et al.); 0.440 (ID 118, Smyl, the overall winner at total OWA 0.821). Median 0.794. sNaive 0.627, Theta 1.006.
  - All 49 submissions' point forecasts are in `Point Forecasts/`, which allows paired per-series comparisons.
- **Like-for-like caveat.** Teams optimised total OWA over 100k series, not Weekly alone. A frequency-specialised agent is not like-for-like; state this plainly.
- **Pitfalls.** "Originally the starting date wasn't provided to the participants" [V, README], so withhold `StartingDate`. Calendar alignment across series enables look-ahead leakage. 359 series give noisy averages; bootstrap over series.
- **Contamination: high.** The test values are public in the repo. Later methods such as N-BEATS reportedly publish per-frequency M4 results (UNVERIFIED), which would give the agent hindsight.

### C5 CDC FluSight: https://github.com/cdcepi/FluSight-forecast-hub
- **Download (200).** `raw.githubusercontent.com/cdcepi/FluSight-forecast-hub/main/target-data/{time-series.csv (95,069,683 B), target-hospital-admissions.csv (616,178 B)}` and `model-output/<model>/<ref_date>-<model>.csv` (for example FluSight-ensemble 2026-01-10, 1,071,584 B). `time-series.csv` has an `as_of` vintage column (header verified by ranged GET).
- **Scale** [computed from the repo tree; directory counts]:
  - 2025–26 season: 68 model directories with files, of which 56 are not hub-generated `FluSight-*` entries, from 35 distinct team prefixes. 29 reference dates (2025-10-18 to 2026-05-30). Whether every model submitted the admissions target is UNVERIFIED.
  - 2026–27 season: 89 directories (79 non-hub, 42 team prefixes), 5 reference dates so far. The challenge "will run until May 26, 2027" [V, README].
- **Vintage coverage.**
  - `auxiliary-data/target-data-archive/` holds 25 hospital-admission snapshots in the 2025–26 window, with gaps (for example no 2025-10-18 to 2025-11-08).
  - Ranged reads at 59 offsets of `time-series.csv` found `as_of` values for weekly Wednesday vintages from 2025-11-19 to 2026-06-24 [computed].
  - Full per-week coverage, and the October 2025 dates, are UNVERIFIED. If they are missing, the retrospective cannot be replicated exactly for those weeks.
- **Target and metric** [V, README]. Quantile forecasts of weekly confirmed influenza admissions, horizons 0–3; "horizon of −1 will not be scored". WIS and relative WIS are "the ratio of average WIS values for each pair of models… normalizes by the mean pairwise WIS ratio for the baseline model" [V, Mathis et al. 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11282251/, Methods].
- **Prior-season human reference** [V, same paper, Table 1 "Performance metrics for teams meeting inclusion criteria", re-read from raw HTML]:
  - 2021–22: best CMU-TimeSeries (STAT) 0.74; Flusight-ensemble 0.82.
  - 2022–23: best MOBS-GLEAM_FLUH 0.61; Flusight-ensemble 0.77.
  - FluSight-baseline 1.00. "26 modeling teams submitted", of which "21 and 16" were eligible.
  - For 2025–26 the reference must be **recomputed from the submitted files** with the same scorer; it is not quoted from a page.
- **Replication: medium.** The agent must forecast each week from the `as_of` vintage only. Teams submitted unevenly, and inclusion rules matter. Truth is revised, so fix the scoring snapshot in advance.
- **Licence.** The README says "Anyone interested in using these data for additional research or publications is requested to contact flusight@cdc.gov".
- **Contamination.** For 2025–26 (Oct 2025 to May 2026), the season's shape may be in model pretraining. The 2026–27 prospective run is after a June 2026 cutoff, so it is contamination-free, but its result only arrives about June 2027.

### C6 Tourism 2010: paper https://robjhyndman.com/papers/forecompijf.pdf ("Corrected 20 September 2010")
- **Download (200).** `https://zenodo.org/api/records/4656096/files/tourism_monthly_dataset.zip/content` (199,791 B, CC BY 4.0, "366 monthly time series used in the Kaggle Tourism forecasting competition"). The CRAN `Tcomp` package (GPL-3) is described as "Data from the 2010 Tourism Forecasting Competition" [V]; whether its train/test split matches the paper is UNVERIFIED.
- **Data.** "366 monthly, 427 quarterly and 518 yearly series" [V]. Horizons (from the Table 4–6 columns): 24, 8 and 4.
- **Reference** [V, Table 4, MASE row, "Average 1–24"]: ARIMA 1.38, ForePro 1.40, ETS 1.49, SNaive 1.54, Theta 1.55, Damped 1.66. These are methods the organisers ran, plus the Forecast Pro package; they are not independent teams.
- **Gaps.** The Kaggle-phase team scores are in "The value of feedback in forecasting competitions" (IJF 27(3):845–849), which I did not fetch (UNVERIFIED). Whether the Kaggle data is identical to the paper data is also UNVERIFIED. The reference is weak.

### C7 TabArena-v0.1: https://github.com/autogluon/tabarena (paper arXiv 2506.16791, v4 2025-11-03)
- **Protocol** [V, README]. 51 curated datasets with 9–30 splits each. Models are "tuned by TabArena under a shared protocol" with search spaces "contributed by the method authors", up to 200 configs, 8-fold bagging. The leaderboard https://tabarena.ai 301-redirects to an HF Space that did not render.
- **Results.** "Per-dataset and per-split results: not hosted". They are generated as `results_per_split.csv` by their scripts. There is no page to quote, so every number is UNVERIFIED.
- **Lock-once fit.** Repeated outer CV puts every row in some test fold, so only split 0 (TabArena-Lite) can be locked.
- **Weaknesses.** The references are tuned baselines, not human teams, and curated features leave little room for feature engineering.

## 3. Ranked top 3 for a first showcase

**1. C1 PhysioNet/CinC 2012 (Event 1, set A → set C).**
- **Why it ranks first.**
  - Open data under ODC-BY, labels now public, about 20 MB in total.
  - Every specified element of the protocol is reproducible: train on A, one shot on C, per-record inference. Only the B-feedback loop is not.
  - The published top 10 of a 28-entrant field.
  - A clinical domain with genuine room for feature engineering on irregular 48 h time series, all on a laptop CPU.
- **Contamination: moderate.** The dataset is widely reused and the winners' papers are public (UNVERIFIED background knowledge).
- **Mitigations.**
  - Report the hindsight advantage: 2012 teams lacked 2013–2026 literature.
  - Give the field percentile with bootstrap CIs.
  - Run a pre-run memorisation probe, for example asking the LLM for set C mortality rates or top scores.
  - Strip leak columns.
  - Optionally re-run open-source human entries from `sources/` for paired tests (UNVERIFIED that they run).

**2. C2 Higgs 2014 (AMS on the private set).**
- **Why it ranks here.** It has the strongest human reference: 1,785 teams, with exact private-leaderboard recomputation from CC0 data. GBDT plus feature engineering is competitive (ranks 8 and 45 used XGBoost). I estimate 1–5 minute iterations with LightGBM on 250K × 30 (UNVERIFIED, not benchmarked).
- **Contamination: high.** It is the most famous of the set.
- **Mitigations.**
  - Present it as "rank band within 1,785 teams under a stricter single-shot protocol", not as a win.
  - Log and scan agent transcripts for recalled recipes (for example CAKE or the winner's DNN).
  - Report against the XGBoost rows, not only rank 1.

**3. C3 KDD Cup 1998 (net profit on validation).**
- **Why it ranks here.** The human protocol matches ours (one returned file, no feedback). The full 21-entry table is published, and the mail-everyone baseline reproduces to the dollar ($10,560.08 vs $10,560). Its 481 raw fields demand real feature engineering. Note that only 12 of 21 entries beat mail-everyone.
- **Contamination: moderate.**
- **Mitigations.**
  - Bootstrap CIs, given the heavy-tailed gifts.
  - Add a post-1998 expert reference before claiming anything (currently UNVERIFIED).
  - Disclose the dual licence terms.

**Time-series slot and follow-up.**
- If the first showcase must include forecasting, use **C4 M4 Weekly** (49 teams, every submission's forecasts public). State the frequency-tuning caveat and the high contamination.
- The best answer to contamination is **C5 FluSight 2026–27 run prospectively**: post-cutoff, 79 non-hub model directories from 42 team prefixes, scored with the hub's own data. Treat it as the second showcase (result about mid-2027). The human reference there is recomputed from the submitted files, not quoted.

## 4. Open uncertainties
- No median is published for C1 or C2. The C2 median is an inference from Table 2 brackets.
- The M4 original licence is UNVERIFIED.
- The KDD98 legacy notification contacts may be defunct.
- No published 2025–26 FluSight evaluation table was found. FluSight vintage coverage for October 2025 is UNVERIFIED.
- The contamination judgements are my background knowledge, not checked today.
- TabArena per-dataset numbers need tooling to generate.
- Several page summaries came via a summariser. The headline numbers for C1–C3 were re-checked verbatim from raw HTML or PDF text.
