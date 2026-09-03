---
name: ai-film-prompt-engineering
description: "Prompt craft for AI film production on fal.ai: GPT Image 2 image prompts (structured, 3-panel landscape character sheets, @tag references), MiniMax H3 Max video prompts (motion-only, dialogue in quotes, soundscape), and the rules that keep characters consistent."
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [film, prompts, fal-ai, gpt-image-2, minimax, prompting]
    related_skills: [ai-film-pipeline, ai-film-keyframe-authoring, ai-film-cinematography, fal-ai-ops]
---

# AI Film Prompt Engineering (fal.ai stack)

*Use when: writing any generation prompt — image (GPT Image 2) or video (MiniMax H3
Max). The rules below are the ones that actually move quality.*

## The non-negotiable rules

1. **Never put metadata in a prompt.** No "key prop — appears in Ep 4-6", no
   shot numbers, no production notes. Pure visual description only.
2. **Character consistency comes from references, not words.** Anchor every
   image to the approved character sheet with @tags. Never re-describe a
   face from scratch.
3. **Physical cues, not emotions.** "jaw tightens", "eyes drop to the floor",
   "hands clench" work. The word "sad" or "confused" alone doesn't.
4. **No text, no watermark, no labels** — append to image prompts when text
   bleeding is a risk.

## Image prompts (GPT Image 2 / GPT Image 2 edit)

GPT Image 2 follows a **structured prompt template** — it reasons about the
prompt and adheres strongly to long, multi-part instructions. Use this exact
shape (the model's own documented format):

```
Scene: [where this happens, time of day, background, environment]
Subject: [who or what is the main focus]
Important details: [materials, clothing, texture, lighting, camera angle, lens feel, composition, mood]
Use case: [editorial photo / product mockup / concept frame]
Constraints: [no watermark / no logos / no extra text / preserve face / preserve layout]
```

### Asset templates (full writing structure + sheet formats: `references/bible-and-asset-writing.md`)

- **Character sheet = 3-panel, landscape (1536×1024), ONE face.** Plain neutral
  gray (#e0e0e0) backdrop; equal-width panels — face+shoulders close-up,
  full-body front (A-pose), full-body back (same pose as center). Photorealism
  vocabulary (camera/lens/lighting/skin-texture/material language beats vague
  "quality" adjectives): full-frame DSLR 85mm f/2.8, soft three-point studio
  light, visible skin pores, named real materials. Avoid
  "hyperrealistic / ultra realistic / 8K / flawless". No text/labels/watermarks,
  no inconsistent proportions, no background props.
- **Location / setting:** **4-panel sheet, 16:9 landscape (1536×864)**, locked
  lighting/time-of-day. Wide establishing (top-left, largest) + alternate wide
  ~90° (top-right) + corner depth (bottom-left) + detail shot of a key feature
  (bottom-right). No people, environment only, consistent lighting across panels.
  Add spatial dimensions (e.g. "a room roughly 4m × 6m") to help the model
  reconcile the angles.
- **Prop:** **4-panel grid, neutral gray (#e0e0e0)**, studio lighting, no cast
  shadows, consistent scale. Front + side (90°) + back + close-up detail
  (texture/material/functional details). No hands, no scene context, no text labels.

### Keyframes (`openai/gpt-image-2/edit`)

Upload the reference images as `image_urls`, describe the composition ("the
woman from the first reference image, in the cafe from the second reference
image"); optional mask for surgical edits. First frames are generated at
**high quality** for best clips.

> **LEGACY — FLUX prompting (pre-GPT Image 2):** natural-language Subject +
> Action + Style + Context, JSON structured prompts, `@image1`–`@image9`
> reference tags, HEX colors. Official rules in `flux-prompting`. Do not use
> FLUX structure for GPT Image 2 prompts.

## Video prompts (MiniMax H3 Max)

The video prompt describes **motion only** — the keyframe image already sets
the scene, look and lighting. Structure:

```
[What moves / the action] + [camera move] + [dialogue in quotes with delivery
tone] + [soundscape: room tone, ambient cues]
```

**Dialogue** goes in quotes with a tone clause — the model speaks it and
syncs the lips:

```
Slow push-in over her shoulder. NOVA says: "It's everything. The whole
ledger." — tired, flat, quiet. Quiet cafe ambience, distant city traffic.
```

**One speaker per clip, lines ≤ 5 seconds.** Two voices in one clip = muddy
mouths. Break dialogue into shot/reverse-shot close-ups.

**Soundscape:** always state the audio environment, even for "silent" scenes
— the model generates a soundtrack otherwise. Say what the room sounds like.

**Keep it simple:** the engine is excellent at subtle moves and bad at stunt
choreography. "Slow push-in" works. A dolly zoom + orbit + chair spin will
look broken.

## Camera language (shared by image and video prompts)

- Framing: wide / medium / medium close-up / close-up / extreme close-up /
  over-shoulder / insert / POV
- Lens: 32mm (environmental), 50mm (natural), 85mm (tight singles)
- Movement: breath-like handheld float (dramatic default), slow push-in
  (reveals), subtle handheld bob (walking), static tripod (establishing),
  slow pan (scanning), handheld float settling (action → stillness)

## The seven key rules (print these)

1. One speaker per clip, dialogue ≤ 5 seconds
2. Video prompts describe motion ONLY
3. Dialogue in quotes with a delivery tone
4. Generate at 768p, upscale later
5. Character consistency via reference images + @tags
6. Physical cues, not emotions
7. Clips 3–6 seconds

See also: `ai-film-keyframe-authoring` (first-frame prompts), `fal-ai-ops`
(generation commands), and the Prompt & Template Pack.