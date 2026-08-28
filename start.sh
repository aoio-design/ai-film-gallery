#!/usr/bin/env bash
# Start the shot-review gallery.
#
# Logins are email + password. Create your account first (one time):
#   python3 accounts/aoio_auth.py add you@example.com --name "Your Name"
# It prints a generated password — save it. Change it any time with:
#   python3 accounts/aoio_auth.py passwd you@example.com
# List accounts:
#   python3 accounts/aoio_auth.py list
#
# FIRST RUN, before any account exists: the app prints a RANDOM one-time setup
# code to gallery.log — use it to open the page once, then create your account.
# No password is hardcoded here or in the source, so this public repo gives an
# attacker nothing: `grep setup- gallery.log` on YOUR server is the only way in.
cd "$(dirname "$0")"

# Stable session key so restarting the gallery does not sign you out.
if [ ! -f .secret ]; then
  head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' > .secret
  chmod 600 .secret
fi
export GALLERY_SECRET="$(cat .secret)"

# Set this to 1 once the gallery is reached only over HTTPS (Cloudflare tunnel):
# it marks the session cookie Secure. Leave unset while testing on 127.0.0.1.
# export GALLERY_SECURE_COOKIE=1

export GALLERY_PORT=80
# Use port 8080 instead if port 80 is unavailable on your server.
.venv/bin/python app.py > gallery.log 2>&1 &
echo "Gallery started"
