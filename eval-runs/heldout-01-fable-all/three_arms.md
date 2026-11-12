# Comparison of the arms

Model: fable. Judge: sonnet. Total list-price cost of these runs: $107.64.

## Score (share of graders passed, mean over cases)

In brackets: the same mean computed from run 1 alone, run 2 alone, and so on.

| Stratum | Cases | With the skill | No skill |
|---|---|---|---|
| health | 6 | 0.98 (0.98, 0.98) | 0.94 (0.91, 0.96) |
| other fields | 4 | 0.97 (0.97, 0.97) | 0.84 (0.86, 0.83) |
| all | 10 | 0.97 (0.97, 0.97) | 0.90 (0.89, 0.91) |

## Pass rate by grader family

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

## Per case

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

## Primary outcome and the rule fixed before the run

- With the skill against "No skill", 10 cases: mean case score 0.975 against 0.900, difference +0.075 (by run: +0.083, +0.068). The skill scored higher on 4 cases, the same on 6, lower on 0.
  - health (6 cases): 0.979 against 0.937, difference +0.042.
  - other fields (4 cases): 0.969 against 0.844, difference +0.125.
  - **Statement under the rule: Mixed: the per-question table is the result.**

## Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 22.2 | 396 of 445 (89%) | 15 | 34 |
| No skill | 6.8 | 114 of 136 (84%) | 0 | 22 |

## Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 28.9 | 7.6 | $3.79 | 26.9 |
| No skill | 7.6 | 1.6 | $1.14 | 6.6 |

## Verdicts that are not judgements

2 scored verdict(s) are failed calls to the judge, which the evaluation tool recorded as fails. They are counted above as recorded; nothing was judged again.

- ho-o-01, No skill, run 1, check `03-recall-sf-cabspotting` (grader threw: judge call failed: API Error: No response from API (waited 3m, then 10m on the retry). If a prox)
- ho-o-01, No skill, run 2, check `03-recall-sf-cabspotting` (grader threw: judge call failed: API Error: No response from API (waited 3m, then 10m on the retry). If a prox)

Had they been passes: mean case score 0.975 with the skill against 0.914 without, difference +0.061; higher on 3 cases, the same on 7, lower on 0; statement under the rule: Mixed: the per-question table is the result.

## Checks

- Skill triggered in 20 of 20 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0
- Runs without grader verdicts, scored 0 and kept in every mean: 0
- Runs per arm: With the skill 20, No skill 20.

