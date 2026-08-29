---
name: ai-film-keyframe-authoring
description: "Authoring first-frame keyframe prompts for AI film shots: the frozen moment, @tag references, camera spec, exposure, movement language, timing and per-shot asset loading (fal.ai FLUX 2 pro edit)."
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

1. **First frame ONLY** — never a first+last pair. The video model moves
   forward from this one image.
2. **The moment BEFORE the action** — if the image already shows the action,
   the video model gets confused and "un-does" it. The action belongs in the
   video prompt, not the image.
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

## Timing (3–6 second shots)

- 3s — quick reaction, cutaway, insert
- 4s — standard action, medium shot
- 5s — dialogue line, character moment
- 6s — establishing shot, reveal, dramatic hold

Durations are earned, not assigned to fill time. Dialogue pacing ≈ 3–4 words
per second: a 35–40 word paragraph is ~9–10s — too long for one clip. Split
it into a multi-shot sequence (speaker close-up → reaction/insert cutaway →
speaker finish) and let the line carry across the cutaways.

## Per-shot asset loading (fal.ai — FLUX 2 pro edit)

FLUX 2 pro edit accepts **up to 9 reference images** in one request. The
`@image1`–`@image9` tags in the prompt refer to the images **in the order you
upload them** for that run — there is no fixed global map. The typical
keyframe call uploads two: the character sheet and the location image.

```
SHOT N — [description]
  Image 1: [character sheet file]     → referenced as @image1
  Image 2: [location image file]      → referenced as @image2
  Prompt:  "[CHARACTER] from @image1 in the setting from @image2, [frozen
           moment]…" (or use the @TAG names directly — the model understands
           both)
```

Write the loading spec per shot before queueing, then verify the generated
image actually contains the right character and place before generating video
— a wrong keyframe wastes a paid video clip.

## Reference

- Prompt templates pack (Downloads page): `keyframe-prompt-format.md`,
  `character-sheet-prompt.md`, `the-7-key-rules.md`
- Generation commands: see the `fal-ai-ops` skill
