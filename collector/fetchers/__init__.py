"""Fetcher implementations.

Each fetcher takes a Source + Channel and returns an iterable of Items
(see collector.storage.Item). Fetchers are responsible for the wire protocol
only — dedup happens at the Storage layer, triage happens in Task #4.

Harness principle: fail loud, don't retry. If a feed is broken, the orchestrator
logs it and moves on. Silent retries hide source rot, which Mechanism A
(SCOPE.md §10) needs to surface.
"""

from collector.fetchers.rss import fetch_rss
from collector.fetchers.scrape import fetch_scrape

__all__ = ["fetch_rss", "fetch_scrape"]
