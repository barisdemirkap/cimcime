#!/bin/zsh
# Thin launcher for the Python watchdog (src/cimcime/watchdog.py), run every minute by
# com.cimcime.watchdog (launchd). The shell version it replaces restarted the session after 20 min of
# silence even while it was busy, killing in-flight work (2026-11-11). Logs stay in $REPO/logs.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export CIMCIME_DATA_DIR="$REPO"
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
cd "$REPO" && uv run --quiet python -m cimcime.cli watchdog >/dev/null 2>>"$REPO/logs/launchd-watchdog.err"
exit 0
