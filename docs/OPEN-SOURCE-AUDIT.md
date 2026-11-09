# Phase 0 audit (2026-11-09)

## Secrets / PII
- Token patterns (GitHub, OpenAI-style, Slack, AWS, Telegram bot, private keys) across full git history: **none found**.
- Telegram chat id and local `/Users/...` paths: **none in tree or history**.
- Personal identifiers still in tree (fix in Phase 1): `DEFAULT_REPO` in `src/cimcime/cli.py`, repo name in `tests/test_state_store_github.py`, repo names in ADR-0012.
- Git author name/email in history is personal; Phase 5 uses a fresh single-commit history anyway.

## Licensing
- `.claude/skills/*` are third-party (Matt Pocock skills; `pr` also credits Dex Horthy's `show-me`). No LICENSE file ships with them. **Blocker**: either confirm upstream license and add attribution, or exclude them from the public repo and document how to install them separately.
- `docs/topics/*` and `docs/research/*` are summaries derived from roadmap.sh and linked resources. **Decision needed**: keep only our own summaries with source links, or drop and let users regenerate via the Learning Phase.

## User-specific vs generic
- Specific: Telegram bridge wiring, `turkish-translator` agent, launchd plists, self-hosted runner `deploy.yml`, ADR-0005/0011 (Mac mini).
- Generic: agent hierarchy, board, state store, approval gates, CLI.

## Decisions (user, 2026-11-09)
- Skills: option A, excluded from the public repo; setup docs explain how to install them separately.
- Topics/research: option B, kept with source links.
