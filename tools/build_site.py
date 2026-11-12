#!/usr/bin/env python3
"""Build the showcase page from real evaluation output.

    python3 tools/build_site.py --arms eval-runs/heldout-01/three_arms.json \
        [--audit eval-runs/heldout-01/audit_summary.json] \
        --label "Held-out set: 10 questions, Sonnet 5.5, 3 runs per arm" \
        [--preview]            # marks the numbers as a development preview
        [--verify-demo docs/assets/verify-demo.txt]

Writes docs/index.html (a complete page for GitHub Pages) and
docs/artifact.html (the same content without the document skeleton, for
publishing as a Claude artifact). Every number on the page is read from the
JSON files named on the command line; nothing is typed in by hand.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decision_rule import conditions, decide, marking_verdict  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARMS = [("with", "With the skill", "s1"), ("without", "No skill", "s2"), ("prompted", "No skill, told to verify", "s3")]
FAMILIES = [("recall", "Found the suitable datasets"),
            ("access", "Stated how to obtain them correctly"),
            ("trap", "Avoided the unsuitable famous one"),
            ("long tail", "Surfaced a less-known fitting dataset")]


def esc(text):
    return html.escape(str(text), quote=True)


def pct(value, digits=0):
    return "n/a" if value is None else ("%." + str(digits) + "f%%") % (100.0 * value)


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# ------------------------------------------------------------------ chart (inline SVG)

def grouped_bars(rows, arms, width=720):
    """One group per item, one thin horizontal bar per arm on a shared 0-100% axis.

    rows: [(label, {arm_key: value or None}, n_graders)]. A share of checks passed
    is a magnitude from zero, so bars are honest here, and separate lanes keep
    three arms readable when their values coincide (dots on one line hid each
    other). Identity is carried by colour, the legend above the chart and the
    order of the lanes, which never changes; every bar has its value written at
    its end. A table of the same numbers follows the chart on the page.
    """
    left, right, top, lane, bar_h, group_gap = 250, 52, 12, 15, 10, 18
    plot_w = width - left - right
    group_h = lane * len(arms)
    height = top + (group_h + group_gap) * len(rows) - group_gap + 34
    axis_y = height - 26
    parts = ['<svg class="chart" viewBox="0 0 %d %d" role="img" aria-label="Share of checks passed by kind of check, '
             'one bar per arm">' % (width, height)]
    for tick in (0, 25, 50, 75, 100):
        x = left + plot_w * tick / 100.0
        parts.append('<line class="grid" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x, top - 4, x, axis_y))
        parts.append('<text class="tick" x="%.1f" y="%d" text-anchor="middle">%d%%</text>' % (x, height - 8, tick))
    for index, (label, values, n) in enumerate(rows):
        group_top = top + (group_h + group_gap) * index
        middle = group_top + group_h / 2.0
        words = label.split(" ")
        line1, line2 = label, ""
        if len(label) > 30:
            cut = len(words) // 2 + 1
            line1, line2 = " ".join(words[:cut]), " ".join(words[cut:])
        if line2:
            parts.append('<text class="rowlabel" x="%d" y="%.1f" text-anchor="end">%s</text>' % (left - 16, middle - 3, esc(line1)))
            parts.append('<text class="rowlabel" x="%d" y="%.1f" text-anchor="end">%s</text>' % (left - 16, middle + 13, esc(line2)))
        else:
            parts.append('<text class="rowlabel" x="%d" y="%.1f" text-anchor="end">%s</text>' % (left - 16, middle + 5, esc(line1)))
        for position, (key, label_arm, slot) in enumerate(arms):
            value = values.get(key)
            y = group_top + lane * position + (lane - bar_h) / 2.0
            if value is None:
                parts.append('<text class="val none" x="%d" y="%.1f">not run</text>' % (left + 6, y + bar_h - 1))
                continue
            length = max(2.0, plot_w * value)
            radius = min(4.0, length / 2.0)
            # square at the baseline, rounded at the data end
            path = "M%.1f %.1f h%.1f a%.1f %.1f 0 0 1 %.1f %.1f v%.1f a%.1f %.1f 0 0 1 %.1f %.1f h%.1f z" % (
                left, y, length - radius, radius, radius, radius, radius, bar_h - 2 * radius, radius, radius, -radius, radius,
                -(length - radius))
            parts.append('<g class="mark" tabindex="0" data-tip="%s, %s: %s%s">' % (
                esc(label), esc(label_arm), pct(value), (" of %s checks" % n) if n else ""))
            parts.append('<rect class="hit" x="%d" y="%.1f" width="%d" height="%d"/>' % (left, group_top + lane * position, plot_w + right, lane))
            parts.append('<path class="bar %s" d="%s"/>' % (slot, path))
            parts.append('<text class="val" x="%.1f" y="%.1f">%s</text>' % (left + length + 6, y + bar_h - 1, pct(value)))
            parts.append('</g>')
    parts.append('<line class="axis" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (left, top - 4, left, axis_y))
    parts.append('</svg>')
    return "\n".join(parts)


def legend(arms):
    items = "".join('<span class="key"><span class="swatch %s"></span>%s</span>' % (slot, esc(label)) for _, label, slot in arms)
    return '<div class="legend" aria-hidden="false">%s</div>' % items


# ------------------------------------------------- the pre-registered decision rule

def by_run_text(arms_data, other):
    """The difference of each repeat on its own, when the run record carries it."""
    stored = ((arms_data.get("decision") or {}).get(other) or {}).get("diff_by_run") or []
    if len(stored) < 2:
        return ""
    return "; taking each repeat on its own: " + ", ".join(signed(100.0 * d, 1) for d in stored)


def signed(value, digits=2):
    text = ("%+." + str(digits) + "f") % value
    return text.replace("-", "\u2212")


def points(value):
    """A difference between two shares, in percentage points."""
    text = signed(100.0 * value, 1)
    if float(text.replace("\u2212", "-")) == 0:
        text = text.lstrip("+\u2212")
    return text + " points"


def trigger_section(trigger):
    """One line from tools/trigger_test.py: does the skill start when it should, and only then."""
    if not trigger or not trigger.get("should"):
        return ""
    extra = ""
    if trigger.get("no_result"):
        extra = " %d runs ended without a result." % len(trigger["no_result"])
    return ('<h4>Does it start when it should</h4><p>Each of %d requests was sent once to a fresh session with only this '
            'plugin added, and the session\'s first action was recorded. The skill started on %d of %d requests that ask '
            'for datasets and on %d of %d requests that do not (profiling a file already on disk, writing a data loader, '
            'finding papers, and the like).%s</p>' % (
                trigger["should"] + trigger["should_not"], trigger["fired_when_it_should"], trigger["should"],
                trigger["fired_when_it_should_not"], trigger["should_not"], esc(extra)))


ARM_WORDS = {"with": "with the skill", "without": "without the skill", "prompted": "told to verify"}


def failed_judge_note(data):
    """One sentence about verdicts that are failed judge calls, with the outcome had they been passes."""
    failures = (data or {}).get("judge_failures") or []
    if not failures:
        return ""
    other = (data.get("if_judge_failures_passed") or {}).get("without")
    arms_hit = sorted({ARM_WORDS.get(f["arm"], f["arm"]) for f in failures})
    text = ("%d of the verdicts %s, recorded by the evaluation tool as %s (%s). "
            "Nothing was judged again." % (len(failures), "is a failed call to the judge" if len(failures) == 1
                                           else "are failed calls to the judge", "a fail" if len(failures) == 1 else "fails",
                                           "; ".join(
                "%d in the arm %s" % (sum(1 for f in failures if ARM_WORDS.get(f["arm"], f["arm"]) == arm), arm)
                for arm in arms_hit)))
    if other:
        text += (" Counted as %s instead, the scores are %s with the skill and %s without it (difference %s; higher on %d "
                 "questions, the same on %d, lower on %d)." % (
                     "a pass" if len(failures) == 1 else "passes", pct(other["with"], 1), pct(other["other"], 1),
                     points(other["mean_diff"]), other["better"], other["same"], other["worse"]))
    prompted = (data.get("if_judge_failures_passed") or {}).get("prompted")
    if prompted:
        text += (" Against the arm told to verify the difference would then be %s (higher on %d, the same on %d, lower "
                 "on %d)." % (points(prompted["mean_diff"]), prompted["better"], prompted["same"], prompted["worse"]))
    return text


def headline(arms_data, preview):
    main = decide(arms_data.get("per_case", []), "without")
    if not main:
        return ""
    detail = ("Mean score with the skill %s, without it %s (difference %s%s). The skill scored higher on %d of %d questions, "
              "the same on %d and lower on %d." % (pct(main["with"], 1), pct(main["other"], 1), points(main["mean_diff"]),
                                                    by_run_text(arms_data, "without"), main["better"], main["n"],
                                                    main["same"], main["worse"]))
    extra = ""
    prompted = decide(arms_data.get("per_case", []), "prompted")
    if prompted:
        extra = (" Against Claude told to search and verify: %s with the skill, %s without (difference %s); higher on %d, "
                 "the same on %d, lower on %d." % (pct(prompted["with"], 1), pct(prompted["other"], 1),
                                                   points(prompted["mean_diff"]), prompted["better"], prompted["same"],
                                                   prompted["worse"]))
    label = "By the rule fixed before the run" if not preview else "By the same rule, on the development questions (not a claim)"
    note = failed_judge_note(arms_data)
    return ('<div class="verdict"><p class="vlabel">%s</p><p class="vtext">%s</p><p class="small">%s</p>'
            '<p class="small">%s%s</p>%s</div>'
            % (esc(label), esc(main["statement"]), esc(conditions(main)), esc(detail), esc(extra),
               ('<p class="small">%s</p>' % esc(note)) if note else ""))


# ----------------------------------------------------------------------- page pieces

TITLES = {}   # case name -> short description of the question, set from --titles


def case_cell(case):
    if TITLES.get(case):
        return "%s <code>%s</code>" % (esc(TITLES[case]), esc(case))
    return "<code>%s</code>" % esc(case)


def results_section(arms_data, audit, label, preview):
    present = [(k, l, s) for k, l, s in ARMS if any(k in v for v in arms_data.get("score", {}).values())]
    strata = list(arms_data.get("score", {}).keys())
    out = []
    banner = ""
    if preview:
        banner = ('<p class="note"><strong>Preview.</strong> These numbers come from the development questions, '
                  'which were used while the skill was being written. They show how the comparison works; '
                  'the claim rests on the sealed held-out questions, reported here when that run is done.</p>')
    out.append('<p class="runlabel">%s</p>%s%s' % (esc(label), banner, headline(arms_data, preview)))

    # headline tiles: one row per stratum, never pooled
    tiles = []
    for stratum in strata:
        scores = arms_data["score"][stratum]
        cells = "".join(
            '<div class="tile"><div class="tlabel"><span class="swatch %s"></span>%s</div><div class="tvalue">%s</div></div>'
            % (slot, esc(lab), pct(scores.get(key))) for key, lab, slot in present)
        tiles.append('<div class="tilerow"><h4>%s questions</h4><div class="tiles">%s</div>'
                     '<p class="small">Share of a question\'s content checks passed, averaged over its runs and then over '
                     'the questions. Differences on this page are computed before rounding. Dates are in Japan time.</p></div>'
                     % (esc(stratum.capitalize()), cells))
    out.append("".join(tiles))

    # grouped bars by kind of check
    for stratum in strata:
        rows = []
        for fam_key, fam_label in FAMILIES:
            entry = arms_data.get("families", {}).get("%s / %s" % (stratum, fam_key))
            if entry:
                rows.append((fam_label, entry, (arms_data.get("family_n") or {}).get("%s / %s" % (stratum, fam_key))))
        if rows:
            out.append('<h4>%s questions, by kind of check</h4>%s<div class="chartwrap">%s</div>'
                       % (esc(stratum.capitalize()), legend(present), grouped_bars(rows, present)))
            head = "".join("<th scope=\"col\">%s</th>" % esc(l) for _, l, _ in present)
            body = "".join("<tr><th scope=\"row\">%s</th>%s</tr>" % (
                esc(lab), "".join("<td>%s</td>" % pct(vals.get(k)) for k, _, _ in present)) for lab, vals, _ in rows)
            out.append('<details class="tableview"><summary>Same numbers as a table</summary><div class="scroll"><table>'
                       '<thead><tr><th scope="col">Check</th>%s</tr></thead><tbody>%s</tbody></table></div></details>'
                       % (head, body))

    # the access checks of both groups together, the figure the showcase page leads with
    pooled_bits = []
    for arm, name in (("with", "with the skill"), ("without", "without it")):
        passed = total = 0
        for stratum in strata:
            key = "%s / access" % stratum
            entry = arms_data.get("families", {}).get(key)
            n = (arms_data.get("family_n") or {}).get(key) or 0
            if entry and entry.get(arm) is not None:
                passed += int(round(entry[arm] * n))
                total += n
        if total:
            pooled_bits.append("%d of %d checks (%s) %s" % (passed, total, pct(passed / total), name))
    if len(pooled_bits) == 2:
        out.append('<p>Both groups together: access conditions were stated correctly in %s and in %s.</p>' % tuple(pooled_bits))

    # per question: always visible, with the difference written out
    per_case = arms_data.get("per_case", [])
    if per_case:
        head = "".join("<th scope=\"col\">%s</th>" % esc(l) for _, l, _ in present)

        def gap(row):
            if row.get("with") is None or row.get("without") is None:
                return "n/a"
            points = 100.0 * (row["with"] - row["without"])
            return "0" if abs(points) < 0.5 else ("%+.0f" % points).replace("-", "\u2212")
        body = "".join("<tr><th scope=\"row\">%s</th><td>%s</td>%s<td>%s</td></tr>" % (
            case_cell(row["case"]), esc(row["stratum"]),
            "".join("<td>%s</td>" % pct(row.get(k)) for k, _, _ in present), gap(row)) for row in per_case)
        out.append('<h4>Every question, including the ones where the skill did not help</h4>'
                   '<div class="scroll"><table><thead><tr><th scope="col">Question</th><th scope="col">Stratum</th>%s'
                   '<th scope="col">Skill minus no skill, points</th></tr></thead>'
                   '<tbody>%s</tbody></table></div><p class="small">Share of content checks passed, averaged over the runs of '
                   'each question.</p>' % (head, body))

    # links and effort
    links, effort = arms_data.get("links", {}), arms_data.get("effort", {})
    rows = []
    for key, lab, slot in present:
        link = links.get(key, {})
        eff = effort.get(key, {})
        total = link.get("total") or 0
        working = ("%d of %d" % (link.get("ok", 0), total)) if total else "none given"
        rows.append("<tr><th scope=\"row\"><span class=\"swatch %s\"></span>%s</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            slot, esc(lab),
            "n/a" if link.get("per_answer") is None else "%.1f" % link["per_answer"], working, link.get("dead", 0),
            link.get("blocked", 0),
            "n/a" if eff.get("minutes") is None else "%.1f min" % eff["minutes"],
            "n/a" if eff.get("cost_usd") is None else "$%.2f" % eff["cost_usd"]))
    out.append('<h4>Links, time and cost per answer</h4><div class="scroll"><table><thead><tr><th scope="col">Arm</th>'
               '<th scope="col">Links per answer</th><th scope="col">Links that resolve</th><th scope="col">Dead links</th>'
               '<th scope="col">Site blocked the link checker</th>'
               '<th scope="col">Time</th><th scope="col">List-price cost</th></tr></thead><tbody>%s</tbody></table></div>'
               '<p class="small">Links were requested by a script after the runs; some sites refuse automated requests, and '
               'those links are counted apart, neither as working nor as dead. Cost is the list-price estimate reported by the '
               'evaluation tool.</p>'
               % "".join(rows))

    if audit:
        rows = []
        for key, lab, slot in present:
            entry = (audit.get("per_arm") or {}).get(key)
            if not entry:
                continue
            def cell(share, right, judged, entry=entry):
                if entry.get(judged) is None:
                    return pct(entry.get(share))
                return "%s (%d of %d)" % (pct(entry.get(share)), entry.get(right, 0), entry[judged])
            rows.append("<tr><th scope=\"row\"><span class=\"swatch %s\"></span>%s</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                slot, esc(lab), entry.get("n", 0), cell("exists", "exists_true", "exists_judged"),
                cell("access_correct", "access_true", "access_judged"), cell("meets_must_haves", "fit_true", "fit_judged")))
        if rows:
            out.append('<h4>Blind audit of every recommended dataset</h4><div class="scroll"><table><thead><tr>'
                       '<th scope="col">Arm</th><th scope="col">Datasets audited</th><th scope="col">Exist as described</th>'
                       '<th scope="col">Access stated correctly</th><th scope="col">Meet the must-haves</th></tr></thead>'
                       '<tbody>%s</tbody></table></div><p class="small">One answer per question from each of the two main arms (the first '
                       'run). An auditor on a different model looked up the official page of each recommended dataset. Each '
                       'share leaves out the items the auditor could not settle: a page that could not be reached, no access '
                       'condition stated, documentation that does not say. The auditor was not told which arm '
                       'wrote which answer, but the answers differ visibly (one carries links and marks what it checked), '
                       'so the blinding is by label only. The audit asks whether what an answer says about a dataset '
                       'is right; the access checks above ask whether the answer states the particular facts a researcher '
                       'needs. An answer can be right in what it says and still leave those facts out.</p>' % "".join(rows))
            marks = []
            for key, lab, slot in present:
                by_mark = ((audit.get("per_arm") or {}).get(key) or {}).get("by_mark")
                if not by_mark:
                    continue
                def mark_cell(m, by_mark=by_mark):
                    entry = by_mark.get(m) or {}
                    if not entry.get("n"):
                        return "none marked this way"
                    if entry.get("right") is not None:
                        return "%s (%d of %d)" % (pct(entry.get("correct")), entry["right"], entry["n"])
                    return "%s (of %d)" % (pct(entry.get("correct")), entry["n"])
                cells = "".join("<td>%s</td>" % mark_cell(m) for m in ("today", "memory", "none"))
                marks.append("<tr><th scope=\"row\"><span class=\"swatch %s\"></span>%s</th>%s</tr>" % (slot, esc(lab), cells))
            if marks:
                out.append('<h4>Are statements marked "checked today" more often right?</h4><div class="scroll"><table><thead><tr>'
                           '<th scope="col">Arm</th><th scope="col">Marked as checked today: correct</th>'
                           '<th scope="col">Said to be recalled or from memory: correct</th><th scope="col">Not marked: correct</th></tr></thead>'
                           '<tbody>%s</tbody></table></div><p class="small">The skill marks each access statement as confirmed today '
                           'or recalled. The marking is only useful if the first kind is right more often. %s</p>'
                           % ("".join(marks), esc(marking_verdict(((audit.get("per_arm") or {}).get("with") or {}).get("by_mark"))[1])))
    return "\n".join(out)


CSS = r"""
/* Layout: one reading column; the hero is a real question followed by the kind of record the skill returns. */
:root{
  --bg:#f5f6f8; --surface:#ffffff; --ink:#152238; --muted:#566079; --rule:#d7dbe4; --accent:#12805c; --link:#1d4fd7;
  --warn:#9a5b00; --stop:#b3261e; --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --codebg:#eef0f4;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Source Serif 4",Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,"Hiragino Sans","Noto Sans",sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f141d; --surface:#171d29; --ink:#e8ecf4; --muted:#9ba6bb; --rule:#2b3447; --accent:#43c493; --link:#8fb1ff;
  --warn:#e2a53a; --stop:#ff8a80; --s1:#3987e5; --s2:#d95926; --s3:#199e70; --codebg:#1e2533; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#0f141d; --surface:#171d29; --ink:#e8ecf4; --muted:#9ba6bb; --rule:#2b3447; --accent:#43c493; --link:#8fb1ff;
  --warn:#e2a53a; --stop:#ff8a80; --s1:#3987e5; --s2:#d95926; --s3:#199e70; --codebg:#1e2533; color-scheme:dark }
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans)}
.wrap{max-width:1040px;margin:0 auto;padding-block:56px 96px;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:var(--link);text-underline-offset:3px} a:focus-visible,button:focus-visible,.mark:focus-visible{outline:2px solid var(--link);outline-offset:3px}
.eyebrow{font:600 12px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 20px}
h1{font:500 clamp(34px,6vw,60px)/1.08 var(--serif);letter-spacing:-.01em;margin:0 0 20px;max-width:16ch;text-wrap:balance}
.lede{font-size:19px;line-height:1.55;max-width:62ch;margin:0 0 28px;color:var(--ink)}
h2{font:500 clamp(24px,3.4vw,34px)/1.15 var(--serif);margin:72px 0 14px;text-wrap:balance;max-width:24ch}
h3{font:600 17px/1.3 var(--sans);margin:0 0 6px} h4{font:600 15px/1.3 var(--sans);margin:32px 0 10px}
p{max-width:68ch;margin:0 0 14px} .small{font-size:13.5px;color:var(--muted)}
code,pre,.mono{font-family:var(--mono);font-size:13.5px}
.ask{font:italic 400 19px/1.5 var(--serif);border-left:3px solid var(--accent);padding:2px 0 2px 16px;margin:0 0 18px;max-width:60ch}
.record{background:var(--surface);border:1px solid var(--rule);border-radius:6px;overflow:hidden;margin:0 0 12px}
.record .row{display:grid;grid-template-columns:minmax(0,2.2fr) minmax(0,1.3fr) minmax(0,1fr) auto;gap:16px;align-items:center;padding:14px 18px;border-top:1px solid var(--rule)}
.record .row:first-child{border-top:0}
.record .name{font-weight:600;min-width:0} .record .host{display:block;font:400 12.5px/1.4 var(--mono);color:var(--muted)}
.badge{display:inline-flex;align-items:center;gap:6px;font:600 12.5px/1 var(--sans);padding:6px 9px;border-radius:4px;border:1px solid currentColor;white-space:nowrap}
.badge.open{color:var(--accent)} .badge.apply{color:var(--warn)} .badge.inst{color:var(--stop)} .badge.none{color:var(--muted);border-style:dashed}
.stamp{font:700 10.5px/1 var(--mono);letter-spacing:.1em;color:var(--accent);border:1.5px solid var(--accent);border-radius:3px;padding:5px 7px;white-space:nowrap}
.stamp.no{color:var(--stop);border-color:var(--stop)}
@media (max-width:720px){ .record .row{grid-template-columns:1fr;gap:8px} }
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:8px}
.cols > div{min-width:0;border-top:2px solid var(--ink);padding-top:14px}
@media (max-width:820px){ .cols{grid-template-columns:1fr} }
.steps{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:0;margin:18px 0 6px;border:1px solid var(--rule);border-radius:6px;background:var(--surface);overflow:hidden}
.steps div{padding:14px 14px 16px;border-left:1px solid var(--rule);min-width:0} .steps div:first-child{border-left:0}
.steps b{display:block;font:600 14px/1.3 var(--sans);margin-bottom:4px} .steps span{font-size:13px;color:var(--muted);line-height:1.45;display:block}
.steps i{font:700 11px/1 var(--mono);font-style:normal;color:var(--accent);display:block;margin-bottom:8px;letter-spacing:.08em}
@media (max-width:900px){ .steps{grid-template-columns:repeat(2,minmax(0,1fr))} .steps div{border-left:0;border-top:1px solid var(--rule)} .steps div:nth-child(-n+2){border-top:0} .steps div:nth-child(even){border-left:1px solid var(--rule)} }
.shot{border:1px solid var(--rule);border-radius:6px;overflow:hidden;background:var(--surface);margin:16px 0}
.shot img{display:block;width:100%;height:auto}
figure{margin:0} figcaption{font-size:13.5px;color:var(--muted);margin-top:8px;max-width:68ch}
.runlabel{font:600 13px/1.4 var(--mono);color:var(--muted);margin:6px 0 12px;max-width:none}
.verdict{border-top:2px solid var(--ink);border-bottom:1px solid var(--rule);padding:16px 0 12px;margin:14px 0 22px;max-width:760px}
.vlabel{font:600 12px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.vtext{font:500 clamp(20px,2.6vw,26px)/1.25 var(--serif);margin:0 0 10px}
.note{background:var(--codebg);border-left:3px solid var(--warn);padding:12px 16px;border-radius:0 4px 4px 0;max-width:72ch}
.tilerow{margin:18px 0 6px} .tilerow h4{margin:0 0 10px}
.tiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;max-width:760px}
.tile{background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:14px 16px;min-width:0}
.tlabel{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:8px}
.tvalue{font:600 34px/1.15 var(--sans);margin-top:6px}
@media (max-width:640px){ .tiles{grid-template-columns:1fr} }
.swatch{display:inline-block;width:10px;height:10px;border-radius:50%;flex:none;margin-right:6px;vertical-align:baseline}
.swatch.s1{background:var(--s1)} .swatch.s2{background:var(--s2)} .swatch.s3{background:var(--s3)}
.legend{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:13.5px;color:var(--muted);margin:4px 0 6px} .key{display:inline-flex;align-items:center}
.chartwrap{background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:12px 8px 4px;overflow-x:auto;position:relative}
.chart{display:block;width:100%;min-width:560px;height:auto;font-family:var(--sans)}
.chart .grid{stroke:var(--rule);stroke-width:1} .chart .tick{fill:var(--muted);font-size:11.5px}
.chart .rowlabel{fill:var(--ink);font-size:13.5px}
.chart .hit{fill:transparent} .chart .val{fill:var(--ink);font-size:12px;font-weight:600} .chart .val.none{fill:var(--muted);font-weight:400}
.chart .axis{stroke:var(--muted);stroke-width:1}
.chart .bar.s1{fill:var(--s1)} .chart .bar.s2{fill:var(--s2)} .chart .bar.s3{fill:var(--s3)}
.chart .mark{cursor:default;outline:none} .chart .mark:hover .bar,.chart .mark:focus .bar{stroke:var(--ink);stroke-width:1.5}
.chart .mark:focus-visible .hit{stroke:var(--link);stroke-width:1.5}
.tip{position:fixed;z-index:20;pointer-events:none;background:var(--ink);color:var(--bg);font-size:12.5px;padding:6px 9px;border-radius:4px;max-width:260px}
.scroll{overflow-x:auto} table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums;background:var(--surface);border:1px solid var(--rule);border-radius:6px}
th,td{text-align:left;padding:9px 12px;border-top:1px solid var(--rule);vertical-align:top} thead th{border-top:0;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}
tbody th{font-weight:500} .tableview{margin:10px 0 0} .tableview summary{cursor:pointer;font-size:13.5px;color:var(--link);padding:6px 0}
pre{background:var(--codebg);border:1px solid var(--rule);border-radius:6px;padding:14px 16px;overflow-x:auto;line-height:1.55;margin:10px 0 14px;white-space:pre}
.cmd{display:flex;align-items:stretch;gap:0;max-width:760px;margin:10px 0}
.cmd pre{margin:0;flex:1;min-width:0;border-radius:6px 0 0 6px}
.cmd button{font:600 13px/1 var(--sans);border:1px solid var(--rule);border-left:0;background:var(--surface);color:var(--ink);padding:0 14px;border-radius:0 6px 6px 0;cursor:pointer}
ul.plain{padding-left:20px;max-width:68ch} ul.plain li{margin-bottom:6px}
footer{margin-top:80px;padding-top:20px;border-top:1px solid var(--rule);font-size:13.5px;color:var(--muted)}
@media (prefers-reduced-motion: reduce){ *{scroll-behavior:auto} }
"""

JS = r"""
(function(){
  var tip=null;
  function show(el,x,y){ if(!tip){tip=document.createElement('div');tip.className='tip';tip.setAttribute('role','status');document.body.appendChild(tip);}
    tip.textContent=el.getAttribute('data-tip'); tip.hidden=false;
    var w=tip.offsetWidth; tip.style.left=Math.max(8,Math.min(window.innerWidth-w-8,x-w/2))+'px'; tip.style.top=Math.max(8,y-44)+'px'; }
  function hide(){ if(tip) tip.hidden=true; }
  document.querySelectorAll('.mark').forEach(function(m){
    m.addEventListener('pointermove',function(e){show(m,e.clientX,e.clientY);});
    m.addEventListener('pointerleave',hide);
    m.addEventListener('focus',function(){var r=m.getBoundingClientRect();show(m,r.left+r.width/2,r.top);});
    m.addEventListener('blur',hide);
  });
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var text=document.getElementById(b.getAttribute('data-copy')).textContent;
      function done(){var old=b.textContent;b.textContent='Copied';setTimeout(function(){b.textContent=old;},1400);}
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,function(){select();});}else{select();}
      function select(){var r=document.createRange();r.selectNodeContents(document.getElementById(b.getAttribute('data-copy')));var s=window.getSelection();s.removeAllRanges();s.addRange(r);}
    });
  });
})();
"""


def second_model_section(data, label):
    if not data:
        return ""
    main = decide(data.get("per_case", []), "without")
    rows = "".join("<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        case_cell(r["case"]), esc(r["stratum"]), pct(r.get("with")), pct(r.get("without"))) for r in data.get("per_case", []))
    summary = ""
    if main:
        summary = ("Mean score with the skill %s, without it %s (difference %s) on %d questions; higher on %d, the same "
                   "on %d, lower on %d." % (pct(main["with"], 1), pct(main["other"], 1), points(main["mean_diff"]), main["n"],
                                           main["better"], main["same"], main["worse"]))
    note = failed_judge_note(data)
    effort, links = data.get("effort") or {}, data.get("links") or {}
    cost = ""
    if effort.get("with") and effort.get("without"):
        cost = ("On this model an answer with the skill took %.1f minutes and $%.2f at list price, against %.1f minutes and "
                "$%.2f without it, and carried %.1f links against %.1f." % (
                    effort["with"]["minutes"], effort["with"]["cost_usd"], effort["without"]["minutes"],
                    effort["without"]["cost_usd"], (links.get("with") or {}).get("per_answer") or 0,
                    (links.get("without") or {}).get("per_answer") or 0))
    return ('<h4>On a stronger model</h4><p class="runlabel">%s</p><p>%s The lift from a skill can shrink as the model '
            'itself gets better, so the same comparison was repeated on a stronger model. Three of these questions were run as the protocol planned; the other seven were added after the result above was known. The rule was set for the main comparison only, so this is reported as a description.</p>%s<div class="scroll"><table><thead><tr>'
            '<th scope="col">Question</th><th scope="col">Stratum</th><th scope="col">With the skill</th>'
            '<th scope="col">No skill</th></tr></thead><tbody>%s</tbody></table></div>%s'
            % (esc(label), esc(summary), ('<p class="note">%s</p>' % esc(note)) if note else "", rows,
               ('<p class="small">%s</p>' % esc(cost)) if cost else ""))


def question_of(result, case):
    """The question of a case, without the settings block of its prompt file."""
    for entry in (result or {}).get("cases", []):
        if entry.get("name") == case:
            text = entry.get("promptMarkdown") or ""
            if text.startswith("---"):
                end = text.find("\n---", 3)
                if end >= 0:
                    text = text[end + 4:]
            return " ".join(text.split())
    return ""


def pick_pages(pages):
    """Two pages, both chosen mechanically: the one the protocol names, and the one with most verification stamps."""
    written = [row for row in (pages or {}).get("runs", []) if row.get("page") and row.get("arm") == "with"]
    if not written:
        return None, None
    by_rule = sorted(written, key=lambda row: (row["case"], row["index"]))
    first_run_pages = [row for row in by_rule if row["index"] == 1]
    rule = (first_run_pages or by_rule)[0]
    best = sorted(written, key=lambda row: (-row.get("verified", 0), row["case"], row["index"]))[0]
    return rule, best


def pages_section(pages, result, prefix, shots):
    rule, best = pick_pages(pages)
    if not rule:
        return ""
    written = [row for row in pages["runs"] if row.get("page") and row.get("arm") == "with"]
    with_runs = [row for row in pages["runs"] if row.get("arm") == "with"]
    out = ['<p>When a run completes the workflow it writes one self-contained page: filter by access or licence, compare fit '
           'requirement by requirement, tick the datasets you want and take away the access plan. In the held-out run the '
           'page was written in %d of %d runs with the skill; the other answers say that it was not built. The pages below '
           'are rendered by the current version from the data each run recorded; the pages as they were written at the '
           'time, which showed "Unknown" for some access conditions the run had found, are in '
           '<code>eval-runs/heldout-01/pages/</code>.</p>' % (len(written), len(with_runs))]

    def block(row, heading, why, shot_key):
        href = prefix + row["run"] + ".html"
        figure = ""
        if shots.get(shot_key):
            figure = ('<figure class="shot"><img src="%s" alt="Top of the page written for this question: the requirements, '
                      'what was searched, and the comparison table with access, licence, size, fit and time to access" '
                      'loading="lazy"></figure>' % esc(shots[shot_key]))
        stamps = "%d of its %d datasets carry the skill's own verification stamp" % (row.get("verified", 0), row.get("datasets", 0))
        return ('<h4>%s</h4><p class="ask">"%s"</p>%s<p><a href="%s">Open this page</a>. %s; %s.</p>'
                % (esc(heading), esc(question_of(result, row["case"])), figure, esc(href), esc(why), esc(stamps)))

    out.append(block(rule, "The example the protocol picks",
                     "Chosen by a rule written down before any result was read: run 1 of the first question in alphabetical "
                     "order whose run wrote a page", "rule"))
    if best["run"] != rule["run"]:
        out.append(block(best, "The page with the most verified datasets",
                         "Chosen as the page with the largest number of verification stamps, to show the other end", "best"))
    rows = "".join("<tr><th scope=\"row\"><a href=\"%s\">%s, run %d</a></th><td>%d</td><td>%d</td><td>%d</td></tr>" % (
        esc(prefix + row["run"] + ".html"), esc(TITLES.get(row["case"]) or row["case"]), row["index"], row.get("datasets", 0),
        row.get("verified", 0), row.get("access_unknown", 0)) for row in sorted(written, key=lambda r: r["run"]))
    out.append('<details class="tableview"><summary>All %d pages written during the held-out run</summary><div class="scroll">'
               '<table><thead><tr><th scope="col">Question and run</th><th scope="col">Datasets on the page</th>'
               '<th scope="col">With the skill\'s verification stamp</th><th scope="col">Access left unknown</th></tr></thead>'
               '<tbody>%s</tbody></table></div><p class="small">The stamps are the skill\'s own record of what it checked. '
               'The blind audit below is the independent measure. Inside a hosted preview the page\'s "Download plan" button '
               'may be blocked by the viewer; "Copy plan" works, and so does the page opened from disk.</p></details>'
               % (len(written), rows))
    return "\n".join(out)


def pipeline_section(pipeline):
    """How far the with-skill runs went through the workflow, from tools/pipeline_use.py."""
    if not pipeline or not pipeline.get("runs"):
        return ""
    used, total = pipeline.get("used") or {}, pipeline["runs"]
    steps = [("Loaded the skill", pipeline.get("skill_loaded")), ("Searched the registries", used.get("search")),
             ("Searched the literature", used.get("papers")), ("Ran the verifier", used.get("verify")),
             ("Read access pages with the tool", used.get("read")), ("Rendered the interactive page", used.get("render"))]
    rows = "".join("<tr><th scope=\"row\">%s</th><td>%s of %d</td></tr>" % (esc(name), count, total)
                   for name, count in steps if count is not None)
    note = ""
    if "pages_written" in pipeline:
        missing = total - pipeline["pages_written"]
        false_claims = len(pipeline.get("answers_pointing_to_a_missing_page") or [])
        silent = len(pipeline.get("no_page_and_not_said") or [])
        if missing:
            note = ("The page was not written in %d of %d runs. In %d of those the answer says so; %d answers point to a page "
                    "that does not exist." % (missing, total, missing - silent - false_claims, false_claims))
    return ('<h4>How far the runs with the skill went through the workflow</h4><div class="scroll"><table><thead><tr>'
            '<th scope="col">Step</th><th scope="col">Runs that did it</th></tr></thead><tbody>%s</tbody></table></div>'
            '<p class="small">Read from the traces. %s</p>' % (rows, esc(note)))


def install_section(owner, local_path):
    """The commands that work for the reader: the marketplace once the repository is public, a local copy before."""
    local = ""
    if local_path:
        local = ('<p>From a local copy, for one session, with nothing installed:</p>'
                 '<div class="cmd"><pre id="c0">claude --plugin-dir %s</pre><button type="button" data-copy="c0">Copy</button></div>'
                 % esc(os.path.join(local_path, "plugins", "dataset-shortlist")))
    if owner and owner != "OWNER":
        market = ('<p>In Claude Code:</p>'
                  '<div class="cmd"><pre id="c1">/plugin marketplace add %s/dataset-shortlist</pre><button type="button" data-copy="c1">Copy</button></div>'
                  '<div class="cmd"><pre id="c2">/plugin install dataset-shortlist@dataset-shortlist-marketplace</pre><button type="button" data-copy="c2">Copy</button></div>'
                  % esc(owner))
    else:
        market = ('<p class="small">The repository is not published yet. Once it is, the two marketplace commands '
                  '(<code>/plugin marketplace add</code> and <code>/plugin install</code>) go here.</p>')
    return market + local if owner and owner != "OWNER" else local + market


def page(arms_data, audit, label, preview, verify_demo, shots, owner, second=None, second_label="", example=None,
         local_path=None, pipeline=None, pages=None, result=None, pages_prefix="examples/heldout/", trigger=None):
    results = results_section(arms_data, audit, label, preview) if arms_data else \
        '<p class="note">The comparison has not been run yet.</p>'
    results += pipeline_section(pipeline)
    results += second_model_section(second, second_label)
    results += trigger_section(trigger)
    demo = ""
    if verify_demo:
        demo = ('<h2>It catches what is not there</h2><p>Four planted entries were mixed with three real records: '
                'a record number that does not exist, a DOI that was never registered, a repository home page passed off '
                'as a dataset, and a real record cited under an invented title. This is the verifier\'s output, '
                'unedited.</p><pre>%s</pre>' % esc(verify_demo))
    shot_html = ""
    if shots.get("top"):
        shot_html += ('<figure class="shot"><img src="%s" alt="The interactive shortlist page: the research question, the requirements, '
                      'and a comparison table with access, licence, size, fit and time to access for each dataset" loading="lazy"></figure>'
                      % esc(shots["top"]))
    if shots.get("card"):
        shot_html += ('<figure class="shot"><img src="%s" alt="One dataset card: can I get it, may I use it, does it fit, with a '
                      'requirement-by-requirement check and the steps to obtain access" loading="lazy"></figure>' % esc(shots["card"]))
    if example and example.get("href"):
        # a page the skill wrote during a recorded run, shown as it was written
        sample_link = ('<p><a href="%s">Open this page</a> and try the filters, the selection and the plan export. %s</p>'
                       % (esc(example["href"]), esc(example.get("caption", ""))))
        if example.get("question"):
            sample_link = '<p class="ask">"%s"</p>' % esc(example["question"]) + sample_link
    else:
        sample_link = ('<p><a href="examples/sample-report.html">Open the sample page</a> and try the filters, the selection and '
                       'the plan export. The datasets in the sample are invented, to show the page without endorsing any.</p>')
    return """<title>dataset-shortlist</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>%(css)s</style>
<div class="wrap">
<p class="eyebrow">An agent skill for Claude Code</p>
<h1>Find research data you can actually get.</h1>
<p class="lede">Tell it what you want to study. It returns a short list of datasets, each checked against its registry record or landing page where one could be reached: how it is obtained, what its licence permits, whether it has what your question needs, and papers that used it. Every fact is marked as checked today or recalled.</p>
<p class="ask">"I want to predict sepsis onset in adult ICU patients. What can I start on this week, and what is worth applying for?"</p>
<div class="record" aria-label="What an answer contains, in outline">
  <div class="row"><div class="name">A challenge dataset built for this task<span class="host">registry record · open licence</span></div><div><span class="badge open">Direct download</span></div><div class="small">Start today</div><div><span class="stamp">VERIFIED</span></div></div>
  <div class="row"><div class="name">A large hospital database<span class="host">registry record · custom agreement</span></div><div><span class="badge apply">Application required</span></div><div class="small">Training and agreement, about two weeks</div><div><span class="stamp">VERIFIED</span></div></div>
  <div class="row"><div class="name">A database that needs project review<span class="host">landing page read</span></div><div><span class="badge inst">Approval per study</span></div><div class="small">Weeks to months</div><div><span class="stamp">VERIFIED</span></div></div>
  <div class="row"><div class="name">A famous dataset that lacks the label<span class="host">set aside, with the reason</span></div><div><span class="badge none">Not recommended</span></div><div class="small">No onset times</div><div><span class="stamp no">DOES NOT FIT</span></div></div>
</div>
<p class="small">An outline of the answer's shape. Real answers name the datasets, link them and quote the evidence.</p>

<h2>Three ways a fluent answer goes wrong</h2>
<div class="cols">
  <div><h3>Names and links that do not hold up</h3><p class="small">In a 2026 study of research agents, 3–13%% of the URLs they cited were hallucinated and 5–18%% did not resolve. <a href="https://arxiv.org/abs/2604.03173">Rao, Wong and Callison-Burch</a>, measured on citation URLs.</p></div>
  <div><h3>Only the famous few</h3><p class="small">Across 1,000 computer-science papers, roughly four out of five of the datasets and metrics the papers used were not suggested by any of three language models. <a href="https://arxiv.org/abs/2606.26130">Carlon et al.</a>, pipeline estimates.</p></div>
  <div><h3>"Publicly available" that is not</h3><p class="small">Valuable research data often needs training, an application or an institutional signature, and licence labels on hosting sites are often missing or wrong: "license omission of 70%%+ and error rates of 50%%+". <a href="https://arxiv.org/abs/2310.16787">Longpre et al.</a></p></div>
</div>
<p class="small" style="margin-top:14px">Adjacent evidence. We found no study that measures invented datasets or wrong access claims directly, so this project measures them.</p>

<h2>What it does</h2>
<div class="steps">
  <div><i>1</i><b>Requirements</b><span>The question becomes a short list of must-haves.</span></div>
  <div><i>2</i><b>Search</b><span>Five registries, the literature, and the field's own repositories.</span></div>
  <div><i>3</i><b>Verify</b><span>Registry record, DOI or landing page. What could not be confirmed is marked as recalled.</span></div>
  <div><i>4</i><b>Access and licence</b><span>From the source, in plain words, with the steps and the time.</span></div>
  <div><i>5</i><b>Fit</b><span>Each requirement marked met, partly met or not met, with evidence.</span></div>
  <div><i>6</i><b>Answer and page</b><span>A ranked reply and an interactive page to compare and pick.</span></div>
</div>
<p class="small">It is a verification layer over existing registries, not a new search engine.</p>

<h2>The answer comes with a page</h2>
%(pagesblock)s

<h2>Does it beat Claude without the skill?</h2>
<p>The same model answers the same questions in fresh, isolated sessions. All arms have web search, page fetching and a shell. The questions and their answer keys were built from published papers and official pages by agents that never saw the skill, and graders check content only.</p>
%(results)s
<h4>What this does and does not show</h4>
<ul class="plain small">
  <li>The answer keys were built by Claude agents from published sources and re-checked on a different model. They were not written by human domain experts.</li>
  <li>The judge is a language model. Link checks are done by script.</li>
  <li>Famous datasets are known to every arm from training, so finding those measures little. The access facts and the less-known datasets carry most of the signal.</li>
  <li>Several access checks ask for an explicit statement of how the data is obtained. An answer that names a hosting site without saying whether an application is needed fails such a check.</li>
  <li>The sample of questions is small, and the web changes: access rules and links are those of the day of the run.</li>
</ul>
<p class="small">Protocol, written before the results: <code>docs/EVAL_PROTOCOL.md</code>. Reproduce with <code>tools/run_eval.sh</code>.</p>

%(demo)s

<h2>Install</h2>
%(install)s
<p>Then ask your question in plain words. It needs Python 3.9 or newer and outbound HTTPS, no packages and no API keys. The skill follows the open Agent Skills format, so other agents that load <code>SKILL.md</code> folders should be able to use it; it has been tested only in Claude Code.</p>

<h2>Limits</h2>
<ul class="plain">
  <li>It finds and checks. It does not download data or apply for access on your behalf.</li>
  <li>Access conditions and licences change. Every answer carries the date of the check.</li>
  <li>Registry metadata can be wrong; a licence chosen by an uploader is a claim. When a record is silent the skill reads the landing page, and when it cannot establish a fact it says so.</li>
  <li>Five registries are searched systematically; other repositories depend on web search. When a field keeps its data elsewhere, less is verified, and the answer says so.</li>
  <li>The interactive page is not always written; when it is not, the answer says so. The evaluation above counts how often.</li>
  <li>An answer costs more time and money than one without the skill; the table above gives both figures.</li>
</ul>

<footer>
<p>Built on existing registries and earlier work: <a href="https://github.com/musharna/data-aggregator-mcp">data-aggregator-mcp</a>, <a href="https://github.com/mobus-ai/Mobus">Mobus</a>, <a href="https://github.com/viswavi/datafinder">DataFinder</a>, <a href="https://github.com/GAIR-NLP/DatasetResearch">DatasetResearch</a>, and the idea from <a href="https://github.com/karpathy/autoresearch">karpathy/autoresearch</a> that a research workflow can be programmed as a Markdown file an agent follows. MIT licence.</p>
</footer>
</div>
<script>%(js)s</script>
""" % {"css": CSS, "js": JS, "results": results, "demo": demo,
       "pagesblock": pages_section(pages, result, pages_prefix, shots) or (
           '<p>Every completed run writes one self-contained page. Filter by access or licence, compare fit requirement by '
           'requirement, tick the datasets you want and export the access plan.</p>' + shot_html + sample_link),
       "install": install_section(owner, local_path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--arms", help="three_arms.json from tools/combine_arms.py")
    parser.add_argument("--audit", help="audit_summary.json from tools/audit_packets.py aggregate")
    parser.add_argument("--label", default="")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--verify-demo", help="text file with captured verifier output")
    parser.add_argument("--owner", default="OWNER", help="GitHub owner shown in the install command")
    parser.add_argument("--second", help="three_arms.json of the run on the second model")
    parser.add_argument("--second-label", default="")
    parser.add_argument("--pipeline", help="pipeline_use.json from tools/pipeline_use.py")
    parser.add_argument("--titles", help="JSON object: case name -> short description of the question")
    parser.add_argument("--trigger", help="trigger_summary.json from tools/trigger_test.py")
    parser.add_argument("--pages", help="pages_summary.json from tools/harvest_pages.py; the pages themselves are expected "
                                        "under <out-dir>/examples/heldout/<run>.html")
    parser.add_argument("--result", help="result.json of the run, for the wording of each question")
    parser.add_argument("--local-path", help="path of a local copy of the repository; adds the command that works without installing")
    parser.add_argument("--example-href", help="page written during a recorded run, relative to the site, e.g. examples/x.html")
    parser.add_argument("--example-question", default="", help="the question that page answers")
    parser.add_argument("--example-caption", default="", help="one sentence saying where the page comes from")
    parser.add_argument("--out-dir", default=os.path.join(REPO, "docs"))
    parser.add_argument("--full-name", default="index.html", help="file name of the complete page")
    parser.add_argument("--fragment-name", default="artifact.html", help="file name of the fragment; empty to skip it")
    parser.add_argument("--back", default="", help="href of the front page, shown as a link at the top")
    args = parser.parse_args()

    if args.titles and os.path.isfile(args.titles):
        TITLES.update(load(args.titles))
    arms_data = load(args.arms) if args.arms else None
    audit = load(args.audit) if args.audit and os.path.isfile(args.audit) else None
    demo = open(args.verify_demo, encoding="utf-8").read().rstrip() if args.verify_demo else ""
    shots = {}
    for key, name in (("top", "assets/report-top.png"), ("card", "assets/report-card.png"),
                      ("rule", "assets/example-rule.png"), ("best", "assets/example-best.png")):
        if os.path.isfile(os.path.join(args.out_dir, name)):
            shots[key] = name
    second = load(args.second) if args.second and os.path.isfile(args.second) else None
    example = {"href": args.example_href, "question": args.example_question, "caption": args.example_caption} \
        if args.example_href else None
    pipeline = load(args.pipeline) if args.pipeline and os.path.isfile(args.pipeline) else None
    pages = load(args.pages) if args.pages and os.path.isfile(args.pages) else None
    result = load(args.result) if args.result and os.path.isfile(args.result) else None
    if pages:
        rule, best = pick_pages(pages)
        print("example by the protocol's rule: %s; most verification stamps: %s" % (
            rule and rule["run"], best and best["run"]))
    trigger = load(args.trigger) if args.trigger and os.path.isfile(args.trigger) else None
    fragment = page(arms_data, audit, args.label, args.preview, demo, shots, args.owner, second, args.second_label, example,
                    args.local_path, pipeline, pages, result, trigger=trigger)
    if args.owner and args.owner != "OWNER":
        repo = "https://github.com/%s/dataset-shortlist" % args.owner
        fragment = fragment.replace("<code>docs/EVAL_PROTOCOL.md</code>", '<a href="%s/blob/main/docs/EVAL_PROTOCOL.md"><code>docs/EVAL_PROTOCOL.md</code></a>' % repo)
        fragment = fragment.replace("<code>tools/run_eval.sh</code>", '<a href="%s/blob/main/tools/run_eval.sh"><code>tools/run_eval.sh</code></a>' % repo)
        fragment = fragment.replace("<code>eval-runs/heldout-01/pages/</code>", '<a href="%s/tree/main/eval-runs/heldout-01/pages"><code>eval-runs/heldout-01/pages/</code></a>' % repo)
        fragment = fragment.replace("</footer>", '<p><a href="%s">Source on GitHub</a></p>\n</footer>' % repo, 1)
    if args.back:
        fragment = fragment.replace('<p class="eyebrow">An agent skill for Claude Code</p>',
                                    '<p class="eyebrow"><a href="%s">&larr; dataset-shortlist</a> &middot; every number</p>' % esc(args.back), 1)
    if args.fragment_name:
        with open(os.path.join(args.out_dir, args.fragment_name), "w", encoding="utf-8") as handle:
            handle.write(fragment)
    # The fragment opens with <title>, a meta tag and <style>; in the stand-alone page they belong in <head>.
    split = fragment.index('<div class="wrap">')
    head_part, body_part = fragment[:split], fragment[split:]
    document = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<meta name="description" content="An agent skill that finds research datasets you can actually obtain: '
                'each one checked against its registry record or landing page where possible, with access conditions and '
                'licence, and every fact marked as checked or recalled.">\n%s</head>\n<body>\n%s</body>\n</html>\n'
                % (head_part, body_part))
    with open(os.path.join(args.out_dir, args.full_name), "w", encoding="utf-8") as handle:
        handle.write(document)
    print("wrote %s%s" % (os.path.join(args.out_dir, args.full_name),
                          (" and " + os.path.join(args.out_dir, args.fragment_name)) if args.fragment_name else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
