# Studio Operations Skill

*Use when: managing the review studio — creating projects and seasons, saving
generated assets into shot folders, populating the Character Bible & Assets
page, reading and acting on feedback.*

## What the studio is

A private web app (Flask) on the VPS, behind an email + password login, that
displays every shot of a film as a card: image → audio → video prompt → video
+ feedback. Every project uses `"format": "director"` — that is the only
layout in use. It also has a **Character Bible & Assets** page where
characters, locations and props (with voices, references and full character
notes) are reviewed.

Pages: `/projects` (seasons/films landing) · `/s/<season>` (episode cards) ·
`/a/<season>` (Character Bible & Assets) · `/p/<episode>` (script pane + shot
cards). The owner reviews characters on `/a/…` and script + shots on `/p/…`;
both panes are drag-resizable and every box has a feedback field.

Light/dark mode is available on every page (🌙/☀️ button, top-right). The
choice is remembered per browser.

## Where everything lives

| Path | What it is |
|---|---|
| `/opt/data/studio/` | The app (edit nothing except `start.sh`) |
| `/opt/data/studio/data/projects.json` | The list of seasons, films and their shots |
| `/opt/data/studio/shots/<film>/<shot>/` | One folder per shot, media inside |
| `/opt/data/studio/assets/<season>/<asset>/` | Character/Location/Prop folders for the Bible & Assets page |
| `/opt/data/studio/masters/<film>/<shot_id>.mp4` | Approved clips upscaled to 4K — the owner's finished footage |
| `gallery.YOUR-DOMAIN.com` | The public address (Cloudflare tunnel) |

## Accounts & logins (email + password)

The gallery and the owner's agent Web UI share ONE account store — the
stdlib-only program `aoio_auth.py`. It normally lives at
`/opt/data/aoio-auth/aoio_auth.py` (the gallery's `start.sh` points at it with
`export AOIO_AUTH_DIR=/opt/data/aoio-auth`); a standalone copy also ships inside
the app at `/opt/data/studio/accounts/aoio_auth.py`.

```bash
python3 /opt/data/aoio-auth/aoio_auth.py list                      # who can sign in
python3 /opt/data/aoio-auth/aoio_auth.py passwd owner@example.com   # reset (prints a new password)
python3 /opt/data/aoio-auth/aoio_auth.py add editor@example.com --role reviewer
python3 /opt/data/aoio-auth/aoio_auth.py disable editor@example.com
python3 /opt/data/aoio-auth/aoio_auth.py verify owner@example.com 'password'   # test a login
```

- Roles: `owner` = gallery **and** agent Web UI. `reviewer` = gallery only.
- **There is no password-reset email and there never will be** — the VPS runs no
  mail server (providers block outgoing mail ports), so a reset link could not be
  delivered. When the owner says "I forgot my password", run the `passwd` command
  above and tell them the new password. Never invent a reset link or claim an
  email was sent.
- First run, before any account exists: the app prints a RANDOM one-time setup
  code to `gallery.log` (`grep setup- /opt/data/studio/gallery.log`). It dies the
  moment an account exists. There is NO default password in the source (the repo is
  public) — never look for one, never invent one.
- Both login surfaces throttle failures: 10 per IP per 5 minutes → HTTP 429. If the
  owner reports "Too many attempts", wait out the window instead of retrying; verify
  the password out-of-band with
  `AOIO_PASSWORD='…' python3 /opt/data/aoio-auth/aoio_auth.py verify <email>`
  (env var keeps it out of shell history).
- Minimum password length is 12 characters.
- The agent Web UI login is served by the gate at
  `/opt/data/agent-gate/gate.py` (port 8790). Health check:
  `curl -s http://127.0.0.1:8790/health` → `ok`. If the gate is down, nobody can
  sign in to the Web UI (`/login` returns 502) — restart it with
  `nohup python3 /opt/data/agent-gate/gate.py >> /opt/data/logs/agent-gate.log 2>&1 &`
  and confirm the tunnel still routes `^/(login|api/auth/login)/?$` to port 8790.
- Never print a password into a shared channel other than the owner's own chat,
  and never write one into a file or a log.

## Seasons & episodes

`projects.json` supports an optional `"seasons"` key:

```json
{"seasons": [{"id": "my-s1", "title": "My Season 1", "episodes": ["my-ep1", "my-ep2"]}]}
```

- `/projects` lists seasons (when present), each linking to its season page.
- `/s/<season_id>` is the season page → episode cards + the Character Bible & Assets link.
- `/p/<episode_id>` is the episode page (the shot cards).
- Without seasons the gallery falls back to a flat project list (backward compatible).

## Character Bible & Assets page (`/a/<scope>`)

The scope is a season id (preferred) or a project id. Assets live in
`assets/<scope>/<asset_id>/metadata.json` + media files. Each asset is one
folder; the agent populates it by dropping files + `metadata.json` in.

**metadata.json fields** (all optional, all editable in the UI):

```json
{
  "id": "nora-chen",
  "name": "Nora Chen",
  "type": "Character",            // Character | Location | Prop
  "role": "Lead — the story's protagonist",
  "appearance": "…",
  "personality": "…",             // personality & backstory
  "distinguishing": "…",          // distinguishing features
  "wardrobe": "…",                // palette, silhouette, texture
  "emotional_range": "…",         // NEUTRAL/HAPPY/CONCERNED/… cards
  "body_language": "…",           // movement & posture profile
  "voice": "nora_voice.wav",      // voice file reference
  "status": "Approved",           // Approved | Revision | Generated
  "description": "…",
  "prompt": "…",                  // generation prompt
  "feedback": [{"timestamp": "…", "text": "…"}]
}
```

**Character Bible table** (type=Character) renders two rows per character:
row 1 = Appearance · Personality & Backstory · Distinguishing Features ·
Reference (images); row 2 = Wardrobe / Style · Emotional Range · Body
Language Profile · Voice (audio). Every field is an editable autosave
textarea (except Reference/Voice which show media). Character name, Status
and Feedback span both rows. Characters sort **leads/main first, then
supporting** (derived from `role`).

**Location Scenes and Props table** (all non-Character types): Type · Name ·
Preview (images/audio) · Prompt (editable) · Status · Feedback.

Voices live inline in the Bible's Voice column — do NOT create standalone
Voice assets.

## File naming the gallery expects

| File name | What it shows on the card |
|---|---|
| `image.png` or `image.jpg` | Keyframe image row |
| `video.mp4` (`.webm`, `.mov`) | Video row |
| `*.wav`, `*.mp3`, `*.m4a`, `*.flac`, `*.ogg`, `*.aac` | Audio row — several allowed (`line-1.wav`, `line-2.wav`, `ambient.wav`) |
| `metadata.json` | Script, prompts, feedback notes (with timestamps) |

## Episode script pane

Each episode page has an Episode Script editor at the top (left pane,
monospace, line numbers). It autosaves on blur. If
`shots/<film>/_episode_script.json` exists, its `text` wins (assembled with
`[ShotID]` markers); otherwise it's assembled from each shot's `script`
field. Feedback on the script lives in that JSON's `feedback[]` too.

## Rules

1. **A shot only appears if it's listed in `projects.json`.** Dropping files
   into `shots/` is not enough — add the shot to the project's `shots` list.
2. **Exact names or nothing.** The app looks up media by the exact filenames
   in the table above.
3. **Feedback is timestamped and incremental.** Read ONLY notes newer than
   the shot's last regeneration; act on those, then regenerate.
4. **One layout only:** always set `"format": "director"` on a new project.
   The 5-row "standard" layout is retired — never offer it to the owner.
5. **The agent uploads assets** (characters, locations, props) into
   `assets/<season>/<asset_id>/` so the owner can review and leave feedback
   on them — same feedback loop as shots.

## The production loop (follow this order — it is the owner's workflow)

The gallery starts EMPTY. Nothing in it is created by hand by the owner; you
create it all. The loop:

1. **Idea chat (Web UI).** The owner brings an idea; you ask questions and
   shape it with them. No files yet.
2. **Write it up, then populate the studio.** When the owner says go: write the
   script, break it into 3–6 second shots, build the character/location/prop
   bible, then create everything in the gallery — the project (or season) in
   `projects.json`, the assets in `assets/<season>/…` (`/a/<season>`), the
   episode entries (`/s/<season>`) and every shot card (`/p/<episode>`), with
   the episode script in `_episode_script.json`. **Words only at this stage —
   no generation, no cost.**
3. **Draft review.** The owner leaves feedback on `/a/<season>` (characters,
   sets, props) and on `/p/<episode>` (script pane + per-shot boxes). Read only
   notes newer than your last revision, amend the drafts, re-upload, and say
   what changed. Loop until the owner approves the words.
4. **Generation — ASK ABOUT THE COST FIRST (see the rule below).** Generate
   keyframes and clips through the owner's fal.ai account (see the
   `fal-ai-ops` skill), save them into the shot folders / asset folders with
   the exact filenames, and tell the owner what is ready to review and what
   the batch cost.
5. **Media review.** Same feedback loop: a note on a card = regenerate that one
   shot or asset. An "approved" note = done.
6. **Approved video → 4K master.** When the owner approves a shot's video,
   upscale that clip to 4K with the fal.ai upscaler (see the `fal-ai-ops`
   skill), then save the master on the VPS as
   `/opt/data/studio/masters/<film>/<shot_id>.mp4` (create the folder if it
   doesn't exist) and tell the owner the exact path. Never overwrite the
   review copy in `shots/<film>/<shot>/video.mp4` — the card keeps showing
   that one. If the owner ever asks where their finished clips are, answer
   with this folder.

## fal.ai key and spending rule (MANDATORY — never break this)

All generation runs through the owner's **fal.ai** account — the key is
stored as `FAL_KEY` in the Hermes app's Keys page (see the `fal-ai-ops`
skill) — and every successful output costs the owner money (roughly US$0.06
per image, ~US$0.40 per 5-second clip, ~US$0.14 per 4K upscale).

- **Never** start a paid batch, assume one was approved, or silently wait.
- The moment you receive feedback (from the gallery, the watcher, or chat)
  that requires generation, message the owner on **Telegram or WhatsApp** and
  ask ONE of these, then do exactly what they answer:
  1. *"Shall I generate the [N] shots now? It'll cost about US$X."* → wait for
     a yes, then run the whole batch in one go.
  2. *"Which shots should I regenerate?"* → re-roll only the shots they name.
- Check the fal balance before a batch and warn the owner to top up if it's
  low. Report what each batch actually cost when it finishes.
- Never generate before the script and drafts are approved — words cost
  nothing, media costs money.

## Feedback watcher (optional but recommended)

`studio-feedback-watch.py` scans every shot's `metadata.json` feedback[]
plus each project's `_episode_script.json` feedback[], and reports ONLY
entries newer than the last run (marker file, 60s grace). Silent when nothing
new. Wire it up as a scheduled job every 30 minutes:

```
hermes cron create 'every 30m' --name 'Studio feedback watcher' --no-agent --script studio-feedback-watch.py
```

First run records the baseline silently. This closes the loop: owner leaves
feedback → watcher pings → agent reads the files and acts.

## Troubleshooting

- `502 Bad Gateway` → the app stopped. Check `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:80/` — `302` means fine; no answer means restart with `bash /opt/data/studio/start.sh`.
- Shot missing from the page → not in `projects.json` (rule 1).
- `Address already in use` → already running; do nothing.
- Light/dark toggle not remembered → check the browser's localStorage
  (`aio-theme` key); it is shared with the Guide site by design.
