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

# A revoked/deleted bot token makes the service look healthy (process up, logs clean) while
# receiving nothing - Telegram just answers 401. Fail loudly here instead.
TOKEN="$(sed -n 's/^TELEGRAM_BOT_TOKEN=//p' ~/.claude/channels/telegram/.env 2>/dev/null | tr -d '"\r ')"
if ! curl -fsS "https://api.telegram.org/bot$TOKEN/getMe" >/dev/null 2>&1; then
  echo "error: Telegram rejects the bot token in ~/.claude/channels/telegram/.env (revoked or missing)." >&2
  echo "Create a bot with @BotFather and save the token there, then re-run this script." >&2
  exit 1
fi

# Every claude session that loads the telegram plugin starts its own bot server, and a new
# server SIGTERMs the previous one (one poller per token) - so any other session silences
# this service. Disable the plugin globally; the service enables it for itself via --settings.
python3 - <<'PY'
import json, os
p = os.path.expanduser("~/.claude/settings.json")
d = json.load(open(p)) if os.path.exists(p) else {}
d.setdefault("enabledPlugins", {})["telegram@claude-plugins-official"] = False
json.dump(d, open(p, "w"), indent=2)
PY

mkdir -p "$REPO/logs" ~/Library/LaunchAgents
DEST=~/Library/LaunchAgents/com.cimcime.telegram-channel.plist
sed -e "s#REPO_PATH#$REPO#g" -e "s#CLAUDE_BIN_PATH#$CLAUDE_BIN#g" -e "s#BUN_DIR#$BUN_DIR#g" \
  "$REPO/scripts/com.cimcime.telegram-channel.plist" > "$DEST"
launchctl unload "$DEST" 2>/dev/null || true
launchctl load "$DEST"
echo "Installed $DEST (claude binary: $CLAUDE_BIN, bun dir: $BUN_DIR)"

# Watchdog: every 5 minutes restarts the service if it has died and records service /
# Telegram API / DNS health in logs/health.log.
WD_DEST=~/Library/LaunchAgents/com.cimcime.watchdog.plist
sed -e "s#REPO_PATH#$REPO#g" "$REPO/scripts/com.cimcime.watchdog.plist" > "$WD_DEST"
launchctl unload "$WD_DEST" 2>/dev/null || true
launchctl load "$WD_DEST"
echo "Installed $WD_DEST"
