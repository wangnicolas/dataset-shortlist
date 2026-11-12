# Evaluation summary

Model: sonnet. Judge: sonnet. Cases: 4. Total list-price cost: $2.87.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 2 | 0.84 | n/a | n/a | 0 / 0 / 0 |
| other fields | 2 | 0.68 | n/a | n/a | 0 / 0 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
|---|---|---|---|---|
| health | recall | 0.89 | n/a | 9 |
| health | access | 0.86 | n/a | 7 |
| health | trap | 1.00 | n/a | 2 |
| health | long tail | 0.50 | n/a | 2 |
| other fields | recall | 0.62 | n/a | 8 |
| other fields | access | 0.57 | n/a | 7 |
| other fields | trap | 1.00 | n/a | 2 |
| other fields | long tail | 1.00 | n/a | 2 |

## Per case

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| dev-crop-type-sentinel2 | other fields | 0.67 (0.00) | n/a (0.00) | n/a |
| dev-household-load-forecasting | other fields | 0.70 (0.00) | n/a (0.00) | n/a |
| dev-icu-sepsis-early-warning | health | 0.91 (0.00) | n/a (0.00) | n/a |
| dev-parkinsons-voice-audio | health | 0.78 (0.00) | n/a (0.00) | n/a |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 4 | 12.2 | 45 of 49 (92%) | 2 | 2 |
| without | 0 | n/a | n/a | 0 | 0 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 13.5 | 78 | $0.44 | 126549 |
| without | n/a | n/a | $n/a | n/a |

## Checks

- Skill triggered in 0 of 4 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs that ended with an error: 0.
- Traces missing: 0 of 4.

