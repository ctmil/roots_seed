#!/usr/bin/env bash
# sync-agents-skills.sh — move agents/skills between the three layers of the seed:
#
#   base   roots_seed/{agents,skills}/*.md      (cross-project library, this repo)
#   store  <repo>/.roots/{agents,skills}/*.md   (tracked: where they live and evolve)
#   act.   <repo>/.claude/agents/*.md           (local activation, flat .md)
#          <repo>/.claude/skills/<name>/SKILL.md (local activation, directory form)
#
# The store keeps skills as a flat <name>.md; Claude Code wants <name>/SKILL.md. This script
# does that conversion so the two layers cannot drift silently.
#
# Usage:
#   ./sync-agents-skills.sh activate [<name>...]   store  -> .claude   (all if no name given)
#   ./sync-agents-skills.sh harvest  [<name>...]   .claude -> store    (bring local edits back)
#   ./sync-agents-skills.sh import <name>...       base   -> store     (needs --seed)
#   ./sync-agents-skills.sh check                  report drift, exit 1 if any
#   ./sync-agents-skills.sh list                   what exists in each layer
#
# Options:
#   --repo <path>   repo root (default: cwd)
#   --seed <path>   roots_seed checkout (default: ./roots_seed/main, then ./roots_seed)
#   --agents-only | --skills-only
#   -n, --dry-run
#
# Portable: POSIX-ish bash, works with bash 3.2 (stock macOS) and BSD or GNU coreutils.
set -euo pipefail

REPO="$PWD"; SEED=""; DRY=0; DO_AGENTS=1; DO_SKILLS=1; CMD=""; NAMES=()

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
say() { printf '%s\n' "$*"; }
run() { if [ "$DRY" -eq 1 ]; then printf '  [dry-run] %s\n' "$*"; else eval "$@"; fi; }

while [ $# -gt 0 ]; do
  case "$1" in
    activate|harvest|import|check|list) CMD="$1" ;;
    --repo) REPO="${2:?}"; shift ;;
    --seed) SEED="${2:?}"; shift ;;
    --agents-only) DO_SKILLS=0 ;;
    --skills-only) DO_AGENTS=0 ;;
    -n|--dry-run) DRY=1 ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    -*) die "unknown option: $1" ;;
    *) NAMES+=("$1") ;;   # bash 3.1+ (stock macOS bash 3.2 is fine)
  esac
  shift
done
[ -n "$CMD" ] || { sed -n '2,25p' "$0"; exit 1; }

[ -d "$REPO" ] || die "repo not found: $REPO"
STORE_A="$REPO/.roots/agents"; STORE_S="$REPO/.roots/skills"
ACT_A="$REPO/.claude/agents";  ACT_S="$REPO/.claude/skills"

if [ -z "$SEED" ]; then
  for c in "$REPO/roots_seed/main" "$REPO/roots_seed" "$REPO/../roots_seed/main"; do
    [ -d "$c/agents" ] && SEED="$c" && break
  done
fi

wanted() {  # wanted <name> -> 0 if it should be processed
  [ ${#NAMES[@]} -eq 0 ] && return 0
  for n in "${NAMES[@]}"; do [ "$n" = "$1" ] && return 0; done
  return 1
}

# --- agents: flat .md on both sides -------------------------------------------------
sync_agents() {  # sync_agents <src_dir> <dst_dir>
  local src="$1" dst="$2" f base
  [ -d "$src" ] || return 0
  run "mkdir -p '$dst'"
  for f in "$src"/*.md; do
    [ -e "$f" ] || continue
    base="$(basename "$f" .md)"
    case "$base" in README|*.template) continue ;; esac
    wanted "$base" || continue
    if [ -e "$dst/$base.md" ] && cmp -s "$f" "$dst/$base.md"; then continue; fi
    say "  agent  $base"
    run "cp '$f' '$dst/$base.md'"
  done
}

# --- skills: flat <name>.md  <->  <name>/SKILL.md ------------------------------------
skills_to_act() {  # store -> .claude (flat -> dir)
  local f base
  [ -d "$STORE_S" ] || return 0
  for f in "$STORE_S"/*.md; do
    [ -e "$f" ] || continue
    base="$(basename "$f" .md)"
    case "$base" in README) continue ;; esac
    wanted "$base" || continue
    if [ -e "$ACT_S/$base/SKILL.md" ] && cmp -s "$f" "$ACT_S/$base/SKILL.md"; then continue; fi
    say "  skill  $base"
    run "mkdir -p '$ACT_S/$base'"
    run "cp '$f' '$ACT_S/$base/SKILL.md'"
  done
}

skills_to_store() {  # .claude -> store (dir -> flat)
  local d base
  [ -d "$ACT_S" ] || return 0
  run "mkdir -p '$STORE_S'"
  for d in "$ACT_S"/*/; do
    [ -e "$d" ] || continue
    base="$(basename "$d")"
    wanted "$base" || continue
    [ -f "$d/SKILL.md" ] || { say "  ! $base has no SKILL.md — skipped"; continue; }
    if [ -e "$STORE_S/$base.md" ] && cmp -s "$d/SKILL.md" "$STORE_S/$base.md"; then continue; fi
    say "  skill  $base"
    run "cp '$d/SKILL.md' '$STORE_S/$base.md'"
  done
}

case "$CMD" in
  activate)
    say "→ store → activation  ($REPO)"
    [ "$DO_AGENTS" -eq 1 ] && sync_agents "$STORE_A" "$ACT_A"
    [ "$DO_SKILLS" -eq 1 ] && skills_to_act
    say "✓ done. Activation is local — it does not need to be committed."
    ;;
  harvest)
    say "→ activation → store  ($REPO)"
    [ "$DO_AGENTS" -eq 1 ] && sync_agents "$ACT_A" "$STORE_A"
    [ "$DO_SKILLS" -eq 1 ] && skills_to_store
    say "✓ done. The store IS tracked — review and commit the diff."
    ;;
  import)
    [ -n "$SEED" ] || die "seed checkout not found — pass --seed <path>"
    [ ${#NAMES[@]} -gt 0 ] || die "import needs at least one name"
    say "→ base ($SEED) → store"
    [ "$DO_AGENTS" -eq 1 ] && sync_agents "$SEED/agents" "$STORE_A"
    if [ "$DO_SKILLS" -eq 1 ] && [ -d "$SEED/skills" ]; then
      for n in "${NAMES[@]}"; do
        [ -f "$SEED/skills/$n.md" ] || continue
        say "  skill  $n"
        run "mkdir -p '$STORE_S'"
        run "cp '$SEED/skills/$n.md' '$STORE_S/$n.md'"
      done
    fi
    say "✓ imported into the store. Now: $0 activate ${NAMES[*]}"
    ;;
  check)
    drift=0
    for f in "$STORE_A"/*.md; do
      [ -e "$f" ] || continue
      base="$(basename "$f" .md)"; case "$base" in README|*.template) continue ;; esac
      if [ ! -e "$ACT_A/$base.md" ]; then say "store-only agent : $base"; drift=1
      elif ! cmp -s "$f" "$ACT_A/$base.md"; then say "DRIFT agent      : $base"; drift=1; fi
    done
    for f in "$ACT_A"/*.md; do
      [ -e "$f" ] || continue; base="$(basename "$f" .md)"
      [ -e "$STORE_A/$base.md" ] || { say "activation-only agent: $base (not tracked!)"; drift=1; }
    done
    for f in "$STORE_S"/*.md; do
      [ -e "$f" ] || continue
      base="$(basename "$f" .md)"; case "$base" in README) continue ;; esac
      if [ ! -e "$ACT_S/$base/SKILL.md" ]; then say "store-only skill : $base"; drift=1
      elif ! cmp -s "$f" "$ACT_S/$base/SKILL.md"; then say "DRIFT skill      : $base"; drift=1; fi
    done
    for d in "$ACT_S"/*/; do
      [ -e "$d" ] || continue; base="$(basename "$d")"
      [ -e "$STORE_S/$base.md" ] || { say "activation-only skill: $base (not tracked!)"; drift=1; }
    done
    [ "$drift" -eq 0 ] && say "✓ store and activation are in sync" || say "→ fix with: $0 activate | harvest"
    exit "$drift"
    ;;
  list)
    printf '%-28s %-8s %-8s %s\n' NAME BASE STORE ACTIVE
    seed_names=""; [ -n "$SEED" ] && seed_names="$(ls "$SEED/agents" "$SEED/skills" 2>/dev/null | sed 's/\.md$//')"
    all="$( { ls "$STORE_A" "$STORE_S" 2>/dev/null | sed 's/\.md$//'
              ls "$ACT_A" 2>/dev/null | sed 's/\.md$//'
              ls "$ACT_S" 2>/dev/null
              printf '%s\n' "$seed_names"; } | grep -v '^README$' | grep -v '^$' | sort -u )"
    for n in $all; do
      b=" "; s=" "; a=" "
      printf '%s\n' "$seed_names" | grep -qx "$n" && b="yes"
      { [ -e "$STORE_A/$n.md" ] || [ -e "$STORE_S/$n.md" ]; } && s="yes"
      { [ -e "$ACT_A/$n.md" ] || [ -e "$ACT_S/$n/SKILL.md" ]; } && a="yes"
      printf '%-28s %-8s %-8s %s\n' "$n" "$b" "$s" "$a"
    done
    ;;
esac
