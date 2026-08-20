# AI Film Gallery

A password-protected **shot-review gallery** for AI film production. It shows every shot of your film as a card — script text, audio, prompts, generated video, and your feedback notes — in one private web page you open in your browser.

Part of the **[Agentic AI Film Production Studio](https://guide.aoiostudios.cloud)** guide. It runs on the same VPS as your AI agent; no extra hosting, no extra cost.

## Features

- **Shot cards** — one card per shot: script, audio files, image/video prompts (editable inline), generated video, and a feedback thread.
- **Video Preview** — a sequence player at the top of each episode page that plays every generated clip end-to-end, with Prev/Play/Next, Loop, and a Follow toggle that scrolls the card row in sync with playback.
- **Two formats per project** — `director` (Script → Audio → Video Prompt → Video) and `standard` (adds Image Prompt + Image rows). Switch by editing the `"format"` field in `data/projects.json`.
- **Password protected** — one password, typed once per browser session.
- **Self-contained** — only needs Python + Flask. No database, no build step.

## Quick start

```bash
git clone https://github.com/aoio-design/ai-film-gallery.git
cd ai-film-gallery
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

1. **Set your own password** — open `start.sh` and replace `change-me` with a password only you know (at least 12 characters).

   > ⚠️ **Security:** the app has a fallback password built into its code, and anyone who reads this README (or owns the guide) knows what it is. **Never run the gallery without setting `GALLERY_PASSWORD`** — you'd leave your film's front door unlocked.

2. **Start it:**

   ```bash
   bash start.sh
   ```

   Verify it's alive: `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:80/` → expect `302` (login redirect). If you get `Permission denied` on port 80, change `GALLERY_PORT=80` to `8080` in `start.sh`.

3. **Reach it from the internet** with a Cloudflare tunnel (the guide's Chapter 3/7 walks through this): point a subdomain at `http://localhost:80` (or `8080`).

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
