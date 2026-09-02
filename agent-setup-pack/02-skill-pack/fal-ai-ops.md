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
export PATH="$HOME/.genmedia:$PATH"
```

Verify the connection: `genmedia models minimax --limit 3` — a list with no
error means the key works. To see any model's exact flags:
`genmedia run <model-id> --help`.

## The four models (guide stack, August 2026)

| Job | Model | Default settings |
|---|---|---|
| Character reference sheets | `openai/gpt-image-2` | `--image_size '{"width":1536,"height":1024}'`, `--quality high`, `--output_format png` |
| Location & prop reference images | `openai/gpt-image-2` | `--image_size '{"width":1536,"height":864}'`, `--quality medium`, `--output_format png` |
| First-frame edits (keyframes) | `openai/gpt-image-2/edit` | `--image_urls <refs>`, `--image_size '{"width":1920,"height":1080}'`, `--quality high` |
| Video clips (with sound) | `minimax/h3-max/image-to-video` | `--duration 5`, `--resolution 768P`, `--prompt_expansion_mode balanced` |
| Upscaler (masters) | `fal-ai/bytedance-upscaler/upscale/video` | `--target_resolution 4k`, `--enhancement_preset aigc`, `--target_fps 24` |

### Reference image — text to image (GPT Image 2)

```bash
genmedia run openai/gpt-image-2 \
  --prompt "<structured prompt — see templates below>" \
  --image_size '{"width":1536,"height":1024}' --quality high --output_format png --download
```

**Structured prompt format:** `Scene:` / `Subject:` / `Important details:` / `Use case:` / `Constraints:`
**Character sheet (three-panel, landscape, ONE face):** plain neutral gray (#e0e0e0) backdrop, equal-width 3-panel horizontal sheet: Panel 1 face+shoulders close-up (front, neutral), Panel 2 full-body front (A-pose), Panel 3 full-body back (same pose as center); landscape 1536x1024. Use photographic vocabulary (full-frame DSLR 85mm f/2.8, soft three-point studio light, visible skin texture/pores, individual hair strands, real materials). Describe the character as realistic and unpolished — "avoid conventionally polished or symmetrical features". Do NOT include text labels, watermarks, inconsistent proportions, or background props.
**Location:** **4-panel sheet, 16:9 landscape** — wide establishing + alternate wide (~90°) + corner depth + detail shot; locked lighting/time-of-day, no people, environment only. (Full template in character-set-design skill.)
**Prop:** **4-panel grid, neutral gray (#e0e0e0)** — front + side (90°) + back + close-up detail; studio lighting, no cast shadows, consistent scale, no text labels.

### First-frame edit (keyframes) — GPT Image 2 edit

Upload the owner's reference images first, then reference them by URL:

```bash
genmedia upload /opt/data/studio/assets/<season>/<asset>/<file>.png
# → prints a cdn_url like https://v3b.fal.media/files/b/...
genmedia run openai/gpt-image-2/edit \
  --prompt "<composition prompt: put the subject from image 1 in the setting from image 2…>" \
  --image_urls "<cdn_url_1>,<cdn_url_2>" --image_size '{"width":1920,"height":1080}' --quality high --output_format png --download
```

(Render keyframes at a **fixed 1920×1080 (16:9)** — supersampled above H3 Max's 768p-class canvas (1344×768) so the model downsamples clean detail. `image_urls` accepts up to 16 refs. Optional `mask_url`: white = editable, black = preserved.)

### Video clip (first frame → clip with sound)

```bash
genmedia upload /opt/data/studio/shots/<film>/<shot>/image.png
genmedia run minimax/h3-max/image-to-video \
  --prompt "<motion + camera + dialogue-in-quotes + soundscape>" \
  --image_url "<cdn_url>" \
  --duration 5 --resolution 768P --prompt_expansion_mode balanced --download
```

Feed the 1920×1080 keyframe from the edit stage as-is — H3 Max downsamples to its native 768p-class output (1344×768 @ 24 fps).

Dialogue goes inside the prompt in quotes with a delivery tone
(`NOVA says: "It's everything. The whole ledger." — tired, flat, quiet`).
One speaker per clip, lines ≤ 5 seconds. The clip comes back with the voice
and room sound baked in — there are no separate audio files.

### 4K master (approved clip → upscaled)

```bash
genmedia upload /opt/data/studio/shots/<film>/<shot>/video.mp4
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
medium, US$0.16 per keyframe, ~US$0.40 per 5-second clip at 768p, ~US$0.14 per 4K
upscale — check `genmedia pricing <model-id>` for live rates).

- **Never start a paid batch without asking first.** Message the owner on
  Telegram or WhatsApp: *"Shall I generate the [N] shots now? It'll cost
  about US$X."* Wait for a yes. Regenerating a single bad shot from review
  feedback is fine to confirm the same way ("re-roll shot 4? ~US$0.40").
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
   an MP4 with audio, then copy it into the studio folder with the exact
   filename the gallery expects (`image.png`, `video.mp4`, …).
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
