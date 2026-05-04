"""Scrape fetcher with RSS auto-discovery first.

Strategy (cheapest → most expensive):
1. Try RSS auto-discovery on the page (most modern blogs expose <link rel="alternate">).
   If a feed URL is found, hand off to fetch_rss.
2. Try /feed, /rss, /atom.xml, /index.xml conventions.
3. Otherwise: scrape the page for article links — generic article-list extraction.
   This is best-effort; if it produces nothing useful, the source is flagged
   for HITL ('scrape_no_articles_found') so a human can either provide an
   RSS URL, write a per-source extractor, or accept the source is dead.

Harness principle: don't write per-source XPath selectors in v1. The first
~5 sources where the generic extractor fails will tell us whether to:
(a) build a smarter generic extractor (probably trafilatura),
(b) write per-source adapters for the few high-value ones, or
(c) downgrade those sources.
That decision needs data, not guesses.
"""

from __future__ import annotations

from collections.abc import Iterator
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from collector.config import Channel, Source
from collector.fetchers.rss import USER_AGENT, FetchError, fetch_rss
from collector.storage import Item

REQUEST_TIMEOUT_SEC = 15
COMMON_FEED_PATHS = ("/feed", "/feed/", "/rss", "/rss.xml", "/atom.xml", "/index.xml")


def fetch_scrape(
    source: Source,
    channel: Channel,
    scaffolding_note: str | None = None,
) -> Iterator[Item]:
    """Scrape a page for article links.

    `scaffolding_note`: when set, every yielded Item carries this tag so the
    meta-loop knows the item came in via a removable fallback path (e.g.
    "rss_unrecovered_anthropic.com" — drop the scrape adapter when Anthropic's
    RSS comes back online).
    """
    if not channel.url:
        return

    discovered_feed = _discover_feed(channel.url)
    if discovered_feed:
        for item in fetch_rss(source, Channel(kind="rss", url=discovered_feed)):
            item.scaffolding_note = scaffolding_note
            yield item
        return

    for item in _scrape_article_list(source, channel.url):
        item.scaffolding_note = scaffolding_note
        yield item


def _discover_feed(page_url: str) -> str | None:
    """RSS auto-discovery via <link rel='alternate'> + common feed paths."""
    try:
        resp = requests.get(
            page_url,
            timeout=REQUEST_TIMEOUT_SEC,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )
        if resp.status_code != 200:
            return _try_common_feed_paths(page_url)
    except requests.RequestException:
        return _try_common_feed_paths(page_url)

    soup = BeautifulSoup(resp.text, "lxml")
    for link in soup.find_all("link", rel="alternate"):
        link_type = (link.get("type") or "").lower()
        if "rss" in link_type or "atom" in link_type or "xml" in link_type:
            href = link.get("href")
            if href:
                return urljoin(page_url, href)

    return _try_common_feed_paths(page_url)


def _try_common_feed_paths(page_url: str) -> str | None:
    parsed = urlparse(page_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    for path in COMMON_FEED_PATHS:
        candidate = urljoin(base, path)
        try:
            head = requests.head(
                candidate,
                timeout=REQUEST_TIMEOUT_SEC,
                headers={"User-Agent": USER_AGENT},
                allow_redirects=True,
            )
        except requests.RequestException:
            continue
        ctype = head.headers.get("Content-Type", "").lower()
        if head.status_code == 200 and ("xml" in ctype or "rss" in ctype or "atom" in ctype):
            return candidate
    return None


def _scrape_article_list(source: Source, page_url: str) -> Iterator[Item]:
    try:
        resp = requests.get(
            page_url,
            timeout=REQUEST_TIMEOUT_SEC,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )
    except requests.RequestException as e:
        raise FetchError(f"scrape request failed for {page_url}: {e}") from e

    if resp.status_code != 200:
        raise FetchError(f"scrape got HTTP {resp.status_code} for {page_url}")

    soup = BeautifulSoup(resp.text, "lxml")
    page_host = urlparse(page_url).netloc

    seen_urls: set[str] = set()
    yielded = 0
    for a in soup.find_all("a", href=True):
        link = urljoin(page_url, a["href"])
        if not _looks_like_article(link, page_host):
            continue
        if link in seen_urls:
            continue
        seen_urls.add(link)

        title = a.get_text(strip=True) or None
        if not title or len(title) < 10:
            continue

        yield Item(
            source_id=source.id,
            url=link,
            title=title,
            excerpt=None,
            published_at=None,
            pillar_tags=source.pillar_tags,
            raw_size_bytes=len(str(a)),
        )
        yielded += 1

    if yielded == 0:
        raise FetchError(f"scrape found no article links at {page_url}")


def _looks_like_article(url: str, page_host: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.netloc and parsed.netloc != page_host:
        return False
    path = parsed.path.lower()
    if not path or path == "/":
        return False
    skip_prefixes = ("/tag/", "/category/", "/author/", "/page/", "/feed", "/rss", "/about", "/contact", "/privacy", "/terms")
    if any(path.startswith(p) for p in skip_prefixes):
        return False
    skip_exts = (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".css", ".js", ".xml")
    if any(path.endswith(e) for e in skip_exts):
        return False
    return True
