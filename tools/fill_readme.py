#!/usr/bin/env python3
"""Write the results block of README.md from the evaluation records.

    python3 tools/fill_readme.py --arms eval-runs/heldout-01/three_arms.json \
        --label "Ten sealed questions, Sonnet 5.5, three runs per arm, 12 November 2026" \
        [--audit eval-runs/heldout-01/audit_summary.json] \
        [--second eval-runs/heldout-01-fable/three_arms.json --second-label "..."] \
        [--records eval-runs/heldout-01] [--readme README.md]

Everything between the two RESULTS markers in the README is replaced. Every
number comes from the JSON files named on the command line, and the sentence
about the outcome comes from tools/decision_rule.py, so the README cannot drift
from the run records.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decision_rule import conditions, decide, marking_verdict  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = "<!-- RESULTS:START"
END = "<!-- RESULTS:END -->"
ARMS = [("with", "With the skill"), ("without", "No skill"), ("prompted", "No skill, told to verify")]
FAMILIES = [("recall", "Found the suitable datasets"),
            ("access", "Stated how to obtain them correctly"),
            ("trap", "Avoided the unsuitable famous one"),
            ("long tail", "Surfaced a less-known fitting dataset")]
LIMITS = [
    "The answer keys were built by Claude agents from published papers and official pages and re-checked on a "
    "different model. They were not written by human domain experts.",
    "The judge is a language model. Link checks are done by script.",
    "Famous datasets are known to every arm from training, so finding those measures little.",
    "Several access checks ask for an explicit statement of how the data is obtained. An answer that names a hosting "
    "site without saying whether an application is needed fails such a check.",
    "Ten questions is a small sample; the result is descriptive and no significance test is claimed.",
    "The web changes: access rules and links are those of the day of the run.",
]


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def pct(value, digits=0):
    return "n/a" if value is None else ("%." + str(digits) + "f%%") % (100.0 * value)


def points(value, digits=1):
    text = ("%+." + str(digits) + "f") % (100.0 * value)
    if float(text) == 0:
        text = text.lstrip("+-")
    return text.replace("-", "\u2212")


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return lines


def pooled_family(arms, family, key):
    """A family's pass rate over all strata, weighted by the number of graders in each."""
    passed = total = 0.0
    for name, entry in (arms.get("families") or {}).items():
        if not name.endswith("/ " + family) or entry.get(key) is None:
            continue
        n = (arms.get("family_n") or {}).get(name) or 0
        passed += entry[key] * n
        total += n
    return (passed / total) if total else None


def failed_judge_note(data):
    """One sentence about verdicts that are failed judge calls, with the outcome had they been passes."""
    failures = data.get("judge_failures") or []
    if not failures:
        return ""
    other = (data.get("if_judge_failures_passed") or {}).get("without")
    arms_hit = sorted({ARM_WORDS.get(f["arm"], f["arm"]) for f in failures})
    text = ("%d of the verdicts %s, recorded by the evaluation tool as %s (%s). "
            "Nothing was judged again." % (len(failures), "is a failed call to the judge" if len(failures) == 1
                                           else "are failed calls to the judge", "a fail" if len(failures) == 1 else "fails",
                                           "; ".join(
                "%d in the arm %s" % (sum(1 for f in failures if ARM_WORDS.get(f["arm"], f["arm"]) == arm), arm)
                for arm in arms_hit)))
    if other:
        text += (" Counted as %s instead, the scores are %s with the skill and %s without it (difference %s points; "
                 "higher on %d questions, the same on %d, lower on %d)." % (
                     "a pass" if len(failures) == 1 else "passes", pct(other["with"], 1), pct(other["other"], 1),
                     points(other["mean_diff"]), other["better"], other["same"], other["worse"]))
    prompted = (data.get("if_judge_failures_passed") or {}).get("prompted")
    if prompted:
        text += (" Against the arm told to verify the difference would then be %s points (higher on %d, the same on %d, "
                 "lower on %d)." % (points(prompted["mean_diff"]), prompted["better"], prompted["same"], prompted["worse"]))
    return text


ARM_WORDS = {"with": "with the skill", "without": "without the skill", "prompted": "told to verify"}


def results_block(arms, label, audit=None, second=None, second_label="", records="", pipeline=None, titles=None,
                  trigger=None):
    titles = titles or {}
    present = [(key, name) for key, name in ARMS if any(key in scores for scores in arms.get("score", {}).values())]
    per_case = arms.get("per_case", [])
    main = decide(per_case, "without")
    out = []
    if main:
        by_run = ((arms.get("decision") or {}).get("without") or {}).get("diff_by_run") or []
        out += ["**Result.** %s. By the rule fixed before the run:" % label.rstrip("."), "",
                "> **%s**" % main["statement"], "",
                conditions(main), "",
                "Mean case score %s with the skill and %s without it, a difference of %s points%s. The skill scored higher "
                "on %d of the %d questions, the same on %d and lower on %d." % (
                    pct(main["with"], 1), pct(main["other"], 1), points(main["mean_diff"]),
                    (" (each repeat on its own: " + ", ".join(points(d) for d in by_run) + ")") if len(by_run) > 1 else "",
                    main["better"], main["n"], main["same"], main["worse"]), ""]
        note = failed_judge_note(arms)
        if note:
            out += [note, ""]
        prompted = decide(per_case, "prompted")
        if prompted:
            out += ["Against Claude without the skill but told to search the web and verify: %s with the skill and %s "
                    "without, a difference of %s points; higher on %d questions, the same on %d, lower on %d." % (
                        pct(prompted["with"], 1), pct(prompted["other"], 1), points(prompted["mean_diff"]),
                        prompted["better"], prompted["same"], prompted["worse"]), ""]

    # one table: content per stratum, then links, time and cost
    rows = []
    counts = {}
    for row in per_case:
        counts[row["stratum"]] = counts.get(row["stratum"], 0) + 1
    for stratum, scores in arms.get("score", {}).items():
        rows.append(["Mean case score: %s (%d questions)" % (stratum, counts.get(stratum, 0))]
                    + [pct(scores.get(key)) for key, _ in present])
    links, effort = arms.get("links", {}), arms.get("effort", {})
    rows.append(["Links per answer"] + ["n/a" if links.get(k, {}).get("per_answer") is None
                                        else "%.1f" % links[k]["per_answer"] for k, _ in present])
    rows.append(["Links that resolve"] + [("%d of %d" % (links[k].get("ok", 0), links[k]["total"]))
                                          if links.get(k, {}).get("total") else "none given" for k, _ in present])
    rows.append(["Dead links"] + [str(links.get(k, {}).get("dead", 0)) for k, _ in present])
    rows.append(["Time per answer"] + ["n/a" if effort.get(k, {}).get("minutes") is None
                                       else "%.1f min" % effort[k]["minutes"] for k, _ in present])
    rows.append(["List-price cost per answer"] + ["n/a" if effort.get(k, {}).get("cost_usd") is None
                                                  else "$%.2f" % effort[k]["cost_usd"] for k, _ in present])
    out += table([""] + [name for _, name in present], rows) + [""]
    out += ["A case score is the share of a question's content checks that passed, averaged over its runs. Differences "
            "are computed before rounding, so they can differ by a tenth from the difference of the rounded figures. "
            "Dates are in Japan time.", ""]

    # by kind of check
    strata = list(arms.get("score", {}).keys())
    rows = []
    for fam_key, fam_label in FAMILIES:
        for stratum in strata:
            entry = arms.get("families", {}).get("%s / %s" % (stratum, fam_key))
            if entry:
                rows.append([fam_label, stratum] + [pct(entry.get(key)) for key, _ in present])
    if rows:
        out += ["By kind of check (share passed):", ""] + table(["Check", "Questions"] + [name for _, name in present], rows) + [""]

    if arms.get("family_n"):
        parts = []
        for fam_key, words in (("access", "access conditions stated correctly"),
                               ("long tail", "a less-known fitting dataset surfaced"),
                               ("recall", "the suitable well-known datasets found"),
                               ("trap", "the unsuitable famous dataset avoided")):
            a, b = pooled_family(arms, fam_key, "with"), pooled_family(arms, fam_key, "without")
            if a is not None and b is not None:
                parts.append("%s %s with the skill against %s without" % (words, pct(a), pct(b)))
        if parts:
            out += ["Pooled over all questions: " + "; ".join(parts) + ".", ""]

    if pipeline and pipeline.get("runs"):
        used = pipeline.get("used") or {}
        text = ("How far the %d with-skill runs went through the workflow: registry search %d, literature search %d, "
                "verifier %d, interactive page %d." % (pipeline["runs"], used.get("search", 0), used.get("papers", 0),
                                                       used.get("verify", 0), used.get("render", 0)))
        if "pages_written" in pipeline:
            missing = pipeline["runs"] - pipeline["pages_written"]
            false_claims = len(pipeline.get("answers_pointing_to_a_missing_page") or [])
            silent = len(pipeline.get("no_page_and_not_said") or [])
            if missing:
                text += (" In the %d runs without a page, %d answers say that it was not built and %d point to a page "
                         "that does not exist." % (missing, missing - silent - false_claims, false_claims))
        out += [text, ""]

    if audit and audit.get("per_arm"):
        rows = []
        for key, name in present:
            entry = audit["per_arm"].get(key)
            if entry:
                def cell(share, right, judged):
                    if entry.get(judged) is None:
                        return pct(entry.get(share))
                    return "%s (%d of %d)" % (pct(entry.get(share)), entry.get(right, 0), entry[judged])
                rows.append([name, entry.get("n", 0), cell("exists", "exists_true", "exists_judged"),
                             cell("access_correct", "access_true", "access_judged"),
                             cell("meets_must_haves", "fit_true", "fit_judged")])
        if rows:
            out += ["Blind audit of the two main arms. For one answer per question and arm (the first run), an auditor on "
                    "a different model looked up the official page of every dataset the answer recommends. It was not told "
                    "which arm wrote which answer, but the answers differ visibly, so the blinding is by label only. Each "
                    "share leaves out the items the auditor could not settle (a page that could not be reached, no access "
                    "condition stated, documentation that does not say):", ""]
            out += table(["", "Datasets audited", "Exist as described", "Access stated correctly", "Meet the must-haves"], rows)
            out += [""]
        marks = (audit["per_arm"].get("with") or {}).get("by_mark") or {}
        if marks:
            out += ["The skill marks each access statement as confirmed today or recalled. " + marking_verdict(marks)[1], ""]
        out += ["The audit and the checks measure different things. The audit asks whether what an answer says about a "
                "dataset is right. The access checks ask whether the answer states the particular facts a researcher needs "
                "in order to decide. An answer can be right in what it says and still leave those facts out.", ""]

    if per_case:
        rows = []
        for row in per_case:
            gap = "n/a" if row.get("with") is None or row.get("without") is None else points(row["with"] - row["without"], 0)
            name = ("%s (`%s`)" % (titles[row["case"]], row["case"])) if titles.get(row["case"]) else "`%s`" % row["case"]
            rows.append([name, row["stratum"]] + [pct(row.get(key)) for key, _ in present] + [gap])
        out += ["<details>", "<summary>Every question, including the ones where the skill did not help</summary>", ""]
        out += table(["Question", "Stratum"] + [name for _, name in present] + ["Skill minus no skill, points"], rows)
        out += ["", "</details>", ""]

    extras = second if isinstance(second, list) else ([(second, second_label, "")] if second else [])
    for extra, extra_label, extra_note in extras:
        if not (extra and extra.get("per_case")):
            continue
        outcome = decide(extra["per_case"], "without")
        if not outcome:
            continue
        out += [("On %s: %s with the skill and %s without it, a difference of %s points; higher on "
                 "%d, the same on %d, lower on %d." % (
                     extra_label.rstrip("."), pct(outcome["with"], 1), pct(outcome["other"], 1),
                     points(outcome["mean_diff"]), outcome["better"], outcome["same"], outcome["worse"]))
                + ((" " + extra_note) if extra_note else ""), ""]
        note = failed_judge_note(extra)
        if note:
            out += [note, ""]
        effort, links = extra.get("effort") or {}, extra.get("links") or {}
        if effort.get("with") and effort.get("without"):
            out += ["On that model an answer with the skill took %.1f minutes and $%.2f at list price, against %.1f "
                    "minutes and $%.2f without it, and carried %.1f links against %.1f." % (
                        effort["with"]["minutes"], effort["with"]["cost_usd"], effort["without"]["minutes"],
                        effort["without"]["cost_usd"], (links.get("with") or {}).get("per_answer") or 0,
                        (links.get("without") or {}).get("per_answer") or 0), ""]

    if trigger and trigger.get("should"):
        out += ["Does it start when it should: each of %d requests was sent once to a fresh session with only this plugin "
                "added. The skill started on %d of %d requests that ask for datasets and on %d of %d that do not." % (
                    trigger["should"] + trigger["should_not"], trigger["fired_when_it_should"], trigger["should"],
                    trigger["fired_when_it_should_not"], trigger["should_not"]), ""]

    out += ["What this does not show:", ""] + ["- " + item for item in LIMITS] + [""]
    if records:
        out += ["Run records, with every answer and every grader verdict: [`%s`](%s)." % (records, records), ""]
    return "\n".join(out).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--arms", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--audit")
    parser.add_argument("--second", action="append", default=[], help="three_arms.json of a further model; repeatable")
    parser.add_argument("--second-label", action="append", default=[])
    parser.add_argument("--second-note", action="append", default=[])
    parser.add_argument("--records", default="", help="path of the run records, linked from the README")
    parser.add_argument("--pipeline", help="pipeline_use.json from tools/pipeline_use.py")
    parser.add_argument("--titles", help="JSON object: case name -> short description of the question")
    parser.add_argument("--trigger", help="trigger_summary.json from tools/trigger_test.py")
    parser.add_argument("--readme", default=os.path.join(REPO, "README.md"))
    parser.add_argument("--print", action="store_true", help="print the block instead of writing the README")
    args = parser.parse_args()

    block = results_block(load(args.arms), args.label,
                          load(args.audit) if args.audit and os.path.isfile(args.audit) else None,
                          [(load(path), (args.second_label + [""] * len(args.second))[i],
                            (args.second_note + [""] * len(args.second))[i])
                           for i, path in enumerate(args.second) if os.path.isfile(path)],
                          "", args.records,
                          load(args.pipeline) if args.pipeline and os.path.isfile(args.pipeline) else None,
                          load(args.titles) if args.titles and os.path.isfile(args.titles) else None,
                          load(args.trigger) if args.trigger and os.path.isfile(args.trigger) else None)
    if args.print:
        sys.stdout.write(block)
        return 0
    with open(args.readme, encoding="utf-8") as handle:
        text = handle.read()
    if START not in text or END not in text:
        sys.stderr.write("the README has no RESULTS markers\n")
        return 2
    head = text[:text.index(START)]
    tail = text[text.index(END) + len(END):]
    marker = START + " written by tools/fill_readme.py from the run records; do not edit by hand -->"
    with open(args.readme, "w", encoding="utf-8") as handle:
        handle.write(head + marker + "\n" + block + END + tail)
    print("README results block written (%d lines)" % block.count("\n"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
