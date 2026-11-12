#!/usr/bin/env python3
"""Does the skill start on the requests it should, and stay out of the ones it should not?

    python3 tools/trigger_test.py <out-dir> [--model sonnet] [--only N]

Runs every query of docs/eval/trigger_eval.json once in a fresh, non-interactive
Claude Code session with only this plugin added, and records what the session
does first. The session is stopped as soon as its first tool call or its final
answer arrives, and only the Skill tool is granted, so nothing is searched or
written and a run costs a few cents. These are real, billed model calls.

A run that ends without a tool call and without a final answer is reported as
"no result", not as "did not start".
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def first_action(query, model, log_path, timeout=240):
    """Returns (outcome, detail): outcome is 'skill', 'other-tool', 'answer' or 'no result'."""
    command = ["claude", "-p", query, "--plugin-dir", os.path.join(REPO, "plugins", "dataset-shortlist"),
               "--model", model, "--setting-sources", "project", "--strict-mcp-config",
               "--allowedTools", "Skill", "--permission-prompts", "none",
               "--max-budget-usd", "0.5", "--no-session-persistence",
               "--output-format", "stream-json", "--verbose"]
    workdir = tempfile.mkdtemp(prefix="trigger-")
    started = time.time()
    outcome, detail = "no result", ""
    with open(log_path, "w", encoding="utf-8") as log:
        process = subprocess.Popen(command, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            for line in process.stdout:
                log.write(line)
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get("type") == "assistant":
                    for block in (event.get("message") or {}).get("content") or []:
                        if block.get("type") == "tool_use":
                            name = block.get("name")
                            if name == "Skill":
                                skill = str((block.get("input") or {}).get("skill"))
                                outcome, detail = ("skill", skill) if "dataset-shortlist" in skill else ("other-tool", "Skill:" + skill)
                            else:
                                outcome, detail = "other-tool", str(name)
                            break
                    if outcome != "no result":
                        break
                elif event.get("type") == "result":
                    outcome, detail = "answer", "final answer without a tool call"
                    break
                if time.time() - started > timeout:
                    detail = "timed out"
                    break
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
    return outcome, detail


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("out_dir")
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--only", type=int, help="run only the first N queries (smoke test)")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(REPO, "docs", "eval", "trigger_eval.json"), encoding="utf-8") as handle:
        queries = json.load(handle)
    if args.only:
        queries = queries[:args.only]
    rows = []
    for index, item in enumerate(queries):
        outcome, detail = first_action(item["query"], args.model, os.path.join(args.out_dir, "q%02d.jsonl" % index))
        rows.append({"id": "q%02d" % index, "query": item["query"], "should_trigger": bool(item["should_trigger"]),
                     "outcome": outcome, "detail": detail, "fired": outcome == "skill"})
        print("%s  should=%s  %s %s" % (rows[-1]["id"], "yes" if item["should_trigger"] else "no ", outcome, detail), flush=True)
    should = [r for r in rows if r["should_trigger"]]
    should_not = [r for r in rows if not r["should_trigger"]]
    no_result = [r["id"] for r in rows if r["outcome"] == "no result"]
    summary = {"model": args.model, "fired_when_it_should": sum(r["fired"] for r in should), "should": len(should),
               "fired_when_it_should_not": sum(r["fired"] for r in should_not), "should_not": len(should_not),
               "no_result": no_result, "rows": rows}
    with open(os.path.join(args.out_dir, "trigger_summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    lines = ["# Trigger test (%s)" % args.model, "",
             "The skill started on %d of %d requests that ask for datasets and on %d of %d requests that do not.%s" % (
                 summary["fired_when_it_should"], summary["should"], summary["fired_when_it_should_not"],
                 summary["should_not"], (" Runs without a result: %s." % ", ".join(no_result)) if no_result else ""),
             "", "| Should start | First action | Request |", "|---|---|---|"]
    for r in rows:
        lines.append("| %s | %s | %s |" % ("yes" if r["should_trigger"] else "no",
                                          "the skill" if r["fired"] else (r["detail"] or r["outcome"]),
                                          r["query"][:110].replace("|", "/")))
    with open(os.path.join(args.out_dir, "trigger_summary.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print("\n".join(lines[:3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
