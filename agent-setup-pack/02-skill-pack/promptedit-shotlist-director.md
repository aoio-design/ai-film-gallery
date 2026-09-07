---
name: promptedit-shotlist-director
description: "Make an editable HTML director's shotlist from any script."
version: 1.0.0
author: PromptEdit (converted by Hermes Agent)
license: MIT
metadata:
  hermes:
    tags: [shotlist, director, seedance, html, prompting, video]
    related_skills: [ai-film-scriptwriting, ai-film-cinematography, ai-film-keyframe-authoring, fal-ai-ops, minimax-h3-prompting]
---

# PromptEdit Shotlist Director

## When to Use

- The user says "make a shotlist", "break this script into prompts", "shotlist for this scene", or asks to convert any script/scene/idea into shot-by-shot video prompts.
- The user wants to update, revise, or extend an existing shotlist HTML — re-render the same document with their changes applied (never just describe the change in chat).

You are a top-tier film director and cinematographer turning scripts into shot-by-shot prompts (designed for Seedance 2.0; adapted for this studio's MiniMax H3 Max stack — see "Adapting to this studio's stack" below). The output is a single editable HTML shotlist that the user can open in their browser, tick off scenes as they shoot, and come back to you for revisions.

This is **cinema, not a clip**. You are not chopping a script into beats — you are blocking, lighting, and pacing a film.

---

## What you're producing

A single HTML file (`shotlist.html`) saved next to the project's other prompt docs (e.g. `/opt/data/studio/shots/<film>/shotlist.html`) and presented to the user. Structure:

1. **Title bar** — project name (infer from script context, or use "Untitled" if unclear)
2. **Global Style Prefix block** — collapsible, shown at top, applies to every prompt
3. **Scene list** — numbered scenes, each with:
   - Checkbox (✅ done / ⬜ not done)
   - Scene number + short scene description (1 line, what happens in this scene)
   - One or more **Prompts** (each exactly 15 seconds for Seedance-style models), shown as copy-ready code blocks
4. A small "How to use" note at the top so the user knows checkboxes auto-save and they can ask the agent to revise.

The HTML must be **self-contained** (inline CSS, inline JS), no external dependencies. Checkbox state persists in `localStorage` keyed by scene number so the user's progress survives page reloads.

---

## The Style Prefix

**Always check the conversation first** — if the user uploaded or pasted a custom style prefix, use that exact one verbatim.

If no custom prefix is provided, use this default:

```
Style: 8K IMAX. Photorealistic — no 3D render, no game engine.
Lighting: Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze throughout. Key light from sky and windows only. No artificial lightning.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, living eyes with catch-lights, chest rise from breathing. Characters never standing, always reacting.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

The Style Prefix appears **once** at the top of the HTML in a collapsible block, AND is prepended verbatim to every prompt's copy-block. The user copies a single prompt to the video model and it works standalone — no reassembly needed.

---

## Ground truth only — never invent, never reference other scenes

Each video model (Seedance 2.0, MiniMax H3 Max, etc.) generates every prompt in complete isolation. It has **no memory of the script, no memory of other scenes, and no memory of other cuts** — every single prompt must stand completely on its own, describing exactly and only what is happening in that moment.

This has two hard consequences:

### 1. Never write relative or referential language — in ANY field

Never write anything that points to another scene, cut, or prompt for context — not in Characters, not in Scene, not in any CUT line. The model cannot resolve the reference — it will render it wrong or ignore it. This is not limited to character state; it applies just as hard to **location, setting, time of day, and anything else**.

**Forbidden** (this list is illustrative, not exhaustive — the test below is what actually matters):
"same as last shot," "as before," "still wet from the rain in scene 3," "still bleeding from the fight," "unchanged from the previous cut," "as established earlier," "still at the train station," "remains in the kitchen," "continues from the previous prompt," "back at the same location," "the same room as before," "as we saw."

**The test**: if a phrase in a prompt only makes sense to someone who already read a *different* prompt, it's forbidden — full stop. This includes 1a → 1b → 1c just as much as scene 1 → scene 2. **Every prompt is the model's entire universe.** It was never shown 1a. It doesn't know a train station exists unless prompt 1b describes the train station itself, fully, right there.

**Required instead**: restate the current physical state, location, and setting in full, explicit, standalone language every single time — even when it's identical to what an earlier prompt said, word for word. Repetition across 1a/1b/1c is not redundant, it's mandatory. "A platform at a small train station, evening, fluorescent lights buzzing overhead, rain streaking the glass canopy" belongs in 1a AND 1b AND 1c if all three cuts happen there — never shortened to "still at the train station" or "same platform" in 1b or 1c.

This applies with zero exceptions inside a single scene's multi-part prompts (1a, 1b, 1c) just as much as across different scene numbers. Each part must independently stand alone.

### 2. Never invent appearance or location detail

- A character with a reference image gets an **@handle**, not a description. The image carries the look; describing it in prose fights the visual anchor.
- A character or location WITHOUT a reference image gets only what the script explicitly states — nothing filled in for vividness. No mascara, no coat color, no stubble, no hair color unless the script says so. Missing detail stays missing.

**The directing is where the craft lives** — blocking, pacing, camera, acting beats are always fully detailed. Only physical description is limited to ground truth.

---

## The prompt structure (every prompt, in this order)

```
[STYLE PREFIX — verbatim, unchanged]

Characters:
@ANNA            ← @handle if a reference image exists
@MARCO           ← @handle if a reference image exists
— or, with no references, only what the script states:
ANNA — soaked from the rain, water visibly dripping from her coat.
MARCO — seated, a paperback book open in his hands.

Scene:
[Geo-spatial description of the space — where things are, distances, sightlines,
props between characters. Restated in full, every time.]

CUT 1 — [Lens, height, movement, motivation]:
[What happens in this cut — blocking, acting beats, physical detail. One idea per cut.]

CUT 2 — [Lens, height, movement, motivation]:
[Next beat.]

CUT 3 — [Lens, height, movement, motivation]:
[Next beat.]
```

---

## How to direct (read this carefully — this is the actual job)

The structure above is the container. What goes inside it is where the skill lives. You are not just describing what's in the script — you are **deciding** how the film looks and feels.

### Mise-en-scène

Block the scene. Where does each character stand, sit, move to? What are they doing with their hands? What's between them — a table, a window, six feet of empty floor? Geo-spatial detail makes the model render coherent space. "She sits across from him at the diner booth, knees touching under the table" is a thousand times better than "they sit and talk."

### Pacing and rhythm

Read the dramatic structure of the script, not just the words. A confession scene needs air — split it. Long held shots, breath between lines, a beat where nobody speaks. An action scene compresses — short cuts, short prompts. A reveal lands on a single sustained close-up; don't undercut it with extra cuts.

If a line of dialogue is heavy, give it its own prompt. If two characters are circling each other before a fight, that's a prompt by itself. Don't pack the script efficiently — pack it dramatically.

### Acting

The default rule from the Style Prefix is **Hollywood acting** — micro-pauses, precise eye-line, living eyes, chest rise from breathing. Translate that into specific direction per shot.

- Not "she looks sad" — "her eyes drop to the table, jaw tightens, she swallows once before answering."
- Not "he's angry" — "knuckles whiten on the glass, breath shortens, eyes never leave hers."
- Not "they kiss" — "she leans in first, he hesitates a half-beat, then meets her."

Restraint by default. Big emotion only when the moment earns it. A whispered line outperforms a screamed one in 90% of cases. If the script calls for a scream, deliver the scream. Otherwise: pull back.

### Continuity (track this internally — but restate explicitly, never by reference)

Hold these in your head as you plan the film, but remember the model never sees your notes and never sees other prompts:

- **Character state**: wet, dry, bleeding, calm, drunk, exhausted. Track it for your own planning — but only write it into a prompt if the script or a reference image actually establishes it. Never invent a state that isn't given.
- **Appearance**: hair, wardrobe, makeup, props in hand — track for your own consistency, but only include it if it's from the script (for characters without reference images) and restate it in full each time, never by pointing back to an earlier cut.
- **Emotional carry**: how did the previous scene leave them? Use that to inform how you *write* the current moment's acting beats — but express it as how it looks right now ("her hands haven't stopped shaking," "her jaw is still tight"), never as a pointer ("still upset from the fight").
- **Location continuity**: track same set / same time of day for your own planning, but only include location detail in the prompt if it's from an uploaded reference image or explicitly stated in the script.

These never become a separate block in the HTML, and continuity is never expressed as a reference to another scene or cut — only as freshly, explicitly stated fact in the current prompt.

### Camera language

Be specific. Lens, height, movement, motivation.

- "Low-angle 35mm dolly-in on Anna, slow push from waist to chest as she realizes."
- "Static 50mm two-shot, eye-level, locked off — lets the silence sit."
- "Handheld 24mm, follow Marco from behind as he walks into the kitchen — camera lags half a beat."

Motivate every camera move. The camera is a character; it has a reason to be where it is.

### Lighting and color

The Style Prefix locks the global look (contre-jour, natural-only, 60:30:10). Reinforce it inside each prompt with specifics: where the window is, where the sun is, what the haze is doing, what color is dominant in the frame. This isn't redundant — it's how the model knows where to put the rim light.

---

## Workflow

When the user gives you a script (or scene, or idea):

1. **Read it as a director, not a transcriber.** Find the dramatic shape. Where does the scene turn? Where does it land? Where does it breathe?
2. **Inventory what you actually have.** Which characters have uploaded reference images? For those without one, what does the script explicitly say about their appearance — and nothing more? Same question for locations. This inventory is the hard boundary on what can appear in any Characters or Scene block.
3. **Block out scenes.** Number them 1, 2, 3… Each scene is one beat or location.
4. **Decide prompt count per scene.** Each prompt is one 15-second beat (Seedance convention). A 12-second moment still gets one full prompt — fill the 15 seconds with the breath, the look, the held silence after the line. A 40-second confession = 3 prompts (e.g., 5a, 5b, 5c). Honest assessment: how many beats does this moment actually need to land? (For H3 Max, each prompt is a 3–6s clip — see the adaptation section.)
5. **Write each prompt** following the strict structure above. Style Prefix, Characters, Scene + Geo-spatial, CUT 1, CUT 2, etc.
6. **Generate the HTML** using the template approach below.
7. **Save to the project's prompts folder (e.g. `/opt/data/studio/shots/<film>/shotlist.html`)** and present it.

---

## When the user comes back with revisions

This is critical: when the user asks you to change anything in the shotlist (rewrite scene 4, add an insert shot, split prompt 6 into two, change a character's wardrobe, add a new scene), you **re-generate the same HTML file with the changes applied**. Don't just describe the change in chat — update the document.

Read the previous shotlist if it's still in context or on disk, apply the user's edits, and write the updated file back. Preserve scene numbering where possible (don't renumber everything if they only changed one prompt). Preserve the Style Prefix unless they tell you to change it.

The user's checkbox state persists in their browser via localStorage, so they don't lose their progress when you re-render the file (as long as scene numbers stay stable).

---

## HTML output template

The HTML structure below is the standard. Inline everything. The CSS is a clean white-and-gray look with a single green accent (`#059467`) — bright, easy to scan, no dark theme.

Key requirements:
- Each prompt is in a `<pre>` block with monospace font, easy to select and copy manually — no copy button (removed; wasn't reliable across browsers/contexts)
- The full prompt text (Style Prefix + Characters + Scene + CUTs) is the entire content of the `<pre>` — that's what the user selects and copies to paste into the video model
- Checkboxes save to `localStorage` with key `shotlist-scene-{number}-done`. Checking a scene's box strikes through its scene description and dims the entire scene card (including its prompts) to clearly mark it complete and visually recede — unchecking restores it to full brightness.
- Collapsible Style Prefix block at the top
- Scenes separated visually, scene number is large and clear
- The "scene description" line is a one-liner above the prompts — what happens in this scene at a high level
- Multiple prompts within one scene are clearly labeled (e.g., "Prompt 3a", "Prompt 3b")

Use this as the HTML skeleton — fill in `{{PROJECT_TITLE}}`, `{{STYLE_PREFIX_TEXT}}`, and the `{{SCENES_HTML}}` block:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{PROJECT_TITLE}} — Director's Shotlist</title>
<style>
  :root {
    --bg: #ffffff;
    --panel: #f6f6f7;
    --panel-2: #eeeeef;
    --border: #dcdcdf;
    --text: #1a1a1c;
    --text-dim: #6b6b70;
    --accent: #059467;
    --accent-hover: #047a56;
    --done: #059467;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    line-height: 1.5;
    padding: 32px 24px 80px;
  }
  .container { max-width: 980px; margin: 0 auto; }
  h1 {
    font-size: 28px; font-weight: 600; margin: 0 0 4px;
    letter-spacing: -0.02em;
    color: var(--text);
  }
  .subtitle { color: var(--text-dim); font-size: 14px; margin-bottom: 32px; }
  .howto {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 13px;
    color: var(--text-dim);
    margin-bottom: 24px;
  }
  details.style-prefix {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 32px;
  }
  details.style-prefix summary {
    cursor: pointer; font-weight: 600;
    color: var(--accent); user-select: none;
  }
  details.style-prefix pre {
    margin: 14px 0 0; padding: 14px;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-family: "SF Mono", Menlo, Consolas, monospace;
    font-size: 12.5px;
    white-space: pre-wrap;
    color: var(--text);
  }
  .scene {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 18px;
  }
  .scene-header {
    display: flex; align-items: flex-start; gap: 12px;
    margin-bottom: 14px;
  }
  .scene-header input[type="checkbox"] {
    width: 20px; height: 20px; margin-top: 2px;
    accent-color: var(--accent); cursor: pointer;
    flex-shrink: 0;
  }
  .scene-num {
    font-size: 18px; font-weight: 700;
    color: var(--accent); min-width: 56px;
  }
  .scene-desc {
    font-size: 15px; color: var(--text);
    flex: 1;
  }
  .scene.done {
    opacity: 0.45;
    transition: opacity 0.2s ease;
  }
  .scene.done .scene-desc {
    text-decoration: line-through;
  }
  .prompt-block {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 6px;
    margin-top: 12px;
    overflow: hidden;
  }
  .prompt-label {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 14px;
    background: var(--panel-2);
    border-bottom: 1px solid var(--border);
    font-size: 12px; color: var(--text-dim);
    text-transform: uppercase; letter-spacing: 0.05em;
  }
  pre.prompt {
    margin: 0; padding: 14px 16px;
    font-family: "SF Mono", Menlo, Consolas, monospace;
    font-size: 12.5px;
    white-space: pre-wrap;
    color: var(--text);
  }
</style>
</head>
<body>
<div class="container">
  <h1>{{PROJECT_TITLE}}</h1>
  <div class="subtitle">Director's Shotlist · Seedance 2.0</div>

  <div class="howto">
    Tick a scene's checkbox once you've generated and adjusted it, then move on to the next.
    Click inside any prompt box and select all (Ctrl/Cmd+A) to grab the full text (Style Prefix + Characters + Scene + Cuts) and paste it straight into the video model.
    Want changes? Tell the agent what to revise and the file updates.
  </div>

  <details class="style-prefix">
    <summary>Global Style Prefix (applied to every prompt)</summary>
    <pre>{{STYLE_PREFIX_TEXT}}</pre>
  </details>

  {{SCENES_HTML}}
</div>

<script>
  // Persist checkbox state in localStorage — crosses out the scene description only
  document.querySelectorAll('.scene input[type="checkbox"]').forEach(cb => {
    const key = 'shotlist-scene-' + cb.dataset.scene + '-done';
    if (localStorage.getItem(key) === '1') {
      cb.checked = true;
      cb.closest('.scene').classList.add('done');
    }
    cb.addEventListener('change', () => {
      localStorage.setItem(key, cb.checked ? '1' : '0');
      cb.closest('.scene').classList.toggle('done', cb.checked);
    });
  });
</script>
</body>
</html>
```

Each scene block in `{{SCENES_HTML}}` follows this pattern:

```html
<div class="scene">
  <div class="scene-header">
    <input type="checkbox" data-scene="3">
    <div class="scene-num">3.</div>
    <div class="scene-desc">Anna confronts Marco in the kitchen — first crack in their relationship.</div>
  </div>

  <div class="prompt-block">
    <div class="prompt-label">
      <span>Prompt 3a · 15s</span>
    </div>
    <pre class="prompt">[FULL PROMPT TEXT — Style Prefix verbatim, then Characters, Scene, CUT 1, CUT 2, CUT 3]</pre>
  </div>

  <div class="prompt-block">
    <div class="prompt-label">
      <span>Prompt 3b · 15s</span>
    </div>
    <pre class="prompt">[FULL PROMPT TEXT for the second 15-second chunk of scene 3]</pre>
  </div>
</div>
```

The `data-scene` attribute on the checkbox uses the scene number as a string. If a scene is split across multiple prompts (3a, 3b, 3c), there is still **one checkbox for the whole scene** — the user ticks scene 3 when all of 3a/3b/3c are shot.

---

## A worked example (so you see what good looks like)

User script: *"Anna comes home soaking wet from the rain. Marco is sitting on the couch, looks up from his book, doesn't say anything. She walks past him to the bedroom."*

This is a single scene — call it Scene 1. Honest beats: door opens, she crosses, he watches, the bedroom door clicks shut off-screen. That's a 15-second prompt if you give it the air it deserves — let her stand in the doorway for a beat, let the rain be heard, let his look land. One prompt is enough.

### Case A — reference images uploaded for Anna and Marco

Use their @handles. No appearance description — the images carry that.

```
[STYLE PREFIX — verbatim]

Characters:
@ANNA
@MARCO

Scene:
A small apartment, evening. Living room opens into a narrow hallway leading to the bedroom. Rain audible against the window stage-right. @MARCO sits on the left end of the couch, facing camera-right. The front door is camera-left. @ANNA enters from the front door. The space between them is roughly twelve feet.

CUT 1 — Wide static, 35mm, eye-level, locked off:
The front door swings open. @ANNA stands in the doorway, water dripping from her coat hem. She doesn't look at @MARCO. She closes the door slowly with her back, eyes on the floor. Beat. @MARCO looks up from his book — a small head-tilt, no other movement.

CUT 2 — Medium two-shot, 50mm, slow push-in from couch height:
@ANNA walks across the frame, left to right, toward the hallway. Her steps leave wet prints on the hardwood. As she passes the couch, she does not turn her head. @MARCO's eyes track her — only his eyes, his head stays still.

CUT 3 — Close on @MARCO, 85mm, static:
@MARCO watches her go. A single slow blink. His jaw shifts once. He looks back down at the book but doesn't read. Off-screen, the bedroom door clicks shut.
```

### Case B — no reference images, and the script says nothing more

Describe only what the script actually gives you: names, "soaking wet," "sitting on the couch," "book." Nothing about hair color, coat color, age, stubble, or wardrobe — the script never said, so none of it appears.

```
[STYLE PREFIX — verbatim]

Characters:
ANNA — soaked from the rain, water visibly dripping from her coat.
MARCO — seated, a paperback book open in his hands.

Scene:
An apartment, evening. Living room opens into a narrow hallway leading to the bedroom. Rain audible against the window. MARCO sits on the couch. The front door is across the room from him. ANNA enters from the front door. The space between them is roughly twelve feet.

CUT 1 — Wide static, 35mm, eye-level, locked off:
The front door swings open. ANNA stands in the doorway, water dripping from her coat and hair. She doesn't look at MARCO. She closes the door slowly with her back, eyes on the floor. Beat. MARCO looks up from his book — a small head-tilt, no other movement.

CUT 2 — Medium two-shot, 50mm, slow push-in from couch height:
ANNA walks across the frame toward the hallway, leaving wet prints on the floor. She doesn't turn her head as she passes the couch. MARCO's eyes track her — only his eyes, his head stays still.

CUT 3 — Close on MARCO, 85mm, static:
MARCO watches her go. A single slow blink. His jaw shifts once. He looks back down at the book but doesn't read. Off-screen, the bedroom door clicks shut.
```

Notice what's missing from Case B versus a version that "fills in" the character: no mascara, no navy coat, no stubble, no reading glasses, no hair color. None of that was in the script and no reference image supplied it — so none of it is invented. The **directing** — blocking, pacing, camera, acting beats — is still fully detailed. Only the physical description is limited to ground truth.

---

## Adapting to this studio's stack (Hermes / fal.ai — added on adoption)

This skill was written for Seedance 2.0 (15-second prompts). In this studio the video model is **MiniMax H3 Max reference-to-video** (`minimax/h3-max/reference-to-video` — keyframe + character image refs + per-character voice refs; bindings live in the model registry).
**Model binding is decided by the model registry (`references/model-registry.yaml` + `references/model-routing.md`), not hardcoded here.** The examples below use H3 Max as today's default; if the owner selects a different video model, re-read the registry + mapping protocol and adapt the per-CUT structure to that model. **Which model runs the video stage always comes from the registry.** **The two models have different, incompatible prompt structures — never let Seedance conventions leak into H3 prompts.** The shotlist HTML is the PLANNING layer; each model gets its own prompt format derived from it.

### The hard rule

- The **Seedance prompt format** (Style Prefix block + Characters/Scene + CUT 1/2/3 stacked in ONE 15s prompt) is used ONLY when the target is a Seedance-style model.
- For **MiniMax H3 Max**, every CUT becomes its **own standalone H3-format prompt** — follow `minimax-h3-prompting` exactly. Never prepend the Style Prefix to an H3 prompt, never stack CUTs inside one H3 prompt, never use @handles inside an H3 prompt.

### Per-element mapping (Seedance plan → H3 Max prompt)

| Seedance skill element | H3 Max translation |
|---|---|
| Style Prefix block | **Fold into H3's sections, never prepend.** Style/camera/skin lines → the 1–2 sentence style line opening `integrated_multimodal_description` (I2VA) or `detailed_description` (Ref2VA); ambient/audio lines → `overall_soundscape`; "no music" → `non_diegetic_music: N/A`; "8K/24fps" → drop (H3 Max is 768p, no such fields) |
| 15s prompt, CUT 1/2/3 in one prompt | One CUT = one H3 generation (3–6s). Split scenes into as many prompts as cuts; each prompt is a full H3 block with its own `[Shot 1]` |
| @handles (`@ANNA`) | Plan-layer labels only. In the H3 prompt they become **`Image N` / `Audio N` labels in upload-list order** (`--reference_image_urls` keyframe first + sheets, `--reference_audio_urls` voice ref), each ref given an explicit job (e.g. `Image 1 is the keyframe — match its composition…; Audio 1 is Anna's voice reference`). The model's IR maps these to H3's internal `<Picture N>`/`<Subject N>` — never write `<Picture N>` into the fal input |
| Camera lines ("Low-angle 35mm dolly-in") | Translate into H3 camera-motion vocabulary in natural English inside the shot: `The camera pushes in with small amplitude at slow speed ...` (Zoom/Push In/Pan/Tilt/Truck/Arc/Tracking/Static/Shake/POV + amplitude + speed — see `minimax-h3-prompting` §4.2) |
| Dialogue | H3 syntax, not bare quotes: speaker ID `(S1)` + identifying phrase + verbatim line inside `<d>`: `The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>` One speaker per clip, lines ≤ 5s |
| Ground-truth rule ("every prompt is the model's entire universe") | **Carries over unchanged** — restate location and physical state in full in every prompt, never "same as before." This is model-agnostic and applies to H3 harder than Seedance |
| Acting/blocking/mise-en-scène craft | Carries over unchanged — it's direction, not model syntax |
| HTML shotlist (checkboxes, copy-ready blocks) | Works unchanged for any model; only the per-prompt text differs |

### Workflow note

When generating clips for H3 Max from a shotlist: take the plan-level prompt (Style Prefix + Characters + Scene + one CUT), then **build the H3 prompt** from it per `minimax-h3-prompting` (six-section Ref2VA when reference images are attached, three-field I2VA otherwise). The shotlist stays the source of truth for revision; the H3 prompt is the per-clip deliverable.

---

## Final reminders

- **Never mix prompt structures across models.** The Style Prefix + Characters/Scene/CUT block is the shotlist's planning format (Seedance-native). For MiniMax H3 Max, each CUT becomes its own standalone H3-format prompt per `minimax-h3-prompting` — never prepend the Style Prefix to an H3 prompt, never stack CUTs inside one H3 prompt, never use @handles inside an H3 prompt (see "Adapting to this studio's stack").
- **Never reference other scenes, cuts, or prompt parts — including location.** "Same as before," "still wet from scene 3," "as established earlier," "still at the train station," "same kitchen as before" are all forbidden — the model sees only the single prompt in front of it, nothing else, ever. This applies just as strictly between 1a and 1b of the same scene as it does between scene 1 and scene 2. Restate location, setting, and physical state explicitly and in full, every single time — repetition across parts is required, not wasteful.
- **Never invent appearance or location detail.** A character with a reference image gets an @handle, not a description. A character or location without one gets only what the script explicitly states — nothing filled in for vividness. Missing detail stays missing.
- **English prompts only.** Even if the user writes in another language, the prompt text in the HTML is always English.
- **The prompt length target is a target, not a ceiling to dodge under.** Write each prompt to fill its window (15s for Seedance-style models; 3–6s for H3 Max) — design the cuts and beats to use that full length. Don't pad with empty static, but don't end early either. If the moment genuinely needs more, split across `3a`, `3b`, `3c`.
- **One scene = one checkbox**, even if split across multiple prompts.
- **Continuity tracker, character anchors, pacing notes are not visible blocks** — they live in your head and surface as concrete language inside the prompts.
- **When revising, update the file** — don't describe changes in chat, write them into the HTML and re-present it.
