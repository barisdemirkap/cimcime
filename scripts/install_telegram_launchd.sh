#!/bin/zsh
# Installs the always-on Telegram Channels service on this Mac (use on the M1 Mac mini):
#   com.cimcime.telegram-channel   keeps `claude --channels plugin:telegram@claude-plugins-official`
#                                   running persistently, restarting it if it exits.
#
# Run this only after the plugin itself has been configured and paired (ticket 6, issue #7) -
# this script just keeps that already-working session alive across reboots. Mirrors the
# music-pipeline repo's scripts/install_launchd.sh pattern (ADR-0005).
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_BIN="$(command -v claude)"
if [[ -z "$CLAUDE_BIN" ]]; then
  echo "error: 'claude' not found on PATH. Install Claude Code first." >&2
  exit 1
fi

# launchd gives services a minimal PATH that won't include wherever Bun lives, and the
# telegram channel plugin is a Bun script - without this, the service starts but the
# plugin silently fails to connect. Resolve Bun's directory now, from whatever PATH this
# install script itself was run with (falls back to the default installer location).
BUN_BIN="$(command -v bun || true)"
[[ -z "$BUN_BIN" && -x "$HOME/.bun/bin/bun" ]] && BUN_BIN="$HOME/.bun/bin/bun"
if [[ -z "$BUN_BIN" ]]; then
  echo "error: 'bun' not found. Install it first: curl -fsSL https://bun.sh/install | bash" >&2
  exit 1
fi
BUN_DIR="$(dirname "$BUN_BIN")"

# claude shows a one-time "do you trust this folder?" dialog the first time it runs
# in a directory, and nothing can answer it inside launchd (no interactive stdin to
# type "Yes" into, even with the script(1) pty workaround below - it would just hang
# forever and KeepAlive would never see it exit). The answer persists per-directory
# in ~/.claude.json once given, so require it to already be given before installing.
if ! python3 -c "
import json, sys
d = json.load(open('$HOME/.claude.json'))
sys.exit(0 if d.get('projects', {}).get('$REPO', {}).get('hasTrustDialogAccepted') else 1)
" 2>/dev/null; then
  echo "error: this folder isn't trusted yet. Run 'claude' once in $REPO in a normal" >&2
  echo "terminal, answer \"Yes, I trust this folder\" at the prompt, then exit (Ctrl-D)" >&2
  echo "and re-run this script." >&2
  exit 1
fi

mkdir -p "$REPO/logs" ~/Library/LaunchAgents
DEST=~/Library/LaunchAgents/com.cimcime.telegram-channel.plist
sed -e "s#REPO_PATH#$REPO#g" -e "s#CLAUDE_BIN_PATH#$CLAUDE_BIN#g" -e "s#BUN_DIR#$BUN_DIR#g" \
  "$REPO/scripts/com.cimcime.telegram-channel.plist" > "$DEST"
launchctl unload "$DEST" 2>/dev/null || true
launchctl load "$DEST"
echo "Installed $DEST (claude binary: $CLAUDE_BIN, bun dir: $BUN_DIR)"
