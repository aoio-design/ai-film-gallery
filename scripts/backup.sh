#!/bin/bash
# Weekly backup to your private GitHub repo — SILENT on success; prints a line on failure.
# One-time setup (your agent can do this):
#   1. Create a PRIVATE GitHub repo (e.g. "my-agent-backup") and a personal access token.
#   2. git clone https://<TOKEN>@github.com/YOU/my-agent-backup.git /opt/data/hermes-backup
#   3. The script below copies your data in, commits and pushes.
# If your paths differ from the defaults, set BACKUP_DIR / REPO_URL at the top.
BACKUP_DIR="${BACKUP_DIR:-/opt/data/hermes-backup}"
cd "$BACKUP_DIR" || exit 1

# Copy latest data (skip nothing: config, skills, memories, pipeline, gallery data)
cp /opt/data/config.yaml ./config.yaml 2>/dev/null
cp -r /opt/data/skills/* ./skills/ 2>/dev/null
cp /opt/data/memories/* ./memories/ 2>/dev/null
cp -r /opt/data/ai-film-pipeline/* ./pipeline/ 2>/dev/null
cp -r /opt/data/gallery/data ./gallery-data/ 2>/dev/null

# Scrub secrets from the committed config copy
sed -i 's/api_key:.*/api_key: REDACTED/' config.yaml 2>/dev/null

if git add -A && git commit -m "auto-backup $(date +%Y-%m-%d)" >/dev/null 2>&1; then
  if git push >/dev/null 2>&1; then
    : # silent = healthy
  else
    echo "[backup] push FAILED on $(date -u +%Y-%m-%dT%H:%MZ) — check the git remote"
  fi
fi
