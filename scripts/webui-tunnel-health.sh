#!/bin/bash
# Web UI + Cloudflare tunnel watchdog — SILENT when healthy; prints one line only when it restarted something.
# Assumes the layout from the AI Film Studio guide: WebUI at /opt/data/hermes-webui (port 8787),
# cloudflared binary at /opt/data/cloudflared/cloudflared, tunnel config at /opt/data/.cloudflared/config.yml.
# Wire it up: hermes cron create 'every 5m' --name 'Web UI & tunnel health' --no-agent --script webui-tunnel-health.sh
WEBUI_DIR="${WEBUI_DIR:-/opt/data/hermes-webui}"
WEBUI_PORT="${WEBUI_PORT:-8787}"
OUT=""

# 1. Web UI on 8787
if ! curl -sf --max-time 5 "http://127.0.0.1:${WEBUI_PORT}/health" >/dev/null 2>&1; then
  if [ -x "$WEBUI_DIR/ctl.sh" ]; then
    cd "$WEBUI_DIR" && ./ctl.sh start >> /opt/data/logs/webui.log 2>&1
    OUT="$OUT restarted WebUI"
  fi
fi

# 2. Cloudflare tunnel (any named tunnel should have a live connector)
if ! pgrep -f "cloudflared tunnel run" >/dev/null; then
  CF=/opt/data/cloudflared/cloudflared
  if [ -x "$CF" ] && [ -f /opt/data/.cloudflared/config.yml ]; then
    TUNNEL=$(grep -m1 '^tunnel:' /opt/data/.cloudflared/config.yml | awk '{print $2}')
    if [ -n "$TUNNEL" ]; then
      nohup "$CF" tunnel run "$TUNNEL" >> /opt/data/logs/cloudflared.log 2>&1 </dev/null &
      OUT="$OUT restarted tunnel"
    fi
  fi
fi

[ -n "$OUT" ] && echo "[webui-tunnel-health] $(date -u +%H:%MZ):$OUT"
