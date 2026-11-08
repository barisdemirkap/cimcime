#!/bin/zsh
# Health check for the telegram-channel service, run every few minutes by
# com.cimcime.watchdog (launchd). Appends one line per run to logs/health.log and
# restarts the service when it has no running process. Does NOT restart on a rejected
# bot token: that needs a human, and a restart loop would only hide it.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$REPO/logs/health.log"
LABEL=com.cimcime.telegram-channel
mkdir -p "$REPO/logs"

svc=ok
launchctl list "$LABEL" 2>/dev/null | grep -q '"PID"' || {
  svc=restarted
  launchctl kickstart -k "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || svc=restart-failed
}

TOKEN="$(sed -n 's/^TELEGRAM_BOT_TOKEN=//p' ~/.claude/channels/telegram/.env 2>/dev/null | tr -d '"\r ')"
curl -fsS -m 10 "https://api.telegram.org/bot$TOKEN/getMe" >/dev/null 2>&1 && api=ok || api=FAIL
dns=$(dscacheutil -q host -a name api.telegram.org 2>/dev/null | grep -q ip_address && echo ok || echo FAIL)

echo "$(date -u +%FT%TZ) service=$svc telegram_api=$api dns=$dns" >> "$LOG"
# keep the log bounded
[[ $(wc -l < "$LOG") -gt 5000 ]] && tail -n 2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
exit 0
