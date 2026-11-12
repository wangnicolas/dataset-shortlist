# Evaluation summary

Model: fable. Judge: sonnet. Cases: 10. Total list-price cost: $107.64.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 6 | 0.98 | 0.94 | +0.04 | 2 / 4 / 0 |
| other fields | 4 | 0.97 | 0.84 | +0.13 | 2 / 2 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
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

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-h-cxr-free-text-reports | health | 0.94 (0.06) | 0.94 (0.06) | +0.00 |
| ho-h-derm-skin-tone | health | 1.00 (0.00) | 0.86 (0.14) | +0.14 |
| ho-h-ecg-rhythm-labels | health | 1.00 (0.00) | 0.89 (0.00) | +0.11 |
| ho-h-measured-bp-surveys | health | 0.94 (0.06) | 0.94 (0.06) | +0.00 |
| ho-h-wrist-activity-outcomes | health | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-o-01 | other fields | 1.00 (0.00) | 0.86 (0.00) | +0.14 |
| ho-o-02 | other fields | 0.88 (0.00) | 0.88 (0.00) | +0.00 |
| ho-o-03 | other fields | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-o-04 | other fields | 1.00 (0.00) | 0.64 (0.07) | +0.36 |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 20 | 22.2 | 396 of 445 (89%) | 15 | 34 |
| without | 20 | 6.8 | 114 of 136 (84%) | 0 | 22 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 28.9 | 456 | $3.79 | 757680 |
| without | 7.6 | 94 | $1.14 | 90342 |

## Checks

- Skill triggered in 20 of 20 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs without grader verdicts, scored 0: 0.
- Runs that never started: 0. The tool reports the suite as complete.
- Runs that ended with an error: 0.
- Traces missing: 0 of 40.

