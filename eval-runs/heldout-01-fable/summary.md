# Evaluation summary

Model: fable. Judge: sonnet. Cases: 3. Total list-price cost: $33.14.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 2 | 0.97 | 0.97 | +0.00 | 0 / 2 / 0 |
| other fields | 1 | 1.00 | 0.86 | +0.14 | 1 / 0 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
|---|---|---|---|---|
| health | recall | 1.00 | 1.00 | 14 |
| health | access | 0.92 | 0.92 | 12 |
| health | trap | 1.00 | 1.00 | 2 |
| health | long tail | 1.00 | 1.00 | 4 |
| other fields | recall | 1.00 | 0.67 | 6 |
| other fields | access | 1.00 | 1.00 | 4 |
| other fields | trap | 1.00 | 1.00 | 2 |
| other fields | long tail | 1.00 | 1.00 | 2 |

## Per case

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-h-cxr-free-text-reports | health | 0.94 (0.06) | 0.94 (0.06) | +0.00 |
| ho-o-01 | other fields | 1.00 (0.00) | 0.86 (0.00) | +0.14 |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 6 | 25.0 | 145 of 150 (97%) | 1 | 4 |
| without | 6 | 3.2 | 18 of 19 (95%) | 0 | 1 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 34.0 | 513 | $4.11 | 1004860 |
| without | 5.8 | 118 | $0.85 | 94674 |

## Checks

- Skill triggered in 6 of 6 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs without grader verdicts, scored 0: 0.
- Runs that never started: 0. The tool reports the suite as complete.
- Runs that ended with an error: 0.
- Traces missing: 0 of 12.

