#!/bin/bash
# Weekly Hermes Agent update check — SILENT when nothing new; prints a reminder
# (with the Hostinger UI steps) only when a newer build exists.
# Wire it up: hermes cron create '0 1 * * 1' --name 'Hermes update check' --no-agent --script hermes-update-check.sh

INSTALLED=$(hermes --version 2>/dev/null | grep -oE '[0-9]{4}\.[0-9]{1,2}\.[0-9]{1,2}(\.[0-9]+)?' | head -1)
[ -z "$INSTALLED" ] && exit 0

LATEST=$(curl -s --max-time 20 "https://hub.docker.com/v2/repositories/nousresearch/hermes-agent/tags?page_size=25&ordering=last_updated" \
  | grep -oE '"name":"v20[0-9]{2}\.[0-9]+\.[0-9]+(\.[0-9]+)?"' \
  | head -1 | grep -oE '20[0-9]{2}\.[0-9]+\.[0-9]+(\.[0-9]+)?')
[ -z "$LATEST" ] && exit 0

norm() { echo "$1" | awk -F. '{for(i=1;i<=NF;i++) printf "%04d", $i}'; }

if [ "$(norm "$LATEST")" \> "$(norm "$INSTALLED")" ]; then
  echo "🆕 A new Hermes Agent version is available: $LATEST (you are on $INSTALLED)."
  echo ""
  echo "Update it in Hostinger (no terminal needed):"
  echo "  hpanel.hostinger.com → VPS → Docker Manager → Applications →"
  echo "  hermes-agent → ⋮ (three-dots icon) → Update."
  echo ""
  echo "Chats, memory and settings survive the update (they live outside the app container)."
fi
