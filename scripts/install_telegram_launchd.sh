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

mkdir -p "$REPO/logs" ~/Library/LaunchAgents
DEST=~/Library/LaunchAgents/com.cimcime.telegram-channel.plist
sed -e "s#REPO_PATH#$REPO#g" -e "s#CLAUDE_BIN_PATH#$CLAUDE_BIN#g" \
  "$REPO/scripts/com.cimcime.telegram-channel.plist" > "$DEST"
launchctl unload "$DEST" 2>/dev/null || true
launchctl load "$DEST"
echo "Installed $DEST (claude binary: $CLAUDE_BIN)"
