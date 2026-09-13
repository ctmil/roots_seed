#!/usr/bin/env bash
# leaf-fall.sh — leaf fall: sweep the litter off the Forest floor.
#
#   Roots > Forest > Grove > Tree > Branch > Leaf
#
# A LEAF is an ephemeral session artifact (a DOM snapshot, a verification capture, a raw API
# dump). It hangs from a Branch — a task — not from the Forest, and it is DESIGNED to fall.
# Its place is .roots/workbench/leaves/<date>-<front>/ ; the Forest floor (the workspace root) is NOT.
#
# Why this exists: measured on a live Forest, the root had 1929 loose files / 246 MB, INVISIBLE to
# `git status` because the .gitignore starts with `/*`. The origin of the mess was a missing noun.
#
# HYGIENE WARNS, IT DOES NOT BLOCK: nothing here rejects a commit or interrupts a session.
# A check that blocks ends up bypassed with --no-verify; one that warns gets read.
#
# Usage:
#   leaf-fall.sh status            # count the litter on the floor + what has already fallen
#   leaf-fall.sh sweep [front]     # MOVE what is loose into leaves/<today>-<front>  (default: floor)
#   leaf-fall.sh compost [days]    # list fallen piles older than N days (default 30)
#
# Config (env):
#   FOREST       root of the workspace            (default: $CLAUDE_PROJECT_DIR, else $PWD)
#   LEAF_KEEP    extra floor allowlist, space-separated globs   (e.g. "Makefile *.code-workspace")
set -uo pipefail

FOREST="${FOREST:-${CLAUDE_PROJECT_DIR:-$PWD}}"
LEAVES_DIR="$FOREST/.roots/workbench/leaves"

# What legitimately lives on the Forest floor; everything else is a leaf.
# Directories are NEVER touched: they are Trees (bare+worktree repos) and coordination layers.
is_kept() {
  case "$1" in
    CLAUDE.md|README.md|LICENSE|.gitignore|.gitmodules|.editorconfig) return 0 ;;
    forest.json|fleet.json|*.code-workspace|Makefile) return 0 ;;
    setup-module.sh|setupbranch.sh|pull-all.sh|dashboard.sh) return 0 ;;
  esac
  local pat
  for pat in ${LEAF_KEEP:-}; do
    # shellcheck disable=SC2053
    [[ "$1" == $pat ]] && return 0
  done
  return 1
}

# List the loose leaves: regular files on the floor, no recursion, allowlist excluded.
list_litter() {
  local f base
  for f in "$FOREST"/* "$FOREST"/.[!.]*; do
    [ -f "$f" ] || continue
    base="${f##*/}"
    is_kept "$base" && continue
    printf '%s\n' "$f"
  done
}

human() { numfmt --to=iec --suffix=B "${1:-0}" 2>/dev/null || echo "${1:-0}B"; }

cmd_status() {
  local n=0 bytes=0 sz oldest="" base piles
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    n=$((n + 1))
    sz=$(stat -c %s "$f" 2>/dev/null || echo 0)
    bytes=$((bytes + sz))
    if [ -z "$oldest" ] || [ "$f" -ot "$oldest" ]; then oldest="$f"; fi
  done < <(list_litter)

  echo "Forest floor ($FOREST)"
  if [ "$n" -eq 0 ]; then
    echo "  clean — 0 loose leaves."
  else
    echo "  $n loose leaves · $(human "$bytes")"
    [ -n "$oldest" ] && echo "  oldest: ${oldest##*/} ($(date -r "$oldest" +%F 2>/dev/null))"
    echo "  by type:"
    list_litter | while IFS= read -r f; do
      base="${f##*/}"
      case "$base" in *.*) echo "${base##*.}" ;; *) echo "(no extension)" ;; esac
    done | sort | uniq -c | sort -rn | head -8 | sed 's/^/    /'
    echo
    echo "  -> sweep with: $0 sweep <front>"
  fi

  echo
  echo "Already fallen ($LEAVES_DIR)"
  if [ -d "$LEAVES_DIR" ]; then
    piles=$(find "$LEAVES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
    echo "  $piles piles · $(du -sh "$LEAVES_DIR" 2>/dev/null | cut -f1)"
  else
    echo "  (not created yet)"
  fi
}

cmd_sweep() {
  local front="${1:-floor}" dest n=0
  dest="$LEAVES_DIR/$(date +%F)-$front"

  if [ -z "$(list_litter)" ]; then
    echo "Floor is clean — nothing to sweep."
    return 0
  fi

  mkdir -p "$dest" || return 1
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    mv -n -- "$f" "$dest/" && n=$((n + 1))
  done < <(list_litter)

  echo "$n leaves moved to $dest"
  echo "Reminder: what these leaves taught should ALREADY be in .roots/ (plan / doc / decision)."
}

cmd_compost() {
  local days="${1:-30}"
  echo "Leaf piles older than $days days in $LEAVES_DIR:"
  find "$LEAVES_DIR" -mindepth 1 -maxdepth 1 -type d -mtime "+$days" \
    -printf '  %f\t' -exec du -sh {} \; 2>/dev/null | cut -f1,3
  echo
  echo "Delete by hand and with judgement: first verify the finding went down into .roots/."
}

case "${1:-status}" in
  status)  cmd_status ;;
  sweep)   cmd_sweep "${2:-}" ;;
  compost) cmd_compost "${2:-}" ;;
  *) sed -n '2,22p' "$0"; exit 2 ;;
esac
