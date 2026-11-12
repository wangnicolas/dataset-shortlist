#!/usr/bin/env python3
"""The decision rule of docs/EVAL_PROTOCOL.md, in one place.

tools/combine_arms.py writes its outcome into the run record and
tools/build_site.py and tools/fill_readme.py print it, so the sentence shown
anywhere is computed from the per-case scores and never typed by hand.
"""
from __future__ import annotations

import math

MARGIN = 0.05          # mean difference in case score that counts as a difference
SHARE_BETTER = 0.7     # "better on at least 7 of the ten cases"
EPS = 1e-9

# The wording fixed in the protocol.
STATEMENTS = {
    "beats": "The skill beats Claude without it on these questions.",
    "level": "On content the skill and Claude without it are level.",
    "worse": "The skill does worse than Claude without it on content.",
    "mixed": "Mixed: the per-question table is the result.",
    # not in the protocol table: the comparison could not be completed (see its notes of 2026-11-12)
    "incomplete": "Incomplete: some questions have no scored run in one of the two arms.",
}


def _mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def decide(per_case, other="without"):
    """Apply the rule to rows of {"case", "stratum", "with", <other>}.

    Returns None when no case has both scores. Otherwise a dict with the verdict
    key, the means, the mean difference, how many cases went each way, and the
    means per stratum.
    """
    rows = [r for r in per_case if r.get("with") is not None and r.get(other) is not None]
    if not rows:
        return None
    # A case that was run in neither arm is not part of this comparison (the prompted arm, for
    # instance, may cover fewer cases); a case scored in one arm only makes it incomplete.
    one_sided = [r["case"] for r in per_case if (r.get("with") is None) != (r.get(other) is None)]
    diffs = [r["with"] - r[other] for r in rows]
    mean_diff = sum(diffs) / len(diffs)
    better = sum(d > EPS for d in diffs)
    worse = sum(d < -EPS for d in diffs)
    strata = {}
    for row in rows:
        strata.setdefault(row.get("stratum", ""), []).append(row)
    by_stratum = {}
    for name, members in sorted(strata.items()):
        with_mean = _mean([m["with"] for m in members])
        other_mean = _mean([m[other] for m in members])
        by_stratum[name] = {"n": len(members), "with": with_mean, "other": other_mean, "diff": with_mean - other_mean}
    lower_in_a_stratum = any(entry["diff"] < -EPS for entry in by_stratum.values())
    needed = int(math.ceil(SHARE_BETTER * len(rows) - EPS))
    if mean_diff >= MARGIN - EPS and better >= needed and not lower_in_a_stratum:
        verdict = "beats"
    elif abs(mean_diff) < MARGIN - EPS:
        verdict = "level"
    elif mean_diff <= -MARGIN + EPS:
        verdict = "worse"
    else:
        verdict = "mixed"
    if one_sided:
        verdict = "incomplete"
    return {"one_sided_cases": one_sided, "verdict": verdict, "statement": STATEMENTS[verdict], "against": other, "n": len(rows),
            "with": _mean([r["with"] for r in rows]), "other": _mean([r[other] for r in rows]),
            "mean_diff": mean_diff, "better": better, "worse": worse, "same": len(rows) - better - worse,
            "needed_better": needed, "lower_in_a_stratum": lower_in_a_stratum, "by_stratum": by_stratum}


def marking_verdict(by_mark):
    """The conclusion fixed in the protocol about the skill's "confirmed today" / "recalled" marking.

    by_mark: {"today": {"correct": share or None, "n": int}, "memory": {...}, "none": {...}} for the
    skill arm, from the blind audit. Returns (key, sentence); key is "informative", "decoration" or
    "not assessable".
    """
    today = (by_mark or {}).get("today") or {}
    memory = (by_mark or {}).get("memory") or {}
    n_today, n_memory = today.get("n") or 0, memory.get("n") or 0
    if not n_today or not n_memory or today.get("correct") is None or memory.get("correct") is None:
        return "not assessable", ("The marking could not be assessed: the audit found %d access statements marked as "
                                  "checked today and %d marked as recalled, and both kinds are needed to compare them."
                                  % (n_today, n_memory))
    def part(entry, n):
        if entry.get("right") is not None:
            return "%d of %d" % (entry["right"], n)
        return "%.0f%% of %d" % (100.0 * entry["correct"], n)
    numbers = "%s statements marked as checked today were right, against %s marked as recalled" % (
        part(today, n_today), part(memory, n_memory))
    if today["correct"] > memory["correct"] + EPS:
        return "informative", "The marking carries information: %s." % numbers
    return "decoration", ("By the rule set beforehand the marking is decoration: %s, so a statement marked as checked "
                          "was not more often right." % numbers)


def conditions(outcome):
    """One sentence saying which of the three conditions for "beats" were met."""
    if not outcome:
        return ""
    gain = outcome["mean_diff"] >= MARGIN - EPS
    cases = outcome["better"] >= outcome["needed_better"]
    strata = not outcome["lower_in_a_stratum"]
    def word(flag):
        return "met" if flag else "not met"
    return ("The rule's three conditions for \"beats\": a mean gain of 5 points or more, %s (%+.1f); a higher score on at "
            "least %d of the %d questions, %s (%d); no stratum lower, %s." % (
                word(gain), 100.0 * outcome["mean_diff"], outcome["needed_better"], outcome["n"], word(cases),
                outcome["better"], word(strata)))
