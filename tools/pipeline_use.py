#!/usr/bin/env python3
"""How far each with-skill run went through the skill's workflow, read from the traces.

    python3 tools/pipeline_use.py <eval-output-dir>

Counts, for every with-skill run, which commands of the skill's tool were used
(search, papers, verify, read, render, ...), whether web search and page
fetching were used, and, when tools/harvest_pages.py has been run, whether the
answer's statement about the interactive page agrees with what is on disk: an
answer that points to a page that was never written would be a false claim.

Writes pipeline_use.json and pipeline_use.md into the same directory.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

COMMANDS = ("search", "add", "show", "lookup", "read", "verify", "papers", "render")
# the tool is usually called through a shell variable: S=.../scout.py; python3 $S search ...
CALL = re.compile(r"(?:scout\.py|\$\{?[A-Za-z_]+\}?(?:/scripts/scout\.py)?)[\"']?\s+(%s)\b" % "|".join(COMMANDS))
NO_PAGE = re.compile(r"(did not|didn't|did n't|could not|couldn't|no)\b[^.\n]{0,60}(page|dataset-shortlist\.html)|skipped it", re.I)


def read_run(path):
    used = collections.Counter()
    other = collections.Counter()
    references = set()
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") != "assistant":
                continue
            for block in (event.get("message") or {}).get("content") or []:
                if block.get("type") != "tool_use":
                    continue
                tool, given = block.get("name"), block.get("input") or {}
                if tool == "Bash":
                    command = given.get("command", "")
                    for match in CALL.finditer(command):
                        used[match.group(1)] += 1
                    references.update(re.findall(r"references/([a-z\-]+\.md)", command))
                elif tool == "Read":
                    references.update(re.findall(r"references/([a-z\-]+\.md)", given.get("file_path", "")))
                else:
                    other[tool] += 1
    return {"commands": dict(used), "web_search": other["WebSearch"], "web_fetch": other["WebFetch"],
            "skill": other["Skill"] > 0, "references": sorted(references)}


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(__doc__)
        return 2
    out_dir = argv[1]
    traces = os.path.join(out_dir, "traces")
    pages = {}
    pages_path = os.path.join(out_dir, "pages_summary.json")
    if os.path.isfile(pages_path):
        with open(pages_path, encoding="utf-8") as handle:
            pages = {row["run"]: row["page"] for row in json.load(handle)["runs"]}
    rows = []
    for name in sorted(os.listdir(traces)):
        if "__with__" not in name or not name.endswith(".jsonl"):
            continue
        run = name[:-len(".jsonl")]
        row = dict(run=run, **read_run(os.path.join(traces, name)))
        answer_path = os.path.join(out_dir, "answers", run + ".md")
        if pages and os.path.isfile(answer_path):
            with open(answer_path, encoding="utf-8") as handle:
                answer = handle.read()
            row["page_written"] = bool(pages.get(run))
            if row["page_written"]:
                # the phrase search below is only meant for answers of runs that left no page
                row["answer_points_to_page"] = "dataset-shortlist.html" in answer
                row["answer_says_no_page"] = False
            else:
                row["answer_says_no_page"] = bool(NO_PAGE.search(answer))
                row["answer_points_to_page"] = "dataset-shortlist.html" in answer and not row["answer_says_no_page"]
        rows.append(row)

    total = len(rows)
    used = {c: sum(1 for row in rows if row["commands"].get(c)) for c in COMMANDS}
    summary = {"runs": total, "used": used,
               "skill_loaded": sum(row["skill"] for row in rows),
               "web_search": sum(1 for row in rows if row["web_search"]),
               "web_fetch": sum(1 for row in rows if row["web_fetch"]), "rows": rows}
    lines = ["# How far the with-skill runs went through the workflow", "",
             "Read from the traces of %d with-skill runs." % total, "",
             "| Step | Runs that did it |", "|---|---|",
             "| Loaded the skill | %d |" % summary["skill_loaded"]]
    for command, label in (("search", "Searched the registries"), ("papers", "Searched the literature"),
                           ("verify", "Ran the verifier"), ("read", "Read access pages with the tool"),
                           ("add", "Added candidates found elsewhere"), ("render", "Rendered the interactive page")):
        lines.append("| %s (`%s`) | %d |" % (label, command, used[command]))
    lines += ["| Used web search | %d |" % summary["web_search"], "| Fetched pages with the agent's own tool | %d |" % summary["web_fetch"]]
    if pages:
        written = sum(1 for row in rows if row.get("page_written"))
        false_claim = [row["run"] for row in rows if row.get("answer_points_to_page") and not row.get("page_written")]
        silent = [row["run"] for row in rows if not row.get("page_written") and not row.get("answer_says_no_page")]
        summary.update({"pages_written": written, "answers_pointing_to_a_missing_page": false_claim,
                        "no_page_and_not_said": silent})
        lines += ["", "## The interactive page", "",
                  "- Written in %d of %d runs." % (written, total),
                  "- Answers that point to a page that was not written: %d%s" % (
                      len(false_claim), "" if not false_claim else " (" + ", ".join(false_claim) + ")"),
                  "- Runs without a page whose answer does not say so: %d%s" % (
                      len(silent), "" if not silent else " (" + ", ".join(silent) + ")")]
    with open(os.path.join(out_dir, "pipeline_use.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=1)
    text = "\n".join(lines) + "\n"
    with open(os.path.join(out_dir, "pipeline_use.md"), "w", encoding="utf-8") as handle:
        handle.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
