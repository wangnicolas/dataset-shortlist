# Evaluation summary

Model: fable. Judge: sonnet. Cases: 7. Total list-price cost: $74.50.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 4 | 0.98 | 0.92 | +0.06 | 2 / 2 / 0 |
| other fields | 3 | 0.96 | 0.84 | +0.12 | 1 / 2 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
|---|---|---|---|---|
| health | recall | 1.00 | 1.00 | 26 |
| health | access | 0.95 | 0.91 | 22 |
| health | trap | 1.00 | 1.00 | 8 |
| health | long tail | 1.00 | 0.62 | 8 |
| other fields | recall | 1.00 | 0.89 | 18 |
| other fields | access | 1.00 | 0.94 | 16 |
| other fields | trap | 1.00 | 1.00 | 6 |
| other fields | long tail | 0.67 | 0.33 | 6 |

## Per case

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| ho-h-derm-skin-tone | health | 1.00 (0.00) | 0.86 (0.14) | +0.14 |
| ho-h-ecg-rhythm-labels | health | 1.00 (0.00) | 0.89 (0.00) | +0.11 |
| ho-h-measured-bp-surveys | health | 0.94 (0.06) | 0.94 (0.06) | +0.00 |
| ho-h-wrist-activity-outcomes | health | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-o-02 | other fields | 0.88 (0.00) | 0.88 (0.00) | +0.00 |
| ho-o-03 | other fields | 1.00 (0.00) | 1.00 (0.00) | +0.00 |
| ho-o-04 | other fields | 1.00 (0.00) | 0.64 (0.07) | +0.36 |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 14 | 21.1 | 264 of 295 (89%) | 11 | 20 |
| without | 14 | 8.4 | 98 of 117 (84%) | 4 | 15 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 26.7 | 432 | $3.66 | 651745 |
| without | 8.4 | 83 | $1.26 | 88485 |

## Checks

- Skill triggered in 14 of 14 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs without grader verdicts, scored 0: 0.
- Runs that never started: 0. The tool reports the suite as complete.
- Runs that ended with an error: 0.
- Traces missing: 0 of 28.

