"""Trigger rules — the catalog of "this is bad, here's how to fix it" patterns.

Each trigger is a function `evaluate(state) -> Trigger | None`. State is the
HealthState dict assembled by health.py. A trigger fires when a specific
threshold is crossed; when it does, it returns a Trigger object with:
- severity: 🟢 / 🟡 / 🔴
- title: short headline
- detail: data backing the alert
- fix: specific action the user should take
- reference: link to PROJECT_LOG / SCOPE / code where context lives

This module is where new monitoring rules accumulate over time. Every time a
silent failure surprises us, the fix is to add a trigger here so it can't
hide twice.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

GREEN = "🟢"
YELLOW = "🟡"
RED = "🔴"


@dataclass
class Trigger:
    severity: str
    layer: str          # "collector" / "triage" / "pulse" / "cost" / "engagement"
    title: str
    detail: str
    fix: str
    reference: str = ""


TriggerFn = Callable[[dict[str, Any]], Optional[Trigger]]


# =============================================================================
# COLLECTOR triggers
# =============================================================================

def collector_uncollected_sources(state: dict) -> Trigger | None:
    """Sources declared in sources.yaml but never collected (no items in DB).

    Catches the silent failure surfaced in Session 7: yaml had 185 sources
    but only 5 had ever been hit because all smoke tests used --limit-sources.
    Without this trigger, "we have 1073 items" felt like good coverage when
    really it was 5/185 sources × heavy concentration in OpenAI archive.
    """
    declared = state.get("collector_declared_sources", set())
    collected = set(state.get("collector_per_source", {}).keys())
    if not declared:
        return None
    uncollected = sorted(declared - collected)
    if not uncollected:
        return None
    pct_missing = len(uncollected) / len(declared)
    sample = ", ".join(uncollected[:8])
    if len(uncollected) > 8:
        sample += f", ... ({len(uncollected) - 8} more)"
    return Trigger(
        severity=RED if pct_missing > 0.5 else YELLOW,
        layer="collector",
        title=f"{len(uncollected)} of {len(declared)} declared sources have never been collected",
        detail=(
            f"{pct_missing:.0%} of sources.yaml entries have zero items in DB.\n"
            f"Sample: {sample}"
        ),
        fix=(
            "Run `collect` (no --limit-sources flag) so the orchestrator hits every "
            "supported source. ~30–45 min, $0 API cost (HTTP only). Backlog of items "
            "then needs `triage` (~$2 / 1000 items at Haiku rates)."
        ),
        reference="Session 7 PROJECT_LOG; collector/run.py orchestrator",
    )


def collector_extract_success_too_low(state: dict) -> Trigger | None:
    """Per-source extract_success_rate < 0.5 → likely needs JS-render fix."""
    bad = []
    for s_id, m in state.get("collector_per_source", {}).items():
        if m["total"] >= 5 and m["extract_success_rate"] < 0.5:
            bad.append((s_id, m))
    if not bad:
        return None
    detail_lines = [
        f"  {s_id}: {m['extract_success_rate']:.0%} extract success "
        f"({m['with_excerpt']}/{m['total']} items have excerpt)"
        for s_id, m in sorted(bad, key=lambda x: x[1]["extract_success_rate"])
    ]
    return Trigger(
        severity=RED if any(m["extract_success_rate"] < 0.2 for _, m in bad) else YELLOW,
        layer="collector",
        title=f"{len(bad)} source(s) failing excerpt extraction",
        detail="Sources where >50% items have NULL excerpt:\n" + "\n".join(detail_lines),
        fix=(
            "Likely JS-rendered pages. Add Wayback Machine fallback in collector/extract.py:\n"
            "  - When fetch_excerpt returns None, try `https://web.archive.org/web/0/<url>`\n"
            "  - Wayback usually has rendered DOM snapshots; ~30-line addition, no Chromium dep"
        ),
        reference="See PROJECT_LOG.md backlog 'JS-rendered article extraction'",
    )


def collector_source_dead(state: dict) -> Trigger | None:
    """Source hasn't produced any item in N days (cadence_dead_threshold)."""
    threshold_days = 60
    dead = []
    for s_id, m in state.get("collector_per_source", {}).items():
        last = m.get("last_fetched_at_days_ago")
        if last is not None and last > threshold_days:
            dead.append((s_id, last))
    if not dead:
        return None
    detail_lines = [f"  {s_id}: last item {days}d ago" for s_id, days in dead]
    return Trigger(
        severity=RED,
        layer="collector",
        title=f"{len(dead)} source(s) appear dead",
        detail=f"No new items in {threshold_days}+ days:\n" + "\n".join(detail_lines),
        fix=(
            "Per SCOPE.md §10 source-health rule: investigate and either (a) demote in "
            "sources.yaml, (b) replace via Mechanism A3, or (c) accept and document."
        ),
        reference="SCOPE.md §10 — Source list 三通路自我更新",
    )


def collector_scrape_fallback_dominance(state: dict) -> Trigger | None:
    """A backbone source is on scrape-fallback path (RSS broken) — flag for re-probe."""
    affected = []
    for s_id, m in state.get("collector_per_source", {}).items():
        if m["total"] >= 5 and m.get("scrape_fallback_rate", 0) >= 0.5:
            affected.append((s_id, m["scrape_fallback_rate"]))
    if not affected:
        return None
    detail_lines = [f"  {s_id}: {rate:.0%} of items via scrape_fallback" for s_id, rate in affected]
    return Trigger(
        severity=YELLOW,
        layer="collector",
        title=f"{len(affected)} source(s) primarily on RSS scrape-fallback",
        detail="Items tagged `scaffolding_note='rss_unrecovered_*'`:\n" + "\n".join(detail_lines),
        fix=(
            "Their declared RSS endpoint is dead. Either:\n"
            "  - Manually probe alternative RSS paths, update sources.yaml\n"
            "  - Accept scrape fallback long-term, but at least once/quarter retry RSS"
        ),
        reference="collector/fetchers/rss.py ALT_RSS_PATHS, SCOPE.md §10 source health",
    )


# =============================================================================
# TRIAGE triggers
# =============================================================================

def triage_pillar_thin(state: dict) -> Trigger | None:
    """A Pillar has <2 high-signal items in the last lookback window."""
    threshold = 2
    thin = []
    for n, count in state.get("triage_high_signal_per_pillar", {}).items():
        if count < threshold:
            thin.append((n, count))
    if not thin:
        return None
    detail_lines = [f"  Pillar {n}: {count} high-signal items" for n, count in thin]
    return Trigger(
        severity=YELLOW,
        layer="triage",
        title=f"{len(thin)} Pillar(s) thin on high-signal items",
        detail=detail_lines[0] if len(thin) == 1 else "\n".join(detail_lines),
        fix=(
            "Source coverage gap for these Pillars. Two paths:\n"
            "  (a) Run Mechanism A3: scan Pulse outputs for cited-but-unlisted sources, propose adds\n"
            "  (b) Manual: review sources.yaml, ensure these Pillars have ≥10 active sources each"
        ),
        reference="SCOPE.md §2 Pillar definitions, §10 Mechanism A3",
    )


def triage_score_compression(state: dict) -> Trigger | None:
    """Score compression: low stddev AND narrow range.

    A pure stddev check fires false positives when a healthy distribution
    happens to have a heavy mode (e.g. mass at 0.70 because that's a natural
    "solid but not must-read" score). The honest signal is "stddev low AND
    range narrow" — if we see scores from 0.60 to 0.90 (range=0.30), Pulse
    can pick differentiated Top 3 even if many items cluster at 0.70.

    Threshold: range < 0.20 (i.e. all high-signal items within 0.6–0.8) AND
    stddev < 0.05 → real compression. Either condition alone is fine.
    """
    info = state.get("triage_high_signal_score_stats")
    if not info or info["count"] < 10:
        return None
    score_range = info["max"] - info["min"]
    if info["stddev"] >= 0.05 or score_range >= 0.20:
        return None
    return Trigger(
        severity=YELLOW,
        layer="triage",
        title="Score compression in high-signal bucket",
        detail=(
            f"High-signal items: count={info['count']}, mean={info['mean']:.2f}, "
            f"stddev={info['stddev']:.3f}, range=[{info['min']:.2f}, {info['max']:.2f}] "
            f"(target: stddev ≥0.05 OR range ≥0.20)"
        ),
        fix=(
            "Haiku is collapsing all high items into a narrow band — Pulse can't "
            "pick true Top 3. Either: (a) tighten triage prompt's signal calibration "
            "section, (b) feed triage more cross-source diversity (single-source "
            "samples compress naturally)."
        ),
        reference="synthesizer/prompts.py TRIAGE_SYSTEM § 'Signal calibration'",
    )


# =============================================================================
# COST triggers
# =============================================================================

def cost_weekly_alarm(state: dict) -> Trigger | None:
    """SCOPE.md §9 alarm: weekly cost > $5."""
    weekly = state.get("cost_last_7d_usd", 0.0)
    if weekly < 5.0:
        return None
    return Trigger(
        severity=RED if weekly > 7.0 else YELLOW,
        layer="cost",
        title=f"Weekly cost ${weekly:.2f} exceeds $5 budget alarm",
        detail=f"Last 7 days API spend: ${weekly:.4f}",
        fix=(
            "Per SCOPE.md §9, investigate:\n"
            "  - Source explosion (unexpected volume from a noisy feed)\n"
            "  - Prompt bloat (system prompt grew, cache invalidating)\n"
            "  - Sonnet/Opus called more than expected (Foundation track misfiring)\n"
            "  - Run `python -c \"from monitor.health import cost_breakdown_by_purpose; cost_breakdown_by_purpose()\"`"
        ),
        reference="SCOPE.md §9 cost budget alarm",
    )


# =============================================================================
# Registry
# =============================================================================

ALL_TRIGGERS: list[TriggerFn] = [
    # Collector
    collector_uncollected_sources,
    collector_extract_success_too_low,
    collector_source_dead,
    collector_scrape_fallback_dominance,
    # Triage
    triage_pillar_thin,
    triage_score_compression,
    # Cost
    cost_weekly_alarm,
]
