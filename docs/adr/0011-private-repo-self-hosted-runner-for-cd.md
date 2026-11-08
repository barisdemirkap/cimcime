---
status: accepted
---

# Repo is private; a self-hosted runner on the Mac Mini handles continuous deployment, triggered only by push to main

This repo was switched from public to private specifically to run a GitHub Actions
self-hosted runner on the Mac Mini safely. Self-hosted runners on public repos are a known
risk: anyone could fork the repo and open a pull request whose workflow run executes
arbitrary code on the runner's host — in this case, the same physical machine holding the
Telegram bot token and running Cimcime itself. Going private removes that attack surface.

As a second, independent layer of defense (not a substitute for going private, in case
visibility ever changes back): the self-hosted deploy workflow (`.github/workflows/
deploy.yml`) is triggered only by `push` to `main`, never `pull_request`. Pushing to `main`
already requires repo write access, so this restricts who can ever cause code to run on the
self-hosted runner to the same people who could already push directly. The existing fast
test-suite workflow (`tests.yml`) keeps running on GitHub's own hosted runners and still
triggers on `pull_request`, since that one never touches the Mac Mini.

The runner uses its own checkout under `~/actions-runner/_work/`, separate from the user's
manually-managed working clone — the standard GitHub Actions pattern, chosen over having CI
operate on the user's own clone to avoid any risk of CI clobbering uncommitted local changes.
`scripts/install_telegram_launchd.sh` needed no changes to support this: it already derives
the repo path from wherever it's invoked from, so running it from the runner's checkout
naturally points the `launchd` service at that checkout instead.

The runner process is itself a launchd service (`svc.sh install`), otherwise it stays offline after a
reboot and deploys silently stop. Because the Telegram session then runs from the runner's checkout,
its Claude permissions must be in the committed `.claude/settings.json`, not `settings.local.json`.

## Considered options

- Keep the repo public, restrict the self-hosted job to `push`-only (same trigger
  restriction, without changing visibility) — rejected as the sole safeguard: it's a real
  mitigation, but going private removes the risk at its source rather than relying on a
  workflow-file convention nobody is forced to respect later.
- Run the deploy job against the user's existing working clone instead of a separate runner
  checkout — rejected: creates two copies of the repo to keep straight on one machine, for no
  real benefit over the standard pattern.
