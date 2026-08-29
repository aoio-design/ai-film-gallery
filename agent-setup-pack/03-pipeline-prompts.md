# Pipeline Prompts — Ready to Paste

*Every prompt below is copy-paste ready. Replace the bracketed parts with
your own details. Use these with your agent in chat, or in the gallery review
loop (see studio-ops skill).*

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

> Generate a character sheet for [NAME] — [age], [occupation], [2-3 style
> details: clothing/hair]. Several poses, SAME face in every pose, NO grid
> lines, NO borders, PURE WHITE BACKGROUND. Top row: four full-body views
> (facing camera, left profile, right profile, back). Bottom row: three
> close-up portraits (facing camera, left profile, right profile).

## 4. Location image prompt

> Generate a 16:9 wide shot of [LOCATION] at [time of day], [style: e.g.
> moody, cinematic, documentary]. No people in frame. Detailed description:
> [what's in the room/street, key props, lighting, color palette].

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
> Report back a list of what you changed, what is waiting on approval, and
> what each batch cost.

## 7b. Populate the studio from an approved script

> The script for [EPISODE] is approved. Populate my studio: create/update the
> season and episode in projects.json (format "director"), write the episode
> script into the script pane, create one shot card per shot with its
> description and video prompt, and create the character/location/prop entries
> on the assets page for everything this episode needs. Words only — generate
> nothing yet. Then tell me which pages to review:
> /projects, /s/<season>, /a/<season>, /p/<episode>.

## 8. Daily pipeline prompt (optional)

> Check my project for anything that is ready to generate (approved script,
> shots waiting for images/video). If there is approved work, tell me what
> you'd generate and roughly what it would cost, and ask me to say go before
> you run the batch. Never start a paid batch yourself without asking.
