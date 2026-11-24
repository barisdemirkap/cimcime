# Setup notes: known issues and hardening

Lessons from running Cimcime always-on. Each item is something that actually went wrong or was added because of it.

## Unattended restart gets stuck on a permission dialog
After a power cut the Mac booted, but the session stayed offline until someone clicked an OS permission dialog (a Homebrew-related one on macOS).
- Do a deliberate first run after install and grant every OS permission prompt once (Terminal/launchd, Homebrew-installed tools, Full Disk Access if you use it).
- The watchdog now alerts when a permission prompt is on screen, even when no unanswered message is logged. Keep `cimcime service` installed so it runs.
- Planned: a boot-stall alert so a machine that never came back is reported.

## Always-on session and message recovery
- Every Telegram message is logged; a restarted session runs `unanswered-messages` first and answers anything missed. Do not delete the message log between restarts.
- One Telegram bot token can be polled by one session only.

## Approval gates are enforced for agent shell commands
Install the `PreToolUse` hook from `docs/approval-hook.md` and confirm with `cimcime doctor`. It is a guard against model mistakes, not a security boundary.

## Machine hygiene checks
`cimcime doctor` also checks disk encryption (FileVault/LUKS) and that private files (logs, secrets) have private permissions. Fix any FAIL before relying on the install.

## Your data
`cimcime export-data` and `cimcime delete-data` export or erase the private message/decision logs.

## Usage limits
Use `cimcime usage-check` rather than any cached number; stale data (older than 15 minutes) is reported as `unknown`, and large jobs should wait for a fresh reading.
