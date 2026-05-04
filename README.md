# ai-intel-harness

> Weekly AI intelligence pipeline serving a Practitioner-Strategist Hybrid: IBM consultant selling AI transformation to Taiwan banks + manufacturers, and harness engineer in formation. Built in public as a portfolio artifact for harness engineering work.

## Architecture

```
~140 sources  →  Wide Scan (~$0)  →  Cheap Filter (Haiku 4.5, ~$0.05/wk)
                                       ↓
              Selective Deep Read (Sonnet 4.6, ~$0.60/wk)
                       +
              Foundation Deep Dive (Opus 4.6, ~$2/wk, rotates weekly through curriculum)
                       ↓
              Bilingual digest (English first, 繁中 with English jargon)
                       ↓
              `digests/YYYY-WNN.md` in this repo + email notification with link
```

Total budget: ~$150–200/year.

## Status

Day 1. Currently building Task #3: collector + dedup. See [`PROJECT_LOG.md`](PROJECT_LOG.md) for canonical state, [`SCOPE.md`](SCOPE.md) for the contract, [`sources.yaml`](sources.yaml) for the source registry.

## Why this exists

Three goals stacked on the same artifact:

1. **Operational** — keep client-facing AI vocabulary current for sales conversations
2. **Learning** — internalize harness engineering by building a real harness end-to-end
3. **Portfolio** — every weekly digest + every commit becomes hiring signal

## The harness engineering bet

Each scaffolding choice (a hardcoded rule, a strict filter, a forced format) encodes "the model can't do this alone." The discipline: justify each one, test removability when models improve, and write up the trade-off as a design note. Several anti-patterns have already been caught and removed — see [`PROJECT_LOG.md`](PROJECT_LOG.md) for the running list.

## Layout

```
collector/        # Task #3 — wide scan + dedup
synthesizer/      # Task #4 — Haiku triage + Sonnet/Opus synthesis (not yet built)
delivery/         # Task #5 — write to digests/, email notification (not yet built)
data/             # SQLite dedup DB (committed once stable)
digests/          # Weekly outputs, YYYY-WNN.md format
```

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
collect            # run the wide scan
```

## License

MIT.
