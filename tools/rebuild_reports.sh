#!/bin/bash
# Rebuild everything that is derived from the held-out records: the combined tables, the written
# report, the results block of the README and the showcase page. Nothing here calls a model.
#
#   tools/rebuild_reports.sh [--owner <github-owner>] [--local-path <path of this repository>]
#
# Inputs (all under eval-runs/):
#   heldout-01            with the skill / no skill, Sonnet          (tools/run_eval.sh)
#   heldout-01-prompted   no skill, told to search and verify        (tools/run_eval.sh)
#   heldout-01-opus       Opus on the ten questions, if present      (tools/run_eval.sh)
#   heldout-01-fable-all  Fable on all ten questions                 (tools/run_eval.sh twice, tools/merge_runs.py)
#   heldout-01/audit      blind audit, if present                    (tools/audit_packets.py)
#   trigger-01            trigger test, if present                   (tools/trigger_test.py)
# The pages written during the run are collected by tools/harvest_pages.py, which needs the
# evaluation tool's kept folders on the machine that ran it; its output is part of the records.
set -eu
cd "$(dirname "$0")/.."
PY=${PYTHON:-python3}
OWNER=OWNER
LOCAL=""
SITE_OUT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --owner) OWNER=$2; shift 2 ;;
    --local-path) LOCAL=$2; shift 2 ;;
    --site-out) SITE_OUT=$2; shift 2 ;;   # build only the page, into this folder (it must hold assets/ and examples/)
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done

MAIN=eval-runs/heldout-01
PROMPTED=eval-runs/heldout-01-prompted
FABLE=eval-runs/heldout-01-fable-all      # joined by tools/merge_runs.py from heldout-01-fable and heldout-01-fable-rest7
TRIGGER=eval-runs/trigger-01
TITLES=docs/eval/heldout_case_titles.json
LABEL="Ten sealed questions, Sonnet 5.5 (claude-sonnet-5-5), three runs per arm, 12 November 2026"
FABLE_LABEL="Fable 5.2 (claude-fable-5-2), the ten questions, two runs per arm, 11 and 12 November 2026"
FABLE_NOTE="Three of these questions were run as the protocol planned, with version 0.1.0 of the skill; the other seven were added after the result above was known, with version 0.1.1. The rule was set for the main comparison only, so this is reported as a description. An earlier run of Fable 5.2 without the skill on three of the seven (eval-runs/heldout-01-fable-plain3, three runs each: skin tone 1.00, linked employer-employee data 0.92, galaxy images 0.62) is kept beside this one and is not part of these means; counted in, the skin-tone question would read the same instead of higher."
OPUS=eval-runs/heldout-01-opus
OPUS_LABEL="Opus 5.5 (claude-opus-5-5), the ten questions, three runs per arm, 12 November 2026"
OPUS_NOTE="This run was made after the result above was known, with version 0.1.1 of the skill. The rule was set for the main comparison only, so this is reported as a description."

$PY tools/combine_arms.py $MAIN $PROMPTED > /dev/null
# The session traces are large and stay on the machine that ran the evaluation; without them the
# recorded summary of how the runs used the workflow is kept as it is.
if [ -d $MAIN/traces ]; then $PY tools/pipeline_use.py $MAIN > /dev/null; else echo "no traces here: keeping $MAIN/pipeline_use.json as recorded"; fi

args_second=(); report_second=(); args_audit=(); args_trigger=()
# further models on the same questions, in the order they are reported
if [ -f $OPUS/summary.json ]; then
  $PY tools/combine_arms.py $OPUS - > /dev/null
  args_second+=(--second $OPUS/three_arms.json --second-label "$OPUS_LABEL" --second-note "$OPUS_NOTE")
  report_second+=(--second $OPUS --second-label "$OPUS_LABEL" --second-note "$OPUS_NOTE")
fi
if [ -f $FABLE/summary.json ]; then
  $PY tools/combine_arms.py $FABLE - > /dev/null
  args_second+=(--second $FABLE/three_arms.json --second-label "$FABLE_LABEL" --second-note "$FABLE_NOTE")
  report_second+=(--second $FABLE --second-label "$FABLE_LABEL" --second-note "$FABLE_NOTE")
fi
if ls $MAIN/audit/*/audit.json > /dev/null 2>&1; then
  $PY tools/audit_packets.py aggregate $MAIN > /dev/null
  args_audit=(--audit $MAIN/audit_summary.json)
fi
args_trigger_json=()
[ -f $TRIGGER/trigger_summary.md ] && args_trigger=(--trigger $TRIGGER)
[ -f $TRIGGER/trigger_summary.json ] && args_trigger_json=(--trigger $TRIGGER/trigger_summary.json)

if [ -z "$SITE_OUT" ]; then
$PY tools/make_report.py --main $MAIN --prompted $PROMPTED ${report_second[@]+"${report_second[@]}"} ${args_trigger[@]+"${args_trigger[@]}"} \
  --titles $TITLES --label "$LABEL" --out docs/eval/heldout_report.md

$PY tools/fill_readme.py --arms $MAIN/three_arms.json ${args_audit[@]+"${args_audit[@]}"} ${args_second[@]+"${args_second[@]}"} \
  --pipeline $MAIN/pipeline_use.json --titles $TITLES --label "$LABEL" --records docs/eval/heldout_report.md \
  ${args_trigger_json[@]+"${args_trigger_json[@]}"}
fi

site_out=()
[ -n "$SITE_OUT" ] && site_out=(--out-dir "$SITE_OUT")
site_local=()
[ -n "$LOCAL" ] && site_local=(--local-path "$LOCAL")
# The page with every number (docs/evidence.html) ...
$PY tools/build_site.py --arms $MAIN/three_arms.json ${args_audit[@]+"${args_audit[@]}"} ${args_second[@]+"${args_second[@]}"} \
  --pipeline $MAIN/pipeline_use.json --pages $MAIN/pages_summary.json --result $MAIN/result.json \
  --titles $TITLES --label "$LABEL" --verify-demo docs/assets/verify-demo.txt --owner "$OWNER" \
  --full-name evidence.html --fragment-name "" --back index.html \
  ${site_local[@]+"${site_local[@]}"} ${site_out[@]+"${site_out[@]}"} ${args_trigger_json[@]+"${args_trigger_json[@]}"}
# ... and the showcase page in front of it (docs/index.html, docs/artifact.html).
$PY tools/render_examples.py > /dev/null
$PY tools/build_showcase_data.py > /dev/null
$PY tools/build_showcase.py --owner "$OWNER" ${site_local[@]+"${site_local[@]}"} ${site_out[@]+"${site_out[@]}"}

find . -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null || true
if [ -n "$SITE_OUT" ]; then echo "page built in $SITE_OUT"; else
echo "rebuilt: docs/eval/heldout_report.md, README.md (results block), docs/index.html, docs/artifact.html, docs/evidence.html"; fi
