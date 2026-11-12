#!/usr/bin/env python3
"""Collect the pages the skill wrote during an evaluation run.

    python3 tools/harvest_pages.py <eval-output-dir>

`claude plugin eval --keep-temp` keeps each run's working folder under a sealed
directory. The trace of a run names that folder, so this script finds, for every
run in <eval-output-dir>/traces, the files the session left behind:

    dataset-shortlist.html         the interactive page
    dataset-shortlist/shortlist.json   the data behind it

and copies them to <eval-output-dir>/pages/<case>__<arm>__<n>/. It then counts,
from the JSON, what each page holds: how many datasets, how many carry a
verification stamp, how many have an access condition other than "unknown".
The counts go to pages_summary.json and pages_summary.md.

Unsealing changes the mode of the kept directories (they are created read-only
because they hold output written by the plugin under test).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys


def session_folder(trace_path):
    """The working folder of the run, read from the first event of its trace."""
    with open(trace_path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") == "system" and event.get("cwd"):
                return event["cwd"]
            break
    return None


def sealed_copy(cwd):
    """Where the kept copy of a run's working folder is, or None."""
    marker = "/home/cwd"
    if not cwd or not cwd.endswith(marker):
        return None
    kept = cwd[:-len(marker)]
    sealed = os.path.join(kept, "sealed")
    for path in (kept, sealed):
        if os.path.isdir(path):
            try:
                os.chmod(path, 0o700)
            except OSError:
                return None
    folder = os.path.join(sealed, "home", "cwd")
    return folder if os.path.isdir(folder) else None


PAGE_TIERS = ("open", "account", "gated", "controlled", "closed", "unknown")   # the words the page of 0.1.0 knows


def describe(shortlist):
    datasets = shortlist.get("datasets") or []
    verified = unknown_access = with_steps = with_papers = licensed = 0
    words = []
    for entry in datasets:
        record = entry.get("record") or {}
        check = record.get("verification") or {}
        if check.get("verified") and check.get("method") and check.get("checked_at"):
            verified += 1
        access = record.get("access")
        tier = (access.get("tier") if isinstance(access, dict) else access) or "unknown"
        tier = str(tier).strip().lower()
        words.append(tier)
        if tier == "unknown":
            unknown_access += 1
        if entry.get("access_steps"):
            with_steps += 1
        if entry.get("papers"):
            with_papers += 1
        if (record.get("licence") or {}).get("id") or (record.get("licence") or {}).get("name"):
            licensed += 1
    return {"access_words": words, "datasets": len(datasets), "verified": verified, "access_unknown": unknown_access,
            "with_access_steps": with_steps, "with_papers": with_papers, "with_licence": licensed,
            "not_recommended": len(shortlist.get("not_recommended") or []), "gaps": len(shortlist.get("gaps") or [])}


VERIFY_LINE = re.compile(r"^\s*\d+\.\s+(NOT VERIFIED|VERIFIED)\s+\[([^\]]*)\]\s+(.+?)\s*$", re.M)


def verify_outcomes(trace_path):
    """What the verifier printed during the run: one entry per record it checked, in order."""
    found, seen = [], set()
    with open(trace_path, encoding="utf-8") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") != "user":
                continue
            for block in (event.get("message") or {}).get("content") or []:
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                content = block.get("content")
                text = content if isinstance(content, str) else " ".join(
                    part.get("text", "") for part in content or [] if isinstance(part, dict))
                for status, bracket, title in VERIFY_LINE.findall(text):
                    key = (status, title[:80])
                    if key in seen:
                        continue
                    seen.add(key)
                    found.append({"verified": status == "VERIFIED", "source": bracket.split("|")[0].strip(),
                                  "title": title[:140]})
    return found


def candidates_summary(folder):
    """How many candidate records the run collected from each registry, and the queries it sent."""
    path = os.path.join(folder, "dataset-shortlist", "candidates.json")
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (ValueError, OSError):
        return {}
    records = data.get("records") if isinstance(data, dict) else data
    by_source = {}
    for record in records or []:
        source = (record or {}).get("source") or "unknown"
        by_source[source] = by_source.get(source, 0) + 1
    queries = [q if isinstance(q, str) else (q or {}).get("query") for q in (data.get("queries") or [])] \
        if isinstance(data, dict) else []
    return {"candidates_by_source": by_source, "candidates_total": len(records or []),
            "candidate_queries": [q for q in queries if q]}


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(__doc__)
        return 2
    out_dir = argv[1]
    traces = os.path.join(out_dir, "traces")
    if not os.path.isdir(traces):
        sys.stderr.write("no traces folder in %s\n" % out_dir)
        return 1
    rows = []
    for name in sorted(os.listdir(traces)):
        if not name.endswith(".jsonl"):
            continue
        run_id = name[:-len(".jsonl")]
        parts = run_id.split("__")
        if len(parts) != 3:
            continue
        case, arm, index = parts
        row = {"run": run_id, "case": case, "arm": arm, "index": int(index), "kept": False, "page": False, "json": False}
        folder = sealed_copy(session_folder(os.path.join(traces, name)))
        if folder:
            row["kept"] = True
            if arm == "with":
                row.update(candidates_summary(folder))
                row["verify_outcomes"] = verify_outcomes(os.path.join(traces, name))
            target = os.path.join(out_dir, "pages", run_id)
            page = os.path.join(folder, "dataset-shortlist.html")
            data = os.path.join(folder, "dataset-shortlist", "shortlist.json")
            if os.path.isfile(page) or os.path.isfile(data):
                os.makedirs(target, exist_ok=True)
            if os.path.isfile(page):
                shutil.copyfile(page, os.path.join(target, "dataset-shortlist.html"))
                row["page"] = True
                row["page_bytes"] = os.path.getsize(page)
            if os.path.isfile(data):
                shutil.copyfile(data, os.path.join(target, "shortlist.json"))
                row["json"] = True
                try:
                    with open(data, encoding="utf-8") as handle:
                        row.update(describe(json.load(handle)))
                except (ValueError, OSError) as error:
                    row["json_error"] = str(error)
        rows.append(row)

    summary = {"runs": rows, "per_arm": {}}
    lines = ["# Pages written during the run", "",
             "Counted from the files each session left in its working folder.", "",
             "| Arm | Runs | Folder kept | Page written | Datasets on the pages | With a verification stamp | Access left unknown |",
             "|---|---|---|---|---|---|---|"]
    for arm in sorted({row["arm"] for row in rows}):
        selected = [row for row in rows if row["arm"] == arm]
        pages = [row for row in selected if row["page"]]
        counted = [row for row in selected if "datasets" in row]
        entry = {"runs": len(selected), "kept": sum(row["kept"] for row in selected), "pages": len(pages),
                 "datasets": sum(row["datasets"] for row in counted), "verified": sum(row["verified"] for row in counted),
                 "access_unknown": sum(row["access_unknown"] for row in counted),
                 "with_papers": sum(row["with_papers"] for row in counted)}
        summary["per_arm"][arm] = entry
        lines.append("| %s | %d | %d | %d | %d | %d | %d |" % (arm, entry["runs"], entry["kept"], entry["pages"],
                                                             entry["datasets"], entry["verified"], entry["access_unknown"]))
    # What the sessions wrote in the access field, and what the page of 0.1.0 made of it.
    counts = {}
    for row in rows:
        for word in row.get("access_words") or []:
            counts[word] = counts.get(word, 0) + 1
    total_words = sum(counts.values())
    not_shown = sum(n for word, n in counts.items() if word not in PAGE_TIERS)
    summary["access_words"] = counts
    summary["access_words_total"] = total_words
    summary["access_words_shown_as_unknown_though_stated"] = not_shown
    if total_words:
        lines += ["", "## The access field on the pages", "",
                  "The page of version 0.1.0 knows six words (%s) and shows anything else as \"Unknown\"." % ", ".join(PAGE_TIERS),
                  "", "| Word written in the access field | Datasets | Shown by the page as |", "|---|---|---|"]
        for word, n in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append("| %s | %d | %s |" % (word, n, "its own tier" if word in PAGE_TIERS else "Unknown"))
        lines += ["", "Of %d datasets, %d carry a word the page did not know: the session had written an access condition "
                      "and the page showed \"Unknown\". %d were written as unknown." % (
                          total_words, not_shown, counts.get("unknown", 0))]

    lines += ["", "## Per run", "", "| Run | Page | Datasets | Verified | Access unknown | With papers |", "|---|---|---|---|---|---|"]
    for row in rows:
        if row["arm"] != "with":
            continue
        lines.append("| %s | %s | %s | %s | %s | %s |" % (row["run"], "yes" if row["page"] else "no", row.get("datasets", ""),
                                                        row.get("verified", ""), row.get("access_unknown", ""),
                                                        row.get("with_papers", "")))
    with open(os.path.join(out_dir, "pages_summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    text = "\n".join(lines) + "\n"
    with open(os.path.join(out_dir, "pages_summary.md"), "w", encoding="utf-8") as handle:
        handle.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
