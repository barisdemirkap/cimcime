# Approval-gate hook (ADR-0016)

`src/cimcime/approval_hook.py` is a Claude Code `PreToolUse` hook for the `Bash` tool. It enforces
the ADR-0001 approval gates on agent shell commands. It is a **guard against model mistakes, not a
security boundary**: it stops honest errors, not a determined same-user process.

## Install (owner step)

Cimcime does not edit live settings. Merge the `hooks` block from
`docs/examples/claude-settings.approval-gate.example.json` into the settings file you want:

- project: `.claude/settings.json` (or `.claude/settings.local.json`), where `$CLAUDE_PROJECT_DIR`
  is the Cimcime checkout, or
- user: `~/.claude/settings.json`, replacing `$CLAUDE_PROJECT_DIR/src/cimcime` with the absolute
  path of your Cimcime checkout. Use the same block in other repos (alfred, camondo) the same way.

Keep the trailing `|| exit 2`: Claude Code treats most non-zero exits (for example 127, python not
found) as non-blocking, and only exit 2 blocks. Then run `cimcime doctor`; the `approval hook` line
reports whether a settings file wires it in.

## What it does

Blocks, naming the gate (exit 2, reason on stderr):

| Gate | Examples |
|---|---|
| production_deploy | `git push` to a remote other than `origin`, force/mirror/delete pushes, `git remote add/set-url`; `launchctl` other than `kickstart [-k] gui/<uid>/<...alfred...>` and read-only verbs; `systemctl` stop/disable/...; `npm/pnpm/uv/cargo/gem publish`, `twine upload`, `docker push`; `terraform apply`, `kubectl apply`, `helm upgrade`, `vercel/fly/wrangler/firebase deploy`; `scp`/`rsync` to a remote host; `gh repo create/delete/edit`, `gh release create`, writes to the public mirror repo |
| third_party_communication | `curl`/`wget`/`http` writes (POST, PUT, PATCH, DELETE, uploads) to a non-local host; Telegram/Slack/Discord/Twilio send endpoints; `nc`, `sendmail`, `mail`, `osascript` driving Mail/Messages; `gh api` non-GET; `gh issue/pr` writes in repos not owned by the owner; inline Python/Node code that uses the network or subprocesses |
| spend_or_account_change | `aws`/`gcloud`/`az`/`doctl`/`stripe`/... with non-read-only verbs; `gh secret`, `gh auth`, `gh codespace create` |

Fails closed (blocks with "unverifiable"): invalid hook input, shell parse errors, a command name
from a variable, glob or substitution (`$CMD push`), a shell or interpreter reading code from a
pipe (`curl ... | sh`), nesting deeper than 8, any internal error. Also blocks Bash edits of
`.claude/settings*.json` and of the hook file.

Allowed without a prompt: everything else, in particular local routine work (`git add/commit/pull`,
`git push` / `git push origin <branch>`, `gh issue ...`, `gh pr ...`, `gh api` GET calls such as the
ADR-0014 head comparison, tests, builds, read-only cloud verbs, `launchctl kickstart` of the alfred
bot, HTTP writes to localhost such as the Ollama API).

There is no override. To proceed with a blocked command, the owner approves it and runs it himself
(for example with `!` in the session).

## Known bypasses (not exhaustive)

- Any file the hook does not read: `bash deploy.sh`, `python publish.py`, `make deploy`, a
  `package.json` script. The hook sees the command line, not the script body.
- Any tool other than Bash: an MCP server, the Write/Edit tools (including editing settings), a
  subagent configured without the hook, `Task` children in another settings scope.
- Programs that talk to the network without a recognisable name or inline code (a compiled binary,
  `perl -MLWP`, a language not in the list).
- Config-driven redirects the hook cannot see: a changed `origin` URL set earlier, `~/.gitconfig`
  aliases, `GIT_SSH_COMMAND`, `PATH` or shell aliases/functions that shadow `git` or `curl`.
- `curl -K config` style indirection.
- `gh` flags the parser does not model, `gh api graphql` with a mutation read from a file the
  heuristic misses.
- A same-user process can edit the settings or the hook directly.
- Heuristics are conservative both ways: a legitimate command can be blocked (for example inline
  Python that imports `subprocess`). Run it yourself or put the code in a script file.

Each miss found in practice becomes a fixture in `tests/test_approval_hook.py` first.
