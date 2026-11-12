#!/usr/bin/env python3
"""Assemble the written report of a held-out evaluation from its run records.

    python3 tools/make_report.py --main eval-runs/heldout-01 \
        [--second eval-runs/heldout-01-fable --second-label "..."] \
        [--trigger eval-runs/trigger-01] [--titles docs/eval/heldout_case_titles.json] \
        --label "..." --out docs/eval/heldout_report.md

The report is the machine-written records put in reading order under plain
headings, with two things computed here: which graders differ between the two
main arms, and how the primary outcome moves when one kind of check is left
out (a look taken after the results, and labelled as such). No number in the
report is typed by hand.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decision_rule import conditions, decide, marking_verdict  # noqa: E402

FAMILY_WORDS = {"recall": "found the suitable datasets", "access": "stated how to obtain them correctly",
                "trap": "avoided the unsuitable famous one", "long tail": "surfaced a less-known fitting dataset"}


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().strip()


def demote(markdown, levels=1):
    """Push the headings of an embedded record down so they sit under the report's own."""
    out = []
    for line in markdown.splitlines():
        if line.startswith("#"):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out)


def per_case_scores(runs, keep):
    rows = {}
    for run in runs:
        if run["arm"] not in ("with", "without"):
            continue
        graders = [g for g in run["graders"] if g["scored"] and keep(g)]
        if not graders:
            continue
        rows.setdefault((run["case"], run["stratum"]), {}).setdefault(run["arm"], []).append(
            sum(g["passed"] for g in graders) / len(graders))
    out = []
    for (case, stratum), arms in sorted(rows.items()):
        out.append({"case": case, "stratum": stratum,
                    "with": sum(arms["with"]) / len(arms["with"]) if arms.get("with") else None,
                    "without": sum(arms["without"]) / len(arms["without"]) if arms.get("without") else None})
    return out


def sensitivity(runs):
    lines = ["| Checks counted | With the skill | No skill | Difference, points | Higher / same / lower | Under the rule |",
             "|---|---|---|---|---|---|"]
    views = [("all (the primary outcome)", lambda g: True)]
    for family, words in FAMILY_WORDS.items():
        views.append(("all except: %s" % words, lambda g, f=family: g["family"] != f))
    for family, words in FAMILY_WORDS.items():
        views.append(("only: %s" % words, lambda g, f=family: g["family"] == f))
    for label, keep in views:
        outcome = decide(per_case_scores(runs, keep))
        if not outcome:
            continue
        lines.append("| %s | %.1f%% | %.1f%% | %+.1f | %d / %d / %d | %s |" % (
            label, 100 * outcome["with"], 100 * outcome["other"], 100 * outcome["mean_diff"], outcome["better"],
            outcome["same"], outcome["worse"], outcome["verdict"]))
    return lines


def differing_graders(runs, titles):
    table = {}
    for run in runs:
        if run["arm"] not in ("with", "without"):
            continue
        for grader in run["graders"]:
            if not grader["scored"]:
                continue
            entry = table.setdefault((run["case"], grader["name"]), {"with": 0, "without": 0, "n_with": 0, "n_without": 0,
                                                                    "family": grader["family"]})
            entry[run["arm"]] += int(grader["passed"])
            entry["n_" + run["arm"]] += 1
    gained, lost, both_fail = [], [], []
    for (case, name), entry in sorted(table.items()):
        row = "| %s | `%s` | %s | %d of %d | %d of %d |" % (titles.get(case, case), name, entry["family"], entry["with"],
                                                          entry["n_with"], entry["without"], entry["n_without"])
        if entry["with"] > entry["without"]:
            gained.append(row)
        elif entry["with"] < entry["without"]:
            lost.append(row)
        elif entry["with"] == 0:
            both_fail.append(row)
    head = ["| Question | Check | Kind | With the skill | No skill |", "|---|---|---|---|---|"]
    lines = ["Checks the skill passed more often (%d):" % len(gained), ""] + head + gained
    lines += ["", "Checks the skill passed less often (%d):" % len(lost), ""] + head + lost
    lines += ["", "Checks neither arm passed in any run (%d):" % len(both_fail), ""] + head + both_fail
    return lines


def judge_agreement(result_paths):
    """How often the three votes of the judge agreed, over every scored check of the given runs."""
    total = unanimous = 0
    for path in result_paths:
        if not os.path.isfile(path):
            continue
        for case in load(path).get("cases", []):
            for runs in (case.get("arms") or {}).values():
                for run in runs or []:
                    for grader in run.get("graders") or []:
                        votes = grader.get("judgeVotes")
                        if not grader.get("scored", True) or grader.get("withOnly") or not isinstance(votes, list) or not votes:
                            continue
                        total += 1
                        unanimous += len(set(bool(v) for v in votes)) == 1
    if not total:
        return ""
    return ("The judge voted three times on each check. Over all the arms of the Sonnet runs its three votes agreed on "
            "%d of %d verdicts (%.1f%%); the other %d were decided two to one. Verdicts whose judge call failed carry no "
            "votes and are not in this count." % (unanimous, total, 100.0 * unanimous / total, total - unanimous))


def judge_failures(result_path):
    """Scored checks whose verdict is not a judgement: the judge call itself failed and the tool recorded a fail."""
    found = []
    if not os.path.isfile(result_path):
        return found
    for case in load(result_path).get("cases", []):
        for arm, runs in (case.get("arms") or {}).items():
            for index, run in enumerate(runs or [], 1):
                for grader in run.get("graders") or []:
                    if not grader.get("scored", True) or grader.get("withOnly"):
                        continue
                    if not isinstance(grader.get("judgeVotes"), list) or not grader.get("judgeVotes"):
                        found.append({"case": case["name"], "arm": arm, "run": index, "grader": grader.get("name"),
                                      "passed": bool(grader.get("passed")),
                                      "explanation": " ".join(str(grader.get("explanation") or "").split())[:120]})
    return found


def with_failures_passed(runs, failures):
    """The run list with the failed judge calls counted as passes instead: the other way the missing verdicts could go."""
    keys = {(f["case"], f["arm"], f["run"], f["grader"]) for f in failures}
    changed = []
    for run in runs:
        graders = [dict(g, passed=True) if (run["case"], run["arm"], run["run"], g["name"]) in keys else g
                   for g in run["graders"]]
        changed.append(dict(run, graders=graders))
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--main", required=True, help="output directory of the main run (with and without the skill)")
    parser.add_argument("--prompted", help="output directory of the prompted arm, for the judge agreement count")
    parser.add_argument("--second", help="output directory of the run on the second model")
    parser.add_argument("--second-label", default="")
    parser.add_argument("--trigger", help="output directory of tools/trigger_test.py")
    parser.add_argument("--titles")
    parser.add_argument("--label", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    titles = load(args.titles) if args.titles and os.path.isfile(args.titles) else {}
    summary = load(os.path.join(args.main, "summary.json"))
    arms = load(os.path.join(args.main, "three_arms.json"))
    outcome = decide(arms["per_case"], "without")
    out = ["# Held-out evaluation: the report", "",
           "%s." % args.label.rstrip("."), "",
           "This file is assembled by `tools/make_report.py` from the records in `%s`; no number in it is typed by hand. "
           "The protocol, written before any result existed, is `docs/EVAL_PROTOCOL.md`." % args.main, "",
           "## 1. The statement under the rule fixed before the run", "",
           "> **%s**" % outcome["statement"], "", conditions(outcome), ""]

    out += ["## 2. The comparison", "", demote(read(os.path.join(args.main, "three_arms.md")), 2), ""]

    agreement = judge_agreement([os.path.join(args.main, "result.json")] +
                                ([os.path.join(args.prompted, "result.json")] if args.prompted else []))
    if agreement:
        out += [agreement, ""]
    failures = judge_failures(os.path.join(args.main, "result.json"))
    if failures:
        other = decide(per_case_scores(with_failures_passed(summary["runs"], failures), lambda g: True))
        out += ["%d of the verdicts of the two main arms %s not a judgement: the call to the judge failed and the "
                "evaluation tool recorded a fail. Under the protocol's note on runs and verdicts they are counted as "
                "they were recorded, and nothing was judged again:" % (len(failures), "is" if len(failures) == 1 else "are"), ""]
        out += ["- `%s`, %s, run %d, check `%s` (%s)" % (
            f["case"], "with the skill" if f["arm"] == "with" else "no skill", f["run"], f["grader"], f["explanation"])
            for f in failures]
        out += ["", "Had %s been a pass instead, the mean difference would be %+.1f points with the skill higher on %d "
                    "questions, the same on %d and lower on %d, and the statement under the rule would be: \"%s\"" % (
                        "it" if len(failures) == 1 else "they", 100 * other["mean_diff"], other["better"], other["same"],
                        other["worse"], other["statement"]), ""]

    out += ["## 3. Which checks differ between the two main arms", "",
            "Each check was judged in three runs per arm.", ""] + differing_graders(summary["runs"], titles) + [""]

    out += ["## 4. A look taken after the results: the outcome with one kind of check left out", "",
            "This table is not part of the rule. It was computed after the result was known, to see where the difference "
            "comes from, and it is descriptive only.", ""] + sensitivity(summary["runs"]) + [""]

    section = 5
    for name, heading in (("pipeline_use.md", "How far the runs with the skill went through the workflow"),
                          ("pages_summary.md", "The pages written during the run"),
                          ("audit_summary.md", "Blind audit of every recommended dataset (the two main arms)")):
        path = os.path.join(args.main, name)
        if os.path.isfile(path):
            out += ["## %d. %s" % (section, heading), "", demote(read(path), 2), ""]
            if name == "audit_summary.md":
                audit = load(os.path.join(args.main, "audit_summary.json"))
                marks = ((audit.get("per_arm") or {}).get("with") or {}).get("by_mark")
                out += ["The skill marks each access statement as confirmed today or recalled. " + marking_verdict(marks)[1], "",
                        "The auditors were ten agents started on the model alias `opus`, which their transcripts name as "
                        "`claude-opus-5-5` (the answers were written by `claude-sonnet-5-5`), one per question, each given a folder with the question and the two answers and nothing else; the record "
                        "of how they were run is in `%s/audit/README.md`. The auditor was not told which arm wrote which "
                        "answer, but the answers differ visibly, so the blinding is by label only." % args.main, "",
                        "The audit and the checks of section 2 measure different things. The audit asks whether what an "
                        "answer says about a dataset is right. The access checks ask whether the answer states the "
                        "particular facts a researcher needs in order to decide. An answer can be right in what it says "
                        "and still leave those facts out.", ""]
            section += 1

    if args.second and os.path.isfile(os.path.join(args.second, "three_arms.md")):
        second = load(os.path.join(args.second, "three_arms.json"))
        second_outcome = decide(second["per_case"], "without")
        out += ["## %d. The same comparison on a stronger model" % section, "",
                "%s. Three of these questions were run as the protocol planned; the other seven were added after the result above was known. The rule was set for the main comparison only, so this is reported as a description." % args.second_label.rstrip("."), ""]
        if second_outcome:
            out += ["Mean case score %.1f%% with the skill and %.1f%% without it (difference %+.1f points); higher on %d "
                    "questions, the same on %d, lower on %d." % (100 * second_outcome["with"], 100 * second_outcome["other"],
                                                                100 * second_outcome["mean_diff"], second_outcome["better"],
                                                                second_outcome["same"], second_outcome["worse"]), ""]
        if second.get("judge_failures"):
            other = (second.get("if_judge_failures_passed") or {}).get("without")
            out += ["%d of this run's verdicts are failed calls to the judge, recorded as fails; the list is in the "
                    "table below.%s" % (len(second["judge_failures"]), (
                        " Counted as passes instead, the scores are %.1f%% with the skill and %.1f%% without it "
                        "(difference %+.1f points)." % (100 * other["with"], 100 * other["other"], 100 * other["mean_diff"]))
                        if other else ""), ""]
        out += [demote(read(os.path.join(args.second, "three_arms.md")), 2), ""]
        section += 1

    if args.trigger and os.path.isfile(os.path.join(args.trigger, "trigger_summary.md")):
        out += ["## %d. Does the skill start when it should" % section, "",
                demote(read(os.path.join(args.trigger, "trigger_summary.md")), 2), ""]
        section += 1

    out += ["## %d. Limits" % section, "",
            "- The answer keys were built by Claude agents from published papers and official pages and re-checked on a "
            "different model. They were not written by human domain experts.",
            "- The judge is a language model; three votes per check, majority wins. Link checks are done by script.",
            "- Several access checks ask for an explicit statement of how the data is obtained. An answer that names a "
            "hosting site without saying whether an application is needed fails such a check.",
            "- Famous datasets are known to every arm from training, so finding those measures little.",
            "- Ten questions is a small sample; the result is descriptive and no significance test is claimed.",
            "- The web changes: access rules and links are those of the day of the run.",
            "- The held-out questions are published with these records, so they are spent. A later version needs a new set.", ""]
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(out).rstrip() + "\n")
    print("report written to %s (%d lines)" % (args.out, len(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
