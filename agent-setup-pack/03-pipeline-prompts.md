# Pipeline Prompts — Ready to Paste

*Every prompt below is copy-paste ready. Replace the bracketed parts with
your own details. Use these with your agent in chat, or in the gallery review
loop (see studio-ops skill).*

> **House rule that applies to every prompt here:** if an instruction is
> ambiguous — which assets are meant, whether "finished reviewing" means
> "approved, go ahead", which step "generate" refers to — ask the user what
> they mean and WAIT before taking any action. Never guess, never pick a
> reasonable default.

---

## 1. Screenwriter prompt

> You are my screenwriter. Write a short film scene for AI video generation.
>
> Requirements:
> - [N] characters: [names, ages, one-line descriptions]
> - One location: [location + time of day]
> - A clear beginning, middle, and end
> - Total runtime about [25] seconds
> - Dialogue lines of one or two sentences each. No long speeches.
> - No more than [6] shots
>
> Output the script in plain text, with the character's name before each line.

## 2. Shot breakdown prompt

> Break this script into shots for AI video generation:
>
> [paste the script]
>
> Use a table with columns: Shot # | Type (wide/medium/close-up/over-shoulder/
> insert/POV) | Description | Duration (3–6s) | Dialogue
> Rules: one idea per shot; 3–6 seconds per shot; the speaker always gets
> their own close-up for dialogue; total runtime about [25] seconds.

## 3. Character sheet prompt

> Generate a full body character reference turnaround sheet of [NAME] —
> [age], [occupation], [2-3 style details: clothing/hair], featuring four
> distinct views arranged side-by-side on a single wide frame: far left
> close-up facial portrait, followed by full-body side profile, full-body
> rear view, and full-body front view. The character has [hair detail],
> wearing [outfit detail]. Unedited RAW studio photography, shot on
> Hasselblad H6D-100c, 85mm lens, f/8 aperture, soft diffuse high-key
> lighting, authentic skin texture with visible pores, isolated on a
> seamless pure white background.

## 4. Location image prompt

> Generate a 4-panel location reference sheet arranged in a 2x2 grid layout
> of [LOCATION] — [setting, style, mood]. Four distinct environmental views
> on a single wide frame: top-left wide eye-level view, top-right high-angle
> perspective, bottom-left close-up detail view, bottom-right reverse/low-angle
> view. The scene features [key architecture, props, materials, lighting,
> weather]. No people in frame. Unedited RAW architectural photography, shot
> on Hasselblad H6D-100c, 24mm tilt-shift lens, f/8 aperture, soft diffuse
> overcast lighting, authentic surface textures, edge-to-edge frame sharpness.

## 5. Keyframe image prompt

> Generate the FIRST FRAME of this shot (the moment BEFORE the action
> starts): [shot description]. Character [NAME] with [facial expression —
> mouth closed/neutral if this shot has dialogue]. [Camera framing], [lighting],
> [style]. Reference the character sheet with @[CHARACTER_TAG] and the
> location with @[LOCATION_TAG].

## 6. Dialogue line prompt (in the clip's video prompt)

> When you generate the clip for [CHARACTER]'s line "[the line]", write the
> line inside the video prompt in quotes with a delivery tone — e.g.
> `NOVA says: "It's everything. The whole ledger." — tired, flat, quiet`.
> The video model speaks it and syncs the lips. Keep the line under 5
> seconds and keep one speaker per clip.

## 7. Studio review prompt

> Review my studio for [PROJECT]. Read every feedback note newer than your last
> revision — on the assets page `/a/<season>` (characters, sets, props), on the
> episode script pane, and on each shot card `/p/<episode>`.
>
> For notes about WORDS (script, character descriptions, shot plan): amend the
> draft, re-upload it, and report what changed. No generation, no cost.
>
> For notes that need GENERATION (images, video, upscales): do NOT start a
> paid batch. List what needs regenerating, then message me on Telegram or
> WhatsApp and ask either "shall I generate the [N] shots now? it'll cost
> about US$X" or "which shots should I regenerate?", and follow my answer.
>
> If a note is ambiguous — it could mean approve-and-proceed, or only some
> assets, or a later step — ask me what I mean first, then act. Never guess
> what a note is asking for.
>
> Report back a list of what you changed, what is waiting on approval, and
> what each batch cost.

## 7b. Populate the studio from an approved script

> The script for [EPISODE] is approved. Populate my studio: create/update the
> season and episode in projects.json (format "director"), write the episode
> script into the script pane, create one shot card per shot with its
> description and video prompt, and create the character/location/prop entries
> on the assets page for everything this episode needs — the character bible
> (looks, wardrobe, voice notes) and set/prop descriptions. Words only —
> generate nothing yet. Then tell me: "The character bible and assets are
> ready for your review at /a/<season> — nothing is generated until you
> approve them." Do not offer keyframes, video prompts or clips before I
> approve both the script and the bible.

## 8. Daily pipeline prompt (optional)

> Check my project for anything that is ready to generate (approved script,
> shots waiting for images/video). If there is approved work, tell me what
> you'd generate and roughly what it would cost, and ask me to say go before
> you run the batch. Never start a paid batch yourself without asking.
