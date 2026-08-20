#!/bin/bash
# Gallery watchdog — SILENT when healthy; prints one line only when it restarted the gallery.
# Set GALLERY_DIR / GALLERY_PORT if your install differs from the defaults.
# Wire it up: hermes cron create 'every 5m' --name 'Gallery health check' --no-agent --script gallery-watchdog.sh
GALLERY_DIR="${GALLERY_DIR:-/opt/data/gallery}"
GALLERY_PORT="${GALLERY_PORT:-80}"

code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://127.0.0.1:${GALLERY_PORT}/" 2>/dev/null)
if [ "$code" != "200" ] && [ "$code" != "302" ]; then
  cd "$GALLERY_DIR" 2>/dev/null || exit 0
  bash start.sh >> /opt/data/gallery-watchdog.log 2>&1
  echo "[gallery-watchdog] gallery was ${code:-down} — restarted"
fi
