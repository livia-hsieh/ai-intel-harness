"""Opus quarterly synthesis: cross-Track integrated view of harness engineering.

Runs once per quarter (every 12 weeks, after a full B→G curriculum cycle).
Reads the 6 Track wiki essays + this quarter's high-signal items + recent
Pulse outputs. Produces a single ~5000-word integrated synthesis written to
the wiki/perspectives/ directory.

Why this exists: weekly Foundation deep-reads cover ONE Track at a time.
After 12 weeks, Livia has 6 vertical Track essays but no horizontal
integration. The quarterly synthesis fixes that — see
synthesizer/prompts.py QUARTERLY_SYNTHESIS_SYSTEM for full design.

Cost: ~$1-2 per quarterly run (Opus, larger context than Foundation since
it ingests all 6 Track essays). Annual: 4 quarters × $1.5 = ~$6.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from collector.config import Source
from collector.storage import Storage
from synthesizer.client import MODEL_FOUNDATION, Client
from synthesizer.prompts import (
    QUARTERLY_SYNTHESIS_SYSTEM,
    TRACK_TOPICS,
    quarter_for_week,
    quarterly_user_message,
)

log = logging.getLogger("quarterly")


@dataclass
class QuarterlyResult:
    quarter_label: str
    track_essays_used: list[str]
    item_count: int
    week_count: int
    synthesis_markdown: str
    cents: float


def _read_track_essays(wiki_root: Path) -> dict[str, str]:
    """Find Foundation track essays already sedimented to wiki.

    Looks under wiki_root/concepts/ for files named track-<x>.md (the
    sediment naming convention used by foundation.write_foundation_to_files).
    Returns {track_id: essay_content}. Tracks that haven't been written yet
    are silently skipped — quarterly synthesis can run on partial data with
    a caveat in the synthesis itself.
    """
    essays: dict[str, str] = {}
    concepts_dir = wiki_root / "concepts"
    if not concepts_dir.exists():
        return essays
    for track_id in TRACK_TOPICS.keys():
        candidate = concepts_dir / f"track-{track_id.lower()}.md"
        if candidate.exists():
            essays[track_id] = candidate.read_text(encoding="utf-8")
    return essays


def _gather_quarter_items(storage: Storage, sources_by_id: dict[str, Source]) -> list[dict]:
    """Top-30 high-signal items across all Pillars for the quarter.

    For now: pull all high-signal items (≥0.6) across all Pillars, sort by
    signal × Pillar 4 weight (Pillar 4 is our harness-eng main interest),
    take top 30 deduped by item id.
    """
    seen: dict[int, dict] = {}
    for p in [4, 3, 2, 1, 5]:
        for it in storage.list_high_signal_items_for_pillar(p, min_signal=0.7):
            seen[it["id"]] = it
    items = list(seen.values())
    items.sort(key=lambda x: -x.get("signal", 0))
    # enrich with source name
    out = []
    for it in items:
        src = sources_by_id.get(it["source_id"])
        out.append({**it, "source_name": src.name if src else it["source_id"]})
    return out


def run_quarterly_synthesis(
    storage: Storage,
    sources_by_id: dict[str, Source],
    *,
    quarter_label: str | None = None,
    wiki_root: Path,
    client: Client,
    week_count: int = 12,
    min_tracks: int = 5,
    force: bool = False,
) -> QuarterlyResult:
    """Quarterly synthesis with min-track guard.

    `min_tracks`: minimum number of Track essays needed for a meaningful
        synthesis. Default 5 — synthesizing fewer would produce a thin
        quarterly that doesn't justify the cost. Auto-trigger respects
        this guard; manual `--force` overrides.
    `force`: skip the min_tracks guard and synthesize whatever is available.
    """
    if quarter_label is None:
        now = datetime.now()
        try:
            iso_year, iso_week, _ = now.isocalendar()
        except Exception:
            iso_year, iso_week = now.year, 1
        quarter_label = quarter_for_week(iso_week, iso_year)

    track_essays = _read_track_essays(wiki_root)
    items = _gather_quarter_items(storage, sources_by_id)

    log.info(
        "Quarterly synthesis %s: %d Track essays available (%s), %d high-signal items",
        quarter_label,
        len(track_essays),
        sorted(track_essays.keys()),
        len(items),
    )

    if not track_essays:
        # No Foundation essays yet → can't synthesize, fail soft.
        return QuarterlyResult(
            quarter_label=quarter_label,
            track_essays_used=[],
            item_count=len(items),
            week_count=week_count,
            synthesis_markdown=(
                f"# 本季 Harness Engineering 整合視角 — {quarter_label}\n\n"
                f"_(無 Track 深讀可整合。請先連續跑滿 12 週 weekly digest 累積 "
                f"Track B–G 各一篇，再回來執行 quarterly synthesis。)_\n"
            ),
            cents=0.0,
        )

    if len(track_essays) < min_tracks and not force:
        # Below quality bar — synthesizing on too few tracks produces a thin
        # quarterly that doesn't justify the cost. Skip auto-run; user can
        # override with --force if they want a partial synthesis anyway.
        return QuarterlyResult(
            quarter_label=quarter_label,
            track_essays_used=sorted(track_essays.keys()),
            item_count=len(items),
            week_count=week_count,
            synthesis_markdown=(
                f"# 本季 Harness Engineering 整合視角 — {quarter_label}\n\n"
                f"_(only {len(track_essays)} of {min_tracks} required Track essays "
                f"available — auto-synthesis skipped to avoid thin output. "
                f"Use `synthesize-quarter --force` to synthesize anyway.)_\n\n"
                f"Available tracks: {sorted(track_essays.keys())}\n"
                f"Missing tracks: {sorted(set('BCDEFG') - set(track_essays.keys()))}\n"
            ),
            cents=0.0,
        )

    user_msg = quarterly_user_message(
        quarter_label=quarter_label,
        track_essays=track_essays,
        high_signal_items=items,
        week_count=week_count,
    )

    result = client.call(
        model=MODEL_FOUNDATION,  # Opus — synthesis quality matters most here
        system=QUARTERLY_SYNTHESIS_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=12000,  # quarterly is essay-length × 2 (繁中 + EN mirror)
        purpose=f"quarterly:{quarter_label}",
    )

    return QuarterlyResult(
        quarter_label=quarter_label,
        track_essays_used=sorted(track_essays.keys()),
        item_count=len(items),
        week_count=week_count,
        synthesis_markdown=result.text,
        cents=result.cents,
    )


def write_quarterly_to_wiki(result: QuarterlyResult, wiki_root: Path) -> Path:
    """Sediment to wiki/perspectives/harness-engineering-<quarter>.md."""
    perspectives_dir = wiki_root / "perspectives"
    perspectives_dir.mkdir(parents=True, exist_ok=True)
    out_path = perspectives_dir / f"harness-engineering-{result.quarter_label.lower()}.md"
    header = (
        f"# Harness Engineering — {result.quarter_label} Integrated View\n\n"
        f"_本季合成基於 {len(result.track_essays_used)} 篇 Foundation Track 深讀 "
        f"({', '.join('Track ' + t for t in result.track_essays_used)}) "
        f"+ {result.item_count} 篇 high-signal items。_\n\n"
        f"_Synthesis cost: ${result.cents/100:.4f} USD_\n\n"
    )
    out_path.write_text(header + result.synthesis_markdown + "\n", encoding="utf-8")
    return out_path
