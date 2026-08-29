---
name: ai-film-cinematography
description: "Cinematography knowledge for AI film production. Covers camera shots, angles, movements, lens choices, composition, lighting design, visual style archetypes (16 archetypes across sci-fi, comedy, dramedy, and romance), and a 76-entry Film & Series Visual Library (scene-prompt formulas for top films and series across genres) — all translated into effective AI image/video prompts."
version: 1.13.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cinematography, camera, lighting, composition, shot-list, ai-film]
    related_skills: [ai-film-pipeline, ai-film-prompt-engineering, ai-film-scriptwriting]
---

# AI Film Cinematography

## Overview

Cinematography decisions translated for AI generation. When directing FLUX (image) and MiniMax H3 Max (video) prompts, you can't "set up a camera" — but you CAN encode every cinematography choice into the prompt. This skill maps filmmaking craft to AI-prompt language.

## When to Use

- The user needs shot-by-shot camera direction for a scene
- Writing first-frame prompts for video clips
- Determining lighting design for a scene
- Composing scenes within Flux's strengths (and avoiding its weaknesses)
- Any visual direction task in the pipeline

## Camera Shot Sizes

| Shot | What It Shows | Best For | Prompt Keyword |
|------|--------------|----------|----------------|
| **Extreme Wide Shot (EWS)** | Character is tiny in landscape | Establishing location | "extreme wide shot, tiny figure against vast landscape" |
| **Wide Shot (WS)** | Full body + environment | Action, entrance | "wide shot, full body visible" |
| **Medium Wide Shot (MWS)** | Knees up | Dialogue with context | "medium wide shot, cowboy shot" |
| **Medium Shot (MS)** | Waist up | Standard dialogue | "medium shot" |
| **Medium Closeup (MCU)** | Chest up | Emotional dialogue | "medium closeup, chest up" |
| **Closeup (CU)** | Face fills frame | Emotion, reaction | "closeup, face filling frame" |
| **Extreme Closeup (ECU)** | Eyes, hands, detail | Dramatic emphasis | "extreme closeup of eyes/hands" |

### AI-Reality: Flux is best at Medium to Medium Closeup
FLUX produces the most photorealistic faces at **MCU to MS** range. Extreme closeups can look waxy. Wide shots often have garbled background details. Plan your "hero shots" (the frames you'll use as keyframes) in the MCU-MS range.

## Camera Angles

| Angle | Description | Prompt Phrase | Emotional Effect |
|-------|-------------|---------------|------------------|
| **Eye level** | Neutral, 5ft height | "eye level shot" | Normal, documentary |
| **Low angle** | Camera looks up | "low angle shot, camera looking up" | Power, menace, grandeur |
| **High angle** | Camera looks down | "high angle shot, bird's eye view" | Vulnerability, overview |
| **Dutch angle** | Tilted horizon | "dutch angle, tilted frame" | Unease, disorientation |
| **Over-the-shoulder (OTS)** | Behind character | "over the shoulder shot" | Conversation, perspective |
| **POV** | Character's eyes | "first person point of view" | Immersion, identification |
| **God's eye** | Directly overhead | "top down view, aerial shot" | Omniscience, fate |

## Camera Movement (For Video Prompts)

Camera movement in AI video models is controlled via **prompt description**, not physical camera rigging. Different models handle this differently:

| Model | Camera Control Method | Reliability |
|-------|----------------------|-------------|
| **Wan 2.2 14B** | ✅ Prompt-only — best-in-class motion understanding | High — Wan reads camera language well |
| **MiniMax H3 Max** | Prompt only | High — plain-language camera moves work natively |
| **HunyuanVideo** | Prompt-only | Medium |

> **For our pipeline (MiniMax H3 Max):** Camera movement is handled by prompt language only. "Camera slowly pushes in" produces a dolly-in effect; plain-language camera moves work natively. No add-ons needed.

### Movement Reference Table

| Movement | Prompt phrase |
|----------|----------------------|-----------------------|------------------|
| **Dolly in** | "camera slowly pushes in toward the subject" | "camera slowly pushes in" | ✅ Via Dolly Out reversed |
| **Dolly out** | "camera slowly pulls back from the subject" | "camera slowly pulls back" | ✅ `Dolly-Out` |
| **Truck (track)** | "camera tracks left, following the character" | "camera tracks left to right" | ✅ `Dolly-Right` |
| **Pan** | "camera pans right, revealing the room" | "camera pans right" | ✅ `Pan-Right` |
| **Crane up** | "camera rises up smoothly" | "camera rises up" | ✅ `Jib-Up` |
| **Crane down** | "camera descends to eye level" | "camera descends" | ✅ `Jib-Down` |
| **Static** | "static camera, locked off" | "static camera, locked off" | ✅ `Static` |
| **Handheld** | "handheld camera, slight natural shake" | "handheld camera, slight shake" | — Use prompt only |
| **Steadicam** | "smooth floating steadicam shot" | "smooth floating camera movement" | — Use prompt only |

### Camera Prompting Tips

1. **Use full sentences, not tags** — "the camera slowly dollies in on the character's face as she realizes the truth" works better than "dolly in, closeup, reveal"
2. **Pair camera movement with subject action** — Don't just describe the camera; describe what the camera sees changing
3. **Motion arcs work across the full clip** — The camera move happens over the entire video duration, not between the first and last frame
4. **Weight matters** — Use "slowly" and "smoothly" for intentional-feeling camera moves; the model follows the adverb

### First → Last Frame Strategy

The first and last frame images should differ ONLY in the intended change. Background, lighting, character position (when not moving) must match:

```
WEAK: First frame = wide shot of room, Last frame = closeup of face
       → Morphing artifacts, disorienting

STRONG: First frame = character sitting at desk looking down
        Last frame = character sitting at desk looking up, surprised
         → Natural head movement, believable transition
```

### Tip: Describe the Motion Arc in the Prompt

Instead of just "dolly in," describe the full motion:

```
WEAK: "camera pushes in"
STRONG: "camera slowly dollies in on the character's face,
         background slightly blurring, soft focus effect,
         warm light intensifying as we move closer"
```

## Composition Rules for AI Prompts

| Rule | How to Encode in Prompt | Effect |
|------|------------------------|--------|
| **Rule of thirds** | "off-center composition, subject in left third" | Dynamic, professional |
| **Leading lines** | "leading lines drawing eye to subject, corridor perspective" | Depth, direction |
| **Framing** | "framed by doorway, vignette of shadows around edges" | Depth, focus |
| **Negative space** | "vast empty space on the right, subject small on left" | Isolation, scale |
| **Symmetry** | "perfectly symmetrical composition" | Grandeur, order |
| **Depth of field** | "shallow depth of field, background bokeh" | Focus on subject |
| **Shallow focus** | "only subject in focus, foreground and background blurry" | Intimacy |
| **Deep focus** | "everything in focus from foreground to background" | Clarity, documentary |

## Lens Characteristics

| Lens | Look | Prompt Phrase | Best For |
|------|------|---------------|----------|
| **35mm** | Standard, natural | "35mm lens" | Dialogue, natural scenes |
| **50mm** | "Nifty fifty", human eye | "50mm lens, standard focal length" | Portraits, intimacy |
| **85mm** | Compression, flattering | "85mm portrait lens" | Closeups, beauty shots |
| **24mm** | Wide, distorted edges | "24mm wide angle lens" | Landscapes, interiors |
| **14mm** | Ultra-wide, dramatic | "ultra wide angle lens, 14mm, dramatic perspective" | Establishing shots |
| **200mm** | Telephoto, compression | "200mm telephoto lens, compressed background" | Surveillance, isolation |
| **Anamorphic** | Cinematic flares, 2.35:1 | "anamorphic lens, blue lens flares" | Cinematic, sci-fi |
| **Fisheye** | Extreme distortion | "fisheye lens, curved distortion" | Unreality, POV |

## Lighting Design

### Lighting Styles

| Style | Prompt Description | Mood |
|-------|-------------------|------|
| **Three-point** | "key light from right, fill light left, rim light from behind" | Standard, professional |
| **Rembrandt** | "Rembrandt lighting, triangle of light on cheek, single key light" | Dramatic, classic |
| **Chiaroscuro** | "chiaroscuro lighting, deep shadows, strong contrast" | Noir, mystery |
| **High key** | "high key lighting, bright even illumination, minimal shadows" | Happy, commercial |
| **Low key** | "low key lighting, mostly shadows, single small light source" | Suspense, noir |
| **Silhouette** | "backlit silhouette, rim light, subject dark" | Mystery, drama |
| **Practical light** | "lit only by table lamp, warm 2700K, shadows reaching up" | Cozy, intimate |
| **Neon** | "neon lighting, magenta and cyan, pools of colored light" | Cyberpunk, stylized |
| **Golden hour** | "golden hour light, warm orange, long soft shadows" | Romantic, nostalgic |
| **Moonlight** | "moonlit scene, cool blue light, pale shadows" | Night, mystery |

### Color Temperature in Prompts

| Temperature | Kelvin | Prompt Words |
|-------------|--------|-------------|
| Warm | 2700-3500K | "warm amber light, candlelight, golden" |
| Neutral | 5000-5500K | "neutral white light, daylight balanced" |
| Cool | 6000-7500K | "cool blue light, moonlight, clinical white" |
| Mixed | Varies | "warm key light against cool background, color contrast" |

### AI Film Lighting Tips

1. **Flux handles dramatic lighting beautifully** — chiaroscuro, neon, and silhouette are where it shines. Flat "office lighting" produces the worst results.
2. **Describe the light SOURCE** — not just "dim" but "lit by a single bare bulb hanging from the ceiling, harsh shadows, spiderweb of cracks in the plaster"
3. **The video model struggles with flickering/changing lights** — if the light changes mid-clip, the result looks unnatural. Keep lighting consistent within a clip unless it's a dramatic reveal.
4. **"Cinematic lighting" is a real prompt phrase** that Flux understands. Use it as a quality booster.

## Color Palette (Film Look)

| Palette | Prompt Colors | Mood |
|---------|--------------|------|
| **Teal & Orange** | "teal shadows, orange skin tones, blockbuster color grade" | Hollywood, modern |
| **Desaturated** | "desaturated, muted colors, low saturation" | Bleak, realistic |
| **Warm / Amber** | "warm color grade, amber shadows" | Nostalgic |
| **Cool / Blue** | "cool blue color grade, cyan tint" | Sci-fi, clinical |
| **Technicolor** | "vibrant saturated colors, technicolor look" | Stylized, retro |
| **Monochrome** | "black and white, monochrome, high contrast" | Noir, timeless |
| **Split tone** | "split toning, teal shadows with peach highlights" | Stylized modern |
| **Sepia** | "sepia tone, vintage photograph look" | Period, memory |

### Color Grade System (Stacks on Film Stock)

The color grade is the final color treatment — it stacks on top of the film stock's base color science. Specify both for precise control:

| Grade | Prompt Phrase | Stacks On |
|-------|---------------|-----------|
| **Teal and orange** | "teal shadows, orange skin tones, blockbuster color grade" | ARRI Alexa |
| **High contrast crushed blacks** | "crushed blacks, deep shadows, high contrast" | Any stock |
| **Desaturated flat** | "desaturated, muted colors, flat matte finish" | Fujifilm |
| **Golden hour amber** | "warm amber grade, golden highlights" | Kodak Portra |
| **Vibrant saturated** | "vibrant colors, saturated, technicolor" | 35mm |
| **Cool blue and teal** | "cool blue color grade, teal highlights" | ARRI Alexa |
| **Flat matte lifted shadows** | "lifted blacks, flat matte finish, modern commercial" | Any stock |

## Film Stock / Camera Body (Visual DNA)

Each camera body carries a distinct color science and visual feel applied globally across the shoot. This is the **visual DNA** — get this right and everything downstream benefits.

| Camera Body | Look | Prompt Phrase | Best For |
|-------------|------|---------------|----------|
| **ARRI Alexa** | Cinematic, clean, neutral | "shot on ARRI Alexa, cinematic color science" | General cinema, blockbuster look |
| **Fujifilm** | Warm, faded, filmic | "Fujifilm stock, warm color profile, slightly faded" | Nostalgic, indie, romance |
| **Kodak Portra 400** | Editorial, natural skin tones | "Kodak Portra 400, editorial color" | Portraits, fashion, beauty |
| **16mm** | Grainy, raw, documentary | "16mm film stock, heavy grain, raw documentary feel" | Gritty realism, found footage |
| **35mm** | Classic grain, cinema | "35mm film stock, classic cinema grain" | Period pieces, classic cinema |
| **Hasselblad** | Tonal depth, medium format | "Hasselblad medium format, rich tonal gradation" | High-end editorial, luxury |
| **Disposable camera** | Flash, nostalgic, lo-fi | "disposable camera aesthetic, direct flash, slightly overexposed" | 90s nostalgia, candid moments |
| **GoPro** | Fisheye, action POV | "GoPro POV, wide fisheye, action camera" | Action sequences, POV shots |

**Film stock + color grade stacking example:** `Fujifilm (warm, faded) + High contrast crushed blacks` = warm-but-punchy indie look. `ARRI Alexa (clean) + Flat matte lifted shadows` = modern commercial aesthetic.

## Cut Types & Pacing (Video Editing)

For multi-shot sequences, specify cut types between shots to control energy and time:

| Cut | Prompt Phrase | Effect |
|-----|---------------|--------|
| **Smash cut** | "smash cut to" | Jarring, maximum contrast — best for tense reveals, flashbacks |
| **Hard cut** | "hard cut to" | Clean, standard — invisible editing |
| **Dissolve** | "dissolve to" | Time passing, soft transition — dreamlike, reflective |
| **Match cut** | "match cut, [visual element] carries through" | Visual rhyme — connects two scenes through a shared shape/motion |
| **Whip pan** | "whip pan to" | Energy, disorientation — action beat between shots |

### Pacing Styles

| Style | Clip Duration | Feel | Best For |
|-------|--------------|------|----------|
| **Fast cuts** | 2-3s per clip | Urgent, energetic | Action, trailers, TikTok |
| **Slow cinema** | 4-8s per clip | Deliberate, contemplative | Drama, emotional beats |
| **Mixed** | Varies (fast flashback / slow present) | Dynamic | Timeline splits, genre blends |

## Aspect Ratios

| Ratio | Name | Use | Flux Generation Size |
|-------|------|-----|---------------------|
| **16:9** | Widescreen | Standard video | 1024×576 or 1216×684 |
| **2.35:1** | Cinemascope | Epic film look | 1216×512 or 1344×576 |
| **4:3** | Academy | Vintage, surveillance | 1024×768 |
| **1:1** | Square | Social media | 1024×1024 |
| **9:16** | Vertical | TikTok/Reels/Shorts | 576×1024 |

> **Recommendation for micro-dramas:** 16:9 for YouTube, 9:16 for TikTok/Reels distribution. Flux produces best quality at resolutions divisible by 64 (e.g., 1024×576, 1216×684).

## Shot List Template (for Pipeline)

Each script scene is broken into **sub-scenes** (1A, 1B, 1C...) — one per camera position.
Each sub-scene becomes one shot card in the studio with one first-frame keyframe image.

```markdown
## SHOT LIST — [Scene Title]

| Sub | Shot | Size | Angle | Movement | Lens | Lighting | Duration | Keyframe (moment before action) |
|-----|------|------|-------|----------|------|----------|----------|-------------|
| 1A | WS | Wide | Eye level | Dolly in | 35mm | Golden hour | 5s | Character at the room's edge, before entering |
| 1B | MCU | Medium | Low angle | Static | 85mm | Rembrandt | 5s | Character looking down, before the look up |
| 1C | CU | Closeup | Eye level | Push in | 50mm | Chiaroscuro | 4s | Neutral expression, before the smile |
```

## Sub-Scene Shot Size Convention

| Letter | Shot Size | Best For |
|--------|-----------|----------|
| **A** | Wide / Establishing | Location setting, scale |
| **B** | Medium / Two-shot / OTS | Dialogue, interaction |
| **C** | Closeup / ECU | Emotion, reaction, detail |

## Storyboard Grid Annotation Strips

A production-level storyboard grid (9-panel 3×3) needs annotation strips under each panel to communicate camera, action, and mood. These are written as screenplay-style slug lines — short, uppercase, period-separated.

### Three-Line Format

Each panel's annotation strip carries three short lines:

```
CAM:    [camera framing and movement]
MOVE:   [what the subject does — short, punchy]
MOOD:   [emotional / atmospheric beat]
```

### Genre-Adaptive Third Line

The third line adapts to what matters most for the genre:

| Line Tag | Genre | Carries |
|----------|-------|---------|
| **MOOD** | Default drama / dance / cinematic narrative | Atmosphere, emotion |
| **VOICE** | Vlog / influencer / dialogue-driven | The spoken line |
| **STYLE** | Martial arts / action / fight choreography | Stance or technique |

### Annotation Rhythm

Annotations must read like a director's notes, not a paragraph. Target cadence:

- **2-6 words per line**
- **End-of-line periods** to separate short phrases: `SLOW LOW ORBIT. WIDE.`
- **Uppercase** for production-note feel
- **No full sentences** — slug lines only

### Strong Examples

```
CAM: SLOW LOW ORBIT. WIDE.         CAM: WHIP-PAN WITH LUNGE. MEDIUM.
MOVE: STANDOFF. CHERRY PETALS.     MOVE: VIPER LUNGES, PALM STRIKE.
MOOD: TENSION. STILLNESS.          STYLE: VIPER — SILAT / VIPER'S BITE.

CAM: SELFIE CAM. CLOSE.            CAM: RISING ORBIT. PUSH-IN.
MOVE: HOLDS BOTTLE UP TO CAMERA.   MOVE: FULL-BODY EXTENSION. ARMS REACH.
VOICE: "OKAY GUYS, I FOUND IT."    MOOD: AWAKENING. SOFT PIANO. BUILD.
```

### Design Rule

Request the annotation text in a clean, high-contrast sans-serif font legible at the rendered grid size. The whole point of the strip is that the user can read it — bad legibility kills the board's usefulness as a production document.

## Scene Breakdown Format (Sub-Scene Naming)

For AI film production, each script scene should be broken into **sub-scenes** by shot size/angle. Each sub-scene gets one card, one first+last frame generation, and one video clip.

### Naming Convention
```
Scene 1A — The Archive (Wide)
Scene 1B — The Archive (Confrontation)
Scene 1C — The Archive (Reaction)
```

### Standard Breakdown Template

| Sub-Scene | Shot Size | Purpose | Duration |
|-----------|-----------|---------|----------|
| **A** | Wide / Establishing | Set the scene, show location | 10-15s |
| **B** | Medium / Two-shot / OTS | Dialogue, interaction | 15-30s |
| **C** | Closeup / ECU | Reaction, emotional beat, reveal | 5-10s |

### Per Micro-Drama (5 script scenes × 3 shots each = 15 sub-scenes)

For a 10-minute film with 5 script scenes, the breakdown typically produces 10-15 sub-scenes:

| Script Scene | Sub-Scenes | Total Clips |
|-------------|------------|-------------|
| Scene 1 | 1A (Wide) + 1B (Medium) + 1C (CU) | 3 |
| Scene 2 | 2A (Wide) + 2B (CU) | 2 |
| Scene 3 | 3A (Wide) + 3B (Two-shot) + 3C (CU) | 3 |
| Scene 4 | 4A (Wide) + 4B (Medium) + 4C (CU) | 3 |
| Scene 5 | 5A (Wide) + 5B (CU) | 2 |
| **Total** | | **13** |

### First-Frame Strategy per Sub-Scene

Each sub-scene gets **one first-frame keyframe**: the opening composition at this shot size, captured the moment BEFORE the action. The video model moves forward from it — the motion and camera move go in the video prompt, not the image.

The camera direction should describe the **progression within the shot**, e.g.:
- "Wide → medium push" means the camera stays wide at start and pushes in by end
- "Closeup" means the camera stays tight throughout
- "Pull back" means starting tight and ending wider

### Why This Format Works for AI

1. **The video model generates 3-6 second clips** — each sub-scene maps to one generation
2. **Consistent framing within a clip** — easier for the model than a scene that mixes wide and closeup
3. **Clear approval workflow** — approve/reject individual shots without redoing the whole scene
4. **Each card gets 2 attachments** (first + last frame) and produces 1 video — clean mapping

## Visual Style Archetypes

For establishing the **overall visual language of an entire project** (not just individual shots), these archetypes package color grade, lighting, camera movement, and architectural vocabulary into a single consistent system. Pick one archetype at the concept stage — it becomes the visual DNA every prompt inherits.

### Sci-Fi Archetypes

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Dominant cyan and magenta | "cyan and magenta color grade, neon palette, high-saturation highlights" |
| **Lighting** | High-contrast chiaroscuro | "chiaroscuro lighting, deep shadows, pools of neon light" |
| **Camera** | Heavy anamorphic flares | "anamorphic lens, blue lens flares, wide angle" |
| **Environment** | Constant rain or haze, brutalist architecture | "rain-slicked streets, steam from vents, brutalist concrete structures, towering holographic billboards" |
| **Exemplars** | *Blade Runner, Blade Runner 2049, The Matrix, Ghost in the Shell* |

**Prompt formula:**
```
Cyberpunk neon noir aesthetic: [SUBJECT] in a rain-slicked alley,
cyan and magenta neon reflections in puddles, steam rising,
anamorphic lens flares, chiaroscuro lighting with deep shadows
```

### Grounded Speculative Realism

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Desaturated, sterile earth tones + clinical whites | "desaturated, muted earth tones, sterile whites, flat matte finish" |
| **Lighting** | Flat, clinical overhead | "flat overhead fluorescent lighting, no dramatic shadows, clinical white" |
| **Camera** | Slow objective tracking, wide deep-focus | "slow tracking shot, deep focus, wide frame, objective camera" |
| **Environment** | Empty corridors, isolation, technological vastness | "empty corridor, human figure small against massive structure, sterile surfaces" |
| **Exemplars** | *2001: A Space Odyssey, Arrival, Interstellar, Gattaca* |

**Prompt formula:**
```
Grounded speculative realism aesthetic: [SUBJECT] in a sterile
environment, desaturated earth tones and clinical whites, flat
overhead lighting, deep focus wide frame, human isolation against
technological scale
```

### Industrial Grunge & Retrofuturism

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Monochromatic green CRT glow, grease-and-steam shadows | "green CRT monitor glow, monochromatic palette, grease and grime tones" |
| **Lighting** | Heavy shadow, single practical sources | "single practical light source, harsh shadows, pools of darkness" |
| **Camera** | Claustrophobic framing, high grain | "claustrophobic framing, heavy film grain, handheld, 16mm texture" |
| **Environment** | Tactile mechanical interfaces, steam, cramped corridors | "grease-stained machinery, steam vents, cramped corridors, physical switches, riveted metal panels" |
| **Exemplars** | *Alien, The Terminator, Children of Men, Snowpiercer* |

**Prompt formula:**
```
Industrial grunge aesthetic: [SUBJECT] in a cramped mechanical space,
grease and steam, single harsh light source, green CRT glow, heavy
grain, claustrophobic framing, tactile analog controls
```

### Maximalist Space Opera & Cyber Action

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Vibrant, high-saturation, massive depth | "vibrant saturated colors, rich deep blacks, teal and orange grade" |
| **Lighting** | Dramatic, multi-source with rim lights | "dramatic multi-source lighting, rim light, volumetric light beams" |
| **Camera** | Fluid kinetic movement, complex compositions | "fluid steadicam, kinetic camera movement, layered composition, crane shot" |
| **Environment** | Massive spatial depth, impossible scale | "vast interior space, impossible scale, floating elements, deep depth of field" |
| **Exemplars** | *Dune, Star Wars: Empire Strikes Back, The Fifth Element, Inception* |

**Prompt formula:**
```
Maximalist space opera aesthetic: [SUBJECT] in a vast interior with
impossible scale, vibrant saturated colors, dramatic rim lighting,
fluid camera movement, layered composition with massive depth
```

### Clinical Corporate Dystopia

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Pastel blues, surgical whites | "pastel blue and surgical white palette, cool color grade, sterile" |
| **Lighting** | Flat fluorescent, no shadows | "flat fluorescent overhead lighting, even illumination, no shadows" |
| **Camera** | Locked-off static shots, symmetrical framing | "locked-off static camera, perfectly symmetrical composition, wide shot" |
| **Environment** | Flawless sterile interiors, architectural grids | "flawless sterile interior, grid-pattern ceiling, identical cubicles, white walls, no personal items" |
| **Exemplars** | *Severance, Westworld, Black Mirror, Devs, Altered Carbon* |

**Prompt formula:**
```
Clinical corporate dystopia aesthetic: [SUBJECT] in a sterile
corridor, pastel blue and white palette, flat fluorescent lighting,
perfectly symmetrical composition, locked-off static camera, no
shadows, identical repeating architecture
```

### Cosmic Realism & Space Politics

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Bleak, low-lux deep space vs harsh vacuum light | "bleak low-lux interior, cold metal tones, harsh unfiltered sunlight" |
| **Lighting** | High-contrast hard light or bleak low-lux | "hard single-source light simulating unfiltered sunlight, or low-lux deep space darkness with small practicals" |
| **Camera** | Handheld documentary-style | "handheld documentary camera, slight natural shake, verite style" |
| **Environment** | Functional interiors, worn ship surfaces | "functional spacecraft interior, worn metal surfaces, exposed wiring, utilitarian furniture" |
| **Exemplars** | *The Expanse, Battlestar Galactica, For All Mankind, Foundation* |

**Prompt formula:**
```
Cosmic realism aesthetic: [SUBJECT] on a functional spacecraft, worn
metal surfaces, handheld documentary camera, hard vacuum light or
bleak low-lux interior, utilitarian, no stylization
```

### Gritty Post-Apocalyptic Survival

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Blown-out overexposed sunlight + decaying organic | "blown-out overexposed highlights, desaturated organic decay, muted greens and browns" |
| **Lighting** | Harsh natural light, no artificial sources | "harsh natural sunlight, no artificial lighting, overexposed sky" |
| **Camera** | Handheld tracking, frantic energy | "frantic handheld tracking shot, immediate physical stakes, tight on subject" |
| **Environment** | Overgrown urban ruins, decaying concrete | "decaying concrete ruins, overgrown with vegetation, rubble, collapsed structures, rust" |
| **Exemplars** | *Fallout, Silo, The Last of Us, Station Eleven, Dark* |

**Prompt formula:**
```
Gritty post-apocalyptic aesthetic: [SUBJECT] in overgrown urban ruins,
blown-out overexposed sky, harsh natural sunlight, handheld tracking
shot, decayed concrete and rust
```

### Suburban Paranormal & Period Sci-Fi

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Warm nostalgic amber → cold oppressive shadows | "warm amber tungsten tones shifting to cold blue shadows, heavy grain" |
| **Lighting** | Warm tungsten with abrupt strobe | "warm practical lamp lighting, abruptly shifting to cold strobe effect, flickering" |
| **Camera** | Nostalgic framing, then disorienting angles | "nostalgic medium shot, warm and comfortable, then dutch angle, disorienting handheld" |
| **Environment** | Suburban domestic → anomalous overlay | "suburban living room, wood paneling, warm lamps, then" cold anomalous overlay, flickering shadows" |
| **Exemplars** | *Stranger Things, Fringe, X-Files, Orphan Black, Tales from the Loop* |

**Prompt formula:**
```
Suburban paranormal aesthetic: [SUBJECT] in a warm amber-lit domestic
interior, heavy grain, nostalgic texture — then abruptly shifting to
cold oppressive shadows with strobe effect as the anomalous elements
appear
```

### How to Use These Archetypes

1. **Pick one at concept stage** — The entire project inherits the archetype's visual DNA.
2. **Reference the archetype name in every scene prompt** — e.g., `Clinical corporate dystopia aesthetic: [scene description]`
3. **Mix archetypes for specific beats** — A story set in Clinical Corporate Dystopia can cut to Suburban Paranormal for a flashback. Just be deliberate and consistent about which archetype governs which timeline.
4. **Archetype stacks on film stock and color grade** — The archetype establishes the overall visual language; film stock and color grade refine the execution. `Clinical corporate dystopia + ARRI Alexa + cool blue grade` is a valid stack.

---

### Comedy Archetypes

#### Bright High-Key Commercial

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Vibrant, highly saturated primary colors | "vibrant saturated primary colors, clean bright palette, bold reds and blues" |
| **Lighting** | Ultra-bright high-key, minimal shadows | "high-key lighting, flawless bright illumination, no shadow depth, soft fill from all directions" |
| **Camera** | Wide or medium multi-camera setups | "wide frame allowing full-body physical comedy, medium two-shot for dialogue, locked-off multi-camera style" |
| **Environment** | Flawless, clean commercial spaces | "bright clean interior, organized space, vibrant pops of color in set dressing" |
| **Exemplars** | *Anchorman, The Hangover, Superbad, Step Brothers, Dumb and Dumber* |

**Prompt formula:**
```
Bright high-key commercial comedy aesthetic: [SUBJECT] in a vibrant
clean environment, ultra-bright high-key lighting, minimal shadows,
saturated primary colors, wide frame for physical comedy timing
```

#### Stylized Deadpan & Absurdist

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Muted pastel or sharply curated monochrome | "muted pastel color palette, carefully curated monochrome tones, deliberate color restriction" |
| **Lighting** | Flat, deliberate, or theatrical | "flat even lighting, no naturalism, theatrical spotlight, stark single source" |
| **Camera** | Whip-pans, sudden zooms, rigid tracking | "whip pan, crash zoom, rigid tracking shot, perfectly symmetrical framing, flat composition" |
| **Environment** | Meticulously symmetrical or deliberately flat | "perfectly symmetrical room, flat depth, minimalist set design, curated absurdity" |
| **Exemplars** | *The Grand Budapest Hotel, Airplane!, Monty Python and the Holy Grail, Shaun of the Dead* |

**Prompt formula:**
```
Stylized deadpan absurdist comedy aesthetic: [SUBJECT] in a perfectly
symmetrical frame, muted pastel palette or curated monochrome, flat
lighting, whip-pan and crash zoom camera language
```

---

### Dramedy Archetypes

#### Grounded Naturalistic Melancholy

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Muted organic tones (olive greens, ambers, soft blues) | "muted organic tones, olive green and soft amber, desaturated earth palette" |
| **Lighting** | Soft single-source natural, realistic shadow drop-off | "soft natural window light, single key source, realistic shadow falloff, diffused and gentle" |
| **Camera** | Handheld or loose tracking, lingering on quiet spaces | "handheld camera, loose tracking shot, lingering frame, quiet observational pauses" |
| **Environment** | Lived-in domestic or functional spaces | "lived-in apartment, warm but messy, functional kitchen, cluttered shelves" |
| **Exemplars** | *Fleabag, The Bear, Ted Lasso, Succession, Atlanta, Barry* |

**Prompt formula:**
```
Grounded naturalistic dramedy aesthetic: [SUBJECT] in a lived-in space,
soft natural window light, muted organic olive and amber tones,
handheld camera lingering on quiet domestic details
```

#### Vibrant Witty Maximalism

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Warm, highly saturated, stylized | "warm highly saturated palette, stylized rich colors, golden and jewel tones" |
| **Lighting** | Warm stylized lighting, theatrical warmth | "warm theatrical lighting, golden fill, stylized practical lamps" |
| **Camera** | Energetic sweeps, whip-pans, tightly paced | "energetic camera sweep, whip pan, rapid-fire editing pace, kinetic movement" |
| **Environment** | Vibrant, over-styled, character-rich | "vibrant maximalist interior, character-rich decor, bold wallpaper, eclectic furniture" |
| **Exemplars** | *The Marvelous Mrs. Maisel, Sex Education, Schitt's Creek, The Good Place* |

**Prompt formula:**
```
Vibrant witty maximalism aesthetic: [SUBJECT] in a vibrant over-styled
interior, warm highly saturated colors, energetic camera sweeps,
theatrical golden lighting, rapid editing pace
```

---

### Romance Archetypes

#### Golden Hour Idealism

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Rich warm amber, rose, and golden tones | "warm golden amber palette, rose-tinted highlights, golden hour warmth" |
| **Lighting** | Backlit, diffusion-filtered, soft glow | "backlit with diffusion filter, soft glowing rim light, warm wrap-around fill" |
| **Camera** | Shallow depth of field, locked on couple | "shallow depth of field, background completely blurred, locked on the couple, 85mm portrait lens" |
| **Environment** | Romantic vistas, intimate secluded spaces | "golden hour landscape, secluded intimate space, warm-toned interior with soft curtains" |
| **Exemplars** | *The Notebook, La La Land, About Time, Before Sunrise, Pride & Prejudice* |

**Prompt formula:**
```
Golden hour idealism romance aesthetic: [SUBJECTS] in a sunlit
secluded space, backlit with warm diffusion, shallow depth of field,
rose and amber tones, soft glowing rim light
```

#### Moody Indie Tender

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Cool desaturated, or mixed-source warmth | "cool desaturated palette, mixed-source lighting, dim intimate tones" |
| **Lighting** | Neon streetlights, dim bedroom lamps, mixed sources | "neon streetlight through window, dim bedside lamp, mixed color temperatures" |
| **Camera** | Handheld intimate, close on hands/eyes/micro-interactions | "handheld intimate camera, extreme closeup on hands, shallow focus on eyes, tight framing" |
| **Environment** | Dim interiors, late-night city spaces | "dim apartment interior at night, city lights through window, quiet late-night space" |
| **Exemplars** | *Past Lives, Her, Eternal Sunshine of the Spotless Mind, Portrait of a Lady on Fire* |

**Prompt formula:**
```
Moody indie tender romance aesthetic: [SUBJECTS] in a dim intimate
space, cool desaturated with mixed-source warmth, handheld closeup on
hands and eyes, neon bleed from window
```

#### Opulent Period Romanticism

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Deep majestic jewel tones (emeralds, sapphires, rich crimsons) | "deep jewel tones, emerald and sapphire, rich crimson accents, opulent color palette" |
| **Lighting** | Glistening candlelight, soft daytime interior | "glistening candlelight, warm wax glow, soft daytime window light diffused through curtains" |
| **Camera** | Wide sweeping cinematic dollies, grand framing | "wide sweeping dolly shot, grand cinematic framing, crane movement, majestic scale" |
| **Environment** | Historical estates, opulent ballrooms, grand landscapes | "opulent historical estate, grand ballroom with chandeliers, sweeping landscape with manor" |
| **Exemplars** | *Bridgerton, Normal People, Outlander, Crash Landing on You, Queen of Tears* |

**Prompt formula:**
```
Opulent period romanticism aesthetic: [SUBJECTS] in a grand historical
estate, deep jewel tones, glistening candlelight, wide sweeping dolly,
majestic framing emphasizing societal scale
```

#### Bittersweet Contemporary Realism

| Dimension | Description | Prompt Keywords |
|-----------|-------------|-----------------|
| **Color** | Low-contrast, cool overcast or soft domestic ambers | "low-contrast palette, cool overcast tones, soft domestic ambers" |
| **Lighting** | Overcast soft, or warm practical lamps | "soft overcast window light, no hard shadows, warm practical lamp in evening scenes" |
| **Camera** | Lingering steady closeups, long takes | "lingering steady closeup, long uninterrupted take, patient camera, uncomfortable pauses" |
| **Environment** | Everyday domestic spaces, quiet shared routines | "everyday apartment, quiet domestic routine, shared kitchen, sofa at night" |
| **Exemplars** | *One Day, Normal People, Heartstopper, Lovesick, Feel Good* |

**Prompt formula:**
```
Bittersweet contemporary romance aesthetic: [SUBJECTS] in a quiet
domestic space, cool overcast light with soft amber warmth, lingering
steady closeup, long take capturing unedited space between them
```

---

## Film & Series Visual Library

A reference library mapping essential sci-fi films and series to their visual DNA. Use these to rapidly generate prompts that capture a specific film's look.

**Format note:** Entries 1-20 (from the initial 40-entry bulk import) use a compact table with: Archetype, Palette, Lighting, Camera, Production, Scene formula. Entries 21+ (from later analysis batches) use an extended format that adds Costume + Gen Keywords columns. For corresponding image/video/character prompt keywords for entries 1-20, see `ai-film-prompt-engineering` → Film-Specific Prompt Keywords Reference.

Each entry lists the archetype it exemplifies, its unique color/lighting/camera signature, and a prompt formula for its most iconic scene.

### Top 20 Sci-Fi Films

#### 1. 2001: A Space Odyssey (1968)
| Element | Description |
|---------|-------------|
| **Archetype** | Grounded Speculative Realism |
| **Palette** | Stark white, deep black, bone ivory, electric blue, warm amber |
| **Lighting** | Clinical overexposed whites; HAL's red eye as single warm tone |
| **Camera** | Extreme wide shots for human insignificance; slow deliberate pans; perfect symmetry; 2.20:1 anamorphic |
| **Production** | Minimalist techno-sublime; sterile corporate futurism; white curved ergonomics vs cosmic abstraction |
| **Scene formula** | `2001 aesthetic: extreme wide shot of [SUBJECT] against pristine white curved interior, clinical overexposed light, perfect symmetry, slow deliberate pan, deep black void visible through porthole, minimalist techno-sublime scale` |

#### 2. Blade Runner (1982)
| **Archetype** | Cyberpunk Neon Noir |
| **Palette** | Acid rain grey, neon magenta, amber sodium, teal shadow, soot black |
| **Lighting** | Hard directional shafts through smoke and rain; venetian blind shadows; flame jets as sole warmth |
| **Camera** | Low angles emphasizing urban scale; extreme deep focus; slow searching movements; 2.39:1 |
| **Production** | Noir retro-futurism; layered vertical city; ancient structures encrusted in corporate signage |
| **Scene formula** | `Blade Runner aesthetic: [SUBJECT] in rain-slicked alley, neon magenta and teal reflections, hard light shafts through smoke, low angle against towering brutalist structures, anamorphic flares, acid rain grey atmosphere` |

#### 3. Alien (1979)
| **Archetype** | Industrial Grunge & Retrofuturism |
| **Palette** | Industrial charcoal, rust brown, sickly yellow, deep shadow black, pale skin ivory |
| **Lighting** | Motivated practical sources — flickering fluorescents, handheld lamps, emergency reds; large areas of deliberate darkness |
| **Camera** | Handheld in chase; slow creeping tracking; extreme close-ups of alien anatomy; 2.39:1 scope |
| **Production** | Blue-collar spacecraft — worn consoles, dripping pipes; Giger's alien ship as ossified nightmare |
| **Scene formula** | `Alien aesthetic: [SUBJECT] in worn industrial spacecraft interior, flickering fluorescent light, dripping condensation, rust and charcoal tones, handheld camera, claustrophobic framing, deliberate dark areas, emergency red glow` |

#### 4. The Matrix (1999)
| **Archetype** | Cyberpunk Neon Noir |
| **Palette** | Matrix green, desaturated blue-grey, warm amber, electric blue, black leather |
| **Lighting** | Strong color grading per world — green for simulation, cold blue for real; hard contrast for action |
| **Camera** | Bullet-time 360-degree freeze; wire-fu; 12,000fps extreme slow-motion; handheld chaos |
| **Production** | Cyberpunk tech-noir; leather-and-black aesthetic; clean corporate simulation vs industrial dystopia |
| **Scene formula** | `Matrix aesthetic: [SUBJECT] in green-tinted simulation, desaturated blue-grey reality contrast, bullet-time 360-degree rotation around action, cascading green code rain, black leather, wire-fu choreography in extreme slow motion` |

#### 5. Interstellar (2014)
| **Archetype** | Grounded Speculative Realism |
| **Palette** | Dust ochre, deep space black, ice blue, golden wheat, horizon orange |
| **Lighting** | Natural sunlit farmland vs zero-point darkness; Gargantua's accretion disc as warm artificial sun |
| **Camera** | IMAX 70mm ground-level dust bowl perspective; immersive space travel; intimate handheld for emotion |
| **Production** | Oklahoma Dust Bowl authenticity; practical cockpit for IMAX; tesseract as memory palace |
| **Scene formula** | `Interstellar aesthetic: [SUBJECT] in sweeping dust bowl landscape, golden ochre wheat fields, natural sunlit horizon, IMAX 70mm ground-level perspective, then cutting to deep space black with ice blue cold, Gargantua's warm accretion disc glow` |

#### 6. Star Wars: A New Hope (1977)
| **Archetype** | Maximalist Space Opera |
| **Palette** | Desert tan, imperial grey, rebel orange, starfield black, lightsaber blue and red |
| **Lighting** | Harsh desert sun; clean fluorescent Empire; warm fire-lit Rebels; theatrical rim for heroes |
| **Camera** | Dutch angles for menace; dynamic dogfight camera; wipe transitions as visual grammar |
| **Production** | "Used future" principle — everything worn and functional; Death Star as brutalist evil |
| **Scene formula** | `Star Wars aesthetic: [SUBJECT] in used-future space, desert tan and imperial grey palette, harsh natural light, Dutch angle, wipe transitions, lived-in functional technology, lightsaber blue and red contrast, John Williams heroic scale` |

#### 7. Arrival (2016)
| **Archetype** | Grounded Speculative Realism |
| **Palette** | Mist grey, forest green, amber memory warmth, obsidian black, blue-tinted dawn |
| **Lighting** | Diffused overcast natural light; otherworldly glow inside heptapod shell; warm for memory/future |
| **Camera** | Long patient shots; camera tilts disorienting inside ship; extreme close-ups of ink |
| **Production** | Shell ship as massive tilting void; circular rooms echoing heptapod language structure |
| **Scene formula** | `Arrival aesthetic: [SUBJECT] facing alien heptapod through glass barrier, mist grey and obsidian black palette, diffused overcast light, circular interior with tilted perspective, alien ink bloom emerging on glass, patient long take, quiet dread` |

#### 8. Inception (2010)
| **Archetype** | Maximalist Space Opera |
| **Palette** | Amber dreamscape, cool city grey, white limbo, sepia memory, deep shadow black |
| **Lighting** | Distinct temperature per dream level — warm amber for deep, cool blue for city, harsh white for hospital |
| **Camera** | Handheld for reality; strange angles for dreams; zero-g hallway rotating camera; wide lens distortion |
| **Production** | Paris streets that fold; hotel corridors rotating 360º; Limbo as half-built brutalist city on ocean |
| **Scene formula** | `Inception aesthetic: [SUBJECT] in dreamspace with warm amber tones, architectural surrealism, impossible geometry, slow push-in as reality bends, layered dream levels each with distinct color temperature, zero-gravity object physics` |

#### 9. Ex Machina (2014)
| **Archetype** | Clinical Corporate Dystopia |
| **Palette** | Concrete grey, forest green, transparent glass, flesh tones, cold blue LED |
| **Lighting** | Clinical overlit facility vs organic dappled forest; Ava lit from within by LED |
| **Camera** | Static symmetric framing; slow methodical push-ins; minimal camera mirrors controlled environment |
| **Production** | Glass-and-concrete facility; each room a psychological trap; Ava's transparent body as art object |
| **Scene formula** | `Ex Machina aesthetic: [SUBJECT] in glass-and-concrete underground facility, clinical overlit white, static symmetrical framing, slow methodical push-in, transparent android with internal LED glow, cold blue technology contrast with forest green through window` |

#### 10. Dune (2021)
| **Archetype** | Maximalist Space Opera |
| **Palette** | Sandstone amber, deep ochre, bone white, shadow indigo, blood orange horizon |
| **Lighting** | Extreme natural desert silhouette; interior blue-violet for Bene Gesserit; green for Caladan |
| **Camera** | Immense wide shots making figures microscopic; extreme macro for sand granules; slow zoom for reveals |
| **Production** | Nabataean rock-cut architecture; Fremen sietch as underground cathedral; ornithopter as dragonfly craft |
| **Scene formula** | `Dune aesthetic: [SUBJECT] as microscopic figure against immense sandstone dune, amber and ochre palette, extreme natural desert light creating silhouette, wide shot of impossible scale, sandworm emerges from bone white horizon, Hans Zimmer subsonic rumble` |

#### 11. Gravity (2013)
| **Archetype** | Grounded Speculative Realism |
| **Palette** | Cosmic black void, brilliant white sunlit spacecraft, blue Earth atmosphere, orange fire re-entry |
| **Lighting** | Single sun source — extreme contrast; all shadows absolute; Earth terminator creates dramatic half-light |
| **Camera** | 17-minute continuous virtual opening shot; 360º floating camera; claustrophobic helmet POV |
| **Production** | ISS at 1:1 detail; Soyuz as coffin and womb; debris as ballet of shrapnel |
| **Scene formula** | `Gravity aesthetic: [SUBJECT] floating in vast black void, single sun source creating absolute shadows, Earth rotating below in blue atmosphere, continuous floating camera, claustrophobic helmet POV, tears floating as droplets, cosmic silence` |

#### 12. Metropolis (1927)
| **Archetype** | Clinical Corporate Dystopia |
| **Palette** | Black and white expressionism, stark contrasts, silver robot gleam, geometric shadow |
| **Lighting** | German Expressionist extreme contrast; long diagonal shadows; single key theatrical chiaroscuro |
| **Camera** | Monumental scale shots; extreme close-ups of machinery; Expressionist tilted angles; crowd choreography |
| **Production** | Art Deco futurism; upper city as paradise, underground as labyrinthine industrial hell |
| **Scene formula** | `Metropolis aesthetic: [SUBJECT] in German Expressionist frame, stark black and white contrast, long diagonal shadows, Art Deco mega-city with soaring towers above and industrial labyrinth below, masses moving in mechanical unison, silver robot chrome gleam` |

#### 13. Children of Men (2006)
| **Archetype** | Gritty Post-Apocalyptic Survival |
| **Palette** | Grey-green fatigue, concrete brown, blood red spots, dirty white, rare warm amber for hope |
| **Lighting** | Desaturated naturalistic; overcast UK skies; firelight as only warmth; no beauty |
| **Camera** | Long unbroken takes (4-min car attack, 5-min battle); handheld documentary; digital grain; blood on lens |
| **Production** | Britain as refugee camp; Bexhill as Gaza-inspired internment; familiar landmarks in decay |
| **Scene formula** | `Children of Men aesthetic: [SUBJECT] in grey-green desaturated near-future collapse, overcast UK sky, handheld documentary camera, long unbroken take, blood spatter on lens, concrete brown ruins, rare warm firelight, exhausted survival posture` |

#### 14. The Terminator (1984)
| **Archetype** | Industrial Grunge & Retrofuturism |
| **Palette** | Night blue neon, orange flame, chrome silver, shadow black, red targeting HUD |
| **Lighting** | 80s LA neon-and-streetlight; Terminator POV red HUD overlay; Tech-Noir bar neon |
| **Camera** | Low-angle making Terminator monolithic; red-tinted POV; documentary chase urgency |
| **Production** | 80s LA as authentic document; future as apocalyptic blue-grey; factory as industrial hellscape |
| **Scene formula** | `Terminator aesthetic: [SUBJECT] in night-time LA, blue neon and orange flame palette, low angle shot making figure monolithic, red targeting HUD POV overlay, chrome glint on machinery, unstoppable mechanical movement, documentary chase aesthetic` |

#### 15. Annihilation (2018)
| **Archetype** | Suburban Paranormal & Period Sci-Fi (with bioluminescent horror) |
| **Palette** | Bioluminescent green, iridescent rainbow sheen, flesh pink, swamp grey-green, crystalline white |
| **Lighting** | The Shimmer as diffused rainbow prism light; lighthouse as clinical white descent |
| **Camera** | Steady observation as biological survey; floating handheld when horror erupts; double-exposure for doppelgänger |
| **Production** | Abandoned town colonised by human-shaped plants; lighthouse as mutating flesh architecture |
| **Scene formula** | `Annihilation aesthetic: [SUBJECT] inside the Shimmer, bioluminescent rainbow sheen over everything, iridescent plant-life grown into human shapes, crystalline trees refracting prism light, steady observational camera, then rupturing into body horror, Lighthouse as clinical white descent` |

#### 16. District 9 (2009)
| **Archetype** | Gritty Post-Apocalyptic Survival |
| **Palette** | Documentary grey-brown, alien blue-black, sewage sepia, orange rust, red blood |
| **Lighting** | Harsh Johannesburg sunlight; no romance — clinical naturalism; available light philosophy |
| **Camera** | Mockumentary with interview segments; shaky handheld in action; news-cam aesthetic |
| **Production** | Prawn shacks in actual Soweto locations; alien exoskeleton as scavenged industrial; MNU corporate glass |
| **Scene formula** | `District 9 aesthetic: [SUBJECT] in Johannesburg shantytown, harsh natural sunlight, documentary handheld camera, mockumentary interview segments, alien blue-black against grey-brown poverty, rust and sewage sepia, newscam style, social realism as sci-fi` |

#### 17. Minority Report (2002)
| **Archetype** | Clinical Corporate Dystopia |
| **Palette** | Desaturated blue-silver, warm amber sepia, white corporate clean, green holographic |
| **Lighting** | Washed-out silver over-exposure; amber for Pre-Crime memory; clinical white for facility |
| **Camera** | Wide angle distortion for surveillance unease; extreme eye close-ups; fluid Steadicam vertical city |
| **Production** | Gestural holographic UI; magnetised vertical highways; pre-crime cathedral of surveillance |
| **Scene formula** | `Minority Report aesthetic: [SUBJECT] in desaturated blue-silver future DC, gestural holographic interface with translucent panels, vertical city with magnetic highway traffic, eye-level surveillance unease, amber memory sequences, personified advertising scanning retinal ID` |

#### 18. Avatar (2009)
| **Archetype** | Maximalist Space Opera |
| **Palette** | Bioluminescent blue-violet, emerald jungle, floating mountain mist, RDA military grey, Na'vi turquoise |
| **Lighting** | Pandora's bioluminescence as ecosystem-that-IS-lighting; RDA harsh fluorescence; cloud diffusion |
| **Camera** | Performance-capture matched to 3D digital; wide-angle for ecological scale; intimate for Na'vi culture |
| **Production** | Fully consistent biosphere; floating Hallelujah Mountains; Hometree as living cathedral |
| **Scene formula** | `Avatar aesthetic: [SUBJECT] on bioluminescent Pandora, every footstep triggering rippling blue light in moss, emerald jungle with floating mist mountains, performance-capture Na'vi with turquoise skin and iridescent scales, living forest as interactive light installation, RDA cold military grey contrast` |

#### 19. Sunshine (2007)
| **Archetype** | Grounded Speculative Realism |
| **Palette** | Extreme solar white, deep black void, golden amber interior, red warning, blue Earth memory |
| **Lighting** | Sun as character — overwhelming, beautiful, fatal; warm amber inside vs solar annihilation outside |
| **Camera** | Overexposed sun bleach-out; Dutch angles increasing as psychology deteriorates; staccato edit for madness |
| **Production** | Icarus II as functional spacecraft with observation room toward sun; dying Icarus I as horror ship |
| **Scene formula** | `Sunshine aesthetic: [SUBJECT] on sun-proximity spacecraft, extreme solar white overwhelming the frame, warm amber observation room light, faces half-lit in solar glow reflecting sun-gaze rapture, Dutch angles as psychology deforms, overexposed star surface, gold visor spacesuits` |

#### 20. Everything Everywhere All at Once (2022)
| **Archetype** | Vibrant Witty Maximalism / Stylized Deadpan Absurdist |
| **Palette** | Chaotic rainbow multiverse, hot pink, IRS grey-beige despair, googly eye black-white |
| **Lighting** | Deliberately inconsistent — each universe distinct temperature; IRS fluorescent; verse-jumping streaks |
| **Camera** | Extreme rapid editing (2,000 cuts); crash zooms; split-diopter; handheld chaos; aspect ratio changes per universe |
| **Production** | IRS as existential purgatory; laundromat as domestic battlefield; bagel as void; wardrobe signals tone per universe |
| **Scene formula** | `Everything Everywhere aesthetic: [SUBJECT] in chaotic multiverse, hot pink and IRS grey-beige contrast, rapid cut between universes with distinct color temperatures, crash zoom into absurdist detail, googly eyes as philosophical commentary, split-diopter of mundane and cosmic simultaneously` |

### Top 20 Sci-Fi Series

| Rank | Series | Archetype | Palette | Lighting & Camera | Scene Prompt Formula |
|------|--------|-----------|---------|-------------------|---------------------|
| **1** | Battlestar Galactica (2004-2009) | Cosmic Realism | Military khaki, deep black, amber cockpit, algae-tank green | Documentary handheld with crash zooms; realistic combat inertia | `Battlestar Galactica aesthetic: [SUBJECT] on aging warship bridge, documentary handheld, amber cockpit glow, military khaki and deep space black, DRADIS triangular radar display, worn consoles and hand-chalked kill boards, post-9/11 military realism` |
| **2** | Black Mirror (2011-) | Clinical Corporate Dystopia | Clinical white, screen blue, surveillance grey, hot memory colour | Episode-specific — documentary handheld, music-video gloss, surveillance cam | `Black Mirror aesthetic: [SUBJECT] in near-future technology horror, clinical white and screen blue palette, surveillance camera style, dystopian interface overlays, cold digital fluorescence, discomfort in clean familiar spaces` |
| **3** | The Expanse (2015-2022) | Cosmic Realism | Belter grey-brown, UN blue, Mars red-grey, protomolecule blue, Rocinante orange | Physics-accurate lighting—all illumination from specific sources; zero-gravity with no inertial dampeners | `Expanse aesthetic: [SUBJECT] on physics-accurate spacecraft, zero-g with thrust gravity effects, faction-specific fashion—Belter scavenged vs UN authority blue vs Mars military red, protomolecule electric blue bioluminescence, documentary realism in space` |
| **4** | Westworld (2016-2022) | Clinical Corporate Dystopia | Wild West golden brown, control room sterile white, red-black Shogun World, Futureworld chrome-blue | Warm Western sun vs cool clinical lab; host awakening signaled by lighting shift | `Westworld aesthetic: [SUBJECT] in theme park of cruelty, warm golden Western sun on Sweetwater main street, cutting to sterile white control room, host perfect loop behavior fracturing, Ford's creator gaze, maze as internal consciousness journey` |
| **5** | Dark (2017-2020) | Suburban Paranormal | Pine forest green-black, amber lamplight, era-specific grading—1953 sepia, 2019 grey-blue, 2053 ash | Each era distinct temperature; caves in amber lantern light; symmetrical loops | `Dark aesthetic: [SUBJECT] in German small town across three eras, symmetrical composition mirroring time loops, 1953 warm tungsten sepia, 2019 cold LED grey-blue, 2053 apocalyptic ash, cave as nexus with amber lantern light, slow push-in revealing connections` |
| **6** | Severance (2022-) | Clinical Corporate Dystopia | Lumon corporate white, medical fluorescent, outie warm muted, file room blue-grey | Zero natural light on severed floor — full artificial fluorescence; Kubrickian one-point perspective | `Severance aesthetic: [SUBJECT] on Lumon severed floor, zero natural light, perfectly symmetrical corridor extending to vanishing point, medical fluorescent white, macrodata refinement amber, corporate-warm outie world contrast, Kubrickian slow zoom, existential dread in beige` |
| **7** | Stranger Things (2016-) | Suburban Paranormal | 80s warm amber, Upside Down deep red-black, Lab fluorescent, neon pink, Christmas light warm | Spielberg golden-hour exterior; Upside Down deep crimson; lab harsh fluorescence | `Stranger Things aesthetic: [SUBJECT] in 1983 suburban Indiana, warm Spielberg golden hour, Hawkins Lab harsh fluorescence, Upside Down as deep red-black mirror world with floating particles, nostalgic 80s props, child protagonists on bikes at dusk, D&D reference as visual metaphor` |
| **8** | The X-Files (1993-2018) | Suburban Paranormal | Pacific NW green-grey, flashlight yellow cone, government office grey, alien green, conspiracy amber | Flashlight as primary light source; government harshly over-lit; absolute black for alien | `X-Files aesthetic: [SUBJECT] in Pacific Northwest gloom, flashlight cutting through darkness as primary light source, government building harsh over-lit, alien green glow in absolute black, Mulder's conspiracy-wall office, partner walking at matched investigative pace` |
| **9** | Star Trek: TNG (1987-1994) | Maximalist Space Opera | Enterprise gold-red, LCARS orange-blue, alien chromatic diversity | Luxury hotel warm; distinct temperature per alien world; theatrical formal framing | `Star Trek: TNG aesthetic: [SUBJECT] on Enterprise-D bridge, warm luxury hotel lighting, LCARS orange-blue display panels, formal theatrical framing, three-camera dialogue blocking, optimistic utopian future, Picard command stance, make-it-so decisiveness` |
| **10** | Firefly (2002-2003) | Cosmic Realism | Frontier dust brown, engine orange, Alliance blue-white, Western earth tones | Practical engine warm glow; Core harsh commercial; frontier natural UV-harsh | `Firefly aesthetic: [SUBJECT] on Serenity, frontier dust brown and warm engine glow, handheld documentary camera in space, zoom and whip-pan news-cam style, Alliance sterile corporate contrast, lived-in working ship with distinct rooms, Chinese-English mixed signage` |
| **11** | Altered Carbon (2018-2020) | Cyberpunk Neon Noir | Neon magenta, deep teal shadow, rain-soaked black, gold plutocrat amber | Extreme Blade Runner neon; Meth towers warm gold above street purgatory | `Altered Carbon aesthetic: [SUBJECT] in Bay City 300 years further into decay, neon magenta and teal shadow, rain-soaked black streets below, gold amber Meth towers above clouds, cortical stack glowing purple, hotel AI as holographic Victorian, sleeve-transfer body horror` |
| **12** | For All Mankind (2019-) | Grounded Specular Realism | NASA orange-grey, lunar white-shadow, Mars red, alternate history amber | Period color grading per decade; lunar harsh vacuum light; IMAX-quality space | `For All Mankind aesthetic: [SUBJECT] in alternate history space race, period-accurate color grading per decade, lunar surface harsh vacuum light, Jamestown base as Cold War outpost, IMAX-quality space photography, NASA documentary mixed with dramatic reconstruction` |
| **13** | Devs (2020) | Clinical Corporate Dystopia | Gold leaf, silicon valley green, quantum white, night blue SF, blood red | Devs building as impossible gold light; exterior SF tech-boom clean; surveillance blue | `Devs aesthetic: [SUBJECT] in quantum computing sanctuary, impossibly lit gold-leaf interior with no visible source, symmetrical static frames, deterministic horror beneath calm surfaces, silicon valley green campus, quantum simulation displays as overlapping probability, quiet dread` |
| **14** | Andor (2022-) | Cosmic Realism | Industrial grey-brown, Imperial white, rebel ochre, Ferrix warm stone, Coruscant cold blue | Practical working-class lighting; Imperial oppressive over-lighting; rebel shadow and inadequate lamp | `Andor aesthetic: [SUBJECT] in Star Wars working-class reality, Imperial Stasi-esque security office, Ferrix industrial town with practical labour light, handheld documentary realism, un-glamorous rebellion, Luthen's double-identity body language shift, Narkina 5 brutalist prison` |
| **15** | Station Eleven (2021-2022) | Grounded Specular Realism | Pre-pandemic warm amber, Year Twenty muted earth, Symphony theatrical colour | Before: warm and full; After: natural overcast; Theatre candlelight as beacon | `Station Eleven aesthetic: [SUBJECT] in post-collapse world, pre-pandemic warm amber memory, Year Twenty muted earth natural light, Traveling Symphony performing Shakespeare by candlelight, airport as accidental settlement, fragmented timeline fluid camera, survival as art` |
| **16** | Fringe (2008-2013) | Suburban Paranormal | Amber fringe lab, parallel universe sepia, FBI institutional grey, fedora black, cortexiphan blue | Walter's lab warm; FBI procedural cold; parallel universe distinct sepia grade | `Fringe aesthetic: [SUBJECT] in Walter's eccentric lab, warm amber scientific chaos, alternate universe sepia grade, Observer fedora black and clinical stillness, fringe science as procedural, dual-universe production design, cortexiphan blue energy glow` |
| **17** | Raised by Wolves (2020-2022) | Industrial Grunge & Retrofuturism | Kepler-22b tan desert, android chrome-white, Mithraic jewel-purple, blood red | Alien binary sun creating foreign shadows; Mother's white eye glow; Mithraic torchlight | `Raised by Wolves aesthetic: [SUBJECT] on Kepler-22b alien planet, binary sun creating foreign shadow angles, android chrome-white with internal light, Mithraic jewel-purple torch rituals, South African desert as alien topography, biblical creation myth as hard sci-fi` |
| **18** | Humans (2015-2018) | Clinical Corporate Dystopia | Synth grey-blue, domestic warm home, corporate white, Niska red warning | Synths cooler than humans; conscious synths develop warmer personal space lighting | `Humans aesthetic: [SUBJECT] with synthetic human, synth slightly cooler blue-grey lighting, domestic warm human contrast, conscious awakening shown through posture graduation from service-submissive to human-assertive, charging station as furniture, Persona Synthetics Apple-dystopia` |
| **19** | Travelers (2016-2018) | Clinical Corporate Dystopia | Future transmission blue-white, host body warm present, FBI grey, team ochre | Consciousness arrival as overloaded flash; Vancouver naturalistic grey; emergency red | `Travelers aesthetic: [SUBJECT] in body-takeover drama, future consciousness arriving as white flash in present body, present-day Vancouver naturalistic grey, FBI procedural aesthetic, small-scale time travel, anachronistic gesture learning curves, daily life as ethical minefield` |
| **20** | The Peripheral (2022-) | Clinical Corporate Dystopia | Appalachian rust-green, London 2099 chrome blue, peripheral orange-metal | Rural warm documentary; 2099 London cold corporate; peripheral body with wrong warmth | `Peripheral aesthetic: [SUBJECT] in dual-timeline, Appalachian rural warmth vs 2099 London cold corporate chrome, peripheral body with uncanny wrong-warmth lighting, consciousness transfer seamless jump-cut, Jackpot collapse as historical texture, future technology with no visible interface` |

### Additional Entries (Expanded Coverage)

#### 21. Blade Runner 2049 (2017)
| Element | Description | Gen Keywords |
|---------|-------------|-------------|
| **Archetype** | Cyberpunk Neon Noir | `cinematic neo noir future` |
| **Palette** | Amber deserts, cold cyan interiors, industrial grey, neon orange | `brutalist science fiction architecture` |
| **Lighting** | Volumetric haze, diffused practical, strong silhouettes, atmospheric fog | `volumetric lighting` |
| **Camera** | Large-format compositions, extreme depth, slow controlled movement, monumental architecture dominating figures | `slow cinematic tracking shot` |
| **Production** | Decaying megacity, industrial farms, corporate authoritarian environments | `lonely futuristic detective` |
| **Costume** | Minimalist utilitarian, structured silhouettes, muted colours | `emotionally restrained futuristic investigator` |
| **Scene formula** | `Blade Runner 2049 aesthetic: [SUBJECT] isolated in monumental amber desert, volumetric haze and atmospheric fog, cold cyan neon against industrial grey, slow tracking shot through decaying megastructure, lonely figure dwarfed by brutalist architecture` | |

#### 22. Dune: Part Two (2024)
| Element | Description | Gen Keywords |
|---------|-------------|-------------|
| **Archetype** | Maximalist Space Opera | `epic desert science fiction` |
| **Palette** | Sand gold, black, deep blue, muted earth tones | `cinematic IMAX scale` |
| **Lighting** | Natural sunlight, harsh desert contrast, dramatic silhouettes | `futuristic ancient civilization` |
| **Camera** | IMAX large-scale compositions emphasizing landscapes, wide framing, slow majestic movement | `slow monumental camera movement` |
| **Production** | Ancient futuristic civilizations, brutalist spacecraft, ritualistic architecture | `massive desert battle` |
| **Costume** | Cultural garments inspired by historical civilizations and desert survival gear | `futuristic desert warrior` |
| **Scene formula** | `Dune Part Two aesthetic: [SUBJECT] as microscopic figure against impossible-scale desert landscape, sand gold and deep blue palette, harsh natural light creating warrior silhouettes, IMAX wide framing emphasizing prophecy and scale, Fremen ritual ceremonial movement` | |

#### 23. Her (2013)
| Element | Description | Gen Keywords |
|---------|-------------|-------------|
| **Archetype** | Moody Indie Tender | `warm futuristic romance` |
| **Palette** | Soft reds, orange, pastel tones, warm neutrals | `minimal technology lifestyle` |
| **Lighting** | Natural sunlight, gentle interior lighting, emotional close-up warmth | `soft cinematic lighting` |
| **Camera** | Warm intimate photography, slow observational shots, close character framing | `intimate future relationship scene` |
| **Production** | Near-future city that feels familiar rather than futuristic; technology is invisible and integrated | `lonely futuristic writer` |
| **Costume** | High-waisted contemporary clothing with soft futuristic styling | `modern soft fashion` |
| **Scene formula** | `Her aesthetic: [SUBJECT] in warm soft-lit near-future apartment, warm amber and pastel tones, natural sunlight through windows, intimate close-up framing, invisible AI voice interface, emotional vulnerability in quiet domestic space, soft futuristic everyday clothing` | |

#### 24. Aliens (1986)
| Element | Description | Gen Keywords |
|---------|-------------|-------------|
| **Archetype** | Industrial Grunge & Retrofuturism (military variant) | `military science fiction` |
| **Palette** | Military green, black, grey, industrial orange | `alien colony battlefield` |
| **Lighting** | Tactical lighting, flashlights, emergency illumination | `futuristic marines` |
| **Camera** | Handheld combat photography, military action framing, squad formation shots | `tactical squad movement` |
| **Production** | Colonial marine dropship, Hadley's Hope colony, alien hive biomechanical architecture | `future marine soldier` |
| **Costume** | Colonial marine armour, tactical survival equipment, pulse rifles | `advanced combat armour` |
| **Scene formula** | `Aliens aesthetic: [SUBJECT] in tactical military squad formation, green and black industrial palette, flashlight cutting through dark colony corridors, handheld combat camera, pulse rifle weapon readiness, dropship interior with army equipment, biomechanical alien hive as overwhelming threat` | |

#### 25. The Fifth Element (1997)
| Element | Description | Gen Keywords |
|---------|-------------|-------------|
| **Archetype** | Maximalist Space Opera | `colourful retro futuristic city` |
| **Palette** | Neon orange, blue, yellow, white, vibrant saturated colours | `1990s sci-fi fashion` |
| **Lighting** | Bright futuristic city lighting, theatrical colour effects | `fantasy technology` |
| **Camera** | Fast movement, unusual angles, playful composition, energetic adventure style | `fast futuristic adventure sequence` |
| **Production** | Highly imaginative future metropolis, flying car highways, luxury space hotel | `vibrant space opera` |
| **Costume** | Avant-garde futuristic fashion with exaggerated silhouettes | `eccentric future hero` |
| **Scene formula** | `Fifth Element aesthetic: [SUBJECT] in vibrant neon retro-future metropolis, orange and blue saturated colour, fast playful camera movement, flying car traffic highway, avant-garde exaggerated fashion, alien cultures in dense visual environment, fantasy technology, theatrical comedic energy` | |

#### 26. Gattaca (1997)
| Element | Description | Gen Keywords |
|---------|-------------|-------------|
| **Archetype** | Clinical Corporate Dystopia | `retro futuristic corporate world` |
| **Palette** | Sepia, grey, cream, muted blue, corporate neutrals | `genetic engineering society` |
| **Lighting** | Soft natural lighting with controlled shadows | `minimalist architecture` |
| **Camera** | Precise compositions, symmetry, restrained movement, elegant minimalist framing | `quiet futuristic corporate drama` |
| **Production** | Retro-futuristic architecture blending 1960s aesthetics with advanced biometric technology | `biometric technology scene` |
| **Costume** | Formal minimalist corporate fashion, clean professional lines | `future corporate professional` |
| **Scene formula** | `Gattaca aesthetic: [SUBJECT] in elegant retro-futuristic corporate facility, sepia and cream palette, soft natural light through modernist architecture, symmetrical restrained framing, biometric scanner interfaces, formal minimalist fashion, hidden identity beneath perfect genetic society` | |

#### 27. Moon (2009)
| Element | Description | Gen Keywords |
|---------|-------------|-------------|
| **Archetype** | Grounded Speculative Realism | `lonely lunar base` |
| **Palette** | Cold whites, industrial greys, metallic blues, muted earth tones | `retro futuristic science fiction` |
| **Lighting** | Clinical artificial lighting contrasted with dark lunar environments | `minimal space drama` |
| **Camera** | Slow controlled movement, static compositions, observational framing | `slow astronaut isolation scene` |
| **Production** | Functional lunar mining facility with retro-futuristic technology | `isolated lunar worker` |
| **Costume** | Simple astronaut work suits, practical industrial clothing | `functional astronaut suit` |
| **Scene formula** | `Moon aesthetic: [SUBJECT] in solitary lunar mining facility, cold white and metallic grey palette, clinical artificial light against dark lunar surface, static observational frame, retro-futuristic computer terminals, slow repetitive movement in empty corridors, isolation and identity questioning` | |

### Expanded Series Coverage

| Rank | Series | Archetype | Palette | Lighting & Camera | Scene Prompt Formula |
|------|--------|-----------|---------|-------------------|---------------------|
| **21** | Silo (2023-) | Gritty Post-Apocalyptic Survival | Industrial grey, rust, brown, muted green, low-saturation | Practical industrial lighting; vertical compositions; confined claustrophobic framing | `Silo aesthetic: [SUBJECT] in massive underground silo, industrial grey and rust palette, practical industrial lighting, vertical architecture reinforcing hierarchy, slow investigative movement through confined tunnels, functional workwear reflecting social status, hidden history beneath survival` |
| **22** | Foundation (2021-) | Maximalist Space Opera | Gold, white, deep space black, jewel tones, metallic colours | Elegant palace lighting; cosmic illumination; large-scale establishing shots, slow majestic movement | `Foundation aesthetic: [SUBJECT] in galactic imperial palace, gold and white jewel-toned palette, elegant cosmic illumination, grand establishing shot of Trantor city-planet, characters as historical figures within enormous civilization, ceremonial futuristic royal clothing` |
| **23** | The Last of Us (2023-) | Gritty Post-Apocalyptic Survival | Earth tones, faded greens, grey skies, warm human interiors | Naturalistic lighting; abandoned urban shadows; slow character-focused movement | `The Last of Us aesthetic: [SUBJECT] in overgrown abandoned city, faded green and grey palette, natural light through decaying structures, slow emotional character journey, worn practical survival clothing, fungal growth reclaiming urban infrastructure, quiet trust-building between survivors` |
| **24** | 3 Body Problem (2024-) | Grounded Speculative Realism | Cold scientific blues, dark space tones, warm historical sequences | Scientific laboratory lighting; surreal virtual environments; large-scale cinematic framing | `3 Body Problem aesthetic: [SUBJECT] in modern research laboratory, cold scientific blue palette, virtual reality headset interface, cosmic mystery behind everyday science, professional contemporary clothing, characters confronting existential alien threat through physics and mathematics` |

## Reference Files

This skill has support files in the `references/` directory:

- `references/archetype-film-mapping.md` — Quick-lookup index of which films/series map to each of the 16 Visual Style Archetypes. Use this to find all entries for a given archetype without scanning the full library.

### Comedy Film Entries

| # | Film | Archetype | Palette | Lighting & Camera | Scene Formula |
|---|------|-----------|---------|-------------------|---------------|
| **C1** | The Grand Budapest Hotel (2014) | Stylized Deadpan & Absurdist | Pastel pinks, lavender, cream, gold, vintage European tones | Soft diffused storybook lighting; precise symmetrical framing, fast lateral movements, theatrical staging | `Grand Budapest Hotel aesthetic: [SUBJECT] in symmetrical pastel-coloured European hotel, soft diffused lighting like a painted illustration, precise theatrical framing, fast lateral tracking, vintage formal uniforms, deadpan expression amid absurd elegance` |
| **C2** | Groundhog Day (1993) | Grounded Naturalistic Melancholy | Warm small-town colours, winter blues, cosy interiors | Natural daylight and comfortable domestic lighting; straightforward observational framing supporting comedic timing | `Groundhog Day aesthetic: [SUBJECT] in charming small-town winter setting, warm cosy interiors and winter blues palette, repeating daily routine through natural daylight, character transformation from arrogant to humble, comfortable domestic lighting` |
| **C3** | Superbad (2007) | Bright High-Key Commercial | Warm suburban tones, party colours, everyday environments | Practical party lighting; handheld movement, conversational framing, energetic editing | `Superbad aesthetic: [SUBJECT] in awkward teenage suburban setting, warm naturalistic party lighting, handheld conversational camera, awkward teenage physicality, realistic casual fashion, friendship under social pressure` |
| **C4** | Airplane! (1980) | Stylized Deadpan & Absurdist | 1970s aviation colours, muted interiors, bright airport environments | Standard commercial film lighting; traditional cinematic framing played completely seriously for comedic effect | `Airplane! aesthetic: [SUBJECT] in 1970s airline setting, realistic aviation interior lighting, deadpan straight-faced delivery of absurd dialogue, serious cinematic framing creating comedic contrast, retro aviation uniforms and period technology` |
| **C5** | The Hangover (2009) | Bright High-Key Commercial | Warm Las Vegas neon, gold, nightlife colours, urban tones | Nightclub and hotel lighting mixed with bright daytime; handheld energy with polished commercial comedy shots | `Hangover aesthetic: [SUBJECT] in Las Vegas adventure, warm neon nightlife lighting, luxury hotel environments, chaotic comedy journey through increasingly absurd consequences, modern casual nightlife clothing, friendship tested by forgotten events` |
| **C6** | Monty Python and the Holy Grail (1975) | Stylized Deadpan & Absurdist | Earth tones, muted medieval colours, natural landscapes | Natural outdoor lighting; traditional medieval adventure framing interrupted by absurd visual jokes | `Monty Python Holy Grail aesthetic: [SUBJECT] in absurd medieval setting, natural outdoor light and simple interiors, intentionally imperfect low-budget production design, overdramatic theatrical movement, serious fantasy staging undermined by surreal comedy` |
| **C7** | Bridesmaids (2011) | Grounded Naturalistic Melancholy | Warm domestic tones, soft pastels, colourful wedding environments | Natural daylight and cosy interiors; conversational framing, reaction shots, ensemble coverage | `Bridesmaids aesthetic: [SUBJECT] in modern wedding preparation setting, warm naturalistic domestic lighting, emotional comedy through social pressure, contemporary fashion reflecting personality and insecurity, friendship dynamics through group interaction` |
| **C8** | Mean Girls (2004) | Bright High-Key Commercial | Pink, pastel colours, bright school environments, fashionable tones | Clean commercial-style lighting; energetic school-life coverage with reaction-focused editing | `Mean Girls aesthetic: [SUBJECT] in high school hierarchy, bright pink and pastel commercial lighting, social groups organised visually like a battlefield, fashionable teen costume identity design, competition through physical confidence and eye contact` |
| **C9** | Dumb and Dumber (1994) | Bright High-Key Commercial | Bold colours, roadside landscapes, playful tones | Bright commercial lighting; wide shots emphasising physical comedy | `Dumb and Dumber aesthetic: [SUBJECT] in 1990s road trip adventure, bright bold colour palette, wide frame for slapstick physical comedy, iconic colourful outfits, extreme exaggerated facial reactions, awkward confidence and misunderstanding-driven chaos` |
| **C10** | The Truman Show (1998) | Clinical Corporate Dystopia (satirical) | Bright pastel colours, artificial blues, cheerful suburban tones | High-key TV production lighting; surveillance-style angles mixed with traditional cinematic framing | `Truman Show aesthetic: [SUBJECT] in perfect artificial suburb, high-key television production lighting, surveillance camera angles, symmetrical perfect town revealing its constructed reality, controlled social behaviour becoming natural, 1990s casual suburban clothing` |
| **C11** | Jojo Rabbit (2019) | Stylized Deadpan & Absurdist | Warm autumn colours, pastel tones, playful contrasts | Soft natural storybook lighting; stylised centred compositions and expressive movement | `Jojo Rabbit aesthetic: [SUBJECT] in romanticised European wartime village, warm autumn and pastel palette, soft natural storybook warmth, symmetrical composition with childlike perspective, playful innocence contrasting with serious reality, period clothing with youthful exaggeration` |
| **C12** | Ferris Bueller's Day Off (1986) | Bright High-Key Commercial | Bright suburban colours, blue skies, vibrant interiors | Clean youthful commercial lighting; dynamic movement, breaking conventions, playful framing | `Ferris Bueller aesthetic: [SUBJECT] in 1980s suburban adventure, bright blue skies and vibrant colour palette, energetic playfully breaking the fourth wall, direct audience engagement, iconic 80s teenage fashion, city as a playground, confident dance movements` |

## Common Pitfalls

1. **Asking Flux for shots it can't do** — Wide shots with multiple characters often have garbled anatomy. If you need a wide shot, describe it abstractly or use silhouette. Save closeups for &quot;hero&quot; images.
2. **The video model can't do rapid camera moves** — a whip pan or crash zoom will look like a glitch. Stick to slow dollying, trucking, or subtle pushes.
3. **Mixing lighting in one clip** — If the keyframe is &quot;golden hour&quot; but the prompt asks for a &quot;moonlit&quot; shift mid-clip, the model produces weird semi-lit frames. Keep lighting consistent within a clip.
4. **Aspect ratio consistency** — Keep your keyframes 16:9 from the start; the clip inherits the keyframe's aspect ratio, so a mixed set of ratios breaks the edit.
5. **Too much camera movement for short clips** — In a 5-second clip, a &quot;dolly in from wide to closeup&quot; is too much distance. Use subtle movement for short clips.

### Dramedy Series Entries

| # | Series | Archetype | Palette | Lighting & Camera | Scene Formula |
|---|--------|-----------|---------|-------------------|---------------|
| **D1** | Ted Lasso (2020-2023) | Grounded Naturalistic Melancholy | Bright greens, warm yellows, soft blues, welcoming colours | Natural daylight and stadium lighting; fluid movement, expressive close-ups, team-focused framing | `Ted Lasso aesthetic: [SUBJECT] in warm optimistic football setting, bright green pitch and yellow sunshine, natural daylight and cosy pub interiors, team-focused framing emphasising human connection, British football casual sportswear, open body language of trust and kindness` |
| **D2** | The Bear (2022-) | Grounded Naturalistic Melancholy | Warm restaurant tones, steel grey, earthy colours, natural textures | Practical kitchen lighting; fast handheld movement, close-ups, chaotic energy | `The Bear aesthetic: [SUBJECT] in intense working restaurant kitchen, warm steel and earth-tone palette, practical kitchen lighting and close-ups, fast handheld camera capturing chaotic energy, chef whites and aprons, stress and pressure felt in tight spaces, food preparation as emotional language` |
| **D3** | Fleabag (2016-2019) | Grounded Naturalistic Melancholy | Natural London tones, muted colours, occasional warm highlights | Realistic interiors; close emotional framing with direct-to-camera moments | `Fleabag aesthetic: [SUBJECT] in intimate London setting, muted natural palette with warm highlights, close emotional framing breaking the fourth wall, realistic interiors of cafes and apartments, contemporary fashion revealing character, humour masking vulnerability through direct audience connection` |
| **D4** | The Office (US) (2005-2013) | Grounded Naturalistic Melancholy | Neutral office tones, beige, grey, natural workplace colours | Fluorescent office lighting; handheld documentary movement, zooms, reaction shots | `The Office US aesthetic: [SUBJECT] in mundane office environment, beige and grey fluorescent-lit cubicles, handheld mockumentary camera with awkward reaction zooms, corporate casual clothing, social discomfort as comedy through documentary observation` |
| **D5** | Succession (2018-2023) | Vibrant Witty Maximalism | Dark luxury tones, grey, black, blue, neutral colours | Corporate interiors with natural light and dramatic shadows; handheld, sudden zooms, documentary influence | `Succession aesthetic: [SUBJECT] in luxury corporate environment, dark neutral tones and dramatic shadows, aggressive handheld camera with sudden zooms, high-end business attire showing understated wealth, power struggles through verbal battles and strategic manipulation, emotional isolation despite luxury` |
| **D6** | Only Murders in the Building (2021-) | Vibrant Witty Maximalism | Warm apartments, autumn colours, rich interior tones | Soft dramatic lighting with cosy mystery atmosphere; elegant movement, visual clues | `Only Murders aesthetic: [SUBJECT] in stylish New York apartment building, warm autumn and rich interior tones, soft mystery lighting, elegant camera revealing visual clues alongside comedic character moments, distinctive character-driven fashion, unlikely friendship through podcast investigation` |
| **D7** | Barry (2018-2023) | Grounded Naturalistic Melancholy | Muted blues, grey urban tones, occasional warm emotional contrasts | Naturalistic lighting with dramatic shadows; controlled static compositions mixed with sudden chaotic movement | `Barry aesthetic: [SUBJECT] in Los Angeles suburban-crime duality, muted blue and grey palette, naturalistic lighting with dramatic shadows, controlled static frames ruptured by sudden violence, simple realistic clothing hiding a double life, blank exterior masking internal moral collapse` |
| **D8** | Atlanta (2016-2022) | Grounded Naturalistic Melancholy | Warm urban tones, muted colours, atmospheric night scenes | Naturalistic city lighting with expressive low-light; slow observational shots with unexpected visual shifts | `Atlanta aesthetic: [SUBJECT] in authentic Atlanta urban setting, warm muted palette with expressive night photography, slow observational camera shifting into surreal commentary, contemporary streetwear and cultural fashion, casual confidence mixed with uncertainty in everyday scenes` |
| **D9** | Master of None (2015-2021) | Vibrant Witty Maximalism | Warm urban colours, soft pastels, natural tones | Natural daylight and intimate restaurant lighting; slow thoughtful compositions, conversational framing | `Master of None aesthetic: [SUBJECT] in New York creative lifestyle, warm urban and pastel palette, natural daylight and intimate restaurant lighting, slow thoughtful compositions treating everyday moments cinematically, modern minimalist fashion, relationships explored through observational humour` |
| **D10** | Reservation Dogs (2021-2023) | Grounded Naturalistic Melancholy | Earth tones, warm landscapes, muted rural colours | Natural daylight and sunset tones; observational handheld with emotional close-ups | `Reservation Dogs aesthetic: [SUBJECT] in rural Oklahoma community, warm earth tones and sunset landscapes, natural daylight observational camera, contemporary youth clothing with cultural elements, teenage friendship through humour and grief, community environment as character` |
| **D11** | Shameless (US) (2011-2021) | Grounded Naturalistic Melancholy | Cold Chicago tones, warm interiors, gritty urban colours | Natural and practical household lighting; handheld realism with energetic movement | `Shameless US aesthetic: [SUBJECT] in working-class Chicago home, cold urban exterior and warm crowded interior contrast, handheld naturalistic camera, affordable everyday clothing reflecting economic reality, family chaos as survival, arguments mixed with affection in cramped spaces` |
| **D12** | After Life (2019-2022) | Grounded Naturalistic Melancholy | Soft countryside tones, muted colours, warm interiors | Natural daylight and intimate home lighting; slow reflective compositions, emotional close-ups | `After Life aesthetic: [SUBJECT] in quiet English small town, soft muted countryside palette, natural daylight and cosy home lighting, slow reflective camera emphasising isolation, simple contemporary clothing, sarcasm masking grief, gradually opening to connection through dry humour and compassion` |
| **D13** | The Marvelous Mrs. Maisel (2017-2023) | Vibrant Witty Maximalism | Vibrant pinks, reds, blues, 1950s fashion colours | Elegant stage lighting with classic Hollywood-inspired illumination; fluid tracking shots and long takes | `Mrs. Maisel aesthetic: [SUBJECT] in 1950s New York comedy world, vibrant pink and red period palette, elegant stage lighting and fluid tracking shots, detailed 1950s fashion with bold colours, confident stage movement and quick wit, comedy club as liberation from domestic life` |

### Romance Film Entries

| # | Film | Archetype | Palette | Lighting & Camera | Scene Formula |
|---|------|-----------|---------|-------------------|---------------|
| **R1** | Before Sunrise (1995) | Moody Indie Tender | Soft natural tones, warm sunset colours, European city hues | Natural daylight to evening ambience; long takes, walking shots, uninterrupted conversations | `Before Sunrise aesthetic: [SUBJECTS] walking through Vienna at sunset, soft natural European tones, long uninterrupted conversation takes, wandering through cafes and parks, intimate connection through dialogue, casual traveller clothing, city as romantic landscape` |
| **R2** | The Notebook (2004) | Golden Hour Idealism | Warm golden tones, summer colours, nostalgic softness | Romantic sunset lighting and gentle natural illumination; sweeping emotional shots and intimate close-ups | `Notebook aesthetic: [SUBJECTS] in golden hour 1940s Southern landscape, warm nostalgic softness, sunset lighting on lake house porch, sweeping romance with intimate close-ups, period romantic fashion, love enduring through time, rain-drenched reunion kiss` |
| **R3** | La La Land (2016) | Golden Hour Idealism | Vivid primary colours, neon nights, dreamy pastels | Magical-hour and stage lighting; long takes, choreography, sweeping camera movement | `La La Land aesthetic: [SUBJECTS] in magical-hour Los Angeles, vivid primary colours and dreamy pastels, choreographed dance through city streets at sunset, long takes with sweeping camera, colour-coded modern fashion, jazz club neon, dreams and bittersweet romance` |
| **R4** | Titanic (1997) | Opulent Period Romanticism | Deep ocean blues, warm gold interiors, period elegance | Soft candlelight and dramatic sunsets; sweeping wide shots vs intimate close-ups | `Titanic aesthetic: [SUBJECTS] on Edwardian luxury ocean liner, deep blue ocean and warm gold interior candlelight, sweeping wide shot of grand staircase contrasting intimate deck romance, period Edwardian fashion reflecting class, love against inevitable fate` |
| **R5** | Eternal Sunshine of the Spotless Mind (2004) | Moody Indie Tender | Cold winter blues contrasted with warm memories | Soft natural light with dreamlike transitions; fluid camera, handheld intimacy, visual memory shifts | `Eternal Sunshine aesthetic: [SUBJECTS] in surreal memory landscape, cold winter blue reality vs warm golden memories, fluid camera transitioning through dream logic, distinctive creative casual fashion, awkward imperfect intimacy, emotional permanence versus erasure` |
| **R6** | Pride & Prejudice (2005) | Opulent Period Romanticism | Earth tones, greens, cream, soft natural colours | Natural candlelight and countryside illumination; slow graceful movement, composed romantic framing | `Pride & Prejudice aesthetic: [SUBJECTS] in English Regency countryside estate, soft green and cream palette, natural candlelight in ballrooms, slow graceful camera through manor gardens, period formal fashion reflecting class, love expressed through glances and restrained gesture` |
| **R7** | (500) Days of Summer (2009) | Moody Indie Tender | Warm urban colours, soft blues, nostalgic tones | Natural daylight and city evening lighting; creative editing, fantasy sequences, emotional contrast | `500 Days of Summer aesthetic: [SUBJECTS] in indie Los Angeles, warm urban palette with nostalgic blue tones, creative edits contrasting fantasy vs reality of relationship, modern indie fashion, playful chemistry shifting to emotional distance, nonlinear love story` |
| **R8** | Casablanca (1942) | Bittersweet Contemporary Realism | Monochrome contrast with dramatic shadows | Film noir-inspired expressive highlights; elegant close-ups, controlled classical framing | `Casablanca aesthetic: [SUBJECTS] in 1940s Moroccan nightclub, black and white dramatic shadow contrasts, film noir lighting in Rick's Cafe, elegant formal wartime fashion, love versus duty, long looks and sacrifice, melancholic farewell` |
| **R9** | When Harry Met Sally... (1989) | Bittersweet Contemporary Realism | Warm autumn colours, New York neutrals, cosy interiors | Soft natural lighting with warm restaurant ambience; conversational framing, medium shots and intimate close-ups | `When Harry Met Sally aesthetic: [SUBJECTS] in autumn New York City, warm fall colours and cosy restaurant lighting, conversational framing through city walks and diner talks, late-80s casual urban fashion, friendship evolving into love, romantic timing and emotional honesty` |
| **R10** | Atonement (2007) | Opulent Period Romanticism | Soft greens, cream tones, wartime muted colours | Natural daylight and candlelight with dramatic shadows; slow movement, sweeping landscapes, emotional close-ups | `Atonement aesthetic: [SUBJECTS] in 1930s English estate, soft green and cream palette shifting to wartime muted tones, sweeping landscape shots of countryside, period formal fashion, love disrupted by misunderstanding, tragic separation, single long-take Dunkirk beach` |
| **R11** | The Fault in Our Stars (2014) | Bittersweet Contemporary Realism | Soft blues, warm interiors, gentle pastel tones | Natural daylight and intimate bedroom lighting; close emotional framing and personal perspective | `Fault in Our Stars aesthetic: [SUBJECTS] in contemporary young adult romance, soft blue and warm interior palette, intimate close framing, casual youth fashion, emotional connection shaped by illness, Amsterdam travel scenes, love as acceptance of limited time` |
| **R12** | Call Me by Your Name (2017) | Moody Indie Tender | Warm Italian summer tones, greens, yellows, soft earth colours | Natural sunlight and golden afternoon light; slow observational framing, lingering shots, emotional close-ups | `Call Me by Your Name aesthetic: [SUBJECTS] in northern Italian summer villa, warm golden and green palette, slow observational camera lingering on summer sensations, 80s relaxed intellectual summer fashion, first love through silence and proximity, bittersweet memory` |
| **R13** | Crazy Rich Asians (2018) | Opulent Period Romanticism (or Vibrant Witty Maximalism) | Gold, emerald, jewel tones, vibrant tropical colours | High-end fashion lighting and elegant event illumination; dynamic movement, sweeping luxury shots | `Crazy Rich Asians aesthetic: [SUBJECTS] in Singapore luxury world, gold and emerald jewel-toned palette, high-fashion lighting at opulent events, dynamic camera through luxury homes and wedding venues, designer fashion with cultural influences, family expectations versus romantic love` |
| **R14** | Notting Hill (1999) | Bittersweet Contemporary Realism | Soft London colours, warm interiors, cosy tones | Natural daylight and intimate indoor lighting; gentle movement and conversational framing | `Notting Hill aesthetic: [SUBJECTS] in Notting Hill London, soft warm palette of bookshops and neighbourhood streets, gentle conversational camera, late-90s casual British fashion, ordinary person meeting celebrity, vulnerability and humour in unexpected love, neighbourhood belonging` |
| **R15** | Amélie (2001) | Moody Indie Tender | Saturated reds, greens, yellows, warm nostalgic tones | Soft romantic lighting with heightened colour expression; playful movement, visual metaphors, imaginative framing | `Amélie aesthetic: [SUBJECT] in whimsical Paris Montmartre, saturated red and green nostalgic tones, playful camera with visual metaphors and magical realism, quirky vintage French fashion, shy curiosity expressed through kind acts, city as romantic playground` |
| **R16** | The Shape of Water (2017) | Moody Indie Tender | Deep teal, green, blue, golden highlights | Moody atmospheric underwater-inspired tones; fluid dreamlike movement, symmetrical compositions | `Shape of Water aesthetic: [SUBJECTS] in dark fairy tale 1960s laboratory, deep teal and green palette with warm golden highlights, fluid camera moving like water, silent communication through touch and gesture, love beyond boundaries in isolated spaces` |
| **R17** | Silver Linings Playbook (2012) | Bittersweet Contemporary Realism | Warm suburban colours, autumn tones, everyday neutrals | Natural daylight and realistic interiors; handheld realism with intimate emotional framing | `Silver Linings Playbook aesthetic: [SUBJECTS] in Philadelphia suburban homes, warm autumn palette and natural daylight, handheld intimate camera capturing emotional intensity, casual American everyday clothing, two emotionally complicated people finding connection through dance` |

### Romance Series Entries

| # | Series | Archetype | Palette | Lighting & Camera | Scene Formula |
|---|--------|-----------|---------|-------------------|---------------|
| **RS1** | Normal People (2020) | Bittersweet Contemporary Realism | Muted greens, soft blues, warm neutrals, natural skin tones | Available light and soft window lighting; close emotional framing, lingering shots, quiet observation | `Normal People aesthetic: [SUBJECTS] in intimate Irish spaces, muted green and soft blue palette, available light through windows, lingering close-ups capturing micro-expressions, quiet restrained movement, minimal everyday clothing, miscommunication and longing in small rooms` |
| **RS2** | Bridgerton (2020-) | Opulent Period Romanticism | Pastel colours, jewel tones, gold accents, luxurious textures | Soft romantic candlelit elegance; sweeping ballroom shots, dramatic close-ups | `Bridgerton aesthetic: [SUBJECTS] in Regency London ballroom, pastel and jewel-toned palette with gold accents, soft candlelit elegance, sweeping camera through grand estates, exaggerated period fashion with modern luxury, longing glances across crowded rooms, forbidden attraction under social rules` |
| **RS3** | Outlander (2014-) | Opulent Period Romanticism | Earth tones, forest greens, stone greys, warm candle colours | Natural landscapes and firelight; sweeping landscapes combined with emotional close-ups | `Outlander aesthetic: [SUBJECTS] in 18th-century Scottish Highlands, forest green and stone grey palette, firelight in castle interiors, sweeping landscape shots of wilderness, detailed historical Scottish clothing, epic love story across time, protective and resilient physicality` |
| **RS4** | The Crown (2016-2023) | Opulent Period Romanticism | Muted royal blues, golds, greys, rich period tones | Naturalistic period lighting and candlelight; formal compositions, slow tracking shots, intimate portraits | `The Crown aesthetic: [SUBJECTS] in royal palace interiors, muted royal blue and gold palette, naturalistic candlelight, formal composed camera, highly detailed royal fashion, duty versus love in grand spaces, emotional restraint behind protocol` |
| **RS5** | Sex Education (2019-2023) | Vibrant Witty Maximalism | Bright colours, pastel tones, playful contrasts | Soft natural lighting with vibrant interiors; energetic movement, expressive framing, ensemble storytelling | `Sex Education aesthetic: [SUBJECTS] in colourful British school, bright pastel palette with playful contrasts, energetic camera through expressive school spaces, bold vintage-inspired youth fashion, teenage awkwardness and emotional exploration, romance through humour and insecurity` |
| **RS6** | This Is Us (2016-2022) | Bittersweet Contemporary Realism | Warm family tones, soft browns, nostalgic colours | Warm domestic lighting; close emotional framing with timeline transitions | `This Is Us aesthetic: [SUBJECTS] in American family homes, warm brown and nostalgic palette, close emotional camera across multiple timelines, realistic clothing changing across decades, family bonds through hugs and comforting touch, love expressed through support and memory` |
| **RS7** | Love (2016-2018) | Bittersweet Contemporary Realism | Muted LA tones, warm interiors, urban neutrals | Natural apartment lighting and realistic city illumination; handheld intimacy, conversational framing | `Love aesthetic: [SUBJECTS] in LA apartments and neighbourhoods, muted urban warm palette, handheld intimate camera capturing awkward modern dating, casual millennial fashion, unfiltered emotional reactions, romance through imperfection and honesty` |
| **RS8** | One Day (2024) | Bittersweet Contemporary Realism | Warm nostalgic tones evolving across decades | Naturalistic lighting reflecting changing life stages; character-focused close-ups, location-based storytelling | `One Day aesthetic: [SUBJECTS] across decades of British life, warm nostalgic palette evolving through time periods, character-focused close-ups tracking same-date reunions, period-accurate fashion from 90s onward, friendship and timing as romantic tension` |
| **RS9** | Younger (2015-2021) | Vibrant Witty Maximalism | Bright urban colours, pastels, fashion-forward tones | Clean commercial-style lighting; fast-paced movement, polished compositions | `Younger aesthetic: [SUBJECTS] in stylish New York publishing world, bright pastel and fashion-forward palette, polished commercial lighting, fast-paced camera through offices and events, high-fashion contemporary wardrobe, romance through wit and reinvention` |
| **RS10** | Jane the Virgin (2014-2019) | Vibrant Witty Maximalism | Bright tropical colours, warm family tones, vibrant interiors | Soft romantic lighting with cheerful warmth; expressive close-ups, dramatic zooms, playful movement | `Jane the Virgin aesthetic: [SUBJECTS] in colourful Miami family setting, bright tropical and warm family palette, playful telenovela-inspired camera with dramatic zooms, vibrant contemporary fashion, family bonds and destiny in love, heightened emotion in everyday spaces` |
| **RS11** | Emily in Paris (2020-) | Vibrant Witty Maximalism | Pastels, bright colours, Parisian neutrals, fashion tones | Soft glamorous lighting and elegant city ambience; touristic city compositions, stylish character shots | `Emily in Paris aesthetic: [SUBJECT] in fashionable Paris, pastel and bright palette against Parisian neutrals, soft glamorous cafe lighting, touristic camera through luxury city landmarks, high-fashion contemporary outfits, Paris as romantic fantasy, flirtatious charm and spontaneity` |
| **RS12** | Virgin River (2019-) | Bittersweet Contemporary Realism | Forest greens, mountain blues, warm cabin tones | Soft natural daylight and cosy interior lighting; slow scenic shots, emotional close-ups | `Virgin River aesthetic: [SUBJECTS] in small mountain town, forest green and warm cabin palette, soft natural daylight through trees, slow scenic camera of river and forests, practical rural clothing, healing and second chances through community and love` |
| **RS13** | The Time Traveler's Wife (2022) | Moody Indie Tender | Soft warm tones, muted blues, nostalgic colours | Natural romantic lighting with surreal transitions; intimate close-ups contrasted with timeline shifts | `Time Traveler's Wife aesthetic: [SUBJECTS] in emotional time-crossed romance, soft warm and muted blue palette, natural lighting with temporal disappearance transitions, intimate close-ups in homes and libraries, contemporary fashion in changing timelines, patience and enduring love across time` |
| **RS14** | The Summer I Turned Pretty (2022-) | Golden Hour Idealism | Warm sunlight, ocean blues, pastel summer tones | Golden hour and beach daylight; dreamy montages, emotional close-ups | `Summer I Turned Pretty aesthetic: [SUBJECTS] in coastal beach town, warm golden sunlight and ocean blue palette, dreamy summer montage camera, youthful playful fashion, first love and heartbreak on the boardwalk, summer as memory and emotional milestone` |
| **RS15** | Heartstopper (2022-) | Bittersweet Contemporary Realism | Pastel colours, soft greens, yellows, optimistic tones | Natural daylight with warm interiors; intimate close-ups, expressive reaction shots, playful movement | `Heartstopper aesthetic: [SUBJECTS] in British school setting, pastel soft green and yellow optimistic palette, natural daylight in warm classrooms, intimate close-ups with hand-drawn animation overlays, casual teenage fashion, first love through friendship and kindness, gentle emotional sincerity` |
| **RS16** | Daisy Jones & The Six (2023) | Vibrant Witty Maximalism | Warm vintage tones, amber lighting, faded film colours | Concert and studio warmth with retro atmosphere; handheld documentary style mixed with performance shots | `Daisy Jones aesthetic: [SUBJECTS] in 1970s rock scene, warm amber and faded vintage palette, handheld documentary camera in recording studios and concert stages, authentic 70s rock fashion, creative passion and romantic tension, expressive stage performance` |
| **RS17** | The Affair (2014-2019) | Bittersweet Contemporary Realism | Different palettes representing different character perspectives | Realistic coastal and domestic lighting; perspective-driven framing, emotional close-ups | `The Affair aesthetic: [SUBJECTS] in coastal and city environments, perspective-shifting palette reflecting different memories, subjective camera showing same event from different viewpoints, realistic contemporary fashion, desire and betrayal through conflicting perspectives` |
| **R18** | In the Mood for Love (2000) | Moody Indie Tender | Deep crimson, bottle green silk, shadow amber lantern, rain-slicked 1960s Hong Kong, melancholy blue | Extreme practical lighting — single bulbs and street lights; scenes drowning in shadow with subjects emerging; extreme slow motion for cheongsam sequences; narrow corridor framing | `In the Mood for Love aesthetic: [SUBJECTS] in 1962 Hong Kong, deep crimson and green palette, practical single-bulb lighting with faces emerging from shadow, extreme slow motion of cheongsam descent, desire expressed through withheld touch, narrow corridors as romantic compression` |
| **R19** | Portrait of a Lady on Fire (2019) | Moody Indie Tender | Breton grey-green sea, firelight amber, white linen, island fog, flame orange red | 18th century authentic candle-and-firelight only — no artificial sources; static composed shots as Dutch master paintings; the female gaze as the film's light source | `Portrait of a Lady on Fire aesthetic: [SUBJECTS] in Breton coastal manor, firelight amber and grey-green sea palette, lit entirely by candle and fireplace, static painterly compositions, white linen and period dress, looking as intimacy, fire as liberation, the final concert close-up` |
| **R20** | Dirty Dancing (1987) | Golden Hour Idealism (with grounded naturalism) | Catskills summer green, dance hall amber, leather jacket black, pink innocence, watermelon red | Performance spaces in warm amber dance-hall light; lush summer outdoor greens; dance shot full-body for choreography; low-angle for final lift scale | `Dirty Dancing aesthetic: [SUBJECTS] in Catskills summer resort, dance hall amber and summer green palette, warm performance lighting for mambo, full-body wide shots for dance choreography, leather and pink costume, dance as transgression and liberation, nobody puts Baby in a corner` |
| **R21** | Roman Holiday (1953) | Moody Indie Tender (period) | Black and white Rome, travertine stone grey, Vespa freedom white, garden party white | Golden mid-century studio black and white; Rome's outdoor light captured on location; Hepburn lit as the frame's primary subject in classical Hollywood soft focus | `Roman Holiday aesthetic: [SUBJECTS] in 1953 Rome, black and white Travertine palette, location photography through Colosseum and Spanish Steps, Vespa through ancient streets, princess haircut as liberation, one perfect day as entire romance, sacrifice as love's measure` |
| **R22** | Pretty Woman (1990) | Bittersweet Contemporary Realism (fairy tale variant) | Rodeo Drive pastel, Beverly Wilshire gold-cream, Hollywood Boulevard neon, red dress red | Beverly Hills hotel luxury warm light; harsh Hollywood neon contrast; opera in theatrical red-gold; shopping montage as fashion film | `Pretty Woman aesthetic: [SUBJECTS] in Beverly Hills fairy tale, Rodeo Drive pastels and red dress palette, luxury hotel warm lighting, shopping montage as transformation arc, strawberry in champagne, fire escape rescue as romantic gesture, Cinderella in LA` |
| **R23** | Breakfast at Tiffany's (1961) | Moody Indie Tender (period) | Manhattan silver-grey, little black dress, Tiffany's window blue, apartment warm lamp | New York late 50s colour cinematography with black-and-white glamour influence; Holly's apartment in warm chaotic lamp light; rain scene in flat grey New York light | `Breakfast at Tiffany's aesthetic: [SUBJECT] in 1961 New York, Manhattan silver-grey and Tiffany blue palette, warm apartment lamp light, rain scene in flat grey emotion, little black dress and oversized sunglasses, fire escape guitar, loneliness in beautiful disguise` |
| **R24** | Say Anything (1989) | Bittersweet Contemporary Realism | Seattle grey-green, kickboxing gym warm, achievement-world beige, boombox grey | Pacific Northwest naturalistic grey; Diane's family home in warm achievement light; airplane cabin in commercial airline light | `Say Anything aesthetic: [SUBJECT] in late 80s Seattle, grey-green and warm beige palette, naturalistic grey Pacific Northwest light, boombox upraised in early morning, trenchcoat sincerity, kickboxing as physical grace, love without strategy` |

### More Romance Series Entries

| # | Series | Archetype | Palette | Lighting & Camera | Scene Formula |
|---|--------|-----------|---------|-------------------|---------------|
| **RS18** | Downton Abbey (2010-2015) | Opulent Period Romanticism | Highclere Castle stone cream, Edwardian jewel colour, servants' quarters grey-brown, English countryside green | Period chandelier and firelight upstairs; practical functional lamp light below-stairs; wide establishing shots of Abbey grandeur; formal parlour staging | `Downton Abbey aesthetic: [SUBJECTS] in Edwardian country estate, stone cream and jewel-tone palette, chandelier upstairs and practical lamp below stairs, wide Abbey establishing shots, period formal fashion, upstairs-downstairs love, class structure examined through romance` |

### Comedy Film Entries (Expanded)

| # | Film | Archetype | Palette | Lighting & Camera | Scene Formula |
|---|------|-----------|---------|-------------------|---------------|
| **C13** | Some Like It Hot (1959) | Stylized Deadpan & Absurdist | Black and white contrast, platinum blonde, shadow and pinstripe, Florida beach glare | Diffused glamour key for Monroe; hard shadows on gangsters; bright flat beach light; classical Hollywood framing with precise comic editing | `Some Like It Hot aesthetic: [SUBJECTS] in jazz-era speakeasy or Florida resort, black and white shadow contrast, men in women's clothes performed with contrasting commitment, Monroe's luminous walk, sex farce vs gangster noir, 'nobody's perfect' closing` |
| **C14** | Annie Hall (1977) | Grounded Naturalistic Melancholy | New York grey-brownstone, Hamptons sun white, California golden tan, flashback warm sepia | Gordon Willis's dark underexposure — faces often in shadow; direct address to camera; split-screen conversations; subtitles revealing true thoughts; animated sequences | `Annie Hall aesthetic: [SUBJECTS] in neurotic New York, dark underexposed Gordon Willis cinematography, direct-to-camera address, split-screen anxiety, nervous hand gestures and intellectual performance, 70s New York as romantic battlefield` |
| **C15** | The Big Lebowski (1998) | Stylized Deadpan & Absurdist | Bowling alley neon, rug rust-brown, LA smog amber, nihilist black | Perpetual LA golden haze; bowling alley as neon cathedral; dream sequences in expressionist light; slow tracking shots through bowling alley; unhurried camera reflecting Dude's pace | `Big Lebowski aesthetic: [SUBJECT] in LA smog-golden haze, bowling alley neon cathedral, The Dude's horizontal physical philosophy, dream sequence Busby Berkeley choreography, Chandler noir as stoner comedy, misplaced rug tying everything together` |
| **C16** | This Is Spinal Tap (1984) | Stylized Deadpan & Absurdist | Rock and roll black, stage spotlight white, backstage fluorescent, album cover excess | Documentary naturalism for backstage; theatrical excess for concert sequences; mockumentary handheld throughout; rock-star sincerity in provincial venues | `Spinal Tap aesthetic: [SUBJECTS] in rock documentary, backstage fluorescent light, stadium gestures on pub stages, amplifiers that go to eleven, miniature Stonehenge set, songwriter's total sincerity about mediocre work` |
| **C17** | The Princess Bride (1987) | Bright High-Key Commercial | Fairy tale green, Buttercup yellow, pirate ship ocean blue, ROUS brown, flame-spurt orange | Storybook warmth throughout; Pit of Despair in Gothic gloom; Fire Swamp with practical fire effects; classic adventure wides for landscape, medium for swashbuckling | `Princess Bride aesthetic: [SUBJECTS] in fairy tale Florin, storybook warmth and castle green, swordplay as wit made physical, Inigo's revenge recited for 20 years, miracle Max in his hovel, true love requiring giant and fire swamp` |
| **C18** | Dr. Strangelove (1964) | Stylized Deadpan & Absurdist | Black and white clinical, War Room grey, bomber cockpit amber, Ripper's desk dark | Cold institutional War Room lighting; fish-eye lens for Ripper's mania; handheld documentary for bomber crew; Kubrick's symmetrical satire | `Dr. Strangelove aesthetic: [SUBJECTS] in Cold War endgame, Ken Adam's War Room, nuclear rodeo on falling bomb, Sellers' three-body performance, General Ripper's paranoid fish-eye, fighting arm that won't stop saluting` |
| **C19** | Clueless (1995) | Bright High-Key Commercial | Beverly Hills pastel, tartan yellow plaid, pool turquoise, mall white marble, California sun gold | Perpetual California golden hour; mall and school in aspirational commercial light; Cher's computerised closet as character POV; no shadows in Cher's world | `Clueless aesthetic: [SUBJECT] in 1995 Beverly Hills, perpetual golden hour sun, pastel plaid matching, computerised outfit selection interface, rolling through life with genuine warmth beneath apparent shallowness, 'as if'` |
| **C20** | Borat (2006) | Stylized Deadpan & Absurdist | American highway tan, suburb manicured green, hotel room beige, documentary grey | Documentary naturalism — subjects filmed in their own environment with their own light; hidden camera and documentary crew; America filmed as Borat sees it | `Borat aesthetic: [SUBJECT] in real America as documentary, grey suit and mankini, inappropriate physical proximity as social investigation tool, genuine American reactions caught on hidden camera, cultural collision as comedy` |
| **C21** | Knives Out (2019) | Vibrant Witty Maximalism | New England autumn ochre, mansion dark mahogany, knife-wheel silver, Benoit Blanc cream | Old dark house gothic warmth; interrogation scenes in practical lamp pools; wide shots for ensemble comedy; close-ups on Blanc's accent performance | `Knives Out aesthetic: [SUBJECTS] in New England Gothic mansion, autumn ochre and dark wood palette, knife wheel overhead shot, Blanc's Southern detective gentleness, Marta's vomiting tell, family entitlement exposed, donut hole metaphor` |
| **C22** | Four Weddings and a Funeral (1994) | Grounded Naturalistic Melancholy | English grey sky, wedding white, country house muted green, funeral black, London brown brick | English diffused overcast as default; wedding venues in romantic warm uplighting; funeral in cold grey light; ensemble staging with wide coverage | `Four Weddings aesthetic: [SUBJECTS] in English wedding circuit, diffused overcast light, Grant's stammering charm, MacDowell's American directness, funeral bringing Auden's elegy, rain-soaked anti-proposal as most romantic speech` |
| **C23** | Blazing Saddles (1974) | Stylized Deadpan & Absurdist | Western desert tan, Wild West saloon amber, Warner Bros backlot generic | Western genre lighting conventions played straight while absurdity erupts; Mel Brooks's vaudevillian precision; the film that breaks its own fourth wall at climax | `Blazing Saddles aesthetic: [SUBJECT] in Western parody, Rock Ridge as generic Western town, campfire flatulence played deadpan, Black sheriff's cool competence against stupid prejudice, fourth wall shattered into Warner Bros musical finale` |
| **C24** | Home Alone (1990) | Bright High-Key Commercial | Christmas warm red and green, suburban house yellow light, Chicago winter white | Christmas movie golden interior light vs blue winter exterior; kid's POV framing; trap sequences with broad physical comedy; Old Man Marley in warm amber church light | `Home Alone aesthetic: [SUBJECT] in Chicago Christmas suburb, warm holiday interior light, eight-year-old's autonomy fantasy, paint can pendulum and blowtorch traps, aftershave slap scream, Kevin's competence and Marv's suffering` |
| **C25** | The Favourite (2018) | Stylized Deadpan & Absurdist | Palace candlelit amber, powdered white wig, garden green, dark wood mahogany, blood and mud | Candlelight only for period-accurate interiors; fisheye wide-angle for distorted court perspective; low angles making characters loom; Lanthimos's characteristic formal distance | `The Favourite aesthetic: [SUBJECTS] in 18th century English court, candlelit amber chiaroscuro, fisheye distortion of power, duck races as political ritual, Queen Anne's gout-swollen vulnerability, Abigail's rising heel and rabbit-seeking foot` |
| **C26** | The Princess Bride (1987) | Bright High-Key Commercial | (Also covered at C17 above — included in both film analysis JSONs) | `Princess Bride aesthetic: [SUBJECTS] in fairy tale Florin, storybook warmth, sword duels as conversation, Inigo's lifelong revenge, true love as the most powerful force in the universe` |

### Dramedy Series Entries (Expanded)

| # | Series | Archetype | Palette | Lighting & Camera | Scene Formula |
|---|--------|-----------|---------|-------------------|---------------|
| **D14** | Schitt's Creek (2015-2020) | Vibrant Witty Maximalism | Small town beige, Rosebud motel salmon, Alexis fashionista colour, David's all-black | Warmly lit for emotional scenes; motel room as intimate comedy stage; town exteriors in Canadian naturalism; character close-ups for reaction comedy | `Schitt's Creek aesthetic: [SUBJECTS] in small town motel poverty, Rose family performance surviving wealth-stripping, Moira's theatrical gesture armour, David's arms-crossed self-protection learning to open, community as unexpected home` |
| **D15** | Abbott Elementary (2021-) | Grounded Naturalistic Melancholy | School institutional beige, Philadelphia brown brick, classroom primary colours, copy machine grey | Documentary naturalism — school fluorescents, no glamourising; mockumentary talking-heads; wide shots capturing ensemble teacher dynamics; beauty in institutional stubborn reality | `Abbott Elementary aesthetic: [SUBJECTS] in underfunded Philadelphia school, fluorescent institutional light, mockumentary teacher interviews, Janine's forward-leaning optimism, Barbara's veteran stillness, Melissa's Philadelphia realness` |
| **D16** | Arrested Development (2003-2019) | Stylized Deadpan & Absurdist | Orange County beige privilege, banana stand yellow, model home incomplete | Documentary naturalism; narrator-driven callbacks requiring visual echoes; aerial shots of Bluth community geography; the Bluth house always slightly wrong | `Arrested Development aesthetic: [SUBJECTS] in Orange County privilege, model home suburb, documentary narrator framing the densest joke construction on TV, Tobias's acting-theory body language, Gob's unearned confidence` |
| **D17** | Curb Your Enthusiasm (2000-2024) | Grounded Naturalistic Melancholy | LA outdoor white, restaurant interior warm, golf course green, Larry's khaki and blue | Perpetual Southern California outdoor light; no special lighting — comedy needs no atmosphere; improvisation-responsive wide coverage; zoom-ins on Larry's dismay | `Curb Your Enthusiasm aesthetic: [SUBJECT] in LA social navigation, perpetual outdoor Californian light, Larry's minimal affect missing every social cue, documentary intimacy of social contract violation, refusal of polite fiction` |
| **D18** | Hacks (2021-) | Vibrant Witty Maximalism | Las Vegas neon excess, Deborah's white and gold, Ava's millennial minimal, comedy club spotlight | Vegas stage lighting as Deborah's habitat; intimate close-ups for writers' room confrontations; road-trip handheld for middle seasons; showbiz wide shots for performances | `Hacks aesthetic: [SUBJECTS] in comedy industry, Vegas neon stage lighting, Deborah's showbiz-perfected posture, Ava's millennial chaos, desert road between generations, female creative partnership as generational bridge` |
| **D19** | What We Do in the Shadows (2019-2024) | Stylized Deadpan & Absurdist | Staten Island grey, vampire crimson, documentary neutral, Manor dark wood, supernatural purple-black | Documentary naturalism applied to vampires — candlelight and coffin-sleeping with BBC neutrality; camera witnesses the unreportable; ancient power meeting modern bureaucracy | `What We Do in the Shadows aesthetic: [SUBJECTS] in Staten Island vampire manor, documentary-camera neutrality on supernatural activity, 800-year-old warrior confused by DoorDash, familiar yearning to be vampire, Laszlo's aristocratic confusion` |
| **D20** | Enlightened (2011-2013) | Grounded Naturalistic Melancholy | Hawaii healing blue-green, corporate office beige, Amy's white awakening wardrobe | Hawaii in transcendent golden light vs corporate office in clinical fluorescence — the journey between these two lighting states; intimate documentary close-ups of Dern's face | `Enlightened aesthetic: [SUBJECT] in spiritual awakening vs corporate reality, Hawaii transcendent light vs office fluorescence, Amy's explosive physical openness read as mania or vision, reformer as comedy and hero simultaneously` |
| **D21** | Insecure (2016-2021) | Grounded Naturalistic Melancholy | Inglewood neighbourhood warm, LA sun gold, party neon, apartment intimate amber | Issa Dee's world warmed with Black Los Angeles light; Molly's law firm in cool corporate contrast; mirror rap sequences as formal signature; wide shots of South LA as love letter | `Insecure aesthetic: [SUBJECTS] in Inglewood LA, warm Black neighbourhood light, mirror rap as internal dialogue, Issa's self-underestimating physicality, Molly's professional precision failing in love, female friendship as central relationship` |
| **D22** | Better Things (2016-2022) | Grounded Naturalistic Melancholy | LA home warm gold, kitchen morning light, backyard California green | Home lighting as emotional grammar — kitchen morning vs bedroom night; observational patience, long takes, naturalism over flattery; children at their own eye level | `Better Things aesthetic: [SUBJECT] in LA family home, kitchen morning light as emotional grammar, working-mother perpetual motion, Pam Adlon's radical naturalism, motherhood without sentimentality, living daughters as real family` |
| **D23** | Catastrophe (2015-2019) | Grounded Naturalistic Melancholy | London grey everyday, apartment functional warm, Irish family home comfortable | Naturalistic throughout — no romantic lighting for an unromantic love story; two-shot preference emphasising couple-as-unit; handheld documentary aesthetic of real relationship | `Catastrophe aesthetic: [SUBJECTS] in London couple's reality, naturalistic unromantic light, accidental love made deliberate through daily imperfect choice, Rob's American sincerity, Sharon's Irish emotional restraint cracking open` |
| **D24** | Extras (2005-2007) | Grounded Naturalistic Melancholy | Film set grey-beige, extras' waiting area fluorescent, celebrity dressing room warm | Behind-the-scenes film set lighting; documentary style with celebrity cameos as genuine on-set footage; Andy's embarrassment requires close-up coverage | `Extras aesthetic: [SUBJECT] in film industry margins, fluorescent extras holding area vs warm celebrity trailer, Andy's cringe management, celebrity cameos' self-parody, fame's Faustian bargain as tragicomedy` |
