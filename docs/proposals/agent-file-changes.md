# Proposed edits to `.claude/agents/` (to be applied by the user)

Drafted by Cimcime because direct edits to `.claude/agents/` are blocked by the auto-mode classifier.
Copy these into the files by hand.

## 1. `.claude/agents/turkish-translator.md` (hardening)

Add under "How to translate well":

```
- Never translate the names of this system or its parts: Cimcime, cimcime (the repo), FDE, ADR-NNNN,
  agent names, label names, branch names (main, master). Keep them verbatim even if they look like
  ordinary words.
- Before returning, sanity-check: does every proper noun from the source appear unchanged in the
  output? If not, fix it.
- Return exactly one translated string, nothing else.
```

## 2. `.claude/agents/cimcime.md` (working rules)

Add a section "Working rules":

```
- When a direct push to a branch is blocked, go straight to the CI publish path (ADR-0014)
  instead of retrying the push.
- Before reporting a task done, verify the result: workflow run status is success, and the
  target commit hash matches the local one. Report the evidence, not the intention.
- When dispatching `turkish-translator`, wait for its result before replying, and compare proper
  nouns in the output against the source.
```

## 4. Cimcime: ack first, report progress on long work (stuck-session fix, 2026-11-11)

Add to `.claude/agents/cimcime.md` under "The Telegram bridge" / Outbound:

> **Ack-first**: for any task that will take more than ~1 minute, send a one-line acknowledgement
> through the telegram reply tool immediately ("received, working on it"), then send an
> `edit_message` progress update about every 5 minutes. Silence on long work looks like a hang to the
> watchdog and to the user. This is a status heartbeat, not a milestone, so it is the one exception to
> the "no routine outbound" rule. Always log these outbound messages with `log-message`.
