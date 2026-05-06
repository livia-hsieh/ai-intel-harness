"""Health monitoring — Layer 0 across collector/triage/pulse/engagement.

Per SCOPE.md §10 the meta-loop trigger conditions span four pipeline layers.
This module computes per-layer health signals from the existing DB + cost log,
evaluates them against trigger rules, and produces a human-readable report
the user can act on without retracing the whole pipeline.

Design principle: every trigger is named, justified, and tells the user
exactly what to fix. "Yellow alert: P1 high-signal count <2/week for 4 weeks
→ Mechanism A3 should propose new banking sources" beats "warn: low signal".
"""

__version__ = "0.1.0"
