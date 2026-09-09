# fal.ai Ops Skill — generating images, video and masters via the fal API

*Use when: generating any media for the owner's films — reference images,
first-frame keyframes, video clips, or 4K masters — through the owner's fal.ai
account. There is no GPU to rent, no pod to start or stop: generation is a
paid API call that returns finished files.*

## The account and the key

- The owner has a **fal.ai** account (prepaid credits) and an **API key**
  stored as **`FAL_KEY`** in the Hermes app's **Keys** page — which puts it in
  your process environment. Confirm it with:
  ```bash
  echo ${FAL_KEY:+FAL_KEY is set}
  ```
  If it prints nothing, tell the owner to add `FAL_KEY` on the Keys page of
  their Hermes app (guide Chapter 4, Section 4.4) — **never** ask them to
  paste the key in chat.
- **Never print, log, or echo the key itself.** Secrets live in the
  environment; `echo $FAL_KEY` is for the *presence* check above only.

## The tool: genmedia (fal's CLI for agents)

Install once (the guide's Chapter 4, Section 4.5 has the owner-facing
instructions; if it's missing here, install it):

```bash
curl https://genmedia.sh/install -fsS | bash
export PATH="$HOME/.genmedia/bin:$PATH"
```

Verify the connection: `genmedia models minimax --limit 3` — a list with no
error means the key works. To see any model's exact flags:
`genmedia run <model-id> --help`.

## The five models (guide stack, 2026)

| Job | Model | Default settings |
|---|---|---|
| Character reference sheets | `openai/gpt-image-2` | `--image_size '{"width":1536,"height":1024}'`, `--quality high`, `--output_format png` |
| Location & prop reference images | `openai/gpt-image-2` | `--image_size '{"width":1536,"height":864}'`, `--quality medium`, `--output_format png` |
| Edits to an existing asset image | `openai/gpt-image-2/edit` | upload that image → `--image_urls '["<cdn>"]'`, single image at the asset's AR (location 1536×864 / character 1536×1024), quality tier follows the asset |
| First-frame edits (keyframes) | `openai/gpt-image-2/edit` | `--image_urls <refs>`, `--image_size '{"width":1920,"height":1080}'` (16:9 default; a vertical 9:16 project → `'{"width":1152,"height":2048}'`), `--quality high` |
| Reference voices (per character, once) | `fal-ai/elevenlabs/tts/eleven-v3` | 7-second line per character (~US$0.01); saved as `<season>_<CharacterName>_Audio_Reference_v1.wav` |
| Video clips (sound + cloned voice) | `minimax/h3-max/reference-to-video` | `--reference_image_urls <keyframe, then char sheets>` `--reference_audio_urls <speaker's voice wav>`, `--duration 5`, `--resolution 768P`, `--aspect_ratio 16:9`, `--prompt_expansion_mode balanced` |
| Upscaler (masters) | `fal-ai/bytedance-upscaler/upscale/video` | `--target_resolution 4k`, `--enhancement_preset aigc`, `--target_fps 24` |

### Reference image — text to image (GPT Image 2)

```bash
genmedia run openai/gpt-image-2 \
  --prompt "<structured prompt — see templates below>" \
  --image_size '{"width":1536,"height":1024}' --quality high --output_format png --download
```

**Structured prompt format:** `Scene:` / `Subject:` / `Important details:` / `Use case:` / `Constraints:`
**Character sheet (three-panel, landscape, ONE face):** plain neutral gray (#e0e0e0) backdrop, equal-width 3-panel horizontal sheet: Panel 1 face+shoulders close-up (front, neutral), Panel 2 full-body front (A-pose), Panel 3 full-body back (same pose as center); landscape 1536x1024. Use photographic vocabulary (full-frame DSLR 85mm f/2.8, soft three-point studio light, visible skin texture/pores, individual hair strands, real materials). Describe the character as realistic and unpolished — "avoid conventionally polished or symmetrical features". Do NOT include text labels, watermarks, inconsistent proportions, or background props.
**Location:** **4-panel sheet, 16:9 landscape** — wide establishing + alternate wide (~90°) + corner depth + detail shot; locked lighting/time-of-day, no people, environment only. (Full writing structure: `references/bible-and-asset-writing.md`.)
**Prop:** **4-panel grid, neutral gray (#e0e0e0)** — front + side (90°) + back + close-up detail; studio lighting, no cast shadows, consistent scale, no text labels.

### First-frame edit (keyframes) — GPT Image 2 edit

Upload the owner's reference images first, then reference them by URL:

```bash
genmedia upload /opt/data/studio/assets/<season>/<asset>/<file>.png
# → prints a cdn_url like https://v3b.fal.media/files/b/...
genmedia run openai/gpt-image-2/edit \
  --prompt "<composition prompt: put the subject from image 1 in the setting from image 2…>" \
  --image_urls '["<cdn_url_1>","<cdn_url_2>"]' --image_size '{"width":1920,"height":1080}' --quality high --output_format png --download
```

(Render keyframes at **1920×1080 (16:9)** by default — supersampled above H3 Max's 768p-class canvas (1344×768) so the model downsamples clean detail. `image_urls` accepts up to 16 refs. Optional `mask_url`: white = editable, black = preserved. Match the project's aspect ratio: a vertical-shorts project renders keyframes **1152×2048** (tell your agent "this is a vertical 9:16 project" when you start — 1080×1920 is not a valid custom size) and passes `--aspect_ratio 9:16` on clips. Character sheets and location images are always landscape — only keyframes follow the project's shape.)

### Asset image edit (rework an EXISTING reference image)
When the owner points at an image they can already see and asks for a change ("extract the top-left panel and go wider", "re-light this one"), EDIT that image — upload it, pass it as `--image_urls '["<cdn>"]'`, and say what the image shows + the ONE change. **Never re-run the whole-sheet text prompt for an image-driven change.** Deliver a SINGLE image at the asset's AR and quality tier (location 1536×864 medium / character 1536×1024 high), saved under a NEW versioned filename — the old take stays until the owner stars the new one. If instead the owner changed the *words* (edited the card's description/prompt), that IS a whole-sheet re-run from the amended prompt. Quote the fal price before running.

### Reference voice (per character — generate once, reuse on every clip)

Before clips: one short voice reference per speaking character.

```bash
genmedia run fal-ai/elevenlabs/tts/eleven-v3 \
  --text "<one neutral ~7s line in the character's voice>" \
  --voice "<voice preset or clone id — picked with the owner>" --download
```

~US$0.01 per character (US$0.10 per 1,000 chars). The character's asset card carries a **Reference Voice Prompt**; the same saved file is uploaded as Audio 1 on every clip where that character speaks.

### Video clip (keyframe + refs → clip with CLONED voice)

Everything goes in **one request** — the keyframe first (Image 1), then the character sheets of everyone on screen (Images 2, 3, …), then the speaker's voice reference (Audio 1). References are named in the prompt **by modality and list order**.

```bash
genmedia upload /opt/data/studio/shots/<film>/<shot>/<film>_<shot>_v1.png
genmedia upload /opt/data/studio/assets/<season>/<char>/<sheet>.png
genmedia upload /opt/data/studio/assets/<season>/<char>/<char>_Audio_Reference_v1.wav
# → three cdn_urls
genmedia run minimax/h3-max/reference-to-video \
  --prompt "Image 1 is the keyframe — the shot opens on this exact composition: match its framing, blocking and lighting. Image 2 is <Char>'s identity reference — preserve the face, hair, build and outfit exactly; <Char> is the speaker. Audio 1 is <Char>'s voice reference — the line is delivered in this voice. <scene + action + camera + soundscape> <Char> says, <delivery>: \"<line>\"" \
  --reference_image_urls '["<keyframe_cdn>","<sheet_cdn>"]' \
  --reference_audio_urls "<voice_cdn>" \
  --duration 5 --resolution 768P --aspect_ratio 16:9 --prompt_expansion_mode balanced --download
```

Rules:

- **AR is explicit per project** — 16:9 in this Guide (pass `--aspect_ratio`; vertical-shorts projects use 9:16, keyframes 1152×2048).
- **One speaker per clip, lines ≤ 5 seconds.** Two-speaker exchanges are generated as separate clips (shot/reverse-shot).
- **Voice consistency across shots = the same Audio ref file** every time that character speaks.
- **Do NOT re-upload the location sheet at the clip stage** — the keyframe already carries the setting, and every clip request has a small free allowance of reference inputs (~4 images' worth). Reference videos cost extra and are rarely needed.
- Dialogue goes inside the prompt in quotes with a delivery tone
  (`NOVA says: "It's everything." — tired, flat, quiet`), matched to the
  voice reference. One speaker per clip. The clip comes back with the voice
  and room sound baked in — there are no separate audio files.

### 4K master (approved clip → upscaled)

```bash
genmedia upload /opt/data/studio/shots/<film>/<shot>/<film>_<shot>_v1.mp4
genmedia run fal-ai/bytedance-upscaler/upscale/video \
  --video_url "<cdn_url>" \
  --target_resolution 4k --enhancement_preset aigc --target_fps 24 --download
```

(`--target_resolution 1080p` is the cheaper social option; 4K is the master
the owner stores in `/opt/data/studio/masters/<film>/`. `--target_fps 24`
matches H3 Max's 24 fps clips — the upscaler defaults to 30 fps and would
otherwise re-time them.)

## The spending rule (MANDATORY — never break this)

Generation costs the owner real money **per successful output** (roughly
US$0.17 per character sheet at high quality, US$0.04 per location or prop at
medium, US$0.16 per keyframe, ~US$0.01 per character for the one-time voice
reference, ~US$0.40 per 5-second clip at 768p, ~US$0.14 per 4K
upscale — check `genmedia pricing <model-id>` for live rates).

- **Never start a paid batch without asking first.** Message the owner on
  Telegram or WhatsApp: *"Shall I generate the [N] shots now? It'll cost
  about US$X."* Wait for a yes. Regenerating a single bad shot from review
  feedback is fine to confirm the same way ("re-roll shot 4? ~US$0.40").
- **Quote the cost, then get an explicit yes — even when the owner says
  "go generate".** "Go" or "yes" to an earlier step is NOT approval for a
  paid batch: state the exact scope and estimated cost and WAIT for an
  explicit yes to that message. Never announce a batch and its cost in the
  same message as launching it — the quote comes first, on its own.
- **Check the balance before a batch.** If you can't confirm credit is
  available (the owner's fal dashboard), warn them to top up — a request with
  no credit simply waits, and you should say why.
- **Report the actual cost when a batch finishes** ("12 clips + 2 upscales:
  ~US$5.20"). Batch work: collect everything that needs generating and run it
  in one go — don't ask twice for the same batch.
- **Only successful outputs are billed** — failed requests and queue time are
  free, so a re-roll costs one clip, not a session.

## Verification (before you tell the owner anything is ready)

1. Every `genmedia run … --download` writes the output file(s) locally; check
   they exist and are non-trivial in size (an image ≥ ~100 KB; a 5-second
   clip several MB).
2. Play/check the clip briefly if possible (ffprobe or similar), confirm it's
   an MP4 with audio, then copy it into the studio folder under its
   descriptive versioned name (the studio-ops skill's naming standard) —
   never a bare `image.png`/`video.mp4`, and never overwrite an existing file.
3. Only then tell the owner what is ready to review. Never claim a
   generation succeeded without the downloaded file on disk.

## Failure → action

| Symptom | Action |
|---|---|
| `FAL_KEY is set` prints nothing | Key not stored — tell the owner to add it on the Keys page (guide Ch4 §4.4). Stop. |
| `401 Unauthorized` / `403` | Key wrong or scope not **API** — ask the owner to check the key on fal.ai. |
| `429` or queue waits long | Platform is busy or out of credit — check the balance; wait and retry, or ask the owner to top up. |
| Model error in the response | Re-read `genmedia run <model> --help`, fix the parameter, retry. One retry, then report. |
| Output file missing/empty after `--download` | The request may have failed — check the JSON output for an error before assuming success. |

## No teardown

There is no pod to stop, no volume to lose, no hourly meter. When a batch is
done, copy everything to the owner's VPS (`shots/…` for review copies,
`/opt/data/studio/masters/<film>/` for approved 4K masters), verify the
copies, and report the cost. Done.
