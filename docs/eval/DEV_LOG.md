# Development log

What each development run showed and what was changed because of it. The
development cases (`plugins/dataset-scout/evals/dev-*`) were visible while the
skill was written, so nothing here supports a claim; the claim rests on the
sealed held-out run (`docs/EVAL_PROTOCOL.md`). The log is kept so that the path
to the frozen skill can be checked.

All runs: Sonnet 5.5 for the answers, Sonnet as the judge, fresh isolated
sessions through `claude plugin eval`, identical tools in every arm.

## Probe before any run (2026-11-11)

One question, two runs without the skill. The model answered from memory in a
single turn, used no tool, gave no link, and wrote that it had not checked the
licences. Cost about $0.07, about 40 seconds. This is why a third arm ("no
skill, told to verify") was added to the protocol.

## Run 01 (2026-11-12): skill version 1, one run per arm

Files: `eval-runs/dev-01/`, `eval-runs/dev-01-prompted/`.

| | Health (2 cases) | Other fields (2 cases) | Links per answer | Links that resolve | Cost per answer | Time per answer |
|---|---|---|---|---|---|---|
| With the skill (v1) | 0.84 | 0.74 | 8.5 | 33 of 34 | $0.35 | 4.1 min |
| No skill | 0.95 | 0.63 | 0 | none given | $0.06 | 0.4 min |
| No skill, told to verify | 0.84 | 0.68 | 12.2 | 45 of 49 | $0.44 | 1.3 min |

Score is the share of content graders passed, averaged over cases. Cost and time
are those of the answer, judging excluded.

Overall the skill and the plain baseline tied (0.79 against 0.79). The skill
triggered in 4 of 4 runs and no run read an evaluation file.

**What went wrong.** Reading the answers showed one pattern behind almost every
grader the skill lost:

- When an access page could not be read, the skill wrote "Not confirmed" where
  the baseline stated the access process from memory, correctly.
- A dataset the model knew was left out of one answer because the registry
  search did not return it and memory was never consulted.
- A dataset found only as a third-party copy was moved to "what I could not
  find" instead of being listed.

The arm that was only told to verify lost the same ground on the health cases.
Once the model starts researching, it reports what it confirmed and drops what
it remembers.

**What was changed (skill version 2).**

- The answer keeps everything the model knows and marks each fact as confirmed
  today or recalled. "Not confirmed" alone is no longer an allowed entry.
- Memory is the first of four routes for collecting candidates.
- A fitting dataset stays in the answer whether or not it verified, under
  "Known, not confirmed".
- Access facts are worked down a ladder: registry record, the landing page
  through a new `read` command that quotes its sentences about access, the
  agent's own fetch tool, a web search, and finally labelled recall.
- An open release that lacks something a restricted release has is still a
  candidate, described release by release.

These are changes of principle, not of content: no dataset name was added to the
skill.

**Also found.** The evaluation sandbox routes traffic through a local proxy, and
bodies were cut short when the five registries were queried side by side. That
is specific to the sandbox, but it costs the skill arm searches, so the tool now
queries one registry at a time behind a proxy and retries a cut body.

## Independent code review (2026-11-12)

A reviewer agent that had written none of the code found 28 problems, three of
them serious: registry facts leaking between records, repositories that hold
only a loading script reported as open, and an invented name on a real record
address coming back as verified. The review is in
`docs/research/code_review_2026-11-12.md` with the log of fixes.

## Run 02 (2026-11-12): skill version 2, two runs per arm

Files: `eval-runs/dev-02/`. The prompted arm does not depend on the skill, so
its figures are those of run 01 (one run per case).

| | Health (2 cases) | Other fields (2 cases) | Links per answer | Links that resolve | Cost per answer | Time per answer |
|---|---|---|---|---|---|---|
| With the skill (v2) | 0.97 | 0.81 | 11.2 | 88 of 90, none dead, 2 refused the checker | $0.39 | 3.5 min |
| No skill | 0.90 | 0.76 | 0 | none given | $0.07 | 0.5 min |
| No skill, told to verify (run 01) | 0.84 | 0.68 | 12.2 | 45 of 49 | $0.44 | 1.3 min |

The skill was better on three cases, level on one and worse on none. By kind of
check: access facts 0.93 against 0.79 on the health cases and 0.64 against 0.50
on the others; recall 1.00 against 0.94 and 0.88 against 0.88; both arms avoided
every unsuitable famous dataset and both named a less-known one in every run.
The skill triggered in 8 of 8 runs and no run read an evaluation file.

**Checked for inflation.** Version 2 asks for everything that fits, so answers
could simply have grown. They did grow: about 6,500 characters and 6 to 10
shortlist rows, against about 3,400 characters for the baseline. The
unsuitable-dataset check still passed in every run, so the extra rows were not
indiscriminate, but the answers are longer and that is a cost to the reader.

**Still wrong.** 42 registry searches failed inside the evaluation sandbox in
these eight runs, all with bodies cut short behind the sandbox proxy. One
licence that only a code repository states was missed by every arm.

**What was changed.** Nothing in the skill's instructions. The tool was fixed:
the findings of the code review, and one registry at a time with retries when a
proxy is in use.

## Run 03 (2026-11-12): skill version 2 with the review fixes, two runs per arm

Files: `eval-runs/dev-03/`.

| | Health (2 cases) | Other fields (2 cases) | Links per answer | Links that resolve | Cost per answer | Time per answer |
|---|---|---|---|---|---|---|
| With the skill | 0.95 | 0.81 | 9.0 | 68 of 72, 1 dead, 3 refused the checker | $0.40 | 5.5 min |
| No skill | 0.95 | 0.78 | 0 | none given | $0.06 | 0.4 min |

Level. The skill's scores were the same as in run 02 (0.97 and 0.81); the
baseline's moved from 0.90 and 0.76 to 0.95 and 0.78 with nothing changed, which
shows how much two runs of four cases move by chance. No conclusion is drawn
from the difference between runs 02 and 03.

**Still wrong, and not a matter of chance.** 82 registry searches failed inside
the evaluation sandbox, more than in run 02, although the tool now queried one
registry at a time. And in most runs the agent never read an access page or
searched the literature.

**What was found.** A probe run inside the sandbox fetched the same five
addresses with Python's HTTP client and with curl. Python's client received a
cut body in 5 of 12 transfers; curl received every body whole. The cause is the
sandbox's proxy, and the effect was that the skill arm had been answering
largely from memory.

**What was changed.**

- The tool sends requests through curl when a proxy is configured, and falls
  back to curl when Python's client receives a cut body.
- `verify` now prints what the landing page says about access for every dataset
  that needs more than a download, so the sentences reach the agent without a
  separate step.

## Check run (2026-11-12): with the skill only, one run per case

Files: `eval-runs/dev-04-check/`. Purpose: confirm the two changes work, not to
compare arms. Failed registry searches fell from 82 to 2, the time per answer
from 5.5 to 3.3 minutes, and the access sentences appeared in every run. Scores:
0.95 on the health cases and 0.82 on the others, in line with the earlier runs.

The skill was frozen after this run. Development stopped here by the rule set
beforehand (three comparison runs); the two remaining weaknesses seen in the
development answers, a known dataset occasionally left out and access details
that only a separate page states, were left as they are.

## Held-out run 01 (2026-11-12): the measurement

Files: `eval-runs/heldout-01/` (with the skill, no skill),
`eval-runs/heldout-01-prompted/` (no skill, told to search and verify),
`eval-runs/heldout-01-fable/` (three questions on the stronger model). The
numbers are in `docs/eval/heldout_report.md`, which is assembled from those
records; this entry is about how the run went and what it showed besides the
scores.

**How it was run.** From the frozen commit, the three runs one after another
with nothing else running; the commands are in the freeze record of the
protocol. While the first run was in progress, and before any result had been
read, the notes at the end of the protocol were written (how a run without an
answer counts, what the audit covers, how the example page is chosen) and the
analysis tools were extended. None of that touches the skill.

**What the records showed besides the scores.**

- *The page step is skipped in part of the runs.* Those sessions searched the
  registries and usually ran the verifier, then answered in text. Every such
  answer says that the page was not built; none points to a page that does not
  exist. The reasons the answers give are that the registries did not hold that
  field's data, that pages refused automated reading, or that the reply already
  covered it. The skill's "quick pass" section, which allows skipping the page
  for small questions, invites the last one. The development questions never
  showed this: their data sat in the registries the tool searches.
- *The page showed "Unknown" for conditions written in plain words.* When the
  agent corrected an access tier by hand it often wrote "application",
  "restricted", "registered" or "fee". The page knows six tier words and showed
  the rest as "Unknown". The format reference did not list the six words. Fixed
  in 0.1.1, after the evaluation (see `CHANGELOG.md`).
- *Three verdicts are failed judge calls.* The evaluation tool records a fail
  when the call to the judge fails. One fell on the skill arm of the main run;
  two fell on the no-skill arm of the run on the stronger model, during a
  network failure on the evaluating machine, and by themselves made the skill
  look better there. They are counted as recorded, and every report prints the
  outcome with them counted as passes beside it.
- *The example page named by the protocol's rule is the weakest one*: a question
  whose data live in archives the tool does not search, so nothing on the page
  carries a verification stamp, and the page says so. It is shown as the rule
  says, beside the page with the most stamps.

**What was not done.** Nothing was run again, no check was changed, and the
skill's instructions were not touched after the results. The one change to the
plugin after the evaluation (0.1.1) is in the renderer and in the reference page
that describes the shortlist format.

**The run on the stronger model.** All twelve sessions had ended before the
network failure began; only the judging of the last two was delayed by it. On
that model the baseline is no longer a one-turn answer from memory: it searches
and gives links on its own, and an answer with the skill costs several times
more than on the main model. The report gives the figures.
