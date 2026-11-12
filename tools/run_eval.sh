#!/usr/bin/env bash
# Run the with-skill versus without-skill comparison (see docs/EVAL_PROTOCOL.md).
#
#   tools/run_eval.sh <eval-dir-name> <output-dir> [extra `claude plugin eval` options]
#
# Examples:
#   tools/run_eval.sh evals          eval-runs/dev-01     --model sonnet --runs 1 -j 4
#   tools/run_eval.sh evals-heldout  eval-runs/heldout-01 --model sonnet --runs 3 -j 4 --max-cost-usd 150
#
# These are real, billed model runs. Each case runs in fresh isolated sessions,
# with and without the plugin, with identical tools. The report is never
# published (--no-publish).
set -euo pipefail

REPO=$(cd "$(dirname "$0")/.." && pwd)
# The third arm ("no skill, told to verify") runs against an empty plugin:
#   python3 tools/make_prompted_arm.py plugins/dataset-shortlist/evals evals-prompted
#   SCOUT_EVAL_PLUGIN=tools/no-skill-plugin tools/run_eval.sh evals-prompted eval-runs/dev-01-prompted --ablation none --model sonnet --runs 1 -j 4
PLUGIN="${SCOUT_EVAL_PLUGIN:-$REPO/plugins/dataset-shortlist}"
case "$PLUGIN" in /*) ;; *) PLUGIN="$REPO/$PLUGIN" ;; esac
EVAL_DIR=${1:?name of the eval directory below the plugin, e.g. evals}
OUT=${2:?output directory}
shift 2
case "$EVAL_DIR" in
  *heldout*)
    # The held-out run is made once, from the frozen commit (docs/EVAL_PROTOCOL.md).
    dirty=$(git -C "$REPO" status --porcelain -- . ':!eval-runs' | grep -v "evals-heldout" || true)
    if [ -n "$dirty" ]; then
      echo "refusing to run a held-out directory from a working tree with uncommitted changes:" >&2
      echo "$dirty" >&2
      exit 1
    fi
    ;;
esac
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)

# `claude plugin eval` needs git 2.31 or newer; some machines have an older git first on PATH.
GITBIN=$(mktemp -d)
for candidate in /usr/bin/git /opt/homebrew/bin/git /usr/local/bin/git "$(command -v git || true)"; do
  [ -x "$candidate" ] || continue
  version=$("$candidate" --version | awk '{print $3}')
  major=${version%%.*}; rest=${version#*.}; minor=${rest%%.*}
  if [ "$major" -gt 2 ] || { [ "$major" -eq 2 ] && [ "$minor" -ge 31 ]; }; then
    ln -sf "$candidate" "$GITBIN/git"
    break
  fi
done
[ -e "$GITBIN/git" ] || { echo "no git >= 2.31 found" >&2; exit 1; }
export PATH="$GITBIN:$PATH"

{
  echo "started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "skill commit: $(git -C "$REPO" rev-parse HEAD) $(git -C "$REPO" status --porcelain | grep -q . && echo '(working tree has uncommitted changes)' || echo '(clean)')"
  echo "claude: $(claude --version)"
  echo "eval dir: $EVAL_DIR"
  echo "extra options: $*"
} > "$OUT/run-info.txt"

cd "$PLUGIN"
set +e
claude plugin eval . --eval-dir "$EVAL_DIR" --trust-plugin --no-publish --keep-temp \
  --judge-model sonnet --output-dir "$OUT" --json "$OUT/result.json" --report "$OUT/report.html" \
  "$@" --allow-tools Bash Write Edit WebSearch "WebFetch(domain:*)" > "$OUT/eval.log" 2>&1
status=$?
set -e
echo "claude plugin eval exit status: $status (1 only means some case scored below the threshold)" >> "$OUT/run-info.txt"
echo "finished: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUT/run-info.txt"

python3 "$REPO/tools/analyze_eval.py" "$OUT/result.json" "$OUT"
cat "$OUT/run-info.txt"
