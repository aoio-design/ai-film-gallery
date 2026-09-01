# Model Routing — workflow, mapping protocol, governance (customer-pack mirror)

**Companion to `model-registry.yaml`** (the data). This file holds the *rules*: which model runs
which stage, how binding scope is resolved, how to map an unmapped model, and the exact agent↔user
workflow for generation. The registry lists *what's available*; this file tells you *how to pick
and how to talk to the owner about it*.

Two-part structure on purpose: **stage logic is model-agnostic** ("what" never changes); **model
binding is living data** ("which model" changes — and appends instead of overriding).

## Part 1 — Stages (model-agnostic; ~never changes)

| Stage | Deliverable | Layout convention / method | Downstream dependency |
|---|---|---|---|
| **Reference images** | character sheets / set stills / prop sheets | char **3-panel** (face close-up ‖ front/back, ONE-face rule) · loc **4-panel** 2×2 · prop 2-view | consistency for the video model |
| **Keyframe** (first-frame edit) | one frozen frame per shot — opening+closing **if the video binding demands a pair** | single opening frame, mouth closed/neutral on dialogue shots | **AR inherited from the VIDEO binding** |
| **Video clip** | clip with dialogue + sound | motion + dialogue-in-quotes, one speaker ≤5s, soundscape stated | master |
| **Master** | 4K (or 1080p social) upscale | aigc preset | output |

> **The one living rule: the selected VIDEO model owns the frame aspect ratio (and whether a
> first-last frame pair is required).** The keyframe stage reads the video binding BEFORE emitting
> frame dimensions. Today that's H3 Max ⇒ single 1344×768 first frame. If the project's video
> binding wants other dims or a frame pair, the keyframe stage re-derives from it.

## Binding scope — precedence (resolved highest → lowest at generation time)

| Level | What it sets | Example |
|---|---|---|
| **Shot override** | one shot → one alternative model | `Ep3-12A → seedance-2.5` (fast-action rescue) |
| **Project binding** | a whole film pins alternatives | "this series refs on nanobanana" |
| **Global default** | the frozen stack for new projects | gpt-image-2 + h3-max + bytedance |

A shot's `model: <id>` + `resolved_at: <ts>` records what produced it (**provenance**). Adding an
alternative profile NEVER touches the default — selection is additive.

## Mapping protocol — for a recognized/unknown model

1. **Confirm scope + name.** Which stage, and shot / project / global? (Named model + "this
   touches N files: …".)
2. **Gather, cheapest first:**
   a. `genmedia run <model-id> --help` (fal's own param registry — local + free)
   b. the fal.ai model page
   c. the provider's dev page.
   **Provider/search steps are permission-gated** (may burn Firecrawl/gateway credits); prefer
   `curl` for known URLs. If the owner asks you to search the web for prompt structure, ask first.
3. **Extract a provisional profile:** prompt structure, params, native dims/AR, whether a frame
   pair is required, cost/quality tiers, documented quality dialect.
4. **Re-verify layout METHOD** — 3/4-panel conventions stay pipeline-owned, but the *method*
   (one-shot multi-panel vs hero+edit) must be checked against the new model's capabilities.
5. **Quality dialect is PROVISIONAL, not inherited.** Do NOT copy the gpt-image-2
   "camera/lens beats photorealistic" finding into a new model. If docs are silent, run a
   **one-shot smoke test** (cheapest tier) to confirm dialect + dims before any batch.
6. **Verify gate (mandatory).** Confirm prompt structure + dims against official docs, run the
   smoke test, report its cost, get approval before a real batch.
7. **Append the profile** (dated, source URLs, verified-by) under the matching stage in
   `model-registry.yaml`, then set scope. **After** the smoke test passes — not before the batch.

## Agent↔owner workflow (the journey)

**Principle: the studio (gallery / FAB) REVIEWS + collects feedback; the CHAT session orchestrates
generation** (skills, FAL key, cost quoting, registry). Generation is never triggered from the FAB
(the feedback watcher is deliberately read-only). When the owner hits "generate" in the FAB,
redirect them to the chat session.

**Invocation:** `/ai-film-pipeline` + an idea. Loads the pipeline + scriptwriting skills, switches
to production mode. (Also auto-loads on film intent voiced in plain language.)

```
1. SESSION START      /ai-film-pipeline + idea → clarify (plain prose). No generation.
2. CREATE PROJECT     summarize plan → seek approval to create the project AND state the initial
                       model binding (global defaults or a project override) + a first cost
                       estimate for the reference-image stage. On approval, create it. Owner
                       reviews assets + shot pages, gives feedback in the studio.
3. REFERENCE IMAGES   (a) FAB "generate assets" → redirect to chat.
                      (b) In chat: RESOLVE SCOPE → present stage's current primary (+ registry
                          alternatives) → LIVE fal.ai cost quote → seek approval.
                          · approved → small smoke test if new/unmapped → batch → upload to assets
                            page → report actual cost.
                          · alternative named → MAPPING PROTOCOL → amended prompt to assets page →
                            owner verifies/edits prompt → approve → smoke ONE → batch → promote
                            profile to mapped + append.
                          · post-round change (images not up to quality) → same alternative branch.
4. FIRST FRAMES       first check: all reference assets approved? Then same shape (scope → quote →
                       approve/test/alternative). Keyframe reads VIDEO binding for dims/frame-pair.
                       Owner may opt to generate the first 3 frames as a test.
5. VIDEO CLIPS        first check: all first frames approved? Then same shape. If video mixing, FLAG
                       a dominant spec (look-consistency risk); re-edge rescue shots if the owner
                       wants a uniform look.
6. MASTER             clarify 1080p vs 4K → first check: all clips approved? → cost quote → upscale
                       → save to master folder → report done + cost + per-shot model provenance.
```

### The generate-approval loop (compressed rule)
`RESOLVE SCOPE` → (alternative named → MAPPING PROTOCOL) → `LIVE COST QUOTE` → `SEEK APPROVAL`
(never start a paid batch without an explicit yes) → `GENERATE + PROVENANCE` → `report actual cost`.

## Governance

- **Append, never override.** A model is added once, selected by scope. The global default row is
  frozen unless the owner names a model.
- **Post-round model change is a first-class branch**, not an edge case — it is the escape hatch
  (e.g. "this fast-action clip looks bad on H3, regenerate it on Seedance 2.5"). Always through
  scope → quote → approval.
- **Cost basis in the registry is guidance only.** ALWAYS `genmedia pricing <id>` live before
  quoting the owner.
- **Audit trail:** every mapping append is recorded (dated, source URLs, verified-by).