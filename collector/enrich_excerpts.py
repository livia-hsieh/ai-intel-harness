"""One-shot back-fill: items with NULL excerpt → fetch article body, update row.

Why this exists separate from collector/run.py:
- collector.run.main() inserts NEW items (URL hash dedup blocks updates).
- This script targets EXISTING items where excerpt is NULL — caused by
  pre-extract.py-era scrape that only grabbed `<a>` tag text, not article body.
- Idempotent: re-running on items that now have excerpts is a no-op.

After running, items where extraction succeeded have:
- excerpt populated
- content_hash recomputed (since hash is over normalized excerpt)
- scaffolding_note cleared if it was 'excerpt_extraction_failed'
- triage state RESET (triage_at = NULL etc) so next `triage` run re-evaluates
  with the new excerpt — this is the whole point.

Items where extraction still fails keep their NULL excerpt + get
scaffolding_note='excerpt_extraction_failed' (or its existing value retained).
Their triage state is NOT reset — no point re-triaging without new info.

Usage:
    enrich-excerpts                         # back-fill all NULL-excerpt items
    enrich-excerpts --limit 10              # smoke test
    enrich-excerpts --dry-run               # show what would be touched
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

from urllib.parse import urlparse

from collector.extract import fetch_excerpt
from collector.fetchers.scrape import _looks_like_nav_link
from collector.storage import Storage, content_hash

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "data" / "dedup.sqlite"

log = logging.getLogger("enrich")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    storage = Storage(args.db)
    raw_targets = _list_null_excerpt_items(storage, limit=args.limit)
    # Skip items that look like nav links / fragment URLs — fetching them
    # returns the listing page's body, which is wrong, not "no excerpt".
    targets = [t for t in raw_targets if not _is_nav_link(t)]
    skipped_nav = len(raw_targets) - len(targets)
    log.info(
        "targets: %d items with NULL excerpt (%d nav-link items skipped)",
        len(targets), skipped_nav,
    )

    if args.dry_run:
        for t in targets[:20]:
            print(f"  id={t['id']:<4} {t['source_id']:<30} {(t['title'] or '')[:60]}")
        if len(targets) > 20:
            print(f"  ... and {len(targets) - 20} more")
        return 0

    summary = {"attempted": 0, "extracted": 0, "still_failed": 0, "triage_reset": 0}
    t0 = time.time()
    for i, target in enumerate(targets, start=1):
        summary["attempted"] += 1
        url = target["url"]
        excerpt = fetch_excerpt(url)
        if excerpt:
            summary["extracted"] += 1
            had_triage = target["triage_at"] is not None
            _update_excerpt(storage, target["id"], excerpt, reset_triage=had_triage)
            if had_triage:
                summary["triage_reset"] += 1
            log.info("OK    id=%-4d %-30s %s", target["id"], target["source_id"], (target["title"] or "")[:50])
        else:
            summary["still_failed"] += 1
            _mark_extraction_failed(storage, target["id"])
            log.info("FAIL  id=%-4d %-30s %s", target["id"], target["source_id"], (target["title"] or "")[:50])
        if i % 25 == 0:
            elapsed = time.time() - t0
            log.info("  progress: %d/%d (%.1fs)", i, len(targets), elapsed)

    print()
    print("=== enrich summary ===")
    print(f"  attempted:           {summary['attempted']}")
    print(f"  excerpts extracted:  {summary['extracted']}")
    print(f"  still failed:        {summary['still_failed']}")
    print(f"  triage state reset:  {summary['triage_reset']}")
    print(f"  elapsed:             {time.time() - t0:.1f}s")
    return 0


def _is_nav_link(target: dict) -> bool:
    """Title looks like nav OR URL has a hash fragment / lacks a real path."""
    if _looks_like_nav_link(target["title"] or ""):
        return True
    parsed = urlparse(target["url"] or "")
    if parsed.fragment:  # href="#main-content" → wrong target
        return True
    if not parsed.path or parsed.path == "/":
        return True
    return False


def _list_null_excerpt_items(storage: Storage, limit: int | None = None) -> list[dict]:
    """All items where excerpt is NULL (or empty)."""
    sql = """
        SELECT id, source_id, url, title, triage_at
          FROM items
         WHERE (excerpt IS NULL OR excerpt = '')
         ORDER BY id ASC
    """
    if limit:
        sql += f" LIMIT {int(limit)}"
    with storage._conn() as conn:
        cols = ("id", "source_id", "url", "title", "triage_at")
        return [dict(zip(cols, row)) for row in conn.execute(sql)]


def _update_excerpt(storage: Storage, item_id: int, excerpt: str, *, reset_triage: bool) -> None:
    new_hash = content_hash(excerpt)
    with storage._conn() as conn:
        if reset_triage:
            conn.execute(
                """
                UPDATE items
                   SET excerpt = ?, content_hash = ?, scaffolding_note = NULL,
                       triage_at = NULL, triage_pillars = NULL,
                       triage_signal = NULL, triage_reason = NULL,
                       triage_model = NULL
                 WHERE id = ?
                """,
                (excerpt, new_hash, item_id),
            )
        else:
            conn.execute(
                """
                UPDATE items
                   SET excerpt = ?, content_hash = ?, scaffolding_note = NULL
                 WHERE id = ?
                """,
                (excerpt, new_hash, item_id),
            )


def _mark_extraction_failed(storage: Storage, item_id: int) -> None:
    with storage._conn() as conn:
        conn.execute(
            """
            UPDATE items
               SET scaffolding_note = COALESCE(scaffolding_note, 'excerpt_extraction_failed')
             WHERE id = ?
            """,
            (item_id,),
        )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="enrich-excerpts", description="Back-fill missing excerpts.")
    p.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    p.add_argument("--limit", type=int, help="Process at most this many items")
    p.add_argument("--dry-run", action="store_true", help="List targets without fetching")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
