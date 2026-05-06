"""Health CLI.

Usage:
    health                        # full check; prints to stdout, writes markdown + jsonl
    health --quiet                # write files only, no stdout
    health --no-write             # only print, don't write files (smoke test)

The Markdown report at data/health_latest.md is intentionally repo-friendly:
commit it after each weekly digest run so the repo's git history shows
pipeline health over time. That's portfolio gold — anyone scrolling commits
sees "the pipeline is alive and self-monitoring", not just code.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from monitor.health import (
    append_health_log,
    assemble_state,
    evaluate,
    render_markdown,
    write_latest_markdown,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "data" / "dedup.sqlite"
DEFAULT_COST_LOG = REPO_ROOT / "data" / "cost_log.jsonl"
DEFAULT_HEALTH_LOG = REPO_ROOT / "data" / "health_log.jsonl"
DEFAULT_HEALTH_MD = REPO_ROOT / "data" / "health_latest.md"


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if not args.verbose else logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    state = assemble_state(args.db, args.cost_log)
    triggers = evaluate(state)
    md = render_markdown(state, triggers)

    if not args.quiet:
        print(md)

    if not args.no_write:
        append_health_log(state, triggers, args.health_log)
        write_latest_markdown(md, args.health_md)
        print(f"\n_log: {args.health_log}_")
        print(f"_md:  {args.health_md}_")

    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="health", description="Pipeline health monitor.")
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--cost-log", type=Path, default=DEFAULT_COST_LOG)
    p.add_argument("--health-log", type=Path, default=DEFAULT_HEALTH_LOG)
    p.add_argument("--health-md", type=Path, default=DEFAULT_HEALTH_MD)
    p.add_argument("--quiet", action="store_true", help="Don't print report; only write files")
    p.add_argument("--no-write", action="store_true", help="Print only; don't write files")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
