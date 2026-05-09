# Bi-weekly AI Intel Pipeline — Project Log

## Pending Cowork review

> Claude Code writes here when it hits a strategic / judgment question. Livia brings these to Cowork to discuss with Claude. Resolved items get checked off and the decision recorded in the decisions log below.

## Backlog (deferred, with explicit revisit triggers)

> Single canonical list of "things we know we should do later but parked for valid reasons". Per-source disposition stored in `sources.yaml` notes; this list groups them by category + revisit trigger.

### B1. JS-rendered article extraction (Wayback fallback)

- [ ] ~110 old OpenAI archive items + a few JS-rendered sources (apollo-research, agents-blog, weights-and-biases) can't be extracted because `trafilatura` sees only SPA shell.
- **Defer rationale**: archive items are pre-30-day so cursor filter excludes them; new RSS-fed items work.
- **Revisit trigger**: any JS-rendered source's high-signal items consistently NULL-excerpt for 2 consecutive weekly runs.
- **Fix when triggered**: 30-line Wayback Machine fallback (`https://web.archive.org/web/0/<url>`). No Chromium dep.

### B2. Source recovery — Asian corp / Taiwan banks (custom scrapers needed)

The Phase 1.5 URL probing recovered 4 sources (Foxconn ⚠️ partial, ESun ❌ scrape-empty, Compal ❌ scrape-empty, Inventec ✅ working). Three more groups remain in `mvp_active: false`:

**🔴 HIGH priority — direct sales-relevance to Livia's IBM clients:**
- [ ] **TSMC** — WAF-level bot block, even Safari UA. Try Wayback fallback (B1). If still blocked, paid scraping API as last resort.
- [ ] **ESun 玉山金控** — URL recovered but scrape returns 0 articles (page structure unusual). Per-source scraper needed.
- [ ] **Compal 仁寶** — same pattern as ESun.
- [ ] **CTBC 中信金控** — 404 on news paths, need URL exploration.
- [ ] **Cathay Life 國泰人壽 (subsidiary)** — currently unverified; maybe works via parent cathay-financial.

**🟡 MEDIUM — Taiwan manufacturing / financial coverage redundant via other sources:**
- [ ] Wistron 緯創 — bot blocked
- [ ] Quanta 廣達 — site PHP rendering broken
- [ ] Pegatron 和碩 — scrape no articles
- [ ] Sinopac 永豐, Taishin 台新, Taipei Fubon 台北富邦 — various 404 / bot issues
- [ ] Mizuho 瑞穗銀行 (Japan), UOB (Singapore) — non-Taiwan Asian banks

**🟢 LOW — international / US enterprise blogs:**
- [ ] Bloomberg AI, Wells Fargo Tech, Goldman Sachs developer portal (paywall / auth required)
- [ ] xAI, Bosch, ABB, Honeywell Forge, Mitsubishi Electric (dead domains / WAF)
- [ ] Apollo Research, agents.blog, Weights & Biases (JS-rendered — covered by B1)
- [ ] Various Chinese corporate sites (Ping An, ZhongAn) — Great Firewall + locale handling
- [ ] Various Taiwan government / institute sites (III, ITRI, NSTC, MAS Veritas) — custom structure

**Revisit trigger for HIGH-priority**: After Phase 4 ships and we have ≥4 weekly digests, any HIGH-priority source still missing → invest in custom scraper. Target: per-source scraper takes ~30 min dev each.

### B3. Pillar 5 (community discourse) coverage thin

- [ ] P5 has ~57 high-signal items vs P4's 759 — 13× imbalance.
- **Cause**: under-collected — only Latent Space + a few individual newsletters. Missing: Lex Fridman (fixed in Phase 1), Cognitive Revolution, BG2 Pod, more academic blogs.
- **Defer rationale**: 57 items still enough to write Pulse Pillar 5 weekly briefing.
- **Revisit trigger**: if Pulse Pillar 5 output quality (Livia checkbox: ⚠️/❌ ratio > 30%) signals weakness for 2 consecutive weeks.
- **Fix**: add 5-8 more P5 sources, run targeted collect.

### B4. Triage prompt — old-paper Pillar 5 false positives

- [ ] ~5 OpenAI 2018-2020 papers (GPT-3 paper, emergent tool use, etc.) tagged P5 by Haiku when really P3 historical.
- **Defer rationale**: pre-30-day cursor filter excludes them from Pulse anyway.
- **Revisit trigger**: if any of these surface in actual Pulse output (shouldn't, due to date filter).
- **Fix**: add explicit guidance in TRIAGE_SYSTEM that historical papers belong to P3 (capability research) not P5 (current discourse).

### B5. Collector — no Medium platform support

- [ ] Towards Data Science / Netflix Tech Blog / The Sequence are added but `medium.com/@netflixtechblog`, `medium.com/airbnb-engineering` etc not yet in sources.yaml.
- **Defer rationale**: 3 Medium-hosted sources already in (towards-data-science, the-sequence, netflix-techblog); marginal value of more.
- **Revisit trigger**: when adding sources for Pillar 4 expansion or P5 thin coverage (B3).
- **Fix**: add 5-8 Medium sources to yaml.

### B6. Governance — pending controls

(See `GOVERNANCE.md` "Pending governance work" for the full list. Highlights:)
- [ ] **Cost circuit breaker** (3-layer) — Phase 5 prerequisite. Pre-run check, mid-run abort, post-run anomaly.
- [ ] **Prompt versioning** — `triage_prompt_version` column on items.
- [ ] **Manual override** — CLI to record human corrections of triage decisions.
- [ ] **Kill switch** — `PIPELINE_DISABLED=1` env var honored by every CLI entry.
- [ ] **Sampled re-triage** — quarterly random 30 items re-triaged with current prompt, compare to original decisions, flag drift.

- [x] 2026-05-04 [delivery] Digest 交付管道選哪個？— resolved: GitHub repo markdown (主) + email 連結通知 (輔)
- [x] 2026-05-04 [visual format] Mermaid vs SVG vs PNG 何時用哪個？— resolved: 規則表已寫入 CLAUDE.md
- [x] 2026-05-04 [github] Repo 名字 + 帳號歸屬?— resolved: `livia-hsieh/ai-intel-harness`
- [x] 2026-05-04 [v1 coverage scope] HITL kinds 哪些寫 adapter — resolved: 等 4 週數據,但**現在就埋 metrics**(`collected_count`, `haiku_pass_rate`, `digest_inclusion_rate`, `livia_engagement_score`,signal_yield = digest_inclusion × engagement)。決策規則:>0.5 寫 adapter,0.2~0.5 觀察,<0.2 降權,0 移除。預測:substack/github/huggingface 是 config 問題(都有 RSS),paywall/interview_aggregation 永遠 HITL by design,youtube 短期 HITL 撐住,twitter(14 個 influencer)是 4 週後唯一真正要評估的 adapter 投資對象。
- [x] 2026-05-04 [broken feeds] Anthropic / DeepMind RSS — resolved: 不降權(這兩個是 backbone source,transport 問題不該懲罰 content 價值)。先試替代 endpoint(Anthropic: `/news/rss.xml`, `/index.xml`, `/feed`, sitemap;DeepMind: `/api/v1/feed/blog`, 舊 deepmind.com domain, sitemap)。若全死,寫 HTML scrape fallback **加 `scaffolding_note` metadata** 標明「RSS 恢復就拆」+ meta-loop 每季 probe RSS endpoints。這個 scaffolding 管理 pattern 是 portfolio 設計筆記金礦。
- [x] 2026-05-04 [over-fetch] OpenAI 929 篇 — resolved: **不採用 Livia 提案,date filter 放 collector 層而非 triage**。理由:(1) Date 是 metadata 不是 content,單一職責;(2) Triage 929 篇 Haiku ~$0.19 純浪費;(3) Triage prompt 不該被 date 邏輯污染。架構:Collector 對每個 source 維護 `SourceCursor(last_successful_pub_date)`,cold start 抓 30 天,steady state 增量。「Wide scan」是 source 廣度不是時間廣度——這個觀念釐清值得寫進 SCOPE.md changelog。Backfill 若需要做獨立 one-shot script,不混進 weekly run。
- [ ] 2026-05-04 [triage prompt versioning] 要不要在 items 加 `triage_prompt_version` 欄位,當 Pillar 定義改變時可以 diff 新舊決策?加一欄、0 runtime cost。現在加 vs 第一次真的需要 diff 才加?

---


**Single source of truth** for this multi-session build. Both Livia and Claude check in here at the start of each session and update at the end.

This file lives in the workspace folder (filesystem-persistent), not in Claude's session memory. It survives Claude restarts, new conversations, and tool changes.

---

## Project at a glance

A bi-weekly automated digest of frontier AI / agent engineering / software engineering / top transformation consulting content. Three goals stacked:

1. **Operational** — keep Livia's client-facing vocabulary current for AI at Scale sales conversations.
2. **Learning** — internalize harness engineering by building a real harness end-to-end.
3. **Portfolio** — public GitHub artifact for harness engineer job applications.

---

## Decisions log

| Date | Decision | Rationale |
|---|---|---|
| 2026-05-03 | Stack: **Python** | Universality, alignment with harness engineering community (Anthropic, LangChain, Parallel are Python-first), strongest job-search signal. |
| 2026-05-03 | GitHub release: **Day 1 public, build in public** | Commit history itself becomes portfolio signal; iteration of thinking is visible to interviewers. |
| 2026-05-03 | AI 知識庫 location: **`/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫`** | Connected via Cowork directory picker. IBM OneDrive corporate folder, suitable for work-context knowledge accumulation. |
| 2026-05-03 | Memory protocol: **3-layer (auto-memory / project folder / 知識庫)**, project folder must remain self-contained | See "Memory protocol" section below. |
| 2026-05-04 | GitHub repo: **`livia-hsieh/ai-intel-harness`** | Same account as personal brand; "harness" in name signals harness eng job-search positioning to recruiters. |
| 2026-05-04 | Delivery: **markdown in `digests/YYYY-WNN.md`** (primary) + **short email with link only** (notification) | Repo digests double as portfolio artifacts; email is push-to-phone trigger, content stays on GitHub for accumulation + visibility. |
| 2026-05-04 | Visual format rule table written into CLAUDE.md | Mermaid default for ≤10-node standard diagrams; SVG for hero visuals / quadrants / matrices; PNG for quantitative charts; explicit decision rule for synthesizer. The rule itself is a portfolio design note. |
| 2026-05-04 | Private source dump: **deferred** — use sources.yaml v0.1, grow via Mechanism A3 + manual additions later | Not worth blocking Task #3 on; collector should be source-agnostic anyway. |
| 2026-05-04 | HITL adapter eval: **measure signal_yield over 4 weeks before investing** | Per-source metrics埋進 collector + triage (`signal_yield = digest_inclusion_rate × livia_engagement_score`). Decision rule: >0.5 build adapter / 0.2~0.5 watch / <0.2 demote / 0 remove. Twitter (14 influencers) likely the only real adapter investment question; substack/github/huggingface are RSS config fixes. |
| 2026-05-04 | Broken RSS feeds: **scrape fallback with `scaffolding_note` metadata, never demote backbone sources** | Anthropic/DeepMind are Pillar 3/4 backbone; transport problems don't justify content devaluation. Try alternative RSS endpoints first; if all dead, scrape fallback marked as removable scaffolding. Meta-loop probes RSS endpoints quarterly for restoration. |
| 2026-05-04 | Date filtering: **collector layer (incremental cursor), NOT triage** | Reverses Livia's initial proposal. Reasons: (1) date is metadata not content - single responsibility; (2) triage cost on 929 items is $0.19 wasted; (3) triage prompt purity. "Wide scan" means source breadth, not temporal breadth. Cold-start: last 30 days. Steady state: items newer than `SourceCursor.last_successful_pub_date`. |
| 2026-05-04 | MVP free-only mode, paid sources deferred | Phase 1 proves value with $0 source cost. Paywall = HITL ad-hoc only; Twitter API = deferred. Individual influencers reach via echo channel (1-2 week lag through Latent Space / Interconnects / Import AI / The Batch / arXiv citations). 4-week eval triggers Twitter API consideration only if echo coverage < 70% AND specific influencer signal_yield > 0.5. |
| 2026-05-04 | Engagement mechanism: **3-layer (inline checkbox / Cowork review / downstream citation)** | Closes the previously hand-waved `livia_engagement_score` loop. Layer 1 (passive, git-tracked): per-briefing ✅/⚠️/❌ checkbox in markdown. Layer 2 (active, qualitative): weekly 5-10min Cowork review writing to `engagement_log.md`. Layer 3 (passive, strongest signal): grep wiki + project folder for `<!-- from: digests/... -->` source tags to count downstream citations. signal_yield = digest_inclusion × checkbox_score × (1 + citation_bonus). Written into SCOPE §13. |
| 2026-05-04 | Layer 3 redesign: **Cowork AI-mediated, zero consumer burden** | Initial Layer 3 required Livia to manually tag `<!-- from: digests/... -->` — she rejected as friction-heavy + not user-friendly. Redesigned: (1) Cowork passively detects digest references in conversation and logs silently; (2) monthly Cowork-led recall check ("which items did you actually use?"); (3) wiki backlink auto-propose when editing wiki via Cowork. Consumer-side action: zero. Tag maintenance burden moved entirely to Claude. This is the harness eng principle "scaffolding should serve humans, not the other way around" applied. |

---

## Memory protocol (the contract)

**Three layers, three roles:**
- **Claude auto-memory** — pointers and stable user context only; no long-form content.
- **Project folder (this folder)** — complete self-contained record of the project. Working notes, decisions, drafts, AND copies of any knowledge artifacts distilled out of this project.
- **AI 知識庫** — cross-project, topic-organized, polished knowledge artifacts. Future projects draw from here.

**Knowledge flow:**
1. Generated in conversation → written to **project folder** first (working state).
2. Once stable → **copied** (not moved) to 知識庫 under a topic subfolder.
3. Project folder keeps its copy + adds a pointer "consolidated version: 知識庫/<path>".
4. Auto-memory updated with reference pointer only.

**Conflict resolution (priority order):**
- Project state (progress, decisions, todo) → **PROJECT_LOG.md** wins.
- Distilled knowledge (frameworks, playbooks) → **知識庫** wins for canonical version.
- User profile/preferences → **auto-memory** wins.
- Filesystem (project folder / 知識庫) always > auto-memory on conflict.

**Per-session protocol:**
- **Start:** Claude reads PROJECT_LOG.md first to recover working context.
- **During:** major decisions written into PROJECT_LOG immediately, not at end of session.
- **End:** update session log, decisions log, task statuses; if new knowledge stabilized, copy to 知識庫 and update auto-memory pointer.

**Don'ts:**
- Don't move knowledge artifacts to 知識庫 — always copy.
- Don't put long content in auto-memory — pointers only.
- Don't depend on TaskList for cross-session state — it is session-scoped.
- Don't maintain divergent versions — once an artifact is consolidated, the 知識庫 version is the canonical one; the project-folder copy is a frozen snapshot.

---

## Pending decisions (need Livia input)

- ✅ ~~**GitHub username + repo name**~~ — resolved 2026-05-04: `livia-hsieh/ai-intel-harness`
- ✅ ~~**Delivery channel for digests**~~ — resolved 2026-05-04: markdown in repo + email notification with link only
- **Scope priority exercise** — "If a week's digest could only fit 5 items, which 5 sources would you most refuse to lose?" Forces a real ranking instead of "everything matters." (still open; not blocking Task #3)
- ✅ ~~**Session 1 framework writeup**~~ — resolved 2026-05-03 per Session 1 log line 170

---

## Phase gates (development discipline)

Established 2026-05-06 (Session 7) after Livia called out rush-forward / regress pattern. **No advancing to phase N+1 until phase N meets DONE criteria measured against representative full-scale data, not cherry-picked smoke samples.**

| Phase | DONE criteria | Gate | Current status |
|---|---|---|---|
| **1. Sources foundation** | Full `collect` ≥85% success, health all-green (no uncollected_sources / source_dead), every Pillar ≥10 items from ≥3 distinct sources | Don't build/iterate Triage logic | ✅ **DONE** (98.5%, all Pillars pass, 2 acceptable yellows) |
| **2. Triage** | Each Pillar audited on ≥30 items, ≥90% reasonable judgments, score range ≥0.20, data-quality issues fixed in Collector not Triage prompt | Don't build/iterate Pulse | ✅ **DONE** (4293 triaged, range 0.00–0.90, all 5 Pillars ≥95% reasonable) |
| **3. Pulse** | All 5 Pillars produce contract-compliant briefings on real backlog, content audit clean (provenance / URL / bilingual), cross-Pillar source diversity | Don't build Foundation | **🟡 1/5 Pillars** (Pillar 4 only) |
| **4. Foundation** | Full B→G curriculum cycle, each deep-read wiki-stable, 3 weeks reproducible | Don't ship as v1.0 | ⏳ not started |
| **5. Delivery + Meta-loop** | Real weekly run, email notification working, Livia reads + ≥1 prompt-refinement iteration based on real read feedback | v1.0 ship | ⏳ not started |

**Rules:**
1. Smoke test ≠ done. Smoke = "code doesn't crash on a small input". Done = "stage delivers full contract on representative full-scale data".
2. When a gap surfaces in a "done" stage, treat it as a failure of DONE criteria — update the criteria, add a health trigger, don't just patch the gap silently.
3. Data-quality issues belong in the Collector layer, not in downstream prompts. Resist the temptation to band-aid in Triage / Pulse prompts.
4. Cost discipline: a properly-staged single audit is cheaper than 4 partial smoke tests + regressions.

**Honest current state**: we're in **Phase 1**, not Phase 4. Stop zig-zagging into Pulse / Foundation iteration until Phase 1 + Phase 2 are properly DONE.

---

## Tasks

| # | Task | Status | Notes |
|---|---|---|---|
| 1 | Define scope of pipeline | completed | SCOPE.md v0.2 |
| 2 | Build source registry + channel fallbacks | completed | sources.yaml v0.1 (185 sources) |
| 3 | Implement collector + dedup (harness principles) | completed | Sessions 4–5. RSS + scrape + HITL + SQLite dedup + cursor incremental + RSS alt-endpoint + scaffolding_note + MVP routing per SCOPE v0.3.1. |
| 4 | Implement synthesizer (LLM clustering + vocab surfacing) | in_progress | Session 6: triage layer (Haiku) shipped + dry-run-tested. Pulse + Foundation TBD. |
| 5 | Implement delivery + first end-to-end run | pending | |
| 6 | Build meta-loop (self-correcting sources + prompt) | pending | The most harness-flavored phase |
| 7 | GitHub portfolio packaging + self-promotion artifacts | pending | |

Status values: `pending` / `in_progress` / `completed` / `blocked`.

---

## Session log

### Session 7 — 2026-05-06 — Excerpt enrichment + meta-loop health monitor

**Problem caught (Livia's pushback):** Earlier "fix" for Anthropic engineering items having NULL excerpts was a triage prompt change ("score from title alone if title is informative"). That moved the problem instead of solving it — Pulse layer hit the same root cause when it tried to synthesize. Inconsistent logic.

**Root fix:**
- New `collector/extract.py` — single responsibility: given URL, return article body's first 500 chars. Uses `trafilatura` (de-facto Python content-extraction library, ~90% success on news/blog HTML).
- `collector/fetchers/scrape.py` — calls `fetch_excerpt` for each yielded item; also added `_looks_like_nav_link` filter to drop site nav / footer / legal links pre-DB.
- `collector/fetchers/rss.py` — calls `fetch_excerpt` when RSS entry has no summary (RSS feeds without summaries are rare but real).
- `collector/enrich_excerpts.py` — one-shot back-fill for items already in DB with NULL excerpt. Idempotent. Resets triage state on items where extraction succeeded so the next `triage` run re-evaluates with the new content.

**Enrich smoke test (208 NULL-excerpt items):** 81 extracted (39%) · 127 still failed (61% — mostly old OpenAI archive on JS-rendered pages) · 37 triage states reset · 232s elapsed.

**Meta-loop health monitor (the bigger ask):**
- New `monitor/` module: `triggers.py` (catalog of named alert rules) + `health.py` (assemble state from DB + cost log) + `run.py` (CLI).
- `health` command computes per-source extract success rate, per-source cadence, scrape fallback dominance, triage distribution, score-compression detection, per-Pillar high-signal counts, weekly cost trend.
- Output: console + `data/health_latest.md` (committed to repo as portfolio evidence) + `data/health_log.jsonl` (per-run history, gitignored).
- First run **auto-detected the score-compression issue** Livia and I had been manually noticing — proves the monitor pattern works.

**Tasks completed this session:**
- ✅ Collector excerpt extraction (root fix)
- ✅ Enrich one-shot back-fill
- ✅ Health monitor v0.1 (3 collector triggers, 2 triage triggers, 1 cost trigger)

**Anti-patterns NOT introduced (extending list):**
11. ❌ Did not band-aid the excerpt issue with another prompt tweak. Root fix in collector instead.
12. ❌ Did not build headless-browser extraction for JS pages. Wayback fallback (~30 lines) is the right complexity-vs-coverage trade-off when the time comes — recorded in backlog with explicit revisit trigger.
13. ❌ Did not pre-build all triggers anyone can think of. Started with 6 high-value triggers (the patterns we already hit). New triggers accumulate when silent failures surprise us — every surprise becomes a permanent trigger.

**Pending Cowork question (open):**
- The triage_pillar_thin trigger uses raw-count threshold (`<2 high-signal`). For backlog data spanning years this is meaningless; it should be weekly-windowed. Defer until we have ≥4 weeks of weekly-cadence data; revisit threshold then.

---

### Session 6 — 2026-05-04 — Synthesizer triage layer (Task #4, part 1/3)

**What we did:**
- Stood up `synthesizer/` module with Haiku 4.5 triage as the first concrete piece. Pulse (Sonnet) and Foundation (Opus) deferred to next sessions — ship one stage end-to-end before adding the next.
- **`synthesizer/client.py`** — Anthropic SDK wrapper centralising three concerns: API-key handling (refuses to call without `ANTHROPIC_API_KEY`, surfaces `NoAPIKeyError` early), prompt caching (system prompt auto-tagged `cache_control: ephemeral`, ~70% cost cut on Sonnet/Opus runs), and per-call cost accounting to `data/cost_log.jsonl`. Lazy SDK import means `--dry-run` works with no `anthropic` package installed.
- **`synthesizer/prompts.py`** — `TRIAGE_SYSTEM` carries the full 5-Pillar contract (~3KB / 750 tokens), making it the right size to cache. Per-item user message stays small (~200 tokens) so per-call fresh input cost is minimal.
- **`synthesizer/triage.py`** — runner that pulls un-triaged items from DB, calls Haiku per item, parses tolerant JSON output, writes decisions back via `Storage.record_triage`. Three-bucket bookkeeping (high ≥0.6 / watch 0.3–0.6 / skip <0.3) matches SCOPE.md §10 calibration.
- **Storage migration** — added `items.triage_pillars`, `items.triage_signal`, `items.triage_reason`, `items.triage_at`, `items.triage_model`. Idempotent migration via existing `MIGRATIONS` list — DB seamlessly upgraded from v0.2 → v0.3 schema.
- **CLI** — `triage --dry-run --limit N` for cost forecast without API calls; `triage --limit N` for live runs. Cost summary printed at the end (total USD + cents/item).

**Smoke test (dry-run, 10 items):**
- 10 items processed, 0 errors
- Forecast: $0.02 USD (uncached estimate; real cached cost ~30% lower)
- Per-item: 0.20 cents — at 1028 items in DB → ~$2 uncached / ~$1.30 cached for full DB
- `data/cost_log.jsonl` written (10 records)

**Tasks completed this session:**
- ✅ Task #4 part 1/3: Triage layer (Haiku) shipped + dry-run-tested

**Next up (Task #4 parts 2/3, 3/3):**
- Pulse synthesis (Sonnet) — per-Pillar weekly briefing from triaged items
- Foundation deep-read (Opus) — rotating curriculum (B→C→D→E→F→G)

**Anti-patterns NOT introduced:**
8. ❌ No batch API (Anthropic Batch API) — premature; weekly volume too low to justify the async machinery, and per-item triage gives clean error isolation. Will revisit when weekly run >2000 items.
9. ❌ No retry-with-backoff on transient API errors — orchestrator pattern from collector applies here too: log + skip, don't pretend transient failures are normal.
10. ❌ No "fallback to Sonnet if Haiku output unparseable" — adds cost for ambiguous benefit. Tolerant JSON regex catches Haiku's occasional code-fence wrapping; bigger failures should surface as errors.

**Cowork question (open, not blocking):**
- Triage system prompt embeds Pillar definitions inline. When a Pillar definition changes (e.g., Pillar 1 expands to include insurers), the cache invalidates and the next ~12 hours of items get re-triaged with the new prompt. Acceptable, but want to flag: do we want a `triage_prompt_version` column on items so we can compare decisions across prompt revisions? Adds 1 column, 0 runtime cost. Defer or build now?

---

### Session 5 — 2026-05-04 — Collector retrofit per SCOPE v0.3.1 (Task #3 v0.2)

**What we did:**
- Retrofitted collector to honor SCOPE v0.3.1 decisions made in Cowork between Sessions 4 and 5.
- **`source_cursor` table** + `get_cursor` / `update_cursor` API on Storage. Cold-start = now − 30 days; steady state = `last_successful_pub_date`. Items older than cursor are filtered before insert. Smoke test: filtered 957 items (mostly OpenAI archive) — first concrete proof that "wide scan = source breadth, not temporal breadth."
- **Idempotent migrations** in `Storage._migrate()` via `PRAGMA table_info()` — added `items.scaffolding_note`, `fetch_log.used_channel`, `fetch_log.tried_endpoints` to existing v0.1 DB without dropping data. Survives v0.x → v0.x upgrades cleanly.
- **RSS alternative endpoints** in `fetchers/rss.py`. New `fetch_rss_with_metadata` returns `FetchAttempt(items, used_endpoint, tried_endpoints)`. Tries 9 common alt paths (`/rss`, `/feed`, `/feed.xml`, `/atom.xml`, `/index.xml`, `/news/rss.xml`, `/blog/rss.xml`, etc) on the same host before giving up. Smoke test: `google-deepmind` RSS now succeeds via `/blog/rss.xml` instead of declared `/discover/blog/rss.xml`.
- **Scrape-as-RSS-fallback** with `scaffolding_note` in orchestrator. When all RSS endpoints for a host die, the orchestrator falls through to scrape on the host page and tags every yielded item with `scaffolding_note: rss_unrecovered_<host>`. Smoke test: 19 Anthropic research items now ingested via scrape fallback, all tagged for the meta-loop to re-probe quarterly.
- **MVP routing** via `mvp_active` / `mvp_mode` fields on Source. Three modes: `full`, `echo_only`, `hitl_adhoc`. Tagged 14 individual influencers (twitter primary) as `echo_only` and 3 paywall sources (`stratechery`, `the-information-ai`, `liang-wenfeng`) as `hitl_adhoc`. They route to HITL queue with mode-specific reasons; collector skips fetch.
- **`tried_endpoints` logging** in `fetch_log` so the meta-loop can see which alt endpoints were probed.

**Tasks completed this session:**
- ✅ Task #3 v0.2: Collector retrofit complete. All four SCOPE v0.3.1 decisions implemented and smoke-tested.

**Smoke test results (re-run of first 5 sources, post-retrofit):**
- 5 ok, 0 errors (was 3 ok / 2 errors yesterday)
- 25 new items, 957 filtered by cursor (vs 1028 ingested wholesale yesterday)
- 19 items tagged `rss_unrecovered_www.anthropic.com`
- 5 source cursors written
- HITL queue: 1 (yesterday's `liang-wenfeng` test) + new MVP routings on next full run

**What's NOT done (deferred to Task #4 by design):**
- Signal yield columns on items (`haiku_pass`, `digest_inclusion`, `engagement_score`) — no data to fill until triage exists. Storage migration will add them when Task #4 needs them.
- Engagement log file format / inline checkbox — Task #5 (delivery) concern.
- Echo channel A3 self-discovery — Task #6 (meta-loop).
- Per-source `signal_yield` aggregate function — needs at least 4 weeks of triage + checkbox data first.

**Anti-patterns NOT introduced (extending Session 4 list):**
5. ❌ Did not pre-build signal_yield columns — those need data from Task #4/5; ALTER TABLE later
6. ❌ Did not write per-host RSS endpoint maps (e.g. "for anthropic.com try this specific list") — generic alt-path list works for both Anthropic and DeepMind in the smoke test; per-host overrides only when a real source forces it
7. ❌ Did not delete the v0.1 DB to migrate — `PRAGMA table_info` + ALTER TABLE keeps history intact, which is the correct pattern for any portfolio repo where someone might pull at a v0.1 commit and test-run

---

### Session 4 — 2026-05-04 — Collector + dedup (Task #3)

**What we did:**
- Resolved 3 blocking decisions before coding (GitHub repo name `livia-hsieh/ai-intel-harness`, delivery = markdown in repo + email link notification, visual format rules table written into CLAUDE.md).
- Built the collector: `collector/` package with `storage.py` (SQLite, 3 tables: items / fetch_log / hitl_queue), `config.py` (sources.yaml loader handling both single-channel and multi-channel `primary` shapes), `fetchers/rss.py` (feedparser), `fetchers/scrape.py` (RSS auto-discovery → common feed paths → generic article-list extractor), `run.py` (orchestrator with `--dry-run`, `--source`, `--limit-sources` flags).
- Set up repo: `git init`, `pyproject.toml` (hatchling), `.gitignore`, `README.md`, package install via `pip install -e .` exposing `collect` CLI.
- Smoke-tested against first 5 sources: 3 OK / 2 RSS parse errors (Anthropic research + DeepMind RSS feeds genuinely return invalid XML — not our bug). 1028 items ingested. Re-run produced 0 new items (dedup proven). HITL routing tested separately on `liang-wenfeng` (paywall) — correctly queued.
- Lowered Python floor from 3.11 → 3.9 because user's machine is on system Python 3.9.6 (no brew/pyenv); harness-eng signal is "open box and run," not "newest version." Dropped `slots=True` from 3 dataclasses, kept `from __future__ import annotations` everywhere.

**Tasks completed this session:**
- ✅ Task #3: Collector + dedup — runs end-to-end, dedup proven, HITL routing in place.

**Open issues for Session 5 (Task #4 — synthesizer):**
- 3 new "Pending Cowork review" items at top of file (v1 coverage scope / broken feeds / over-fetch architecture question).
- Task #4 needs to add date filtering at triage layer (NOT collector layer, per architectural reasoning in pending Cowork item #3).
- 26 sources currently HITL-queued (twitter 14, youtube 3, paywall 3, interview_aggregation 3, github 1, huggingface 1, substack 1) — Cowork to decide which adapters to build.

**Anti-patterns NOT introduced (caught during build):**
1. ❌ Did not add retry-with-exponential-backoff for failed fetches — fail loud, log, move on (per SCOPE.md fail-fast principle)
2. ❌ Did not write per-source XPath selectors for scrape — generic extractor first, observe failures, decide later
3. ❌ Did not pre-build SQLite columns for embedding/extracted_facts/briefing_snippet — those are Task #4/5 concerns; ALTER TABLE when needed
4. ❌ Did not build a separate `hitl.py` handler module — `Source.hitl_reason` + `Storage.queue_hitl` are sufficient surface; an extra abstraction layer would be premature

These four "scaffolding NOT added" decisions are the strongest design notes from this session.

---

### Session 3 — 2026-05-03 — Source registry (Task #2)

**What we did:**
- Initially proposed Tier-based source registry (T1/T2/T3) with scoring rubric. Livia caught this as over-scaffolding (her second harness eng correction; first was the hardcoded "source must contain code" rule). Pivoted entire architecture to **Wide Scan + Cheap Filter + Selective Deep Read** — signal-driven prioritization at runtime, no static tiers.
- Wrote sources.yaml v0.1 (~140 sources) with proper categorization including a missing first-class category: **Individual Influencers (multiplatform)** — Karpathy, Jensen Huang, Sam Altman, Lisa Su, Kai-Fu Lee, Andrew Ng, Yann LeCun, etc. Previously buried inside org listings.
- Bumped SCOPE to v0.2 with: 6 synthesis disciplines (added URL citation + bilingual), Pillar 2 source map expanded (MBB + Big Tech + Big 4 + academic think tanks), Memory L0 content cache, Mechanism A 3-channel update (A1 quarterly cross-validation / A2 user flagging / A3 system self-discovery).
- Wrote CLAUDE.md as Claude Code onboarding for transition.
- Token economics revised: Haiku triage / Sonnet Pulse / Opus Foundation hybrid → ~$3/week → $150-200/year. Bilingual output (~$50-80/year extra).
- Source list correctly framed as **incomplete by design** — Mechanism A3 grows it over time. Livia will dump her implicit private sources (IBM internal, Slack/Discord, Chinese newsletters) into v0.2.

**Tasks completed this session:**
- ✅ Task #2: Build source registry → sources.yaml v0.1 + CLAUDE.md ready for Claude Code transition

**Open issues to resolve before Session 4:**
- Get GitHub username + repo name preference
- Livia dumps her private/implicit sources (IBM internal, Chinese substacks, individual X follows) for v0.2
- Decide delivery channel for digest output (file in repo / email / Notion / Cowork artifact)

**Session 4 transition:**
- Switch from Cowork to **Claude Code**. Concrete instructions in next post-session message.
- Task #3 onwards (collector + dedup + synthesizer + meta-loop) all in Claude Code.
- Cowork still useful for strategic discussions about pipeline output quality, source list curation, and design notes drafting.

**Anti-patterns caught + recorded for portfolio:**
1. Hardcoded "source must contain X" rule (Session 1) — over-scaffolding source materials
2. Tier-based source registry with rubric weights (Session 3) — over-scaffolding source priority
3. "Wiki backward probe" as ×3 weight criterion (Session 3) — confirmation bias trap
4. Patronizing reduction "3 vocabulary words/week" (Session 2) — wrong consumer mental model

These four corrections are themselves the strongest design notes for the eventual portfolio README.

---

### Session 2 — 2026-05-03 — Scope definition (Task #1)

**What we did:**
- Completely reframed the digest from "vocabulary practice helper" (initial wrong reduction) to "personal intelligence briefing service for a Practitioner-Strategist Hybrid" — Livia pushed back hard on the original framing and forced a derivation from her identity model rather than from output backwards.
- Built a 12-track domain map of harness engineering (A: 模型/基礎能力 → L: 技術乾貨來源) so that Pillar 4's curriculum is grounded in a real discipline structure rather than ad-hoc topics.
- Locked the 5-Pillar structure with Pulse + Foundation dual track per Pillar.
- Corrected Pillar 2 from "non-AI business literacy" to "AI as discussed at C-Level / boards / regulators" (Livia's catch — original framing matiematically wrong because she sells AI transformation).
- Removed over-scaffolded synthesis rules ("source must contain X") in favor of knowledge-density-first + provenance/inference markers (Livia's catch — itself a harness engineering correction; this anecdote is portfolio gold).
- Cadence shifted from bi-weekly to weekly (+ event-triggered rapid updates).
- Decided memory layer (L1 URL + L2 content + L3 semantic embedding), token budget ($150-200/year hybrid model strategy), visual format (Mermaid primary), Cowork→Claude Code transition point (Task #3).
- Wrote SCOPE.md v0.1 to project folder as the locked contract. All downstream design is derivative of this document.

**Tasks completed this session:**
- ✅ Task #1: Define scope of bi-weekly AI intel pipeline → SCOPE.md v0.1

**Open issues to resolve before Session 3 (Task #2 — source registry):**
- Get GitHub username + repo name preference (Livia still owes this)
- Have Livia answer "top 5 sources you'd refuse to lose" — this is the seed for source list reverse-derivation
- Decide if Foundation curriculum order (B→C→D→E→F→G) should be reordered to prioritize G (governance) given Livia's IBM work

**Session 3 agenda preview:**
- From the 5 Pillars in SCOPE.md, reverse-derive the source list (Task #2): per-Pillar top companies/authors/channels with primary + fallback paths.
- Output: `sources.yaml`.
- This is still Cowork (markdown / yaml writing). Task #3 onwards switches to Claude Code.

---

### Session 1 — 2026-05-03

**What we did:**
- Deconstructed Livia's friend's reframe (old IBM 6-capability framework → new "Agent Engineering blueprint" with Agent marketplace / Ontology / Harness atoms) into a seven-lever framework + four cautions + a weekly practice routine. Full writeup pending placement in Livia's AI 知識庫.
- Commissioned this bi-weekly intel pipeline project as a multi-purpose vehicle (sales vocabulary refresh + harness engineering practice + portfolio).
- Mapped the project's components onto the harness engineering element list (orchestration loop / tools / memory / context / guardrails / evals / HITL / meta-loop) so Livia can explain the project in interviewer-ready language from day one.
- Made stack and public-release decisions (see decisions log).
- Created task breakdown (#1–#7).
- Provided Silicon Valley self-promotion playbook for harness engineer job search.

**Open issues to resolve before Session 2:**
- ✅ ~~Get Livia's AI 知識庫 path~~ — resolved 2026-05-03; path is `/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫`
- ✅ ~~Write the Session 1 framework writeup~~ — completed 2026-05-03; canonical lives at `知識庫/wiki/perspectives/frontier-vocabulary-arbitrage-7-levers.md`; snapshot in this folder at `frontier_vocabulary_arbitrage_7_levers_snapshot.md`
- Get GitHub username + repo name preference.
- Have Livia complete the "top 5 sources you'd refuse to lose" exercise before Session 2.

**Session 2 agenda (preview):**
- Walk through Task #1 (scope definition) — output: a written scope statement that becomes the contract.
- Begin Task #2 (source registry first draft) — output: initial `sources.yaml`.
- Set up GitHub repo skeleton with README + this PROJECT_LOG moved/copied in.

---

## How this file gets maintained

- **Every session start:** Claude reads this file first to recover context.
- **Every session end:** Claude updates the session log, decisions log, and task statuses.
- **When we set up the GitHub repo (Session 2 or 7):** this file moves into the repo as part of the portfolio.
- **Source of truth ranking:** this file > Claude auto-memory > TaskList. If they disagree, this file wins.
