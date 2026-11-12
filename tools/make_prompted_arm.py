#!/usr/bin/env python3
"""Build the cases for the third arm of docs/EVAL_PROTOCOL.md ("no skill, told to verify").

    python3 tools/make_prompted_arm.py <dir with case folders> [<name of eval dir, default evals-prompted>]

Copies every case into tools/no-skill-plugin/<eval dir>/ and appends one fixed
sentence to its prompt. The copies are then run against the empty plugin in
tools/no-skill-plugin with `--ablation none`, which gives a single arm with no
skill loaded. The script copies files without printing their content.
"""
from __future__ import annotations

import os
import shutil
import sys

SENTENCE = ("Please search the web rather than answering from memory, and check that each "
            "dataset you recommend really exists and how it can be accessed.")


def main(source, eval_dir="evals-prompted"):
    here = os.path.dirname(os.path.abspath(__file__))
    target_root = os.path.join(here, "no-skill-plugin", eval_dir)
    if os.path.isdir(target_root):
        shutil.rmtree(target_root)
    os.makedirs(target_root)
    count = 0
    for name in sorted(os.listdir(source)):
        case = os.path.join(source, name)
        if not os.path.isfile(os.path.join(case, "prompt.md")):
            continue
        target = os.path.join(target_root, name)
        shutil.copytree(case, target)
        indicator = os.path.join(target, "graders", "00-skill-fired.md")
        if os.path.exists(indicator):
            os.remove(indicator)  # there is no skill in this arm
        with open(os.path.join(target, "prompt.md"), encoding="utf-8") as handle:
            text = handle.read().rstrip("\n")
        with open(os.path.join(target, "prompt.md"), "w", encoding="utf-8") as handle:
            handle.write(text + "\n\n" + SENTENCE + "\n")
        count += 1
    print("%d case(s) prepared in %s" % (count, target_root))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
