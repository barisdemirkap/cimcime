# Run Cimcime on a VM

The same setup that runs on a Mac mini runs on a Linux VM (Ubuntu/Debian tested by design, not yet on a real VM): Claude Code is the runtime, Cimcime is a repo plus a small Python CLI, state lives in GitHub issues and local files.

## Steps
1. Install prerequisites: `git`, `gh` (then `gh auth login`), Claude Code (`claude`), `bun` (the Telegram plugin needs it), `util-linux` (`script`), `uv`.
2. `curl -fsSL https://raw.githubusercontent.com/barisdemirkap/cimcime/master/install.sh | sh`
3. Sign in to Claude Code once on the VM: run `claude` and follow the URL/device login. API-key billing (`ANTHROPIC_API_KEY`) is a spend decision that is yours.
4. `cimcime init <owner>/<repo>` and pair Telegram (`scripts/telegram-setup-wizard.sh` equivalent: follow `cimcime init`).
5. `cimcime service install` writes systemd **user** units and runs `loginctl enable-linger` so the session keeps running after you log out.
6. `cimcime doctor` must show no FAIL. On Linux it also checks `script` and linger.

## Notes
- One Telegram bot token can be polled by one session only: do not run the Mac mini and the VM with the same token at the same time.
- Back up the data dir (message log, decision log) if you want continuity between machines.
- The unit files are rendered and unit-tested; a full run on a fresh VM has not been done yet.
