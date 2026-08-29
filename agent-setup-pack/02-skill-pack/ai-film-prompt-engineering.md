---
name: ai-film-prompt-engineering
description: "Prompt craft for AI film production on fal.ai: FLUX image prompts (JSON-structured, HEX colors, @tag references), MiniMax H3 Max video prompts (motion-only, dialogue in quotes, soundscape), and the rules that keep characters consistent."
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [film, prompts, fal-ai, flux, minimax, prompting]
    related_skills: [ai-film-pipeline, ai-film-keyframe-authoring, ai-film-cinematography, fal-ai-ops]
---

# AI Film Prompt Engineering (fal.ai stack)

*Use when: writing any generation prompt — image (FLUX) or video (MiniMax H3
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

## Image prompts (FLUX 1.1 pro ultra / FLUX 2 pro edit)

FLUX models follow **long, detailed, natural-language instructions** — 80–250
words of structured, camera-style description beats tag soup every time.

**Formula:**

```
[Shot type & subject] + [Age & appearance] + [Clothing] + [Environment] +
[Lighting & mood] + [Style/medium] + [Camera angle & lens] + [Constraints]
```

**JSON-structured prompts** give the most control for complex shots (FLUX
supports them natively):

```json
{
  "scene": "Overall setting description",
  "subjects": [
    {"type": "Subject category", "description": "Physical attributes and details", "pose": "Action or stance", "position": "foreground/midground/background"}
  ],
  "style": "Artistic rendering approach",
  "color_palette": ["color1", "color2", "color3"],
  "lighting": "Lighting conditions and direction",
  "mood": "Emotional atmosphere",
  "composition": "rule of thirds/centered/dynamic diagonal",
  "camera": {"angle": "eye level/low angle/high angle", "distance": "close-up/medium shot/wide shot", "lens": "35mm/50mm/85mm"}
}
```

**HEX color control** — exact colors with `color #HEX` or `hex #HEX`:
"a wall painted in color #2ECC71". Pair with a swatch image for accuracy.

**@tag references** — FLUX 2 pro edit understands `@image1`–`@image9` for the
uploaded images: "the person from @image1 wearing the outfit from @image2".

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
(generation commands), and the Prompt & Template Pack on the Downloads page.
