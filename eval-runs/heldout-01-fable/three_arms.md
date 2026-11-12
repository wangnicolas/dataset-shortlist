# Comparison of the arms

Model: fable. Judge: sonnet. Total list-price cost of these runs: $33.14.

## Score (share of graders passed, mean over cases)

In brackets: the same mean computed from run 1 alone, run 2 alone, and so on.

| Stratum | Cases | With the skill | No skill |
|---|---|---|---|
| health | 2 | 0.97 (1.00, 0.94) | 0.97 (1.00, 0.94) |
| other fields | 1 | 1.00 (1.00, 1.00) | 0.86 (0.86, 0.86) |
| all | 3 | 0.98 (1.00, 0.96) | 0.93 (0.95, 0.91) |

## Pass rate by grader family

| Stratum | Family | With the skill | No skill | Verdicts per arm (checks x runs) |
|---|---|---|---|---|
| health | recall | 1.00 | 1.00 | 14 |
| health | access | 0.92 | 0.92 | 12 |
| health | trap | 1.00 | 1.00 | 2 |
| health | long tail | 1.00 | 1.00 | 4 |
| other fields | recall | 1.00 | 0.67 | 6 |
| other fields | access | 1.00 | 1.00 | 4 |
| other fields | trap | 1.00 | 1.00 | 2 |
| other fields | long tail | 1.00 | 1.00 | 2 |

## Per case

Mean over the runs of the case; in brackets, each run.

| Case | Stratum | With the skill | No skill |
|---|---|---|---|
| ho-h-checkpoint-response-rnaseq | health | 1.00 (1.00, 1.00) | 1.00 (1.00, 1.00) |
| ho-h-cxr-free-text-reports | health | 0.94 (1.00, 0.88) | 0.94 (1.00, 0.88) |
| ho-o-01 | other fields | 1.00 (1.00, 1.00) | 0.86 (0.86, 0.86) |

## Primary outcome and the rule fixed before the run

- With the skill against "No skill", 3 cases: mean case score 0.979 against 0.932, difference +0.048 (by run: +0.048, +0.048). The skill scored higher on 1 cases, the same on 2, lower on 0.
  - health (2 cases): 0.969 against 0.969, difference +0.000.
  - other fields (1 cases): 1.000 against 0.857, difference +0.143.
  - The rule is defined for the 10 held-out cases; with 3 cases no statement is made.

## Links in the final answers (checked by script)

| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |
|---|---|---|---|---|
| With the skill | 25.0 | 145 of 150 (97%) | 1 | 4 |
| No skill | 3.2 | 18 of 19 (95%) | 0 | 1 |

## Cost of an answer (mean per run)

| Arm | Turns | Minutes | List-price cost | Tool calls |
|---|---|---|---|---|
| With the skill | 34.0 | 8.5 | $4.11 | 32.0 |
| No skill | 5.8 | 2.0 | $0.85 | 4.8 |

## Verdicts that are not judgements

2 scored verdict(s) are failed calls to the judge, which the evaluation tool recorded as fails. They are counted above as recorded; nothing was judged again.

- ho-o-01, No skill, run 1, check `03-recall-sf-cabspotting` (grader threw: judge call failed: API Error: No response from API (waited 3m, then 10m on the retry). If a prox)
- ho-o-01, No skill, run 2, check `03-recall-sf-cabspotting` (grader threw: judge call failed: API Error: No response from API (waited 3m, then 10m on the retry). If a prox)

Had they been passes: mean case score 0.979 with the skill against 0.979 without, difference +0.000; higher on 0 cases, the same on 3, lower on 0.

## Checks

- Skill triggered in 6 of 6 with-skill runs.
- Runs that touched evaluation files (invalid): 0
- Runs that ended with an error: 0
- Runs without grader verdicts, scored 0 and kept in every mean: 0
- Runs per arm: With the skill 6, No skill 6.

