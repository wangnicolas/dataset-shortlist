#!/usr/bin/env python3
"""Render the example pages of the site from the data each run recorded, with the current renderer.

    python3 tools/render_examples.py

For every folder eval-runs/heldout-01/pages/<run>/ that holds a shortlist.json, writes
docs/examples/heldout/<run>.html. The page as it was written during the run stays beside the data, in
eval-runs/heldout-01/pages/<run>/dataset-shortlist.html. The two can differ: the version that was
evaluated showed "Unknown" for some access conditions it had found, which later versions show as
their tier (CHANGELOG, 0.1.1).
"""
from __future__ import annotations

import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts"))

from scoutlib import render  # noqa: E402


def main():
    source = os.path.join(REPO, "eval-runs", "heldout-01", "pages")
    target = os.path.join(REPO, "docs", "examples", "heldout")
    os.makedirs(target, exist_ok=True)
    count = 0
    for run in sorted(os.listdir(source)):
        data_file = os.path.join(source, run, "shortlist.json")
        if not os.path.isfile(data_file):
            continue
        with open(data_file, encoding="utf-8") as handle:
            data = json.load(handle)
        with open(os.path.join(target, run + ".html"), "w", encoding="utf-8") as handle:
            handle.write(render.render_html(data))
        count += 1
    print("rendered %d example pages into docs/examples/heldout" % count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
