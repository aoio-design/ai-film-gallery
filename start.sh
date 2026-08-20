#!/usr/bin/env bash
# Start the shot-review gallery.
# SET YOUR OWN PASSWORD FIRST (see README) — the code has a public fallback.
cd "$(dirname "$0")"
export GALLERY_PASSWORD=change-me
export GALLERY_PORT=80
# Use port 8080 instead if port 80 is unavailable on your server.
.venv/bin/python app.py > gallery.log 2>&1 &
echo "Gallery started"
