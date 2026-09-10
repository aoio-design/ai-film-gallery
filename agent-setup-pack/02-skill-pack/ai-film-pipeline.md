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

> **Which model runs which stage is decided by the model registry, not by the
> prose below.** Read `references/model-registry.yaml` + `references/model-routing.md`
> before any generation. The stack below is the current global default; if the
> owner selects an alternative for a step (shot / project / global), follow the
> mapping protocol and append, don't override.

```
1. IDEA        →  talk it through with the owner; nothing is created yet
2. SCRIPT      →  write it, break it into 5–15 second shots — H3 Max's floor is 5s (see
                  ai-film-scriptwriting)
3. WORDS OK    →  two gates, in order: owner approves the SCRIPT first, then
                  you write the character bible + asset text and they approve
                  that (words only — nothing is generated yet)
4. IMAGES      →  reference images on fal.ai: character sheets + locations/props
                  (openai/gpt-image-2; characters high ~$0.17, locations/props
                  medium ~$0.04)
5. KEYFRAMES   →  first frame per shot (openai/gpt-image-2/edit: upload
                  character sheet + location refs, compose the frozen moment)
6. CLIPS       →  one clip per shot (MiniMax H3 Max: keyframe + motion
                  prompt; dialogue in quotes in the prompt — the model
                  speaks it and syncs the lips)
7. REVIEW      →  owner reviews in the studio; feedback on a card =
                  regenerate that one shot; "approved" = done
8. MASTER      →  approved clip → 4K upscale (bytedance upscaler, aigc
                  preset) → /opt/data/studio/masters/<film>/<shot_id>.mp4
```

## Rules that never bend

- **CLARIFY FIRST — ambiguous instruction = ask, then wait.** If any instruction is ambiguous (chat, gallery review loop, anywhere), ASK the user what they mean and WAIT before taking ANY action. Never guess, never pick a "reasonable default". Ambiguity includes: which assets/steps are meant, whether a review message means "approved, go ahead", which phase "generate" refers to, or anything readable more than one way. A clarifying question is correct action; acting on a guess is not.
- **Words before media.** Never generate before the script, shot plan and
  character bible are approved.
- **Two approval gates, in order.** (1) After drafting a script, hand it back
  to the owner for review and WAIT — never offer or start keyframe,
  video-prompt or clip work in the same breath. (2) Only after the script is
  approved, write the character bible + asset text and populate the studio's
  assets page (words only — every character gets all six bible fields
  plus the Character Sheet Prompt composed from them; schema in studio-ops),
  then hand THAT back for approval too.
  Generation starts only after both gates pass. Skipping ahead wastes review
  time and spends money early.
- **Spending rule.** Every successful generation bills the owner (about US$0.17
  per character sheet, US$0.04 per location or prop, US$0.16 per keyframe,
  ~US$0.40 per 5-second clip at 768p, ~US$0.14 per 4K upscale). Never
  start a paid batch without asking on Telegram/WhatsApp ("shall I generate
  the N shots now? it'll cost about US$X"), check the balance first, report
  the actual cost when done. See `fal-ai-ops`.
- **Quote first, then get an explicit yes — even when the owner says "go
  generate".** "Go" or "yes" to an earlier step is NOT approval for a paid
  batch: state the exact scope and the estimated cost and WAIT for an
  explicit yes to THAT message. Never announce a batch and its cost in the
  same message as launching it — the quote comes first, on its own.
- **One speaker per clip, lines ≤ 5 seconds.** The model syncs one mouth to
  one voice per clip. Break dialogue into shot/reverse-shot close-ups.
- **Consistency comes from reference images.** Anchor every shot with the
  same character sheet and @tags — the model has no memory between clips.
- **Motion-only video prompts.** The keyframe sets the scene; the prompt
  only describes what moves and the camera.
- **Verify before claiming success.** Every generated file must exist on
  disk with a sensible size and be copied into the right studio folder under
  its descriptive versioned name (the studio-ops skill's naming standard) —
  never a bare `image.png`/`video.mp4`, and never overwrite an existing
  file. Masters go in `masters/`.
- **The card's prompt field is the reviewed words; the sent prompt lives in a
  provenance map.** A shot's `image_prompt`/`video_prompt` in its
  `metadata.json` are what the owner reviewed and what the NEXT run must send
  verbatim — generators READ them, never write them. After each successful
  generation, record the exact text actually sent under
  `metadata["prompts"][<take filename>] = {"prompt": …, "model": …,
  "sent_at": …}`. That provenance map is a BACKEND-ONLY audit record: never
  render it in the Studio UI. Draft-authoring scripts must refuse to touch any
  card that already holds media (drafting happens only BEFORE generation).
  Two writers fighting over one field is how a review surface ends up
  displaying text that never ran — one field, one meaning, immutable
  send-log. (This is the same contract the owner's own studio follows.)

## Where things live

- Project words: `/opt/data/studio/` (projects.json, shot cards, script pane)
- Reference media: `/opt/data/studio/assets/<season>/<asset>/`
- Review copies: `/opt/data/studio/shots/<film>/<shot>/` (versioned media files)
- Masters: `/opt/data/studio/masters/<film>/<shot_id>.mp4`

## Done?

Tell the owner what is ready to review, what each batch cost, and — when a
shot is approved and upscaled — the exact master path. Then back to step 1
for the next episode: same characters, same voices, same rules.
