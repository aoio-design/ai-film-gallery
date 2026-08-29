---
name: ai-film-scriptwriting
description: "Scriptwriting for AI short films and micro-dramas (30s–5min), short films (5–15min), and drama series (3–6 episodes × 10–12min). Covers loglines, reveal architecture, correction patterns, multi-season lore planning, and reveal-architecture for mystery and sci-fi series. Outputs formatted screenplays optimized for AI production pipeline."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [scriptwriting, screenplay, micro-drama, short-film, storytelling, dialogue]
    related_skills: [ai-film-pipeline, ai-film-prompt-engineering]
---

# AI Film & Micro-Drama Scriptwriting

## Overview

Scriptwriting for **short form** content (30 seconds to 5 minutes), **short films** (5–15 minutes), and **drama series** (3–6 episodes × 10–12 minutes each) produced via AI generation. Unlike feature films, micro-dramas need **every second to count** — minimal scenes, maximum impact. Series work needs **reveal architecture** — carefully controlling what the audience learns when. This skill covers ideation through finished screenplay, optimized for the AI film pipeline (FLUX images → MiniMax H3 Max clips with dialogue).

## When to Use

- The user wants to develop a new concept or logline
- The user needs a screenplay for a micro-drama
- Breaking down a script into shot-by-shot scenes
- Writing dialogue that the video model will speak (the line goes in the clip's prompt)
- Adapting an existing story into short-form format
- Any script-related creative work for the pipeline

## Micro-Drama Lengths & Structures

### Duration Templates

| Length | Scenes | Structure | Best For |
|--------|--------|-----------|----------|
| **15-30s** (Short) | 1-2 scenes | Hook → Payoff | Teasers, social clips |
| **30-60s** (Micro) | 2-3 scenes | Setup → Conflict → Twist | TikTok/Reels dramas |
| **1-3 min** (Short) | 3-5 scenes | Inciting → Rising → Climax → Resolution | YouTube shorts, episodes |
| **3-5 min** (Mini-ep) | 5-8 scenes | Full 3-act compressed | Episode 1 pilot |

### Structure Selection by Duration

Pick the right structure for your target runtime:

| Duration | Structure | Scenes | Pacing Density |
|----------|-----------|--------|----------------|
| **15-30s** (Teaser) | Hook → Payoff | 1-2 | Maximal — every second is a beat |
| **30-60s** (Micro) | Setup → Conflict → Twist | 2-3 | High — 1-2 beats per scene |
| **60-120s** (Short micro-drama) | 4-Scene (below) | 3-4 | Moderate — scenes have room to breathe |
| **3-5 min** (Mini-episode) | 3-Act Compression (below) | 5-8 | Relaxed — full act structure with pacing waves |
| **5-15 min** (Short film) | Full 3-Act | 8-15 | Varied — build, sustain, release cycles |

### Standard 4-Scene Structure (for 60-120s Micro-Dramas Only)

This structure is tightly calibrated for **60-120 second** episodes. Do NOT use it for longer films — the pacing will feel rushed and scenes won't have room to breathe. For 3+ minute films, use the 3-Act Compression or Full 3-Act structure below.

| Scene | Time | Purpose | Key Element |
|-------|------|---------|-------------|
| 1 | 0-30s | Hook & Setup | Inciting incident in first 5 seconds |
| 2 | 30-60s | Development | First complication |
| 3 | 60-90s | Escalation | Key revelation/twist |
| 4 | 90-120s | Resolution + Cliffhanger | Partial resolution, forward hook |

### The 3-Act Compression (for 3-5 Minute Mini-Episodes & Short Films)

For longer works, each act contains multiple scenes with their own mini-arc. The pacing is **wave-based** rather than linear — tension builds, crests, settles, then builds again.

```
ACT I  (25% of runtime) — Establish
  ─ Scene 1: Hook (grab attention in 3-5 seconds)
  ─ Scene 2: Character introduction + world

ACT II (50% of runtime) — Complicate
  ─ Scene 3: Conflict escalates
  ─ Scene 4: Low point / revelation

ACT III (25% of runtime) — Resolve
  ─ Scene 5: Climax / twist
  ─ Scene 6: Resolution with lingering question
```

For sub-60s: compress to **Hook → Conflict → Twist** in 2-3 scenes.

### Logline Formula

```logline
When [PROTAGONIST] wants [GOAL] in [SETTING],
but [OBSTACLE] stands in their way,
they must [ACTION] before [STAKES] or lose [CONSEQUENCE].
```

### Title Construction: The Triple-Meaning Principle

The most powerful series titles operate on **three levels** — diegetic, thematic, and symbolic. Each meaning reveals itself at a different stage of the audience's journey.

| Level | When the Audience Gets It | Example: a one-word mystery title |
|-------|--------------------------|-------------------|
| **Diegetic** (in-world) | Mid-season reveal (Ep 4) | The word scrawled at the centre of the missing professor's investigation board, in red |
| **Thematic** (what the story is about) | End of season (Ep 6) | What the system demands — the endless cycle the characters are trapped in |
| **Symbolic** (the antagonist's identity) | Final reveal + rewatch | The name of the force that has been pulling strings all along |

**Validation:**
- The title should work as a *noun* (who they are), a *verb* (what they do), and a *command* (what the system demands)
- A good test: a viewer who watched the whole season should say "OH, that's what the title means" — and a rewatcher should see new layers

**Cheeky romance example:** *"When a jaded detective discovers his new AI assistant is programmed to find him love instead of solving crimes, he must teach her what real human connection means before his promotion—and his heart—slips away forever."*

**Sci-fi mystery example:** *"In a colony on Europa where memories can be traded like currency, a rookie archivist discovers someone is erasing her own past—one citizen at a time."*

## Screenplay Format (Pipeline-Optimized)

Standard screenplay format adapted for AI generation. Each scene maps to one video clip. We use a **markdown hybrid** that's both human-readable and easy for me to generate, but we can also output in **Fountain** format for interoperability with professional screenwriting tools.

### Primary Format: Markdown Hybrid

```markdown
# PROJECT: [Title]
LOGLINE: [One sentence]
GENRE: [Primary / Secondary]
TONE: [Mood keywords]
TOTAL DURATION: [Time]

---

## SCENE 1 — TITLE

INT./EXT. — LOCATION — TIME OF DAY

[Atmosphere / lighting description in 1 sentence]

CHARACTER A
(line direction)
Dialogue line here.

CHARACTER B
(line direction)
Response dialogue here.

> CAMERA: Medium two-shot, slow dolly in
> TRANSITION: Dissolve to next scene
> DURATION: ~15 seconds
> SFX: [sound effects needed]
> MUSIC: [music mood for the video prompt]
```

### Alternative: Fountain Format (Interoperability)

[Fountain](https://fountain.io) is a plain-text screenplay markup language compatible with Final Draft, Fade In, and Highland. I can output scripts in Fountain format for the user to import into professional screenwriting tools.

```fountain
Title: Project Title
Author: [Your Name]
Draft: 1
Date: 2026-06-22

**SCENE ONE**

INT. APARTMENT - NIGHT

A dimly lit room, moonlight streaming through venetian blinds,
casting striped shadows across the floor.

KAI
(whispering)
I found it. The notebook.

RIN
(skeptical)
Are you sure it's the right one?

> CAMERA: Slow dolly in on Kai's face
> DURATION: ~15 seconds
```

**Fountain rules:** Scene headings in ALL CAPS, Character names in ALL CAPS before dialogue, transition in ALL CAPS, notes/comments in `[[brackets]]`.

### Key Rules for AI-Produced Scripts

1. **Dialogue must sound natural when spoken aloud** — short sentences, avoid homophones, spell out numbers ("twenty-four" not "24")
2. **Scene descriptions are ALSO image prompts** — each description must be visual enough to feed directly into FLUX
3. **Camera direction is mandatory per scene** — the video model needs to know what kind of camera movement to generate
4. **Keep dialogue minimal in action-heavy scenes** — the model lip-syncs one speaker per clip, so dialogue works best in static close-ups, or as voiceover over scenes where the character is not speaking on-screen

## 5-Beat Structure for Micro-Dramas

| Beat | % | What Happens |
|------|---|-------------|
| **Hook** | First 5s | Grab attention — visual spectacle, mysterious image, intriguing line |
| **Context** | 15% | Show world, character, what's normal |
| **Inciting Push** | 30% | Something disrupts the normal — a discovery, a visitor, a message |
| **Rising Complication** | 35% | The problem gets worse, stakes clarify |
| **Twist / Reveal** | Remaining | Payoff — the answer, the betrayal, the kiss, the punchline |

## Dialogue Writing for the Video Model

Since dialogue is spoken by the video model itself (MiniMax H3 Max — the line
goes in quotes inside the clip's video prompt, with a delivery tone):

**DO:**
- Short sentences (15 words or fewer per line)
- Contractions → "I'm" not "I am", "can't" not "cannot"
- Spell out numbers → "thirty seven" not "37"
- Use phonetic spelling for unusual names → "Ky-ra" for Kyra
- Add parentheticals for tone → (whispering), (sarcastic), (urgent)

**DON'T:**
- Avoid long monologues (>30 words without a break)
- Avoid dense dialect or heavy accents (the model will mangle them)
- Avoid puns that require visual timing (the model can't pause comedically)
- Avoid characters talking over each other (one speaker per clip)

## Character Archetype System (Shorthand)

For rapid micro-drama development, use initial-based character archetypes. Each archetype has defined voice traits:

| Initial | Role | Purpose | Dialogue Style |
|---------|------|---------|----------------|
| **A** | Protagonist (POV) | Drives the story, makes choices | Conversational, emotional, full sentences |
| **B** | Catalyst / Antagonist | Creates change, challenges A | Short punchy lines, fragments, creates questions |
| **C** | Supporting | Provides info, creates complications | Functional dialogue, brief appearances |
| **M** | Mother / Authority | Advice, conflict | Concerned, wise, grounded |
| **F** | Friend | Support, comic relief | Casual, encouraging, light |
| **R** | Rival | Competition, tension | Sharp, competitive, clipped |

**Rules:**
- Keep cast small (2-5 characters per episode)
- Each character has one of: a surface WANT, an internal NEED, and an OBSTACLE
- Voice patterns stay consistent throughout the episode
- Physical actions align with character profile

## Pacing Framework: Hook by 5 Seconds (for Micro-Dramas Under 2 Minutes)

This framework is calibrated for **60-120 second** micro-dramas. Every second is accounted for. For longer films (3+ minutes), see the pacing section below.

```
0-5s:     HOOK — Grab attention immediately (visual spectacle, intriguing line)
0-10s:    HOOK+SETUP — Establish premise, introduce characters
10-30s:   SETUP — Introduce characters, establish conflict
30-60s:   DEVELOPMENT — Complications, escalation
60-90s:   COMPLICATION — Peak tension, key revelations
90-120s:  CLIFFHANGER — End on unresolved tension
```

**Scene requirements:**
- Each scene must have a **visual hook** — something visually interesting happens
- Each scene must have **clear purpose** — advances plot OR develops character
- Dialogue must **reveal character/conflict** — not just exposition
- Each scene needs a **clear transition** to the next (physical or emotional)

## Pacing for Longer Films (3+ Minutes)

For works over 3 minutes, pacing follows a **wave-based** architecture rather than a tight timeline. The 5-second hook rule still applies for the opening, but thereafter the rhythm expands to full act structure.

### Timing Calibration

| Duration | Hook Window | Scene Length | Pacing Pattern |
|----------|-------------|--------------|----------------|
| **3-5 min** | First 5-10s | 30-60s per scene | 2-3 tension waves |
| **5-10 min** | First 10-15s | 45-90s per scene | 3-4 tension waves |
| **10-15 min** | First 10-20s | 60-120s per scene | Full 3-act rhythm |

### Tension Wave Principle (for 3+ Minutes)

Instead of a single 90-second arc, longer works use multiple tension waves. Each wave has:
1. **Build** — rising tension, new information, stakes escalation
2. **Crest** — peak moment (revelation, confrontation, decision)
3. **Release** — emotional settling, new direction

```
Wave 1 (0-90s):     BUILD → CREST (inciting incident) → RELEASE (new normal)
Wave 2 (90-180s):   BUILD → CREST (complication) → RELEASE (deeper stakes)
Wave 3 (180s+):     BUILD → CREST (climax) → RELEASE (resolution, lingering question)
```

Each wave spans roughly 1/3 of the runtime for a 3-minute film, or 1/4 for longer works where the middle expands.

### Pacing Density Scale

| Density | Beats per Minute | Feel | Best For |
|---------|-----------------|------|----------|
| **Maximal** | 8-12 | Breathless, urgent | Teasers, 15-30s ads |
| **High** | 4-6 | Punchy, fast | Micro-dramas 30-60s |
| **Moderate** | 2-3 | Natural, engaging | 60-120s micro-dramas |
| **Relaxed** | 1-1.5 | Room to breathe | 3-5 min mini-episodes |
| **Varied** | 0.5-2 | Cinematic rhythm | 5-15 min short films |

For 3+ minute films:
- **Open hot** (first 5-10s hook still applies)
- **Middle acts expand** — Act II is the longest (50% of runtime) with multiple scenes, not just one
- **End with payoff** — the final act wraps the story, not just a cliffhanger
- **Let scenes breathe** — dialogue scenes can run 60-90s, not the 30s micro-drama limit
- **Subplots welcome** — 3+ minutes gives room for B-stories, character beats, and world-building moments

## Scene Transitions

Use standard screenplay transitions between scenes:

```
FADE TO:
```

```
SMASH CUT TO BLACK.
```

```
TRANSITION:
```

For cliffhangers, end episodes with:

```
[beat]

CHARACTER:
Final line that creates intrigue.

[END EPISODE — CLIFFHANGER]
```

Or use text-on-screen:

```
TEXT ON SCREEN: "[Message]"

[END EPISODE]
```

## Banned Content Checklist

Always check generated scripts against this list before delivering:

**Absolute no-go:**
- Graphic violence or gore
- Sexual content or nudity
- Hate speech or discrimination
- Illegal activities promoted
- Dangerous stunts or behaviors
- Real people or real brands
- Medical misinformation
- Self-harm or suicide encouragement

**Platform restrictions (verify per platform):**
- Check current community guidelines (TikTok, Reels, Shorts)
- Avoid political content
- No copyrighted music/lyrics

## Writer's Room Workflow (6-Step Process)

A structured creative development workflow for generating scripts from scratch. Each step builds on the previous.

### Step 0: Clarify-First Methodology

**Before writing a single line, map the concept collaboratively.**

The user often has ideas in bits and pieces. Your job is to ask targeted questions to build a coherent framework before you draft. Do NOT start writing without this step — it prevents wasted work and structural rewrites later.

#### Mandatory Clarify Questions (ask these before any script work):

| Area | Questions |
|------|-----------|
| **Format** | Short film (10–15 min) or series (3–6 episodes × 10–12 min)? Standalone pilot? |
| **Title** | Does the user have one? If not, suggest 3–4 options with reasoning. |
| **Tone** | Slow-burn mystery? Action-thriller? Moody-paranoid? Dark satire? Give reference titles (Arrival, Dark, They Live, The Matrix). |
| **Setting** | Real city? Generic nameless? Fictional? |
| **Protagonists** | Ages, occupations, how they meet, first impressions of each other. |
| **The "Good" Aliens** | Visibly present? Supernatural/angelic encounters? Vision-only? Human avatars? |
| **Ending Vibe** | Hopeful, tragic, open-ended, bittersweet? |
| **Visual Palette** | Cyberpunk-neon, brutalist grey, warm-but-worn, naturalistic/handheld? |

#### Episode/Scene Structure Questions (for series):

- How many episodes? (3–6 is the sweet spot for tight AI-produced series)
- What does each episode's audience learn? (the **reveal timeline** — see Reveal Architecture below)
- Where is the season cliffhanger? (mid-season, end-of-season, or both)
- Which revelations are saved for which episode? (never front-load a series)

#### Acceptable Starting Points

It IS acceptable to start the conversation by asking ALL clarifying questions in a single batch, then proceeding once the user confirms the framework. The user has explicitly stated they prefer being asked clarifying questions before work begins — lean into this.

### Step 1: Workspace Scan & Constraint Extraction
Read all reference materials (style guide, script format, character sheets, example episodes, locations). Produce a comprehensive summary of constraints:
- Tone & style guidelines
- Script format requirements
- Content constraints
- Example episode analysis

### Step 2: Premise Development
Generate **3 distinct episode premises**, each with:
- **Logline**: One-sentence hook (max 20 words)
- **Genre**: Romance, Thriller, Comedy, Drama, Sci-Fi, etc.
- **Setting**: Where the story takes place
- **Core Conflict**: Central tension or problem
- **Character Pairing**: Who drives the story
- **Episode Hook**: What creates intrigue (first 10 seconds)
- **Cliffhanger**: What makes viewers want the next episode
- **Episode Structure**: Scene breakdown with timing
- **Tone**: Emotional, Tense, Uplifting, Dramatic
- **Tropes**: 2-3 genre tropes used

Recommend one option and justify why it best fits the style guidelines.

### Step 3: Episode Beats & Outline
Create a detailed beat sheet with:
- **Working Title**: Catchy 3-5 words
- **Scene-by-scene breakdown**: Duration, location, characters, purpose, visual hook, dialogue start
- **Pacing notes**: Rhythm of dialogue vs. action, where to accelerate, where to pause
- **Dialogue guidelines**: Speech patterns per character, key lines, phrases to avoid
- **Arc notes**: How this episode fits the larger story, character development moments

### Step 4: Script Draft Generation
Write the complete episode script following the format from SCRIPT_FORMAT.md. Quality standards:
- Every scene advances plot or character
- Dialogue reveals character and advances conflict
- Visual storytelling in action lines
- Clear emotional arc within episode
- Strong cliffhanger that demands a follow-up

### Step 5: Production Artifacts
Generate support materials:
- **Cast sheet**: Characters with descriptions, personality traits, arc notes
- **Writers Room Dashboard**: HTML artifact summarizing episode development (see reference template)

### Step 6: Cohesiveness Review (Post-Draft)

After ALL episodes are drafted (not before), run a structured continuity pass. This catches logical breaks that individual episode editing misses.

#### 6A: Timeline Verification

Build a chronological timeline of the entire season. For multi-episode series taking place over 1-3 days, verify:

- **Duration**: How many days/hours elapse across the season?
- **Episode-to-episode transitions**: Does each episode start at a logical time offset from the previous?
- **Character availability**: Can a character who was in one location at the end of Ep N realistically be in a different location at the start of Ep N+1?
- **Reveal timing**: Was the Ep 6 reveal accidentally telegraphed in Ep 2? (Check for front-loading.)

**Common timeline breaks found in practice:**
- A character describing themselves as "watching a location for weeks" in Ep 6 when they were actively street-preaching in Ep 2 (the previous day). Fix: align the explanation with the actual elapsed time.
- A flashback slugged "three weeks ago" when the protagonist said the mentor vanished "a week ago" in Ep 1. Fix: harmonise dates across all references.
- A false-alarm door creak in Ep 5 that's never explained in Ep 6. Fix: ensure the Ep 6 character's entry method resolves the ambiguity.

#### 6B: Edit Cascade Check

Every screenplay edit to Ep N may require updates to:
- Ep N's **production notes** section
- Ep 1's **appendix / series outline** (if the edit changes series-wide facts)
- Any **reference documents** (episode guides, character sheets, story bible)
- Earlier episodes' **character arc notes** if the edit retcons backstory

**The cascade pattern:** User approves a change → patch the target episode → immediately check and patch the appendix + production notes + references. Do not wait for a separate request.

#### 6C: Cross-Episode Logic Audit

For each logical issue found, produce a table:

| Issue | Ep N vs. Ep M | Severity | Description | Fix |
|-------|---------------|----------|-------------|-----|
| Concise label | The two clashing elements | 🚨 Critical / ⚠️ Medium / ℹ️ Low | What the audience will notice as a contradiction | Specific, actionable fix recommendation |

**Validation:** After implementing all fixes, the entire season should be watchable without the audience noticing any timeline or continuity glitches. If a fix hasn't been approved, the issue stays in the output so the user can decide.

#### 6D: Runtime vs. Target Check

For each episode, estimate screen time using the screenplay-line standard (~1 page ≊ 1 minute for formatted scripts; for markdown hybrid scripts, count scenes × density). Compare against the target runtime per episode (e.g., ~10 min). Flag episodes 2+ minutes under or over for structural additions, not just dialogue padding. Proven additions: B-plot flashbacks, POV vision sequences, solo investigative montages, cold opens.

### Step 7 (if needed): Targeted Patches from Review

When implementing fixes from the cohesiveness review, follow the Edit Cascade Check (6B) — fix the episode AND its dependencies in a single pass. Batch independent patches together across files. Never implement only half a fix.

## Sub-Scene Breakdown (1A, 1B, 1C...)

For AI film production, each script scene is broken into **sub-scenes** — one per camera angle/shot size. Each sub-scene becomes a single clip generated from its first-frame keyframe.

### Scene → Sub-Scene Mapping

| Script Scene | Sub-Scenes | Camera Progression |
|-------------|------------|-------------------|
| Opening/Establishing | **1A**: Wide establishing shot | Sets location and mood |
| | **1B**: Medium two-shot | Character interaction |
| | **1C**: Closeup | Reaction, emotional beat |

### Sub-Scene Card Format

Each sub-scene is a single studio shot card containing:
- **1 image** (the first-frame keyframe)
- **Description** with the keyframe prompt, camera direction, and character/set references

```
Card: 🎬 Scene 1A — The Archive (Wide)

Description contains:
  First Frame: Wide shot of the archive chamber. Rows of server racks
    stretch into darkness. The protagonist sits at a console, small against the scale.
    
  Last Frame: Closeup on the protagonist's face as realization dawns.
    The blue holographic light plays across his features.
    
  CAMERA: Wide → slow dolly to closeup
  Characters: Protagonist (contact enters, exits)
  Set: Archive Chamber
  Lighting: Cold overhead blue, faces half in shadow
  Shot size: Wide establishing → closeup
```

### Sub-Scene Template

```markdown
Card: 🎬 Scene [N][Letter] — [Scene Title] ([Shot Type])

First Frame: [Describe the opening shot — be specific about composition,
character position, lighting, what's in frame]

Last Frame: [Describe how the scene changes — character movement,
expression shift, camera push, new element entering frame]

CAMERA: [Shot size progression, e.g. "Wide → medium two-shot"]
Characters: [Who is in this sub-scene]
Set: [Which approved set reference to use]
Lighting: [Lighting description for prompts]
Shot size: [Progression of shot sizes]
```

### Why Break Into Sub-Scenes?

1. **The video model generates 3-6 second clips** — each sub-scene is one clip
2. **Different shot sizes = different prompts** — wide establishing shots need different composition than closeups
3. **Review granularity** — the user can approve/reject individual camera angles without redoing the whole scene
4. **Consistency** — each sub-scene references the same approved character + set assets from the consistency tracker

| Trope | Why It Shines | Example Prompt Angle |
|-------|--------------|---------------------|
| **Neon noir cityscapes** | Flux excels at cyberpunk environments | "Rain-slicked streets, holographic billboards" |
| **Android / AI characters** | Uncanny valley works in your favor | "Flawless synthetic skin, LED iris" |
| **Alien landscapes** | No real-world reference needed | "Bioluminescent flora, twin suns" |
| **Memory / VR sequences** | Abstract visuals are forgiven | "Glitchy reality, digital artifacts" |
| **Minimalist sci-fi** | Clean backgrounds = easier for AI | "White sterile room, single light source" |

## Mystery Tropes That Work Well

| Trope | Why It Shines |
|-------|--------------|
| **Clues as visual objects** | Strong first/last frame contrast: find → reveal |
| **Interrogation scenes** | Static two-shot = easy for the video model, dialogue-heavy |
| **Surveillance footage aesthetic** | Grainy low-res hides AI imperfections |
| **Red herrings in background** | Flux puts unexpected details in frame naturally |

## Cheeky Romance Tropes

| Trope | Why It Shines |
|-------|--------------|
| **Enemies to lovers banter** | Dialogue-driven, light on action |
| **Misunderstanding comedy** | Relies on reaction shots (two frames) |
| **Near-miss encounters** | "Almost kiss" moment — strong first/last frame |
| **Text messages on screen** | Overlay text, no voice acting needed |

## SF New Wave Core Principles (Structural)

When developing sci-fi concepts, these core principles from the SF New Wave movement (Ballard, Moorcock, and *New Worlds* magazine, 1960s-70s) provide a structural/philosophical foundation. These are **principles of approach**, not content tropes — they shape *how* you tell the story, not *what* the story is about.

### Principle 1: Inner Space Over Outer Space

Ballard's central thesis: **"The only truly alien planet is Earth."**

Science fiction doesn't need to go to the stars to find the extraordinary — it's right here, in the psychological landscape. The most powerful sci-fi explores:
- The alien within (consciousness, identity, memory)
- The strangeness of the everyday (technology's invisible transformation of ordinary life)
- Psychological and subjective reality as the primary frontier

> **How to apply:** Before adding a space-ship or alien planet, ask: *What would this story look like if the extraordinary happened in a familiar setting?* The familiarity makes the strangeness land harder.

### Principle 2: Content Expansion Beyond Technology

Golden Age SF privileged technological speculation — gadgets, space travel, physics. The New Wave expanded what SF could be about:
- **Sexuality, identity, and the body**
- **Social isolation and alienation in a connected world**
- **Eco-catastrophe and environmental collapse**
- **Entropy** — systems breaking down, heat death, decay as narrative force
- **Class structures and social systems**
- **Psychological states**: obsession, paranoia, grief, dissociation

> **How to apply:** Identify your story's core tension — is it about a technology, or is it about a *condition* (loneliness, surveillance, inequality) that technology amplifies? The latter is always richer.

### Principle 3: Theme Over Plot as Primary Engine

The New Wave prioritised **situation and theme** over conventional plot mechanics. A story could be about a state of being rather than a sequence of events.
- The setting *is* the story — the environment functions as a character
- Characters exist to explore an idea, not just to execute a plot
- Mood, atmosphere, and texture can be the primary payload

> **How to apply:** Start with a what-if question about *the human condition*, not about *technology*. "What if memory could be erased?" is an idea about grief, not about a machine.

### Principle 4: Formal Experimentation

The New Wave brought modernist and postmodernist literary techniques into SF:
- Non-linear narrative structures
- Unreliable narrators and multiple perspectives
- Stylised, dense, or poetic prose over transparent storytelling
- Fragmentation — stories as collage, cut-up, or found-document format
- Language as a primary element, not just a vehicle for plot

> **How to apply:** For AI film, this translates to: vary your visual language between scenes, use non-linear reveals, let the audience piece together meaning from visual fragments rather than exposition.

### Principle 5: The Alien is Already Here

Ballard's "condensed novels" transformed mundane settings into sites of the surreal. The extraordinary doesn't announce itself — it *leaks* into the everyday:
- A crashed UFO is less interesting than the suburban family pretending the UFO didn't crash
- The alien invasion is less interesting than the humans who adapt to it without noticing
- The technology is less interesting than how people *feel* about the technology

> **How to apply:** Set your most "impossible" events in the most mundane possible locations. A kitchen, a waiting room, a parking lot. The contrast creates more resonance than another gleaming spaceship corridor.

### Principle 6: Rejection of Optimistic Progress

New Wave SF is fundamentally suspicious of "technology will save us" narratives. Stories are more compelling when:
- Technology creates as many problems as it solves
- Progress comes with a human cost that's not evenly distributed
- Solutions are ambiguous, temporary, or morally compromised
- The future is not better — just *different*, and often stranger

> **How to apply:** When your story's technology solves a problem, make sure it creates a new, more interesting problem in the process. The cost of the solution IS your story.

### Relationship to the Existing Archetype System

These principles are **most compatible with** the sci-fi archetypes already defined in `ai-film-cinematography`:
- **Grounded Speculative Realism** — inner space, everyday alienation, psychological focus
- **Industrial Grunge & Retrofuturism** — systems breaking down, entropy, working-class perspective
- **Clinical Corporate Dystopia** — social systems as the alien environment, class as science fiction

And **least compatible with**:
- **Maximalist Space Opera** (which relies on the very conventions — galactic wars, interstellar travel — that the New Wave explicitly rejected)

## Directing & Storytelling Techniques (From Lee Chang-dong / Burning)

Lessons from one of cinema's most respected directors, applied to AI film production.

### 1. Trust the Audience
Don't hold hands. Don't over-explain. Viewers don't need constant reminders of every plot point.

**In our pipeline:** If a character's motivation is clear from their actions, don't add dialogue explaining it. Let the FLUX-generated expression and body language carry the meaning.

### 2. Deliberate Ambiguity — "No Answers on Purpose"
The most powerful mysteries don't solve themselves. Leave deliberate gaps.

**In our pipeline:** The last frame of a scene can show a character's reaction without revealing what they saw. The audience fills the gap.

### 3. Emotional Restraint — Pull Back Before the Climax
Lee's AD reminded him: *"We restrain things right before the audience is emotionally moved."*

**In our pipeline:** If a scene builds to a dramatic reveal, the last frame should be the **moment before** the reaction — not the reaction itself. The audience imagines it more powerfully than we could show.

### 4. The Unreliable Narrator
Tell the story through a biased perspective. The audience only has the information the protagonist has.

**In our pipeline:** If the protagonist discovers the AI's deception, we should only see what the protagonist sees. Don't cut away to show the AI scheming in another room. We're trapped in their perspective.

### 5. Visual Storytelling — No Internal Monologue
Lee avoids literary tools like voiceover narration. He tells the story visually.

**In our pipeline:** Instead of the protagonist saying "I knew something was wrong," show them: frozen mid-step, eyes locked on the data, hands hovering over the keyboard. Let the image do the work.

### 6. Blur Fantasy and Reality — No Cuts Between Them
Lee doesn't signal when a scene shifts from reality to imagination. No wavy transitions. No sound cues.

**In our pipeline:** If the protagonist imagines a loved one in the hospital, don't add a dreamy dissolve. Cut directly. The audience should question: is this real or memory?

### 7. Emptiness as a Tool — "Forget That It Isn't There"
Hae-mi's invisible tangerine: *"What's important is not to believe something is there, but to forget that it isn't."*

**In our pipeline:** An empty chair where a character should be. A phone that rings with no one on the other end. A locked door. Let the absence tell the story.

### 8. Sustained Tension — The Horizontal Crawl
Instead of building tension progressively (standard 3-act climb), keep tension sustained on a flat line that suddenly spikes at the end.

**In our pipeline:** Scene 1A through 4B maintain a quiet, simmering tension. Then Scene 5A-5B spikes. Don't escalate too early.

### 9. Remove Expected Elements
Lee removes: internal monologue, the body, proof of crime, confrontation. 

**In our pipeline:** If the script calls for a confrontation scene, consider removing it. Instead show the **aftermath** — a character sitting alone, processing what just happened off-screen. The audience imagines the confrontation more vividly than we could generate.

### 10. The Uncanny — Something Familiar and Strange
Ben is perfectly polite but always feels slightly off. His American-ness in a Korean body creates dissonance.

**In our pipeline:** The AI should be warm and helpful — but hold its smile a beat too long. Use slightly unnatural symmetry in its holographic form. The viewer should sense something is wrong without being able to name it.

### 11. Male Lack — Repressed Obsession
Lee's male characters are trapped between childhood and adulthood. They are dysfunctional, obsessed, and their obsession leads to self-destruction.

**In our pipeline:** The protagonist's grief isn't just sadness — it's a fixation. Show them replaying the same memory over and over. The repetition itself tells the audience he's trapped.

### 12. The Blank Page — Creative Block
Jong-su can't write. The paper is blank. This emptiness is the central metaphor.

**In our pipeline:** If a character stares at a blank screen, an empty notebook, an unfinished sentence — this visual communicates more about their internal state than any line of dialogue.

### Applying These to a Mystery Series

| Scene | Lee Chang-dong Technique |
|-------|-------------------------|
| 1A — Archive (Wide) | **Emotional restraint** — the protagonist notices the anomaly but doesn't react dramatically. Just a pause. |
| 2B — Memory | **Blur fantasy/reality** — No dissolve between the apartment and the hospital memory. Direct cut. |
| 3B — Revelation | **Remove expected elements** — We don't see the companion leave. Just the protagonist alone in the corridor. |
| 4B — The AI reveal | **The uncanny** — The AI's warmth should feel a fraction too perfect. |
| 5B — Final moment | **Sustained tension → spike** — No big fight. Just guards entering, the protagonist not running. |
6. **Shipping episodes with runtime gaps** — After drafting all episodes, analyze each against the target runtime (see `references/runtime-analysis.md`). An episode 3+ minutes under target needs structural additions, not just dialogue padding. B-plot flashbacks, POV vision sequences, and solo investigative montages are the proven fixes.
7. **Giving a protagonist full knowledge too early** — A witness who wakes up with complete clarity in Episode 5 has nowhere to go. Fragmentary recall (partial images, no timeline, no instructions) creates productive tension and earns the final reveal. The full picture should be assembled across multiple characters and episodes — never downloaded in one seizure.

8. **Edit cascade omission** — Changing a scene in Ep N often requires updates to Ep 1's appendix, production notes in the same episode, and any reference documents. After every approved edit, check all downstream files before moving on. The most common miss: patching the target episode but leaving the series outline appendix in Ep 1 with the old version.

9. **Unresolved false alarm** — A door-creak or scraping sound from an Ep 5 cliffhanger that's never addressed when the character enters in Ep 6 feels like cheap tension. Ensure the entry method in the later episode (front door vs. window) logistically resolves the sound from the earlier episode.

10. **Redundant information exchange across adjacent scenes** — A character who asked "Where's your lab?" in Scene 1 should not ask again in Scene 2 if no time has passed and they've been walking together. Check every question against what was already established in the same timeline. Characters should act like they remember the last 15 minutes.

11. **Implausibly fast off-screen actions without acknowledgment** — When a character says "they cleared out the office in 3 days" or similar implausibly swift administrative action, the other character should remark on it. Otherwise the audience notices the pacing hole before the characters do. Turn the implausibility into a planted mystery rather than leaving it as a plot hole.

12. **Unearned pre-recorded-history dates** — When referencing dates that predate recorded history (before ~3,400 BC), the character citing them must acknowledge how they know. If a professor's notes contain dates older than recorded history, the protagonist should say "That's before writing. I don't know how he found those dates." The source of the dating is itself a clue — don't present it as accepted fact.

## Black Mirror Style Guide (For the User's Micro-Dramas)

For Black Mirror-style sci-fi projects, key elements of the style:

### Story Structure
- **Near-future technology** — One speculative technology per story (neural memory implants, AI therapists, etc.)
- **Personal stakes** — Technology affects 2-3 characters intimately, not society at large
- **Moral ambiguity** — No clear villain; the technology itself is neutral, human nature is the problem
- **Chilling reveal** — Third act twist that recontextualizes everything before it
- **Ambiguous ending** — Not a happy ending, not a sad ending, a *thought-provoking* one

### Dialogue Style
- **Naturalistic but precise** — Characters speak like real people but every line serves the theme
- **Minimal exposition** — Show the tech through use, not through explanation
- **Subtext** — Characters say one thing but mean another, especially in scenes with the AI/company rep

### Visual Language (AI-Produced)
- **Cold color palette** — Teal, blue, desaturated greens. Warm colors only for "fake" happy memories
- **Clinical interiors** — Clean, minimal, corporate spaces (not gritty dystopia)
- **Intimate closeups** — Faces in tight frame during emotional beats
- **Technology as set design** — Holograms, UI elements, implants should be integrated into the frame

### Scene Writing for AI Pipeline

Each scene needs:
1. **First frame** — A strong visual establishing shot (can be wide)
2. **Middle** — Dialogue or action, 1-2 camera setups
3. **Last frame** — A clear visual change from first frame (character discovered something, a door opened, a hologram appeared)

### Sci-Fi Technique: Non-Verbal Alien Communication

For alien contact scenes, **avoid human-language speech**. The alien communication should feel genuinely *other* — not translated, not telepathic whispers, not English with reverb. The audience should experience the communication the way the character does: as sensation, not conversation.

**The Clicking Pattern (for "good" aliens):**
- Rhythmic clicking/clacking — organic, insectoid, but clearly intelligent
- Pulses and patterns carry meaning — the rhythm *is* the language
- Information transfers as embedded images and concepts, not words
- The protagonist receives flashes of understanding (dead worlds, symbols, faces) triggered by the rhythm
- When the clicking slows, the images fade. When it accelerates, the images intensify.

**Why it works:**
- Makes the revelation inherently **fragmentary** — the character gets images but not narrative, forcing them to interpret
- The protagonist cannot simply *repeat what they were told* — they have to piece together meaning from sensory fragments
- Different from every "alien speaks English" trope — genuinely alien
- Audio design can carry narrative weight (the clicking *is* the dialogue)

**Design rules:**
- Describe the sound in the screenplay: *"CLICK-click. Click-click-CLICK. Not mechanical — alive. Like a language made of bone and chitin."*
- The visions should be described as FLASH sequences — rapid, blurry, no context
- The protagonist should emerge with **partial understanding only** — they know something important was communicated but not the full picture
- The audience should feel the same confusion the character feels — they saw the flashes too but can't fully decode them

## Series Script Development Framework

For **multi-episode series** (3–6 episodes × 10–12 minutes), the workflow differs from single short films. Use this framework alongside the Writer's Room Workflow above.

### Series Scope

| Format | Episodes | Runtime per Ep | Total Runtime | Structure |
|--------|----------|----------------|---------------|-----------|
| **Mini-series** | 3 | 10–12 min | ~30–36 min | Tight 3-act season arc |
| **Season 1** | 4–6 | 10–12 min | ~40–72 min | Extended with subplots and breather episodes |

### Episode Template (10–12 min)

```
ACT I   (2–3 min)  — Hook + Setup. Re-establish stakes from last episode.
ACT II  (5–6 min)  — Escalation. New information, complications, character beats.
ACT III (2–3 min)  — Cliffhanger or mini-resolution. Propel into next episode.
```

Each episode should have:
- **Self-contained mini-arc** — something starts and resolves within the episode
- **Series arc progression** — the season-long mystery advances by one beat
- **Character development beat** — at least one moment that deepens our understanding of a protagonist
- **Forward hook** — the last 30 seconds set up what's next

### Season Arc Architecture (6 episodes)

| Episode | Role | What the Audience Learns | Energy |
|---------|------|--------------------------|--------|
| **Ep 1** | The Inciting Door | Protagonists meet. The mystery is introduced. First hint that something is real. | Open strong, end on connection |
| **Ep 2** | The Deepening | More details emerge. A supernatural/paranormal element is confirmed. First concrete evidence. | Reveal, validate the skeptic |
| **Ep 3** | The Escalation | Antagonists become active. Chase/escape sequence. The conspiracy is real and dangerous. | Raise stakes, introduce threat |
| **Ep 4** | The Breakthrough | Major clue discovered. Hidden base/location found. Protagonists go on the offensive. | Discovery, momentum shift |
| **Ep 5** | The Low Point | Protagonist incapacitated. Information overwhelm. Everything hangs in balance. | Tension, uncertainty |
| **Ep 6** | The Reveal + Cliffhanger | Full exposition dump. Truth is released. But — ambiguous outcome. Door left open for S2. | Catharsis + lingering question |

### Series Cliffhanger Types for Season Endings

| Type | Example | Best For |
|------|---------|----------|
| **Interrupted Moment** | Door breaks, freeze on terrified faces, cut to black | Mysteries where the threat is ambiguous |
| **The Revealed Truth** | Protagonist tells the world, cut to reactions | Conspiracy exposé stories |
| **The Separation** | Protagonists are forcibly split | Character-driven dramas |
| **The Discovery** | A new piece of evidence changes everything | Detective/who-dunnit arcs |
| **The Transformation** | Character is permanently changed | Supernatural/sci-fi series |

#### The "Interrupted Moment" Cliffhanger (Season Finale Technique)

A specific technique for season finales: **freeze on the protagonists' faces at the moment of highest uncertainty**, before any resolution is shown. No escape. No fire. No gunshot. Just the threat arriving — and the characters' faces as they realize it.

**How It Works**

1. **Threat arrives** — A sound from outside (dogs barking, footsteps, a vehicle). Distant but getting closer.
2. **Protagonists react** — Close up on their faces. Not running. Not fighting. Not packing. Just *hearing* what's coming and being frozen by it.
3. **Cut to black** — No escape sequence. No reveal of who's outside. No mobility. The audience is left in the exact same state of fearful paralysis as the protagonists.

**Why It Works for Season Finales**

- **No fake-out** — The protagonists are alive at the moment of the cut. The cliffhanger is about *what happens next*, not *if they survive*.
- **Empathy peak** — The audience is locked into the protagonists' perspective. They feel the fear because they see it on the characters' faces.
- **Season 2 hook** — The open question is irresistible: "Who was at the door?" / "Did they get out?" The audience has to return.
- **Rewatch layering** — On rewatch, the frozen moment carries the weight of everything the season built. It's not a cheap cliffhanger; it's a held breath.
- **The paralysis IS the cliffhanger** — The protagonists are cornered. They have no exit plan, no weapon, no idea what's outside. The moment they *should* be running, they can't move. That frozen terror is more suspenseful than any chase.

**Validation:**
- [ ] Is the threat established earlier? (The audience should recognize the sound — they've seen the antagonists before, or know what's hunting.)
- [ ] Are the protagonists frozen, not fleeing? (Running implies escape. Frozen implies cornered. Frozen is more suspenseful.)
- [ ] Does the blackout come at the peak of tension? (The barking is getting louder, the torch beams are getting closer, the faces show maximum fear — then black.)



For mystery/conspiracy series, a powerful structural archetype is pairing two protagonists who each hold **one half of the puzzle**:

| Role | What They Bring | Limitation |
|------|----------------|------------|
| **Researcher** | Data, patterns, historical context, documents. Can see the *shape* of the conspiracy. | No direct experience. Can't verify if the theory is real. |
| **Witness** | First-hand experience, memory fragments, testimony. Can confirm the conspiracy exists. | Can't articulate the pattern. Fragmented recall. No credibility alone. |

**Why it works:**
- Neither protagonist can solve the mystery alone — they need each other
- Creates natural tension (the researcher is skeptical of the witness; the witness is frustrated they can't prove it)
- Every discovery advances BOTH arcs: a new document makes the witness's memory more credible, and a new memory fragment gives the researcher a clue they couldn't decode
- The audience learns alongside both — through the researcher's analysis AND the witness's raw experience

**Design rules:**
- Each episode should give each protagonist at least ONE moment of contribution
- The researcher should NOT immediately believe the witness — their skepticism is the audience's proxy
- The witness should NOT immediately trust the researcher — they've been burned before
- Their shared breakthrough should come mid-series (Ep 3-4), after which they trust each other enough to share risks

### Three-Protagonist Structure: "Three Perspectives, One Truth"

An extension of the Researcher+Witness pattern for season finales: introduce a **third protagonist** whose discipline bridges or reframes the first two. Each protgainist sees the same conspiracy through a different lens — none has the complete picture alone.

| Perspective | Protagonist | Framework | What They Found |
|-------------|-----------|-----------|-----------------|
| **Discipline A** (e.g. Economics) | Researcher | Data, patterns, institutions | A system designed to extract and control |
| **Discipline B** (e.g. Experiential) | Witness | First-hand encounter, implanted visions | The beings behind the system are real |
| **Discipline C** (e.g. Religious/Spiritual) | Outsider | Scripture, folklore, comparative mythology | Ancient humans witnessed the same thing and encoded it as prophecy |

**Design rules:**
- The third protagonist should be introduced as a *background element* in an earlier episode (e.g. a street preacher shouting scripture in Ep 2) before their full reveal
- Their discipline should be orthogonal to the first two — not just another researcher or another witness
- Their contribution should *reframe* the mystery, not *solve* it. The audience should feel the picture getting clearer without seeing the whole thing
- The three should meet in the final episode and attempt to assemble the pieces — but the full truth remains out of reach (Season 2 territory)
### Two-Protagonist Archetype: "Researcher + Witness"



## Series Validation Checklist

Before delivering a series outline, confirm:
- [ ] Episode 1 has a strong cold open that hooks within 20 seconds
- [ ] Each episode ends with a forward hook (question the audience wants answered)
- [ ] No episode front-loads reveals meant for a later episode
- [ ] Episodes 2-5 each contain at least one NEW piece of the puzzle
- [ ] Episode 6 delivers a satisfying reveal AND leaves an open question for next season
- [ ] The season has a unified emotional arc (not just a plot arc)
- [ ] Episode durations are balanced (no episode doing 2x the work of another)
- [ ] The "easter egg" (a background detail that becomes meaningful later) is discoverable on rewatch

### Internal Consistency Audit (Post-Draft)

A structured check for logical breaks that individual scene editing misses. Run this after ALL episodes in a season are drafted.

**Character accuracy:**
- Are all character titles correct for their education/profession level? (Grad student = "Ms." not "Dr.")
- Does each character's dialogue match their established knowledge level? (A character shouldn't know something they have no way of knowing yet.)
- Does each character's behavior in Ep N+1 logically follow from where they were left in Ep N?

**Physical consistency:**
- Would a character logically keep sensitive materials (detective board, conspiracy notes) in their university office? If not, the board should only appear in a hidden location (cabin, safehouse).
- Are letters, packages, and documents consistent with how they arrived? (Hand-delivered envelope with no markings = no return address, no P.O. box information available.)
- Are timeframes reasonable? (Office cleared in 3 days is suspiciously fast — flag it as a planted mystery rather than leaving it unremarked.)

**Motivational consistency:**
- Would one vague warning letter really make a character who's been researching for 40 years suddenly flee? If not, escalate the threat: make it a single letter with visual evidence (photos of family), not multiple vague warnings.
- Is there a clear *why now?* trigger for each major character decision?

**Temporal consistency:**
- Do characters in Ep N+1 act like they remember what happened in Ep N? (No re-asking questions that were already answered in the same timeline.)
- Are all time references (hours/days/weeks since event X) consistent across episodes?
- If a date predates recorded history (before ~3,400 BC), does the character who references it acknowledge the dating gap? (e.g., "That's before writing. I don't know how he found those dates.")

**Cross-episode continuity:**
- Is a character described as "watching a location for weeks" in Ep 6 when they were actively doing something else in Ep 2 (the previous day)? Align the explanation with actual elapsed time.
- If a false-alarm sound (door creak, scraping at window) occurs in Ep 5, is it explained in Ep 6 when the character enters? If the entry method doesn't match the sound, it's a continuity break.
- Any edit to Ep N's screenplay requires simultaneous fixes to Ep N's production notes AND Ep 1's appendix/series outline. Never patch only the target file.

### Cold Open Techniques for Pilot Episodes

A cold open (the first scene before the title card) must hook the audience within 20 seconds. Three proven techniques for sci-fi/mystery pilots:

#### Technique 1: The Public Humiliation Cold Open

**Show the protagonist being publicly humiliated before the story even starts.** This generates instant audience sympathy and establishes the character's underdog status.

**How it works:**

A mystery object (a letter, a package) sets the stakes in the cold open; then, in the first scene of Act 1, the protagonist is publicly humiliated — mocked on a podcast, stammering "I... I..." while the host throws a headset at the camera and storms off. We haven't even met them properly yet, and we already feel for them.

**Structure:**
```
Cold Open: Mystery object (letter, package, message) establishes the stakes
Title Card
Act 1, First Scene: Protagonist on screen, being humiliated/disbelieved
  --> Audience sympathy locked in
  --> When they meet the other protagonist in the same scene, we want them to connect
```

**Why it works for pilots:**
- Bypasses the "why should I care about this character" problem
- Establishes the protagonist's low point immediately (nowhere to go but up)
- Creates a "meet-cute" moment when the other protagonist recognizes them
- Generates dramatic irony (we know the truth, even if the podcast host doesn't)

#### Technique 2: The Discovery Cold Open

A protagonist finds something they shouldn't have (a note, a file, a device). The audience sees it before anyone else does. Instant mystery.

#### Technique 3: The "Wrong Place, Wrong Time" Cold Open

The protagonist witnesses something they shouldn't have, or someone witnesses THEM. Establishes threat before the plot begins.

**Selection rule:** Use Technique 1 when the protagonist's *credibility* is the central obstacle (e.g., an abductee no one believes). Use Technique 2 when *information* is the central obstacle (a secret to uncover). Use Technique 3 when *survival* is the central obstacle (a chase from the start).

## Reveal Architecture (Information Drip)

The single most important structural skill for mystery/sci-fi series is **managing what the audience learns when**. A story that dumps all its secrets in Episode 1 has no reason to exist in Episode 6.

### Principles

1. **Protect the crown jewels** — Some truths must be earned over the whole season. The full "what the antagonists really are" reveal should not appear until Episode 6 (or be discovered gradually through episodes 2–6).
2. **Give enough to satisfy, not enough to end** — Each episode should answer one question while raising two new ones.
3. **Layered reveals** — The same piece of information can be revealed at different depths:
   - *Surface*: "There are aliens among us."
   - *Depth*: "They've been here for millennia — and they destroyed their own world first."
   - *Core*: "They control us through the systems we believe we chose."
4. **Rewatch value** — Plant easter eggs and background details that only make sense on a second viewing (e.g. a street preacher shouting a verse in Episode 2 that becomes meaningful in Episode 6).
5. **The audience should never feel manipulated** — Clues must be fair. The audience should be able to look back and see the trail.

### Reveal Timeline Template

| Episode | Answered Question | New Question Raised | Depth Level |
|---------|------------------|-------------------|-------------|
| 1 | Are the protagonists real? (Yes) | Is the conspiracy real? (Only hinted) | Surface |
| 2 | Are the memories real? (Emerging evidence) | Who else knows? | Surface → Depth |
| 3 | Is someone following them? (Yes, masked men) | What do the collaborators look like? | Depth |
| 4 | Where is the professor's trail? (Hidden cabin, investigation board) | What does the word on the board mean? | Depth |
| 5 | What is the conspiracy's plan? (Revealing) | How do we fight it? | Depth → Core |
| 6 | What do the good aliens want? (Full reveal) | What happens next? (Cliffhanger) | Core |

### Threat Escalation: Show, Don't Tell

A principle that extends beyond scene description into the *content of threats themselves*. A written threat ("We know where you live") is a bluff that can be dismissed. A **visual threat** (photos of family, personal items, surveillance evidence) is a demonstration of capability that cannot be dismissed.

**Why visual threats work better than written ones:**
- **Capability proof** — The threatener isn't claiming knowledge; they're *showing* it. The victim knows they've been watched.
- **Specificity** — Generic threats target the victim directly. Visual threats target what the victim *cares about* (family, home, work), which is more emotionally devastating.
- **Plot hooks** — A photo of a family member can introduce a new character (the professor's daughter) who may return in future seasons. A written threat has no such potential.
- **Silent menace** — No dialogue needed. The character holds the photo. The audience sees what they see. The threat is fully communicated without a single word of antagonistic dialogue.

**Design rules:**
- The photos should show the target going about their normal life — unaware they're being watched. This is more unsettling than dramatic surveillance shots.
- No note needed. The photos ARE the message. A typed letter can accompany them, but the letter should be generic boilerplate ("drop your research"). The photos carry the real weight.
- The character receiving them should react to the photos, not the letter. Their hands should tremble over the images, not the text.
- The photos should be specific enough to prove surveillance capability (different locations, different times of day) but not so specific that they reveal how the surveillance was conducted.

### Common Reveal Mistakes

- **Front-loading**: Giving the audience key information before they've earned it (e.g. the detective board full reveal in Ep 2 instead of Ep 4)
- **The "As You Know" trap**: Characters explaining things to each other that they would already know, just to inform the audience
- **Rescuing too early**: Letting protagonists discover the answer before the tension peaks
- **Invisible clues**: Revealing information the audience couldn't have possibly noticed (cheating)

### Easter Egg Layering: The Double-Meaning Technique

An easter egg that works on **two levels** — one diegetic (in-story) and one referential (meta/textual) — rewards rewatch and adds depth to the world.

#### How to Build One

1. **Choose a source text** — a verse, proverb, historical date, or symbol that connects to your theme
2. **Embed it diegetically** — give it an in-story meaning that works without the reference (a road number, a password, a background shout, a tattoo)
3. **Layer the reference** — let the audience discover the *source* meaning later (the road number is also a Bible chapter-and-erse; the background shout is a prophetic warning)
4. **Make it optional** — the story works fine if the audience never notices; the easter egg is a bonus, not required plot context

#### Example

| Element | Diegetic Meaning (in-story, front-facing) | Referential Meaning (discovered on rewatch) |
|---------|-------------------------------------------|---------------------------------------------|
| **Route 13** | The highway where the witness was taken. Revealed via a glove-compartment map in Ep 4. | A verse about buying and selling — connects to the control system revealed in Ep 6. |
| **The street preacher's shout** | Background color in Ep 2 — a figure shouting scripture as the protagonists walk past. No interaction. Easily dismissed. | The same verse — the system was announced in plain sight. |
### Two-Protagonist Archetype: "Researcher + Witness"



## Series Validation Checklist

- [ ] Does the diegetic meaning work without the reference? (A road number should still function as a road number.)
- [ ] Does the reference become obvious on rewatch? (Once you know the road number is also a Bible verse, you re-scan earlier episodes for the connection.)
- [ ] Is the reference accessible? (A widely known verse or proverb is better than an arcane reference no one will catch.)
- [ ] Is the background embedment truly background? (The easter egg should not interrupt the scene's primary action — it's in the background, the periphery, the corner of the frame.)
- [ ] Does the reveal recontextualize the easter egg? (Audience reaction: "Wait — that was there the whole time?")

### The Background Observer Technique (Visual Easter Egg)

A recurring visual figure placed in plain sight across multiple scenes — the audience registers them subconsciously but dismisses them as background — whose meaning is only revealed later.

#### Structure

1. **Plant** — A figure appears in the corner of multiple frames across Episodes 1-4. In a crowd photo. At the edge of an event picture. Half-hidden behind a curtain. The audience registers them subconsciously.
2. **Dismiss** — The characters don't notice them (or dismiss them as irrelevant). The narrative doesn't call attention to the pattern. The figure is always slightly blurred, always in the periphery.
3. **Reveal** — In a later episode, the protagonists discover all the photos/evidence compiled. The same figure is circled in every one. A montage of all their appearances hits the audience at once.

#### Why It Works

- Creates satisfying rewatch value (viewers re-scan earlier episodes looking for the figure)
- Makes the conspiracy feel *real* — the audience realizes they saw the watcher and didn't know it
- Doesn't require the protagonists to notice too early (protects the reveal timeline)
- The figure doesn't need to be explained — their *presence* is the message. The professor circled them because their persistent, unnoticed presence across decades is the evidence.

#### Design Rules

- The observer should appear in at least 3-4 distinct scenes/photos before the reveal montage
- Each appearance should be slightly more visible than the last (subconscious escalation)
- The reveal montage should be a silent beat — no dialogue explaining it. Let the images speak.

### Reveal Mechanic: Physical Recall (Memory Seizure)

A powerful technique for progressive information release in sci-fi/mystery series: **the protagonist's body physically reacts when a memory surfaces**, revealing information in fragments across episodes.

#### How it works

1. **Trigger** -- External stimulus (a name, a symbol, a location) activates the implanted memory
2. **Physical cue** -- A slight seizure, trance, or involuntary reaction that signals to the audience: *new information incoming*
3. **Fragmented output** -- Blurry images, single words, or short sentences -- never the full picture
4. **Layered unlocking** -- Each seizure reveals *more* detail about the same core event, building a clearer picture over time
5. **Parallel discovery** -- The memory fragment simultaneously unlocks something the *other* protagonist was stuck on (e.g., the professor's notes the researcher couldn't decipher)

#### Why it works

- **Pacing control** -- Each episode can reveal exactly one new fragment, preventing front-loading
- **Physical storytelling** -- The seizure is a *show* moment, not a *tell* moment; the audience watches the character relive the trauma
- **Character bonding** -- The non-affected protagonist must care for the affected one during/after the seizure, creating intimacy
- **Escalating stakes** -- Later episodes can have longer, more intense seizures with clearer vision output
- **Biological credibility** -- If the "good aliens" implanted knowledge, imperfect recall with physical side-effects feels more realistic than perfect data retrieval

#### Example

```
Ep 2:   Slight seizure in the lab. Triggered by a symbol in the professor's notes.
        Fragment: "The soil was wrong." (cryptic, no vision of another world.
        The researcher connects it to an agricultural economics shift.)
Ep 3:   Near-trigger. The witness recognizes a face in newspaper clippings but
        can't surface the memory. No conscious fragment; the gap builds tension.
Ep 4:   Full collapse at the cabin. Vision of the investigation board — the key
        word in red. The witness passes out; the researcher must protect them.
Ep 5:   The witness sits up mid-seizure. Shouts the clearest output yet.
Ep 6:   Seizure-free. Full narrative recall. The message comes through complete.
        The physical cost has been paid; now the truth can be spoken.
```

#### Design rules

- Each seizure should reveal **one new piece** of the mystery that makes sense in isolation
- The non-affected protagonist should **learn something** from each seizure (cipher, note, connection)
- Seizure duration should **escalate** across the series (2s twitch to 10s convulsion to collapse)
- Never let a seizure dump the full backstory -- that's what the climactic non-seizure recall is for

### The Withholding Principle

A counterintuitive but critical technique: **one or both protagonists should sometimes hold back information they could share**, not because they're hiding it, but because they're *processing within their own discipline*.

**How it works:**
- The **researcher** has the professor's notes containing data that *could* support the conspiracy theory. But she's an economist. She stays in her lane — she processes the fragment as an *agricultural economics* question, not an alien-invasion one.
- This creates productive tension: the audience knows more than the researcher does in that moment, or at least sees the gap between what she knows and what she's willing to conclude
- The character discipline makes the reveal *earned* — when she finally connects the dots, it's because the evidence is overwhelming, not because she jumped to conclusions

**When to use:**
- When a character has professional training (scientist, detective, economist, historian) — let them apply that training, even when it slows down the reveal
- When you want the audience to feel smarter than the protagonist (temporary dramatic irony)
- When the final reveal should feel like a discovery, not a confirmation of what was obvious
- **When the researcher character's notes should NOT contain the full explanation** — the researcher's data should point TOWARD the conspiracy, not pre-explain IT. If the researcher has a complete alien-invasion dossier, there's no story. The researcher should have discipline-appropriate data (economics patterns, historical shifts, power structures) that raises questions the audience can see but the character hasn't answered yet.

**When NOT to use:**
- When the withholding would feel like the character is stupid (the clues are too obvious)
- When the protagonist needs to convey urgency to the audience (don't slow down a chase scene with disciplinary analysis)

**How it works:**
- The **researcher** has the professor's notes containing data that *could* support the conspiracy theory. But she's an economist. She stays in her lane — she processes the fragment as an *agricultural economics* question, not an alien-invasion one.
- This creates productive tension: the audience knows more than the researcher does in that moment, or at least sees the gap between what she knows and what she's willing to conclude
- The character discipline makes the reveal *earned* — when she finally connects the dots, it's because the evidence is overwhelming, not because she jumped to conclusions

**When to use:**
- When a character has professional training (scientist, detective, economist, historian) — let them apply that training, even when it slows down the reveal
- When you want the audience to feel smarter than the protagonist (temporary dramatic irony)
- When the final reveal should feel like a discovery, not a confirmation of what was obvious
- **When the researcher character's notes should NOT contain the full explanation** — the researcher's data should point TOWARD the conspiracy, not pre-explain IT. If the researcher has a complete alien-invasion dossier, there's no story. The researcher should have discipline-appropriate data (economics patterns, historical shifts, power structures) that raises questions the audience can see but the character hasn't answered yet.

**When NOT to use:**
- When the withholding would feel like the character is stupid (the clues are too obvious)
- When the protagonist needs to convey urgency to the audience (don't slow down a chase scene with disciplinary analysis)

### The Background Observer Technique (Visual Easter Egg)

A recurring visual figure placed in plain sight across multiple scenes — the audience sees them but dismisses them as background — whose meaning is only revealed later.

**Structure:**
1. **Plant** — A figure appears in the corner of multiple frames across Episodes 1-4. In a crowd. At the edge of a photo. Half-hidden behind a curtain. The audience registers them subconsciously.
2. **Dismiss** — The characters don't notice them (or dismiss them as irrelevant). The narrative doesn't call attention to the pattern.
3. **Reveal** — In a later episode, the protagonists discover all the photos/evidence compiled. The same figure is circled in every one. A montage of all their appearances hits the audience at once.

**Why it works:**
- Creates satisfying rewatch value (viewers re-scan earlier episodes looking for the figure)
- Makes the conspiracy feel *real* — the audience realizes they saw the watcher and didn't know it
- Doesn't require the protagonists to notice too early (protects the reveal timeline)

## Collaborative Correction Loop

When the user gives script feedback, it follows a specific pattern. Recognize and respond to it.

### The Pattern

1. **User provides high-level concept** (raw ideas, bits and pieces)
2. **Agent drafts episode or series outline**
3. **User corrects SPECIFIC structural decisions** — not prose style but *when and where* information is revealed, *what characters do in a scene*, *internal consistency*, and *character accuracy*
4. **Agent applies targeted patches** to the affected areas

### How to Process Corrections

When the user says "remove that road-number reference from Scene 2" or "she's watching the video, not half-listening":

- **Interpret as structural feedback**, not prose nitpicking — the user is protecting the reveal timeline
- **Apply as targeted patch** — edit only the affected lines. Batch independent patches across files together.
- **Check for cascade** — does removing this detail from one episode require adjusting the appendix/series outline? (Yes — update the appendix/production notes too, in the same pass)
- **Never argue** — the user knows the story better than the agent's first draft

### Specific Correction Pattern: Information Sealing

The most common correction in this session was the user saying **"remove that information — the audience shouldn't know that yet."** This is a first-class structural signal, not a draft quibble.

**Correction types that appeared:**

| User says | What it means | Fix |
|-----------|--------------|-----|
| "Remove the ancient-origin reference from Ep 2" | That's an Ep 6 crown jewel reveal — it front-loads the mystery | Cut the line. The researcher should stay in their discipline, not jump to conclusions |
| "The witness should not talk about another world" | The memory fragment should be cryptic, not explanatory | Reduce to just the fragment. No world-building in vision output |
| "She has photos with shadowy figures circled, not labelled surveillance" | The researcher should have raw data, not labelled conclusions | Researcher has ambiguous data that points TOWARD a conspiracy but doesn't name it |
| "Those notes don't exist" | The researcher's data should be discipline-appropriate | Remove invented evidence. The researcher stays in their professional lane |
| "End on close-ups, no escape" | Cliffhanger should freeze protagonists in fear | Cut the resolution. End on the moment of maximum tension |

**Rule for the Withholding Principle:** When the user says "they don't know that yet" or "that note doesn't exist," they are protecting the reveal timeline. The researcher character should have **discipline-appropriate data**, not a complete explanation dossier. The evidence should be ambiguous enough that the audience watches the character *work toward* the conclusion, not confirm what was already written down.

**Correction types that appeared:**

| User says | What it means | Fix |
|-----------|--------------|-----|
| "Remove the ancient-origin reference from Ep 2" | That's an Ep 6 reveal. It front-loads the mystery. | Cut the line. The researcher should stay in economic analysis, not jump to alien arrival. |
| "The witness should not talk about another world or 'they came here'" | The seizure fragment should be cryptic, not explanatory. | Reduce to just the fragment ("the soil was wrong"). No world-building in seizure output. |
| "The researcher doesn't name the watchers. She just has photos with shadowy figures circled in red." | The researcher should have raw data, not labelled conclusions. | Change surveillance photos → event photos with ambiguous red circles. Don't name what you can't prove. |
| "The researcher doesn't share about similar encounters — those notes don't exist." | The researcher's notes should be discipline-appropriate, not an alien dossier. | Remove the paragraphs about "documented encounters going back centuries." Replace with economics-focused data. |
| "The witness doesn't need to ask where the lab is again" | Redundant information exchange. Characters shouldn't repeat info they just exchanged minutes ago in the same scene/timeline. | Check every line of dialogue for questions already answered in the same scene. Remove the repeat. |
| "Walking question doesn't make sense — she should be asking about his life, not his memory" | Character questions must serve their specific investigative goal, not just advance plot convenience. | If the researcher's goal is understanding WHY the witness was targeted, her questions should probe his background, not his memory recall. |
| "Office cleared in 3 days — that's too fast without explanation" | When something happens implausibly fast in-world, characters should acknowledge it. Don't leave plot holes for the audience to notice alone. | Flag the implausibility in dialogue — turn it into a planted mystery: "They didn't even wait for a missing person report. Like someone knew he was gone before I got the package." |
| "Ancient dates are before recorded history — audience won't connect" | When using dates/events that predate recorded history, the character who references them must show awareness of the dating gap. | Add dialogue acknowledging the mystery: "That's before writing. I don't know how he found those dates." The dating method is its own clue. |
| "She's a grad student, not a Dr." | Character titles and roles must be accurate to their education/profession level. | Use "Ms." not "Dr." for characters who haven't completed their doctorate. Verify all character titles before writing. |
| "Show photos of his daughter instead of 'we know where you live'" | Threats are more powerful when visual and specific to what the character cares about, not when generic or textual. | Replace written threats with surveillance photos, personal items, or other visual evidence that demonstrates capability. "We know where you live" is a bluff — photos of family are a demonstration. |
| "Field trip was passing by, not visiting" | Small believability details matter. If a character says they visited a cabin on a field trip, the audience expects them to have gone inside. | Use indirect encounters: "We drove past it on the way to a conference. He pointed it out." Establishes the location without implying the character entered it. |
| "Kills the headlights → keeping them off" | Think through the practical logistics of every scene action. If the goal is stealth, the character should never turn the lights on in the first place. | Adjust scene actions so the logical sequence matches the character's intent. Headlights never on = no need to "kill" them. |
| "Glove compartment — the researcher should ask, not the witness randomly curious" | Every character action needs clear motivation or direction. Random actions feel like plot convenience. | Have one character direct the other to search. One line of dialogue transforms random action into intentional investigation. |
| "No reaction to returning to the abduction site" | A character returning to the place where they were traumatized should show physical and emotional resistance. | Add physical tells: tightened hands, changed breathing, hesitation. The other character should offer an out. Silence is not a reaction — tension is. |
| "Do not reveal all concepts within one season" | When adding lore that spans multiple seasons, create a layer-by-layer reveal plan. Each season answers one deep question and raises a deeper one. | Structure reveals with a clear "what is withheld" section per season. S2 surface, S3 depth, S4+ core — never skip layers. |
| "Field trip was passing by, not visiting" | Small believability details matter. If a character says they visited a cabin on a field trip, the audience expects them to have gone inside. | Use indirect encounters: "We drove past it on the way to a conference. He pointed it out." Establishes the location without implying the character entered it. |
| "Kills the headlights should be keeping them off" | Every scene action must follow logical logistics. If stealth is the goal, the character should never turn the lights on in the first place. | Adjust scene actions so the logical sequence matches the character's intent. Headlights never on = no need to "kill" them. |
| "Glove compartment — the researcher should ask, not the witness randomly curious" | Every character action needs clear motivation or direction from another character. Random actions feel like plot convenience. | Have one character direct the other to search. One line of dialogue transforms random action into an intentional investigation beat. |
| "No reaction to returning to the abduction site" | A character returning to the place where they were traumatized should show physical and emotional resistance — not silence. | Add physical tells: tightened hands, changed breathing, hesitation. The other character should offer an out. Silence is not a reaction — visible tension is. |
| "Show photos of his daughter instead of 'we know where you live'" | Visual threats (surveillance photos, personal items) are more powerful and believable than written threats. A letter saying "we know where you live" is a bluff — photos prove capability. | Replace generic written threats with specific visual evidence (photos of family, personal belongings). The photos are the message; any accompanying text is secondary. |
| "Dark coats watching from across the street is too cliché for daytime" | Surveillance methods must suit the setting. Dark coats in daylight are a tired trope. Modern surveillance uses vehicles, phones, and digital tracking. | Use period-appropriate surveillance. A black sedan with tinted windows is more modern and menacing than a person in a coat. |
| "She's a grad student, not a Dr." | Character titles must be accurate to their education level. Grad students are Ms./Mr., not Dr. | Verify every character's title before writing dialogue that addresses them. Check across ALL scenes, not just introductions. |
| "Cabin lighting — keep it consistent between episodes" | Props must track across scenes. If a character finds a physical flashlight mid-episode, the transition from phone flashlight to physical one must be visible on screen. | Track key props between scenes. Document lighting source changes in action lines. Don't switch without an on-screen discovery moment. |
| "Dispatch docket on sun visor — no one does that" | Small real-world professional practices must be accurate. Wrong positioning breaks immersion for knowledgeable audience members. | Research how real workers handle documents. Default to the most natural real-world position rather than the most visually convenient one. |

 | `"Dark coats watching from across the street" → cliché for daytime` | Use period-appropriate surveillance (tinted sedan, digital tracking) instead of person-in-coat trope |
| `"The researcher references a subway station" → she didn't register him in Ep 2` | Character dialogue must match what that character actually witnessed. Narrator can set location; characters can only reference what they saw. |
| `"Watch what happened" → "See what happened"` | "Watch" is for ongoing events; "See" is for completed events. Use past-appropriate verbs. |
| `"Flat delivery for apokalypsis line" → should be excited` | Breakthrough revelations should have visible energy — use parentheticals like *(leaning forward, the first spark of energy in his voice)* |
| `"Character enters with weapon" → suspect protagonists are enemy` | Three-way standoff with mistaken identity: the third character enters armed because they think the protagonists are the trackers. Resolution comes from recognising evidence (notebook, photos). |

**Rule:** When the user says "they don't know that yet" or "that note doesn't exist," they are protecting the reveal timeline. The researcher character should have **discipline-appropriate notes**, not a full explanation dossier. The evidence should be ambiguous enough that the audience watches the researcher *work toward* the conclusion, not confirm what was already written down.

### Production Consistency Checklist (Post-Scene Self-Audit)

Before delivering a scene or episode, run this targeted plausibility check. These are the specific categories the user flags most often:

**Logistics audit:**
- Does every character action have clear motivation? (If a character opens a glove compartment, did someone ask them to, or are they just randomly curious?)
- Does the sequence of physical actions match the character's stated intent? (If stealth is the goal, would they ever turn on the headlights in the first place? If so, when do they turn them off — and is the action "kills" or "keeps off"?)
- How would the camera see the critical prop? Is it positioned in a natural actor frame (seat beside character, dashboard)? Or would the camera need an awkward insert shot to catch it (floor, behind seat, under bag)?
- Are props positioned realistically for the profession? (Dispatch docket on seat beside driver, not clipped to sun visor. Documents on passenger seat, not on floor in a courier bag.)

**Timeline plausibility:**
- Would this administrative action realistically happen this fast? (Office cleared in 3 days = implausible — flag it as a planted mystery rather than leaving it unremarked.)
- Do characters in Ep N+1 act like they remember what happened in Ep N? (No re-asking "Where's your lab?" 5 minutes after they were told. No redundant information exchange.)
- If a false-alarm sound (door creak, window scrape, knocking) appears in an earlier episode, does the later episode's character entry method logistically resolve it?

**Character accuracy:**
- Is every character title correct for their education/rank? (Grad student = "Ms." not "Dr." Verify across ALL scenes, not just introductions.)
- Would this character have realistically entered this location before? ("Field trip to a cabin" implies they went inside. "Drove past it on the way to a conference" does not. Use indirect encounters for locations the character only knows about second-hand.)
- Does the character's emotional reaction match the situation? (Returning to an abduction site should trigger visible physical resistance — tightened hands, changed breathing, hesitation. The other character should offer an out. Silence is not a reaction; visible tension is.)
- Would a character who has been researching secretly for 40 years keep a detective board in their university office? No — the board belongs in a hidden location (cabin, safehouse) only.

**Visual plausibility:**
- Does the lighting source stay consistent across scenes within the same location? If a character enters a cabin using phone flashlight in Ep 4, and uses a physical flashlight in Ep 5, the discovery of that physical flashlight must happen on screen.
- Are surveillance methods period- and setting-appropriate? (Dark coats in daytime watching from across the street = cliché. Tinted sedan idling, digital tracking, mobile surveillance = modern and believable.)
- Are sound effects up to date? (Nobody uses typewriters. Replace with mechanical keyboards.)

**Threat believability:**
- Would this threat make a rational character with 40 years of experience act? (Multiple written warnings ignored for years → one envelope with surveillance photos of his daughter = immediate flight.)
- Does the threat target what the character cares about, or the character directly? (Threats through loved ones are more effective than threats to self.)
- Is the threat visual (photos, evidence of capability) or textual (a letter saying "we know where you live")? Visual threats cannot be dismissed as bluffs.

- Write scripts to **`/opt/data/`** NOT `/opt/hermes/` (system directory, write-protected)
- The user can access files from the workspace panel
- Confirm the final path in your response so the user knows where to find it
