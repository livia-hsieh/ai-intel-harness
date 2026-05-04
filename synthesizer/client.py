"""Anthropic API client wrapper with prompt caching + cost accounting.

Centralises three concerns the rest of the synthesizer would otherwise duplicate:
1. Authentication — reads ANTHROPIC_API_KEY from env. Refuses to make calls
   with no key set; surfaces a clear error instead of failing inside the SDK.
2. Prompt caching — the system prompt and any large reference blocks are
   marked with `cache_control: ephemeral` so repeated calls within 5 min reuse
   the cached prefix. This drops Sonnet/Opus cost ~70% during a digest run.
3. Cost log — every call appends to `data/cost_log.jsonl` (model, input_tokens,
   cache_read_input_tokens, output_tokens, cents_estimate, purpose). Per
   SCOPE.md §9 the alarm is >$5/week — the log is what we'd query for that.

Models, per SCOPE.md §9:
- Haiku 4.5  → triage
- Sonnet 4.6 → Pulse synthesis
- Opus 4.6   → Foundation deep-read
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Per Anthropic API pricing (cents per 1M tokens). Update when pricing changes.
PRICING = {
    "claude-haiku-4-5":   {"input": 100,   "cache_read": 10,   "output": 500},
    "claude-sonnet-4-6":  {"input": 300,   "cache_read": 30,   "output": 1500},
    "claude-opus-4-6":    {"input": 1500,  "cache_read": 150,  "output": 7500},
}

# Aliases used internally so callers don't hardcode API model names.
MODEL_TRIAGE = "claude-haiku-4-5"
MODEL_PULSE = "claude-sonnet-4-6"
MODEL_FOUNDATION = "claude-opus-4-6"


@dataclass
class CallResult:
    text: str
    input_tokens: int
    cache_read_input_tokens: int
    cache_creation_input_tokens: int
    output_tokens: int
    cents: float
    model: str
    purpose: str


class NoAPIKeyError(RuntimeError):
    """Raised when an LLM call is attempted without ANTHROPIC_API_KEY set."""


class Client:
    def __init__(self, cost_log_path: Path | None = None, dry_run: bool = False):
        self.dry_run = dry_run
        self.cost_log_path = cost_log_path
        self._client = None  # lazy init so dry-run never imports SDK

    def _ensure_client(self):
        if self._client is not None:
            return self._client
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise NoAPIKeyError(
                "ANTHROPIC_API_KEY is not set. Either:\n"
                "  1. export ANTHROPIC_API_KEY=sk-ant-...   (in your shell)\n"
                "  2. or run with --dry-run to see what would be sent"
            )
        try:
            import anthropic
        except ImportError as e:
            raise RuntimeError(
                "anthropic SDK not installed. Run: pip install anthropic"
            ) from e
        self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def call(
        self,
        *,
        model: str,
        system: str | list[dict[str, Any]],
        messages: list[dict[str, Any]],
        max_tokens: int = 1024,
        purpose: str = "unknown",
        cache_system: bool = True,
    ) -> CallResult:
        """Single Anthropic Messages call, returning text + token + cost stats.

        `system` may be a string (auto-wrapped with cache_control) or a list of
        content blocks (caller controls cache markers explicitly — used when
        a large reference document should be cached separately from the system
        instructions).

        In dry-run mode no network call happens; an estimated input-token count
        is returned (rough char/4 heuristic) for cost forecasting.
        """
        if isinstance(system, str) and cache_system:
            system_param = [
                {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}
            ]
        else:
            system_param = system

        if self.dry_run:
            est_input = _rough_token_estimate(system_param, messages)
            cents = _cents_for(model, est_input, 0, 0, max_tokens)
            result = CallResult(
                text="[dry-run: no API call made]",
                input_tokens=est_input,
                cache_read_input_tokens=0,
                cache_creation_input_tokens=0,
                output_tokens=max_tokens,
                cents=cents,
                model=model,
                purpose=purpose,
            )
            self._log(result, dry_run=True)
            return result

        sdk = self._ensure_client()
        resp = sdk.messages.create(
            model=model,
            system=system_param,
            messages=messages,
            max_tokens=max_tokens,
        )
        usage = resp.usage
        text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
        cents = _cents_for(
            model,
            usage.input_tokens,
            getattr(usage, "cache_read_input_tokens", 0) or 0,
            getattr(usage, "cache_creation_input_tokens", 0) or 0,
            usage.output_tokens,
        )
        result = CallResult(
            text=text,
            input_tokens=usage.input_tokens,
            cache_read_input_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
            cache_creation_input_tokens=getattr(usage, "cache_creation_input_tokens", 0) or 0,
            output_tokens=usage.output_tokens,
            cents=cents,
            model=model,
            purpose=purpose,
        )
        self._log(result, dry_run=False)
        return result

    def _log(self, r: CallResult, *, dry_run: bool) -> None:
        if not self.cost_log_path:
            return
        self.cost_log_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "model": r.model,
            "purpose": r.purpose,
            "input_tokens": r.input_tokens,
            "cache_read_input_tokens": r.cache_read_input_tokens,
            "cache_creation_input_tokens": r.cache_creation_input_tokens,
            "output_tokens": r.output_tokens,
            "cents": round(r.cents, 4),
            "dry_run": dry_run,
        }
        with self.cost_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


def _rough_token_estimate(system: Any, messages: list[dict[str, Any]]) -> int:
    """Char/4 rough estimate. Fine for dry-run cost forecasting; not authoritative."""
    chars = 0
    if isinstance(system, str):
        chars += len(system)
    elif isinstance(system, list):
        for block in system:
            chars += len(block.get("text", ""))
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, str):
            chars += len(content)
        elif isinstance(content, list):
            for block in content:
                chars += len(block.get("text", ""))
    return max(1, chars // 4)


def _cents_for(model: str, input_t: int, cache_read_t: int, cache_creation_t: int, output_t: int) -> float:
    p = PRICING.get(model)
    if not p:
        return 0.0
    # cache_creation costs same as input; cache_read is the discount
    fresh_input = max(0, input_t - cache_read_t)
    return (
        fresh_input * p["input"]
        + cache_read_t * p["cache_read"]
        + output_t * p["output"]
    ) / 1_000_000
