"""Post-processing: turn raw Pulse output into the final reader-friendly digest.

Pure local transformations, zero API cost:
- Strip log lines (INFO / DEBUG / HTTP) so only Markdown content remains
- Convert provenance markers to emojis: [原文] → 📖 / [推論] → 🧠 / [假設] → ⚠️
- Same conversion for English equivalents
- Generate TOC at the top with anchor links
- Generate per-Pillar mini-TL;DR (extract Top 1's 繁中 headline)
- Compute reading time estimate
- Add hero metadata block (week, Pillar item counts, total cost)

Input:  raw `pulse --all` stdout (mixed log + Markdown)
Output: clean `digests/<week>.md` ready to commit

Why a single output file (not per-Pillar files):
- Easier to read on phone (one scroll instead of nav)
- Single git diff per week shows what changed
- Matches SCOPE.md §5 Output Shape spec
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("assemble")

# Provenance marker substitutions (ZH + EN forms).
PROVENANCE_SUBS = [
    (r"\[原文\]", "📖 **原文**"),
    (r"\[推論\]", "🧠 **推論**"),
    (r"\[假設\]", "⚠️ **假設**"),
    (r"\[Source\]", "📖 **Source**"),
    (r"\[Inferred\]", "🧠 **Inferred**"),
    (r"\[Assumed\]", "⚠️ **Assumed**"),
]

# Patterns to drop from raw pulse stdout.
DROP_LINE_PATTERNS = [
    re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+ (INFO|DEBUG|WARNING) "),
    re.compile(r"^={50,}$"),                    # =====...=== separator lines
    re.compile(r"^Pulse run summary$"),
    re.compile(r"^\s*Pillar \d+ \([^)]+\) +items=\s*\d+\s+cents="),  # final summary table
    re.compile(r"^\s*TOTAL: \$"),
]

# `# Pillar N — name` and `# X items · Y USD` produced as comments by run_pulse.
# We DON'T drop these — we transform them into proper section dividers.

PILLAR_HEADER_RE = re.compile(r"^#\s+Pillar\s+(\d+)\s+—\s+(.+?)$")
PILLAR_META_RE = re.compile(r"^#\s+(\d+)\s+items\s+·\s+([\d.]+)\s+USD\s*$")


@dataclass
class PillarBlock:
    n: int
    name: str
    item_count: int
    cost_usd: float
    body: str  # everything after the meta line, before the next pillar
    top1_headline: str | None = None  # extracted for mini-TL;DR


def parse_pulse_output(text: str) -> list[PillarBlock]:
    """Split raw pulse stdout into per-Pillar blocks. Strips logs along the way."""
    lines = text.splitlines()

    # First pass: drop log / separator lines.
    cleaned: list[str] = []
    for line in lines:
        if any(p.search(line) for p in DROP_LINE_PATTERNS):
            continue
        cleaned.append(line)

    # Second pass: chunk by Pillar header.
    blocks: list[PillarBlock] = []
    cur_pillar: int | None = None
    cur_name = ""
    cur_count = 0
    cur_cost = 0.0
    cur_body: list[str] = []

    def flush():
        if cur_pillar is None:
            return
        body = "\n".join(cur_body).strip()
        top1 = _extract_top1_headline(body)
        blocks.append(PillarBlock(
            n=cur_pillar, name=cur_name, item_count=cur_count,
            cost_usd=cur_cost, body=body, top1_headline=top1,
        ))

    i = 0
    while i < len(cleaned):
        line = cleaned[i]
        m = PILLAR_HEADER_RE.match(line)
        if m:
            flush()
            cur_pillar = int(m.group(1))
            cur_name = m.group(2).strip()
            cur_count = 0
            cur_cost = 0.0
            cur_body = []
            # next line should be the meta `# X items · Y USD`
            if i + 1 < len(cleaned):
                meta_match = PILLAR_META_RE.match(cleaned[i + 1])
                if meta_match:
                    cur_count = int(meta_match.group(1))
                    cur_cost = float(meta_match.group(2))
                    i += 2
                    continue
            i += 1
            continue
        if cur_pillar is not None:
            cur_body.append(line)
        i += 1
    flush()
    return blocks


def _extract_top1_headline(body: str) -> str | None:
    """Find the first `### 1. <headline>` line and return its text."""
    for line in body.splitlines():
        m = re.match(r"^###\s+1\.\s+(.+?)\s*$", line)
        if m:
            return m.group(1)
    return None


def apply_provenance_emoji(text: str) -> str:
    for pat, repl in PROVENANCE_SUBS:
        text = re.sub(pat, repl, text)
    return text


def estimate_reading_time(text: str) -> int:
    """繁中 ~250 chars/min, EN ~250 words/min. Rough average."""
    word_chars = len(text)
    return max(1, round(word_chars / 600))  # ~600 chars/min mixed bilingual


def build_toc(blocks: list[PillarBlock]) -> str:
    lines = ["## 📑 目錄"]
    for b in blocks:
        anchor = f"pillar-{b.n}"
        lines.append(f"- [Pillar {b.n} — {b.name}](#{anchor}) · {b.item_count} items · ${b.cost_usd:.4f}")
    return "\n".join(lines)


def build_mini_tldr(blocks: list[PillarBlock]) -> str:
    lines = ["## ⚡ 本週 TL;DR — 5 Pillar 各一句"]
    pillar_emoji = {1: "🏦", 2: "📊", 3: "🚀", 4: "🛠️", 5: "🌐"}
    for b in blocks:
        emoji = pillar_emoji.get(b.n, "📌")
        head = b.top1_headline or "(no Top 1 found)"
        lines.append(f"- {emoji} **P{b.n}**: {head}")
    return "\n".join(lines)


def build_hero_block(week: str, blocks: list[PillarBlock], total_cost_usd: float, reading_min: int) -> str:
    total_items = sum(b.item_count for b in blocks)
    return (
        f"# 🗞️ AI Intel Digest — {week}\n\n"
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        f"{total_items} high-signal items synthesized · "
        f"${total_cost_usd:.4f} USD cost · "
        f"~{reading_min} 分鐘讀完_\n"
    )


def reformat_pillar_block(b: PillarBlock) -> str:
    """Rewrite each Pillar's section with anchor + emoji-converted body."""
    anchor = f"<a id=\"pillar-{b.n}\"></a>"
    pillar_emoji = {1: "🏦", 2: "📊", 3: "🚀", 4: "🛠️", 5: "🌐"}
    emoji = pillar_emoji.get(b.n, "📌")
    header = (
        f"\n---\n\n{anchor}\n\n## {emoji} Pillar {b.n} — {b.name}\n"
        f"_{b.item_count} items · ${b.cost_usd:.4f}_\n"
    )
    body = apply_provenance_emoji(b.body)
    return header + "\n" + body


def assemble(raw_pulse_text: str, week: str) -> str:
    blocks = parse_pulse_output(raw_pulse_text)
    if not blocks:
        return f"# AI Intel Digest — {week}\n\n_(empty: no Pillar content found in input)_\n"

    total_cost_usd = sum(b.cost_usd for b in blocks)
    full_text = "\n".join(b.body for b in blocks)
    reading_min = estimate_reading_time(full_text)

    out_parts = [
        build_hero_block(week, blocks, total_cost_usd, reading_min),
        "",
        build_mini_tldr(blocks),
        "",
        build_toc(blocks),
        "",
    ]
    for b in blocks:
        out_parts.append(reformat_pillar_block(b))

    out_parts.append("")
    out_parts.append("---")
    out_parts.append("")
    out_parts.append("## 📋 引用清單（spot-check 用）")
    out_parts.append("")
    out_parts.append("_本期所有引用 URL 集中於各 Pillar 的 Source / 來源 行；驗證提示集中於各 Pillar 末段 Verification hints。_")
    out_parts.append("")
    return "\n".join(out_parts)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="assemble-digest", description="Post-process pulse output into final digest.")
    p.add_argument("--input", "-i", type=Path, default=None,
                   help="Path to raw pulse output (default: read from stdin)")
    p.add_argument("--output", "-o", type=Path, default=None,
                   help="Output path (default: digests/<week>.md)")
    p.add_argument("--week", type=str, default=None,
                   help="Week label e.g. 2026-W19 (default: ISO week of today)")
    p.add_argument("--print", action="store_true",
                   help="Also echo the assembled digest to stdout")
    args = p.parse_args(argv)

    if args.input:
        text = args.input.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    week = args.week or datetime.now().strftime("%Y-W%V")
    digest = assemble(text, week)

    if args.output is None:
        repo_root = Path(__file__).resolve().parent.parent
        digests_dir = repo_root / "digests"
        digests_dir.mkdir(exist_ok=True)
        out = digests_dir / f"{week}.md"
    else:
        out = args.output

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(digest, encoding="utf-8")
    print(f"wrote {out} ({len(digest)} chars, {digest.count(chr(10))} lines)")

    if args.print:
        print()
        print(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
