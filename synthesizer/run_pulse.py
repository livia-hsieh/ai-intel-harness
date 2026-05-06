"""Pulse CLI — Sonnet weekly per-Pillar synthesis.

Usage:
    pulse --pillar 4                    # synthesize Pillar 4 from triaged items, print to stdout
    pulse --pillar 4 --dry-run          # cost forecast only
    pulse --pillar 4 --write 2026-W18   # write to digests/2026-W18/pillar-4.md
    pulse --all                         # all 5 Pillars, print sequentially
    pulse --all --write 2026-W18        # all 5, write each to file

Prereq: export ANTHROPIC_API_KEY=sk-ant-...   (skip when --dry-run)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from collector.storage import Storage
from synthesizer.client import Client
from synthesizer.prompts import PILLAR_NAMES
from synthesizer.pulse import PulseResult, run_pulse, write_pulse_to_file
from synthesizer.triage import load_sources_indexed

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES_PATH = REPO_ROOT / "sources.yaml"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "dedup.sqlite"
DEFAULT_COST_LOG = REPO_ROOT / "data" / "cost_log.jsonl"

log = logging.getLogger("pulse-cli")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    if not args.all and args.pillar is None:
        log.error("must specify --pillar N or --all")
        return 2

    pillars: list[int] = list(PILLAR_NAMES.keys()) if args.all else [args.pillar]

    storage = Storage(args.db)
    sources = load_sources_indexed(args.sources)
    client = Client(cost_log_path=args.cost_log, dry_run=args.dry_run)

    total_cents = 0.0
    results: list[PulseResult] = []

    for n in pillars:
        result = run_pulse(
            storage,
            sources,
            pillar_n=n,
            client=client,
            min_signal=args.min_signal,
            published_after=args.published_after,
            max_items=args.max_items,
        )
        results.append(result)
        total_cents += result.cents

        if args.write:
            out_path = write_pulse_to_file(result, REPO_ROOT, args.write)
            log.info("wrote %s", out_path)
        else:
            print()
            print("=" * 100)
            print(f"# Pillar {result.pillar_n} — {result.pillar_name}")
            print(f"# {result.item_count} items · {result.cents/100:.4f} USD")
            print("=" * 100)
            print(result.briefing_markdown)

    print()
    print("=" * 60)
    print("Pulse run summary")
    print("=" * 60)
    for r in results:
        print(f"  Pillar {r.pillar_n} ({r.pillar_name[:30]:30}) "
              f"items={r.item_count:>3}  cents={r.cents:.4f}")
    print(f"  TOTAL: {total_cents / 100:.4f} USD")
    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="pulse", description="Sonnet weekly per-Pillar synthesis.")
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--sources", type=Path, default=DEFAULT_SOURCES_PATH)
    p.add_argument("--cost-log", type=Path, default=DEFAULT_COST_LOG)
    p.add_argument(
        "--pillar",
        type=int,
        choices=sorted(PILLAR_NAMES.keys()),
        help="Synthesize one Pillar (1–5)",
    )
    p.add_argument("--all", action="store_true", help="Synthesize all 5 Pillars")
    p.add_argument(
        "--min-signal",
        type=float,
        default=0.6,
        help="Minimum triage signal to include (default 0.6)",
    )
    p.add_argument(
        "--published-after",
        type=str,
        help="ISO8601: only items published after this date (e.g. 2026-04-29 for last week)",
    )
    p.add_argument(
        "--max-items",
        type=int,
        help="Hard cap on items per Pillar (defensive; defaults to no cap)",
    )
    p.add_argument(
        "--write",
        type=str,
        metavar="WEEK",
        help="Write to digests/<WEEK>/pillar-<N>.md instead of stdout (e.g. 2026-W18)",
    )
    p.add_argument("--dry-run", action="store_true", help="No API calls; estimate cost only")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
