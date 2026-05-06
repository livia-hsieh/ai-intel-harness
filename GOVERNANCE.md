# AI Governance Framework — ai-intel-harness

> The same governance disciplines Livia sells to Tier-1 banks, applied to her
> own pipeline. This document maps each layer of the pipeline to NIST AI RMF
> functions, EU AI Act obligations, and concrete mitigations.

---

## Why this document exists

This pipeline ingests web content, classifies it with an LLM (Haiku), synthesizes
client-facing briefings (Sonnet), and produces deep-reads (Opus). Each of those
steps is an automated decision that affects:

- **What Livia tells her bank clients** (Pulse content shapes pitch & vocabulary)
- **What goes into her wiki** (Foundation deep-reads sediment into the knowledge base)
- **Which sources stay in the system** (Mechanism A3 self-discovers)

Same governance bar a Cathay or E.SUN production AI system would have to pass.

---

## Mapping to NIST AI RMF

NIST AI RMF has four functions: **GOVERN, MAP, MEASURE, MANAGE**. Below: where
each function lives in this pipeline.

### 1. GOVERN — policies, accountability, oversight

| Element | Where in this pipeline |
|---|---|
| **Stated AI policy / use cases** | `SCOPE.md` — defines who consumes the pipeline, the 5 Pillars, what's out of scope |
| **Roles & accountability** | Two-tool flow: Cowork = strategy/judgment, Claude Code = execution. PROJECT_LOG.md "Pending Cowork review" is the handoff queue |
| **Risk classification** | Each source has `pillar_tags`, `signal_density`, `mvp_mode`; paywalled & individual-Twitter sources are explicitly deferred (`hitl_adhoc`, `echo_only`) |
| **Change management** | Every prompt revision is a git commit; SCOPE.md has changelog (v0.1 → v0.3.1); PROJECT_LOG decisions log records architectural shifts |
| **Documentation** | This file + SCOPE + CLAUDE.md + PROJECT_LOG |

### 2. MAP — context, scope, stakeholder needs

| Element | Where |
|---|---|
| **Use case context** | SCOPE.md §1 (Practitioner-Strategist Hybrid) defines exactly who this serves |
| **Stakeholder identification** | Livia (sole user, both sides — IBM consultant Role A + harness eng Role B). Recruiters and bank clients are downstream readers |
| **Out-of-scope explicit** | SCOPE.md §3 (excluded categories) + sources.yaml (mvp_deferred entries) |
| **Failure mode catalog** | `monitor/triggers.py` — every failure mode caught becomes a permanent named trigger |

### 3. MEASURE — quality, performance, cost, drift

| Dimension | Mechanism | Status |
|---|---|---|
| **Quality** | Triage signal calibration audited per Pillar (≥30 items × 5 Pillars). Engagement Layer 1 (✅/⚠️/❌ checkbox per Pulse item) | partial — Phase 2 ongoing |
| **Cost** | `data/cost_log.jsonl` per-call; `health` aggregates weekly; hard cap $5/week | partial — circuit breaker pending |
| **Performance** | `fetch_log` per source (items_seen, items_new, error, used_channel); triage cents/item; pulse cents/Pillar | ✅ |
| **Drift detection** | Health triggers: `triage_score_compression`, `collector_extract_success_too_low`, `triage_pillar_thin` | ✅ |
| **Audit trail** | items table records `triage_at`, `triage_model`, `triage_reason`; fetch_log records `tried_endpoints` | ✅ |
| **Reproducibility** | Pending: `triage_prompt_version` column to allow before/after diff when prompt changes | pending — see Pending Cowork |

### 4. MANAGE — controls, intervention, incident response

| Control | Mechanism | Status |
|---|---|---|
| **Cost circuit breaker** | 3-layer: pre-run budget check, mid-run abort, post-run anomaly | pending — implementing now |
| **Quality circuit breaker** | health monitor red triggers can halt next run | partial |
| **HITL gates** | paywall → HITL queue (`hitl_adhoc`); engagement checkbox; weekly Cowork review | ✅ |
| **Manual override** | Pending: ability to mark a triage decision incorrect, reset and re-run | pending — Phase 4+ |
| **Kill switch** | Pending: env var `PIPELINE_DISABLED=1` checked before each layer | pending — Phase 5 |
| **Incident response** | Email notification on hard fail; health red; cost alarm | partial — Phase 5 |

---

## Mapping to EU AI Act (risk-based)

The EU AI Act classifies AI systems by risk tier. This pipeline is a personal
intelligence aggregator — **not a regulated system** under EU AI Act (no
biometric data, no employment decisions, no credit scoring). But the
`limited risk` and `minimal risk` transparency obligations still apply
because Livia uses Pulse output in client conversations:

| Obligation | How met |
|---|---|
| **Transparency (Art. 52)** — users informed when interacting with AI | Pulse output marks every paragraph `[原文]` / `[推論]` / `[假設]` |
| **Output traceability** | Every claim links to source URL; verification hints at digest tail name specific points to spot-check |
| **Human oversight** | Engagement Layer 1 (checkbox), Layer 2 (Cowork review), Layer 3 (downstream citation tracking) per SCOPE.md §13 |
| **Robustness** | Health monitor + retry logic + scaffolding_note for fallback paths + scaffolding-removal discipline |

---

## End-to-End Control Matrix

| Layer | Quality control | Cost control | HITL trigger | Audit |
|---|---|---|---|---|
| **Collector** | extract_success_rate per source; scrape_fallback dominance | $0 (pure HTTP) | source_dead trigger; paywall flag | fetch_log + tried_endpoints |
| **Triage (Haiku)** | per-Pillar audit; score compression detection; calibration rules in prompt | $0.30/wk; circuit breaker on cents/item drift | low-confidence sample for manual review (pending) | items.triage_* + cost_log |
| **Pulse (Sonnet)** | provenance markers required; cross-Pillar diversity check (pending) | $0.30/wk; per-Pillar cost ceiling | engagement checkbox per item | digest commits + cost_log |
| **Foundation (Opus)** | wiki-stability test (pending); 3-week reproducibility | $2/wk; single-run >$5 abort | Cowork review before sediment to wiki | digest commits + wiki provenance |
| **Delivery** | URL link only (no content in email) | minimal | Livia's read = implicit ack | git commit history |
| **Meta-loop** | Mechanism A1/A2/A3 per SCOPE §10 | quarterly run | A2 = Livia flag | PROJECT_LOG decisions log |

---

## Anti-patterns we explicitly govern against

These are recorded so future iterations don't reintroduce:

1. ❌ Hardcoded "must contain X" filtering (over-scaffolding) — caught Session 1
2. ❌ Tier-based source registry T1/T2/T3 (over-scaffolding) — caught Session 3
3. ❌ Wiki backward probe ×3 weight (confirmation bias) — caught Session 3
4. ❌ Reducing digest to "3 vocab words/week" (patronizing reduction) — caught Session 2
5. ❌ Manual citation tagging (friction-heavy, AI-friendly but human-hostile) — caught and redesigned Session 4
6. ❌ Smoke-test-as-done (rush forward, regress, repeat) — caught Session 7
7. ❌ Band-aid data issues in downstream prompts instead of fixing the upstream layer — caught Session 7

---

## Pending governance work

Items recorded here become Phase-N implementation targets. Each must be
shipped before its corresponding phase is DONE per `PROJECT_LOG.md` phase
gates.

- [ ] **Cost circuit breaker (3-layer)** — Phase 5 prerequisite. Implementing in `synthesizer/client.py` next.
- [ ] **Prompt versioning** — items table to gain `triage_prompt_version` column; `PROMPT_VERSIONS` constant in prompts.py. Allows before/after diff when prompts change.
- [ ] **Manual override for triage decisions** — CLI `triage-correct --item-id X --pillars [1,2] --signal 0.8 --note "..."` to record human corrections; create golden-set table.
- [ ] **Kill switch** — env var `AI_INTEL_PIPELINE_DISABLED=1` honored by every CLI entry point.
- [ ] **Cross-Pillar diversity check in Pulse** — health trigger when one source dominates Top 3 across ≥3 Pillars.
- [ ] **Wiki-stability test for Foundation** — Phase 4 prerequisite.
- [ ] **Sampled re-triage** — quarterly random 30 items re-triaged with current prompt, compare against original decisions, flag drift.

---

## Why this matters for portfolio

A hiring manager (or bank CIO) reading this repo:

1. Sees **the consultant who sells AI governance has actually built a system under NIST AI RMF / EU AI Act framing**
2. Can **point at concrete controls** (not just policies on paper): cost circuit breaker code, health triggers code, audit trail in DB
3. Notices **the same governance bar applied at $150/year personal scale** as enterprises typically apply at $1M+ scale — proving the discipline is portable, not contingent on scale

This document is part of the portfolio artifact, not just internal infrastructure.

---

_Version 0.1 · 2026-05-06 · created Session 7_
