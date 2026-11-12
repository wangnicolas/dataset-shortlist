# Cross-model audit of the held-out gold answers

Given to an agent on a different model from the one that built the held-out
cases, before the held-out run. The set stays sealed: the auditor reports
counts only.

## Your job

The folder `<heldout>/` holds
ten evaluation cases (`cases/ho-h-*` and `cases/ho-o-*`) and two files of gold
notes. Another agent built them from published sources. You are the independent
check required by `docs/EVAL_PROTOCOL.md` in the `dataset-shortlist` repository
(read that file first; do not open anything under that repository's `plugins/`
folder).

For every grader of every case:

1. **Re-fetch the source.** Open the official page of the dataset the grader is
   about, today, and confirm that the fact the grader tests is what the page
   says: that the dataset exists, how it is obtained, its licence, or the
   property a trap relies on. Do not rely on the gold notes or on memory.
2. **Check fairness.** Would a careful, correct answer written today by an expert
   pass this grader? A grader fails this test if it demands a detail that is no
   longer true, that the official page does not state, that is one of several
   equally correct ways to put it, or that only an answer copied from the gold
   notes would contain.
3. **Check the question.** It must read like a real researcher's request, state
   or clearly imply at least one must-have requirement, and never mention a
   skill, a tool, an output format or which sites to search.

When something is wrong, fix it in place:

- correct a grader whose fact is out of date or too narrow (keep the format: the
  settings block, then a body that starts with "PASS if" and contains "FAIL if");
- delete a grader that cannot be made fair, and add a replacement only if you can
  ground it in an official page, keeping each case within the protocol's limits
  (3 to 5 recall, 2 to 4 access, at most 1 trap, exactly 1 long-tail);
- never change a question's topic.

Record every change in
`<heldout>/audit_log.md`:
case, grader file, what was wrong, the page that shows it, what you did.

Then run
`/usr/bin/python3 <repo>/tools/check_cases.py <heldout>/cases`
and fix anything it reports.

## What to report

Only: the number of cases and graders checked, the number confirmed unchanged,
corrected, deleted and added, the number of questions reworded, and the
validator's final line. Do not name any topic, question, dataset, registry or
source in your reply; the person reading it must not learn the contents of the
set.
