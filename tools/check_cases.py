#!/usr/bin/env python3
"""Check that eval case folders follow docs/EVAL_PROTOCOL.md and will load in `claude plugin eval`.

    python3 tools/check_cases.py <dir containing case folders>

Prints one line per problem and exits 1 if there is any. It reports only
structure (never the questions or the gold), so it is safe to run on a held-out
set without reading it.
"""
from __future__ import annotations

import os
import re
import sys

ALLOWED_PROMPT_KEYS = {"tags", "max_turns", "timeout_seconds", "allowed_tools"}
RESERVED = {"results", "mocks", "node_modules", "files", "true", "false", "null"}
SKILL_WORDS = re.compile(r"dataset-shortlist|scout\.py|SKILL\.md|\bskill\b", re.I)


def front_matter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end < 0:
        return None, text
    block = text[4:end]
    body = text[end + 4:].lstrip("\n")
    keys = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            keys[key.strip()] = value.strip()
    return keys, body


def check_case(path):
    name = os.path.basename(path)
    problems = []
    if not re.match(r"^[a-z][a-z0-9-]*$", name) or name in RESERVED:
        problems.append("bad case name")
    prompt = os.path.join(path, "prompt.md")
    if not os.path.isfile(prompt):
        problems.append("missing prompt.md")
    else:
        keys, body = front_matter(open(prompt, encoding="utf-8").read())
        if keys is None:
            problems.append("prompt.md has no settings block")
        else:
            extra = set(keys) - ALLOWED_PROMPT_KEYS
            if extra:
                problems.append("prompt.md unknown settings: %s" % ", ".join(sorted(extra)))
            for needed in ("max_turns", "timeout_seconds", "allowed_tools", "tags"):
                if needed not in keys:
                    problems.append("prompt.md missing setting %s" % needed)
            if len(body.strip()) < 40:
                problems.append("prompt text too short")
            if SKILL_WORDS.search(body):
                problems.append("prompt mentions the skill or its tools")
            if "---" in body:
                problems.append("prompt body contains '---'")
    case_yaml = os.path.join(path, "case.yaml")
    if not os.path.isfile(case_yaml):
        problems.append("missing case.yaml")
    else:
        text = open(case_yaml, encoding="utf-8").read()
        if 'schema_version: "1.1"' not in text:
            problems.append('case.yaml needs schema_version: "1.1" (quoted)')
        if not re.search(r"^name: %s\s*$" % re.escape(name), text, re.M):
            problems.append("case.yaml name does not equal the folder name")
        if "expected_outcome: |" not in text:
            problems.append("case.yaml missing expected_outcome block")
    graders = os.path.join(path, "graders")
    files = sorted(f for f in os.listdir(graders)) if os.path.isdir(graders) else []
    md = [f for f in files if f.endswith(".md")]
    if not md:
        problems.append("no graders")
    families = {"recall": 0, "access": 0, "trap": 0, "long-tail": 0}
    for fname in md:
        if not re.match(r"^\d\d-[a-z0-9-]+\.md$", fname):
            problems.append("grader file name not NN-words.md: %s" % fname)
        keys, body = front_matter(open(os.path.join(graders, fname), encoding="utf-8").read())
        if fname == "00-skill-fired.md" and keys is not None and keys.get("type") == "tool_used":
            continue  # the unscored indicator that the skill was invoked
        if keys is None or keys.get("type") != "llm":
            problems.append("grader %s: settings block must have type: llm" % fname)
            continue
        if set(keys) - {"type", "weight", "focus", "arm"}:
            problems.append("grader %s: unknown settings" % fname)
        if not body.strip().startswith("PASS if"):
            problems.append("grader %s: body must start with 'PASS if'" % fname)
        if "FAIL if" not in body:
            problems.append("grader %s: body must contain 'FAIL if'" % fname)
        for family in families:
            if "-%s-" % family in fname or fname.endswith("-%s.md" % family):
                families[family] += 1
    if md:
        if not 3 <= families["recall"] <= 5:
            problems.append("needs 3 to 5 recall graders, found %d" % families["recall"])
        if not 2 <= families["access"] <= 4:
            problems.append("needs 2 to 4 access graders, found %d" % families["access"])
        if families["trap"] > 1:
            problems.append("at most 1 trap grader")
        if families["long-tail"] != 1:
            problems.append("needs exactly 1 long-tail grader")
    return problems, families


def main(root):
    cases = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and d not in RESERVED)
    bad = 0
    for index, case in enumerate(cases, 1):
        problems, families = check_case(os.path.join(root, case))
        label = "case %02d" % index
        counts = ", ".join("%s=%d" % kv for kv in families.items())
        if problems:
            bad += 1
            for problem in problems:
                print("%s: %s" % (label, problem))
        else:
            print("%s: ok (%s)" % (label, counts))
    print("%d case(s), %d with problems" % (len(cases), bad))
    return 1 if bad or not cases else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
