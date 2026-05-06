"""Synthesizer CLI.

Usage:
    triage                       # triage all un-triaged items (full weekly run)
    triage --limit 20            # first 20 (smoke test / quick check)
    triage --dry-run             # estimate cost without calling the API
    triage --source openai-blog  # only items from one source

Cost forecasting:
    triage --dry-run --limit 100  → prints estimated cents per Haiku call
                                     so you can pre-flight a full run.

Prereq: export ANTHROPIC_API_KEY=sk-ant-...   (skip when --dry-run)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from collector.storage import Storage
from synthesizer.client import Client
from synthesizer.triage import load_sources_indexed, run_triage

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES_PATH = REPO_ROOT / "sources.yaml"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "dedup.sqlite"
DEFAULT_COST_LOG = REPO_ROOT / "data" / "cost_log.jsonl"

log = logging.getLogger("synthesizer")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    storage = Storage(args.db)
    sources = load_sources_indexed(args.sources)
    log.info("loaded %d sources", len(sources))

    if args.source and args.source not in sources:
        log.error("source id %r not in sources.yaml", args.source)
        return 2

    client = Client(cost_log_path=args.cost_log, dry_run=args.dry_run)
    summary = run_triage(
        storage, sources, client=client, limit=args.limit, source_id=args.source
    )
    _print_summary(summary, dry_run=args.dry_run)
    return 0


def _print_summary(summary: dict, *, dry_run: bool) -> None:
    print("\n=== triage summary ===")
    mode = "DRY RUN (no API calls; cost estimate only)" if dry_run else "live"
    print(f"  mode:        {mode}")
    print(f"  items seen:  {summary['items_seen']}")
    print(f"  decided:     {summary['decided']}")
    print(f"  errors:      {summary['errors']}")
    print()
    print(f"  high signal (≥0.6):  {summary['high_signal']}")
    print(f"  watch (0.3–0.6):     {summary['watch']}")
    print(f"  skip (<0.3):         {summary['skip']}")
    print()
    print(f"  total cost:  {summary['total_cents'] / 100:.4f} USD")
    if summary["decided"]:
        print(f"  per-item:    {summary['total_cents'] / summary['decided']:.4f} cents/item")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="triage", description="Haiku triage over un-triaged items.")
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--sources", type=Path, default=DEFAULT_SOURCES_PATH)
    p.add_argument("--cost-log", type=Path, default=DEFAULT_COST_LOG)
    p.add_argument("--limit", type=int, help="Triage at most this many items")
    p.add_argument(
        "--source",
        type=str,
        help="Only triage items from this source id (per-Pillar calibration runs)",
    )
    p.add_argument("--dry-run", action="store_true", help="No API calls; estimate cost only")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
