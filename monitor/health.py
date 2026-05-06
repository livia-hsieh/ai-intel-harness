"""Health checker — assemble per-layer state from DB + cost log, evaluate triggers.

Output:
- console: human-readable colored report (when run interactively)
- data/health_log.jsonl: machine-readable record (one JSON line per run)
- data/health_latest.md: human-readable Markdown report (latest only,
  overwritten each run, committed to repo as portfolio evidence)

Why a separate report file: someone reading the GitHub repo six months from
now should be able to glance at health_latest.md and understand what's
green/yellow/red without running anything. That's the harness eng pattern —
state is observable, not buried in logs.
"""

from __future__ import annotations

import json
import logging
import math
import sqlite3
import time
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from monitor.triggers import ALL_TRIGGERS, GREEN, RED, YELLOW, Trigger

log = logging.getLogger("health")


def assemble_state(
    db_path: Path,
    cost_log_path: Path,
    sources_yaml_path: Path | None = None,
) -> dict[str, Any]:
    """Read DB + cost log + sources.yaml, compute per-layer metrics. Returns a dict."""
    state: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "db_path": str(db_path),
    }

    # Load declared source IDs from sources.yaml so we can detect "in yaml but
    # never collected" (the failure mode caught in Session 7). Distinguish:
    # - declared (any active source not deferred / paywall / echo_only)
    # - declared_supported (subset whose primary kind the collector can fetch)
    # The difference between these two sets is "active but routed to HITL by
    # design" — those should NOT trigger the uncollected-sources alert.
    SUPPORTED_KINDS = frozenset({"rss", "scrape", "blog", "rss_partial"})

    def _primary_kinds(s: dict) -> list[str]:
        primary = s.get("primary")
        if isinstance(primary, list):
            return [c.get("kind") for c in primary if isinstance(c, dict)]
        if isinstance(primary, dict):
            return [primary.get("kind")]
        return []

    if sources_yaml_path and sources_yaml_path.exists():
        try:
            import yaml
            with sources_yaml_path.open() as f:
                yml = yaml.safe_load(f)
            declared = set()
            declared_supported = set()
            for s in (yml.get("sources") or []):
                if not isinstance(s, dict) or not s.get("id"):
                    continue
                if s.get("human_required"):
                    continue
                if s.get("mvp_active") is False:
                    continue
                if s.get("mvp_mode", "full") != "full":
                    continue
                sid = s["id"]
                declared.add(sid)
                if any(k in SUPPORTED_KINDS for k in _primary_kinds(s)):
                    declared_supported.add(sid)
            state["collector_declared_sources"] = declared
            state["collector_declared_supported_sources"] = declared_supported
        except Exception as e:  # noqa: BLE001
            log.warning("failed to read sources.yaml for declared-sources check: %s", e)

    if not db_path.exists():
        log.warning("DB not found at %s — first run? state will be empty.", db_path)
        return state

    conn = sqlite3.connect(db_path)
    try:
        # ---- Collector: per-source metrics ----
        per_source: dict[str, dict[str, Any]] = {}
        rows = conn.execute(
            """
            SELECT source_id,
                   COUNT(*) AS total,
                   SUM(CASE WHEN excerpt IS NOT NULL AND excerpt != '' THEN 1 ELSE 0 END) AS with_excerpt,
                   SUM(CASE WHEN scaffolding_note LIKE 'rss_unrecovered_%' THEN 1 ELSE 0 END) AS scrape_fallback,
                   MAX(fetched_at) AS last_fetched
              FROM items
             GROUP BY source_id
            """
        ).fetchall()
        now = datetime.now(timezone.utc)
        for source_id, total, with_excerpt, scrape_fallback, last_fetched in rows:
            extract_rate = (with_excerpt / total) if total else 0.0
            scrape_fallback_rate = (scrape_fallback / total) if total else 0.0
            days_ago = None
            if last_fetched:
                try:
                    last_dt = datetime.fromisoformat(last_fetched.replace("Z", "+00:00"))
                    days_ago = (now - last_dt).days
                except ValueError:
                    days_ago = None
            per_source[source_id] = {
                "total": total,
                "with_excerpt": with_excerpt,
                "extract_success_rate": round(extract_rate, 3),
                "scrape_fallback_rate": round(scrape_fallback_rate, 3),
                "last_fetched_at_days_ago": days_ago,
            }
        state["collector_per_source"] = per_source

        # Distinct source_ids that ever appeared in fetch_log (regardless of
        # outcome) — used by uncollected-sources trigger to distinguish
        # "never attempted" from "attempted with status=ok / items=0".
        state["collector_attempted_sources"] = {
            row[0] for row in conn.execute("SELECT DISTINCT source_id FROM fetch_log")
        }

        # ---- Triage: distribution + per-Pillar high-signal counts ----
        bucket_counts = {"high": 0, "watch": 0, "skip": 0, "untriaged": 0}
        for sig, count in conn.execute(
            """
            SELECT
                CASE
                    WHEN triage_signal IS NULL THEN 'untriaged'
                    WHEN triage_signal >= 0.6 THEN 'high'
                    WHEN triage_signal >= 0.3 THEN 'watch'
                    ELSE 'skip'
                END,
                COUNT(*)
              FROM items
             GROUP BY 1
            """
        ).fetchall():
            bucket_counts[sig] = count
        state["triage_buckets"] = bucket_counts

        # high-signal score stats (mean, stddev) for compression detection
        scores = [
            row[0] for row in conn.execute(
                "SELECT triage_signal FROM items WHERE triage_signal >= 0.6"
            )
        ]
        if scores:
            mean = sum(scores) / len(scores)
            var = sum((s - mean) ** 2 for s in scores) / len(scores)
            state["triage_high_signal_score_stats"] = {
                "count": len(scores),
                "mean": round(mean, 3),
                "stddev": round(math.sqrt(var), 3),
                "min": round(min(scores), 3),
                "max": round(max(scores), 3),
            }

        # high-signal per Pillar (parses triage_pillars JSON)
        per_pillar_counts: dict[int, int] = defaultdict(int)
        for (pillars_json,) in conn.execute(
            "SELECT triage_pillars FROM items WHERE triage_signal >= 0.6 AND triage_pillars IS NOT NULL"
        ):
            try:
                for p in json.loads(pillars_json):
                    if isinstance(p, int):
                        per_pillar_counts[p] += 1
            except json.JSONDecodeError:
                continue
        state["triage_high_signal_per_pillar"] = dict(per_pillar_counts)
    finally:
        conn.close()

    # ---- Cost: last 7d ----
    state["cost_last_7d_usd"] = _cost_last_n_days(cost_log_path, days=7)
    state["cost_total_usd"] = _cost_total(cost_log_path)

    return state


def _cost_last_n_days(cost_log_path: Path, *, days: int) -> float:
    if not cost_log_path.exists():
        return 0.0
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    total_cents = 0.0
    with cost_log_path.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
                if rec.get("dry_run"):
                    continue
                ts = datetime.fromisoformat(rec["ts"])
                if ts >= cutoff:
                    total_cents += rec.get("cents", 0)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    return round(total_cents / 100.0, 4)


def _cost_total(cost_log_path: Path) -> float:
    if not cost_log_path.exists():
        return 0.0
    total_cents = 0.0
    with cost_log_path.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
                if rec.get("dry_run"):
                    continue
                total_cents += rec.get("cents", 0)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    return round(total_cents / 100.0, 4)


def evaluate(state: dict[str, Any]) -> list[Trigger]:
    fired: list[Trigger] = []
    for fn in ALL_TRIGGERS:
        try:
            t = fn(state)
            if t:
                fired.append(t)
        except Exception as e:  # noqa: BLE001
            log.warning("trigger %s raised %s: %s", fn.__name__, type(e).__name__, e)
    return fired


def render_markdown(state: dict[str, Any], triggers: list[Trigger]) -> str:
    """Human-readable Markdown report. Designed to be commit-friendly."""
    lines: list[str] = []
    lines.append(f"# Pipeline Health Report")
    lines.append("")
    lines.append(f"_Generated: {state['ts']}_")
    lines.append("")
    lines.append("## Overall")
    if not triggers:
        lines.append(f"{GREEN} **All green.** No triggers fired.")
    else:
        red_n = sum(1 for t in triggers if t.severity == RED)
        yellow_n = sum(1 for t in triggers if t.severity == YELLOW)
        if red_n:
            lines.append(f"{RED} {red_n} red, {yellow_n} yellow")
        else:
            lines.append(f"{YELLOW} {yellow_n} yellow alert(s) — no reds")
    lines.append("")

    # snapshot of state
    lines.append("## State snapshot")
    lines.append("")
    lines.append("**Collector**:")
    sources = state.get("collector_per_source", {})
    if sources:
        active = sum(1 for m in sources.values() if (m.get("last_fetched_at_days_ago") or 999) <= 30)
        with_excerpt = sum(m["with_excerpt"] for m in sources.values())
        total = sum(m["total"] for m in sources.values())
        lines.append(f"- {len(sources)} sources tracked, {active} fetched in last 30 days")
        lines.append(f"- {with_excerpt} / {total} items have excerpt ({with_excerpt/total:.0%})" if total else "- no items yet")
    lines.append("")
    lines.append("**Triage**:")
    b = state.get("triage_buckets", {})
    lines.append(f"- high (≥0.6): {b.get('high', 0)} · watch (0.3–0.6): {b.get('watch', 0)} · skip: {b.get('skip', 0)} · untriaged: {b.get('untriaged', 0)}")
    stats = state.get("triage_high_signal_score_stats")
    if stats:
        lines.append(f"- high-signal score stats: mean={stats['mean']}, stddev={stats['stddev']}, range=[{stats['min']}, {stats['max']}]")
    pp = state.get("triage_high_signal_per_pillar", {})
    if pp:
        per_pillar = ", ".join(f"P{n}={c}" for n, c in sorted(pp.items()))
        lines.append(f"- high-signal per Pillar: {per_pillar}")
    lines.append("")
    lines.append("**Cost**:")
    lines.append(f"- last 7 days: ${state.get('cost_last_7d_usd', 0):.4f} (alarm at $5)")
    lines.append(f"- total to date: ${state.get('cost_total_usd', 0):.4f}")
    lines.append("")

    # triggered alerts
    if triggers:
        lines.append("## Triggered alerts")
        lines.append("")
        for t in triggers:
            lines.append(f"### {t.severity} [{t.layer}] {t.title}")
            lines.append("")
            lines.append("**Detail:**")
            lines.append("```")
            lines.append(t.detail)
            lines.append("```")
            lines.append("")
            lines.append("**Fix:**")
            lines.append("")
            lines.append(t.fix)
            lines.append("")
            if t.reference:
                lines.append(f"_Reference: {t.reference}_")
                lines.append("")
    return "\n".join(lines) + "\n"


def append_health_log(state: dict, triggers: list[Trigger], log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": state["ts"],
        "trigger_count": len(triggers),
        "triggers": [asdict(t) for t in triggers],
        "state": state,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_latest_markdown(markdown: str, md_path: Path) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown, encoding="utf-8")
