# How the blind audit was run

Date: 12 November 2026, 05:13 to 05:58 Japan time, after the three held-out runs
had ended.

- **What was audited.** For each of the ten questions, the answer of run 1 of
  the arm with the skill and the answer of run 1 of the arm without it
  (`../answers/<case>__with__1.md`, `../answers/<case>__without__1.md`).
  `tools/audit_packets.py make` wrote them as `answer_A.md` and `answer_B.md`
  in an order drawn from a fixed seed, removed the lines that name the skill's
  own output files, and kept the mapping in `../audit_key.json`.
- **What an auditor saw.** A folder outside this repository holding four files:
  `question.md`, `answer_A.md`, `answer_B.md` and `INSTRUCTIONS.md` (a copy of
  `tools/audit_prompt.md`). The message that started each auditor is
  `tools/audit_dispatch_prompt.txt`, with the folder name filled in. The
  auditors were not given the key, the other runs or this repository.
- **Who audited.** Ten agents started from the evaluating session on the model
  alias `opus`, one per question, at most five at a time. Their transcripts name
  the model as `claude-opus-5-5`; the transcripts themselves stay on the machine
  that ran them. The answers under audit were written by `claude-sonnet-5-5`.
- **What came back.** One `audit.json` per question, checked by script for the
  required fields and values and copied here unchanged. No auditor was asked to
  redo anything.
- **Blinding.** By label only. The two answers of a question differ visibly:
  one carries links and marks what it checked. Three packets also kept a phrase
  about the page or the tool that the cleaning step did not remove.
- **Reading the shares.** `null` means the auditor could not settle the point:
  the official page could not be reached, the answer stated no access condition,
  or the documentation does not say. Such items are left out of that share, and
  the summary prints how many were judged.
