# Evaluation summary

Model: sonnet. Judge: sonnet. Cases: 4. Total list-price cost: $2.88.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 2 | 0.84 | 0.95 | -0.11 | 0 / 1 / 1 |
| other fields | 2 | 0.74 | 0.63 | +0.11 | 1 / 1 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
|---|---|---|---|---|
| health | recall | 0.89 | 1.00 | 9 |
| health | access | 0.71 | 0.86 | 7 |
| health | trap | 1.00 | 1.00 | 2 |
| health | long tail | 1.00 | 1.00 | 2 |
| other fields | recall | 0.88 | 0.75 | 8 |
| other fields | access | 0.43 | 0.29 | 7 |
| other fields | trap | 1.00 | 1.00 | 2 |
| other fields | long tail | 1.00 | 1.00 | 2 |

## Per case

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| dev-crop-type-sentinel2 | other fields | 0.78 (0.00) | 0.56 (0.00) | +0.22 |
| dev-household-load-forecasting | other fields | 0.70 (0.00) | 0.70 (0.00) | +0.00 |
| dev-icu-sepsis-early-warning | health | 0.91 (0.00) | 0.91 (0.00) | +0.00 |
| dev-parkinsons-voice-audio | health | 0.78 (0.00) | 1.00 (0.00) | -0.22 |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 4 | 8.5 | 33 of 34 (97%) | 1 | 0 |
| without | 4 | 0.0 | n/a | 0 | 0 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 20.2 | 244 | $0.35 | 513247 |
| without | 1.0 | 24 | $0.06 | 19757 |

## Checks

- Skill triggered in 4 of 4 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs that ended with an error: 0.
- Traces missing: 0 of 8.

