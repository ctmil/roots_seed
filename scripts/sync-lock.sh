#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# sync-lock.sh — SYNC semaphore: one flag per Tree, so two sessions do not sync the same
# module at once (which is how uncommitted changes get overwritten between sessions).
#
# Sibling of work-claim.sh: that one protects the WORK (the subject); this one protects the
# WORKTREES (the files).
#
# Convention:
#   - The flag lives in the CONTAINER of the Tree's branches: <container>/<module>/.SYNCING —
#     NOT inside each branch: per-branch would be recursive, slow, and would leave stale flags
#     behind when a session dies.
#   - Content: FREE | LOCKED|by=…|since=ISO8601|scope=…|task=…
#   - BEFORE touching a Tree's worktrees (above all a cross-version sync): `check`.
#   - The `.SYNCING` files are RUNTIME state: out of git, never committed.
#
# Usage:
#   sync-lock.sh check   <module>
#   sync-lock.sh acquire <module> "<task>"   # fails if LOCKED by another and not stale
#   sync-lock.sh release <module>            # leaves FREE
#   sync-lock.sh list                        # forest view: every .SYNCING
#
# Steal a stale lock: SYNC_FORCE=1 · identity: export SYNC_WHO="<session>"
# Container: export SYNC_WT_CONTAINER=<workspace root>   (default: $CLAUDE_PROJECT_DIR or $PWD)
#
# Why a plain file and not a git operation: a lock must be readable and writable in one syscall,
# must not produce merge conflicts, and must survive a session that dies without cleaning up.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

WT_CONTAINER="${SYNC_WT_CONTAINER:-${CLAUDE_PROJECT_DIR:-$PWD}}"
STALE_SECS="${SYNC_STALE_SECS:-7200}"    # 2h: an older LOCKED is treated as abandoned
WHO="${SYNC_WHO:-$(whoami)@$(hostname -s 2>/dev/null || echo host)}"

cmd="${1:-}"; mod="${2:-}"; task="${3:-}"
flag_path() { printf '%s/%s/.SYNCING' "$WT_CONTAINER" "$1"; }
now_iso() { date -u +%Y-%m-%dT%H:%M:%SZ; }

read_state() { local f; f="$(flag_path "$1")"; [ -f "$f" ] && head -n1 "$f" || echo "FREE"; }

is_locked_by_other() {   # 0 = LOCKED by someone else and NOT stale
  local line; line="$(read_state "$1")"
  case "$line" in
    LOCKED\|*)
      local since owner age
      since="$(printf '%s' "$line" | sed -n 's/.*since=\([^|]*\).*/\1/p')"
      owner="$(printf '%s' "$line" | sed -n 's/.*by=\([^|]*\).*/\1/p')"
      [ "$owner" = "$WHO" ] && return 1
      age=$(( $(date -u +%s) - $(date -u -d "$since" +%s 2>/dev/null || echo 0) ))
      [ "$age" -gt "$STALE_SECS" ] && return 1
      return 0 ;;
    *) return 1 ;;
  esac
}

case "$cmd" in
  check)
    [ -n "$mod" ] || { echo "usage: sync-lock.sh check <module>"; exit 2; }
    read_state "$mod" ;;
  acquire)
    [ -n "$mod" ] || { echo "usage: sync-lock.sh acquire <module> \"<task>\""; exit 2; }
    if [ "${SYNC_FORCE:-0}" != "1" ] && is_locked_by_other "$mod"; then
      echo "BLOCKED: $(read_state "$mod")"
      echo "  (another session is syncing '$mod'. Wait, or SYNC_FORCE=1 if it is stale.)"
      exit 1
    fi
    f="$(flag_path "$mod")"; mkdir -p "$(dirname "$f")"
    printf 'LOCKED|by=%s|since=%s|scope=%s|task=%s\n' "$WHO" "$(now_iso)" "$mod" "${task:-sync}" > "$f"
    echo "LOCKED '$mod' by $WHO" ;;
  release)
    [ -n "$mod" ] || { echo "usage: sync-lock.sh release <module>"; exit 2; }
    f="$(flag_path "$mod")"; mkdir -p "$(dirname "$f")"
    echo "FREE" > "$f"
    echo "FREE '$mod' (released by $WHO)" ;;
  list)
    echo "=== sync semaphore — $WT_CONTAINER/*/.SYNCING ==="
    found=0
    for f in "$WT_CONTAINER"/*/.SYNCING; do
      [ -f "$f" ] || continue
      st="$(head -n1 "$f")"; m="$(basename "$(dirname "$f")")"
      case "$st" in LOCKED\|*) echo "  LOCKED $m : $st"; found=1 ;; esac
    done
    [ "$found" = 0 ] && echo "  (all FREE — no module is being synced)" ;;
  *)
    echo "usage: sync-lock.sh {check|acquire|release|list} <module> [\"task\"]"; exit 2 ;;
esac
