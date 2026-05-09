"""SQLite storage for collected items, fetch logs, HITL queue, and source cursors.

Schema is intentionally minimal. Synthesizer (Task #4) will ALTER TABLE to add
columns for embedding, extracted_facts, briefing_snippet — don't pre-build
columns for tasks that haven't started yet.

Per SCOPE.md §8, storage is content-addressed (URL hash + content hash),
no full-text storage (waste + copyright risk). Excerpt cap: 500 chars.

Per SCOPE.md §13/§14 (v0.3.1):
- `scaffolding_note` on items records when an item came in via a fallback
  path that should be removable later (e.g. RSS recovered → cut the scrape
  fallback). Tracked so meta-loop can re-probe original endpoints.
- `source_cursor` table tracks `last_successful_pub_date` per source so we
  fetch incrementally (cold start = last 30 days; steady state = items
  newer than cursor). "Wide scan" means source breadth, not temporal breadth.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

EXCERPT_CHAR_CAP = 500
COLD_START_LOOKBACK_DAYS = 30

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id              INTEGER PRIMARY KEY,
    source_id       TEXT NOT NULL,
    url             TEXT NOT NULL,
    url_hash        TEXT NOT NULL UNIQUE,
    content_hash    TEXT,
    title           TEXT,
    excerpt         TEXT,
    published_at    TEXT,
    fetched_at      TEXT NOT NULL,
    pillar_tags     TEXT,
    raw_size_bytes  INTEGER,
    scaffolding_note TEXT
);
CREATE INDEX IF NOT EXISTS idx_items_source     ON items(source_id);
CREATE INDEX IF NOT EXISTS idx_items_fetched    ON items(fetched_at);
CREATE INDEX IF NOT EXISTS idx_items_published  ON items(published_at);
CREATE INDEX IF NOT EXISTS idx_items_content    ON items(content_hash);

CREATE TABLE IF NOT EXISTS fetch_log (
    id              INTEGER PRIMARY KEY,
    source_id       TEXT NOT NULL,
    started_at      TEXT NOT NULL,
    finished_at     TEXT,
    status          TEXT NOT NULL,
    items_seen      INTEGER DEFAULT 0,
    items_new       INTEGER DEFAULT 0,
    error_message   TEXT,
    used_channel    TEXT,
    tried_endpoints TEXT
);
CREATE INDEX IF NOT EXISTS idx_log_source ON fetch_log(source_id);
CREATE INDEX IF NOT EXISTS idx_log_status ON fetch_log(status);

CREATE TABLE IF NOT EXISTS hitl_queue (
    id                  INTEGER PRIMARY KEY,
    source_id           TEXT NOT NULL,
    queued_at           TEXT NOT NULL,
    reason              TEXT NOT NULL,
    consecutive_skips   INTEGER DEFAULT 0,
    last_response       TEXT,
    last_response_at    TEXT,
    UNIQUE(source_id, reason)
);

CREATE TABLE IF NOT EXISTS source_cursor (
    source_id               TEXT PRIMARY KEY,
    last_successful_pub_date TEXT,
    last_run_at             TEXT,
    cold_started_at         TEXT
);
"""

# Columns added in later migrations. Each entry is (table, column, type).
# We check PRAGMA table_info() and ALTER TABLE only when missing.
MIGRATIONS = [
    ("items", "scaffolding_note", "TEXT"),
    ("fetch_log", "used_channel", "TEXT"),
    ("fetch_log", "tried_endpoints", "TEXT"),
    # v0.3 — triage (Task #4): Haiku decides per-item Pillar + signal density.
    # Null until triaged. signal score is 0..1; pillars is JSON array of ints
    # (an item can map to multiple Pillars, e.g. 1+2 = banking AI strategy).
    ("items", "triage_pillars", "TEXT"),
    ("items", "triage_signal", "REAL"),
    ("items", "triage_reason", "TEXT"),
    ("items", "triage_at", "TEXT"),
    ("items", "triage_model", "TEXT"),
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _utc_now_minus_days(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")


def url_hash(url: str) -> str:
    return hashlib.sha256(url.strip().encode("utf-8")).hexdigest()


def content_hash(text: str) -> str:
    normalized = " ".join(text.split()).lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


@dataclass
class Item:
    source_id: str
    url: str
    title: str | None
    excerpt: str | None
    published_at: str | None
    pillar_tags: list[int]
    raw_size_bytes: int
    scaffolding_note: str | None = None

    def truncated_excerpt(self) -> str | None:
        if self.excerpt is None:
            return None
        return self.excerpt[:EXCERPT_CHAR_CAP]


class Storage:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as conn:
            conn.executescript(SCHEMA)
            self._migrate(conn)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _migrate(self, conn: sqlite3.Connection) -> None:
        """Idempotent migrations for columns added after v0.1."""
        for table, column, coltype in MIGRATIONS:
            existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
            if column not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")

    def insert_item(self, item: Item) -> bool:
        """Insert if new (by url_hash). Returns True if inserted, False if dup."""
        excerpt = item.truncated_excerpt()
        c_hash = content_hash(excerpt) if excerpt else None
        with self._conn() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO items (
                        source_id, url, url_hash, content_hash, title,
                        excerpt, published_at, fetched_at, pillar_tags,
                        raw_size_bytes, scaffolding_note
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item.source_id,
                        item.url,
                        url_hash(item.url),
                        c_hash,
                        item.title,
                        excerpt,
                        item.published_at,
                        _utc_now(),
                        json.dumps(item.pillar_tags),
                        item.raw_size_bytes,
                        item.scaffolding_note,
                    ),
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def start_fetch(self, source_id: str) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO fetch_log (source_id, started_at, status) VALUES (?, ?, ?)",
                (source_id, _utc_now(), "running"),
            )
            return cur.lastrowid

    def finish_fetch(
        self,
        log_id: int,
        status: str,
        items_seen: int = 0,
        items_new: int = 0,
        error_message: str | None = None,
        used_channel: str | None = None,
        tried_endpoints: list[str] | None = None,
    ) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE fetch_log
                   SET finished_at = ?, status = ?, items_seen = ?, items_new = ?,
                       error_message = ?, used_channel = ?, tried_endpoints = ?
                 WHERE id = ?
                """,
                (
                    _utc_now(),
                    status,
                    items_seen,
                    items_new,
                    error_message,
                    used_channel,
                    json.dumps(tried_endpoints) if tried_endpoints else None,
                    log_id,
                ),
            )

    def queue_hitl(self, source_id: str, reason: str) -> None:
        """Idempotent — UNIQUE(source_id, reason) prevents duplicates."""
        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO hitl_queue (source_id, queued_at, reason, consecutive_skips)
                VALUES (?, ?, ?, 0)
                ON CONFLICT(source_id, reason) DO UPDATE SET
                    consecutive_skips = consecutive_skips + 1
                """,
                (source_id, _utc_now(), reason),
            )

    # --- source cursor (incremental fetch) ---

    def get_cursor(self, source_id: str) -> str:
        """Return the published_at floor for this source.

        Cold start (no row yet): now - 30 days.
        Steady state: last_successful_pub_date.
        Items without a published_at on the source side will pass through
        regardless — URL-hash dedup is the safety net for those.
        """
        with self._conn() as conn:
            row = conn.execute(
                "SELECT last_successful_pub_date FROM source_cursor WHERE source_id = ?",
                (source_id,),
            ).fetchone()
        if row and row[0]:
            return row[0]
        return _utc_now_minus_days(COLD_START_LOOKBACK_DAYS)

    def update_cursor(self, source_id: str, max_pub_date: str | None) -> None:
        """Record the latest published_at seen this run + bump last_run_at.

        If max_pub_date is None (no dated items this run), keep the existing
        cursor untouched but still update last_run_at.
        """
        with self._conn() as conn:
            existing = conn.execute(
                "SELECT last_successful_pub_date, cold_started_at FROM source_cursor WHERE source_id = ?",
                (source_id,),
            ).fetchone()
            cold_started_at = existing[1] if existing else _utc_now()
            new_pub = max_pub_date or (existing[0] if existing else None)
            conn.execute(
                """
                INSERT INTO source_cursor (source_id, last_successful_pub_date, last_run_at, cold_started_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    last_successful_pub_date = excluded.last_successful_pub_date,
                    last_run_at = excluded.last_run_at
                """,
                (source_id, new_pub, _utc_now(), cold_started_at),
            )

    # --- triage (Task #4: Haiku per-item decisions) ---

    def list_untriaged_items(
        self,
        limit: int | None = None,
        source_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Items the triage layer has not yet processed.

        Returned as plain dicts (not the Item dataclass) because the triage
        prompt only needs id/source_id/title/excerpt/published_at/pillar_tags.

        `source_id`: when set, restrict to items from that one source. Used by
        per-Pillar calibration runs (e.g. triage --source openai-blog --limit 30).
        """
        params: tuple = ()
        sql = """
            SELECT id, source_id, url, title, excerpt, published_at, pillar_tags
              FROM items
             WHERE triage_at IS NULL
        """
        if source_id:
            sql += " AND source_id = ?"
            params = (source_id,)
        # Newest items first: this week's actual news gets triaged before any
        # historical backlog. SQLite NULLS LAST = items with no published_at
        # (scrape items missing date) go to end so they don't block fresh items.
        sql += " ORDER BY published_at DESC NULLS LAST, id DESC"
        if limit:
            sql += f" LIMIT {int(limit)}"
        with self._conn() as conn:
            cols = ("id", "source_id", "url", "title", "excerpt", "published_at", "pillar_tags")
            return [dict(zip(cols, row)) for row in conn.execute(sql, params)]

    def record_triage(
        self,
        item_id: int,
        *,
        pillars: list[int],
        signal: float,
        reason: str,
        model: str,
    ) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE items
                   SET triage_pillars = ?, triage_signal = ?, triage_reason = ?,
                       triage_at = ?, triage_model = ?
                 WHERE id = ?
                """,
                (json.dumps(pillars), signal, reason, _utc_now(), model, item_id),
            )

    def list_high_signal_items_for_pillar(
        self,
        pillar_n: int,
        *,
        min_signal: float = 0.6,
        published_after: str | None = None,
    ) -> list[dict[str, Any]]:
        """Items where triage_signal ≥ min_signal AND triage_pillars contains pillar_n.

        Used by Pulse synthesis. `published_after` filters to a digest window
        (e.g. last 7 days for weekly run); when None returns all qualifying items
        in the DB (used for backlog smoke tests).

        Note: triage_pillars is stored as JSON array. We use SQLite's LIKE on the
        JSON text for the pillar membership check — fast and avoids a JSON1
        extension dependency. Pattern: '%[%, ]?<n>[, ]%]?' simplified to LIKE
        '%<n>%' with a string-anchor sanity check at read-time.
        """
        sql = """
            SELECT id, source_id, url, title, excerpt, published_at, pillar_tags,
                   triage_signal, triage_pillars, triage_reason
              FROM items
             WHERE triage_at IS NOT NULL
               AND triage_signal >= ?
               AND triage_pillars LIKE ?
        """
        params: list[Any] = [min_signal, f"%{pillar_n}%"]
        if published_after:
            sql += " AND (published_at >= ? OR published_at IS NULL)"
            params.append(published_after)
        sql += " ORDER BY triage_signal DESC, id ASC"
        cols = (
            "id", "source_id", "url", "title", "excerpt", "published_at",
            "pillar_tags", "signal", "pillars", "triage_reason",
        )
        with self._conn() as conn:
            rows = list(conn.execute(sql, params))
        out = []
        for row in rows:
            d = dict(zip(cols, row))
            # parse triage_pillars JSON, double-check pillar_n really is in there
            try:
                pillars = json.loads(d["pillars"]) if d["pillars"] else []
            except json.JSONDecodeError:
                pillars = []
            if pillar_n not in pillars:
                continue  # LIKE false-positive (e.g. pillar 5 matched within "[15]")
            d["pillars"] = pillars
            out.append(d)
        return out

    def stats(self) -> dict[str, int]:
        with self._conn() as conn:
            return {
                "items_total": conn.execute("SELECT COUNT(*) FROM items").fetchone()[0],
                "items_triaged": conn.execute(
                    "SELECT COUNT(*) FROM items WHERE triage_at IS NOT NULL"
                ).fetchone()[0],
                "fetch_runs": conn.execute("SELECT COUNT(*) FROM fetch_log").fetchone()[0],
                "hitl_pending": conn.execute("SELECT COUNT(*) FROM hitl_queue").fetchone()[0],
                "sources_with_cursor": conn.execute("SELECT COUNT(*) FROM source_cursor").fetchone()[0],
            }
