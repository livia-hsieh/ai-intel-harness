"""Foundation CLI — Opus weekly curriculum-driven deep-read.

Usage:
    foundation                            # auto-derive track from current week
    foundation --week 2026-W19            # explicit week (auto-derives track)
    foundation --track D                  # force a specific track
    foundation --track D --week 2026-W19  # both
    foundation --dry-run                  # cost forecast only

Per SCOPE.md §2 Pillar 4 the curriculum rotates 12 weeks:
    W1, W2  → B (Prompt + Context Engineering)
    W3, W4  → C (Agent architectures)
    W5, W6  → D (Evals)
    W7, W8  → E (Tools & infra)
    W9, W10 → F (Deployment discipline)
    W11, W12→ G (Governance & safety)
    W13+    → cycle restarts (B v2)

Writes:
- digests/<week>/foundation.md (committed to repo)
- <wiki_root>/concepts/<topic-slug>.md (sediment to 知識庫 if reachable)
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from collector.storage import Storage
from synthesizer.client import Client
from synthesizer.foundation import run_foundation, write_foundation_to_files
from synthesizer.prompts import TRACK_TOPICS, track_for_week
from synthesizer.triage import load_sources_indexed

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES_PATH = REPO_ROOT / "sources.yaml"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "dedup.sqlite"
DEFAULT_COST_LOG = REPO_ROOT / "data" / "cost_log.jsonl"
DEFAULT_WIKI_PATH = Path("/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫/wiki")

log = logging.getLogger("foundation-cli")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    week_label = args.week or datetime.now().strftime("%Y-W%V")
    track_id = args.track
    if track_id is None:
        try:
            week_n = int(week_label.split("-W")[-1])
            track_id = track_for_week(week_n)
        except ValueError:
            track_id = "B"

    if track_id not in TRACK_TOPICS:
        log.error("unknown track %r; valid: %s", track_id, sorted(TRACK_TOPICS.keys()))
        return 2

    storage = Storage(args.db)
    sources = load_sources_indexed(args.sources)
    client = Client(cost_log_path=args.cost_log, dry_run=args.dry_run)

    result = run_foundation(
        storage,
        sources,
        week_label=week_label,
        track_id=track_id,
        client=client,
        max_items=args.max_items,
    )

    if args.dry_run:
        print(f"\n=== Foundation dry-run ===")
        print(f"  Week:      {result.week_label}")
        print(f"  Track:     {result.track_id} — {result.track_name}")
        print(f"  Items:     {result.item_count}")
        print(f"  Est cost:  ${result.cents / 100:.4f} USD (uncached)")
        return 0

    if args.write:
        digest_path, wiki_path = write_foundation_to_files(
            result,
            REPO_ROOT,
            wiki_root=args.wiki_root if args.wiki_root.exists() else None,
        )
        print(f"\n=== Foundation Track {result.track_id} written ===")
        print(f"  digest: {digest_path}")
        if wiki_path:
            print(f"  wiki:   {wiki_path}")
        else:
            print(f"  wiki:   (skipped — {args.wiki_root} not reachable)")
        print(f"  cost:   ${result.cents / 100:.4f} USD")
    else:
        print()
        print("=" * 100)
        print(f"# Foundation — Track {result.track_id}: {result.track_name}")
        print(f"# Week {result.week_label} · {result.item_count} items · ${result.cents / 100:.4f} USD")
        print("=" * 100)
        print(result.essay_markdown)

    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="foundation", description="Opus weekly Foundation deep-read.")
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--sources", type=Path, default=DEFAULT_SOURCES_PATH)
    p.add_argument("--cost-log", type=Path, default=DEFAULT_COST_LOG)
    p.add_argument(
        "--week",
        type=str,
        help="Week label (e.g. 2026-W19); defaults to current ISO week",
    )
    p.add_argument(
        "--track",
        type=str,
        choices=sorted(TRACK_TOPICS.keys()),
        help="Force a specific track (B/C/D/E/F/G); else derived from week",
    )
    p.add_argument("--max-items", type=int, default=25,
                   help="High-signal items to feed Opus (default 25)")
    p.add_argument("--write", action="store_true",
                   help="Write to digests/<week>/foundation.md and wiki path (default: stdout)")
    p.add_argument("--wiki-root", type=Path, default=DEFAULT_WIKI_PATH,
                   help=f"Wiki root path (default: {DEFAULT_WIKI_PATH})")
    p.add_argument("--dry-run", action="store_true", help="No API calls; estimate cost only")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
