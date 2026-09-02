#!/bin/bash
# Weekly backup to your private GitHub repo — SILENT on success; prints a line on failure.
# One-time setup (your agent can do this):
#   1. Create a PRIVATE GitHub repo (e.g. "my-agent-backup") and a personal access token.
#      (Guide Method A: the token is stored on the owner's Keys page as GITHUB_TOKEN —
#      never ask for it in a chat.)
#   2. git clone https://<TOKEN>@github.com/YOU/my-agent-backup.git /opt/data/hermes-backup
#   3. The script below copies your data in, commits and pushes.
# If your paths differ from the defaults, set BACKUP_DIR / STUDIO_DIR at the top.
BACKUP_DIR="${BACKUP_DIR:-/opt/data/hermes-backup}"
STUDIO_DIR="${STUDIO_DIR:-/opt/data/studio}"
cd "$BACKUP_DIR" || exit 1

# Copy the small, irreplaceable things: your agent's config, skills and memories,
# plus your studio's WORDS (project list and every shot's script/prompt/feedback
# JSON). Generated media (images, video) is deliberately NOT copied — it is huge,
# and it can be regenerated from the prompts that ARE backed up.
cp /opt/data/config.yaml ./config.yaml 2>/dev/null
cp -r /opt/data/skills/* ./skills/ 2>/dev/null
cp /opt/data/memories/* ./memories/ 2>/dev/null
rm -rf ./gallery-data && mkdir -p ./gallery-data
if [ -d "$STUDIO_DIR/data" ]; then cp -r "$STUDIO_DIR/data" ./gallery-data/data; fi
if [ -d "$STUDIO_DIR/shots" ]; then
  find "$STUDIO_DIR/shots" -name '*.json' 2>/dev/null | while read -r f; do
    rel="${f#$STUDIO_DIR/}"
    mkdir -p "./gallery-data/$(dirname "$rel")"
    cp "$f" "./gallery-data/$rel"
  done
fi

# Scrub secrets from the committed config copy
sed -i 's/api_key:.*/api_key: REDACTED/' config.yaml 2>/dev/null

if git add -A && git commit -m "auto-backup $(date +%Y-%m-%d)" >/dev/null 2>&1; then
  if git push >/dev/null 2>&1; then
    : # silent = healthy
  else
    echo "[backup] push FAILED on $(date -u +%Y-%m-%dT%H:%MZ) — check the git remote"
  fi
fi
