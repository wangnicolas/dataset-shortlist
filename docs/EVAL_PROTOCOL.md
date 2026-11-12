# Evaluation protocol (written before any skill-versus-baseline run)

> **Reading this in the public repository.** The skill was evaluated under its working name `dataset-scout` and
> renamed `dataset-shortlist` afterwards (version 0.1.2, no change in behaviour). The public repository starts from
> a single commit, so the commit hashes quoted below refer to the private development history and cannot be checked
> here; the run records under `eval-runs/` are the ones produced by those commits. Runs added after the first
> held-out run (the trigger test under the new name, Opus 5.5 on the ten questions, and Fable 5.2 on the seven
> questions outside its planned subset) are exploratory and are listed with the changes at the end.

Date: 2026-11-11. This file fixes how the claim is tested before the results exist.
Changes after the first held-out run are listed at the bottom with their date and
reason; a re-run is reported next to the earlier run, never instead of it.

## Claim under test

With the `dataset-scout` skill loaded, a given Claude model answers
dataset-finding questions better than the same model without the skill, on
content a researcher depends on: finding the datasets that suit the question,
stating correctly how each can be obtained, not recommending data that does not
fit, surfacing less famous datasets, and giving links that work.

The claim is always stated together with the model it was measured on.

## Primary outcome and decision rule

Fixed on 2026-11-12, after the first development run and before any held-out
run, so that the headline cannot be chosen after the results are seen.

**Primary outcome.** The case score: the share of a case's scored content graders
that pass, averaged over its runs. The comparison is "with the skill" against
"no skill", on the ten held-out cases, on Sonnet.

**What will be said.**

| Result on the ten held-out cases | Statement |
|---|---|
| Mean difference in case score of +0.05 or more, the skill better on at least 7 cases, and its mean not lower in either stratum | "The skill beats Claude without it on these questions." |
| Mean difference between -0.05 and +0.05 | "On content the skill and Claude without it are level." What differs (links, verified facts, the page) is then reported as secondary, in those words. |
| Mean difference of -0.05 or less | "The skill does worse than Claude without it on content." |
| Anything else | "Mixed", with the per-case table as the result. |

Everything else is secondary and is reported whatever the primary result: the
same comparison against the prompted arm, the breakdown by grader family and by
stratum, link validity, the blind audit, cost and time. With ten cases the
result is descriptive; no significance test is claimed.

**Fable subset.** The three cases are the first two health cases and the first
other-field case in alphabetical order of case name. Two runs per arm, with and
without the skill.

**Conditions of the held-out run.** It starts from a clean working tree at the
frozen commit, with no other evaluation and no agent running, and it is run
once. The runner refuses a held-out directory when the tree has uncommitted
changes.

## Arms

| Arm | What runs |
|---|---|
| with | Claude Code with only the `dataset-scout` plugin loaded |
| without | Claude Code with no plugin (its built-in skills remain) |

Both arms run through `claude plugin eval` (Claude Code 2.1.322): a fresh,
isolated session per run, the same prompt, the same model, the same turn and
time limits, and the same granted tools:

```
--allow-tools Bash Write Edit WebSearch "WebFetch(domain:*)"
```

So the baseline is not a model answering from memory: it has web search, page
fetching and a shell with network access, exactly like the skill arm. This
matters for reading the result, because a memory-only baseline would be far
weaker and would flatter the skill.

`--no-publish` is always passed. Main model: Sonnet 5.5 (`--model sonnet`).
Judge: Sonnet (`--judge-model sonnet`), three votes per grader, majority wins.
A subset of held-out cases is repeated on Fable 5.2 and reported separately,
because the lift may shrink on a stronger model.

### A third arm: the same model, no skill, told to verify

A probe on 2026-11-11 (one question, two runs, before any development or
held-out run) showed what the plain baseline does with these questions: it
answers from memory in a single turn, uses none of its tools, gives no links,
and says so. That is the behaviour a user gets by default, so it stays the main
comparison. It also invites the objection that the skill only makes the model do
its homework. To separate the two, a third arm is run:

| Arm | What runs |
|---|---|
| prompted | Claude Code with no skill; the question is followed by one sentence: "Please search the web rather than answering from memory, and check that each dataset you recommend really exists and how it can be accessed." |

Same model, tools, limits, graders and number of runs as the other arms. It is
reported beside them. If the skill does no better than this arm, the honest
reading is that its value is in making careful behaviour the default and in the
interactive page, not in its registry tooling, and the result will be stated
that way.

## Cases

A case is one question, written the way a researcher would type it: no mention
of a skill, no instruction about output format, no hint about which registries
to use. Each question states or clearly implies at least one must-have
requirement (a label, a population, a modality, an access constraint).

Two sets:

- **Development set** (4 cases: 2 health or biomedical, 2 other fields). Visible
  to the skill author and used to improve the skill.
- **Held-out set** (10 cases: 6 health or biomedical, 4 other fields). Built by
  agents that never see the skill. The skill author does not read these cases or
  their gold answers until the skill commit is frozen and its hash is recorded
  below. The held-out set is run once.

Health and other-field results are reported separately, not pooled.

## Gold answers

Gold is built from published sources and official pages, never from the skill
and never from memory alone. Every gold item carries its source URL and the date
it was checked. Per case:

- **must_find** (3 to 5 datasets): datasets that published work shows are suitable
  for the question. Each needs (a) a paper, review or benchmark that used it for
  this purpose, (b) its official landing page, (c) its access condition and
  licence as stated on the official page, with the sentence quoted.
- **access_facts** (2 to 4): decision-critical statements about how specific
  must_find datasets are obtained, for example "needs credentialing and a signed
  agreement" or "direct download without an account".
- **trap** (0 or 1): a well-known dataset that looks right but fails a stated
  must-have requirement, or cannot be obtained, with the source that shows it.
- **long_tail** (2 to 4): valid, fitting datasets that are clearly less known
  than the must_find ones. Finding any one of them counts.

A gold item whose facts cannot be confirmed on an official page is dropped.

## Graders

All scored graders are `type: llm` on the final message, weight 1, and test
content only. Nothing about format, the HTML page, the JSON file or the skill's
own vocabulary is graded, because only one arm is told to produce those.

| Family | One grader per | Passes when |
|---|---|---|
| recall | must_find dataset | the answer recommends or lists that dataset as a candidate (any version; listed aliases accepted) |
| access | access fact | the answer states that fact about that dataset correctly; an answer that does not mention the dataset fails |
| trap | trap | the answer does not present the trap dataset as meeting the requirement it fails (not mentioning it passes; mentioning it with the limitation passes) |
| long tail | case | the answer recommends at least one of the long_tail datasets |

A `tool_used: Skill` grader is added as an unscored indicator, and the trigger
rate is reported.

Grader file format (exact):

```markdown
---
type: llm
weight: 1
---

PASS if the final answer recommends or lists the "<Dataset name>" dataset (also
known as <aliases>) as a candidate dataset for the user's question, in any
version. FAIL if the answer does not mention it, or mentions it only to say it
is unsuitable.
```

## Measured from the run traces by script (not by the judge)

- **Link validity**: every http(s) URL in the final answer is requested; the
  share that resolves (2xx after redirects) and the number that do not.
- **Datasets recommended**: count of distinct datasets in the final answer.
- **Cost of the answer**: turns, tokens, list-price cost and wall time, per arm,
  taken from the run's own trace so that the judge's cost and time are excluded.
- **Integrity**: every trace is scanned for any read of a path under `evals`;
  a run that read eval files is invalid and is reported as such.

## Blind audit of every recommended dataset

The graders above only look at the gold datasets. To measure precision over
everything an answer recommends, one run per case per arm (run 1) is audited:

- The auditor is an agent on a different model from the one that produced the
  answers. It receives the question and the answer with nothing that reveals the
  arm, and the two answers of a case are given in random order.
- For each dataset the answer recommends, the auditor opens the official page
  and records: does the dataset exist as described; is the access condition the
  answer states correct according to that page; does it meet the must-have
  requirements of the question.
- Reported per arm: the share of recommended datasets that exist, the share
  whose stated access condition is correct, the share that meet the must-haves,
  and the number of datasets per answer.
- The auditor also records how the answer marked each access statement:
  confirmed today, recalled from memory, or not marked. Accuracy is reported for
  each kind separately. If statements marked as confirmed are not more often
  right than those marked as recalled, the marking is decoration and will be
  reported as such (added 2026-11-12 with the second version of the skill, which
  introduced the marking).

This was added on 2026-11-11, before any held-out run, after a survey of prior
work showed that against a baseline with web search the room for improvement is
in precision and in existence and access correctness rather than in recall.

## Runs

| Set | Model | Runs per arm per case |
|---|---|---|
| development | Sonnet | 1 or 2, repeated across skill iterations |
| held-out | Sonnet | 3 |
| held-out subset (3 cases) | Fable | 2 |

## Analysis

- Case score per arm: share of scored graders passed, averaged over runs.
- Headline: mean score with and without, the mean difference, and the per-case
  differences, shown for health and other-field cases separately.
- Breakdown by grader family (recall, access, trap, long tail), since they
  measure different things and an average can hide a loss in one of them.
- Spread across runs is shown for every number. With 10 cases the result is
  descriptive; no significance test is claimed.
- Every run is reported, including cases where the skill is worse.

## Known limits (to be repeated wherever the result is quoted)

- Gold answers are built by Claude agents from published sources, not by human
  domain experts; a second agent on a different model re-checks them.
- The judge is a language model.
- The web changes: access rules and links are date-stamped and may drift.
- Famous datasets are known to both arms from training, so recall of those
  measures little; the access, trap and long-tail families carry most signal.
- Ten held-out questions is a small sample.

## Freeze record

| Item | Value |
|---|---|
| Skill commit frozen for the held-out run | `ef754f46b8795d620ae1f6051094004723da8e39` (committed 2026-11-12 02:34 JST). Later commits change documentation, run records and analysis tools (see the notes below); the plugin directory is identical. |
| Held-out cases copied into the plugin after that commit | 2026-11-12 02:45 JST, with `tools/stage_heldout.sh`, immediately before the main run started (02:45:25 JST) |
| Gold answers | Built by two Opus agents that never opened the plugin; re-checked on Sonnet (78 graders: 77 unchanged, 1 loosened, none deleted) |
| Held-out run commands | `tools/run_eval.sh evals-heldout eval-runs/heldout-01 --model sonnet --runs 3 -j 3 --max-cost-usd 90`; `SCOUT_EVAL_PLUGIN=tools/no-skill-plugin tools/run_eval.sh evals-heldout-prompted eval-runs/heldout-01-prompted --ablation none --model sonnet --runs 3 -j 3 --max-cost-usd 45`; `tools/run_eval.sh evals-heldout-subset eval-runs/heldout-01-fable --model fable --runs 2 -j 2 --max-cost-usd 45` |

## Notes recorded during the first held-out run, before any result was read

Written on 2026-11-12 between 03:00 and 03:20 JST, while the main held-out run
was in progress. At that point only the count of finished runs and the network
log had been looked at; no score, answer or grader verdict of a held-out run.

1. **Runs that end without an answer.** Every run counts; none is dropped and
   none is re-run. When the evaluation tool returns grader verdicts for a run,
   they are used as they are, whatever state the answer was in. When it returns
   none (the session ended in an error, a timeout or the turn limit without an
   answer), the run scores 0 and each of its scored graders counts as failed.
   The analysis script until now left such a run out of the mean, which would
   have favoured the arm that runs longer; it is changed after the main run
   ends and before the next one starts, and the main run is analysed again
   with it. Runs that never started because the cost ceiling stopped the suite
   are reported as missing, not as failed; if a case then has no run in one arm
   the comparison is reported as incomplete instead of a statement under the
   rule.
2. **What "uncommitted changes" means in `run-info.txt`.** The runner writes
   that label when `git status` prints anything. At the start of the main run
   the only entries were untracked: the staged held-out cases
   (`plugins/dataset-scout/evals-heldout*`) and the run records under
   `eval-runs/`, both of which the runner's own check deliberately ignores.
   No tracked file differed from commit `51ffcd6`.
3. **Commits made while the main run was in progress** (02:45 to 03:40 JST):
   the eleven commits from `5c2545c` to `02e554d`, among them the one that adds
   these notes. They change analysis and reporting tools, tests, the README and
   this file. They add: the
   decision rule as one tested module, the per-run values beside every mean,
   the README and page generators, a script that collects the pages written
   during a run, and a trigger test. `git diff ef754f4 HEAD -- plugins/` is
   empty: the skill that is being measured is the frozen one.
4. **Blind audit.** It covers the two main arms (with the skill, no skill). The
   prompted arm is not audited. The auditor is not told which arm wrote which
   answer, but the answers differ visibly (one carries links and marks what it
   checked), so the blinding is by label only and is reported as such.
5. **Example page.** The page shown as the example is the one written in run 1
   of the first held-out case in alphabetical order whose with-skill run wrote
   a page. The verification counts read from the pages are the skill's own
   stamps; the audit is the independent measure.
6. **Order.** The three held-out runs (main, prompted, stronger model) run one
   after another with nothing else running. The audit, the trigger test and
   the acceptance run start only after all three have ended.

## Changes after the first held-out run

The held-out set was run once and nothing was run again. The changes below were
made after its results were known. None of them alters a score.

1. **Version 0.1.1 of the plugin (2026-11-12, after the three runs had ended).**
   The pages collected from the run showed "Unknown" for access conditions the
   sessions had written in plain words ("application", "restricted",
   "registered", "fee"). The renderer now maps such words to their tier and the
   reference page that describes the shortlist format lists the six tier words
   (`CHANGELOG.md`). The graders read the text answer only and never the page,
   so this was not measured again. The measured version is tagged
   `v0.1.0-evaluated`; the pages kept under `eval-runs/heldout-01/pages/` and
   `docs/examples/heldout/` are the ones it wrote, unchanged.
2. **Verdicts that are failed judge calls.** The evaluation tool records a fail
   when the call to the judge itself fails. One verdict of the main run (skill
   arm) and two of the run on the stronger model (no-skill arm, during a network
   failure on the evaluating machine) are of this kind. They are counted as
   recorded, in line with note 1 above, and nothing was judged again. Because
   such a verdict says nothing about the answer, every report now lists them and
   prints the outcome with them counted as passes beside the recorded one. This
   was added after the results were known.
3. **Analysis added after the results** and labelled as such where it is shown:
   the list of checks that differ between the two main arms, the table of the
   outcome with one kind of check left out, the count of how far each run went
   through the workflow, the words found in the access field of the pages, and
   the share of checks on which the judge's three votes agreed.
4. **The analysis script** took the number of runs asked for from each case's
   default, so the run on the stronger model (two runs per arm) was listed as
   having runs that never started. It now takes the number the suite ran.
5. **Local folder names** in the records are replaced by placeholders before the
   records are committed (`tools/scrub_paths.py`).
6. **How the audit was run** is recorded in `eval-runs/heldout-01/audit/README.md`:
   ten auditor agents on Opus 5.5, one per question, each given a folder that
   holds only the question, the two answers and the instructions.
7. **An independent check of the numbers.** A separate agent recomputed every
   number of the README results block and of the report from the raw result
   files with its own scripts and found none that differed. It did find
   sentences that claimed more than the records support (the audit described as
   covering every dataset although a few pages could not be reached, "invented
   datasets and dead links are caught" as an absolute, a statement under the
   rule printed for the three-case subset, labels that named a mean of case
   scores "checks passed"); these were reworded.
8. **Renamed for release (version 0.1.2, 12 November 2026).** The working name
   `dataset-scout` was taken, so the plugin and the skill are now
   `dataset-shortlist`. Nothing the skill does was changed. Because the name is
   part of what the model sees, the trigger test was run again under the new
   name (`eval-runs/trigger-02/`): the skill started on 10 of 10 dataset
   requests and on 0 of 10 near misses, as before. The held-out runs were not
   repeated; their records keep the old name.
9. **More models on the same questions (exploratory).** After the result above
   was known, Opus 5.5 was run on the ten held-out questions and Fable 5.2 on
   the seven that were not in its planned subset, with and without the skill.
   These runs are outside the single held-out run this protocol fixes: the
   questions were no longer unseen by the author, and no rule was set for them
   beforehand. They are reported as a description, with failed judge calls
   counted as recorded and, beside that, as passes. They ran version 0.1.1 of
   the skill; the main run, the prompted arm and the three planned Fable 5.2
   questions ran 0.1.0. A first run of Fable 5.2 without the skill on three of
   those seven questions (`eval-runs/heldout-01-fable-plain3`) is kept beside
   the later one and is not part of its means.
10. **Where the notes are shown (12 November 2026).** To keep the landing page
    short it now carries the chart, one sentence of result and the links. The
    limits are repeated in the README and on the evidence page; the failed
    judge calls are listed there too; which version each run used, when the
    further models were run and the earlier run named in note 9 are recorded
    in the written report (`docs/eval/heldout_report.md`) and in this file
    only. No number changed.
