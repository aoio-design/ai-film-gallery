#!/bin/bash
# Weekly Web UI update check — SILENT when nothing new; prints a reminder when a newer build exists.
# Local version is read from the WebUI's package.json; upstream version from the GitHub repo.
# Wire it up: hermes cron create '0 1 * * 1' --name 'WebUI update check' --no-agent --script webui-update-check.sh
WEBUI_DIR="${WEBUI_DIR:-/opt/data/hermes-webui}"

LOCAL=$(grep -oE '"version": *"[0-9]+\.[0-9]+\.[0-9]+"' "$WEBUI_DIR/package.json" 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
[ -z "$LOCAL" ] && exit 0

LATEST=$(curl -s --max-time 20 "https://raw.githubusercontent.com/nesquena/hermes-webui/main/package.json" \
  | grep -oE '"version": *"[0-9]+\.[0-9]+\.[0-9]+"' | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
[ -z "$LATEST" ] && exit 0

norm() { echo "$1" | awk -F. '{for(i=1;i<=NF;i++) printf "%04d", $i}'; }

if [ "$(norm "$LATEST")" \> "$(norm "$LOCAL")" ]; then
  echo "🆕 A newer Web UI build is available: $LATEST (you are on $LOCAL)."
  echo "Ask your agent to update it, or restart it if you already updated:"
  echo "  cd $WEBUI_DIR && ./ctl.sh restart"
fi
