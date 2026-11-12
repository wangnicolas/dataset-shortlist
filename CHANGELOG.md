# Changelog

## 0.1.2 (2026-11-12, first public release)

- Renamed from the working name `dataset-scout` to `dataset-shortlist`: the old name is taken by a package on PyPI and
  a repository on GitHub that also find datasets. The plugin, the skill, the marketplace and the folder the skill
  works in (`dataset-shortlist/`) carry the new name; the script (`scout.py`) and the environment variables keep
  theirs. The run records of the evaluation keep the old name.
- Author and copyright holder set to Nicolas Wang (plugin manifest, marketplace file, licence).
- The stated requirement is Python 3.9 or newer, the oldest version the tests run on.
- No change to what the skill does. The trigger test was repeated under the new name (`eval-runs/trigger-02/`).

## 0.1.1 (2026-11-12, after the held-out evaluation)

- The page shows access words written by hand as their tier. After reading a
  landing page the agent often wrote "application", "restricted", "registered"
  or "fee" where the page expects `gated`, `account` or `controlled`, and the
  page then showed "Unknown" for a condition that had been established. On the
  16 pages written in the held-out run this affected 31 of 85 datasets
  (`eval-runs/heldout-01/pages_summary.md`). `render` now maps words that state
  a restriction to their tier, prints what it mapped, and warns about text it
  cannot show. Nothing but the exact word `open` is ever read as open.
- The shortlist format reference lists the six tier words.

The main held-out run was not repeated: its graders read the text answer only
and never the page. The list of tier words is in a reference file the model
reads, though, so 0.1.1 is not identical to 0.1.0 in what the model sees. The
runs made later (Opus 5.5, and seven of the ten Fable 5.2 questions) used
0.1.1 and are marked as such wherever they are reported. The pages kept in
`eval-runs/heldout-01/pages/` are those written by 0.1.0, unchanged.

## 0.1.0 (2026-11-12)

The version measured in the held-out evaluation (commit `ef754f4`): five
registries, literature search, verifier, access and licence reading, the
interactive page.
