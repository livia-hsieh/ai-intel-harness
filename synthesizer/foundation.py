"""Opus 4.6 Foundation deep-read: weekly curriculum-driven essay.

Per SCOPE.md §2 Pillar 4, Foundation rotates through Tracks B→C→D→E→F→G
on a 12-week cycle. Each call produces a 2000–3000 word wiki-quality essay
that goes into both the weekly digest AND Livia's 知識庫 wiki.

Foundation is intentionally distinct from Pulse:
- Pulse synthesizes "what happened this week" across 5 Pillars
- Foundation synthesizes "what we now understand about <one topic>"
- Pulse uses Sonnet (cheaper, faster); Foundation uses Opus (deeper)
- Pulse output is briefer (Top 3 + Watch); Foundation output is essay-length
- Foundation MUST include Mermaid diagrams for complex concepts

Cost expectation per Foundation run:
- Input: ~5K-8K tokens (system prompt cached + 15-25 high-signal items
  with full excerpts)
- Output: ~3K-4K tokens (essay with diagrams)
- Opus pricing: $15/M input, $75/M output, $1.50/M cache_read
- Per run: ~$0.30 (cached) to ~$0.50 (cold-start)
- Annual: 52 runs × $0.30 = ~$16
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from collector.config import Source
from collector.storage import Storage
from synthesizer.client import MODEL_FOUNDATION, Client
from synthesizer.prompts import (
    FOUNDATION_SYSTEM,
    TRACK_TOPICS,
    foundation_user_message,
    track_for_week,
)

log = logging.getLogger("foundation")


@dataclass
class FoundationResult:
    track_id: str
    track_name: str
    week_label: str
    item_count: int
    essay_markdown: str
    cents: float


def run_foundation(
    storage: Storage,
    sources_by_id: dict[str, Source],
    *,
    week_label: str,
    track_id: str | None = None,
    client: Client,
    min_signal: float = 0.6,
    max_items: int = 25,
    pillar_filter: list[int] | None = None,
) -> FoundationResult:
    """Synthesize the Foundation deep-read for the week's curriculum track.

    `track_id`: explicit override (e.g. "C"); else derived from week number.
    `pillar_filter`: which Pillars to draw items from. Default = Pillar 4 + 3
        (most curriculum tracks are harness-eng + frontier-capability).
    """
    if track_id is None:
        # Parse week number from label like "2026-W19"
        try:
            week_n = int(week_label.split("-W")[-1])
        except ValueError:
            week_n = 1
        track_id = track_for_week(week_n)

    track = TRACK_TOPICS.get(track_id)
    if not track:
        raise ValueError(f"unknown track {track_id}; valid: {sorted(TRACK_TOPICS.keys())}")

    # Default Pillar selection per track. Most tracks are P4-heavy.
    track_pillars = pillar_filter or {
        "B": [4],
        "C": [3, 4],
        "D": [3, 4],
        "E": [4],
        "F": [1, 4],
        "G": [2, 4],
    }.get(track_id, [4])

    # Pull high-signal items from the relevant Pillars, dedupe by item id.
    items_by_id: dict[int, dict] = {}
    for p in track_pillars:
        for it in storage.list_high_signal_items_for_pillar(p, min_signal=min_signal):
            items_by_id[it["id"]] = it
    items = sorted(items_by_id.values(), key=lambda x: -x["signal"])[:max_items]

    log.info(
        "Foundation Track %s (%s) for %s: %d items from Pillars %s",
        track_id, track["name"], week_label, len(items), track_pillars,
    )

    if not items:
        return FoundationResult(
            track_id=track_id,
            track_name=track["name"],
            week_label=week_label,
            item_count=0,
            essay_markdown=f"# Foundation — Track {track_id}: {track['name']}\n\n_(no high-signal items this week)_\n",
            cents=0.0,
        )

    # Enrich with source name (prompt prefers names over ids)
    items_for_prompt = []
    for it in items:
        src = sources_by_id.get(it["source_id"])
        items_for_prompt.append({
            **it,
            "source_name": src.name if src else it["source_id"],
        })

    user_msg = foundation_user_message(
        track_id=track_id,
        week_label=week_label,
        items=items_for_prompt,
    )

    result = client.call(
        model=MODEL_FOUNDATION,
        system=FOUNDATION_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=8000,  # essay-length output (3000-4000 tokens) + diagrams
        purpose=f"foundation:track-{track_id}:{week_label}",
    )

    return FoundationResult(
        track_id=track_id,
        track_name=track["name"],
        week_label=week_label,
        item_count=len(items),
        essay_markdown=result.text,
        cents=result.cents,
    )


def write_foundation_to_files(
    result: FoundationResult,
    repo_root: Path,
    wiki_root: Path | None = None,
) -> tuple[Path, Path | None]:
    """Write the Foundation essay to two locations:
    1. digests/<week>/foundation.md  — weekly digest component
    2. <wiki_root>/concepts/<topic-slug>.md  — long-term wiki sediment

    Wiki path slugifies the track name. Caller can pass wiki_root=None to
    skip wiki write (useful when wiki path isn't accessible from current
    environment, e.g., GitHub Actions).
    """
    week_dir = repo_root / "digests" / result.week_label
    week_dir.mkdir(parents=True, exist_ok=True)
    digest_path = week_dir / "foundation.md"

    header = (
        f"# Foundation — Track {result.track_id}: {result.track_name}\n\n"
        f"_Week {result.week_label} · {result.item_count} items synthesized · "
        f"${result.cents / 100:.4f} USD_\n\n"
    )
    digest_path.write_text(header + result.essay_markdown + "\n", encoding="utf-8")

    wiki_path = None
    if wiki_root and wiki_root.exists():
        slug = result.track_name.lower().replace(" ", "-").replace("/", "-")
        # Strip non-ascii for wiki filename safety
        ascii_slug = "".join(c if ord(c) < 128 and (c.isalnum() or c in "-_") else "" for c in slug)
        if not ascii_slug:
            ascii_slug = f"track-{result.track_id.lower()}"
        wiki_dir = wiki_root / "concepts"
        wiki_dir.mkdir(parents=True, exist_ok=True)
        wiki_path = wiki_dir / f"{ascii_slug}.md"
        wiki_header = (
            f"# {result.track_name}\n\n"
            f"_Foundation deep-read · first written {result.week_label} · "
            f"_(this file is auto-sedimented from `digests/{result.week_label}/foundation.md` — "
            f"manual edits should be reflected back to the digest source)_\n\n"
        )
        wiki_path.write_text(wiki_header + result.essay_markdown + "\n", encoding="utf-8")

    return digest_path, wiki_path
