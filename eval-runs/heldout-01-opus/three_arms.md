# Comparison of the arms

Model: opus. Judge: sonnet. Total list-price cost of these runs: $57.31.

## Score (share of graders passed, mean over cases)

In brackets: the same mean computed from run 1 alone, run 2 alone, and so on.

| Stratum | Cases | With the skill | No skill |
|---|---|---|---|
| health | 6 | 0.98 (0.98, 0.98, 0.98) | 0.95 (0.96, 0.90, 1.00) |
| other fields | 4 | 0.97 (1.00, 0.93, 0.97) | 0.87 (0.90, 0.83, 0.87) |
| all | 10 | 0.97 (0.99, 0.96, 0.97) | 0.92 (0.94, 0.87, 0.95) |

## Pass rate by grader family

| Stratum | Family | With the skill | No skill | Verdicts per arm (checks x runs) |
|---|---|---|---|---|
| health | recall | 1.00 | 0.97 | 60 |
| health | access | 0.94 | 0.92 | 51 |
| health | trap | 1.00 | 1.00 | 15 |
| health | long tail | 1.00 | 0.94 | 18 |
| other fields | recall | 1.00 | 0.86 | 36 |
| other fields | access | 0.97 | 0.77 | 30 |
| other fields | trap | 1.00 | 1.00 | 12 |
| other fields | long tail | 0.83 | 1.00 | 12 |

## Per case

Mean over the runs of the case; in brackets, each run.

| Case | Stratum | With the skill | No skill |
|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (1.00, 1.00, 1.00) | 1.00 (1.00, 1.00, 1.00) |
| ho-h-cxr-free-text-reports | health | 1.00 (1.00, 1.00, 1.00) | 0.96 (1.00, 0.88, 1.00) |
| ho-h-derm-skin-tone | health | 1.00 (1.00, 1.00, 1.00) | 1.00 (1.00, 1.00, 1.00) |
| ho-h-ecg-rhythm-labels | health | 1.00 (1.00, 1.00, 1.00) | 0.96 (1.00, 0.89, 1.00) |
| ho-h-measured-bp-surveys | health | 0.88 (0.88, 0.88, 0.88) | 0.79 (0.75, 0.62, 1.00) |
| ho-h-wrist-activity-outcomes | health | 1.00 (1.00, 1.00, 1.00) | 1.00 (1.00, 1.00, 1.00) |
| ho-o-01 | other fields | 1.00 (1.00, 1.00, 1.00) | 1.00 (1.00, 1.00, 1.00) |
| ho-o-02 | other fields | 0.92 (1.00, 0.88, 0.88) | 0.96 (1.00, 0.88, 1.00) |
| ho-o-03 | other fields | 1.00 (1.00, 1.00, 1.00) | 0.75 (0.75, 0.75, 0.75) |
| ho-o-04 | other fields | 0.95 (1.00, 0.86, 1.00) | 0.76 (0.86, 0.71, 0.71) |

## Primary outcome and the rule fixed before the run

- With the skill against "No skill", 10 cases: mean case score 0.974 against 0.918, difference +0.056 (by run: +0.052, +0.088, +0.029). The skill scored higher on 5 cases, the same on 4, lower on 1.
  - health (6 cases): 0.979 against 0.952, difference +0.027.
  - other fields (4 cases): 0.967 against 0.868, difference +0.100.
  - **Statement under the rule: Mixed: the per-question table is the result.**

## Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 12.5 | 316 of 376 (84%) | 24 | 36 |
| No skill | 3.4 | 94 of 103 (91%) | 5 | 4 |

## Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 21.6 | 5.8 | $1.28 | 19.6 |
| No skill | 3.0 | 1.0 | $0.27 | 2.0 |

## Checks

- Skill triggered in 30 of 30 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0
- Runs without grader verdicts, scored 0 and kept in every mean: 0
- Runs per arm: With the skill 30, No skill 30.

