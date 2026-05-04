"""Source registry loader.

Reads sources.yaml and normalizes each entry into a Source dataclass. The
yaml schema is intentionally loose (humans edit it). Normalization handles
the missing-fields case so fetchers don't have to.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# Fetcher kinds the v1 collector can handle natively.
# Everything else gets routed to HITL queue with reason='unsupported_kind'.
SUPPORTED_KINDS: frozenset[str] = frozenset({"rss", "scrape", "blog", "rss_partial"})


@dataclass
class Channel:
    kind: str
    url: str | None = None
    handle: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Channel:
        kind = raw.get("kind", "unknown")
        url = raw.get("url")
        handle = raw.get("handle")
        extra = {k: v for k, v in raw.items() if k not in {"kind", "url", "handle"}}
        return cls(kind=kind, url=url, handle=handle, extra=extra)


# MVP modes per SCOPE.md §14 (v0.3.1).
# - full        : fetch as normal
# - echo_only   : do not direct-fetch; rely on Mechanism A3 to surface via echo channel
# - hitl_adhoc  : paywall / restricted; queue for human input but no weekly notification
MVP_MODES: frozenset[str] = frozenset({"full", "echo_only", "hitl_adhoc"})


@dataclass
class Source:
    id: str
    name: str
    type: str
    pillar_tags: list[int]
    primary: Channel
    fallbacks: list[Channel]
    geo: str | None
    signal_density: str | None
    human_required: bool
    notes: str | None
    mvp_active: bool = True
    mvp_mode: str = "full"

    @property
    def is_supported(self) -> bool:
        if not self.mvp_active or self.mvp_mode != "full":
            return False
        if self.human_required:
            return False
        return self.primary.kind in SUPPORTED_KINDS

    @property
    def hitl_reason(self) -> str | None:
        if not self.mvp_active:
            return "mvp_deferred"
        if self.mvp_mode == "echo_only":
            return "mvp_echo_only"
        if self.mvp_mode == "hitl_adhoc":
            return "mvp_hitl_adhoc"
        if self.human_required:
            return "paywall_or_human_required"
        if self.primary.kind not in SUPPORTED_KINDS:
            return f"unsupported_kind:{self.primary.kind}"
        return None


def load_sources(yaml_path: Path) -> list[Source]:
    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    raw_sources = data.get("sources") or []
    out: list[Source] = []
    for raw in raw_sources:
        if not isinstance(raw, dict) or "id" not in raw:
            continue

        # primary may be a single channel dict OR a list of channels (multi-platform).
        # When a list, the first SUPPORTED channel becomes primary; the rest fall in line.
        primary_channels = _normalize_channels(raw.get("primary"))
        explicit_fallbacks = _normalize_channels(raw.get("fallback"))
        all_channels = primary_channels + explicit_fallbacks
        if not all_channels:
            continue

        primary, fallbacks = _split_primary_and_fallbacks(all_channels)

        mvp_mode = raw.get("mvp_mode", "full")
        if mvp_mode not in MVP_MODES:
            mvp_mode = "full"

        out.append(
            Source(
                id=raw["id"],
                name=raw.get("name", raw["id"]),
                type=raw.get("type", "unknown"),
                pillar_tags=list(raw.get("pillar_tags") or []),
                primary=primary,
                fallbacks=fallbacks,
                geo=raw.get("geo"),
                signal_density=raw.get("signal_density"),
                human_required=bool(raw.get("human_required", False)),
                notes=raw.get("notes"),
                mvp_active=bool(raw.get("mvp_active", True)),
                mvp_mode=mvp_mode,
            )
        )
    return out


def _normalize_channels(raw: Any) -> list[Channel]:
    if isinstance(raw, dict):
        return [Channel.from_dict(raw)]
    if isinstance(raw, list):
        return [Channel.from_dict(c) for c in raw if isinstance(c, dict)]
    return []


def _split_primary_and_fallbacks(channels: list[Channel]) -> tuple[Channel, list[Channel]]:
    """Promote the first SUPPORTED channel to primary; remaining stay as fallbacks.

    If none are supported, the literal first channel is primary and the source
    will route to HITL via Source.hitl_reason. This preserves the author's
    declared ordering while preferring fetchable channels when present.
    """
    for i, ch in enumerate(channels):
        if ch.kind in SUPPORTED_KINDS:
            return ch, [c for j, c in enumerate(channels) if j != i]
    return channels[0], channels[1:]
