# Claude Code mechanics for an autonomous ML-research plugin
Checked 2026-11-11 against the local CLI **2.1.322** (`claude --version`). Tags: **[doc]** = page fetched this session (base `https://code.claude.com/docs/en/`); **[cli]** = local help output; **(paraphrase)** = condensed fetch output, not verbatim; **INFERENCE** = my reasoning; **UNVERIFIED** = not confirmed.

## 1. Plugin layout and distribution
Sources: [doc] `plugins/create.md`, `plugins/components.md`, `plugins/manifest-reference.md`, `plugins/create-marketplace.md`, `plugins/install.md`, `plugin-evals.md`; [cli] `claude plugin --help`, `claude plugin {validate,install,init,eval} --help`, `claude plugin marketplace add --help`, `claude --help`.
```text
autoresearch/                      # plugin root = what --plugin-dir points at
├── .claude-plugin/plugin.json     # ONLY file allowed in .claude-plugin/ (components there don't load)
├── skills/<skill>/SKILL.md        # + scripts/, references/ beside it
├── agents/<agent>.md              # subfolders become name segments (plugin:sub:agent)
├── commands/<cmd>.md              # legacy; write skills instead
├── hooks/hooks.json               # top-level "hooks" key, same shape as settings.json
├── workflows/<name>.js            # runs as /autoresearch:<meta.name>
├── monitors/monitors.json         # background watchers; do NOT start under -p
├── bin/<exe>                      # on the Bash tool's PATH while enabled (can't shadow system cmds)
├── settings.json                  # only `agent` and `subagentStatusLine` take effect
└── .mcp.json  .lsp.json  evals/<case>/prompt.md + graders/*.md
```
- `name` is the only required manifest key (kebab-case; no spaces, `@`, `:`). Names starting `claude-`, `anthropic-`, `cc-plugin-` are an error. Component paths must start with `./` and stay inside the root (no `..`). `commands`, `agents`, `outputStyles` and `workflows` **replace** their default folder; `skills` **adds**; `hooks`, `mcpServers` and `lspServers` **merge**.
- A root `CLAUDE.md` is **not** loaded, and validate warns about it. Ship instructions as skills.
- **Design constraint:** plugin `settings.json` honours only `agent` and `subagentStatusLine`. A plugin **cannot ship** permission rules, sandbox config or `advisorModel`. Those must come from a launcher (`--settings file.json`, `--advisor`) or from documented project settings.
- `${CLAUDE_PLUGIN_ROOT}` changes on every update, so don't write state there. `${CLAUDE_PLUGIN_DATA}` (`~/.claude/plugins/data/<id>/`) survives updates and fits a venv. claude.ai/Cowork refuse a plugin that has a top-level `bin/`.
```json
{ "name": "autoresearch", "version": "0.1.0", "description": "Autonomous ML-research workflow",
  "author": { "name": "YOUR NAME" }, "license": "MIT", "repository": "https://github.com/OWNER/REPO", "keywords": ["ml-research", "autoresearch"] }
```
**Marketplace** (`<repo>/.claude-plugin/marketplace.json`; `name`, `owner` and `plugins[]` are required; the entry `name` must equal plugin.json `name`):
```json
{ "name": "autoresearch-marketplace", "owner": { "name": "YOUR NAME" },
  "plugins": [ { "name": "autoresearch", "source": "./plugins/autoresearch",
                 "description": "Autonomous ML-research workflow" } ] }
```
Write relative sources from the marketplace root, the directory that contains `.claude-plugin/`. Other source types: `{"source":"github","repo":"owner/repo"}`, `git-subdir`, `url`, `archive`, `npm`, `command`. Third-party marketplaces have auto-update **off** by default.
**End-user install** ([doc] install.md; under `claude -p`, `/plugin` is unavailable but installed plugins load):
```text
/plugin marketplace add OWNER/REPO            # optionally OWNER/REPO#v0.1.0
/plugin install autoresearch@autoresearch-marketplace   # opens panel, user picks scope
```
```bash
claude plugin marketplace add OWNER/REPO
claude plugin install autoresearch@autoresearch-marketplace --scope user   # user|project|local
claude plugin install autoresearch --marketplace OWNER/REPO                # one step, v2.1.292+
```
**Developer testing:** `claude --plugin-dir ./plugins/autoresearch` loads a directory or `.zip` for one session; the flag repeats, and a folder of plugins loads each child. Alternatives: `--plugin-url <zip>`, the env var `CLAUDE_CODE_PLUGIN_DIRS`, and `claude plugin init <name>`, which scaffolds `~/.claude/skills/<name>/` that loads as `<name>@skills-dir`. Run `/reload-plugins` after edits. To test the marketplace locally, run `claude plugin marketplace add ./my-marketplace`. Pointing `--plugin-dir` at a marketplace root silently loads nothing.
**`claude plugin validate <path> [--strict] [--json] [--profile directory]`** exists [cli]. It checks:
- manifest types and fields, and that paths exist and stay contained (unknown top-level fields are warnings);
- the frontmatter of every skill, agent and command;
- `.mcp.json` entries (v2.1.281+);
- `marketplace.json` syntax, required fields, names and `..` paths;
- an unquoted `${CLAUDE_PLUGIN_ROOT}` in a shell-form hook (warning).
It does not read `.lsp.json` and does not fetch remote sources. Related commands: `claude plugin details <name>` (component inventory and token cost) and `claude plugin tag` (release tag). **`claude plugin eval [target]`** is a behaviour test harness. It runs each `evals/<case>/` (`prompt.md` + `graders/*.md`, or `case.yaml`) in fresh, isolated `claude -p` sessions, by default 3 runs **with** and 3 **without** the plugin, and reports Δ. `claude plugin eval init` interviews you and writes the cases. Exit codes: 0 = pass, 1 = below threshold or error, 2 = partial (cost ceiling or auth), 130 = interrupted, 143 = terminated. Needs v2.1.269+ [doc plugin-evals.md]. CI form from the doc:
```bash
claude plugin eval . --trust-plugin --json results.json --threshold 0.8 \
  --model claude-sonnet-5 --judge-model claude-haiku-4-5 --no-publish --max-cost-usd 20
```

## 2. Skills  ([doc] `skills.md`; the field rows below were re-fetched verbatim and shortened here)
| Field | Semantics |
|---|---|
| `name` | Command name; defaults to the directory name. In a plugin it replaces the last segment of `/plugin:<name>` |
| `description` | When to use the skill. `description` + `when_to_use` are truncated at **1,536 chars** in the listing; if absent, the first body line is used |
| `argument-hint` / `arguments` | Autocomplete hint / named positional args for `$name` |
| `disable-model-invocation: true` | User-only (`/name`). Also blocks preloading into subagents and firing from a session-scheduled task |
| `user-invocable: false` | Claude-only; hidden from the `/` menu |
| `allowed-tools` | No permission prompts **during the invoking turn only**; the grant clears on your next message. String or YAML list |
| `disallowed-tools` | Removed while the skill is active (doc example: `AskUserQuestion` for a background loop) |
| `model` / `effort` | Override for the rest of the turn. With `context: fork` they set the fork's model/effort. `inherit` is allowed |
| `context: fork` + `agent: <type>` (+`background: false` to wait) | Run the skill in a forked subagent of that type |
| `hooks` | Registered on invocation and kept **for the rest of the session** (`once: true` available) |
| `paths` | Globs that limit auto-activation to matching files (relative to the cwd) |
| `when_to_use`, `shell` (bash/powershell for `!` blocks), `metadata`, `license`, `compatibility` | From a condensed fetch (paraphrase) |
**Substitutions:** `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}` (the folder holding SKILL.md), `${CLAUDE_PROJECT_DIR}`, and `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` (plugin skills only). Write `\$` for a literal `$`. If no placeholder is used, the args are appended as `ARGUMENTS: <value>`. **The path variables are substituted into the Markdown body; they are NOT in the environment of Bash-tool commands** ([doc] manifest-reference "Environment variables"). So either write the path into the body or put the CLI in `bin/`.
**Dynamic context:** inline `` !`git status --short` `` or a fenced block opened with ```` ```! ````. Output replaces the placeholder before Claude sees the skill. A non-zero exit **aborts the invocation**. The setting `disableSkillShellExecution: true` turns this off.
**Namespacing:** `skills/run-experiment/SKILL.md` in plugin `autoresearch` runs as `/autoresearch:run-experiment`. Plugin and local skills don't collide. **Size:** keep SKILL.md **under 500 lines** and move reference material into linked files. After auto-compaction, each skill's latest invocation is re-attached (first 5,000 tokens; 25,000 tokens total across skills). Every skill's description costs context on every turn.
```markdown
---
name: run-experiment
description: Run one autoresearch iteration (edit train.py, train, log val metric). Use when the loop asks for the next experiment.
argument-hint: [experiment-id]
allowed-tools:
  - Bash(python3 *)
  - Read
---
Recent history:
!`git log --oneline -5`

Run `python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" $ARGUMENTS` and report the metric line.
```
A skill the loop must call on its own can't set `disable-model-invocation: true`. Use that flag only on a user-started entry point such as `/autoresearch:start`.

## 3. Subagents in plugins  ([doc] `sub-agents.md`, `plugins/components.md`)
- Fields: `name` (required, ≤256 chars, no `:`), `description` (required), `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `autoCompactWindow`, `skills` (preloads full content), `mcpServers`, `hooks`, `memory` (user/project/local), `background`, `omitClaudeMd`, `effort` (low…max), `isolation` (only `worktree`), `color`, `initialPrompt`, `experimental.cacheTtl`.
- **Plugin agents IGNORE `permissionMode`, `hooks`, `mcpServers` and `initialPrompt`.** Ship hooks via `hooks/hooks.json` and servers via `.mcp.json`. If the frontmatter fails to parse, the agent loads with every field ignored.
- `model`: `sonnet` | `opus` | `haiku` | `fable` | a full ID (e.g. `claude-opus-5-5`) | `inherit`. Resolution order: per-call parameter → frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → main model. The Agent tool's per-call `model` accepts **only aliases**.
- Naming: `agents/reviewer.md` loads as `autoresearch:reviewer`; invoke it with `@agent-autoresearch:reviewer`. Precedence: managed > `--agents` > `.claude/agents/` > `~/.claude/agents/` > plugin. Subagents can nest 3 levels by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). If the main session is in bypass, acceptEdits or auto, that mode wins over a subagent's.
```markdown
---
name: reviewer
description: Independently re-checks a claimed metric improvement before it is kept. Use after each experiment.
tools: Read, Grep, Glob, Bash
model: opus
effort: high
---
You verify experiment results. Re-run the eval command, compare against results.tsv, report KEEP or DISCARD with evidence.
```

## 4. Hooks in plugins  ([doc] `hooks.md`, `hooks-guide.md`, `plugins/components.md`)
- **Location:** `hooks/hooks.json` with a top-level `"hooks"` wrapper; the manifest `hooks` key merges with it. **Plugin hooks fire automatically in every session where the plugin is enabled**, not only when a skill runs. Gate them with `matcher`, `if`, or a state-file check inside the script.
- **Exceptions:** `--bare` skips plugin hooks, even for a `--plugin-dir` plugin, and the docs say `--bare` "will become the default for `-p`". `--safe-mode` also disables them. A loop that depends on its hooks must not use `--bare`.
- **Subagents:** tool events inside subagents fire the same hooks; the input carries `agent_id` and `agent_type`. To match a plugin agent type exactly, anchor it: `^autoresearch:reviewer$`.
- **Events:** SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, MessageDisplay, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, SessionEnd.
- **Matcher:** `"*"`, `""` or omitted matches all. A value of only letters, digits, `_`, `-`, spaces, `,` and `|` is an exact name or list (`Edit|Write`). Any other character makes it an unanchored JS regex. Plugin MCP tools are `mcp__plugin_<plugin>_<server>__<tool>`. The per-handler `if` (permission-rule syntax, e.g. `"Bash(git *)"`) is best-effort; the docs say to use the permission system for hard allow/deny.
- **Exit codes:** 0 means stdout is parsed as JSON if it is one object. **2 blocks**, and for PreToolUse stderr goes to Claude as the denial reason. Any other code, **including 1, does NOT block**.
- **PreToolUse JSON:** `hookSpecificOutput.permissionDecision` is `allow` | `deny` | `ask` | `defer` (`defer` is `-p` only). Precedence: deny > defer > ask > allow. `permissionDecisionReason` goes to Claude on deny and to the user on ask. `updatedInput` **replaces the whole input**. `additionalContext` is also accepted. The old top-level `decision: approve/block` is deprecated. **A hook `deny` holds even in `bypassPermissions` / `--dangerously-skip-permissions` and in `dontAsk`**, while a hook `allow` cannot override settings deny rules (hooks-guide "Hooks and permission modes").
- **Input:** common fields `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name` (+`agent_id`, `agent_type`), plus `tool_name`, `tool_input`, `tool_use_id`. Bash `tool_input`: `command`, `description`, `timeout`, `run_in_background`. Write: `file_path`, `content`. Edit: `file_path`, `old_string`, `new_string`, `replace_all`. `file_path` is always absolute.
```json
{ "hooks": { "PreToolUse": [
  { "matcher": "Edit|Write", "hooks": [ { "type": "command", "command": "bash",
      "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/guard_paths.sh"], "timeout": 10 } ] },
  { "matcher": "Bash", "hooks": [ { "type": "command", "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/guard_bash.py"], "timeout": 10 } ] } ],
  "Stop": [ { "hooks": [ { "type": "command", "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/keep_going.py"] } ] } ] } }
```
This uses exec form: with `args`, no shell runs and no quoting is needed. `guard_paths.sh` is adapted from the hooks-guide `protect-files.sh` example:
```bash
INPUT=$(cat); FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
case "$FILE_PATH" in *prepare.py|*/.git/*) echo "Blocked: $FILE_PATH is read-only for the loop" >&2; exit 2;; esac
exit 0
```
- **Limits:**
  - The matcher is the tool name, so an `Edit|Write` matcher never sees file writes done through **Bash** (`sed -i`, `>`, a Python script). The doc states this explicitly for PostToolUse ("doesn't run a `PostToolUse` hook matching `Edit|Write` when a `Bash` command ... rewrites the same file"). `FileChanged` sees such changes but can't block them. For PreToolUse the same follows from the matcher rule (INFERENCE).
  - Inspecting a Bash command string is best-effort parsing. For a hard boundary, use the sandbox's filesystem write limits and deny rules (§5).
  - PreToolUse doesn't fire for `@`-mentioned files.
  - `bashEditDiff` is best-effort.
- **Keeping the agent working (Stop):** return `{"decision":"block","reason":"<next instruction>"}`, exit 2 with a reason on stderr, or return `hookSpecificOutput.additionalContext`. `{"continue":false,"stopReason":"..."}` halts everything. Loop guards:
  - the input field `stop_hook_active` is true when the turn is already a hook continuation;
  - an **8-consecutive-continuation cap** applies, reset whenever Claude calls a tool; `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` raises it.
  - A prompt-type Stop hook answers `{"ok":false,"reason":...}` (or `"impossible":true`).
- **`/goal`** "is a wrapper around a session-scoped prompt-based Stop hook". After each turn the small fast model (`ANTHROPIC_DEFAULT_HAIKU_MODEL`) judges the condition (≤4,000 chars) as met, not met or impossible. The judge can't run tools, so it sees only what the transcript shows. It stops after several turns with no tool use. It works in `-p`, needs workspace trust, and is off when `disableAllHooks` is set.
```python
import json, sys, pathlib            # keep_going.py: composed from documented fields, not executed
d = json.load(sys.stdin); st = pathlib.Path(d["cwd"], ".autoresearch")
if not (st / "RUNNING").exists() or (st / "STOP").exists():
    sys.exit(0)                      # not a loop session, or the loop's own end condition: allow the stop
print(json.dumps({"decision": "block", "reason": "Start the next experiment per program.md."}))
```
Don't exit early on `stop_hook_active` in a loop hook: it is true on every hook-continued turn, so that check ends the loop after one continuation. End the loop on your own condition (a STOP file, an iteration or budget counter). The 8-block cap only catches spinning with no tool calls.

## 5. Unattended runs  ([doc] `headless.md`, `cli-reference.md`, `permission-modes.md`, `best-practices.md`, `agent-view.md`, `goal.md`, `scheduled-tasks.md`, `workflows.md`, `routines.md`, `sandboxing.md`, `plugins/install.md`)
| Option | Key facts |
|---|---|
| `claude -p` | [cli] `--permission-mode {acceptEdits,auto,bypassPermissions,manual,dontAsk,plan}` (`manual` = `default`), `--allowedTools`/`--disallowedTools` (rule syntax `Bash(git diff *)`), `--tools`, `--max-budget-usd`, `--output-format stream-json` (+`--verbose`), `--model`, `--effort`, `--fallback-model`, `--permission-prompts none`, `--json-schema`, `--worktree`, `--bare`. `--max-turns` is in cli-reference and best-practices but **absent from local `--help`** |
| -p default mode | Manual (v2.1.302+): anything needing approval is **denied** unless allowed. `dontAsk` is meant for locked-down CI |
| auto mode | A classifier (Sonnet 5 by default) reviews actions; it reduces prompts but does not guarantee safety. Under `-p`, a block denies that action and the run continues |
| bypassPermissions | Same as `--dangerously-skip-permissions`; use only in isolated containers or VMs without internet; refuses to run as root. Deny rules and hook denies still apply |
| Background | `claude --bg "..."`, `claude agents`, `attach`/`logs`/`stop`/`rm`/`respawn`. A supervisor keeps sessions alive after the terminal closes; they are preserved through machine sleep and resume on wake; a reboot stops them. Can't be combined with `-p` |
| `/goal` | `claude -p "/goal <condition, e.g. ... or stop after 50 turns>"` runs to completion in one invocation |
| `/loop` | Session-scoped (machine on, session open), minimum 1 minute, recurring tasks **expire after 7 days**, no catch-up for missed fires |
| Workflows | JS scripts with `agent()`, `parallel()`, `pipeline()`. Saved in `.claude/workflows/` (project), `~/.claude/workflows/`, or **plugin `workflows/`** as `/plugin:name`. Under `-p` there's no approval prompt, so allow `Workflow` or `Workflow(<name>)`. Limits: no mid-run input, 16 concurrent agents, 1,000 agents per run, no `import()`, `Date.now()`/`Math.random()` throw. Resumable only within the same session |
| Cloud scheduled tasks | `/schedule` or claude.ai/code/routines; Anthropic VM, **fresh GitHub clone**, no local files or GPUs, minimum interval 1 h, starts in auto mode, 100 runs/h, needs a claude.ai login. Cloud sessions don't load locally installed or project-enabled plugins |
| Desktop scheduled tasks | Run on your machine; machine on, no open session needed (comparison table only) |
| Sandbox | `/sandbox` or `sandbox.enabled`; macOS uses Seatbelt. Covers **Bash/PowerShell/Monitor only**, not Read/Edit/Write/WebFetch, hooks, MCP servers or monitors. Reads include `~/.ssh` by default; `allowedDomains` starts empty |
**What the docs recommend** (best-practices "Let Claude run without you"):
1. Define what done looks like.
2. Give it a way to check its own work: tests or a Stop hook.
3. Limit what it can touch: permission rules, `dontAsk`, the sandbox, a worktree, one pushable branch.
4. Set what stops it: `--max-turns`, `--max-budget-usd`.
5. Have a human sign off on the result.
The sandbox guidance adds `failIfUnavailable: true` and `allowUnsandboxedCommands: false`. For a hard boundary, run the whole process in a container or VM. Snippet (keys verified against the sandboxing.md examples):
```json
{ "sandbox": { "enabled": true, "failIfUnavailable": true, "allowUnsandboxedCommands": false, "autoAllowBashIfSandboxed": false,
    "filesystem": { "allowWrite": ["/tmp/autoresearch"] },
    "network": { "allowedDomains": ["github.com", "pypi.org"] },
    "credentials": { "files": [ { "path": "~/.ssh", "mode": "deny" } ] } },
  "permissions": { "deny": ["Read(./.env)", "Bash(git push *)"] } }
```
```bash
claude -p "/goal val_bpb improved and logged in results.tsv, or stop after 60 turns" \
  --settings ./autoresearch.settings.json --permission-mode dontAsk \
  --allowedTools "Read,Edit,Bash(python3 train.py *),Bash(git add *),Bash(git commit *)" \
  --max-budget-usd 20 --worktree overnight --output-format stream-json --verbose
```
Notes on this recipe:
- It is composed from documented flags and was **not executed**. `autoAllowBashIfSandboxed` defaults to true, meaning sandboxed Bash runs unprompted (paraphrase). That would bypass the `--allowedTools` Bash limit, hence `false` above.
- Don't add `--bare` if the plugin's hooks matter. `claude -p --worktree` leaves the worktree for you to remove.
- INFERENCE: on a laptop, "resume on wake" means no progress while asleep, so keep the machine awake or run on a server.

## 6. `/advisor`  ([doc] `advisor.md`, `cli-reference.md`)
- **What it does:** a server-side tool through which Claude consults a second model "at key moments". The advisor "receives the full conversation, including every tool call and result"; Claude decides when to call it, and no setting caps or forces calls.
- **How to set it:** `/advisor <model>` (saved as `advisorModel` in user settings; works in `-p` from v2.1.260), `advisorModel` in settings, or `claude --advisor opus` (doc: "doesn't list `--advisor` in `claude --help`"; [cli] grep confirms it is absent). `/advisor off` turns it off. **Experimental.** Works on the Anthropic API or Claude Platform on AWS only, not Bedrock/Vertex/Foundry, and needs feature-flag fetching. Subagents inherit the advisor, with the same pairing check against their own model.
- **Pairing rule:** the advisor must rank **at or above** the main model. A lower-ranked advisor isn't attached. A Fable main model takes only Fable advisors.
- **Documented pairings:**
  - Sonnet+Opus: Sonnet does routine work and escalates to Opus.
  - Sonnet+Fable.
  - Haiku+Opus: "lowest-cost main model with strong planning".
  - **Opus+Opus**: "A second Opus reviews the first. Useful for high-stakes tasks where an independent check matters more than cost".
  - **Fable+Fable**: "Highest-capability pairing".
  - **Sonnet+Sonnet**: "A lower-cost second opinion for catching routine oversights".
- **Cost:** each call bills at the advisor's rates, or counts toward subscription limits (Fable advisors go to usage credits where Fable does). The advisor's read "is not cached. Each advisor call processes the full transcript anew". Toggling the advisor doesn't invalidate the main model's cache. "Pairing a faster main model with a stronger advisor typically costs less than running the stronger model throughout."
- **Same-model verdict:** valid and documented (Opus/Opus, Fable/Fable, Sonnet/Sonnet). INFERENCE: it buys an independent full-transcript review, not extra capability, at the price of an uncached transcript read per call. That makes sense for high-stakes keep/discard decisions; for cost, the documented route is a cheaper main model with a stronger advisor. A plugin can't set `advisorModel` (§1), so the launcher has to pass `--advisor`.

## 7. Portability  ([doc] `memory.md`, `skills.md`; plus non-Anthropic primary docs as marked)
- **AGENTS.md:** Claude Code reads it natively from v2.1.277, but by default **only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the cwd or above**. To read both, set Project instructions to `claude-md-and-agents-md`, or put `@AGENTS.md` in CLAUDE.md. It does **not** read `AGENTS.local.md`, `AGENTS.override.md` or "anything under a `.agents/` directory". A plugin-root CLAUDE.md isn't loaded (documented); the same presumably holds for AGENTS.md (INFERENCE).
- **Agent Skills is an open standard:** skills.md says Claude Code skills "follow the Agent Skills open standard" (agentskills.io). Outside Claude Code "only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools` are accepted. Other fields cause a hard error at upload or packaging" (paraphrase of a condensed fetch).
- **Spec rules** (agentskills.io/specification, non-Anthropic site):
  - `name` is 1–64 chars of `a-z0-9-`, with no leading, trailing or double hyphen, and **must match the directory name**.
  - `description` is ≤1,024 chars (stricter than Claude Code's 1,536).
  - `allowed-tools` is experimental.
  - Optional folders: `scripts/`, `references/`, `assets/`. Use relative paths one level deep. Body <500 lines / <5,000 tokens.
- **Other agents** (their own docs, not Anthropic's):
  - Codex (learn.chatgpt.com/docs/build-skills.md): builds on the standard. Scans `.agents/skills` from the cwd up to the repo root, plus `$HOME/.agents/skills` and `/etc/codex/skills`. Requires `name` + `description`; its extension file is `agents/openai.yaml`. Codex reads `AGENTS.md` (learn.chatgpt.com/docs/agent-configuration/agents-md).
  - Gemini CLI (geminicli.com/docs/cli/skills/): "Based on the Agent Skills open standard". Workspace skills in `.gemini/skills/` or `.agents/skills/`, user skills in `~/.gemini/skills/` or `~/.agents/skills/`. Activates skills through an `activate_skill` tool with user confirmation. That page doesn't mention AGENTS.md.
- **Portable subset:** `name` and `description` (plus `license`, `compatibility`, `metadata`), a plain Markdown body, and scripts called by relative path or through a CLI on `PATH`.
- **Claude-only features:** `${CLAUDE_SKILL_DIR}` and `${CLAUDE_PLUGIN_ROOT}`, `` !`cmd` `` injection, `$ARGUMENTS`, `context: fork`/`agent`, skill `hooks`, `disable-model-invocation`, plugins, hooks, agents/*.md, workflows, `/goal`, `/advisor`, and `plugin eval`.
- **Recommendation (INFERENCE):** an agent-agnostic core of Python CLI + spec-compliant SKILL.md files + AGENTS.md, with a thin Claude Code plugin wrapper that adds:
  - guard and Stop hooks;
  - reviewer agents;
  - workflows;
  - `bin/`;
  - evals.
  Keep each skill directory name equal to its `name`, and the description ≤1,024 chars.

## UNVERIFIED
1. Whether 2.1.322 accepts `--max-turns` and `--advisor`: both are documented, both are absent from local `--help`, and neither was executed.
2. The exact marketplace `source` string for a plugin at the repo root. A root source is mentioned in manifest-reference; use `./plugins/<name>`.
3. Whether a skill's `agent:` can name a plugin-scoped agent (`autoresearch:reviewer`), and whether `${...}` expands inside `` !`cmd` `` blocks.
4. Plugins in cloud scheduled tasks through org-managed settings (only "cloud sessions don't load local/project plugins" was confirmed).
5. Cursor and other clients' Agent Skills support (the agentskills.io client page rendered empty); whether Claude Code scans `.agents/skills/`; how Codex and Gemini treat Claude-only frontmatter fields.
6. Condensed-fetch text (paraphrase): the skill fields `when_to_use`, `shell`, `metadata`, `license`, `compatibility`; the "hard error outside Claude Code" and "follow the Agent Skills open standard" sentences; the §4 event list, matcher table and exit-code text; the PostToolUse Bash quote; the auto, bypass and sleep descriptions in §5; the `autoAllowBashIfSandboxed` default.
7. Untested composition: the overnight `claude -p` recipe and all hook and skill scripts were never run. Also unconfirmed: whether `stop_hook_active` clears after tool calls, and whether a skill's `allowed-tools` grant survives hook-continued turns (the doc says it clears on the next user message).
