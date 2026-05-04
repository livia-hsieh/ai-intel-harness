"""Collector — Layer 1 of the AI Intel Pipeline.

Wide scan over ~140 sources defined in sources.yaml. Stores deduplicated raw
items into SQLite. Does NOT triage or synthesize — that's Task #4.
"""

__version__ = "0.1.0"
