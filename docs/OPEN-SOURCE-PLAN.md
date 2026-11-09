# Open-sourcing Cimcime: phased plan

Goal: a new public repo `cimcime` that anyone can install and use on macOS, Linux and Windows.
Work is done phase by phase, resumable across sessions. Tick boxes as phases complete.

## Phase 0 - Audit (blocker for publishing)
- [x] Secret/PII scan of the tree and git history (no tokens, chat ids, paths, logs).
- [x] Licensing review (see docs/OPEN-SOURCE-AUDIT.md; skills license is a blocker): third-party skills in `.claude/skills` (credits/license), roadmap.sh derived content in `docs/topics`, `docs/research`. Remove or credit anything not redistributable.
- [x] Decide what stays user-specific (Telegram ids, personal repo names, Turkish-translator persona) vs. generic.

## Phase 1 - Decouple from one machine and one user
- [x] Replace hardcoded `DEFAULT_REPO` and personal repo names with config (env var / config file).
- [x] Config module: `cimcime.toml` + env overrides, platform-aware config dir (stdlib, no platformdirs dep). Data-dir migration for message log/delegation log still TODO.
- [ ] Make the translator and language settings optional/configurable.

## Phase 2 - Cross-platform runtime
- [ ] Replace macOS-only launchd + bash watchdog with a Python watchdog.
- [ ] Service installers: launchd (macOS), systemd user unit (Linux), Task Scheduler (Windows), behind one `cimcime service install`.
- [x] Python-only CLI entrypoint (`cimcime ...`), no bash dependency.
- [x] CI matrix: ubuntu, macos, windows.

## Phase 3 - Easy install and onboarding
- [ ] `pipx install cimcime` / `uv tool install`, plus one-line install scripts (sh and PowerShell).
- [ ] `cimcime init` wizard: GitHub repo, Telegram pairing, permissions, service install.
- [x] `cimcime doctor` to check prerequisites (claude, gh, uv, git).

## Phase 4 - Docs and community files
- [ ] README rewrite (what, why, quickstart for 3 OSes), architecture overview from ADRs.
- [ ] LICENSE (MIT unless told otherwise), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue/PR templates.
- [ ] Security notes: permission model, approval gates, safe defaults.

## Phase 5 - Publish
- [ ] Fresh history (single clean initial commit, no private history).
- [ ] Create public `cimcime` repo, push, enable CI, tag v0.1.0.
- [ ] Final check, then report to the user.

Publishing (Phase 5) happens only after the Phase 0 scan is clean.
