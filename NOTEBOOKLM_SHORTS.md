# NotebookLM Shorts — Automation Workflow for Goal Englize

Design spec for turning top-scoring Telegram news items (from `main.py` →
n8n) into free vertical shorts using NotebookLM's Short Video Overviews
feature. Written after the 2026-07-27 planning session; see decisions below.

## Status

NotebookLM Shorts (Short Video Overviews) launched 2026-06-30, rolling out
first to Google AI Pro/Ultra subscribers. **We are on the free tier — the
feature is not live for us yet.** This doc is the target design; Phase 0
below is what to do in the meantime.

Check access: open notebooklm.google.com → any notebook → Studio panel →
look for a "Video" option with a "Short" length toggle. If it's not there,
we're still waiting on the free-tier rollout.

## Decisions locked in

- **Automation level**: safe / semi-automated. No unofficial API or browser
  automation against Google's NotebookLM — that carries account-ban risk we
  are not taking on a production pipeline. n8n does everything up to and
  including preparing the source text; a human clicks "Generate" in
  NotebookLM itself, ~2-3 min/day.
- **Trigger scope**: new n8n branch, fires only on the highest-scoring news
  items (not every item the watcher forwards) — keeps volume sane and
  quality high.
- **Voice**: Egyptian colloquial Arabic narration, to match the account's
  existing tone.

## Pipeline shape

```
Telegram channels (main.py)
        │  base64 photo + text, per message
        ▼
   n8n webhook (existing)
        │  scores the item
        ▼
   ┌─────────────┴─────────────┐
   │ existing branches (as-is) │   score below top threshold
   └───────────────────────────┘
   │
   │ score ≥ "short-worthy" threshold  (NEW branch)
   ▼
n8n formats a Source Card (template below) and delivers it
to a Telegram bot / inbox you check once a day
        │
        ▼
YOU (2-3 min): paste Source Card into the "Goal Englize Shorts"
NotebookLM notebook → Studio → Video → Short → set options below → Generate
        │
        ▼
Download the ~60s vertical MP4
        │
        ▼
Post-processing checklist (below) → publish
```

NotebookLM cannot watch the Telegram channels itself and has no public API,
so the human step (pasting the Source Card and clicking Generate) is the
one link in the chain that can't be removed without taking on ToS risk.
Everything before and after it is automatable.

## n8n branch — requirements

This repo only owns the Telegram → webhook leg (`main.py`); the scoring and
branching logic lives in n8n itself, so this is a spec for that branch, not
code:

1. **Trigger condition**: existing score ≥ your current "winner" cutoff,
   *plus* a stricter "short-worthy" cutoff on top (recommend: only the
   single best item per polling cycle, or a fixed score floor — tune after
   a week of real data so you don't get more shorts/day than you can post).
2. **Format step**: build the Source Card (below) from the webhook payload
   fields already available (`channel_name`, `text`, `timestamp`, `views`).
3. **Delivery step**: send the Source Card to wherever you'll actually see
   it daily (a dedicated Telegram bot chat is simplest — reuses
   infrastructure you already have).

## Source Card template

Keep this format fixed so every NotebookLM short is generated the same way
— consistency here is what makes the 2-3 min manual step fast:

```
TOPIC: <one-line story headline in Arabic>
SOURCE: <channel_name>, <timestamp>
KEY FACTS:
- <fact 1>
- <fact 2>
- <fact 3>
AUDIENCE: Arabic-speaking football fans, casual/entertainment tone
TONE: Egyptian colloquial Arabic, energetic, Goal Englize voice
FOCUS: <what the short should center on — e.g. "the transfer fee and
reaction", not a full match report>
```

Paste this whole block as the notebook's source text (or as a single doc
source) before generating.

## NotebookLM settings, every time

- Studio → Video → **Short** (not the long-form explainer)
- Output language: **Arabic**
- When prompted for audience/goal: reuse the AUDIENCE/TONE lines from the
  Source Card
- Topic: use the TOPIC/FOCUS lines — don't let it pick a topic for you,
  the auto-suggested angle won't match your hook style

## Post-processing checklist (before publishing)

NotebookLM's raw output is not on-brand by itself:

- [ ] Add Goal Englize intro/outro or logo bug
- [ ] Overlay your own hook text in the first 1-2s if the AI-written hook
      is weak (this is the single biggest lever on short-form retention —
      don't skip it even under time pressure)
- [ ] Add your standard CTA (per the `goal-englize-master` skill's CTA
      system)
- [ ] Check narration accuracy against the Source Card facts — it's
      grounded in what you gave it, but skim before publishing

## Phase 0 (now, free tier)

- Build and test the n8n branch + Source Card formatting end-to-end, but
  hold the "paste into NotebookLM" step as a manual dry run using a regular
  (non-Short) Video Overview or any notebook you already have access to,
  just to rehearse the Source Card format.
- Re-check plan access weekly (Studio panel check above).

## Phase 1 (once Shorts is live on our tier)

- Turn on the n8n branch for real.
- Run for 1-2 weeks, tune the score threshold based on how many
  shorts/day is actually sustainable to post-process and publish.
- Revisit the automation-risk decision only if the 2-3 min/day step
  becomes a real bottleneck at higher volume — not before.

## Known limitations to keep in mind

- No official Google API; anything beyond this manual step is ToS risk.
- Output is grounded only in what's pasted in — garbage Source Card in,
  garbage short out.
- Designed for compact factual summaries, not necessarily punchy
  hook-first viral structure — hence the mandatory hook-overlay step above.
- Feature is 4 weeks old as of this writing; specifics (exact free-tier
  caps, exact customization options) may shift as Google iterates.
