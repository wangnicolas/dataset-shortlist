# Evaluation summary

Model: sonnet. Judge: sonnet. Cases: 10. Total list-price cost: $18.27.

## Score by stratum (share of scored graders passed, mean over cases)

| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |
|---|---|---|---|---|---|
| health | 6 | 0.88 | n/a | n/a | 0 / 0 / 0 |
| other fields | 4 | 0.79 | n/a | n/a | 0 / 0 / 0 |

## Pass rate by grader family

| Stratum | Family | With skill | Without | Graders judged per arm |
|---|---|---|---|---|
| health | recall | 0.90 | n/a | 60 |
| health | access | 0.82 | n/a | 51 |
| health | trap | 1.00 | n/a | 15 |
| health | long tail | 0.83 | n/a | 18 |
| other fields | recall | 0.83 | n/a | 36 |
| other fields | access | 0.73 | n/a | 30 |
| other fields | trap | 1.00 | n/a | 12 |
| other fields | long tail | 0.58 | n/a | 12 |

## Per case

| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |
|---|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (0.00) | n/a (0.00) | n/a |
| ho-h-cxr-free-text-reports | health | 0.96 (0.06) | n/a (0.00) | n/a |
| ho-h-derm-skin-tone | health | 1.00 (0.00) | n/a (0.00) | n/a |
| ho-h-ecg-rhythm-labels | health | 0.67 (0.00) | n/a (0.00) | n/a |
| ho-h-measured-bp-surveys | health | 0.67 (0.06) | n/a (0.00) | n/a |
| ho-h-wrist-activity-outcomes | health | 1.00 (0.00) | n/a (0.00) | n/a |
| ho-o-01 | other fields | 0.86 (0.12) | n/a (0.00) | n/a |
| ho-o-02 | other fields | 0.88 (0.00) | n/a (0.00) | n/a |
| ho-o-03 | other fields | 0.67 (0.12) | n/a (0.00) | n/a |
| ho-o-04 | other fields | 0.76 (0.24) | n/a (0.00) | n/a |

## Links in the final answers (checked by script)

| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|---|
| with | 30 | 11.3 | 278 of 338 (82%) | 22 | 38 |
| without | 0 | n/a | n/a | 0 | 0 |

## Cost of an answer, judging excluded (mean per run)

| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |
|---|---|---|---|---|
| with | 10.1 | 52 | $0.35 | 102762 |
| without | n/a | n/a | $n/a | n/a |

## Checks

- Skill triggered in 0 of 30 with-skill runs.
- Runs that touched evaluation files: 0.
- Runs without grader verdicts, scored 0: 0.
- Runs that never started: 0. The tool reports the suite as complete.
- Runs that ended with an error: 0.
- Traces missing: 0 of 30.

