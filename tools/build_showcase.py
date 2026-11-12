#!/usr/bin/env python3
"""Build the showcase page: docs/index.html (complete page) and docs/artifact.html (fragment).

    python3 tools/build_showcase.py [--owner <github-owner>] [--local-path <repository path>] [--out-dir docs]

The page is tools/showcase/template.html with one JSON block filled in. The block is
docs/assets/showcase.json (written by tools/build_showcase_data.py from the run records) plus:
the verifier demo parsed from docs/assets/verify-demo.txt, the count of access tiers on the pages
written during the evaluation, and the install command. No number is typed in the template.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts"))

from scoutlib.common import ACCESS_TIERS, canonical_tier  # noqa: E402
from scoutlib.render import _TIER_LABELS  # noqa: E402

MODEL_LABELS = {"sonnet": "Sonnet 5.5", "opus": "Opus 5.5", "fable": "Fable 5.2", "haiku": "Haiku 5.5"}


def load(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as handle:
        return json.load(handle)


def verifier_demo():
    """The recorded output of `scout.py verify` on three real and four planted candidates, as items."""
    with open(os.path.join(REPO, "docs", "assets", "verify-demo.txt"), encoding="utf-8") as handle:
        text = handle.read()
    items = []
    for block in re.split(r"\n(?=\s*\d+\.\s)", text):
        match = re.match(r"\s*\d+\.\s+(NOT VERIFIED|VERIFIED)\s+\[([^\]]*)\]\s+(.+)", block)
        if not match:
            continue
        reason = re.search(r"problem: (.+)", block) or re.search(r"note: (.+)", block)
        why = reason.group(1).strip() if reason else ""
        why = re.split(r";| from https?://", why)[0]
        if len(why) > 118:
            why = why[:118].rsplit(" ", 1)[0]
        # a candidate typed in by hand for the demo (source "manual") is one of the planted ones
        items.append({"ok": match.group(1) == "VERIFIED", "planted": match.group(2).split("|")[0].strip() == "manual",
                      "title": match.group(3).strip()[:74], "why": why.rstrip(" ,;:")})
    return items


def tiers_on_pages():
    """How the access field of every dataset on the pages written in the held-out run reads, by tier."""
    words = load("eval-runs/heldout-01/pages_summary.json").get("access_words") or {}
    counts = {}
    for word, n in words.items():
        tier = canonical_tier(word)[0]
        counts[tier] = counts.get(tier, 0) + n
    order = ["open", "account", "gated", "controlled", "closed", "unknown"]
    tiers = [{"key": key, "label": _TIER_LABELS[key], "meaning": ACCESS_TIERS[key], "count": counts.get(key, 0)}
             for key in order if counts.get(key)]
    return tiers, sum(counts.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--owner", default="OWNER")
    parser.add_argument("--local-path", default="")
    parser.add_argument("--out-dir", default=os.path.join(REPO, "docs"))
    args = parser.parse_args()

    data = load("docs/assets/showcase.json")
    data["verifier"] = verifier_demo()
    data["tiers"], data["tier_total"] = tiers_on_pages()
    data["page_shot"] = "assets/page-heldout-meetings.png"
    data["page_link"] = "examples/heldout/ho-o-03__with__2.html"
    sources_dir = os.path.join(REPO, "plugins", "dataset-shortlist", "skills", "dataset-shortlist", "scripts", "scoutlib", "sources")
    data["registries"] = len([name for name in os.listdir(sources_dir) if name.endswith(".py") and not name.startswith("_")])
    data["model_label"] = MODEL_LABELS.get(data["evidence"].get("model"), data["evidence"].get("model") or "")
    second = data["evidence"].get("second_model") or {}
    data["second_label"] = MODEL_LABELS.get(second.get("model"), second.get("model") or "")
    for row in (data.get("benchmark") or {}).get("models") or []:
        row["label"] = MODEL_LABELS.get(row["model"], row["model"])
    started = load("eval-runs/heldout-01/result.json").get("startedAt") or ""
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    if len(started) >= 7 and started[5:7].isdigit():
        data["run_month"] = "%s %s" % (months[int(started[5:7]) - 1], started[:4])
    if args.owner and args.owner != "OWNER":
        data["repo_url"] = "https://github.com/%s/dataset-shortlist" % args.owner
        data["install"] = {"command": "/plugin marketplace add %s/dataset-shortlist" % args.owner,
                           "note": "Then: /plugin install dataset-shortlist@dataset-shortlist-marketplace"}
    elif args.local_path:
        data["install"] = {"command": "claude --plugin-dir %s" % os.path.join(args.local_path, "plugins", "dataset-shortlist"),
                           "note": "Loads it from a local copy for one session; nothing is installed."}
    else:
        data["install"] = {"command": "claude --plugin-dir plugins/dataset-shortlist",
                           "note": "Runs from a clone of the repository for one session; nothing is installed."}

    with open(os.path.join(REPO, "tools", "showcase", "template.html"), encoding="utf-8") as handle:
        template = handle.read()
    block = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    block = block.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    if "__DATA_JSON__" not in template:
        raise SystemExit("the template has no __DATA_JSON__ placeholder")
    fragment = template.replace("__DATA_JSON__", block, 1)
    with open(os.path.join(args.out_dir, "artifact.html"), "w", encoding="utf-8") as handle:
        handle.write(fragment)
    split = fragment.index('<div class="wrap">')
    document = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<meta name="description" content="A Claude Code skill that finds research datasets you can actually obtain: '
                'each one checked against its registry record or landing page where possible, with access conditions and '
                'licence.">\n%s</head>\n<body>\n%s</body>\n</html>\n' % (fragment[:split], fragment[split:]))
    with open(os.path.join(args.out_dir, "index.html"), "w", encoding="utf-8") as handle:
        handle.write(document)
    print("wrote %s and artifact.html (%d bytes of data, %d replays)" % (
        os.path.join(args.out_dir, "index.html"), len(block), len(data["runs"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
