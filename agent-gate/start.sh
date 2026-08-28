#!/usr/bin/env bash
# Start the agent login gate — email + password sign-in for your Hermes Web UI.
#
# Accounts are shared with the gallery (../accounts/aoio_auth.py):
#   python3 ../accounts/aoio_auth.py add you@example.com --name "Your Name"
#
# Your Cloudflare tunnel must send ONLY these two paths here (port 8790):
#   ^/(login|api/auth/login)/?$   ->  http://localhost:8790
#   everything else               ->  http://localhost:8787   (the Web UI)
set -e
cd "$(dirname "$0")"

export WEBUI_URL=http://127.0.0.1:8787
export WEBUI_ENV_FILE=/opt/data/hermes-webui/.env   # where HERMES_WEBUI_PASSWORD lives
export AGENT_GATE_PORT=8790
export AGENT_GATE_TITLE=Hermes

mkdir -p /opt/data/logs
if pgrep -f "agent-gate/gate[.]py" > /dev/null; then
  echo "Agent gate already running"
  exit 0
fi
nohup python3 gate.py >> /opt/data/logs/agent-gate.log 2>&1 &
sleep 1
echo "Agent gate started on port ${AGENT_GATE_PORT} — log: /opt/data/logs/agent-gate.log"
