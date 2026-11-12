# Evaluation summary

Model: opus. Judge: sonnet. Cases: 10. Total list-price cost: $57.31.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 6 | 0.98 | 0.95 | +0.03 | 3 / 3 / 0 |
| other fields | 4 | 0.97 | 0.87 | +0.10 | 2 / 1 / 1 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
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

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-h-cxr-free-text-reports | health | 1.00 (0.00) | 0.96 (0.06) | +0.04 |
| ho-h-derm-skin-tone | health | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-h-ecg-rhythm-labels | health | 1.00 (0.00) | 0.96 (0.05) | +0.04 |
| ho-h-measured-bp-surveys | health | 0.88 (0.00) | 0.79 (0.16) | +0.08 |
| ho-h-wrist-activity-outcomes | health | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-o-01 | other fields | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-o-02 | other fields | 0.92 (0.06) | 0.96 (0.06) | -0.04 |
| ho-o-03 | other fields | 1.00 (0.00) | 0.75 (0.00) | +0.25 |
| ho-o-04 | other fields | 0.95 (0.07) | 0.76 (0.07) | +0.19 |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 30 | 12.5 | 316 of 376 (84%) | 24 | 36 |
| without | 30 | 3.4 | 94 of 103 (91%) | 5 | 4 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 21.6 | 346 | $1.28 | 657056 |
| without | 3.0 | 61 | $0.27 | 45597 |

## Checks

- Skill triggered in 30 of 30 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs without grader verdicts, scored 0: 0.
- Runs that never started: 0. The tool reports the suite as complete.
- Runs that ended with an error: 0.
- Traces missing: 0 of 60.

