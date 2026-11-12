# Three-arm comparison

Model: sonnet. Judge: sonnet. Total list-price cost of these runs: $5.75.

## Score (share of graders passed, mean over cases)

| Stratum | Cases | With the skill | No skill | No skill, told to verify |
|---|---|---|---|---|
| health | 2 | 0.84 | 0.95 | 0.84 |
| other fields | 2 | 0.74 | 0.63 | 0.68 |

## Pass rate by grader family

| Stratum | Family | With the skill | No skill | No skill, told to verify | Graders per arm |
|---|---|---|---|---|---|
| health | recall | 0.89 | 1.00 | 0.89 | 9 |
| health | access | 0.71 | 0.86 | 0.86 | 7 |
| health | trap | 1.00 | 1.00 | 1.00 | 2 |
| health | long tail | 1.00 | 1.00 | 0.50 | 2 |
| other fields | recall | 0.88 | 0.75 | 0.62 | 8 |
| other fields | access | 0.43 | 0.29 | 0.57 | 7 |
| other fields | trap | 1.00 | 1.00 | 1.00 | 2 |
| other fields | long tail | 1.00 | 1.00 | 1.00 | 2 |

## Per case

| Case | Stratum | With the skill | No skill | No skill, told to verify |
|---|---|---|---|---|
| dev-crop-type-sentinel2 | other fields | 0.78 | 0.56 | 0.67 |
| dev-household-load-forecasting | other fields | 0.70 | 0.70 | 0.70 |
| dev-icu-sepsis-early-warning | health | 0.91 | 0.91 | 0.91 |
| dev-parkinsons-voice-audio | health | 0.78 | 1.00 | 0.78 |

## Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 8.5 | 33 of 34 (97%) | 1 | 0 |
| No skill | 0.0 | no links given | 0 | 0 |
| No skill, told to verify | 12.2 | 45 of 49 (92%) | 2 | 2 |

## Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 20.2 | 4.1 | $0.35 | 18.2 |
| No skill | 1.0 | 0.4 | $0.06 | 0.0 |
| No skill, told to verify | 13.5 | 1.3 | $0.44 | 12.5 |

## Checks

- Skill triggered in 4 of 4 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0

