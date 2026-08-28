#!/usr/bin/env bash
# Start the shot-review gallery.
#
# Logins are email + password. Create your account first (one time):
#   python3 accounts/aoio_auth.py add you@example.com --name "Your Name"
# It prints a generated password — save it. Change it any time with:
#   python3 accounts/aoio_auth.py passwd you@example.com
# List accounts:
#   python3 accounts/aoio_auth.py list
cd "$(dirname "$0")"

# Bootstrap-only password: accepted ONLY while zero accounts exist, so a brand
# new install is reachable before you create your first account. It stops
# working the moment an account exists. Change it anyway.
export GALLERY_PASSWORD=change-me-first-run

# Stable session key so restarting the gallery does not sign you out.
if [ ! -f .secret ]; then
  head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' > .secret
  chmod 600 .secret
fi
export GALLERY_SECRET="$(cat .secret)"

export GALLERY_PORT=80
# Use port 8080 instead if port 80 is unavailable on your server.
.venv/bin/python app.py > gallery.log 2>&1 &
echo "Gallery started"
