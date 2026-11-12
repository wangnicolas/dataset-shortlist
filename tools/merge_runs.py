#!/usr/bin/env python3
"""Join the results of several `claude plugin eval` runs of different cases into one run folder.

    python3 tools/merge_runs.py <out-dir> <run-dir> <run-dir> [...]

Used when a model was run on the held-out questions in two parts (a first subset, then the rest).
The cases of every <run-dir>/result.json are put into <out-dir>/result.json, and the copies of the
traces and answers are carried over, so that tools/analyze_eval.py and tools/combine_arms.py can be
run on the joined folder as on any other run. A case that appears in two runs is an error.
"""
from __future__ import annotations

import json
import os
import shutil
import sys


def main(argv):
    if len(argv) < 4:
        sys.stderr.write(__doc__)
        return 2
    out_dir, sources = argv[1], argv[2:]
    merged, seen = None, {}
    for folder in sources:
        with open(os.path.join(folder, "result.json"), encoding="utf-8") as handle:
            result = json.load(handle)
        if merged is None:
            merged = dict(result)
            merged["cases"] = []
            merged["costUsd"] = 0.0
            merged["durationSeconds"] = 0
            merged["mergedFrom"] = []
        version = (((result.get("suite") or {}).get("plugins") or [{}])[0]).get("version")
        for case in result["cases"]:
            case["pluginVersion"] = version          # the runs may have used different versions of the plugin
            case["fromRun"] = os.path.basename(os.path.normpath(folder))
            if case["name"] in seen:
                raise SystemExit("case %s is in %s and in %s" % (case["name"], seen[case["name"]], folder))
            seen[case["name"]] = folder
            merged["cases"].append(case)
        merged["costUsd"] += result.get("costUsd") or 0
        merged["durationSeconds"] += result.get("durationSeconds") or 0
        merged["partial"] = bool(merged.get("partial")) or bool(result.get("partial"))
        merged["mergedFrom"].append({"folder": os.path.basename(os.path.normpath(folder)), "cases": len(result["cases"]),
                                     "startedAt": result.get("startedAt"), "pluginVersion": version})
        for sub in ("traces", "answers"):
            if os.path.isdir(os.path.join(folder, sub)):
                os.makedirs(os.path.join(out_dir, sub), exist_ok=True)
                for name in sorted(os.listdir(os.path.join(folder, sub))):
                    shutil.copyfile(os.path.join(folder, sub, name), os.path.join(out_dir, sub, name))
    merged["cases"].sort(key=lambda case: case["name"])
    versions = {}
    for case in merged["cases"]:
        versions[case.get("pluginVersion")] = versions.get(case.get("pluginVersion"), 0) + 1
    merged.setdefault("suite", {})["pluginVersions"] = versions
    if merged["suite"].get("plugins"):
        merged["suite"]["plugins"][0]["version"] = ", ".join(sorted(v for v in versions if v))
    merged.pop("aggregates", None)          # the tool's own totals belong to the separate runs
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as handle:
        json.dump(merged, handle, indent=1)
    with open(os.path.join(out_dir, "run-info.txt"), "w", encoding="utf-8") as handle:
        handle.write("joined by tools/merge_runs.py from: %s\n" % ", ".join(m["folder"] for m in merged["mergedFrom"]))
    print("%d cases from %d runs written to %s" % (len(merged["cases"]), len(sources), out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
