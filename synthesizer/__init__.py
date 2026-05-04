"""Synthesizer — Layer 2/3 of the AI Intel Pipeline.

Three sub-stages:
- Triage (Haiku 4.5): per-item Pillar relevance + signal density. Cheap, runs
  on every collected item before any expensive synthesis sees it.
- Pulse (Sonnet 4.6): per-Pillar weekly briefing from triaged items.
- Foundation (Opus 4.6): rotating curriculum deep-read, one Pillar/track per week.

Per SCOPE.md §9, the cost split is intentional: Haiku culls the long tail so
Sonnet/Opus only see signal-dense items. Cost target ~$3/week.
"""

__version__ = "0.1.0"
