# Pipeline Health Report

_Generated: 2026-05-06T03:52:52+00:00_

## Overall
🟡 1 yellow alert(s) — no reds

## State snapshot

**Collector**:
- 6 sources tracked, 5 fetched in last 30 days
- 928 / 1073 items have excerpt (86%)

**Triage**:
- high (≥0.6): 146 · watch (0.3–0.6): 89 · skip: 73 · untriaged: 765
- high-signal score stats: mean=0.692, stddev=0.04, range=[0.6, 0.75]
- high-signal per Pillar: P1=41, P2=39, P3=61, P4=136, P5=12

**Cost**:
- last 7 days: $0.6769 (alarm at $5)
- total to date: $0.6769

## Triggered alerts

### 🟡 [triage] Score compression in high-signal bucket

**Detail:**
```
High-signal items: count=146, mean=0.69, stddev=0.040 (target stddev ≥0.05)
```

**Fix:**

Haiku is collapsing all high items to ~0.70 instead of differentiating 0.65 'solid' vs 0.85 'must-read'. Pulse can't pick true Top 3.
Either: (a) tighten triage prompt's signal calibration section, (b) feed triage more cross-source diversity (single-source samples compress naturally).

_Reference: synthesizer/prompts.py TRIAGE_SYSTEM § 'Signal calibration'_

