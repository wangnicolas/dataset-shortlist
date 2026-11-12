# Held-out evaluation: the report

Ten sealed questions, Sonnet 5.5 (claude-sonnet-5-5), three runs per arm, 12 November 2026.

This file is assembled by `tools/make_report.py` from the records in `eval-runs/heldout-01`; no number in it is typed by hand. The protocol, written before any result existed, is `docs/EVAL_PROTOCOL.md`.

## 1. The statement under the rule fixed before the run

> **Mixed: the per-question table is the result.**

The rule's three conditions for "beats": a mean gain of 5 points or more, met (+9.6); a higher score on at least 7 of the 10 questions, not met (6); no stratum lower, met.

## 2. The comparison

### Comparison of the arms

Model: sonnet. Judge: sonnet. Total list-price cost of these runs: $46.44.

#### Score (share of graders passed, mean over cases)

In brackets: the same mean computed from run 1 alone, run 2 alone, and so on.

| Stratum | Cases | With the skill | No skill | No skill, told to verify |
|---|---|---|---|---|
| health | 6 | 0.92 (0.94, 0.90, 0.92) | 0.86 (0.89, 0.85, 0.85) | 0.88 (0.88, 0.88, 0.88) |
| other fields | 4 | 0.89 (0.88, 0.83, 0.97) | 0.73 (0.73, 0.76, 0.70) | 0.79 (0.91, 0.69, 0.77) |
| all | 10 | 0.91 (0.91, 0.87, 0.94) | 0.81 (0.83, 0.82, 0.79) | 0.85 (0.89, 0.81, 0.84) |

#### Pass rate by grader family

| Stratum | Family | With the skill | No skill | No skill, told to verify | Verdicts per arm (checks x runs) |
|---|---|---|---|---|---|
| health | recall | 1.00 | 1.00 | 0.90 | 60 |
| health | access | 0.86 | 0.73 | 0.82 | 51 |
| health | trap | 1.00 | 1.00 | 1.00 | 15 |
| health | long tail | 0.72 | 0.72 | 0.83 | 18 |
| other fields | recall | 0.89 | 0.81 | 0.83 | 36 |
| other fields | access | 0.83 | 0.63 | 0.73 | 30 |
| other fields | trap | 1.00 | 1.00 | 1.00 | 12 |
| other fields | long tail | 0.92 | 0.50 | 0.58 | 12 |

#### Per case

Mean over the runs of the case; in brackets, each run.

| Case | Stratum | With the skill | No skill | No skill, told to verify |
|---|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (1.00, 1.00, 1.00) | 1.00 (1.00, 1.00, 1.00) | 1.00 (1.00, 1.00, 1.00) |
| ho-h-cxr-free-text-reports | health | 0.92 (1.00, 0.88, 0.88) | 0.88 (0.88, 0.88, 0.88) | 0.96 (1.00, 0.88, 1.00) |
| ho-h-derm-skin-tone | health | 0.90 (0.86, 0.86, 1.00) | 0.67 (0.71, 0.71, 0.57) | 1.00 (1.00, 1.00, 1.00) |
| ho-h-ecg-rhythm-labels | health | 0.89 (0.89, 0.89, 0.89) | 0.93 (1.00, 0.89, 0.89) | 0.67 (0.67, 0.67, 0.67) |
| ho-h-measured-bp-surveys | health | 0.79 (0.88, 0.75, 0.75) | 0.75 (0.75, 0.75, 0.75) | 0.67 (0.62, 0.75, 0.62) |
| ho-h-wrist-activity-outcomes | health | 1.00 (1.00, 1.00, 1.00) | 0.96 (1.00, 0.88, 1.00) | 1.00 (1.00, 1.00, 1.00) |
| ho-o-01 | other fields | 0.95 (1.00, 0.86, 1.00) | 1.00 (1.00, 1.00, 1.00) | 0.86 (1.00, 0.71, 0.86) |
| ho-o-02 | other fields | 0.96 (0.88, 1.00, 1.00) | 0.75 (0.75, 0.88, 0.62) | 0.88 (0.88, 0.88, 0.88) |
| ho-o-03 | other fields | 0.75 (0.62, 0.75, 0.88) | 0.75 (0.75, 0.75, 0.75) | 0.67 (0.75, 0.75, 0.50) |
| ho-o-04 | other fields | 0.90 (1.00, 0.71, 1.00) | 0.43 (0.43, 0.43, 0.43) | 0.76 (1.00, 0.43, 0.86) |

#### Primary outcome and the rule fixed before the run

- With the skill against "No skill", 10 cases: mean case score 0.907 against 0.810, difference +0.096 (by run: +0.085, +0.054, +0.150). The skill scored higher on 6 cases, the same on 2, lower on 2.
  - health (6 cases): 0.917 against 0.863, difference +0.054.
  - other fields (4 cases): 0.891 against 0.732, difference +0.159.
  - **Statement under the rule: Mixed: the per-question table is the result.**
- With the skill against "No skill, told to verify", 10 cases: mean case score 0.907 against 0.845, difference +0.062 (by run: +0.020, +0.063, +0.101). The skill scored higher on 6 cases, the same on 2, lower on 2.
  - health (6 cases): 0.917 against 0.882, difference +0.035.
  - other fields (4 cases): 0.891 against 0.790, difference +0.101.

#### Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 8.0 | 217 of 241 (90%) | 4 | 20 |
| No skill | 0.0 | no links given | 0 | 0 |
| No skill, told to verify | 11.3 | 278 of 338 (82%) | 22 | 38 |

#### Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 16.3 | 2.9 | $0.44 | 14.3 |
| No skill | 1.0 | 0.5 | $0.07 | 0.0 |
| No skill, told to verify | 10.1 | 0.9 | $0.35 | 9.1 |

#### Verdicts that are not judgements

1 scored verdict(s) are failed calls to the judge, which the evaluation tool recorded as fails. They are counted above as recorded; nothing was judged again.

- ho-h-cxr-free-text-reports, With the skill, run 2, check `06-access-padchest-request` (grader threw: judge call failed: Not logged in · Please run /login)

Had they been passes: mean case score 0.911 with the skill against 0.810 without, difference +0.100; higher on 6 cases, the same on 2, lower on 2; statement under the rule: Mixed: the per-question table is the result.
Against the arm told to verify, with them as passes: difference +0.066; higher on 6 cases, the same on 3, lower on 1.

#### Checks

- Skill triggered in 30 of 30 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0
- Runs without grader verdicts, scored 0 and kept in every mean: 0
- Runs per arm: With the skill 30, No skill 30, No skill, told to verify 30.

The judge voted three times on each check. Over all the arms of the Sonnet runs its three votes agreed on 694 of 701 verdicts (99.0%); the other 7 were decided two to one. Verdicts whose judge call failed carry no votes and are not in this count.

1 of the verdicts of the two main arms is not a judgement: the call to the judge failed and the evaluation tool recorded a fail. Under the protocol's note on runs and verdicts they are counted as they were recorded, and nothing was judged again:

- `ho-h-cxr-free-text-reports`, with the skill, run 2, check `06-access-padchest-request` (grader threw: judge call failed: Not logged in · Please run /login)

Had it been a pass instead, the mean difference would be +10.0 points with the skill higher on 6 questions, the same on 2 and lower on 2, and the statement under the rule would be: "Mixed: the per-question table is the result."

## 3. Which checks differ between the two main arms

Each check was judged in three runs per arm.

Checks the skill passed more often (13):

| Question | Check | Kind | With the skill | No skill |
|---|---|---|---|---|
| Chest X-rays with free-text reports | `06-access-padchest-request` | access | 1 of 3 | 0 of 3 |
| Skin images with skin-tone labels | `04-access-ddi-registration` | access | 3 of 3 | 2 of 3 |
| Skin images with skin-tone labels | `05-access-scin-download` | access | 3 of 3 | 0 of 3 |
| Skin images with skin-tone labels | `07-long-tail` | long tail | 1 of 3 | 0 of 3 |
| National surveys with measured blood pressure | `06-access-charls-application` | access | 2 of 3 | 0 of 3 |
| Wrist accelerometry linked to outcomes | `05-access-allofus-dura` | access | 3 of 3 | 2 of 3 |
| Linked employer-employee microdata | `06-access-brazil-ministry-agreement` | access | 3 of 3 | 1 of 3 |
| Linked employer-employee microdata | `08-long-tail` | long tail | 3 of 3 | 0 of 3 |
| Meeting recordings for diarization, commercial use | `02-recall-chime6-dinner-party` | recall | 1 of 3 | 0 of 3 |
| Galaxy images with human morphology labels | `03-recall-galaxy-zoo-hubble` | recall | 2 of 3 | 0 of 3 |
| Galaxy images with human morphology labels | `04-access-gz2-free-download` | access | 3 of 3 | 0 of 3 |
| Galaxy images with human morphology labels | `05-access-decals-zenodo` | access | 3 of 3 | 0 of 3 |
| Galaxy images with human morphology labels | `07-long-tail` | long tail | 2 of 3 | 0 of 3 |

Checks the skill passed less often (4):

| Question | Check | Kind | With the skill | No skill |
|---|---|---|---|---|
| 12-lead ECGs with rhythm labels, no application | `09-long-tail` | long tail | 0 of 3 | 1 of 3 |
| National surveys with measured blood pressure | `04-access-nhanes-download` | access | 2 of 3 | 3 of 3 |
| Taxi GPS trajectories | `05-access-sf-cab-login` | access | 2 of 3 | 3 of 3 |
| Meeting recordings for diarization, commercial use | `06-access-notsofar-cc-by` | access | 2 of 3 | 3 of 3 |

Checks neither arm passed in any run (2):

| Question | Check | Kind | With the skill | No skill |
|---|---|---|---|---|
| National surveys with measured blood pressure | `05-access-hse-registration` | access | 0 of 3 | 0 of 3 |
| Meeting recordings for diarization, commercial use | `05-access-chime-commercial-ok` | access | 0 of 3 | 0 of 3 |

## 4. A look taken after the results: the outcome with one kind of check left out

This table is not part of the rule. It was computed after the result was known, to see where the difference comes from, and it is descriptive only.

| Checks counted | With the skill | No skill | Difference, points | Higher / same / lower | Under the rule |
|---|---|---|---|---|---|
| all (the primary outcome) | 90.7% | 81.0% | +9.6 | 6 / 2 / 2 | mixed |
| all except: found the suitable datasets | 87.3% | 73.3% | +14.0 | 6 / 1 / 3 | mixed |
| all except: stated how to obtain them correctly | 93.7% | 88.2% | +5.4 | 4 / 5 / 1 | mixed |
| all except: avoided the unsuitable famous one | 89.3% | 78.1% | +11.2 | 6 / 2 / 2 | mixed |
| all except: surfaced a less-known fitting dataset | 92.2% | 83.7% | +8.5 | 6 / 3 / 1 | mixed |
| only: found the suitable datasets | 95.6% | 92.2% | +3.3 | 2 / 8 / 0 | level |
| only: stated how to obtain them correctly | 86.1% | 66.7% | +19.4 | 6 / 2 / 2 | mixed |
| only: avoided the unsuitable famous one | 100.0% | 100.0% | +0.0 | 0 / 9 / 0 | level |
| only: surfaced a less-known fitting dataset | 80.0% | 63.3% | +16.7 | 3 / 6 / 1 | mixed |

## 5. How far the runs with the skill went through the workflow

### How far the with-skill runs went through the workflow

Read from the traces of 30 with-skill runs.

| Step | Runs that did it |
|---|---|
| Loaded the skill | 30 |
| Searched the registries (`search`) | 30 |
| Searched the literature (`papers`) | 29 |
| Ran the verifier (`verify`) | 27 |
| Read access pages with the tool (`read`) | 26 |
| Added candidates found elsewhere (`add`) | 11 |
| Rendered the interactive page (`render`) | 16 |
| Used web search | 17 |
| Fetched pages with the agent's own tool | 15 |

#### The interactive page

- Written in 16 of 30 runs.
- Answers that point to a page that was not written: 0
- Runs without a page whose answer does not say so: 0

## 6. The pages written during the run

### Pages written during the run

Counted from the files each session left in its working folder.

| Arm | Runs | Folder kept | Page written | Datasets on the pages | With a verification stamp | Access left unknown |
|---|---|---|---|---|---|---|
| with | 30 | 30 | 16 | 85 | 62 | 11 |
| without | 30 | 30 | 0 | 0 | 0 | 0 |

#### The access field on the pages

The page of version 0.1.0 knows six words (open, account, gated, controlled, closed, unknown) and shows anything else as "Unknown".

| Word written in the access field | Datasets | Shown by the page as |
|---|---|---|
| open | 33 | its own tier |
| application | 20 | Unknown |
| unknown | 11 | its own tier |
| restricted | 6 | Unknown |
| account | 5 | its own tier |
| gated | 5 | its own tier |
| fee | 2 | Unknown |
| registered | 2 | Unknown |
| free account | 1 | Unknown |

Of 85 datasets, 31 carry a word the page did not know: the session had written an access condition and the page showed "Unknown". 11 were written as unknown.

#### Per run

| Run | Page | Datasets | Verified | Access unknown | With papers |
|---|---|---|---|---|---|
| ho-h-checkpoint-response-rnaseq__with__1 | yes | 8 | 0 | 8 | 0 |
| ho-h-checkpoint-response-rnaseq__with__2 | no |  |  |  |  |
| ho-h-checkpoint-response-rnaseq__with__3 | no |  |  |  |  |
| ho-h-cxr-free-text-reports__with__1 | yes | 7 | 3 | 0 | 0 |
| ho-h-cxr-free-text-reports__with__2 | yes | 5 | 5 | 2 | 0 |
| ho-h-cxr-free-text-reports__with__3 | yes | 7 | 4 | 0 | 3 |
| ho-h-derm-skin-tone__with__1 | yes | 3 | 3 | 0 | 2 |
| ho-h-derm-skin-tone__with__2 | no |  |  |  |  |
| ho-h-derm-skin-tone__with__3 | no |  |  |  |  |
| ho-h-ecg-rhythm-labels__with__1 | no |  |  |  |  |
| ho-h-ecg-rhythm-labels__with__2 | no |  |  |  |  |
| ho-h-ecg-rhythm-labels__with__3 | no |  |  |  |  |
| ho-h-measured-bp-surveys__with__1 | no |  |  |  |  |
| ho-h-measured-bp-surveys__with__2 | no |  |  |  |  |
| ho-h-measured-bp-surveys__with__3 | no |  |  |  |  |
| ho-h-wrist-activity-outcomes__with__1 | yes | 7 | 2 | 0 | 4 |
| ho-h-wrist-activity-outcomes__with__2 | yes | 6 | 3 | 0 | 5 |
| ho-h-wrist-activity-outcomes__with__3 | no |  |  |  |  |
| ho-o-01__with__1 | no |  |  |  |  |
| ho-o-01__with__2 | no |  |  |  |  |
| ho-o-01__with__3 | no |  |  |  |  |
| ho-o-02__with__1 | yes | 7 | 7 | 0 | 0 |
| ho-o-02__with__2 | yes | 4 | 4 | 0 | 0 |
| ho-o-02__with__3 | yes | 6 | 6 | 0 | 0 |
| ho-o-03__with__1 | yes | 4 | 4 | 0 | 0 |
| ho-o-03__with__2 | yes | 5 | 5 | 0 | 1 |
| ho-o-03__with__3 | yes | 4 | 4 | 1 | 0 |
| ho-o-04__with__1 | yes | 3 | 3 | 0 | 0 |
| ho-o-04__with__2 | yes | 5 | 5 | 0 | 1 |
| ho-o-04__with__3 | yes | 4 | 4 | 0 | 0 |

## 7. Blind audit of every recommended dataset (the two main arms)

#### Blind audit of every recommended dataset (run 1 of each case and arm)

| Arm | Datasets audited | Per answer | Exist as described | Access condition stated correctly | Meet the must-haves |
|---|---|---|---|---|---|
| with | 83 | 8.3 | 99% (80 of 81 judged) | 93% (65 of 70 judged) | 90% (63 of 70 judged) |
| without | 76 | 7.6 | 100% (75 of 75 judged) | 90% (54 of 60 judged) | 94% (61 of 65 judged) |

"Judged" leaves out the items the auditor could not settle: an official page that could not be reached, an answer that stated no access condition, or documentation that does not say.

##### Access statements by how the answer marked them

| Arm | Marked as checked today: correct | Marked as recalled: correct | Not marked: correct |
|---|---|---|---|
| with | 98% (39 of 40) | 87% (26 of 30) | n/a (0 of 0) |
| without | n/a (0 of 0) | 90% (54 of 60) | n/a (0 of 0) |

The skill marks each access statement as confirmed today or recalled. The marking carries information: 39 of 40 statements marked as checked today were right, against 26 of 30 marked as recalled.

The auditors were ten agents started on the model alias `opus`, which their transcripts name as `claude-opus-5-5` (the answers were written by `claude-sonnet-5-5`), one per question, each given a folder with the question and the two answers and nothing else; the record of how they were run is in `eval-runs/heldout-01/audit/README.md`. The auditor was not told which arm wrote which answer, but the answers differ visibly, so the blinding is by label only.

The audit and the checks of section 2 measure different things. The audit asks whether what an answer says about a dataset is right. The access checks ask whether the answer states the particular facts a researcher needs in order to decide. An answer can be right in what it says and still leave those facts out.

## 8. The same comparison on a stronger model

The ten questions, Fable 5.2 (claude-fable-5-2), two runs per arm, 12 November 2026. Three of these questions were run as the protocol planned; the other seven were added after the result above was known. The rule was set for the main comparison only, so this is reported as a description.

Mean case score 97.5% with the skill and 90.0% without it (difference +7.5 points); higher on 4 questions, the same on 6, lower on 0.

2 of this run's verdicts are failed calls to the judge, recorded as fails; the list is in the table below. Counted as passes instead, the scores are 97.5% with the skill and 91.4% without it (difference +6.1 points).

### Comparison of the arms

Model: fable. Judge: sonnet. Total list-price cost of these runs: $107.64.

#### Score (share of graders passed, mean over cases)

In brackets: the same mean computed from run 1 alone, run 2 alone, and so on.

| Stratum | Cases | With the skill | No skill |
|---|---|---|---|
| health | 6 | 0.98 (0.98, 0.98) | 0.94 (0.91, 0.96) |
| other fields | 4 | 0.97 (0.97, 0.97) | 0.84 (0.86, 0.83) |
| all | 10 | 0.97 (0.97, 0.97) | 0.90 (0.89, 0.91) |

#### Pass rate by grader family

| Stratum | Family | With the skill | No skill | Verdicts per arm (checks x runs) |
|---|---|---|---|---|
| health | recall | 1.00 | 1.00 | 40 |
| health | access | 0.94 | 0.91 | 34 |
| health | trap | 1.00 | 1.00 | 10 |
| health | long tail | 1.00 | 0.75 | 12 |
| other fields | recall | 1.00 | 0.83 | 24 |
| other fields | access | 1.00 | 0.95 | 20 |
| other fields | trap | 1.00 | 1.00 | 8 |
| other fields | long tail | 0.75 | 0.50 | 8 |

#### Per case

Mean over the runs of the case; in brackets, each run.

| Case | Stratum | With the skill | No skill |
|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (1.00, 1.00) | 1.00 (1.00, 1.00) |
| ho-h-cxr-free-text-reports | health | 0.94 (1.00, 0.88) | 0.94 (1.00, 0.88) |
| ho-h-derm-skin-tone | health | 1.00 (1.00, 1.00) | 0.86 (0.71, 1.00) |
| ho-h-ecg-rhythm-labels | health | 1.00 (1.00, 1.00) | 0.89 (0.89, 0.89) |
| ho-h-measured-bp-surveys | health | 0.94 (0.88, 1.00) | 0.94 (0.88, 1.00) |
| ho-h-wrist-activity-outcomes | health | 1.00 (1.00, 1.00) | 1.00 (1.00, 1.00) |
| ho-o-01 | other fields | 1.00 (1.00, 1.00) | 0.86 (0.86, 0.86) |
| ho-o-02 | other fields | 0.88 (0.88, 0.88) | 0.88 (0.88, 0.88) |
| ho-o-03 | other fields | 1.00 (1.00, 1.00) | 1.00 (1.00, 1.00) |
| ho-o-04 | other fields | 1.00 (1.00, 1.00) | 0.64 (0.71, 0.57) |

#### Primary outcome and the rule fixed before the run

- With the skill against "No skill", 10 cases: mean case score 0.975 against 0.900, difference +0.075 (by run: +0.083, +0.068). The skill scored higher on 4 cases, the same on 6, lower on 0.
  - health (6 cases): 0.979 against 0.937, difference +0.042.
  - other fields (4 cases): 0.969 against 0.844, difference +0.125.
  - **Statement under the rule: Mixed: the per-question table is the result.**

#### Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 22.2 | 396 of 445 (89%) | 15 | 34 |
| No skill | 6.8 | 114 of 136 (84%) | 0 | 22 |

#### Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 28.9 | 7.6 | $3.79 | 26.9 |
| No skill | 7.6 | 1.6 | $1.14 | 6.6 |

#### Verdicts that are not judgements

2 scored verdict(s) are failed calls to the judge, which the evaluation tool recorded as fails. They are counted above as recorded; nothing was judged again.

- ho-o-01, No skill, run 1, check `03-recall-sf-cabspotting` (grader threw: judge call failed: API Error: No response from API (waited 3m, then 10m on the retry). If a prox)
- ho-o-01, No skill, run 2, check `03-recall-sf-cabspotting` (grader threw: judge call failed: API Error: No response from API (waited 3m, then 10m on the retry). If a prox)

Had they been passes: mean case score 0.975 with the skill against 0.914 without, difference +0.061; higher on 3 cases, the same on 7, lower on 0; statement under the rule: Mixed: the per-question table is the result.

#### Checks

- Skill triggered in 20 of 20 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0
- Runs without grader verdicts, scored 0 and kept in every mean: 0
- Runs per arm: With the skill 20, No skill 20.

## 9. Does the skill start when it should

### Trigger test (sonnet)

The skill started on 10 of 10 requests that ask for datasets and on 0 of 10 requests that do not.

| Should start | First action | Request |
|---|---|---|
| yes | the skill | im starting my masters thesis on predicting hospital readmission for heart failure patients. my supervisor sai |
| yes | the skill | Is there an open dataset of smart-meter readings at 15-minute resolution for at least a few thousand household |
| yes | the skill | we want to benchmark our speech emotion recognition model on something other than the corpus we used so far be |
| yes | the skill | I need longitudinal survey data on adolescent mental health with at least three waves, ideally from East Asia. |
| yes | the skill | can you find me data for training a model to detect rooftop solar panels in aerial imagery? has to be download |
| yes | the skill | How do I get access to the imaging data of a big national biobank, and is there anything similar that is faste |
| yes | the skill | For a class project (due in 3 weeks) on fake news detection in Japanese, what labelled corpora exist? |
| yes | the skill | My PI wants a second external validation cohort for our sepsis model. We already hold credentialed access to o |
| yes | the skill | looking for raw EEG recordings during sleep with expert-scored hypnograms, kids not adults |
| yes | the skill | What data could I use to study the effect of remote work on urban transit ridership since 2020? City level is  |
| no | Bash | I downloaded the taxi trip parquet files into ./data, can you profile them and tell me which columns have the  |
| no | Write | Write a PyTorch Dataset class that loads images and labels from a folder structure like train/<class>/<img>.jp |
| no | Bash | Split my dataset.csv into train/val/test 70/15/15 stratified by the 'label' column and save the three files ne |
| no | final answer without a tool call | I already have the ICU database loaded in BigQuery. Can you explain what its stays table contains and how it l |
| no | ToolSearch | Find me recent papers on diffusion models for time series forecasting and summarise how they handle irregular  |
| no | Bash | I need to generate a synthetic dataset of 10,000 fake customer records with realistic names and addresses for  |
| no | final answer without a tool call | Our Postgres database has an events table with 2 billion rows; how should I index it for range queries on crea |
| no | Bash | Upload my cleaned dataset in ./release to the Hugging Face Hub and write a dataset card for it |
| no | final answer without a tool call | What's the license of scikit-learn and can I ship it inside a commercial product? |
| no | Bash | Convert these 300 DICOM files in ./scans to NIfTI and strip the patient names from the headers |

## 10. Limits

- The answer keys were built by Claude agents from published papers and official pages and re-checked on a different model. They were not written by human domain experts.
- The judge is a language model; three votes per check, majority wins. Link checks are done by script.
- Several access checks ask for an explicit statement of how the data is obtained. An answer that names a hosting site without saying whether an application is needed fails such a check.
- Famous datasets are known to every arm from training, so finding those measures little.
- Ten questions is a small sample; the result is descriptive and no significance test is claimed.
- The web changes: access rules and links are those of the day of the run.
- The held-out questions are published with these records, so they are spent. A later version needs a new set.
