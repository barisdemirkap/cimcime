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

# --- Alive-but-not-answering detection (2026-11-09 incident) -------------------------
# The headless session can sit forever on an interactive prompt (permission dialog, macOS
# password) with the process alive, so "service=ok" alone proved nothing. Look at the
# message log for the oldest inbound message with no outbound after it. At >=10 min: alert
# the user through the Bot API (once per message) and save the session screen tail. At
# >=20 min: restart the service (once per message; the new session recovers the backlog
# through `unanswered-messages`).
MSGDB="${CIMCIME_MESSAGE_LOG:-$HOME/.claude/channels/telegram/messages.db}"
STATE="$REPO/logs/stuck.state"
stuck=none
if [[ -f "$MSGDB" ]]; then
  row=$(sqlite3 "$MSGDB" "
    WITH last_out AS (SELECT COALESCE(MAX(julianday(sent_at)),0) AS t FROM messages WHERE direction='outbound')
    SELECT chat_id, id, CAST((julianday('now')-julianday(sent_at))*1440 AS INTEGER)
    FROM messages, last_out
    WHERE direction='inbound' AND julianday(sent_at) > last_out.t
    ORDER BY julianday(sent_at) ASC LIMIT 1;" 2>/dev/null)
  if [[ -n "$row" ]]; then
    chat=${row%%|*}; rest=${row#*|}; mid=${rest%%|*}; age=${rest#*|}
    notified=$(sed -n 's/^notified=//p' "$STATE" 2>/dev/null)
    restarted=$(sed -n 's/^restarted=//p' "$STATE" 2>/dev/null)
    if (( age >= 10 )) && [[ "$notified" != "$mid" ]]; then
      stuck=alerted
      sed 's/\x1b\[[0-9;?]*[a-zA-Z]//g' "$REPO/logs/launchd-telegram-channel.out" 2>/dev/null | tail -c 3000 > "$REPO/logs/stuck-$(date -u +%Y%m%dT%H%M%SZ).txt"
      curl -fsS -m 10 "https://api.telegram.org/bot$TOKEN/sendMessage" \
        --data-urlencode "chat_id=$chat" \
        --data-urlencode "text=Cimcime has not answered your message for ${age} min (probably stuck on a prompt on the Mac mini). Auto-restart at 20 min." >/dev/null 2>&1
      printf 'notified=%s\nrestarted=%s\n' "$mid" "$restarted" > "$STATE"
    fi
    if (( age >= 20 )) && [[ "$restarted" != "$mid" ]]; then
      stuck=restarted
      launchctl kickstart -k "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || stuck=restart-failed
      printf 'notified=%s\nrestarted=%s\n' "$mid" "$mid" > "$STATE"
    fi
  fi
fi

echo "$(date -u +%FT%TZ) service=$svc telegram_api=$api dns=$dns stuck=$stuck" >> "$LOG"
# keep the log bounded
[[ $(wc -l < "$LOG") -gt 5000 ]] && tail -n 2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
exit 0
