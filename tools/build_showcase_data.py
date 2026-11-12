#!/usr/bin/env python3
"""Collect what the showcase page shows into one JSON file, from the run records only.

    python3 tools/build_showcase_data.py [--out docs/assets/showcase.json]

Two parts:

  runs      a few real runs, step by step, for the replay: the question as it was asked, the
            requirements the session wrote down, how many candidate records came from each
            registry, what the verifier said about the records it checked, the shortlist with
            access condition, licence and fit, and what was set aside.
  evidence  the held-out comparison in the form the page draws it: the statement under the
            rule, the ten questions, counts of checks passed by kind, the blind audit, how far
            the runs went through the workflow, the trigger test, time and usage.

Every value is read from files under eval-runs/ (written by the evaluation and by
tools/harvest_pages.py, combine_arms.py, audit_packets.py, pipeline_use.py, trigger_test.py).
Nothing is typed in here except the short labels of the replay tabs.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scoutlib.common import canonical_tier  # noqa: E402
from scoutlib.render import _TIER_LABELS  # noqa: E402
from decision_rule import decide, conditions  # noqa: E402

# The runs replayed on the page. Labels are the only hand-written text; everything else is read.
REPLAYS = [
    {"id": "meetings", "label": "Meeting audio", "base": "eval-runs/heldout-01",
     "run": "ho-o-03__with__2", "page": "examples/heldout/ho-o-03__with__2.html", "origin": "a held-out question"},
    {"id": "payroll", "label": "Employer and employee records", "base": "eval-runs/heldout-01",
     "run": "ho-o-02__with__1", "page": "examples/heldout/ho-o-02__with__1.html", "origin": "a held-out question"},
    {"id": "hard", "label": "A hard case", "base": "eval-runs/heldout-01",
     "run": "ho-h-checkpoint-response-rnaseq__with__1", "page": "examples/heldout/ho-h-checkpoint-response-rnaseq__with__1.html",
     "origin": "a held-out question"},
]
SOURCE_ORDER = ["physionet", "zenodo", "huggingface", "openaire", "datacite", "manual"]
SOURCE_NAMES = {"physionet": "PhysioNet", "zenodo": "Zenodo", "huggingface": "Hugging Face", "openaire": "OpenAIRE",
                "datacite": "DataCite", "manual": "Found elsewhere"}
FAMILIES = [("access", "Says how to get it"), ("long tail", "Finds a less-known one"),
            ("recall", "Finds the well-known ones"), ("trap", "Avoids the wrong famous one")]


def load(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as handle:
        return json.load(handle)


def prompt_text(markdown):
    text = markdown or ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            text = text[end + 4:]
    return " ".join(text.split())


def host_of(url):
    try:
        host = urlparse(url or "").netloc.lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def shorten(text, limit):
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def replay(spec):
    case, _, index = spec["run"].partition("__with__")
    rows = {row["run"]: row for row in load(spec["base"] + "/pages_summary.json")["runs"]}
    row = rows[spec["run"]]
    shortlist = load("%s/pages/%s/shortlist.json" % (spec["base"], spec["run"]))
    result = load(spec["base"] + "/result.json")
    question = next(prompt_text(c.get("promptMarkdown")) for c in result["cases"] if c["name"] == case)
    summary = load(spec["base"] + "/summary.json")
    run = next(r for r in summary["runs"] if r["case"] == case and r["arm"] == "with" and str(r["run"]) == index)

    requirements = [{"id": r.get("id"), "text": shorten(r.get("text"), 110), "must": bool(r.get("must", True))}
                    for r in shortlist.get("requirements") or []]
    by_source = row.get("candidates_by_source") or {}
    sources = [{"key": key, "name": SOURCE_NAMES.get(key, key), "count": by_source[key]}
               for key in SOURCE_ORDER if by_source.get(key)]
    sources += [{"key": key, "name": SOURCE_NAMES.get(key, key), "count": n} for key, n in sorted(by_source.items())
                if key not in SOURCE_ORDER]

    datasets = []
    for entry in shortlist.get("datasets") or []:
        record = entry.get("record") or {}
        access = record.get("access")
        stated = access.get("tier") if isinstance(access, dict) else access
        tier = canonical_tier(stated)[0]
        licence = record.get("licence") or {}
        check = record.get("verification") or {}
        datasets.append({
            "rank": entry.get("rank"), "title": shorten(record.get("title"), 64), "host": host_of(record.get("url")),
            "tier": tier, "tier_label": _TIER_LABELS[tier],
            "licence": shorten(licence.get("id") or licence.get("name") or "", 34) if isinstance(licence, dict) else shorten(licence, 34),
            "fit": entry.get("fit") or "unrated", "time": entry.get("time_to_access") or "unknown",
            "stamped": bool(check.get("verified") and check.get("method") and check.get("checked_at")),
            "req": {key: (value or {}).get("status", "unknown") for key, value in (entry.get("requirements") or {}).items()},
        })
    verify = [{"ok": bool(v.get("verified")), "title": shorten(v.get("title"), 58),
               "source": v.get("source") if v.get("source") in by_source else "manual"}
              for v in row.get("verify_outcomes") or []]
    return {
        "id": spec["id"], "label": spec["label"], "origin": spec["origin"], "page": spec["page"],
        "question": question, "requirements": requirements,
        "queries": [shorten(q, 60) for q in (row.get("candidate_queries") or [])][:8],
        "sources": sources, "candidates": row.get("candidates_total") or sum(s["count"] for s in sources),
        "verify": verify, "verified": sum(1 for v in verify if v["ok"]), "checked": len(verify),
        "datasets": datasets, "stamped": sum(1 for d in datasets if d["stamped"]),
        "set_aside": [{"name": shorten(item.get("name"), 60), "reason": shorten(item.get("reason"), 150)}
                      for item in shortlist.get("not_recommended") or []],
        "gaps": [shorten(g, 150) for g in shortlist.get("gaps") or []],
        "note": shorten(shortlist.get("notes"), 220),
        "seconds": round(run.get("seconds") or 0), "turns": run.get("turns"),
        "tool_calls": sum((run.get("tools") or {}).values()),
    }


def pooled(arms, family, arm):
    passed = total = 0
    for name, entry in (arms.get("families") or {}).items():
        if name.endswith("/ " + family) and entry.get(arm) is not None:
            n = (arms.get("family_n") or {}).get(name) or 0
            passed += int(round(entry[arm] * n))
            total += n
    return {"passed": passed, "total": total}


def evidence():
    arms = load("eval-runs/heldout-01/three_arms.json")
    titles = load("docs/eval/heldout_case_titles.json")
    outcome = decide(arms["per_case"], "without")
    prompted = decide(arms["per_case"], "prompted")
    data = {
        "model": arms["meta"].get("model"), "statement": outcome["statement"], "verdict": outcome["verdict"],
        "conditions": conditions(outcome), "higher": outcome["better"], "same": outcome["same"], "lower": outcome["worse"],
        "needed": outcome["needed_better"], "n": outcome["n"], "with": outcome["with"], "without": outcome["other"],
        "diff": outcome["mean_diff"],
        "cases": [{"case": row["case"], "title": titles.get(row["case"], row["case"]), "stratum": row["stratum"],
                   "with": row.get("with"), "without": row.get("without"), "prompted": row.get("prompted")}
                  for row in arms["per_case"]],
        "families": [dict(key=key, label=label, with_=pooled(arms, key, "with"), without=pooled(arms, key, "without"))
                     for key, label in FAMILIES],
        "judge_failures": len(arms.get("judge_failures") or []),
    }
    for family in data["families"]:
        family["with"] = family.pop("with_")
    # where the long-tail gain sits: the same counts for each stratum
    data["long_tail_by_stratum"] = {}
    for name, entry in (arms.get("families") or {}).items():
        if name.endswith("/ long tail"):
            n = (arms.get("family_n") or {}).get(name) or 0
            data["long_tail_by_stratum"][name.split(" / ")[0]] = {
                "with": {"passed": int(round(entry["with"] * n)), "total": n},
                "without": {"passed": int(round(entry["without"] * n)), "total": n}}
    result = load("eval-runs/heldout-01/result.json")
    data["runs_per_question"] = max(len((case.get("arms") or {}).get("with") or []) for case in result["cases"])
    data["judge"] = arms["meta"].get("judge")
    if prompted:
        data["prompted"] = {"mean": prompted["other"], "diff": prompted["mean_diff"], "higher": prompted["better"],
                            "same": prompted["same"], "lower": prompted["worse"]}
    effort, links = arms.get("effort") or {}, arms.get("links") or {}
    data["effort"] = {arm: {"minutes": (effort.get(arm) or {}).get("minutes"), "cost_usd": (effort.get(arm) or {}).get("cost_usd"),
                            "tool_calls": (effort.get(arm) or {}).get("tool_calls")} for arm in ("with", "without", "prompted")
                      if effort.get(arm)}
    data["links"] = {arm: links.get(arm) for arm in ("with", "without", "prompted") if links.get(arm)}

    path = os.path.join(REPO, "eval-runs/heldout-01/audit_summary.json")
    if os.path.isfile(path):
        audit = load("eval-runs/heldout-01/audit_summary.json")["per_arm"]
        data["audit"] = {arm: {key: audit[arm].get(key) for key in (
            "n", "exists_true", "exists_judged", "access_true", "access_judged", "fit_true", "fit_judged")}
            for arm in ("with", "without") if arm in audit}
        marks = (audit.get("with") or {}).get("by_mark") or {}
        data["marking"] = {mark: {"right": (marks.get(mark) or {}).get("right"), "n": (marks.get(mark) or {}).get("n")}
                           for mark in ("today", "memory")}
    pipeline = load("eval-runs/heldout-01/pipeline_use.json")
    data["workflow"] = {"runs": pipeline["runs"], "pages": pipeline.get("pages_written"),
                        "used": pipeline.get("used"), "false_page_claims": len(pipeline.get("answers_pointing_to_a_missing_page") or [])}
    path = os.path.join(REPO, "eval-runs/trigger-01/trigger_summary.json")
    if os.path.isfile(path):
        trigger = load("eval-runs/trigger-01/trigger_summary.json")
        data["trigger"] = {key: trigger[key] for key in ("fired_when_it_should", "should", "fired_when_it_should_not", "should_not")}
    path = os.path.join(REPO, "eval-runs/heldout-01-fable/three_arms.json")
    if os.path.isfile(path):
        second = load("eval-runs/heldout-01-fable/three_arms.json")
        fair = (second.get("if_judge_failures_passed") or {}).get("per_case") or second["per_case"]
        recorded = decide(second["per_case"], "without")
        adjusted = decide(fair, "without")
        data["second_model"] = {
            "model": second["meta"].get("model"), "judge_failures": len(second.get("judge_failures") or []),
            "cases": [{"case": row["case"], "title": titles.get(row["case"], row["case"]), "with": row.get("with"),
                       "without": row.get("without")} for row in fair],
            "recorded_diff": recorded["mean_diff"], "diff": adjusted["mean_diff"],
            "higher": adjusted["better"], "same": adjusted["same"], "lower": adjusted["worse"],
            "effort": {arm: {"minutes": (second["effort"].get(arm) or {}).get("minutes"),
                             "cost_usd": (second["effort"].get(arm) or {}).get("cost_usd")} for arm in ("with", "without")},
        }
    return data


BENCH_SOURCES = [
    # model, result file, {arm name in the file: arm on the board}
    ("sonnet", "eval-runs/heldout-01/result.json", {"with": "with", "without": "without"}),
    ("sonnet", "eval-runs/heldout-01-prompted/result.json", {"with": "prompted"}),
    ("opus", "eval-runs/heldout-01-opus/result.json", {"with": "with", "without": "without"}),
    ("fable", "eval-runs/heldout-01-fable/result.json", {"with": "with", "without": "without"}),
    ("fable", "eval-runs/heldout-01-fable-rest7/result.json", {"with": "with", "without": "without"}),
]


def fair_score(run):
    """Share of the content checks of one run that passed, a check whose judge call failed counted as passed.

    The evaluation tool records a failed call to the judge as a failed check. The report gives both readings;
    across models the second one is the fair one, because the failures fell on single arms.
    """
    passed = total = failed_calls = 0
    for grader in run.get("graders") or []:
        if str(grader.get("name") or "").startswith("00-"):
            continue                      # the indicator that the skill started is not a content check
        total += 1
        if "judgeVotes" not in grader and str(grader.get("explanation") or "").startswith("grader threw"):
            failed_calls += 1
            passed += 1
        else:
            passed += 1 if grader.get("passed") else 0
    return (passed / total if total else None), failed_calls


def benchmark():
    """Accuracy and list price of an answer for every model and arm that was run on the held-out questions."""
    cells = {}                            # (model, arm) -> {case: {"scores": [...], "costs": [...]}}
    failures = {}
    for model, path, arms in BENCH_SOURCES:
        if not os.path.isfile(os.path.join(REPO, path)):
            continue
        for case in load(path)["cases"]:
            for arm_in_file, arm in arms.items():
                for run in (case.get("arms") or {}).get(arm_in_file) or []:
                    if run.get("error"):
                        continue
                    score, failed = fair_score(run)
                    failures[(model, arm)] = failures.get((model, arm), 0) + failed
                    if score is None:
                        continue
                    entry = cells.setdefault((model, arm), {}).setdefault(case["name"], {"scores": [], "costs": []})
                    entry["scores"].append(score)
                    entry["costs"].append(run["costUsd"] - (run.get("judgeCostUsd") or 0))

    def summary(per_case, names):
        if not names:
            return None
        return {"accuracy": sum(sum(per_case[n]["scores"]) / len(per_case[n]["scores"]) for n in names) / len(names),
                "cost_usd": sum(sum(per_case[n]["costs"]) / len(per_case[n]["costs"]) for n in names) / len(names),
                "runs": [min(len(per_case[n]["scores"]) for n in names), max(len(per_case[n]["scores"]) for n in names)]}

    models = []
    for model in ("sonnet", "opus", "fable"):
        with_arm, alone = cells.get((model, "with")) or {}, cells.get((model, "without")) or {}
        common = sorted(set(with_arm) & set(alone))
        if not common:
            continue
        diffs = [sum(with_arm[n]["scores"]) / len(with_arm[n]["scores"]) - sum(alone[n]["scores"]) / len(alone[n]["scores"])
                 for n in common]
        row = {"model": model, "n": len(common), "with": summary(with_arm, common), "without": summary(alone, common),
               "higher": sum(1 for d in diffs if d > 1e-9), "lower": sum(1 for d in diffs if d < -1e-9),
               "judge_failures": failures.get((model, "with"), 0) + failures.get((model, "without"), 0)}
        row["same"] = len(common) - row["higher"] - row["lower"]
        prompted = cells.get((model, "prompted")) or {}
        if prompted:
            row["prompted"] = summary(prompted, sorted(set(prompted) & set(common)) or sorted(prompted))
        models.append(row)
    unit = next((row["without"]["cost_usd"] for row in models if row["model"] == "sonnet"), None)
    return {"unit_cost_usd": unit, "models": models}


def before_after(data):
    """The question with the largest gap: the recorded answer of the model alone beside the one with the skill."""
    cases = [c for c in data["cases"] if c.get("with") is not None and c.get("without") is not None]
    if not cases:
        return None
    pick = max(cases, key=lambda c: c["with"] - c["without"])

    def read(arm, run):
        path = os.path.join(REPO, "eval-runs", "heldout-01", "answers", "%s__%s__%d.md" % (pick["case"], arm, run))
        if not os.path.isfile(path):
            return None
        with open(path, encoding="utf-8") as handle:
            return handle.read().strip()

    def links(text):
        return len(set(re.findall(r"https?://[^\s)>\]]+", text)))

    plain = read("without", 1)
    skilled = run_used = None
    for run in (1, 2, 3):
        text = read("with", run)
        if text and re.search(r"^\|[^\n]*\|\s*$", text, re.M):
            skilled, run_used = text, run
            break
    if not plain or not skilled:
        return None
    question, counts = "", {}
    for case in load("eval-runs/heldout-01/result.json")["cases"]:
        if case["name"] == pick["case"]:
            question = prompt_text(case.get("promptMarkdown") or "")
            for arm, index in (("without", 0), ("with", run_used - 1)):
                graders = [g for g in case["arms"][arm][index]["graders"] if not str(g.get("name") or "").startswith("00-")
                           and not ("judgeVotes" not in g and str(g.get("explanation") or "").startswith("grader threw"))]
                counts[arm] = {"passed": sum(1 for g in graders if g.get("passed")), "total": len(graders)}
    return {"case": pick["case"], "title": pick["title"], "question": question, "run": run_used,
            "plain": {"text": plain, "links": links(plain), "words": len(plain.split()), "score": pick["without"],
                      "run_checks": counts.get("without")},
            "skill": {"text": skilled, "links": links(skilled), "words": len(skilled.split()), "score": pick["with"],
                      "run_checks": counts.get("with")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", default=os.path.join(REPO, "docs", "assets", "showcase.json"))
    args = parser.parse_args()
    data = {"runs": [replay(spec) for spec in REPLAYS], "evidence": evidence()}
    data["benchmark"] = benchmark()
    pair = before_after(data["evidence"])
    if pair:
        data["before_after"] = pair
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=1, ensure_ascii=False)
    print("wrote %s: %d replays, %d questions in the evidence" % (os.path.relpath(args.out, REPO), len(data["runs"]),
                                                              len(data["evidence"]["cases"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
