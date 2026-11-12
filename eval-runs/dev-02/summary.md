# Evaluation summary

Model: sonnet. Judge: sonnet. Cases: 4. Total list-price cost: $7.01.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 2 | 0.97 | 0.90 | +0.07 | 2 / 0 / 0 |
| other fields | 2 | 0.81 | 0.76 | +0.06 | 1 / 1 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
|---|---|---|---|---|
| health | recall | 1.00 | 0.94 | 18 |
| health | access | 0.93 | 0.79 | 14 |
| health | trap | 1.00 | 1.00 | 4 |
| health | long tail | 1.00 | 1.00 | 4 |
| other fields | recall | 0.88 | 0.88 | 16 |
| other fields | access | 0.64 | 0.50 | 14 |
| other fields | trap | 1.00 | 1.00 | 4 |
| other fields | long tail | 1.00 | 1.00 | 4 |

## Per case

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| dev-crop-type-sentinel2 | other fields | 0.78 (0.11) | 0.67 (0.00) | +0.11 |
| dev-household-load-forecasting | other fields | 0.85 (0.05) | 0.85 (0.05) | +0.00 |
| dev-icu-sepsis-early-warning | health | 1.00 (0.00) | 0.91 (0.00) | +0.09 |
| dev-parkinsons-voice-audio | health | 0.94 (0.06) | 0.89 (0.00) | +0.06 |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 8 | 11.2 | 88 of 90 (98%) | 0 | 2 |
| without | 8 | 0.0 | n/a | 0 | 0 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 16.2 | 208 | $0.39 | 426887 |
| without | 1.0 | 27 | $0.07 | 20150 |

## Checks

- Skill triggered in 8 of 8 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs that ended with an error: 0.
- Traces missing: 0 of 16.

