#!/usr/bin/env python3
"""Put the three arms of docs/EVAL_PROTOCOL.md side by side.

    python3 tools/combine_arms.py <main-run-dir> <prompted-run-dir> [<output.md>]

<main-run-dir> holds the with/without run, <prompted-run-dir> the single-arm run
of the same cases with the "search and verify" sentence added. Both must have
been analysed (summary.json). Prints a Markdown report and writes it, with a
JSON twin, into the main run directory unless another path is given.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decision_rule import decide  # noqa: E402

ARMS = [("with", "With the skill"), ("without", "No skill"), ("prompted", "No skill, told to verify")]
RULE_CASES = 10   # the decision rule of the protocol is defined for the ten held-out cases
FAMILIES = ("recall", "access", "trap", "long tail")


def load_runs(main_dir, prompted_dir):
    with open(os.path.join(main_dir, "summary.json"), encoding="utf-8") as handle:
        main = json.load(handle)
    runs = list(main["runs"])
    meta = {"model": main.get("model"), "judge": main.get("judge"), "cost_usd": main.get("cost_usd") or 0.0}
    if prompted_dir:
        with open(os.path.join(prompted_dir, "summary.json"), encoding="utf-8") as handle:
            prompted = json.load(handle)
        for run in prompted["runs"]:
            if run["arm"] == "with":      # the empty plugin's only arm
                run = dict(run, arm="prompted")
                runs.append(run)
        meta["cost_usd"] += prompted.get("cost_usd") or 0.0
    return runs, meta


def judge_failures(run_dir, arm_name=None):
    """Scored checks whose verdict is not a judgement: the call to the judge failed and the tool recorded a fail."""
    path = os.path.join(run_dir, "result.json")
    found = []
    if not run_dir or not os.path.isfile(path):
        return found
    with open(path, encoding="utf-8") as handle:
        result = json.load(handle)
    for case in result.get("cases", []):
        for arm, runs in (case.get("arms") or {}).items():
            for index, run in enumerate(runs or [], 1):
                for grader in run.get("graders") or []:
                    if not grader.get("scored", True) or grader.get("withOnly"):
                        continue
                    votes = grader.get("judgeVotes")
                    if not isinstance(votes, list) or not votes:
                        found.append({"case": case["name"], "arm": arm_name or arm, "run": index, "grader": grader.get("name"),
                                      "explanation": " ".join(str(grader.get("explanation") or "").split())[:110]})
    return found


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def fmt(value, digits=2):
    return "n/a" if value is None else ("%." + str(digits) + "f") % value


def spread(values, digits=2):
    """The individual run values behind a mean, so the reader sees how much they move."""
    values = [v for v in values if v is not None]
    if len(values) < 2:
        return ""
    return " (" + ", ".join(fmt(v, digits) for v in values) + ")"


def main(argv):
    main_dir = argv[1]
    prompted_dir = argv[2] if len(argv) > 2 and argv[2] != "-" else None
    out_path = argv[3] if len(argv) > 3 else os.path.join(main_dir, "three_arms.md")
    runs, meta = load_runs(main_dir, prompted_dir)
    arms = [(key, label) for key, label in ARMS if any(r["arm"] == key for r in runs)]
    strata = sorted({r["stratum"] for r in runs})

    def select(arm, stratum=None, case=None):
        return [r for r in runs if r["arm"] == arm and (stratum is None or r["stratum"] == stratum)
                and (case is None or r["case"] == case)]

    def case_mean(arm, stratum):
        cases = sorted({r["case"] for r in select(arm, stratum)})
        return mean([mean([r["score"] for r in select(arm, case=c)]) for c in cases]), len(cases)

    def family_rate(arm, family, stratum=None):
        passed = total = 0
        for run in select(arm, stratum):
            for grader in run["graders"]:
                if grader["scored"] and grader["family"] == family:
                    total += 1
                    passed += bool(grader["passed"])
        return (passed / total if total else None), total

    def replicate_means(arm, stratum=None):
        """Mean over cases of the score of run 1, of run 2, ...: how far the headline moves between repeats."""
        indexes = sorted({r["run"] for r in select(arm, stratum)})
        return [mean([r["score"] for r in select(arm, stratum) if r["run"] == i]) for i in indexes]

    report = {"meta": meta, "score": {}, "score_by_run": {}, "families": {}, "family_n": {}, "links": {}, "effort": {},
              "per_case": [], "decision": {}}
    lines = ["# Comparison of the arms", "",
             "Model: %s. Judge: %s. Total list-price cost of these runs: $%s." % (
                 meta["model"], meta["judge"], fmt(meta["cost_usd"])), "",
             "## Score (share of graders passed, mean over cases)", "",
             "In brackets: the same mean computed from run 1 alone, run 2 alone, and so on.", "",
             "| Stratum | Cases | " + " | ".join(label for _, label in arms) + " |",
             "|---|---|" + "---|" * len(arms)]
    for stratum in strata + ["all"]:
        cells, n_cases = [], 0
        for key, _ in arms:
            value, n_cases = case_mean(key, None if stratum == "all" else stratum)
            by_run = replicate_means(key, None if stratum == "all" else stratum)
            if stratum == "all":
                report["score_all"] = dict(report.get("score_all", {}), **{key: value})
            else:
                report["score"].setdefault(stratum, {})[key] = value
            report["score_by_run"].setdefault(stratum, {})[key] = by_run
            cells.append(fmt(value) + spread(by_run))
        lines.append("| %s | %d | %s |" % (stratum, n_cases, " | ".join(cells)))

    lines += ["", "## Pass rate by grader family", "",
              "| Stratum | Family | " + " | ".join(label for _, label in arms) + " | Verdicts per arm (checks x runs) |",
              "|---|---|" + "---|" * len(arms) + "---|"]
    for stratum in strata:
        for family in FAMILIES:
            cells, total = [], 0
            for key, _ in arms:
                rate, n = family_rate(key, family, stratum)
                total = max(total, n)
                report["families"].setdefault("%s / %s" % (stratum, family), {})[key] = rate
                cells.append(fmt(rate))
            report["family_n"]["%s / %s" % (stratum, family)] = total
            if total:
                lines.append("| %s | %s | %s | %d |" % (stratum, family, " | ".join(cells), total))

    lines += ["", "## Per case", "", "Mean over the runs of the case; in brackets, each run.", "",
              "| Case | Stratum | " + " | ".join(label for _, label in arms) + " |",
              "|---|---|" + "---|" * len(arms)]
    for case in sorted({r["case"] for r in runs}):
        stratum = next(r["stratum"] for r in runs if r["case"] == case)
        row = {"case": case, "stratum": stratum, "runs": {}}
        cells = []
        for key, _ in arms:
            selected = sorted(select(key, case=case), key=lambda r: r["run"])
            value = mean([r["score"] for r in selected])
            row[key] = value
            row["runs"][key] = [r["score"] for r in selected]
            cells.append(fmt(value) + spread(row["runs"][key]))
        report["per_case"].append(row)
        lines.append("| %s | %s | %s |" % (case, stratum, " | ".join(cells)))

    # The decision rule of the protocol, applied to the table above.
    lines += ["", "## Primary outcome and the rule fixed before the run", ""]
    for other, label in arms[1:]:
        outcome = decide(report["per_case"], other)
        if not outcome:
            continue
        report["decision"][other] = outcome
        by_run = [a - b for a, b in zip(report["score_by_run"]["all"].get("with", []),
                                        report["score_by_run"]["all"].get(other, []))
                  if a is not None and b is not None]
        outcome["diff_by_run"] = by_run
        lines.append("- With the skill against \"%s\", %d cases: mean case score %s against %s, difference %+.3f%s. "
                     "The skill scored higher on %d cases, the same on %d, lower on %d." % (
                         label, outcome["n"], fmt(outcome["with"], 3), fmt(outcome["other"], 3), outcome["mean_diff"],
                         (" (by run: " + ", ".join("%+.3f" % d for d in by_run) + ")") if len(by_run) > 1 else "",
                         outcome["better"], outcome["same"], outcome["worse"]))
        for name, entry in outcome["by_stratum"].items():
            lines.append("  - %s (%d cases): %s against %s, difference %+.3f." % (
                name, entry["n"], fmt(entry["with"], 3), fmt(entry["other"], 3), entry["diff"]))
        if other == "without":
            if outcome["n"] >= RULE_CASES:
                lines.append("  - **Statement under the rule: %s**" % outcome["statement"])
            else:
                lines.append("  - The rule is defined for the %d held-out cases; with %d cases no statement is made."
                             % (RULE_CASES, outcome["n"]))

    lines += ["", "## Links in the final answers (checked by script)", "",
              "| Arm | Links per answer | Resolving | Dead | Blocked to automated clients |", "|---|---|---|---|---|"]
    for key, label in arms:
        selected = select(key)
        total = sum(r["links"]["total"] for r in selected)
        ok = sum(r["links"]["ok"] for r in selected)
        dead = sum(r["links"]["dead"] for r in selected)
        blocked = sum(r["links"]["blocked"] for r in selected)
        report["links"][key] = {"per_answer": total / len(selected) if selected else None, "total": total,
                                "ok": ok, "dead": dead, "blocked": blocked}
        lines.append("| %s | %s | %s | %d | %d |" % (
            label, fmt(total / len(selected) if selected else None, 1),
            ("%d of %d (%.0f%%)" % (ok, total, 100.0 * ok / total)) if total else "no links given", dead, blocked))

    lines += ["", "## Cost of an answer (mean per run)", "",
              "| Arm | Turns | Minutes | List-price cost | Tool calls |", "|---|---|---|---|---|"]
    for key, label in arms:
        selected = select(key)
        entry = {"turns": mean([r["turns"] for r in selected]),
                 "minutes": (mean([r["seconds"] for r in selected]) or 0) / 60.0 if selected else None,
                 "cost_usd": mean([r["cost_usd"] for r in selected]),
                 "tool_calls": mean([sum((r.get("tools") or {}).values()) for r in selected])}
        report["effort"][key] = entry
        lines.append("| %s | %s | %s | $%s | %s |" % (label, fmt(entry["turns"], 1), fmt(entry["minutes"], 1),
                                                      fmt(entry["cost_usd"]), fmt(entry["tool_calls"], 1)))

    # Verdicts that are failed judge calls: listed, and the primary outcome recomputed with them as passes.
    failures = judge_failures(main_dir) + (judge_failures(prompted_dir, "prompted") if prompted_dir else [])
    report["judge_failures"] = failures
    if failures:
        keys = {(f["case"], f["arm"], f["run"], f["grader"]) for f in failures}
        alternative = []
        for case in sorted({r["case"] for r in runs}):
            row = {"case": case, "stratum": next(r["stratum"] for r in runs if r["case"] == case)}
            for key, _ in arms:
                scores = []
                for r in select(key, case=case):
                    scored = [g for g in r["graders"] if g["scored"]]
                    passed = sum(1 for g in scored if g["passed"] or (r["case"], r["arm"], r["run"], g["name"]) in keys)
                    scores.append(passed / len(scored) if scored else None)
                row[key] = mean(scores)
            alternative.append(row)
        report["if_judge_failures_passed"] = {other: decide(alternative, other) for other, _ in arms[1:]}
        report["if_judge_failures_passed"]["per_case"] = alternative
        lines += ["", "## Verdicts that are not judgements", "",
                  "%d scored verdict(s) are failed calls to the judge, which the evaluation tool recorded as fails. "
                  "They are counted above as recorded; nothing was judged again." % len(failures), ""]
        lines += ["- %s, %s, run %d, check `%s` (%s)" % (f["case"], dict(ARMS).get(f["arm"], f["arm"]), f["run"],
                                                         f["grader"], f["explanation"]) for f in failures]
        other_outcome = report["if_judge_failures_passed"].get("without")
        if other_outcome:
            lines += ["", "Had they been passes: mean case score %s with the skill against %s without, difference %+.3f; "
                          "higher on %d cases, the same on %d, lower on %d%s" % (
                              fmt(other_outcome["with"], 3), fmt(other_outcome["other"], 3), other_outcome["mean_diff"],
                              other_outcome["better"], other_outcome["same"], other_outcome["worse"],
                              ("; statement under the rule: " + other_outcome["statement"])
                              if other_outcome["n"] >= RULE_CASES else ".")]
            prompted_outcome = report["if_judge_failures_passed"].get("prompted")
            if prompted_outcome:
                lines += ["Against the arm told to verify, with them as passes: difference %+.3f; higher on %d cases, the "
                          "same on %d, lower on %d." % (prompted_outcome["mean_diff"], prompted_outcome["better"],
                                                        prompted_outcome["same"], prompted_outcome["worse"])]

    with_runs = select("with")
    invalid = sorted({(r["case"], r["arm"], r["run"]) for r in runs if r.get("eval_reads")})
    errors = [(r["case"], r["arm"], r["run"]) for r in runs if r.get("error")]
    no_verdicts = sorted({(r["case"], r["arm"], r["run"]) for r in runs if r.get("no_verdicts")})
    report["checks"] = {"skill_triggered": sum(r["skill_used"] for r in with_runs), "with_runs": len(with_runs),
                        "invalid_runs": len(invalid), "error_runs": len(errors), "runs_without_verdicts": len(no_verdicts),
                        "runs_per_arm": {key: len(select(key)) for key, _ in arms}}
    lines += ["", "## Checks", "",
              "- Skill triggered in %d of %d with-skill runs." % (sum(r["skill_used"] for r in with_runs), len(with_runs)),
              "- Runs that touched evaluation files (invalid): %d%s" % (
                  len(invalid), "" if not invalid else ": " + ", ".join("%s/%s/%d" % item for item in invalid)),
              "- Runs that ended with an error: %d%s" % (
                  len(errors), "" if not errors else ": " + ", ".join("%s/%s/%d" % item for item in errors)),
              "- Runs without grader verdicts, scored 0 and kept in every mean: %d%s" % (
                  len(no_verdicts), "" if not no_verdicts else ": " + ", ".join("%s/%s/%d" % item for item in no_verdicts)),
              "- Runs per arm: " + ", ".join("%s %d" % (label, len(select(key))) for key, label in arms) + ".", ""]
    text = "\n".join(lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(os.path.splitext(out_path)[0] + ".json", "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    print(text)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv))
