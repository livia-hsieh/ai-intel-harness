"""Haiku triage runner.

Loads un-triaged items from DB, asks Haiku per-item "which Pillars + signal
density?", writes decisions back. The system prompt (~3KB) is cached per run
so per-item cost stays at the Haiku 4.5 cache-read tier.

Decisions live on `items` table directly (triage_pillars / triage_signal /
triage_reason / triage_at / triage_model) — see collector/storage.py
MIGRATIONS list. Per-item rather than separate table because each item gets
exactly one current decision; re-triage just overwrites.

Per SCOPE.md §10 the eval signal is "post-filter retention" — i.e. of the items
Haiku passed (signal ≥ 0.6), how many ended up in the published digest. That
ratio is the meta-loop trigger for prompt revision; the data lives in
items.triage_signal joined against the engagement log.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass

from collector.config import Source, load_sources
from collector.storage import Storage
from synthesizer.client import MODEL_TRIAGE, Client, NoAPIKeyError
from synthesizer.prompts import TRIAGE_SYSTEM, triage_user_message

log = logging.getLogger("triage")


@dataclass
class TriageDecision:
    pillars: list[int]
    signal: float
    reason: str


def run_triage(
    storage: Storage,
    sources_by_id: dict[str, Source],
    *,
    client: Client,
    limit: int | None = None,
) -> dict[str, int]:
    """Triage all un-triaged items (or first `limit`).

    Returns a summary dict — counts of decisions by signal bucket + total cents.
    """
    summary = {
        "items_seen": 0,
        "decided": 0,
        "errors": 0,
        "high_signal": 0,   # ≥ 0.6
        "watch": 0,          # 0.3..0.6
        "skip": 0,           # < 0.3
        "total_cents": 0.0,
    }

    items = storage.list_untriaged_items(limit=limit)
    log.info("triage queue: %d items", len(items))
    if not items:
        return summary

    for item in items:
        summary["items_seen"] += 1
        source = sources_by_id.get(item["source_id"])
        if source is None:
            log.warning("item %d has unknown source_id %r — skipping", item["id"], item["source_id"])
            continue

        try:
            user_msg = triage_user_message(
                source_name=source.name,
                source_type=source.type,
                source_pillars=source.pillar_tags,
                title=item.get("title"),
                excerpt=item.get("excerpt"),
                published_at=item.get("published_at"),
                url=item["url"],
            )
            result = client.call(
                model=MODEL_TRIAGE,
                system=TRIAGE_SYSTEM,
                messages=[{"role": "user", "content": user_msg}],
                max_tokens=200,
                purpose=f"triage:item:{item['id']}",
            )
            summary["total_cents"] += result.cents
            decision = _parse_decision(result.text)

            if not client.dry_run:
                storage.record_triage(
                    item["id"],
                    pillars=decision.pillars,
                    signal=decision.signal,
                    reason=decision.reason,
                    model=MODEL_TRIAGE,
                )

            summary["decided"] += 1
            bucket = "high_signal" if decision.signal >= 0.6 else "watch" if decision.signal >= 0.3 else "skip"
            summary[bucket] += 1
            log.info(
                "  id=%-5d signal=%.2f pillars=%s — %s",
                item["id"], decision.signal, decision.pillars, decision.reason[:60],
            )
        except NoAPIKeyError:
            raise
        except Exception as e:  # noqa: BLE001
            summary["errors"] += 1
            log.warning("  id=%-5d ERR %s: %s", item["id"], type(e).__name__, e)

    return summary


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_decision(text: str) -> TriageDecision:
    """Tolerant JSON extraction — Haiku occasionally wraps in code fence."""
    if not text or text.startswith("[dry-run"):
        return TriageDecision(pillars=[], signal=0.0, reason="dry-run placeholder")
    match = _JSON_OBJECT_RE.search(text)
    if not match:
        raise ValueError(f"no JSON object found in model output: {text[:200]!r}")
    obj = json.loads(match.group(0))
    pillars_raw = obj.get("pillars") or []
    pillars = [int(p) for p in pillars_raw if isinstance(p, (int, float))]
    signal = float(obj.get("signal", 0.0))
    signal = max(0.0, min(1.0, signal))
    reason = str(obj.get("reason", ""))[:500]
    return TriageDecision(pillars=pillars, signal=signal, reason=reason)


def load_sources_indexed(yaml_path) -> dict[str, Source]:
    return {s.id: s for s in load_sources(yaml_path)}
