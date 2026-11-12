#!/usr/bin/env python3
"""Blind audit support (see "Blind audit of every recommended dataset" in docs/EVAL_PROTOCOL.md).

    python3 tools/audit_packets.py make <eval-output-dir> [--seed 20261111]
    python3 tools/audit_packets.py aggregate <eval-output-dir>

`make` writes, for every case, <dir>/audit/<case>/question.md, answer_A.md and
answer_B.md (run 1 of each arm, in an order decided by the seed) and keeps the
A/B-to-arm mapping in <dir>/audit_key.json, outside the folders the auditor is
given. The auditor writes <dir>/audit/<case>/audit.json:

    {"A": [{"dataset": "...", "official_url": "...", "exists": true,
            "access_stated": "...", "access_correct": true,
            "meets_must_haves": true, "note": "..."}],
     "B": [...]}

where `exists`, `access_correct` and `meets_must_haves` are true, false or null
(null = the answer did not state it, or it could not be established).
`aggregate` joins the audits with the key and prints per-arm shares.
"""
from __future__ import annotations

import json
import os
import random
import re
import sys


def _prompt_text(prompt_markdown):
    text = prompt_markdown or ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            text = text[end + 4:]
    return text.strip()


def make(out_dir, seed):
    with open(os.path.join(out_dir, "result.json"), encoding="utf-8") as handle:
        result = json.load(handle)
    rng = random.Random(seed)
    key = {"seed": seed, "cases": {}}
    for case in result.get("cases", []):
        name = case["name"]
        answers = {}
        for arm in ("with", "without"):
            path = os.path.join(out_dir, "answers", "%s__%s__1.md" % (name, arm))
            if os.path.isfile(path):
                answers[arm] = open(path, encoding="utf-8").read()
        if len(answers) < 2:
            print("skipping %s: missing an answer" % name)
            continue
        order = ["with", "without"]
        rng.shuffle(order)
        folder = os.path.join(out_dir, "audit", name)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "question.md"), "w", encoding="utf-8") as handle:
            handle.write(_prompt_text(case.get("promptMarkdown")) + "\n")
        for letter, arm in zip("AB", order):
            text = answers[arm]
            # Remove traces of the skill's own output files so the arm cannot be read off the answer.
            text = re.sub(r"[^\n]*dataset-shortlist\.html[^\n]*\n?", "", text)
            text = re.sub(r"[^\n]*dataset-shortlist/[^\n]*\n?", "", text)
            with open(os.path.join(folder, "answer_%s.md" % letter), "w", encoding="utf-8") as handle:
                handle.write(text)
        key["cases"][name] = {"A": order[0], "B": order[1]}
    with open(os.path.join(out_dir, "audit_key.json"), "w", encoding="utf-8") as handle:
        json.dump(key, handle, indent=2)
    print("%d audit packets in %s" % (len(key["cases"]), os.path.join(out_dir, "audit")))
    return 0


def _share(items, field):
    known = [item.get(field) for item in items if item.get(field) is not None]
    return (sum(1 for v in known if v) / len(known) if known else None), len(known)


def aggregate(out_dir):
    with open(os.path.join(out_dir, "audit_key.json"), encoding="utf-8") as handle:
        key = json.load(handle)
    per_arm = {"with": [], "without": []}
    per_case = []
    for name, mapping in sorted(key["cases"].items()):
        path = os.path.join(out_dir, "audit", name, "audit.json")
        if not os.path.isfile(path):
            print("no audit yet for %s" % name)
            continue
        with open(path, encoding="utf-8") as handle:
            audit = json.load(handle)
        row = {"case": name}
        for letter in "AB":
            arm = mapping[letter]
            items = audit.get(letter) or []
            per_arm[arm].extend(items)
            row[arm] = {"n": len(items), "exists": _share(items, "exists")[0],
                        "access_correct": _share(items, "access_correct")[0],
                        "meets_must_haves": _share(items, "meets_must_haves")[0]}
        per_case.append(row)

    def pct(value):
        return "n/a" if value is None else "%.0f%%" % (100 * value)

    lines = ["## Blind audit of every recommended dataset (run 1 of each case and arm)", "",
             "| Arm | Datasets audited | Per answer | Exist as described | Access condition stated correctly | Meet the must-haves |",
             "|---|---|---|---|---|---|"]
    summary = {}
    for arm in ("with", "without"):
        items = per_arm[arm]
        n_cases = sum(1 for row in per_case if arm in row) or 1
        exists, n_exists = _share(items, "exists")
        access, n_access = _share(items, "access_correct")
        fit, n_fit = _share(items, "meets_must_haves")
        def count(field):
            return sum(1 for item in items if item.get(field) is True)
        stated = sum(1 for item in items if str(item.get("access_stated") or "").strip().lower() not in ("", "not stated"))
        summary[arm] = {"n": len(items), "exists": exists, "access_correct": access, "meets_must_haves": fit,
                        "n_access_stated": n_access,     # kept for older readers: the number judged, see below
                        "exists_true": count("exists"), "exists_judged": n_exists,
                        "access_true": count("access_correct"), "access_judged": n_access, "access_stated": stated,
                        "fit_true": count("meets_must_haves"), "fit_judged": n_fit}
        lines.append("| %s | %d | %.1f | %s (%d of %d judged) | %s (%d of %d judged) | %s (%d of %d judged) |" % (
            arm, len(items), len(items) / n_cases, pct(exists), count("exists"), n_exists, pct(access),
            count("access_correct"), n_access, pct(fit), count("meets_must_haves"), n_fit))
    lines += ["", "\"Judged\" leaves out the items the auditor could not settle: an official page that could not be "
                  "reached, an answer that stated no access condition, or documentation that does not say.",
              "", "### Access statements by how the answer marked them", "",
              "| Arm | Marked as checked today: correct | Marked as recalled: correct | Not marked: correct |",
              "|---|---|---|---|"]
    for arm in ("with", "without"):
        cells = []
        summary[arm]["by_mark"] = {}
        for mark in ("today", "memory", "none"):
            items = [item for item in per_arm[arm] if (item.get("access_marked") or "none") == mark]
            share, n = _share(items, "access_correct")
            right = sum(1 for item in items if item.get("access_correct") is True)
            summary[arm]["by_mark"][mark] = {"correct": share, "n": n, "right": right}
            cells.append("%s (%d of %d)" % (pct(share), right, n))
        lines.append("| %s | %s |" % (arm, " | ".join(cells)))
    text = "\n".join(lines) + "\n"
    with open(os.path.join(out_dir, "audit_summary.md"), "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(os.path.join(out_dir, "audit_summary.json"), "w", encoding="utf-8") as handle:
        json.dump({"per_arm": summary, "per_case": per_case}, handle, indent=2)
    print(text)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("make", "aggregate"):
        sys.stderr.write(__doc__)
        sys.exit(2)
    if sys.argv[1] == "make":
        seed_value = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 20261111
        sys.exit(make(sys.argv[2], seed_value))
    sys.exit(aggregate(sys.argv[2]))
