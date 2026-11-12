#!/usr/bin/env python3
"""Turn a `claude plugin eval` result into the numbers docs/EVAL_PROTOCOL.md asks for.

    python3 tools/analyze_eval.py <result.json> <output-dir> [--no-links]

Writes into <output-dir>:
  traces/<case>__<arm>__<n>.jsonl   copies of the run traces (the originals are in temp dirs)
  answers/<case>__<arm>__<n>.md     the final answer of every run
  summary.json, summary.md          scores by stratum and grader family, link validity,
                                    cost, trigger rate and the integrity scan

Standard library only.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts"))
from scoutlib import common  # noqa: E402

URL_RE = re.compile(r"https?://[^\s<>\"'`\)\]\}|]+")
EVAL_PATH_RE = re.compile(r"(^|[/\s\"'])evals(-[a-z0-9]+)?(/|\b)|/graders/|gold_notes|dataset-shortlist-heldout", re.I)
FAMILIES = ("recall", "access", "trap", "long tail")


def family_of(grader_name):
    name = grader_name.lower()
    if "-recall-" in name or name.endswith("-recall"):
        return "recall"
    if "-access-" in name or name.endswith("-access"):
        return "access"
    if "-trap-" in name or name.endswith("-trap"):
        return "trap"
    if "long-tail" in name:
        return "long tail"
    return "other"


def stratum_of(case, root=""):
    text = case.get("promptMarkdown") or ""
    prompt_file = os.path.join(root or "", case.get("dir") or "", "prompt.md")
    if os.path.isfile(prompt_file):
        with open(prompt_file, encoding="utf-8") as handle:
            text = handle.read()
    match = re.search(r"^tags:\s*\[([^\]]*)\]", text, re.M)
    tags = [t.strip() for t in match.group(1).split(",")] if match else []
    if "health" in tags:
        return "health"
    if "other" in tags:
        return "other fields"
    return "untagged"


def read_trace(path):
    """Return final answer, tool counts, skill use, suspicious reads and token usage from a trace."""
    info = {"answer": "", "tools": {}, "skill_used": False, "eval_reads": [], "tokens": None, "found": False}
    if not path or not os.path.isfile(path):
        return info
    info["found"] = True
    last_text = ""
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            kind = event.get("type")
            if kind == "assistant":
                for block in (event.get("message") or {}).get("content") or []:
                    if block.get("type") == "text" and (block.get("text") or "").strip():
                        last_text = block["text"]
                    elif block.get("type") == "tool_use":
                        name = block.get("name") or "?"
                        info["tools"][name] = info["tools"].get(name, 0) + 1
                        payload = json.dumps(block.get("input") or {}, ensure_ascii=False)
                        if name == "Skill" and "dataset-shortlist" in payload:
                            info["skill_used"] = True
                        if name in ("Bash", "Read", "Glob", "Grep") and EVAL_PATH_RE.search(payload):
                            info["eval_reads"].append("%s %s" % (name, payload[:240]))
            elif kind == "result":
                info["answer"] = event.get("result") or ""
                info["answer_cost_usd"] = event.get("total_cost_usd")
                info["answer_seconds"] = (event.get("duration_ms") or 0) / 1000.0 or None
                info["answer_turns"] = event.get("num_turns")
                usage = event.get("usage") or {}
                if usage:
                    info["tokens"] = sum(int(usage.get(k) or 0) for k in (
                        "input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
                    info["output_tokens"] = int(usage.get("output_tokens") or 0)
    if not info["answer"]:
        info["answer"] = last_text
    return info


def extract_urls(text):
    urls = []
    for raw in URL_RE.findall(text or ""):
        url = raw.rstrip(".,;:!?*_")
        if "..." in url or "<" in url or "example." in url:
            continue
        if url not in urls:
            urls.append(url)
    return urls


def check_url(url):
    """ok / dead / blocked (the site refused an automated client, so existence is not known)."""
    try:
        resp = common.http_request(url, method="HEAD", timeout=15, retries=1)
        if resp.status in (403, 405, 406, 501) or resp.status >= 500:
            resp = common.http_request(url, method="GET", timeout=20, retries=1, max_bytes=20000)
    except common.FetchError:
        try:
            resp = common.http_request(url, method="GET", timeout=20, retries=1, max_bytes=20000)
        except common.FetchError as exc:
            return "dead", "no response: %s" % exc.reason[:80]
    if 200 <= resp.status < 300:
        return "ok", str(resp.status)
    if resp.status in (401, 403, 429):
        return "blocked", str(resp.status)
    return "dead", str(resp.status)


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def spread(values):
    values = [v for v in values if v is not None]
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def fmt(value, digits=2):
    return "n/a" if value is None else ("%." + str(digits) + "f") % value


def main(argv):
    result_path, out_dir = argv[1], argv[2]
    check_links = "--no-links" not in argv
    with open(result_path, encoding="utf-8") as handle:
        result = json.load(handle)
    os.makedirs(os.path.join(out_dir, "traces"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "answers"), exist_ok=True)

    runs = []
    for case in result.get("cases", []):
        for arm in ("with", "without"):
            for index, run in enumerate((case.get("arms") or {}).get(arm) or [], 1):
                tag = "%s__%s__%d" % (case["name"], arm, index)
                trace_copy = os.path.join(out_dir, "traces", tag + ".jsonl")
                source = run.get("tracePath")
                if source and os.path.isfile(source) and not os.path.isfile(trace_copy):
                    shutil.copyfile(source, trace_copy)
                info = read_trace(trace_copy)
                with open(os.path.join(out_dir, "answers", tag + ".md"), "w", encoding="utf-8") as handle:
                    handle.write(info["answer"] or "(no answer captured)")
                graders = []
                for grader in run.get("graders") or []:
                    graders.append({"name": grader.get("name"), "passed": bool(grader.get("passed")),
                                    "scored": grader.get("scored", True) and not grader.get("withOnly", False),
                                    "family": family_of(grader.get("name") or "")})
                # A run for which the tool returned no verdicts ended without an answer it could grade.
                # It counts as a run that failed every scored grader; it is never left out of a mean
                # (docs/EVAL_PROTOCOL.md, notes of 2026-11-12).
                no_verdicts = not graders
                if no_verdicts:
                    for definition in case.get("graders") or []:
                        graders.append({"name": definition.get("name"), "passed": False,
                                        "scored": definition.get("type") != "tool_used",
                                        "family": family_of(definition.get("name") or "")})
                scored = [g for g in graders if g["scored"]]
                runs.append({
                    "no_verdicts": no_verdicts,
                    "case": case["name"], "stratum": stratum_of(case, (result.get("suite") or {}).get("root")), "arm": arm, "run": index,
                    "score": (sum(g["passed"] for g in scored) / len(scored)) if scored else None,
                    "graders": graders,
                    # the evaluation tool's figures include the judge; the trace has the answer alone
                    "turns": info.get("answer_turns") or run.get("turns"),
                    "cost_usd": info.get("answer_cost_usd") if info.get("answer_cost_usd") is not None
                    else ((run.get("costUsd") or 0) - (run.get("judgeCostUsd") or 0)),
                    "seconds": info.get("answer_seconds") or run.get("durationSeconds"),
                    "cost_with_judge_usd": run.get("costUsd"), "error": run.get("error"),
                    "tokens": info.get("tokens"), "tools": info["tools"], "skill_used": info["skill_used"],
                    "eval_reads": info["eval_reads"], "trace_found": info["found"],
                    "urls": extract_urls(info["answer"]), "answer_chars": len(info["answer"] or ""),
                })

    link_status = {}
    if check_links:
        unique = sorted({url for run in runs for url in run["urls"]})
        with ThreadPoolExecutor(max_workers=8) as pool:
            for url, status in zip(unique, pool.map(check_url, unique)):
                link_status[url] = status
    for run in runs:
        states = [link_status.get(url, ("unchecked", ""))[0] for url in run["urls"]]
        run["links"] = {"total": len(states), "ok": states.count("ok"), "dead": states.count("dead"),
                        "blocked": states.count("blocked"),
                        "dead_urls": [u for u in run["urls"] if link_status.get(u, ("", ""))[0] == "dead"]}

    def arm_runs(arm, stratum=None, case=None):
        return [r for r in runs if r["arm"] == arm and (stratum is None or r["stratum"] == stratum)
                and (case is None or r["case"] == case)]

    def case_scores(arm, stratum=None):
        cases = sorted({r["case"] for r in arm_runs(arm, stratum)})
        return {c: mean([r["score"] for r in arm_runs(arm, case=c)]) for c in cases}

    def family_rate(arm, family, stratum=None):
        passed = total = 0
        for run in arm_runs(arm, stratum):
            for grader in run["graders"]:
                if grader["scored"] and grader["family"] == family:
                    total += 1
                    passed += grader["passed"]
        return (passed / total if total else None), total

    strata = sorted({r["stratum"] for r in runs})
    summary = {"source": os.path.abspath(result_path), "model": (result.get("suite") or {}).get("modelOverride"),
               "judge": (result.get("suite") or {}).get("judgeModel"), "cost_usd": result.get("costUsd"),
               "n_cases": len(result.get("cases", [])), "strata": {}, "per_case": [], "runs": runs}
    lines = ["# Evaluation summary", "",
             "Model: %s. Judge: %s. Cases: %d. Total list-price cost: $%s." % (
                 summary["model"], summary["judge"], summary["n_cases"], fmt(result.get("costUsd"))), ""]

    lines += ["## Score by stratum (share of scored graders passed, mean over cases)", "",
              "| Stratum | Cases | With skill | Without | Difference | Cases better / same / worse |", "|---|---|---|---|---|---|"]
    for stratum in strata:
        with_scores, without_scores = case_scores("with", stratum), case_scores("without", stratum)
        deltas = [with_scores[c] - without_scores[c] for c in with_scores
                  if with_scores.get(c) is not None and without_scores.get(c) is not None]
        better = sum(d > 1e-9 for d in deltas)
        worse = sum(d < -1e-9 for d in deltas)
        entry = {"cases": len(with_scores), "with": mean(with_scores.values()), "without": mean(without_scores.values()),
                 "delta": mean(deltas), "better": better, "same": len(deltas) - better - worse, "worse": worse}
        summary["strata"][stratum] = entry
        lines.append("| %s | %d | %s | %s | %s | %d / %d / %d |" % (
            stratum, entry["cases"], fmt(entry["with"]), fmt(entry["without"]),
            ("%+.2f" % entry["delta"]) if entry["delta"] is not None else "n/a", better, entry["same"], worse))

    lines += ["", "## Pass rate by grader family", "",
              "| Stratum | Family | With skill | Without | Graders judged per arm |", "|---|---|---|---|---|"]
    summary["families"] = {}
    for stratum in strata:
        for family in FAMILIES:
            with_rate, total = family_rate("with", family, stratum)
            without_rate, _ = family_rate("without", family, stratum)
            if total:
                summary["families"]["%s / %s" % (stratum, family)] = {"with": with_rate, "without": without_rate, "n": total}
                lines.append("| %s | %s | %s | %s | %d |" % (stratum, family, fmt(with_rate), fmt(without_rate), total))

    lines += ["", "## Per case", "",
              "| Case | Stratum | With (mean, spread) | Without (mean, spread) | Difference |", "|---|---|---|---|---|"]
    for case in sorted({r["case"] for r in runs}):
        with_values = [r["score"] for r in arm_runs("with", case=case)]
        without_values = [r["score"] for r in arm_runs("without", case=case)]
        stratum = next(r["stratum"] for r in runs if r["case"] == case)
        delta = (mean(with_values) - mean(without_values)) if mean(with_values) is not None and mean(without_values) is not None else None
        summary["per_case"].append({"case": case, "stratum": stratum, "with": mean(with_values),
                                    "without": mean(without_values), "delta": delta})
        lines.append("| %s | %s | %s (%s) | %s (%s) | %s |" % (
            case, stratum, fmt(mean(with_values)), fmt(spread(with_values)), fmt(mean(without_values)),
            fmt(spread(without_values)), ("%+.2f" % delta) if delta is not None else "n/a"))

    lines += ["", "## Links in the final answers (checked by script)", "",
              "| Arm | Runs | Links per answer | Resolving | Dead | Blocked to automated clients |", "|---|---|---|---|---|---|"]
    summary["links"] = {}
    for arm in ("with", "without"):
        selected = arm_runs(arm)
        total = sum(r["links"]["total"] for r in selected)
        ok = sum(r["links"]["ok"] for r in selected)
        dead = sum(r["links"]["dead"] for r in selected)
        blocked = sum(r["links"]["blocked"] for r in selected)
        summary["links"][arm] = {"total": total, "ok": ok, "dead": dead, "blocked": blocked}
        lines.append("| %s | %d | %s | %s | %d | %d |" % (
            arm, len(selected), fmt(total / len(selected) if selected else None, 1),
            ("%d of %d (%.0f%%)" % (ok, total, 100.0 * ok / total)) if total else "n/a", dead, blocked))

    lines += ["", "## Cost of an answer, judging excluded (mean per run)", "",
              "| Arm | Turns | Seconds | List-price cost | Tokens (all kinds) |", "|---|---|---|---|---|"]
    summary["effort"] = {}
    for arm in ("with", "without"):
        selected = arm_runs(arm)
        entry = {"turns": mean([r["turns"] for r in selected]), "seconds": mean([r["seconds"] for r in selected]),
                 "cost_usd": mean([r["cost_usd"] for r in selected]), "tokens": mean([r["tokens"] for r in selected])}
        summary["effort"][arm] = entry
        lines.append("| %s | %s | %s | $%s | %s |" % (arm, fmt(entry["turns"], 1), fmt(entry["seconds"], 0),
                                                     fmt(entry["cost_usd"]), fmt(entry["tokens"], 0)))

    with_runs = arm_runs("with")
    triggered = sum(r["skill_used"] for r in with_runs)
    without_verdicts = [(r["case"], r["arm"], r["run"]) for r in runs if r.get("no_verdicts")]
    expected = {}
    # The command line can ask for fewer runs than a case's own default, and the result file does not
    # record that, so the number asked for is taken as the largest number any case and arm was run.
    wanted = max([len(runs_of_arm or []) for case in result.get("cases", [])
                  for runs_of_arm in (case.get("arms") or {}).values()] or [0])
    for case in result.get("cases", []):
        for arm in ("with", "without"):
            started = len((case.get("arms") or {}).get(arm) or [])
            if (case.get("arms") or {}).get(arm) is not None and started < wanted:
                expected["%s/%s" % (case["name"], arm)] = wanted - started
    summary["runs_without_verdicts"] = without_verdicts
    summary["runs_never_started"] = expected
    summary["partial"] = bool(result.get("partial"))
    suspicious = [(r["case"], r["arm"], r["run"], item) for r in runs for item in r["eval_reads"]]
    errors = [(r["case"], r["arm"], r["run"], r["error"]) for r in runs if r["error"]]
    missing = sum(not r["trace_found"] for r in runs)
    summary["trigger_rate"] = (triggered / len(with_runs)) if with_runs else None
    summary["suspicious_reads"] = suspicious
    summary["run_errors"] = errors
    lines += ["", "## Checks", "",
              "- Skill triggered in %d of %d with-skill runs." % (triggered, len(with_runs)),
              "- Runs that touched evaluation files: %d.%s" % (
                  len({s[:3] for s in suspicious}), "" if not suspicious else " THESE RUNS ARE INVALID: " + "; ".join(
                      "%s/%s/%d" % s[:3] for s in sorted({s[:3] for s in suspicious}))),
              "- Runs without grader verdicts, scored 0: %d%s" % (
                  len(without_verdicts), "." if not without_verdicts else ": " + ", ".join(
                      "%s/%s/%d" % item for item in without_verdicts) + "."),
              "- Runs that never started: %d%s The tool reports the suite as %s." % (
                  sum(expected.values()), "." if not expected else " (" + ", ".join(
                      "%s: %d" % item for item in sorted(expected.items())) + ").",
                  "partial" if result.get("partial") else "complete"),
              "- Runs that ended with an error: %d.%s" % (len(errors), "" if not errors else " " + "; ".join(
                  "%s/%s/%d: %s" % (c, a, n, str(e)[:80]) for c, a, n, e in errors)),
              "- Traces missing: %d of %d." % (missing, len(runs)), ""]

    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv))
