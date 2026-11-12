#!/usr/bin/env bash
# Stage the sealed held-out cases for the one held-out run (docs/EVAL_PROTOCOL.md).
#
#   tools/stage_heldout.sh <folder with the sealed case folders>
#
# It copies the cases into the plugin without printing any of their content, adds
# the unscored "skill was invoked" indicator, prepares the "no skill, told to
# verify" copies for the third arm, and prepares the three-case subset for the
# second model. Run it only after the skill commit is frozen and recorded.
set -euo pipefail
REPO=$(cd "$(dirname "$0")/.." && pwd)
SRC=${1:?folder that holds the sealed case folders}
PLUGIN="$REPO/plugins/dataset-shortlist"

if [ -n "$(git -C "$REPO" status --porcelain -- . ':!eval-runs' | grep -v 'evals-heldout' || true)" ]; then
  echo "the working tree has uncommitted changes; commit and record the frozen commit first" >&2
  exit 1
fi

python3 "$REPO/tools/check_cases.py" "$SRC" > /tmp/heldout-structure.$$ || { cat /tmp/heldout-structure.$$; rm -f /tmp/heldout-structure.$$; exit 1; }
tail -1 /tmp/heldout-structure.$$; rm -f /tmp/heldout-structure.$$

rm -rf "$PLUGIN/evals-heldout" "$PLUGIN/evals-heldout-subset"
mkdir -p "$PLUGIN/evals-heldout" "$PLUGIN/evals-heldout-subset"
cp -R "$SRC"/. "$PLUGIN/evals-heldout/"
python3 "$REPO/tools/add_skill_indicator.py" "$PLUGIN/evals-heldout"

# Second-model subset: the first two health cases and the first other-field case, by name.
count=0
for name in $(cd "$PLUGIN/evals-heldout" && ls -d ho-h-* 2>/dev/null | sort | head -2) $(cd "$PLUGIN/evals-heldout" && ls -d ho-o-* 2>/dev/null | sort | head -1); do
  cp -R "$PLUGIN/evals-heldout/$name" "$PLUGIN/evals-heldout-subset/$name"
  count=$((count + 1))
done
echo "subset for the second model: $count case(s)"

python3 "$REPO/tools/make_prompted_arm.py" "$PLUGIN/evals-heldout" evals-heldout-prompted
echo "frozen commit: $(git -C "$REPO" rev-parse HEAD)"
echo "staged: $(ls "$PLUGIN/evals-heldout" | wc -l | tr -d ' ') case(s)"
