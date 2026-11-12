# Three-arm comparison

Model: sonnet. Judge: sonnet. Total list-price cost of these runs: $9.88.

## Score (share of graders passed, mean over cases)

| Stratum | Cases | With the skill | No skill | No skill, told to verify |
|---|---|---|---|---|
| health | 2 | 0.97 | 0.90 | 0.84 |
| other fields | 2 | 0.81 | 0.76 | 0.68 |

## Pass rate by grader family

| Stratum | Family | With the skill | No skill | No skill, told to verify | Graders per arm |
|---|---|---|---|---|---|
| health | recall | 1.00 | 0.94 | 0.89 | 18 |
| health | access | 0.93 | 0.79 | 0.86 | 14 |
| health | trap | 1.00 | 1.00 | 1.00 | 4 |
| health | long tail | 1.00 | 1.00 | 0.50 | 4 |
| other fields | recall | 0.88 | 0.88 | 0.62 | 16 |
| other fields | access | 0.64 | 0.50 | 0.57 | 14 |
| other fields | trap | 1.00 | 1.00 | 1.00 | 4 |
| other fields | long tail | 1.00 | 1.00 | 1.00 | 4 |

## Per case

| Case | Stratum | With the skill | No skill | No skill, told to verify |
|---|---|---|---|---|
| dev-crop-type-sentinel2 | other fields | 0.78 | 0.67 | 0.67 |
| dev-household-load-forecasting | other fields | 0.85 | 0.85 | 0.70 |
| dev-icu-sepsis-early-warning | health | 1.00 | 0.91 | 0.91 |
| dev-parkinsons-voice-audio | health | 0.94 | 0.89 | 0.78 |

## Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 11.2 | 88 of 90 (98%) | 0 | 2 |
| No skill | 0.0 | no links given | 0 | 0 |
| No skill, told to verify | 12.2 | 45 of 49 (92%) | 2 | 2 |

## Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 16.2 | 3.5 | $0.39 | 14.2 |
| No skill | 1.0 | 0.5 | $0.07 | 0.0 |
| No skill, told to verify | 13.5 | 1.3 | $0.44 | 12.5 |

## Checks

- Skill triggered in 8 of 8 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0

