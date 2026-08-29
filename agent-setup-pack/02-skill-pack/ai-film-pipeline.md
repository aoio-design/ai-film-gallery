---
name: ai-film-pipeline
description: "Master pipeline skill for producing AI short films and micro-dramas with the owner's studio: idea → script → shots → images (FLUX on fal.ai) → clips (MiniMax H3 Max) → gallery review → 4K masters (bytedance upscaler)."
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [film, video, production, pipeline, fal-ai, flux, minimax, automation]
    related_skills: [ai-film-scriptwriting, ai-film-cinematography, ai-film-keyframe-authoring, ai-film-prompt-engineering, studio-ops, fal-ai-ops]
---

# AI Film Production Pipeline

## Overview

The owner's end-to-end pipeline for AI short films and micro-dramas. All
generation runs through their **fal.ai** account (see `fal-ai-ops` for the
models, commands and spending rule); all review happens in their **studio**
gallery (see `studio-ops`). Post-production (assembly, titles, music) is done
by the owner in their video editor.

## The pipeline (follow this order)

```
1. IDEA        →  talk it through with the owner; nothing is created yet
2. SCRIPT      →  write it, break it into 3–6 second shots (see
                  ai-film-scriptwriting)
3. WORDS OK    →  owner approves script + character bible in the studio
                  (no generation, no cost)
4. IMAGES      →  reference images on fal.ai: character sheets and
                  locations (FLUX 1.1 pro ultra, $0.06 each)
5. KEYFRAMES   →  first frame per shot (FLUX 2 pro edit: character sheet
                  + location → the frozen moment, mouth closed/neutral on
                  dialogue shots)
6. CLIPS       →  one clip per shot (MiniMax H3 Max: keyframe + motion
                  prompt; dialogue in quotes in the prompt — the model
                  speaks it and syncs the lips)
7. REVIEW      →  owner reviews in the studio; feedback on a card =
                  regenerate that one shot; "approved" = done
8. MASTER      →  approved clip → 4K upscale (bytedance upscaler, aigc
                  preset) → /opt/data/studio/masters/<film>/<shot_id>.mp4
```

## Rules that never bend

- **Words before media.** Never generate before the script, shot plan and
  character bible are approved. Rewriting is free; regenerating costs money.
- **Spending rule.** Every successful generation bills the owner (~US$0.06
  per image, ~US$0.40 per 5-second clip, ~US$0.14 per 4K upscale). Never
  start a paid batch without asking on Telegram/WhatsApp ("shall I generate
  the N shots now? it'll cost about US$X"), check the balance first, report
  the actual cost when done. See `fal-ai-ops`.
- **One speaker per clip, lines ≤ 5 seconds.** The model syncs one mouth to
  one voice per clip. Break dialogue into shot/reverse-shot close-ups.
- **Consistency comes from reference images.** Anchor every shot with the
  same character sheet and @tags — the model has no memory between clips.
- **Motion-only video prompts.** The keyframe sets the scene; the prompt
  only describes what moves and the camera.
- **Verify before claiming success.** Every generated file must exist on
  disk with a sensible size and be copied into the right studio folder
  (`image.png`, `video.mp4` in the shot folder; masters in `masters/`).

## Where things live

- Project words: `/opt/data/studio/` (projects.json, shot cards, script pane)
- Reference media: `/opt/data/studio/assets/<season>/<asset>/`
- Review copies: `/opt/data/studio/shots/<film>/<shot>/` (`image.png`, `video.mp4`)
- Masters: `/opt/data/studio/masters/<film>/<shot_id>.mp4`

## Done?

Tell the owner what is ready to review, what each batch cost, and — when a
shot is approved and upscaled — the exact master path. Then back to step 1
for the next episode: same characters, same voices, same rules.
