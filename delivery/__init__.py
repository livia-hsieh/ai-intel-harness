"""Delivery — Layer 3 of the AI Intel Pipeline.

Takes raw Pulse / Foundation outputs and assembles them into the final
weekly digest format Livia actually reads. Applies visual improvements via
post-processing (no API calls): emoji provenance markers, TOC, per-Pillar
mini-TL;DR, reading time, hero Mermaid map.

Per CLAUDE.md / SCOPE.md, the canonical output goes to digests/YYYY-WNN.md
in the repo root, committed to git as portfolio artifact.
"""

__version__ = "0.1.0"
