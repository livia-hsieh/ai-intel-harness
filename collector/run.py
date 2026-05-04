"""Orchestrator — wide scan over all sources defined in sources.yaml.

Run modes:
    collect                    # all sources
    collect --source <id>      # one source (debug)
    collect --limit-sources N  # first N sources (smoke test)
    collect --dry-run          # show plan, don't fetch
    collect --force            # ignore cursor; fetch everything (cold-start equivalent)

Per SCOPE.md §14 (v0.3.1):
- Per-source incremental cursor: cold start = last 30 days, steady state = items
  newer than `last_successful_pub_date`. "Wide scan" is source breadth, not
  temporal breadth.
- RSS fallback chain: declared URL → alt endpoints on same host → scrape with
  `scaffolding_note: rss_unrecovered_<host>`. Items via fallback are tagged so
  the meta-loop can re-probe upstream RSS quarterly and remove the scaffolding
  when it recovers.
- MVP routing: sources tagged `mvp_active: false` or `mvp_mode != full` skip
  the fetch path and route to HITL queue with mode-specific reason.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import urlparse

from collector.config import Channel, Source, load_sources
from collector.fetchers.rss import FetchError, fetch_rss_with_metadata
from collector.fetchers.scrape import fetch_scrape
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
    summary = _run(storage, sources, force=args.force)
    _print_summary(summary, storage)
    return 0


def _run(storage: Storage, sources: list[Source], force: bool) -> dict[str, int]:
    summary = {"ok": 0, "error": 0, "hitl": 0, "items_new": 0, "items_dup": 0, "items_filtered_by_cursor": 0}

    for source in sources:
        if not source.is_supported:
            storage.queue_hitl(source.id, source.hitl_reason or "unknown")
            log.info("HITL  %-40s reason=%s", source.id, source.hitl_reason)
            summary["hitl"] += 1
            continue

        log_id = storage.start_fetch(source.id)
        t0 = time.time()
        cursor = None if force else storage.get_cursor(source.id)
        try:
            outcome = _fetch_and_store(storage, source, cursor)
            storage.finish_fetch(
                log_id,
                "ok",
                items_seen=outcome.items_seen,
                items_new=outcome.items_new,
                used_channel=outcome.used_channel,
                tried_endpoints=outcome.tried_endpoints or None,
            )
            if outcome.max_pub_date:
                storage.update_cursor(source.id, outcome.max_pub_date)
            else:
                storage.update_cursor(source.id, None)
            summary["ok"] += 1
            summary["items_new"] += outcome.items_new
            summary["items_dup"] += outcome.items_seen - outcome.items_new
            summary["items_filtered_by_cursor"] += outcome.items_filtered_by_cursor
            log.info(
                "OK    %-40s seen=%-3d new=%-3d filtered=%-3d via=%-20s %.1fs",
                source.id,
                outcome.items_seen,
                outcome.items_new,
                outcome.items_filtered_by_cursor,
                outcome.used_channel or "?",
                time.time() - t0,
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


class _FetchOutcome:
    __slots__ = (
        "items_seen",
        "items_new",
        "items_filtered_by_cursor",
        "max_pub_date",
        "used_channel",
        "tried_endpoints",
    )

    def __init__(self) -> None:
        self.items_seen = 0
        self.items_new = 0
        self.items_filtered_by_cursor = 0
        self.max_pub_date: str | None = None
        self.used_channel: str | None = None
        self.tried_endpoints: list[str] = []


def _fetch_and_store(storage: Storage, source: Source, cursor: str | None) -> _FetchOutcome:
    outcome = _FetchOutcome()
    for item in _fetch_with_fallback(source, outcome):
        if cursor and item.published_at and item.published_at <= cursor:
            outcome.items_filtered_by_cursor += 1
            continue
        outcome.items_seen += 1
        if item.published_at and (not outcome.max_pub_date or item.published_at > outcome.max_pub_date):
            outcome.max_pub_date = item.published_at
        if storage.insert_item(item):
            outcome.items_new += 1
    return outcome


def _fetch_with_fallback(source: Source, outcome: _FetchOutcome) -> Iterator[Item]:
    """Cycle through declared channels.

    Within an RSS channel, also try alternative endpoints on the same host
    before declaring the channel dead. Last resort: if a kind=rss channel is
    fully dead, fall through to scrape on its host page with a scaffolding_note
    so the meta-loop can re-probe RSS later.
    """
    channels = [source.primary, *source.fallbacks]
    last_error: Exception | None = None

    for ch in channels:
        if ch.kind in {"rss", "rss_partial"}:
            attempt = fetch_rss_with_metadata(source, ch)
            outcome.tried_endpoints.extend(attempt.tried_endpoints)
            if attempt.items:
                outcome.used_channel = f"rss:{attempt.used_endpoint}"
                yield from attempt.items
                return
            # all RSS endpoints dead → try scrape on the host page as a tagged fallback
            host = urlparse(ch.url).netloc if ch.url else "unknown"
            note = f"rss_unrecovered_{host}"
            try:
                scraped = list(
                    fetch_scrape(source, Channel(kind="scrape", url=ch.url), scaffolding_note=note)
                )
                if scraped:
                    outcome.used_channel = f"scrape_fallback:{ch.url}"
                    outcome.tried_endpoints.append(f"scrape_fallback:{ch.url}")
                    yield from scraped
                    return
            except FetchError as e:
                last_error = e
            continue

        if ch.kind in {"scrape", "blog"}:
            try:
                scraped = list(fetch_scrape(source, ch))
                if scraped:
                    outcome.used_channel = f"scrape:{ch.url}"
                    yield from scraped
                    return
            except FetchError as e:
                last_error = e
            continue

    if last_error:
        raise last_error


def _print_plan(sources: list[Source]) -> None:
    by_kind: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_mvp_mode: dict[str, int] = {}
    for s in sources:
        by_kind[s.primary.kind] = by_kind.get(s.primary.kind, 0) + 1
        status = "supported" if s.is_supported else f"hitl ({s.hitl_reason})"
        by_status[status] = by_status.get(status, 0) + 1
        by_mvp_mode[s.mvp_mode if s.mvp_active else "deferred"] = (
            by_mvp_mode.get(s.mvp_mode if s.mvp_active else "deferred", 0) + 1
        )
    print("\n=== plan ===")
    print(f"total sources: {len(sources)}")
    print("\nby primary kind:")
    for k, c in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  {k:30s} {c}")
    print("\nby mvp mode:")
    for k, c in sorted(by_mvp_mode.items(), key=lambda x: -x[1]):
        print(f"  {k:30s} {c}")
    print("\nby status:")
    for k, c in sorted(by_status.items(), key=lambda x: -x[1]):
        print(f"  {k:45s} {c}")


def _print_summary(summary: dict[str, int], storage: Storage) -> None:
    print("\n=== run summary ===")
    print(f"  ok:                       {summary['ok']}")
    print(f"  error:                    {summary['error']}")
    print(f"  hitl:                     {summary['hitl']}")
    print(f"  items new:                {summary['items_new']}")
    print(f"  items dup:                {summary['items_dup']}")
    print(f"  items filtered by cursor: {summary['items_filtered_by_cursor']}")
    print(f"\n=== storage ===")
    for k, v in storage.stats().items():
        print(f"  {k:25s} {v}")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="collect", description="Wide scan over sources.yaml.")
    p.add_argument("--sources", type=Path, default=DEFAULT_SOURCES_PATH)
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--source", type=str, help="Run only the source with this id")
    p.add_argument("--limit-sources", type=int, help="Run only the first N sources")
    p.add_argument("--dry-run", action="store_true", help="Show plan without fetching")
    p.add_argument(
        "--force",
        action="store_true",
        help="Ignore source cursors; fetch as if cold-starting (still respects URL dedup).",
    )
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
