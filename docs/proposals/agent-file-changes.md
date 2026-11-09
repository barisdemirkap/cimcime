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
