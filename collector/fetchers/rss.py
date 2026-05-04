"""RSS / Atom fetcher.

Uses feedparser, which is the de facto Python RSS library and handles the
zoo of feed formats (RSS 2.0, Atom, RSS 1.0, malformed XML) without
per-source parsing rules. This is the right kind of scaffolding to keep:
the "model can't do this" is "parse 20 different feed dialects reliably"
and feedparser already encodes that knowledge.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import feedparser

from collector.config import Channel, Source
from collector.storage import Item

USER_AGENT = "ai-intel-harness/0.1 (+https://github.com/livia-hsieh/ai-intel-harness)"


def fetch_rss(source: Source, channel: Channel) -> Iterator[Item]:
    if not channel.url:
        return
    parsed = feedparser.parse(channel.url, agent=USER_AGENT)
    if parsed.bozo and not parsed.entries:
        # Truly broken — let orchestrator log + move on.
        raise FetchError(f"RSS parse failed for {channel.url}: {parsed.bozo_exception}")

    for entry in parsed.entries:
        url = _entry_url(entry)
        if not url:
            continue
        yield Item(
            source_id=source.id,
            url=url,
            title=entry.get("title"),
            excerpt=_entry_excerpt(entry),
            published_at=_entry_published(entry),
            pillar_tags=source.pillar_tags,
            raw_size_bytes=len(str(entry)),
        )


def _entry_url(entry: Any) -> str | None:
    return entry.get("link") or entry.get("id")


def _entry_excerpt(entry: Any) -> str | None:
    # feedparser normalizes content/summary into these fields.
    if entry.get("summary"):
        return _strip_html(entry["summary"])
    content_list = entry.get("content")
    if isinstance(content_list, list) and content_list:
        return _strip_html(content_list[0].get("value", ""))
    return None


def _entry_published(entry: Any) -> str | None:
    # feedparser already parses to time.struct_time; convert to ISO.
    parsed_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed_time:
        return entry.get("published") or entry.get("updated")
    from datetime import datetime, timezone

    dt = datetime(*parsed_time[:6], tzinfo=timezone.utc)
    return dt.isoformat(timespec="seconds")


def _strip_html(html: str) -> str:
    from bs4 import BeautifulSoup

    return BeautifulSoup(html, "lxml").get_text(separator=" ", strip=True)


class FetchError(RuntimeError):
    """Raised when a fetcher cannot produce items. Orchestrator logs + skips."""
