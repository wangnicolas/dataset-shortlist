# Comparison of the arms

Model: sonnet. Judge: sonnet. Total list-price cost of these runs: $46.44.

## Score (share of graders passed, mean over cases)

In brackets: the same mean computed from run 1 alone, run 2 alone, and so on.

| Stratum | Cases | With the skill | No skill | No skill, told to verify |
|---|---|---|---|---|
| health | 6 | 0.92 (0.94, 0.90, 0.92) | 0.86 (0.89, 0.85, 0.85) | 0.88 (0.88, 0.88, 0.88) |
| other fields | 4 | 0.89 (0.88, 0.83, 0.97) | 0.73 (0.73, 0.76, 0.70) | 0.79 (0.91, 0.69, 0.77) |
| all | 10 | 0.91 (0.91, 0.87, 0.94) | 0.81 (0.83, 0.82, 0.79) | 0.85 (0.89, 0.81, 0.84) |

## Pass rate by grader family

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

## Per case

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

## Primary outcome and the rule fixed before the run

- With the skill against "No skill", 10 cases: mean case score 0.907 against 0.810, difference +0.096 (by run: +0.085, +0.054, +0.150). The skill scored higher on 6 cases, the same on 2, lower on 2.
  - health (6 cases): 0.917 against 0.863, difference +0.054.
  - other fields (4 cases): 0.891 against 0.732, difference +0.159.
  - **Statement under the rule: Mixed: the per-question table is the result.**
- With the skill against "No skill, told to verify", 10 cases: mean case score 0.907 against 0.845, difference +0.062 (by run: +0.020, +0.063, +0.101). The skill scored higher on 6 cases, the same on 2, lower on 2.
  - health (6 cases): 0.917 against 0.882, difference +0.035.
  - other fields (4 cases): 0.891 against 0.790, difference +0.101.

## Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 8.0 | 217 of 241 (90%) | 4 | 20 |
| No skill | 0.0 | no links given | 0 | 0 |
| No skill, told to verify | 11.3 | 278 of 338 (82%) | 22 | 38 |

## Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 16.3 | 2.9 | $0.44 | 14.3 |
| No skill | 1.0 | 0.5 | $0.07 | 0.0 |
| No skill, told to verify | 10.1 | 0.9 | $0.35 | 9.1 |

## Verdicts that are not judgements

1 scored verdict(s) are failed calls to the judge, which the evaluation tool recorded as fails. They are counted above as recorded; nothing was judged again.

- ho-h-cxr-free-text-reports, With the skill, run 2, check `06-access-padchest-request` (grader threw: judge call failed: Not logged in · Please run /login)

Had they been passes: mean case score 0.911 with the skill against 0.810 without, difference +0.100; higher on 6 cases, the same on 2, lower on 2; statement under the rule: Mixed: the per-question table is the result.
Against the arm told to verify, with them as passes: difference +0.066; higher on 6 cases, the same on 3, lower on 1.

## Checks

- Skill triggered in 30 of 30 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0
- Runs without grader verdicts, scored 0 and kept in every mean: 0
- Runs per arm: With the skill 30, No skill 30, No skill, told to verify 30.

