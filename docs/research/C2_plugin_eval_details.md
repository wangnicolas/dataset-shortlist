# `claude plugin eval` details for a one-skill plugin ("dataset-scout")
Checked 2026-11-11 against the local CLI 2.1.322.

Sources: **[doc]** https://code.claude.com/docs/en/plugin-evals.md (read in full, 735 lines); **[sbx]** https://code.claude.com/docs/en/sandboxing.md; **[cli]** `claude plugin eval --help`, `claude plugin eval init --help`. **INFERENCE** = my reasoning; **UNVERIFIED** = not confirmed. Nothing was executed.

## 1. Case format [doc "Eval suite reference"]
- **What counts as a case:** a directory under `evals/` (or `experimental.evals` in plugin.json, or `--eval-dir`) that holds `prompt.md`, `case.yaml`, or both. Nest cases under a non-case directory to group them.
- **Graders are mandatory:** a case with no grader fails to load (`invalid case.yaml` naming `graders`).
- **Templates:** `claude plugin eval init --bare <name>` writes a blank `prompt.md` + `graders/criteria.md`. Plain `init` runs an interview that needs a terminal [cli].

**prompt.md frontmatter.** The body is the prompt, sent verbatim (`@path` is not expanded). An unknown key is an error.

| Field | Default | Notes |
|---|---|---|
| `schema_version` | `"1.1"` (auto) | rarely set |
| `name` | directory name | `--case` globs match it |
| `description`, `expected_outcome` | — | for humans only |
| `tags` | `[]` | `--tag` keeps a case if any tag matches |
| `plugins` | nearest enclosing plugin | paths relative to the case dir; use `["../.."]` if auto-detection fails |
| `runs` | `3` | per arm, 1–50; `--runs` overrides |
| `model` | the child session's default | `--model` overrides |
| `max_turns` | `10` | up to 200; hitting the cap is a run error |
| `timeout_seconds` | `300` | up to 3600 |
| `allowed_tools` | `[]` | read-only tools listed here are granted; everything else needs `--allow-tools` (§3) |
| `append_system_prompt` | — | appended to the child's system prompt |
| `env` | `{}` | keys must match `EVAL_[A-Z0-9_]*`; any other key fails the run |

**case.yaml**
- `schema_version: "1.1"` and `name` are required.
- `description`, `tags`, `plugins`, `runs` and `expected_outcome` go at the top level. `model`, `max_turns`, `timeout_seconds`, `allowed_tools`, `append_system_prompt`, `env` and `prompt` go under `execution:`.
- case.yaml-only fields: `context.scaffold_script` (bash, only with `--scaffold`), `context.history_file` (a `.jsonl`; the prompt becomes the next turn), `context.add_dirs` (read-only dirs inside the case dir), and `graders:` (each entry a `name` plus grader keys; `llm` rubric in `criteria`).
- When both files exist, `prompt.md` frontmatter overrides case.yaml, and `graders/*.md` are appended after the case.yaml graders.

**Minimal dataset-scout case.** The answer path is a fixed name so graders can read it. This example shows the format only: plain Claude can name MIT-BIH and PTB-XL from memory, so Δ would sit near zero (a case scoring 1.0 in both arms proves nothing). Real cases need answers the baseline can't produce unaided. The skill must not set `disable-model-invocation: true`, or a natural-language prompt never triggers it.
`evals/ecg-arrhythmia/prompt.md`:
```markdown
---
tags: [smoke]
runs: 3
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill]
---
I need public ECG datasets with beat-level arrhythmia labels for a classification study.
Find candidates and write them to answer.md, one per line: `- <name> | <url> | <license> | <why it fits>`.
```
`evals/ecg-arrhythmia/graders/has-known-dataset.md`:
```markdown
---
type: regex
pattern: 'mit-bih|ptb-xl'
flags: i
target: { source: file, path: answer.md }
---
```
`evals/ecg-arrhythmia/graders/quality.md`:
```markdown
---
type: llm
focus: { source: file, path: answer.md }
weight: 2
---
PASS if every line names a real public dataset with a working-looking URL and a license, and at least 3 have beat-level arrhythmia labels.
FAIL if any entry is invented, has no URL, or lacks arrhythmia labels.
```
`evals/ecg-arrhythmia/graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?dataset-scout"'
---
```
Add `graders/answer-written.md` with `type: file_exists` and `path: answer.md` (shown inline below). The same case in case.yaml only:
```yaml
schema_version: "1.1"
name: ecg-arrhythmia
tags: [smoke]
runs: 3
execution:
  prompt: "I need public ECG datasets ... write them to answer.md ..."
  max_turns: 40
  timeout_seconds: 1200
  allowed_tools: [Read, Glob, Grep, Skill]
graders:
  - { name: answer-written, type: file_exists, path: answer.md }
  - { name: quality, type: llm, focus: { source: file, path: answer.md }, criteria: "PASS if ... FAIL if ..." }
```

## 2. Graders [doc "Grader frontmatter", "Grader types", "What a grader can look at", "How a case is scored"]
- **Common keys:** `type` (required), `weight` (default 1, any positive number), `arm` (`with-only` or `both`). The grader's name is its file name without `.md`. **There are no custom-code graders.**

| Type | Options | Passes when |
|---|---|---|
| `regex` | `pattern`, `flags`, `match` (`not_contains`, `"count:N"`; default = present), `target` | the JavaScript regex is found in the target. Use `flags: i`; inline `(?i)` is unsupported |
| `tool_used` | `tool`, `input_match`, `min` (1), `max` (∞) | the count of matching calls is within [min, max]. "Never called" = `min: 0, max: 0` |
| `tool_order` | `before`, `after` (a name or `{tool, input_match}`) | both were called and the first `before` precedes the first `after` |
| `file_exists` | `path` (glob), `exists` | a file **created during the run** matches (or none does, with `exists: false`) |
| `llm` | `criteria` (the file body), `focus` | the judge votes PASS in at least 2 of 3 votes |
| `baseline` | `baseline_file` (`.jsonl` in the case dir), `criteria` | the judge rates the run at least as good as the reference transcript |
- **What a grader sees** (`target` for regex, `focus` for llm): `last_message` (default, the final reply); `trace` (JSON lines, JSON-escaped; a regex sees all of it, an llm judge only the **first 12 and last 12** messages); `files` (the **paths** Claude created, not contents; scaffold-made or merely modified files excluded); `{ source: file, path: <p> }` (the **contents** of one workspace file after the run; images go to the judge as images, other binaries are refused); `mock_calls`.
- **Scoring:** a run's score is the weighted fraction of its scored graders that passed; a case's score is the mean of its with-arm runs and passes at `--threshold` (default **1.0**); `Δ` = with-arm minus without-arm. `llm` and `baseline` graders cost judge calls; the judge is "the model Claude Code uses for background tasks" [doc], "default: haiku" [cli], overridable with `--judge-model`.
- **Excluded from the score in two-arm runs** (still reported in the with-arm as a "plugin-fired indicator", `scored: false`):
  - every `tool_used` grader with `tool: Skill`;
  - `mock_calls` graders when the mocked servers are the plugin's own;
  - any grader marked `arm: with-only`.
  If *every* grader is excluded, they are all scored. `arm: both` forces scoring in both arms. `--ablation none` excludes nothing.
- **Doc advice:** grade long output with a `regex` over the file's contents, and keep `llm` for short output with concrete PASS/FAIL rubrics. Pair one grader on the result with one on the process. If `tool_used: Skill` passes but Δ is negative, suspect the judge and re-run with `--judge-model sonnet`.

## 3. Tools, sandbox and network [doc "Grant tools", "How runs are isolated"; sbx]
- **No prompts:** runs never stop to ask. A gated tool you didn't grant is removed from the session.
- **Read-only set:** granted only when listed in `allowed_tools`: `Read`, `Glob`, `Grep`, `NotebookRead`, `Skill`, `AskUserQuestion`, `Agent`, `TodoWrite`, `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate`, `TaskStop`.
  - The [cli] `--disallow-tools` text ("even if granted (e.g. Agent TaskStop)") suggests some of these are offered by default (UNVERIFIED).
- **Gated tools** (need `--allow-tools`):
  - [doc]: `Bash`, `Write`, `Edit`, `WebFetch`, **`WebSearch`**.
  - [cli]: "Bash, Write, Edit, WebFetch, mcp__*", with "Supports Tool(pattern:*) syntax".
  - The grant applies **to every case in the run**.
  - Neither a case's `allowed_tools` nor the skill's own `allowed-tools` frontmatter can widen grants.
- **Grant examples:** `Write`, `WebSearch`, `"Bash(python3 *)"` (doc form: `"Bash(npm test *)"`), `"WebFetch(domain:huggingface.co)"`, `"mcp__plugin_<plugin>_<server>__*"` (real servers only).
- **Bash runs under the OS sandbox** whenever Bash is granted in any form:
  - Writes are confined to the run's workspace.
  - **Your home directory and Claude Code configuration are unreadable.**
  - **Network is limited to domains you grant with `--allow-tools "WebFetch(domain:…)"`.**
  - With no sandbox backend, each run is refused: native Windows has none (use WSL2); Linux needs `bubblewrap` and `socat`. macOS uses its built-in Seatbelt.
- **How the network works [sbx]:** sandboxed commands go through a local proxy set via `HTTP_PROXY`/`HTTPS_PROXY`/`ALL_PROXY`; on macOS Seatbelt blocks every other connection. Proxy-aware tools (`curl`, `npm`, git over HTTPS) work; tools that ignore the proxy fail with `Operation not permitted` or `Could not resolve host`. Only a leading `*.` or a bare `*` wildcard applies to sandboxed commands.
- INFERENCE: Python `urllib` reads `HTTPS_PROXY` by default, so `urlopen` should work; don't install an empty `ProxyHandler` or open raw sockets.
- **How to open the network for a suite:** only through the CLI grant above. [doc] documents no network field in `prompt.md`, `case.yaml` or plugin.json, and runs don't load your user or project settings (managed policy still applies). The `WebFetch` tool itself is not sandboxed: a `WebFetch(domain:…)` grant reaches that domain directly, and plugin hooks or real MCP servers can reach any host.
```bash
claude plugin eval . --trust-plugin \
  --allow-tools Write WebSearch "Bash(python3 *)" \
    "WebFetch(domain:huggingface.co)" "WebFetch(domain:*.huggingface.co)" \
    "WebFetch(domain:physionet.org)" "WebFetch(domain:zenodo.org)" "WebFetch(domain:www.kaggle.com)" \
  --runs 3 -j 2 --model claude-sonnet-5 --judge-model sonnet --threshold 0.8 --no-publish --max-cost-usd 15 --json results.json
```
Put the target (`.`) **before** `--allow-tools` and `--json`, because both take values. The command exits 1 if any case is below `--threshold`, so run the §4 `jq` gate as a separate step, not chained with `&&`. Per [doc], `--json` makes the run quiet, so debug without it.

## 4. The baseline arm [doc "The no-plugin baseline", "Score against the no-plugin baseline"]
- **What it is:** the case's runs "repeated with no plugin loaded": the same number of runs, the same prompt and case limits. `--allow-tools` "applies to every case in the run", `--model` sets the model for all cases, and every run gets the same per-run isolation.
- **What it lacks:** no skill, no plugin agents (dispatching one fails with `Agent type '<plugin>:<agent>' not found`), no hooks, and none of the plugin's scripts or `bin/`.
- INFERENCE: the without-arm therefore gets the same granted WebSearch/WebFetch/Bash network. Δ measures the skill over plain Claude with identical tools, which is the comparison you want. If you grant no network, the baseline can't search either. The docs imply equal tools, model and sandbox rather than stating each one (UNVERIFIED in detail).
- **Default ablation** is `with-without` whenever a plugin resolves [cli]. A case runs one arm under `--ablation none`, for a `history_file` case with a path target, or when no plugin resolved. In that last case, add `plugins: ["../.."]`.
- **Gating:** Δ is reported but **never changes the exit code**. To gate on "with beats without", read the JSON:
  ```bash
  jq -e '.aggregates.meanDelta > 0 and ([.cases[].aggregates.delta // 0] | min) >= 0' results.json
  ```

## 5. Outputs [doc "Read the results", "JSON result", "HTML report"; cli]
- **Where results go:** `<plugin>/evals/results/<timestamp>/` holds `aggregate-result.json` and `report.html` for a path target. For a named installed plugin they go to `./evals/results/`. Override with `--output-dir <dir>` and `--report <path>`. Add `results/` to `.gitignore`.
- **`--json [file.json]`:** the same document as `aggregate-result.json` (`schemaVersion: 1`, camelCase, additive-only). Per [cli] it holds "prompts, graders, per-run scores". Per [doc] it also carries the suite config, every grader definition, and per-run grader results with explanations and evidence. Key fields: `partial`/`partialReason` (`cost_ceiling`, `interrupted`, `auth_failed`); `aggregates.{overallScore, casesPassed, casesTotal, meanDelta}`; `cases[].aggregates.{score, delta}`; `cases[].arms.{with,without}[]` with `.error`, `.aborted`, `.skippedPaidGraders`; `costUsd`, `durationSeconds`, `claudeVersion`.
  The final assistant text and the list of written files are **not documented as fields**. They appear only as grader evidence: a `regex` on `last_message`, or a grader with `target: files` (UNVERIFIED).
- **HTML report:** self-contained, no external requests. It shows a verdict line and tiles (suite score, ablation Δ, baseline score, cases passing, perfect runs), per-case cards with Δ and a threshold tick, with-arm then baseline runs with grader chips, the judge's votes and evidence for `llm` graders, and each case's prompt and grader rubrics.
- **Publishing:** with a claude.ai subscription sign-in and artifacts available, the report is also published "as a private artifact" (`Published: <url>`). `--no-publish` keeps it local; API-key auth never publishes; runs started by a Claude Code session stay local unless `--publish-report`. Who can see a private artifact is not spelled out here (UNVERIFIED).
- **Cost:** each case row has a `COST` column and the summary line gives a total. `costUsd` is a **list-price estimate** that includes judge calls, not your plan usage. `--max-cost-usd` is checked before each run starts; the overrun is bounded by the runs already in flight, and hitting it exits 2 with a partial result.

## 6. Working directory and files [doc "How runs are isolated", "Seed the workspace"]
- **Fresh workspace:** each run gets a temporary home, working directory and Claude Code config, and runs as a `claude -p` child with only the plugin loaded.
  - Nothing personal or project-level loads: no user settings, CLAUDE.md, MCP servers or other plugins.
  - The run **can't read the eval directory**, so the graders stay hidden from it.
  - Only an env allowlist (PATH, locale, proxy and certificate vars, provider and auth vars, most `ANTHROPIC_*` and `CLAUDE_CODE_*`) plus `EVAL_*` reaches it. Pass registry tokens as `EVAL_*` and read those names in your scripts.
- **Inputs:** inline in the prompt; `context.add_dirs` (read-only dirs inside the case dir; Claude needs `Read`; where they appear in the run is UNVERIFIED); `context.scaffold_script` (runs as you **outside** the sandbox, only with `--scaffold`, 120 s limit, minimal env); `context.history_file`.
- **Outputs:** files the agent creates stay in the workspace for the graders (`files` for paths, `{source: file}` for contents). `--keep-temp` "keeps every run's sandbox directory and prints its path" [doc]; [cli] describes it as "Preserve scaffold dirs for debugging".

## 7. Limits and caveats [doc "Requirements", "Troubleshooting"]
- **Requirements:** Claude Code **v2.1.269+** (local 2.1.322 meets it); git **≥ 2.31** if installed (older git stops the suite, checked since v2.1.283); a plugin manifest; the same auth and provider as your sessions. Every run and judge call is real usage.
- **Volume:** about cases × runs × 2 agent runs, plus 3 judge calls per `llm` or `baseline` grader per run. `-j 1–8` shares **one** rate limit and only shortens wall-clock time.
- **Rate and usage limits:** a run that ends on a rate- or usage-limit error scores 0 without grading. The command then exits non-zero (baseline runs count too), and the result is not marked partial.
- **Trust:** a first run in an untrusted directory under `--json`, without a TTY, or in CI is refused (exit 1) unless you pass `--trust-plugin`.
- **Exit codes:** 0 / 1 / 2 (cost ceiling or auth) / 130 / 143. The default `--threshold 1.0` exits 1 unless every case is perfect.
- **Run limits:** the defaults of 10 turns and 300 s are too small for web research. Raise them toward 200 turns and 3600 s and use `--max-cost-usd` as the budget.
- **Isolation gaps:** the Artifact tool is off; managed policy still applies; plugin hooks and real MCP servers run outside the sandbox, so treat scores as advisory for untrusted hooks. INFERENCE: plugin monitors won't start, because the child is `claude -p`.
- **macOS:** no documented incompatibility; Seatbelt is built in. Tools that ignore the proxy fail there.
- **Risk to test first (INFERENCE):** "home directory ... unreadable" for Bash could break `python3 "${CLAUDE_SKILL_DIR}/scripts/..."` if the plugin checkout or the `python3` on PATH (e.g. Anaconda) lives under `$HOME`. Smoke-test with one case: `claude plugin eval . --case ecg-arrhythmia --runs 1 --ablation none --keep-temp --allow-tools "Bash(python3 *)" "WebFetch(domain:physionet.org)" Write` (no `--json`).
