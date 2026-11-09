#!/usr/bin/env bash
# Merge broad allow rules + spend/prod deny rules into ~/.claude/settings.json.
# Idempotent; backs up the original. Requires python3.
set -euo pipefail
F="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"
mkdir -p "$(dirname "$F")"
[ -f "$F" ] && cp "$F" "$F.bak.$(date +%s)"
python3 - "$F" <<'PY'
import json, sys, os
p = sys.argv[1]
d = json.load(open(p)) if os.path.exists(p) and os.path.getsize(p) else {}
perm = d.setdefault("permissions", {})
allow = ["Bash", "Read", "Write", "Edit", "WebFetch", "WebSearch", "Agent",
         "mcp__plugin_telegram_telegram__*", "mcp__claude-in-chrome__*"]
deny = ["Bash(*terraform apply*)", "Bash(*terraform destroy*)", "Bash(*kubectl apply*)",
        "Bash(*kubectl delete*)", "Bash(*gh release create*)", "Bash(*npm publish*)",
        "Bash(*twine upload*)", "Bash(*docker push*)", "Bash(*aws *)", "Bash(*gcloud *)",
        "Bash(*az *)", "Bash(*stripe*)", "Bash(*fly deploy*)", "Bash(*vercel --prod*)",
        "Bash(sudo rm -rf*)", "Bash(rm -rf /*)", "Bash(rm -rf ~*)"]
for key, vals in (("allow", allow), ("deny", deny)):
    cur = perm.setdefault(key, [])
    for v in vals:
        if v not in cur: cur.append(v)
json.dump(d, open(p, "w"), indent=2)
print("Updated", p)
PY
