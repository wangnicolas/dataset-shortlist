# Evaluation summary

Model: sonnet. Judge: sonnet. Cases: 4. Total list-price cost: $2.89.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 2 | 0.95 | n/a | n/a | 0 / 0 / 0 |
| other fields | 2 | 0.81 | n/a | n/a | 0 / 0 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
|---|---|---|---|---|
| health | recall | 0.89 | n/a | 9 |
| health | access | 1.00 | n/a | 7 |
| health | trap | 1.00 | n/a | 2 |
| health | long tail | 1.00 | n/a | 2 |
| other fields | recall | 0.75 | n/a | 8 |
| other fields | access | 0.71 | n/a | 7 |
| other fields | trap | 1.00 | n/a | 2 |
| other fields | long tail | 1.00 | n/a | 2 |

## Per case

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| dev-crop-type-sentinel2 | other fields | 0.90 (0.00) | n/a (0.00) | n/a |
| dev-household-load-forecasting | other fields | 0.73 (0.00) | n/a (0.00) | n/a |
| dev-icu-sepsis-early-warning | health | 1.00 (0.00) | n/a (0.00) | n/a |
| dev-parkinsons-voice-audio | health | 0.90 (0.00) | n/a (0.00) | n/a |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 4 | 10.0 | 38 of 40 (95%) | 0 | 2 |
| without | 0 | n/a | n/a | 0 | 0 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 19.5 | 198 | $0.49 | 650524 |
| without | n/a | n/a | $n/a | n/a |

## Checks

- Skill triggered in 4 of 4 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs that ended with an error: 0.
- Traces missing: 0 of 4.

