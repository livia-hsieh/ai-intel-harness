"""Sonnet-driven Pulse synthesis: per-Pillar weekly briefing.

Pulls high-signal triaged items for ONE Pillar from the DB, sends them as a
single batch to Sonnet 4.6 (system prompt cached), gets back a Markdown
briefing per the contract in synthesizer/prompts.py PULSE_SYSTEM.

Output target depends on caller:
- stdout (default; for iteration / smoke tests)
- file: digests/<week>/pillar-<n>.md (when --write set; assembled later by
  delivery layer into the final weekly digest)

Per SCOPE.md §5 the digest's overall shape includes TL;DR + Coverage Check
sections that are NOT this stage's responsibility — those come from a final
digest-assembly step (Task #5 / delivery) that consumes all 5 Pillar Pulse
outputs + Foundation deep-read.

Cost expectation per Pillar at ~30 high-signal items:
- ~10 KB input (system + items) → ~3000 tokens fresh on first call,
  ~2000 cache_read on subsequent Pillar calls within 5 min
- ~2-3 KB Markdown output → ~700 tokens
- Sonnet pricing: $3/M input, $0.30/M cache_read, $15/M output
- Per-Pillar cost: ~3-5 cents. 5 Pillars: ~$0.20/digest.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from collector.config import Source
from collector.storage import Storage
from synthesizer.client import MODEL_PULSE, Client
from synthesizer.prompts import PILLAR_NAMES, PULSE_SYSTEM, pulse_user_message

log = logging.getLogger("pulse")


@dataclass
class PulseResult:
    pillar_n: int
    pillar_name: str
    item_count: int
    briefing_markdown: str
    cents: float


def run_pulse(
    storage: Storage,
    sources_by_id: dict[str, Source],
    *,
    pillar_n: int,
    client: Client,
    min_signal: float = 0.6,
    published_after: str | None = None,
    max_items: int | None = 40,
) -> PulseResult:
    """Synthesize Pulse for one Pillar.

    `max_items` default 40: Pillar 4 backlog has 760 items which blows past
    Sonnet's 30K input-tokens-per-minute org rate limit. 40 highest-signal
    items keep us within rate limits + give Sonnet enough breadth to pick
    real Top 3 with a healthy Watch list. Items are pre-sorted by
    triage_signal DESC inside list_high_signal_items_for_pillar so we keep
    the best 40, not arbitrary 40.
    """
    if pillar_n not in PILLAR_NAMES:
        raise ValueError(f"unknown pillar {pillar_n}")
    pillar_name = PILLAR_NAMES[pillar_n]

    raw_items = storage.list_high_signal_items_for_pillar(
        pillar_n, min_signal=min_signal, published_after=published_after
    )
    if max_items:
        raw_items = raw_items[:max_items]

    log.info(
        "pillar %d (%s): %d high-signal items (min_signal=%.2f)",
        pillar_n, pillar_name, len(raw_items), min_signal,
    )

    if not raw_items:
        return PulseResult(
            pillar_n=pillar_n,
            pillar_name=pillar_name,
            item_count=0,
            briefing_markdown=f"## Pulse — Top 3\n\n_(本期無高訊號 items for Pillar {pillar_n})_\n",
            cents=0.0,
        )

    # Enrich items with source name (Pulse prompt uses source_name, not source_id).
    items_for_prompt = []
    for it in raw_items:
        src = sources_by_id.get(it["source_id"])
        items_for_prompt.append({
            **it,
            "source_name": src.name if src else it["source_id"],
        })

    user_msg = pulse_user_message(
        pillar_n=pillar_n,
        pillar_name=pillar_name,
        items=items_for_prompt,
    )

    result = client.call(
        model=MODEL_PULSE,
        system=PULSE_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=4096,
        purpose=f"pulse:pillar-{pillar_n}",
    )

    return PulseResult(
        pillar_n=pillar_n,
        pillar_name=pillar_name,
        item_count=len(raw_items),
        briefing_markdown=result.text,
        cents=result.cents,
    )


def write_pulse_to_file(result: PulseResult, repo_root: Path, week_label: str) -> Path:
    """Write the Pulse Markdown to digests/<week>/pillar-<n>.md.

    `week_label` is e.g. "2026-W18". The directory is created if missing.
    """
    out_dir = repo_root / "digests" / week_label
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"pillar-{result.pillar_n}.md"
    header = (
        f"# Pillar {result.pillar_n} — {result.pillar_name}\n\n"
        f"_{result.item_count} high-signal items synthesized · "
        f"{result.cents/100:.4f} USD_\n\n"
    )
    out_path.write_text(header + result.briefing_markdown + "\n", encoding="utf-8")
    return out_path
