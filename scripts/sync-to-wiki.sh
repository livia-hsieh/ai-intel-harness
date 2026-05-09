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

# 2. Sync Foundation track essays
#    digests/<week>/foundation.md → wiki/concepts/track-<x>.md
echo ""
echo "📚 Syncing Foundation deep-reads..."
mkdir -p "$WIKI_ROOT/concepts"
copied_foundations=0
for f in digests/*/foundation.md; do
  [ -e "$f" ] || continue
  # Extract Track id from the file content (header has "Track <X>: ...")
  track=$(grep -oE 'Track [A-G]:' "$f" | head -1 | grep -oE '[A-G]')
  if [[ -n "$track" ]]; then
    track_lower=$(echo "$track" | tr A-Z a-z)
    cp "$f" "$WIKI_ROOT/concepts/track-${track_lower}.md"
    echo "   ✓ $f → wiki/concepts/track-${track_lower}.md"
    copied_foundations=$((copied_foundations + 1))
  fi
done

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
