---
status: accepted
---

# A Claude Code PreToolUse hook enforces the approval gates on agent Bash calls, as a guard against model mistakes

ADR-0001 defines three approval gates (production deploy, real third-party communication, real
spend or account changes). Until now they were advisory text in agent instructions. 
directive asks for enforcement where the agent acts: its shell.

`src/cimcime/approval_hook.py` is a Claude Code `PreToolUse` hook with a `Bash` matcher.

- It reads the tool call from stdin, splits the command with a quote-aware parser (chains,
  subshells, command substitution, backticks, heredocs, `bash -c`, `eval`, `ssh host cmd`,
  `env`/`sudo`/`xargs`/`find -exec`/`uv run`/`npx` wrappers) and checks every command it finds.
- It blocks with exit code 2 and a message that names the gate: `git push` to anything but
  `origin` or with force (the public mirror is published only by the ADR-0014 CI workflow),
  `launchctl` beyond the standing `kickstart` of the alfred bot, HTTP writes and raw network or
  mail clients to non-local hosts, package and image publishing, cloud, deploy and spend CLIs
  (read-only verbs stay allowed), `gh` calls that write to the public mirror, to foreign repos, or
  change repo/account settings.
- It fails closed: bad input, a parse error, a command name built from a variable or glob, a
  shell or interpreter reading from a pipe, or any internal error blocks. The example settings
  wrap the call as `... || exit 2`, so a missing Python also blocks (a bare 127 would not).
- Routine work is allowed by default and by an explicit list of local commands.
- It also blocks Bash commands that edit `.claude/settings*.json` or the hook itself.
- There is no override flag: a model that can add an env var to its own command could set it.
  The owner approves by running the command himself.

`cimcime doctor` reports whether the hook is wired into a settings file. The repo ships an example
(`docs/examples/claude-settings.approval-gate.example.json`) and install notes
(`docs/approval-hook.md`) but does not edit any live settings: installing it is the owner's step.

## What this is not

It is a guard against model mistakes, not a security boundary. The agent runs as the same user
as the hook, so it can edit settings through other tools, run an uninspected script file, call
an API from a program, or use a tool the matcher does not cover. Real isolation
needs a process boundary (separate uid or broker). The hook catches the honest, common errors:
a hallucinated push, a copied `curl -X POST`, a stray `terraform apply`. Known bypasses are listed
in `docs/approval-hook.md` and each new miss becomes a test fixture first.

## Considered options

- Prompt text only (status quo): rejected, the model can simply not follow it.
- `permissions.deny` rules alone: prefix matching is easy to evade with chaining and quoting, and
  cannot express "origin only" or "alfred only".
- A broker with grants: the right long-term answer, deferred (needs the boundary work); this hook
  is the cheap interim.
