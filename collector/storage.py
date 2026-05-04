"""SQLite storage for collected items, fetch logs, and HITL queue.

Schema is intentionally minimal for Task #3. Synthesizer (Task #4) will
ALTER TABLE to add columns for embedding, extracted_facts, briefing_snippet.
Don't pre-build columns for tasks that haven't started yet.

Per SCOPE.md §8, storage is content-addressed (URL hash + content hash),
no full-text storage (waste + copyright risk). Excerpt cap: 500 chars.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

EXCERPT_CHAR_CAP = 500

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
    raw_size_bytes  INTEGER
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
    error_message   TEXT
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
"""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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
                        excerpt, published_at, fetched_at, pillar_tags, raw_size_bytes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    ) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE fetch_log
                   SET finished_at = ?, status = ?, items_seen = ?, items_new = ?, error_message = ?
                 WHERE id = ?
                """,
                (_utc_now(), status, items_seen, items_new, error_message, log_id),
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

    def stats(self) -> dict[str, int]:
        with self._conn() as conn:
            return {
                "items_total": conn.execute("SELECT COUNT(*) FROM items").fetchone()[0],
                "fetch_runs": conn.execute("SELECT COUNT(*) FROM fetch_log").fetchone()[0],
                "hitl_pending": conn.execute("SELECT COUNT(*) FROM hitl_queue").fetchone()[0],
            }
