#!/usr/bin/env bash
# WebUI + Cloudflare tunnel watchdog.
# Silent when healthy (empty stdout = no delivery). Prints a one-liner only when it restarted something.
OUT=""

# 1. WebUI on 8787
if ! curl -sf --max-time 5 http://127.0.0.1:8787/health >/dev/null 2>&1; then
  cd /opt/data/hermes-webui
  HERMES_WEBUI_PYTHON=/opt/hermes/.venv/bin/python3 nohup python3 bootstrap.py \
    --skip-agent-install --no-browser --foreground 8787 \
    >> /opt/data/logs/webui.log 2>&1 &
  OUT="$OUT restarted WebUI"
fi

# 2. cloudflared binary (persistent copy under /opt/data; /tmp is wiped on container recreate)
CF=/opt/data/cloudflared/cloudflared
if [ ! -x "$CF" ]; then
  mkdir -p /opt/data/cloudflared
  curl -sL --max-time 120 -o "$CF" \
    https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
  chmod +x "$CF"
  OUT="$OUT reinstalled cloudflared"
fi
# keep /tmp symlink for scripts that still reference /tmp/cloudflared
ln -sf "$CF" /tmp/cloudflared

# 3. Tunnel for consume-gallery (serves .cloud + .com hostnames)
if ! pgrep -f "cloudflared tunnel run consume-gallery" >/dev/null; then
  nohup "$CF" tunnel run consume-gallery \
    >> /opt/data/logs/cloudflared.log 2>&1 </dev/null &
  OUT="$OUT restarted tunnel"
fi

# 4. Coming-soon static page on 9000 (apex aoiostudios.com)
if ! curl -sf --max-time 5 http://127.0.0.1:9000/ >/dev/null 2>&1; then
  nohup python3 -m http.server 9000 --directory /opt/data/coming-soon \
    >> /opt/data/logs/coming-soon.log 2>&1 &
  OUT="$OUT restarted coming-soon"
fi

# 5. AOIO agent login gate on 8790 (email + password in front of the Web UI).
#    If this is down, agent.aoiostudios.com/login 502s and nobody can sign in.
if ! curl -sf --max-time 5 http://127.0.0.1:8790/health >/dev/null 2>&1; then
  nohup python3 /opt/data/agent-gate/gate.py \
    >> /opt/data/logs/agent-gate.log 2>&1 </dev/null &
  OUT="$OUT restarted agent gate"
fi

# 6. AI Film Studio gallery on 80 (own email + password login)
if ! curl -sf --max-time 5 http://127.0.0.1:80/login >/dev/null 2>&1; then
  (cd /opt/data/gallery && nohup bash start.sh >> /opt/data/logs/gallery-restart.log 2>&1 &)
  OUT="$OUT restarted gallery"
fi

if [ -n "$OUT" ]; then
  echo "[webui-tunnel-health] $(date -u +%H:%MZ):$OUT"
fi
