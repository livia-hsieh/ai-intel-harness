# CLAUDE.md — Bi-weekly AI Intel Pipeline

> Onboarding for Claude Code. Read this first, then SCOPE.md, then PROJECT_LOG.md (it has the latest task state).

## What this project is

A weekly automated AI intelligence pipeline serving Livia, who is simultaneously:

- **Role A — IBM Consultant**: selling AI transformation / governance to Taiwan banks (Cathay, E.SUN, CTBC, Taipei Fubon, Taishin, Mega, First, SinoPac, TCB, Taiwan Cooperative) and manufacturers (Wistron, Foxconn, Pegatron, Quanta, Compal, Inventec, TSMC, ASML, MediaTek)
- **Role B — Harness Engineer in formation**: the build itself is portfolio for harness eng job applications

Both roles are full-force simultaneous. Not a "main + side" split.

## Documents to read in order

1. **SCOPE.md** — the contract. All design decisions are derivative of this. v0.2.
2. **sources.yaml** — ~140 sources, no tiers, signal-driven prioritization at runtime. v0.1.
3. **PROJECT_LOG.md** — task state, session history, decisions log. Updated every session.

## Architecture (one-line summary)

**Wide Scan (~140 sources, ~$0)** → **Cheap Filter (Haiku 4.5, ~$0.05/wk)** → **Selective Deep Read (Sonnet 4.6, ~$0.60/wk)** + **Foundation deep dive (Opus 4.6, ~$2/wk)**

Total budget: ~$150-200/year.

## Six synthesis disciplines (rules for every digest)

1. Each Pillar has explicit output shape contract
2. Synthesis rules are guidelines, not gates (knowledge density first)
3. Provenance markers: `[原文]` / `[推論]` / `[假設]`
4. Verification hints at every briefing's tail
5. URL citations mandatory (every claim → URL)
6. Bilingual output: English first, then 繁中 with English term annotations

## Five Pillars

1. 產業 AI 真實落地 (BFSI + 製造業) — Pillar 1
2. AI 戰略 / 治理 / 董事會層級 — Pillar 2
3. Frontier 能力 + 模型動向 — Pillar 3
4. Harness Engineering 實作技藝 (curriculum: B→C→D→E→F→G) — Pillar 4
5. 學派 / 社群 / 思想動態 — Pillar 5

Each Pillar has Pulse + Foundation dual track. Foundation rotates weekly through curriculum.

## Harness engineering disciplines applied to this codebase

- **Scaffolding-removal mindset**: Every component encodes "model can't do this alone." Test removability when models improve. Document each removal as a design note (portfolio gold).
- **HITL is first-class**: Paywalled / restricted sources flag for human input, log responses, trigger review on consecutive skips.
- **Memory layer is content-addressed**: SQLite with URL hash + content hash + embedding + extracted facts. Same URL never re-LLM'd.
- **Signal-driven prioritization**: No hardcoded T1/T2/T3 tiers. Haiku decides per cycle based on title + excerpt.
- **Meta-loop is built in**: Mechanism A1 (quarterly cross-validation), A2 (Livia flags), A3 (system self-discovers from citations).

## Current Task State

See PROJECT_LOG.md for canonical state. As of Session 3 (2026-05-03):

- ✅ Task #1: Define scope → SCOPE.md v0.2
- ✅ Task #2: Build source registry → sources.yaml v0.1 (~140 sources)
- 🟡 Task #3: Implement collector + dedup with harness engineering principles ← **start here**
- ⏳ Task #4: Synthesizer (clustering + vocab surfacing + Pulse/Foundation differentiation)
- ⏳ Task #5: Delivery + first end-to-end run
- ⏳ Task #6: Meta-loop (self-correcting source list + synthesis prompt)
- ⏳ Task #7: GitHub portfolio + self-promotion artifacts

## Stack & conventions

- **Language**: Python
- **Storage**: SQLite for dedup memory + paywall response log + glossary cache
- **GitHub**: `livia-hsieh/ai-intel-harness`, Day 1 public; commit history is part of portfolio signal
- **Models**: Haiku 4.5 (triage), Sonnet 4.6 (Pulse synthesis), Opus 4.6 (Foundation deep), text-embedding-3-small (semantic dedup)
- **Cadence**: Weekly Friday delivery + event-triggered rapid updates
- **Delivery channel**:
  - **Primary**: digests written to `digests/YYYY-WNN.md` in the repo (every digest = portfolio artifact)
  - **Notification**: short email when a new digest publishes — subject `[AI Intel] YYYY-WNN ready`, body contains only the GitHub URL to that week's digest. No content in email. Purpose is phone push → tap → read full version on GitHub.
  - Never put digest content in email (rendering is bad, accumulation is invisible, no portfolio value).

### Visual format selection rules

GitHub markdown renders Mermaid natively, so Mermaid is the cheap default — but it gets ugly fast. Pick by situation, not by habit.

| Situation | Format | Why |
|---|---|---|
| Standard relational diagrams (flowchart, sequence, gantt, ERD, class), ≤10 nodes | **Mermaid** | Versionable, PR-diffable, cheap for LLM to generate |
| Complex relational diagrams (>10 nodes, multi-layer, needs grouping boxes) | **Mermaid `subgraph`** — try once, fall through to inline SVG if ugly | Give Mermaid one shot |
| Weekly digest **hero visual** (one signature image per digest) | **inline SVG** (Claude writes `<svg>` directly) | Portfolio front door — worth hand-crafting |
| Quadrant / matrix / heatmap | **inline SVG** | Mermaid's quadrant chart is ugly and uncontrollable |
| Timeline + event annotations | Mermaid timeline/gantt if ≤15 events, else SVG | Mermaid timeline is fine for simple cases |
| Pure tabular data | **markdown table** | Don't force tables into diagrams |
| Screenshots / logos / photos | `![](path)` PNG/JPG | Don't SVG these |
| Quantitative charts (line, bar, stacked) | **pre-rendered PNG** (matplotlib/plotly export) | Mermaid is bad at charts; SVG by hand is expensive |

**Synthesizer decision rule (when generating a visual):**
1. Node count > 10 → write SVG directly
2. Quadrant / matrix needed → write SVG directly
3. Quantitative comparison (e.g. AI investment $ across banks) → pre-render PNG
4. Otherwise → Mermaid

**Why this rule exists (design note for portfolio):** The naive answer is "let the model generate SVG every time." That's wrong because: SVG token cost is high, models draw skewed shapes, PR diffs become unreadable, and Mermaid is good enough most of the time. Picking the right format is a classic scaffolding trade-off — over-scaffold (force a template) and you lose flexibility; under-scaffold (let the model freelance) and you pay for ugly output. This table is the explicit trade-off.

## What this codebase isn't (out of scope)

- Not a generic AI news aggregator
- Not a vocabulary practice flashcard system (this was an early misframing, corrected)
- Not a "consume more efficiently" tool — it's an asset-building system (Foundation feeds back into AI 知識庫)

## Memory protocol (3 layers)

- **Claude auto-memory**: pointers and stable user context. Loaded at every conversation start automatically.
- **Project folder (this folder)**: complete self-contained record. SCOPE / sources / PROJECT_LOG / future code. Single source of truth for project state.
- **Livia's AI 知識庫** (`/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫`): cross-project polished knowledge. Foundation-track output writes here when stable.

On conflict: filesystem (project folder / 知識庫) > Claude auto-memory.

## Known constraints

- Some sources are paywalled (Stratechery, The Information AI) → human_required: true workflow
- Some sources are non-English (Chinese-language interviews of 梁文鋒, 沈向洋, etc.) → may need HITL transcription
- Some Taiwan corporate sources have no RSS → scrape with sitemap polling, fallback Wayback
- Source list is intentionally incomplete; Mechanism A3 grows it over time

## Tone for digest output

- Tight, opinionated, pushback-friendly (Livia explicitly asks for debate, not summaries)
- No filler / no "AI hype tone"
- Cite or shut up (no claims without URL)
- 繁中 with English jargon inline; English-first synthesis pass

## Anti-patterns we've already eliminated (don't reintroduce)

1. ❌ Hardcoded "source must contain code/architecture" rules — over-scaffolding (Livia caught)
2. ❌ Tier-based source registry (T1/T2/T3) — over-scaffolding (Livia caught)
3. ❌ "Wiki backward probe ×3 weight" — confirmation bias (Livia caught)
4. ❌ "Local necessity ×2 across all Pillars" — only Pillar 1 needs locale (Livia caught)
5. ❌ Reducing digest to "3 frontier vocabulary words a week" — patronizing (Livia caught hard)
6. ❌ Layer 3 citation tracking via manual `<!-- from: digests/... -->` tags — AI-friendly but human-hostile, makes user do the data-cleaning work; corrected to Cowork-mediated auto-detection (Livia caught)

## Cowork ↔ Claude Code handoff protocol

This project uses **two AI tools in tandem**: Cowork (strategy/judgment) and Claude Code (implementation). Claude Code does mechanical work; Cowork does judgmental work. Both share state via PROJECT_LOG.md.

### When Claude Code SHOULD pause and flag for Cowork review

If you (Claude Code) encounter any of the following, **stop coding, write the question into PROJECT_LOG.md's "Pending Cowork review" section, and tell Livia "this is a Cowork question"**:

1. **Scope question** — should this source / topic be in scope? Does this contradict SCOPE.md?
2. **Source curation** — Mechanism A3 self-discovered a new source candidate; needs add/reject decision
3. **Synthesis quality drift** — digest output feels off (too marketing-ish, too thin, missing pillar coverage)
4. **Wiki sedimentation** — a Foundation deep-read is stable, ready to copy into AI 知識庫 (`/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫/wiki/`)
5. **Anti-pattern self-check** — you're about to add scaffolding (a hardcoded rule, a strict filter, a forced format); ask "is this over-scaffolding?"
6. **Portfolio positioning** — README / design note phrasing decisions; how to frame for harness engineer hiring audience
7. **Strategic disagreement** — you think SCOPE.md should change because of something you discovered

### When Livia returns from Cowork to Claude Code

After Cowork resolves a flagged item:
- The decision is recorded in PROJECT_LOG.md (decisions log) or SCOPE.md (if it changes contract)
- The "Pending Cowork review" item is checked off
- Claude Code on next session reads PROJECT_LOG.md, sees resolved items, applies them

### PROJECT_LOG.md "Pending Cowork review" section

Maintain this section at the top of PROJECT_LOG.md. Format:

```markdown
## Pending Cowork review

- [ ] [date] [trigger type] specific question + context
- [x] [date] [trigger type] resolved by [decision]
```

Example entries:
- `[ ] 2026-06-14 [source curation] Sholto Douglas cited in 3 consecutive Pulse outputs but not in sources.yaml — add as individual_influencer?`
- `[ ] 2026-06-14 [anti-pattern] tempted to add retry-with-exponential-backoff for RSS fetch failures; is this over-scaffolding given Anthropic recommends letting model decide retry?`
- `[ ] 2026-06-21 [wiki sedimentation] Track D Foundation deep-read on evals (W5) feels stable; copy to 知識庫/wiki/concepts/evals-design-for-agents.md?`

### What stays in Claude Code (no handoff needed)

- Writing code, debugging, running tests
- git / GitHub operations (init, commit, push, PR)
- File manipulation within repo
- Implementing well-specified tasks from PROJECT_LOG
- Refactoring, code review, performance tuning
- Reading existing code to understand
- Fixing errors with clear root cause
