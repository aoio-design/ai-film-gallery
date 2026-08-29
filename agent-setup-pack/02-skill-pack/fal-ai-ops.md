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
| Reference images (character sheets, sets, props) | `fal-ai/flux-pro/v1.1-ultra` | `--aspect_ratio 16:9`, `--output_format png` |
| First-frame edits (keyframes) | `fal-ai/flux-2-pro/edit` | up to 9 reference images; `@tag` works natively in the prompt |
| Video clips (with sound) | `minimax/h3-max/image-to-video` | `--duration 5`, `--resolution 768P`, `--prompt_expansion_mode balanced` |
| Upscaler (masters) | `fal-ai/bytedance-upscaler/upscale/video` | `--target_resolution 4k`, `--enhancement_preset aigc` |

### Reference image (text-to-image)

```bash
genmedia run fal-ai/flux-pro/v1.1-ultra \
  --prompt "<full image prompt with @tags>" \
  --aspect_ratio 16:9 --output_format png --download
```

### First-frame edit (compose character + location into a keyframe)

Upload the owner's reference images first, then reference them by URL:

```bash
genmedia upload /opt/data/studio/assets/<season>/<asset>/<file>.png
# → prints a cdn_url like https://v3b.fal.media/files/b/...
genmedia run fal-ai/flux-2-pro/edit \
  --prompt "<keyframe prompt, e.g. 'the lead (@image1) stands at the counter
            (@image2 Angle B)…' or 'the person from image 1 in the setting
            from image 2'>" \
  --image_urls "<cdn_url_1>,<cdn_url_2>" --output_format png --download
```

(@image1, @image2 … refer to the images in the order listed in `--image_urls`.)

### Video clip (first frame → clip with sound)

```bash
genmedia upload /opt/data/studio/shots/<film>/<shot>/image.png
genmedia run minimax/h3-max/image-to-video \
  --prompt "<motion + camera + dialogue-in-quotes + soundscape>" \
  --image_url "<cdn_url>" \
  --duration 5 --resolution 768P --prompt_expansion_mode balanced --download
```

Dialogue goes inside the prompt in quotes with a delivery tone
(`NOVA says: "It's everything. The whole ledger." — tired, flat, quiet`).
One speaker per clip, lines ≤ 5 seconds. The clip comes back with the voice
and room sound baked in — there are no separate audio files.

### 4K master (approved clip → upscaled)

```bash
genmedia upload /opt/data/studio/shots/<film>/<shot>/video.mp4
genmedia run fal-ai/bytedance-upscaler/upscale/video \
  --video_url "<cdn_url>" \
  --target_resolution 4k --enhancement_preset aigc --download
```

(`--target_resolution 1080p` is the cheaper social option; 4K is the master
the owner stores in `/opt/data/studio/masters/<film>/`.)

## The spending rule (MANDATORY — never break this)

Generation costs the owner real money **per successful output** (roughly
US$0.06 per image, ~US$0.40 per 5-second clip at 768p, ~US$0.14 per 4K
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
