"""RSS / Atom fetcher.

Uses feedparser, which handles the zoo of feed formats (RSS 2.0, Atom, RSS 1.0,
malformed XML) without per-source parsing rules. The "model can't do this" is
parse 20 different feed dialects reliably — feedparser already encodes that
knowledge.

When the declared RSS URL returns invalid XML, try alternative endpoints on
the same host before giving up (per Cowork resolution 2026-05-04: don't demote
backbone sources because of transport problems). Each attempted endpoint is
returned via FetchAttempt so the orchestrator can log them for the meta-loop
to re-probe later.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin, urlparse

import feedparser

from collector.config import Channel, Source
from collector.storage import Item

USER_AGENT = "ai-intel-harness/0.2 (+https://github.com/livia-hsieh/ai-intel-harness)"

# Tried in order when the declared RSS URL is dead. Same-host only.
ALT_RSS_PATHS = (
    "/rss",
    "/rss.xml",
    "/feed",
    "/feed/",
    "/feed.xml",
    "/atom.xml",
    "/index.xml",
    "/news/rss.xml",
    "/blog/rss.xml",
)


@dataclass
class FetchAttempt:
    """Metadata for one RSS fetch attempt — what we tried and what worked."""
    items: list[Item]
    used_endpoint: str | None
    tried_endpoints: list[str] = field(default_factory=list)


def fetch_rss(source: Source, channel: Channel) -> Iterator[Item]:
    """Iterator API: yields items from whichever endpoint works first."""
    attempt = fetch_rss_with_metadata(source, channel)
    yield from attempt.items


def fetch_rss_with_metadata(source: Source, channel: Channel) -> FetchAttempt:
    """Try declared URL first, then alternative endpoints on the same host.

    Returns an empty items list with tried_endpoints populated if all fail —
    the orchestrator decides whether to fall through to scrape (and tag
    `scaffolding_note`) or just record the failure.
    """
    if not channel.url:
        return FetchAttempt(items=[], used_endpoint=None)

    tried: list[str] = []
    for url in _candidate_urls(channel.url):
        tried.append(url)
        items = _try_one(source, url)
        if items is not None:
            return FetchAttempt(items=items, used_endpoint=url, tried_endpoints=tried)
    return FetchAttempt(items=[], used_endpoint=None, tried_endpoints=tried)


def _candidate_urls(declared_url: str) -> list[str]:
    parsed = urlparse(declared_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    seen = {declared_url}
    out = [declared_url]
    for path in ALT_RSS_PATHS:
        cand = urljoin(base, path)
        if cand not in seen:
            seen.add(cand)
            out.append(cand)
    return out


def _try_one(source: Source, url: str) -> list[Item] | None:
    parsed = feedparser.parse(url, agent=USER_AGENT)
    if parsed.bozo and not parsed.entries:
        return None
    items = []
    for entry in parsed.entries:
        eurl = _entry_url(entry)
        if not eurl:
            continue
        items.append(
            Item(
                source_id=source.id,
                url=eurl,
                title=entry.get("title"),
                excerpt=_entry_excerpt(entry),
                published_at=_entry_published(entry),
                pillar_tags=source.pillar_tags,
                raw_size_bytes=len(str(entry)),
            )
        )
    return items if items else None


def _entry_url(entry: Any) -> str | None:
    return entry.get("link") or entry.get("id")


def _entry_excerpt(entry: Any) -> str | None:
    if entry.get("summary"):
        return _strip_html(entry["summary"])
    content_list = entry.get("content")
    if isinstance(content_list, list) and content_list:
        return _strip_html(content_list[0].get("value", ""))
    return None


def _entry_published(entry: Any) -> str | None:
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
