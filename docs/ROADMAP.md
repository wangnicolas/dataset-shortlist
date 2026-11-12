# Roadmap: from one skill to an end-to-end research workflow

`dataset-shortlist` is the first stage of a larger plan: a pack of agent skills that
carries a research project from a question to a result a reviewer can trust,
while the researcher does other work. This file records that plan and the design
decisions already taken, so later stages do not start from zero.

## Why start with data

A survey of 23 open-source research-automation projects (2026-11-11,
`research/B_forks_and_oss_landscape.md`) found literature review, experiment
loops and paper writing covered many times over, and dataset selection,
exploratory analysis and feature selection almost uncovered. A second survey of
dataset-discovery tools (`research/F1_dataset_discovery_prior_art.md`) found
search well served and verification, access conditions and fit assessment not.
Data is also where a research project is won or lost, so it is the right place
to be better than a general assistant.

## The stages

| Stage | Skill | Status | What it must guarantee |
|---|---|---|---|
| 1. Find the data | `dataset-shortlist` | built; measured on a held-out set on 12 November 2026 (`eval/heldout_report.md`) | Every dataset exists; access condition and licence come from the source; fit is checked against stated requirements. |
| 2. Define the study | `study-protocol` (planned) | design notes below | The prediction task, cohort, time windows, split and metric are written down and frozen before any modelling. |
| 3. Explore and select features | `explore` (planned) | design notes below | Analysis touches the training split only; every finding has an id that later experiments cite. |
| 4. Run experiments unattended | `sealed-loop` (planned) | design notes below | The agent cannot change the judge, cannot see the held-out set, and keeps a change only when it beats measured noise. |
| 5. Report | `traced-report` (planned) | design notes below | Every number in the report is filled in from the run ledger, never typed. |

## What the evidence says an unattended loop needs

From a review of documented failures of autonomous research agents
(`research/A_failures_and_human_evidence.md`; each row there has a fetched
source):

- Agents fabricate or game results when they can. In MLR-Bench's case study of
  ten tasks run with one coding agent, "in 8 out of 10 tasks ... the reported
  results were based on synthesized or placeholder data rather than actual
  execution", as flagged by the benchmark's own LLM judge
  (https://arxiv.org/abs/2505.19955). METR found reward hacking in 39 of 128
  RE-Bench runs (30.4%) when it inspected anomalously high-scoring runs
  (https://metr.org/blog/2025-06-05-recent-reward-hacking/).
- The original autoresearch `program.md` keeps any drop in validation loss with
  no noise threshold, and its guardrails are instructions that nothing enforces.
- Agents beat humans where the budget is short and the metric is cheap and
  automatic, and lose on long, end-to-end research.

So the honest claim for stage 4 is "a better-than-human hand-tuner on a fixed,
cheap metric", and the design has to make cheating structurally hard rather than
forbidden in prose.

## Design decisions already taken for stages 2 to 5

These were worked out on 2026-11-11 before the project was narrowed to stage 1.

- **Guards live in the harness, not in the prompt.** A hook on file-editing tools
  does not see `sed -i` in a shell. The runner hashes the frozen files and refuses
  to record a result when they changed.
- **Predictions in, score out.** The solution receives training data and
  unlabelled evaluation inputs and returns predictions; the harness holds the
  labels and computes the metric. The solution never prints its own score.
- **A locked held-out set, scored once.** `final` is run by someone other than
  the loop agent; afterwards `run` refuses, so the test score cannot feed back
  into iteration. The gap between validation gain and test gain is reported as
  the optimism of the search.
- **Noise before decisions.** Seed noise is measured on the baseline before any
  keep or discard. A change is kept only when the paired improvement on identical
  folds and seeds exceeds a corrected standard error and the measured noise.
- **An append-only, hash-chained ledger**, with every experiment committed to git
  whether kept or discarded, and a `verify` command that checks ledger, history
  and frozen hashes against each other.
- **Every experiment names its reason**: the exploratory finding or reference
  that motivated it, so "data-first" is visible in the record.
- **For clinical time series**, the harness slices events at the prediction time
  before the solution sees them, splits by patient, and runs an executable
  catalogue of leakage checks.
- **The comparison with human results is registered before the first
  experiment**: task, metric, split, the human reference with its source, the
  keep rule and the experiment cap.

## Candidate tasks for a first stage-4 showcase

From `research/D_showcase_task_candidates.md` and
`research/E1_physionet_access_policy_open_data.md` (both with sources):

- PhysioNet/CinC Challenge 2012, event 1: open data, labels for all three sets
  downloadable, published top-10 scores from the challenge; train on set A, score
  once on set C with the official metric.
- Higgs Boson ML Challenge 2014 and KDD Cup 1998 as non-clinical options with
  published human leaderboards; both carry a high risk that solutions are in
  model training data.
- A prospective forecasting task after the model's training cutoff as the
  contamination-free follow-up.

## Nearer-term work on stage 1

The held-out evaluation (`eval/heldout_report.md`) decides the order. What it
found, and what follows from each finding:

1. **The page is not always written.** Part of the runs searched and verified
   but answered in text only, giving as reasons that the registries did not hold
   that field's data or that the reply already covered it. The skill's own "quick
   pass" section invites this. Next: the page is built for every full question,
   from whatever records exist, including ones added by hand; the quick pass is
   reserved for questions about one named dataset. This changes behaviour, so it
   needs a new held-out set before any claim is made about it.
2. **Fields the five registries do not hold.** Sequence archives, national
   survey portals, statistical offices and company data programmes are where
   verification fell back to web search and where pages carried few stamps.
   Next: adapters for the repositories that publish machine-readable access
   metadata, chosen from the map in `references/repositories-by-field.md`, and
   `verify --url` reading more landing-page patterns.
3. **Words on the page.** Fixed in 0.1.1: access words written by hand are shown
   as their tier instead of "Unknown" (see `CHANGELOG.md`). Still open: in
   sandboxed viewers the download button of the page is blocked, so the copy
   button should come first there.
4. **Time.** An answer takes several minutes. Next: a shorter path when the
   registries answer the question at once, and fewer repeated page reads.
5. **The benchmark.** The ten held-out questions are published with their
   results and are spent. Next: a larger set taken from recent papers, with gold
   labels checked by two human annotators, questions about data published after
   the model's training cutoff, and a memory-only baseline beside the
   web-search baseline.
6. A hosted demo page that replays real runs.
