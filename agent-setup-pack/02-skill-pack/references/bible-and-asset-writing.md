# Bible & Asset Text — How to Write Each Field (Studio)

*Use when: populating the studio's Character Bible & Assets page (`/a/<season>`)
at the words-only stage. This is the full writing structure — what each field
must contain and at what depth. Everything is written fresh from the approved
script and your story notes; never open another project's or another asset's
texts to copy the shape — the structure is defined right here.*

## Characters — the six bible fields (write ALL of them)

Depth target: each field is one solid paragraph (roughly 60–120 words);
emotional range and body language may run a little longer. Every detail must
be visual and usable by an image model — never a feeling without its physical
expression.

### 1. `appearance` — Appearance
What it contains: age · height · build · face (eyes, nose, mouth, jaw) · skin ·
hair (colour, cut, texture) · posture at rest · default expression.
Rules: concrete and ordinary, not idealized. Name actual skin/hair/eye
colours and textures. No story recap — pure looks.
> "A 28-year-old woman, slim, medium height. Black hair in a low ponytail
> with loose strands; warm light-olive skin; sharp dark-brown eyes; guarded,
> tired-but-focused default expression. Ordinary posture, neat and precise."

### 2. `personality` — Personality & Backstory
What it contains: who they are now (temperament, traits) · the backstory that
shaped them (2–4 beats) · what they want · how that shows in behaviour.
Rules: backstory must be specific enough to justify the behaviour; tie it to
how they act in the story.
> "A meticulous data analyst — quiet, exacting, slow to trust. Raised by a
> single father who taught her to verify everything twice, which made her
> good at her job and bad at spontaneity. She wants the truth about the
> missing professor even after the case is officially closed."

### 3. `distinguishing` — Distinguishing Features
What it contains: the 2–4 markers that make the character recognizable in any
frame — scar, tattoo, habitual object, always-worn item, distinctive walk or
posture.
Rules: choose markers that survive across scenes and angles (a small scar
survives; a mood does not).
> "Always wears a plain silver ring on her right thumb. Tucks a pencil behind
> her ear when concentrating. Slight hesitation before she enters a room."

### 4. `wardrobe` — Wardrobe / Style
What it contains: palette (2–4 colours) · silhouette (fit and shape) · texture
(real materials) · signature outfit · any variant changes across the story.
Rules: name materials and fit, not just colours. Wardrobe is identity — it
must be reproducible in the sheet and every scene.
> "Muted palette: charcoal, grey, black. Tailored wool coat over a plain knit
> top, straight dark cotton trousers, flat shoes. Nothing shiny, nothing
> loose — a uniform she never varies."

### 5. `emotional_range` — Emotional Range
What it contains: 4–6 named states (NEUTRAL first), each with the physical
tells — face (eyes, brows, mouth), breathing, hands, posture.
Rules: an emotion word is never enough — always the body. These cards become
the acting notes for every scene.
> "NEUTRAL: relaxed face, flat mouth, slow blink. HAPPY: corner-of-the-mouth
> smile, eyes soften, shoulders drop. CONCERNED: brow furrows, eyes track the
> other person. STRESSED: jaw tightens, fingers tap once, glances at the
> nearest exit."

### 6. `body_language` — Body Language Profile
What it contains: how they carry themselves — stance, gesture range, energy ·
the archetype if one fits · one reusable "prompt injection" sentence an image
or video model can paste into any scene prompt.
> "Low centre of gravity, hands near her tools; coiled, watchful posture;
> scans a room before committing to it. Prompt injection: '[Character]
> stands coiled and watchful, shoulders level, hands at her sides, scanning
> the room before she moves.'"

## Then compose `character_sheet_prompt` — Character Sheet Prompt

Build the image-model prompt for the character reference sheet **from the six
fields above**: appearance supplies the physical description, wardrobe the
clothing, personality/emotional range the default expression and demeanour.
Rules:
- Use the sheet format from the `ai-film-prompt-engineering` skill
  (Scene / Subject / Important details / Use case / Constraints) and the
  3-panel character-sheet layout it defines.
- Do NOT invent details absent from the approved fields, and do NOT paste the
  fields verbatim as prose — translate them into sheet language (panels,
  backdrop, lighting, "no text, no labels").
- The sheet prompt is one asset's generation prompt — it lives in
  `character_sheet_prompt`, never in `prompt` (that field is for locations
  and props only).

## Locations — `description` + `prompt`

**`description`** (what the owner reads and reviews): type of space · key
fixed elements (furniture, architecture, landmarks) · approximate size ·
colour palette · **locked** time of day and lighting.
**`prompt`** (what gets generated): the 4-panel location-sheet language from
`ai-film-prompt-engineering` — wide establishing + alternate wide (~90°) +
corner depth + detail shot; locked lighting/time-of-day across panels; no
people; environment only; add spatial dimensions (e.g. "roughly 6m × 8m,
ceiling 2.8m") so the model reconciles the angles.

> "A modest café interior, roughly 6m × 8m, ceiling 2.8m. Exposed brick,
> warm pendant lights, worn wood tables, a long counter with a pastry case.
> Locked to late afternoon: long window light, dust in the air, warm tungsten
> practicals. No people — environment only."

## Props — `description` + `prompt`

**`description`**: what the object is · materials · scale · condition/wear ·
moving parts or deliberate text.
**`prompt`**: the 4-panel prop-sheet language from `ai-film-prompt-engineering`
— front + side (90°) + back + close-up detail; neutral gray backdrop, studio
lighting, no cast shadows, consistent scale; no hands, no scene context, no
stray text (unless the text is part of the object).

> "A scuffed black flip phone, roughly 10cm, worn matte plastic, one cracked
> corner, faint scratch marks. Screen off — no text."

## Rules

1. **Depth over brevity:** every character field must let an image model draw
   the character without guessing. A one-line field is a draft, not a bible.
2. **All six fields are written in one pass** (words only) and approved
   by the owner before any generation — the sheet prompt is composed at the
   same time but nothing is generated until the owner approves the words AND
   the cost.
3. **Never contradict an approved field** in a later prompt — the bible is the
   source of truth for every image and clip.
