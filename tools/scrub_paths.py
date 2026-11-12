#!/usr/bin/env python3
"""Replace this machine's folders in the run records with neutral names.

    python3 tools/scrub_paths.py [--check] <file-or-folder> [...]

The evaluation tool writes absolute paths into its records (where the plugin
was loaded from, where a session worked). They say nothing about the result and
they carry the name of the account that ran it, so before records are committed
the home folder and the project folders are replaced by placeholders:

    <repo>       the folder of this repository
    <heldout>    the folder where the sealed cases were built
    <scratch>    the scratch folder of the session that ran the evaluation
    <home>       the home folder

Only text files are touched (.json, .md, .txt, .log, .html, .yaml, .jsonl).
With --check nothing is written; the files that would change are listed and the
exit status is 1 when there are any.
"""
from __future__ import annotations

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
TEXT = (".json", ".md", ".txt", ".log", ".html", ".yaml", ".yml", ".jsonl")


def replacements():
    pairs = [(REPO + "-heldout", "<heldout>"), (REPO, "<repo>")]
    pairs.append((re.compile(re.escape(os.path.join(HOME, ".claude", "jobs")) + r"/[0-9a-f]+/tmp"), "<scratch>"))
    pairs.append((HOME, "<home>"))
    # the same folders as they appear when a path is turned into a folder name (slashes become dashes)
    pairs.append((HOME.replace("/", "-"), "-home"))
    return pairs


def scrub(text):
    for old, new in replacements():
        text = old.sub(new, text) if hasattr(old, "sub") else text.replace(old, new)
    return text


def files(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
        for root, dirs, names in os.walk(path):
            dirs[:] = [d for d in dirs if d not in (".git", "traces", "__pycache__")]
            for name in names:
                if name.endswith(TEXT):
                    yield os.path.join(root, name)


def main(argv):
    check = "--check" in argv
    paths = [a for a in argv[1:] if a != "--check"]
    if not paths:
        sys.stderr.write(__doc__)
        return 2
    changed = []
    for path in files(paths):
        if os.path.abspath(path) == os.path.abspath(__file__):
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                before = handle.read()
        except (UnicodeDecodeError, OSError):
            continue
        after = scrub(before)
        if after != before:
            changed.append(path)
            if not check:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(after)
    print("%d file(s) %s" % (len(changed), "would change" if check else "changed"))
    for path in changed:
        print("  " + path)
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
