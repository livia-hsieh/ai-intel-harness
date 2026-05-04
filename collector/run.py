"""Orchestrator — wide scan over all sources defined in sources.yaml.

Run modes:
    collect                    # all sources
    collect --source <id>      # one source (debug)
    collect --limit-sources N  # first N sources (smoke test)
    collect --dry-run          # show plan, don't fetch

Output: SQLite at data/dedup.sqlite + a one-line summary to stdout per source.
The summary is intentionally terse (portfolio-readable when piped to a log).
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from collections.abc import Iterator
from pathlib import Path

from collector.config import Source, load_sources
from collector.fetchers import fetch_rss, fetch_scrape
from collector.fetchers.rss import FetchError
from collector.storage import Item, Storage

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES_PATH = REPO_ROOT / "sources.yaml"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "dedup.sqlite"

log = logging.getLogger("collector")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if not args.verbose else logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    sources = load_sources(args.sources)
    if args.source:
        sources = [s for s in sources if s.id == args.source]
        if not sources:
            log.error("source id %r not found", args.source)
            return 2
    elif args.limit_sources:
        sources = sources[: args.limit_sources]

    log.info("loaded %d sources from %s", len(sources), args.sources)

    if args.dry_run:
        _print_plan(sources)
        return 0

    storage = Storage(args.db)
    summary = _run(storage, sources)
    _print_summary(summary, storage)
    return 0


def _run(storage: Storage, sources: list[Source]) -> dict[str, int]:
    summary = {"ok": 0, "error": 0, "hitl": 0, "items_new": 0, "items_dup": 0}

    for source in sources:
        if not source.is_supported:
            storage.queue_hitl(source.id, source.hitl_reason or "unknown")
            log.info("HITL  %-40s reason=%s", source.id, source.hitl_reason)
            summary["hitl"] += 1
            continue

        log_id = storage.start_fetch(source.id)
        t0 = time.time()
        try:
            items_seen, items_new = _fetch_and_store(storage, source)
            storage.finish_fetch(log_id, "ok", items_seen=items_seen, items_new=items_new)
            summary["ok"] += 1
            summary["items_new"] += items_new
            summary["items_dup"] += items_seen - items_new
            log.info(
                "OK    %-40s seen=%-3d new=%-3d %.1fs",
                source.id, items_seen, items_new, time.time() - t0,
            )
        except FetchError as e:
            storage.finish_fetch(log_id, "error", error_message=str(e))
            summary["error"] += 1
            log.warning("ERR   %-40s %s", source.id, e)
        except Exception as e:  # noqa: BLE001 — orchestrator must not crash mid-run
            storage.finish_fetch(log_id, "error", error_message=f"{type(e).__name__}: {e}")
            summary["error"] += 1
            log.warning("ERR   %-40s %s: %s", source.id, type(e).__name__, e)

    return summary


def _fetch_and_store(storage: Storage, source: Source) -> tuple[int, int]:
    items_seen = 0
    items_new = 0
    for item in _fetch_with_fallback(source):
        items_seen += 1
        if storage.insert_item(item):
            items_new += 1
    return items_seen, items_new


def _fetch_with_fallback(source: Source) -> Iterator[Item]:
    """Try primary, fall through fallbacks until one yields items.

    Note: per SCOPE.md the fetcher should fail loud, not silently retry.
    But fallbacks ARE explicit alternates the source author declared
    (e.g. RSS primary + scrape fallback when RSS goes 404), so cycling
    through them is intentional, not retry-with-backoff scaffolding.
    """
    channels = [source.primary, *source.fallbacks]
    last_error: Exception | None = None
    for ch in channels:
        fetcher = _fetcher_for_kind(ch.kind)
        if fetcher is None:
            continue
        try:
            yielded_any = False
            for item in fetcher(source, ch):
                yielded_any = True
                yield item
            if yielded_any:
                return
        except FetchError as e:
            last_error = e
            continue
    if last_error:
        raise last_error


def _fetcher_for_kind(kind: str):
    if kind in {"rss", "rss_partial"}:
        return fetch_rss
    if kind in {"scrape", "blog"}:
        return fetch_scrape
    return None


def _print_plan(sources: list[Source]) -> None:
    by_kind: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for s in sources:
        by_kind[s.primary.kind] = by_kind.get(s.primary.kind, 0) + 1
        status = "supported" if s.is_supported else f"hitl ({s.hitl_reason})"
        by_status[status] = by_status.get(status, 0) + 1
    print("\n=== plan ===")
    print(f"total sources: {len(sources)}")
    print("\nby primary kind:")
    for k, c in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  {k:30s} {c}")
    print("\nby status:")
    for k, c in sorted(by_status.items(), key=lambda x: -x[1]):
        print(f"  {k:40s} {c}")


def _print_summary(summary: dict[str, int], storage: Storage) -> None:
    print("\n=== run summary ===")
    print(f"  ok:        {summary['ok']}")
    print(f"  error:     {summary['error']}")
    print(f"  hitl:      {summary['hitl']}")
    print(f"  items new: {summary['items_new']}")
    print(f"  items dup: {summary['items_dup']}")
    print(f"\n=== storage ===")
    for k, v in storage.stats().items():
        print(f"  {k:15s} {v}")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="collect", description="Wide scan over sources.yaml.")
    p.add_argument("--sources", type=Path, default=DEFAULT_SOURCES_PATH)
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--source", type=str, help="Run only the source with this id")
    p.add_argument("--limit-sources", type=int, help="Run only the first N sources")
    p.add_argument("--dry-run", action="store_true", help="Show plan without fetching")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
