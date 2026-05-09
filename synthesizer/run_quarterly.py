"""Quarterly synthesis CLI.

Usage:
    synthesize-quarter                       # auto-derive quarter from current week
    synthesize-quarter --quarter Q1-2026     # explicit quarter
    synthesize-quarter --dry-run             # cost estimate only
    synthesize-quarter --write               # write to wiki/perspectives/

When run before 12 weeks of Foundation have accumulated, the runner gives
a friendly message and writes a placeholder explaining the prerequisite —
no API call is made, $0 cost.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from collector.storage import Storage
from synthesizer.client import Client
from synthesizer.prompts import quarter_for_week
from synthesizer.quarterly import run_quarterly_synthesis, write_quarterly_to_wiki
from synthesizer.triage import load_sources_indexed

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES_PATH = REPO_ROOT / "sources.yaml"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "dedup.sqlite"
DEFAULT_COST_LOG = REPO_ROOT / "data" / "cost_log.jsonl"
DEFAULT_WIKI_PATH = Path("/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫/wiki")

log = logging.getLogger("quarterly-cli")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    quarter = args.quarter
    if quarter is None:
        now = datetime.now()
        try:
            iso_year, iso_week, _ = now.isocalendar()
        except Exception:
            iso_year, iso_week = now.year, 1
        quarter = quarter_for_week(iso_week, iso_year)

    storage = Storage(args.db)
    sources = load_sources_indexed(args.sources)
    client = Client(cost_log_path=args.cost_log, dry_run=args.dry_run, hard_cap_usd=10.0)

    result = run_quarterly_synthesis(
        storage,
        sources,
        quarter_label=quarter,
        wiki_root=args.wiki_root,
        client=client,
        week_count=args.weeks,
    )

    if args.dry_run:
        print(f"\n=== Quarterly synthesis dry-run ===")
        print(f"  Quarter:           {result.quarter_label}")
        print(f"  Track essays used: {result.track_essays_used}")
        print(f"  Items used:        {result.item_count}")
        print(f"  Est cost:          ${result.cents / 100:.4f} USD")
        return 0

    if not result.track_essays_used:
        print()
        print("=" * 80)
        print(f"Quarterly synthesis SKIPPED for {result.quarter_label}")
        print("=" * 80)
        print(result.synthesis_markdown)
        print()
        print("Cost: $0 (no API call made — prerequisite Foundation essays missing)")
        return 0

    if args.write:
        if not args.wiki_root.exists():
            print(f"⚠️  Wiki root {args.wiki_root} not reachable; printing to stdout instead")
            print(result.synthesis_markdown)
            return 0
        out_path = write_quarterly_to_wiki(result, args.wiki_root)
        print(f"\n=== Quarterly Synthesis written ===")
        print(f"  wiki:    {out_path}")
        print(f"  quarter: {result.quarter_label}")
        print(f"  tracks:  {result.track_essays_used}")
        print(f"  cost:    ${result.cents / 100:.4f} USD")
    else:
        print()
        print("=" * 100)
        print(f"# Quarterly Synthesis — {result.quarter_label}")
        print(f"# {len(result.track_essays_used)} tracks · {result.item_count} items · ${result.cents / 100:.4f} USD")
        print("=" * 100)
        print(result.synthesis_markdown)
    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="synthesize-quarter",
        description="Opus quarterly synthesis: cross-Track integrated view.",
    )
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--sources", type=Path, default=DEFAULT_SOURCES_PATH)
    p.add_argument("--cost-log", type=Path, default=DEFAULT_COST_LOG)
    p.add_argument("--quarter", type=str,
                   help="Quarter label (e.g. Q1-2026); defaults to current quarter")
    p.add_argument("--weeks", type=int, default=12,
                   help="Number of weeks this quarter spans (default 12)")
    p.add_argument("--write", action="store_true",
                   help="Write to wiki/perspectives/ (else stdout)")
    p.add_argument("--wiki-root", type=Path, default=DEFAULT_WIKI_PATH)
    p.add_argument("--dry-run", action="store_true", help="No API calls; estimate cost only")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
