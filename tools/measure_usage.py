#!/usr/bin/env python3
"""Measure what one answer uses, with and without the skill, across main models and effort levels.

    python3 tools/measure_usage.py <out-dir> [--only sonnet,opus] [--efforts medium,xhigh] [--advisor] [--repeat 3] [--case ho-o-03]

For every (model, effort) pair it runs the same question twice in fresh, non-interactive Claude Code
sessions, once with this plugin added and once without, and records what the session reports about
itself: tokens per model and kind, list-price cost, wall time, turns, tool calls, and the plan's
usage-window utilisation that the stream carries. User-level settings, plugins and MCP servers are
left out, so the plugin is the only difference between the two arms.

With --advisor each main model gets the advisor people pair it with (Sonnet with Opus, Opus with
Fable, Fable with Fable), switched on with the `--advisor` flag of `claude`; the advisor's tokens
appear as a second model in the record.

It can be stopped and started again: a cell that finished without an error is skipped. These are real model
calls that count against the account's usage.

Limits of what this can measure: each cell is a single run of one question, so the figures show the
scale, not a precise average; the usage window is reported in whole percentage points, so one run
is usually below what it can show.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(REPO, "plugins", "dataset-shortlist")
MODELS = ["sonnet", "opus", "fable"]
EFFORTS = ["medium", "xhigh", "max"]
ADVISOR = {"sonnet": "opus", "opus": "fable", "fable": "fable"}   # the pairing people use
BUDGET = {"sonnet": "4", "opus": "10", "fable": "14"}      # ceiling per run, list-price dollars
TIMEOUT = {"sonnet": 1500, "opus": 2100, "fable": 2700}    # seconds


def question(case):
    with open(os.path.join(REPO, "eval-runs", "heldout-01", "result.json"), encoding="utf-8") as handle:
        result = json.load(handle)
    for entry in result["cases"]:
        if entry["name"] == case:
            text = entry.get("promptMarkdown") or ""
            if text.startswith("---"):
                end = text.find("\n---", 3)
                if end >= 0:
                    text = text[end + 4:]
            return " ".join(text.split())
    raise SystemExit("no such case: %s" % case)


def run_cell(out_dir, model, effort, arm, prompt, budget, timeout, advisor=None, repeat=1):
    cell = os.path.join(out_dir, "%s%s_%s_%s%s" % (model, "+" + advisor if advisor else "", effort, arm,
                                                 "_r%d" % repeat if repeat > 1 else ""))
    record = os.path.join(cell, "run.json")
    if os.path.isfile(record):
        with open(record, encoding="utf-8") as handle:
            earlier = json.load(handle)
        if earlier.get("stop") == "success" and not earlier.get("is_error") and not earlier.get("timed_out"):
            return earlier      # a cell that timed out, failed or hit the budget cap is run again
    os.makedirs(cell, exist_ok=True)
    workdir = tempfile.mkdtemp(prefix="usage-")
    command = ["claude", "-p", prompt, "--model", model, "--effort", effort,
               "--setting-sources", "project", "--strict-mcp-config",
               "--permission-mode", "auto", "--permission-prompts", "none",
               "--max-budget-usd", budget, "--no-session-persistence",
               "--output-format", "stream-json", "--verbose"]
    if arm == "with":
        command += ["--plugin-dir", PLUGIN]
    if advisor:
        command += ["--advisor", advisor]
    started = time.time()
    trace_path = os.path.join(cell, "trace.jsonl")
    timed_out = False
    with open(trace_path, "w", encoding="utf-8") as trace, open(os.path.join(cell, "stderr.log"), "w") as errors:
        process = subprocess.Popen(command, cwd=workdir, stdin=subprocess.DEVNULL, stdout=trace, stderr=errors)
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            process.wait()
    seconds = time.time() - started

    result, windows, tools, skill = None, [], {}, False
    with open(trace_path, encoding="utf-8") as trace:
        for line in trace:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            kind = event.get("type")
            if kind == "result":
                result = event
            elif kind == "rate_limit_event":
                info = event.get("rate_limit_info") or {}
                windows.append({name: (value or {}).get("utilization") for name, value in (info.get("unifiedWindows") or {}).items()})
            elif kind == "assistant":
                for block in (event.get("message") or {}).get("content") or []:
                    if block.get("type") == "tool_use":
                        name = block.get("name")
                        tools[name] = tools.get(name, 0) + 1
                        if name == "Skill" and "dataset-shortlist" in str((block.get("input") or {}).get("skill")):
                            skill = True
    usage = {}
    for name, entry in ((result or {}).get("modelUsage") or {}).items():
        usage[name] = {key: entry.get(key) for key in ("inputTokens", "outputTokens", "thinkingTokens", "cacheReadInputTokens",
                                                       "cacheCreationInputTokens", "costUSD")}
    answer = (result or {}).get("result") or ""
    with open(os.path.join(cell, "answer.md"), "w", encoding="utf-8") as handle:
        handle.write(answer + "\n")
    page = os.path.join(workdir, "dataset-shortlist.html")
    if os.path.isfile(page):
        shutil.copyfile(page, os.path.join(cell, "dataset-shortlist.html"))
    summary = {
        "model": model, "advisor": advisor, "effort": effort, "arm": arm, "repeat": repeat, "seconds": round(seconds, 1), "timed_out": timed_out,
        "exit_code": process.returncode, "is_error": (result or {}).get("is_error"), "stop": (result or {}).get("subtype"),
        "turns": (result or {}).get("num_turns"), "cost_usd": (result or {}).get("total_cost_usd"),
        "model_usage": usage, "tools": tools, "tool_calls": sum(tools.values()), "skill_loaded": skill,
        "page_written": os.path.isfile(page), "answer_chars": len(answer), "windows": windows,
        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    with open(record, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=1)
    shutil.rmtree(workdir, ignore_errors=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("out_dir")
    parser.add_argument("--only", default=",".join(MODELS), help="comma-separated models")
    parser.add_argument("--efforts", default=",".join(EFFORTS), help="comma-separated effort levels (ultracode is accepted)")
    parser.add_argument("--case", default="ho-o-03", help="the held-out question to ask")
    parser.add_argument("--advisor", action="store_true", help="pair each main model with its usual advisor")
    parser.add_argument("--repeat", type=int, default=1, help="runs of each cell; the second and later ones are named _r2, _r3")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    prompt = question(args.case)
    with open(os.path.join(args.out_dir, "question.txt"), "w", encoding="utf-8") as handle:
        handle.write(prompt + "\n")
    for model in [m for m in args.only.split(",") if m]:
        advisor = ADVISOR.get(model) if args.advisor else None
        for effort, repeat in [(e, n) for e in args.efforts.split(",") if e for n in range(1, args.repeat + 1)]:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                jobs = {arm: pool.submit(run_cell, args.out_dir, model, effort, arm, prompt, BUDGET.get(model, "8"),
                                         TIMEOUT.get(model, 1800), advisor, repeat) for arm in ("with", "without")}
                done = {arm: job.result() for arm, job in jobs.items()}
            a, b = done["with"], done["without"]
            ratio = (a["cost_usd"] / b["cost_usd"]) if a.get("cost_usd") and b.get("cost_usd") else None
            print("%-12s %-9s with: %5.0fs $%.2f %s | without: %5.0fs $%.2f | usage x%s" % (
                model + ("+" + advisor if advisor else ""), effort, a["seconds"], a.get("cost_usd") or 0, "page" if a.get("page_written") else "no page",
                b["seconds"], b.get("cost_usd") or 0, ("%.1f" % ratio) if ratio else "n/a"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
