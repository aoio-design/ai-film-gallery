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

**metadata.json fields** — Characters (all editable in the UI):

```json
{
  "id": "nora-chen",
  "name": "Nora Chen",
  "type": "Character",             // Character | Location | Prop
  "role": "Lead — the story's protagonist",
  "appearance": "…",              // looks: age, build, face, hair, skin, posture
  "personality": "…",             // personality & backstory
  "distinguishing": "…",          // distinguishing features
  "wardrobe": "…",                // palette, silhouette, texture
  "emotional_range": "…",         // NEUTRAL/HAPPY/CONCERNED/… cards
  "body_language": "…",           // movement & posture profile
  "character_sheet_prompt": "…",  // image prompt for the reference sheet —
                                  // compose it from the six fields above
  "voice_prompt": "…",            // voice direction / TTS prompt (if any)
  "voice": "nora_voice.wav",      // voice file reference
  "status": "Approved",           // Approved | Revision | Generated
  "feedback": [{"timestamp": "…", "text": "…"}]
}
```

Locations and Props use the same file with `"type": "Location"` or
`"type": "Prop"` and carry `description` + `prompt` (their generation
prompt) + media only — no bible fields.

**When you populate a Character asset, write EVERY one of the six bible
fields** — appearance, personality & backstory, distinguishing features,
wardrobe/style, emotional range, body language — from the approved script
and your story notes; none is optional. Then write `character_sheet_prompt`,
the image-model prompt for that character's reference sheet, composed from
the relevant text in those six fields (sheet format: `ai-film-prompt-
engineering` skill). The structure is defined right here — never open another
project's or another asset's texts to copy their shape.

**Character Bible table** (type=Character) renders an editable grid per
character: row 1 = Appearance · Personality & Backstory · Distinguishing
Features · Wardrobe / Style; row 2 = Emotional Range · Body Language
Profile · Character Sheet Prompt · Reference Voice Prompt. Reference Images
and Reference Voice sit below the grid. Every text field is an autosave
textarea. Characters sort **leads/main first, then supporting** (derived
from `role`).

**Location Scenes and Props table** (all non-Character types): Type · Name ·
Preview (images/audio) · Prompt (editable) · Status · Feedback.

Voices live inline in the Bible's Voice column — do NOT create standalone
Voice assets.

## Media file naming standard

Save every generated file under a descriptive, VERSIONED name — never a bare
`image.png` / `video.mp4`, and never overwrite an existing file. Each
regeneration is a NEW file with the next version number.

Pattern: `<scope-id>_<Entity>_<Kind>_v<N>[<_option>].<ext>`

| Media | File name |
|---|---|
| Character sheet | `<season-id>_<CharacterName>_Reference_Sheet_v1.png` |
| Location sheet | `<season-id>_<LocationName>_v1.png` |
| Prop sheet | `<season-id>_<PropName>_v1.png` |
| Keyframe image | `<episode-id>_<ShotID>_v1.png` |
| Video clip | `<episode-id>_<ShotID>_v1.mp4` (same v-number as its keyframe) |
| 4K master | same name as the approved clip, in `masters/<film>/` |
| Voice reference | `<season-id>_<CharacterName>_Audio_Reference_v1.wav` |
| `metadata.json` | Script, prompts, feedback notes (with timestamps) |

Rules
- Scope tokens are the studio's own folder ids, verbatim: a season folder
  (`my-s1`) for assets, an episode folder for shots; the shot token is the
  shot id exactly as it appears on the page (`Ep1-01`). Entity names drop
  spaces and apostrophes (`Maya Chen` → `MayaChen`). Underscores are the only
  separator — no spaces or special characters.
- `v<N>` = generation attempt (1, 2, 3 …): bump it every time the owner asks
  for a new or regenerated version. Several candidates delivered in ONE
  attempt get letters: `_v1_a.png`, `_v1_b.png`.
- The studio lists every file it finds in a folder, so older takes stay
  visible for comparison. The owner approves a file with the star; the studio
  auto-clears that approval when a newer file arrives — never edit approvals
  yourself.
- Characters/locations/props reused in later seasons keep their original
  files. Reference them from their home season folder — never copy, rename,
  or regenerate them elsewhere unless the owner asks for a new version.

## Episode script pane

Each episode page has an Episode Script editor at the top (left pane,
monospace, line numbers). It autosaves on blur. If
`shots/<film>/_episode_script.json` exists, its `text` wins (assembled with
`[ShotID]` markers); otherwise it's assembled from each shot's `script`
field. Feedback on the script lives in that JSON's `feedback[]` too.

## Rules

1. **A shot only appears if it's listed in `projects.json`.** Dropping files
   into `shots/` is not enough — add the shot to the project's `shots` list.
2. **Versioned names, never overwrite.** Save media under the naming standard
   above, always bumping `v<N>`; the app lists every file in the folder, so
   old takes stay visible for comparison.
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
   review copy in the shot folder (`shots/<film>/<shot>/`) — the card keeps showing
   that one. If the owner ever asks where their finished clips are, answer
   with this folder.

## fal.ai key and spending rule (MANDATORY — never break this)

> All generation runs through the owner's **fal.ai** account — the key is
> stored as `FAL_KEY` in the Hermes app's Keys page (see the `fal-ai-ops`
> skill) — and every successful output costs the owner money (roughly US$0.17
> per character sheet at high quality, US$0.04 per location or prop at medium,
> US$0.16 per keyframe, ~US$0.40 per 5-second clip, ~US$0.14 per 4K upscale).

- **Never** start a paid batch, assume one was approved, or silently wait.
  **Quote the cost, then get an explicit yes — even when the owner says
  "go generate".** "Go" or "yes" to an earlier step is NOT approval for a
  paid batch: before the first paid request, state the exact scope and the
  estimated cost and WAIT for an explicit yes to THAT message. Never
  announce a batch and its cost in the same message as launching it — the
  quote comes first, on its own, and the batch starts only after approval.
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
- **CLARIFY FIRST — ambiguous feedback = ask, then wait.** If a note or
  instruction could mean more than one thing — which assets are meant,
  whether "finished reviewing" means "approved, go ahead", which step
  "generate" refers to — message the owner and ask what they mean BEFORE
  acting. Never guess, never pick a reasonable default. (Owner's house rule,
  applies to every prompt in the pack.)

## Feedback watcher (recommended — acts on feedback automatically)

`studio-feedback-watch.py` scans EVERY studio feedback location: shot
`metadata.json`, episode `_episode_script.json`, asset (Character Bible)
`metadata.json`, and the studio-wide `_studio_feedback.json` list. It reports
ONLY entries newer than the last run (marker file, 60s grace). Silent when
nothing new.

Wire it up as an **agent-mode cron with monitor_script** (not no_agent) so
your agent receives the feedback, ACTS on it, and **replies back in the
Studio's Talk-to-your-agent drawer**:

```text
hermes cron create 'every 5m' --name 'Studio feedback watcher' --deliver local \
  --monitor-script studio-feedback-watch.py \
  --prompt 'New feedback appeared in the Studio (via the Talk-to-your-agent drawer). Open each reported file, read every feedback entry in full, and act on it: revise the referenced script lines, shots, or asset prompts (text edits cost nothing). Then append a reply to /opt/data/studio/shots/_agent_replies.json as [{"timestamp": "...", "project": "<project id from the file path, or null>", "text": "what you changed"}] so the owner sees it in the drawer. Preserve existing records.
GENERATION / PAID WORK: this cron session has NO paid key and must NEVER attempt generation (no images, clips, upscaling). When the owner asks to generate: (1) look up and state the fal.ai cost, (2) do NOT generate — tell the owner to go back to the WebUI/Telegram/WhatsApp to run it with their paid session, and (3) if they forgot the flow, point them back to their live chat to trigger it. Report concisely what you changed.'
```

> ⚠️ **Two hard rules for this job:**
> 1. **`--deliver local` ONLY.** The agent's reply appears in the studio drawer, so it must NOT also blast a Telegram/WhatsApp channel every time the owner sends feedback (that would spam them on every note). Keep the OTHER scheduled jobs (health checks, backup, update checks) delivering to a channel so the owner is only pinged when something actually needs attention.
> 2. **Never generate from this cron.** The background job has no paid key. Paid generation (images, clips, upscaling via fal.ai) must be run by the owner in their live WebUI/Telegram/WhatsApp session. The agent's job is to report the cost and redirect the owner there — never attempt generation itself.

This closes the loop: you leave feedback → watcher detects it (checks shots,
the episode script, your Character Bible assets, and your general studio
notes every 5 minutes) → your agent applies text changes and TELLS YOU what it
did in the drawer. If paid fal.ai generation is needed, the agent reports the
estimated cost and points you back to your live WebUI/Telegram/WhatsApp
session to run it — so money is only ever spent in a session you are present
in and have approved.

## "Talk to your agent" — how the loop works (and how to fix it)

The **Talk to your agent** button (bottom-right FAB) on every studio page sends
the owner's note to your own agent, and shows the agent's reply back in the
drawer. Any page with the FAB (episode `/p/…`, Character Bible `/a/…`) uses the
same loop — there is only one copy of the wiring, driven by files on disk.

**The loop, end to end:**

1. Owner types a note in the drawer and sends it → saved to a JSON file under
   `shots/` or `assets/` (episode notes → `shots/<project>/_episode_script.json`,
   shot notes → `shots/<project>/<id>/metadata.json`, Character Bible notes →
   `assets/<project>/<asset>/metadata.json`, general notes →
   `shots/_studio_feedback.json`).
2. The **Studio feedback watcher** cron (every 5 min) scans all of those
   locations via `studio-feedback-watch.py`. Only when a *new* note appears
   does it wake you (the agent), so it costs nothing while idle.
3. You read the note, **edit the text** (script line, prompt, character
   description — free, just do it), then **append a reply** to
   `shots/_agent_replies.json`:
   `[{"timestamp":"…","project":"<project id or null>","text":"what you changed"}]`.
   Keep any existing records — do NOT wipe the file.
4. The drawer polls `/agent_replies` every 8 seconds *while open* and shows
   your reply as a light-blue message. No page reload needed.
5. If the owner's request needs **paid fal.ai generation** (images, clips,
   upscaling), do NOT fire it and do NOT try from the cron. Look up and state
   the **estimated cost**, then tell the owner to **go back to their live
   WebUI/Telegram/WhatsApp session** to run it there (the paid key lives in
   that interactive session). If the owner seems to have forgotten the flow
   and asks you to "kick off" generation, point them back to their live chat
   to trigger it — never attempt generation from the cron.

**Design notes live in the studio code:** `docs/FAB-DESIGN.md` (in the studio
app folder) documents the full design, the reuse recipe, and the known
gotchas — read it before changing the FAB/drawer.

**If the owner says "I sent feedback but you didn't reply":** work through these
in order:

1. **Is the watcher cron running?** Ask the owner or run
   `hermes cron list` — confirm the *Studio feedback watcher* job exists and is
   `every 5m` with `--monitor-script studio-feedback-watch.py` AND **`deliver: local`**
   (it must NOT deliver to a channel, or the owner gets a message every time they
   send feedback). If missing, recreate it (command above) — this is the usual
   cause: an *agent-mode monitor* cron, NOT a `--no-agent` script job.
2. **Did the note land where the watcher looks?** Check the file listed by the
   note's target. All four locations are scanned — shots, episode script,
   Character Bible assets, and the general inbox. If you found the note on disk
   but the watcher never reported it, the marker file (`shots/.feedback-watch-state`)
   may have been advanced past it by a manual run — advance it back to ≥60s
   *before* the note's timestamp, then re-run the cron.
3. **Was your reply written?** Confirm `shots/_agent_replies.json` has the new
   record and is valid JSON (preserve prior records). The drawer won't show a
   reply that isn't in that file.
4. **Is the owner looking at the right page?** Replies are filtered by project;
   a reply written with `project: null` shows on every page, one with a project
   id shows only on that project's pages. Match the project id.

## Troubleshooting

- `502 Bad Gateway` → the app stopped. Check `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:80/` — `302` means fine; no answer means restart with `bash /opt/data/studio/start.sh`.
- Shot missing from the page → not in `projects.json` (rule 1).
- `Address already in use` → already running; do nothing.
- Light/dark toggle not remembered → check the browser's localStorage
  (`aio-theme` key); it is shared with the Guide site by design.
