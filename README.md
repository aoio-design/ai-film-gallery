# AI Film Gallery

A private, login-protected **shot-review gallery** for AI film production. It shows every shot of your film as a card — script text, audio, prompts, generated video, and your feedback notes — in one private web page you open in your browser.

Part of the **[Agentic AI Film Production Studio](https://guide.aoiostudios.cloud)** guide. It runs on the same VPS as your AI agent; no extra hosting, no extra cost.

## Features

- **Shot cards** — one card per shot: script, audio files, image/video prompts (editable inline), generated video, and a feedback thread.
- **Video Preview** — a sequence player at the top of each episode page that plays every generated clip end-to-end, with Prev/Play/Next, Loop, and a Follow toggle that scrolls the card row in sync with playback.
- **Two formats per project** — `director` (Script → Audio → Video Prompt → Video) and `standard` (adds Image Prompt + Image rows). Switch by editing the `"format"` field in `data/projects.json`.
- **Email + password login** — real accounts (`owner` / `reviewer`), scrypt-hashed, stored in a local SQLite file. No email server needed, and none used.
- **Self-contained** — only needs Python + Flask. No database, no build step.

## Quick start

```bash
git clone https://github.com/aoio-design/ai-film-gallery.git
cd ai-film-gallery
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

1. **Create your account** (email + password):

   ```bash
   python3 accounts/aoio_auth.py add you@example.com --name "Your Name"
   ```

   It prints a generated password — save it. Set your own instead with
   `python3 accounts/aoio_auth.py passwd you@example.com 'your-password'`.

   > ⚠️ **There is no "forgot password" link, by design.** This app sends no email
   > (your server runs no mail server), so a reset link could never reach you.
   > Reset from the terminal — or ask your AI agent to run it for you:
   > `python3 accounts/aoio_auth.py passwd you@example.com`
   >
   > `start.sh` also ships a one-time `GALLERY_PASSWORD` bootstrap value that is
   > accepted **only while zero accounts exist**, so a fresh install is reachable
   > before the first account is created. It stops working the moment you add one.

2. **Start it:**

   ```bash
   bash start.sh
   ```

   Verify it's alive: `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:80/` → expect `302` (login redirect). If you get `Permission denied` on port 80, change `GALLERY_PORT=80` to `8080` in `start.sh`.

3. **Reach it from the internet** with a Cloudflare tunnel (the guide's Chapter 3/7 walks through this): point a subdomain at `http://localhost:80` (or `8080`).

## Accounts (`accounts/aoio_auth.py`)

One account store, shared by the gallery and the agent gate. Stdlib only — no
extra packages, works with any Python 3.11+.

```bash
python3 accounts/aoio_auth.py list                      # who can sign in
python3 accounts/aoio_auth.py add you@example.com --name "Your Name"
python3 accounts/aoio_auth.py add editor@example.com --role reviewer
python3 accounts/aoio_auth.py passwd you@example.com    # reset (prints a new one)
python3 accounts/aoio_auth.py disable old@example.com
python3 accounts/aoio_auth.py verify you@example.com 'password'   # test a login
```

- Roles: `owner` = gallery **and** agent Web UI; `reviewer` = gallery only.
- Passwords are scrypt-hashed (n=2¹⁵), never stored or logged in plain text.
- Store: `accounts/users.db` (SQLite, chmod 600). Set `AOIO_AUTH_DB` to move it.
- **No password-reset email, ever.** Resets are terminal-only (see above).

## Agent login gate (`agent-gate/`)

The [Hermes Web UI](https://github.com/nesquena/hermes-webui) upstream ships a
single shared password. This gate puts the same email + password login in front
of it **without patching upstream** — so Web UI updates never break it:

| Request | Goes to |
|---|---|
| `GET /login`, `POST /api/auth/login` | the gate (port 8790) — your email + password form |
| everything else | the Web UI (port 8787), untouched |

On a correct email + password the gate signs in to the Web UI with its internal
`HERMES_WEBUI_PASSWORD` and hands your browser the Web UI's own session cookie.
Because your tunnel routes those two paths to the gate, the Web UI's password
form is never exposed to the internet, and its password becomes an internal
secret you don't type.

```bash
bash agent-gate/start.sh        # starts it on port 8790
curl -s http://127.0.0.1:8790/health   # -> ok
```

Cloudflare tunnel ingress (order matters — the path rule must come first):

```yaml
ingress:
  - hostname: agent.YOURDOMAIN.com
    path: ^/(login|api/auth/login)/?$
    service: http://localhost:8790
  - hostname: agent.YOURDOMAIN.com
    service: http://localhost:8787
  - service: http_status:404
```

Passkeys, if you registered any in the Web UI, still work — the gate shows the
passkey button and those endpoints go straight through.

## How your film is stored

- `data/projects.json` — the list of films (`projects`) and their shots. The `"format"` field picks the card layout.
- `shots/<film>/<shot>/` — one folder per shot: `image.png` (keyframe), `video.mp4` (clip), `*.wav`/`*.mp3` (dialogue audio — multiple supported), and `metadata.json` (script, prompts, feedback).

Your film data lives in `data/` and `shots/` — both are git-ignored, so your work never ends up in the repo.

## Agent-friendly

Your AI agent can drive the gallery over two simple endpoints:

- `POST /p/<film>/<shot>/update` with `field=script|image_prompt|video_prompt` + `value=...` — edit prompts programmatically.
- `POST /p/<film>/<shot>/feedback` with `text=...` — leave feedback.

## License

MIT — free to use, modify, and redistribute. Built for the [Agentic AI Film Production Studio](https://guide.aoiostudios.cloud) guide.

## Helper scripts (`scripts/`)

Scheduled-job scripts for keeping your studio alive (see the guide, Chapter 8 "Your automatic crew"):

- `gallery-watchdog.sh` — every 5 min; restarts the gallery if it dies
- `webui-tunnel-health.sh` — every 5 min; restarts the Web UI, the agent login gate, the gallery and the Cloudflare tunnel if any are down
- `backup.sh` — weekly; backs up config/skills/pipeline/gallery data to your private GitHub repo
- `hermes-update-check.sh` — weekly; pings when a newer Hermes build exists (silent when current)
- `webui-update-check.sh` — weekly; pings when a newer Web UI build exists (silent when current)

Each prints output only when it acted (empty stdout = healthy = silent), so they work as `no_agent` cron scripts.

- `gallery-feedback-watch.py` — every 30 min; silent, prints a digest when new shot/script feedback arrives (first run baselines silently)
