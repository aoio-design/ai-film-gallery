---
name: ai-film-keyframe-authoring
description: "Authoring first-frame keyframe prompts for AI film shots: the frozen moment, @tag references, camera spec, exposure, movement language, timing and per-shot asset loading (fal.ai GPT Image 2 edit)."
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [film, keyframes, prompts, fal-ai, flux, storyboard]
    related_skills: [ai-film-pipeline, ai-film-prompt-engineering, ai-film-cinematography, fal-ai-ops]
---

# Keyframe Authoring (first-frame prompts)

*Use when: writing the image prompt for the FIRST FRAME of a video clip — the
starting picture the video model moves from.*

## The format

Each shot gets ONE first-frame prompt. It must contain:

1. **Character identity** — reference the approved character sheet via @tag
2. **Location** — reference the location image via @tag (+ angle)
3. **The frozen moment** — the instant before the action starts
4. **Camera spec** — framing + lens feel + exposure
5. **Style** — consistent look across the film

## Prompt skeleton

```
[CHARACTER] (@[CHARACTER_TAG]) [frozen pose/position] in/at [LOCATION]
(@[LOCATION_TAG] Angle [X]). [Key prop or detail relevant to the shot].
Camera: [framing — e.g. medium close-up, 50mm], [height/angle], [lighting],
underexposed 1–1.5 stops night (or: daylight/soft). [Style: cinematic, film
grain, moody]. Mouth closed/neutral [if the shot has dialogue].
```

## Worked example

```
Nora (@Nora_Chen) stands at the counter of the cafe (@City_Cafe Angle B),
phone held up in one hand, earbuds in, watching her screen intently — she
hasn't looked up yet. Camera: medium shot, 50mm, eye level, warm interior
light spilling from the counter, soft film grain. Mouth closed/neutral.
```

## Keyframe rules (never break these)

1. **First frame by default — an opening+closing pair ONLY if the selected
   video model requires it.** The keyframe is the starting picture the video
   model moves from. Read the video binding in
   `references/model-registry.yaml` before choosing — H3 Max (default) uses a
   single first frame; a model that needs a first+last pair changes this rule.
   If the user picks an alternative video model, follow the mapping protocol in
   `references/model-routing.md` and re-derive the frame count/size from it.
2. If the image already shows the action, the video model gets confused and
   "un-does" it. The moment BEFORE the action — not the action itself. The
   action belongs in the video prompt, not the image.
3. **Mouth closed/neutral for dialogue shots** — the video model lip-syncs
   from the audio it generates; an open mouth in the reference fights it.
4. **Same @tags everywhere = same face everywhere.** Never describe the
   character's face from scratch in a keyframe prompt — always anchor it to
   the approved sheet.

## Camera language (usable in any image or video prompt)

**Framing:** wide / medium / medium close-up / close-up / extreme close-up /
over-shoulder / insert / POV.

**Lens feel:** 32mm (wide, slightly environmental), 50mm (natural, default),
85mm (tight singles), 85mm macro (props, details).

**Movement (for the VIDEO prompt, not the keyframe):**
- `breath-like handheld float` — default for dramatic scenes
- `slow push-in` — reveals, emotional moments
- `subtle handheld bob` — walking, action
- `static tripod shot` — establishing shots
- `slow pan` — scanning a space
- `handheld float settling` — transition from action to stillness

**Exposure guide:**
- Night exterior: underexposed 1.5 stops
- Interior, moonlight only: underexposed 1.5 stops
- Interior, warm lamp: underexposed 0.5 stops
- Day-lit exterior: underexposed 0.5 stops "for mood" — never apply night
  defaults to day scenes

## Timing (H3 Max clips: 5–15 seconds — plan 5–6s)

H3 Max's minimum clip length is **5 seconds** (maximum 15) — never plan a
shorter clip.

- 5s — quick reaction, cutaway, insert, dialogue line
- 6s — standard action, character moment
- 6–10s — establishing shot, reveal, dramatic hold

Durations are earned, not assigned to fill time. Dialogue pacing ≈ 3–4 words
per second: a 35–40 word paragraph is ~9–10s — a long single clip. Prefer
splitting it into a multi-shot sequence (speaker close-up → reaction/insert
cutaway → speaker finish) and let the line carry across the cutaways.

## Per-shot asset loading (fal.ai — GPT Image 2 edit)

`openai/gpt-image-2/edit` accepts **up to 16 reference images** (`image_urls`)
in one request. The composition prompt describes how the references combine —
put the character from one reference into the setting from another. The
typical keyframe call uploads two: the character sheet and the location image.

Render every keyframe at a **fixed 1920×1080 (16:9)**, quality high — the frame
is supersampled above H3 Max's native 1344×768 canvas so the video model
downsamples clean detail (exact command: see the `fal-ai-ops` skill).

Verify the generated image actually contains the right character and place
before generating video — a wrong keyframe wastes a paid video clip.

## Reference

- Prompt templates pack (Downloads page): `keyframe-prompt-format.md`,
  `character-sheet-prompt.md`, `the-7-key-rules.md`
- Generation commands: see the `fal-ai-ops` skill
