#!/usr/bin/env bash
# sync-to-wiki.sh — Pull latest from GitHub + copy Foundation/Quarterly
# essays from repo into Livia's local OneDrive wiki.
#
# Cost: $0 — pure file IO, no API calls.
# Run on Mac (anywhere — repo path is hardcoded). Safe to run repeatedly:
# files are overwritten if newer, idempotent.
#
# Recommended: schedule via launchd or run manually after each weekly digest.

set -euo pipefail

REPO_ROOT="/Users/liviahsieh/Documents/Claude/Projects/推廣 AI at Scale Solution"
WIKI_ROOT="/Users/liviahsieh/Library/CloudStorage/OneDrive-IBM/AI 知識庫/wiki"

cd "$REPO_ROOT"

echo "═══════════════════════════════════════════════════════"
echo "  ai-intel-harness → wiki sync"
echo "  $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "═══════════════════════════════════════════════════════"

# 1. Pull latest from GitHub (in case Actions ran while Mac was off)
echo ""
echo "📥 Pulling latest from GitHub..."
git pull --ff-only

# 2. Sync Foundation track essays — per-week version preserved
#    digests/<week>/foundation.md → wiki/concepts/track-<x>/<week>.md
#    Plus a latest.md pointer that always reflects the newest version.
#    SCOPE.md §2: curriculum essays evolve v1 → v2 → v3, never overwrite.
#
# Note: macOS default bash is 3.x (no associative arrays). We use plain
# files in alphanumeric order — week labels like 2026-W19, 2026-W20 sort
# correctly so the LAST-processed file per track IS the newest.
echo ""
echo "📚 Syncing Foundation deep-reads (per-week versions)..."
copied_foundations=0

# Build a sorted list of (track, week, file) tuples, processed in order.
# Last entry per track wins for the latest.md pointer.
tmp_index=$(mktemp)
trap "rm -f $tmp_index" EXIT

for f in digests/*/foundation.md; do
  [ -e "$f" ] || continue
  track=$(grep -oE 'Track [A-G]:' "$f" | head -1 | grep -oE '[A-G]')
  week=$(echo "$f" | sed -E 's|digests/([^/]+)/foundation\.md|\1|')
  if [[ -n "$track" && -n "$week" ]]; then
    track_lower=$(echo "$track" | tr A-Z a-z)
    track_dir="$WIKI_ROOT/concepts/track-${track_lower}"
    mkdir -p "$track_dir"
    cp "$f" "$track_dir/${week}.md"
    echo "   ✓ $f → wiki/concepts/track-${track_lower}/${week}.md"
    copied_foundations=$((copied_foundations + 1))
    # Append to index for latest-pointer pass
    echo "$track_lower|$week|$f" >> "$tmp_index"
  fi
done

# Update latest.md per track from highest week label seen (sort -r picks newest)
if [[ -s "$tmp_index" ]]; then
  for track_lower in $(awk -F'|' '{print $1}' "$tmp_index" | sort -u); do
    newest=$(awk -F'|' -v t="$track_lower" '$1==t {print $2}' "$tmp_index" | sort -r | head -1)
    src="$WIKI_ROOT/concepts/track-${track_lower}/${newest}.md"
    dst="$WIKI_ROOT/concepts/track-${track_lower}/latest.md"
    cp "$src" "$dst"
    echo "   📌 latest pointer → wiki/concepts/track-${track_lower}/latest.md (= ${newest})"
  done
fi

# 3. Sync Quarterly synthesis
#    digests/perspectives/*.md → wiki/perspectives/*.md
echo ""
echo "🌐 Syncing Quarterly perspectives..."
mkdir -p "$WIKI_ROOT/perspectives"
copied_quarterlies=0
if compgen -G "digests/perspectives/*.md" > /dev/null; then
  for f in digests/perspectives/*.md; do
    base=$(basename "$f")
    cp "$f" "$WIKI_ROOT/perspectives/$base"
    echo "   ✓ $f → wiki/perspectives/$base"
    copied_quarterlies=$((copied_quarterlies + 1))
  done
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Summary"
echo "═══════════════════════════════════════════════════════"
echo "  Foundation essays synced: $copied_foundations"
echo "  Quarterly perspectives synced: $copied_quarterlies"
echo "  OneDrive will auto-sync to your iPhone/iPad in ~30 sec."
echo ""
