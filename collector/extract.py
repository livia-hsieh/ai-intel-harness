"""Article body extraction.

The single responsibility: given an article URL, fetch the page and return the
first ~500 chars of the article's main body text. Used by:
- collector.fetchers.scrape — when scraping a list page, enrich each item
- collector.fetchers.rss     — when an RSS entry has no summary
- collector.enrich_excerpts  — one-shot back-fill for items already in DB

Why a separate module: keeping the extraction logic in one place means we
have one extractor to test, tune, and (eventually) replace if trafilatura
gets superseded by something better. The fetchers just call `fetch_excerpt(url)`
and don't care how it gets the text.

Trafilatura is the de-facto Python content-extraction library — it handles
~90% of news/blog HTML structures (article, main, schema.org metadata) with
a single call. For the remaining 10% that's hostile (paywalls, JS-rendered,
aggressive bot detection), we fail-soft: return None and let callers decide
whether to record a `scaffolding_note='excerpt_extraction_failed'`.

Performance: each call is one HTTP request (~0.3–1.5s typical). We call this
once per article on first sight; results are stored in items.excerpt and
never re-fetched (URL hash dedup).
"""

from __future__ import annotations

import logging

import requests
import trafilatura

USER_AGENT = "ai-intel-harness/0.3 (+https://github.com/livia-hsieh/ai-intel-harness)"
REQUEST_TIMEOUT_SEC = 15
EXCERPT_TARGET_CHARS = 500

log = logging.getLogger("extract")


def fetch_excerpt(url: str) -> str | None:
    """Fetch the article at `url` and return its main body, capped at EXCERPT_TARGET_CHARS.

    Returns None on any failure (network, parse, no body found). Callers that
    want to record provenance should check for None and set
    scaffolding_note='excerpt_extraction_failed' on the item.
    """
    if not url:
        return None
    try:
        resp = requests.get(
            url,
            timeout=REQUEST_TIMEOUT_SEC,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )
    except requests.RequestException as e:
        log.debug("excerpt fetch failed for %s: %s", url, e)
        return None

    if resp.status_code != 200:
        log.debug("excerpt fetch %s for %s", resp.status_code, url)
        return None

    body = trafilatura.extract(
        resp.text,
        url=url,
        include_comments=False,
        include_tables=False,
        favor_precision=True,
        no_fallback=False,
    )
    if not body:
        return None
    body = " ".join(body.split())  # collapse whitespace for hash stability
    if len(body) <= EXCERPT_TARGET_CHARS:
        return body
    return body[:EXCERPT_TARGET_CHARS].rsplit(" ", 1)[0] + "…"
