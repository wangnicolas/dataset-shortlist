#!/usr/bin/env python3
"""Add the unscored "skill was invoked" indicator to every case folder.

    python3 tools/add_skill_indicator.py <dir containing case folders>

Writes graders/00-skill-fired.md into each case. In a with/without run
`claude plugin eval` reports a `tool_used: Skill` grader as an indicator and
leaves it out of the score, so it cannot favour either arm. The script reads no
case content.
"""
from __future__ import annotations

import os
import sys

INDICATOR = """---
type: tool_used
tool: Skill
input_match: '"skill"\\s*:\\s*"(?:[\\w-]+:)?dataset-shortlist"'
---
"""


def main(root):
    count = 0
    for name in sorted(os.listdir(root)):
        graders = os.path.join(root, name, "graders")
        if os.path.isdir(graders):
            with open(os.path.join(graders, "00-skill-fired.md"), "w", encoding="utf-8") as handle:
                handle.write(INDICATOR)
            count += 1
    print("indicator written to %d case(s)" % count)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
