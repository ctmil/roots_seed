#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# work-claim.sh — WORK semaphore between sessions (subjects, not files).
#
# Sibling of sync-lock.sh: that one protects WORKTREES (two sessions overwriting each other's
# uncommitted files); this one protects the WORK — that two sessions do not take the same subject
# without knowing. Nothing in a tracker or a chat says "somebody is already looking at this".
#
# Convention:
#   - One file per scope in <CLAIM_DIR>/<scope>.claim — RUNTIME, out of git (a lock is not a commit
#     and must never produce a merge conflict).
#   - Content: LOCKED|by=…|since=…|touched=…|session=…|loop=…|note=…
#   - Scope = flat subject id: task-<id> · project-<id> · domain-<name> · module-<name> · client-<id>
#   - BEFORE entering a front: `check`. Held by someone else and fresh -> do NOT touch; leave your
#     contribution on the bus (state/comms.md) addressed to the owner.
#
# Usage:
#   work-claim.sh check <scope>           # FREE | LOCKED   (exit 3 = someone else's)
#   work-claim.sh take  <scope> "<note>"  # take it (refuses if held by a live other session)
#   work-claim.sh touch <scope>           # heartbeat: still on it
#   work-claim.sh release <scope>
#   work-claim.sh list [filter] | mine [filter] | owner <scope>
#
# Identity:  export CLAIM_WHO="<role>"      (default: $CLAUDE_TAB, else user@host)
# Loop:      export CLAIM_LOOP="review@10m" (declared; see below)
# Steal a claim of a DEAD session: CLAIM_FORCE=1
#
# WHY `by=` IS NOT ENOUGH: it is a ROLE, and several tabs share it. What identifies a session is
# `session=<tab>/<pid>/<uuid8>` — and with the pid, liveness is a VERIFIABLE FACT (does the session's
# runtime socket still exist?) instead of an inference from elapsed time. More precise than signalling
# the pid: a recycled pid has no such socket.
#   ALIVE / DEAD / ?   (? = claim older than the field, or no way to probe — never a verdict)
#
# ⚠️ A liveness probe MUST detect ITSELF first. A guessed socket path once reported 16 of 16 DEAD,
#    including the session running the check — which reads as "16 abandoned fronts" and invites
#    stealing work from people who are working. Hence `work-claim.sh check --self`.
#
# ⚠️ `loop=` IS DECLARED, NOT DETECTED (nothing in the environment reveals a running loop). It is
#    kept honest two ways: a loop declared by a DEAD session prints as `<spec>!`, and every `touch`
#    rewrites it, so a stopped loop corrects itself.
#    AND THE TRAP THAT COST US: a `touch` from another shell invocation does NOT carry the exported
#    variable, so blindly rewriting `loop=` with whatever is in the environment WIPES the declared
#    value. Measured once as 10 of 16 claims with an empty field — not distracted sessions, the
#    instrument erasing it. An empty `loop=` is what makes a front look retained-and-unreachable.
#    ⇒ we distinguish "declared empty" from "not declared" with ${CLAIM_LOOP+set} and only rewrite
#    when the variable actually EXISTS.
# ─────────────────────────────────────────────────────────────────────────────
set -uo pipefail

CLAIM_DIR="${CLAIM_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}/.claims}"
STALE_SECS="${CLAIM_STALE_SECS:-28800}"        # 8h — a subject is held for hours, not minutes
WHO="${CLAIM_WHO:-${CLAUDE_TAB:-$(whoami)@$(hostname -s 2>/dev/null || echo host)}}"
SOCK_DIR="${CLAUDE_SOCK_DIR:-${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/cc-socks}"
_sid="${CLAUDE_CODE_SESSION_ID:-}"
SESSION="${CLAUDE_TAB:-?}/${CLAUDE_PID:-?}/${_sid:0:8}"
LOOP_DECLARED="${CLAIM_LOOP+set}"              # "set" only if the variable EXISTS (even if empty)
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
epoch() { date -u -d "${1:-now}" +%s 2>/dev/null || echo 0; }

field() { printf '%s' "$1" | tr '|' '\n' | sed -n "s/^$2=//p" | head -1; }

alive() {   # <session-field> -> ALIVE | DEAD | ?
  local sess="$1" pid
  [ -z "$sess" ] && { echo "?"; return; }
  [ -d "$SOCK_DIR" ] || { echo "?"; return; }   # cannot probe -> never claim DEAD
  pid="$(printf '%s' "$sess" | cut -d/ -f2)"
  case "$pid" in ''|*[!0-9]*) echo "?"; return ;; esac
  [ -S "$SOCK_DIR/$pid.sock" ] && echo "ALIVE" || echo "DEAD"
}

same_session() {   # -> yes | no | ?   (compares the uuid8; on doubt "?", NEVER "no")
  local a b
  a="$(printf '%s' "$1"       | cut -d/ -f3)"
  b="$(printf '%s' "$SESSION" | cut -d/ -f3)"
  if [ -n "$a" ] && [ -n "$b" ] && [ "$a" != "?" ] && [ "$b" != "?" ]; then
    [ "$a" = "$b" ] && echo yes || echo no; return
  fi
  [ "$1" = "$SESSION" ] && echo yes || echo "?"
}

foreign() {   # <by> <session> <live> -> 1 if the claim belongs to somebody else
  [ "$1" != "$WHO" ] && { echo 1; return; }
  [ "$(same_session "$2")" = "no" ] && [ "$3" = "ALIVE" ] && { echo 1; return; }
  echo 0
}

read_claim() { cat "$CLAIM_DIR/$1.claim" 2>/dev/null; }

# The probe must see ITSELF before anyone trusts its verdicts.
self_check() {
  echo "socket dir : $SOCK_DIR $([ -d "$SOCK_DIR" ] && echo '(exists)' || echo '(MISSING -> everything reports ?)')"
  echo "my session : $SESSION -> $(alive "$SESSION")"
  if [ "$(alive "$SESSION")" = "DEAD" ]; then
    echo "SELF-CHECK FAILED: the probe says the session running it is dead."
    echo "Do NOT trust any DEAD verdict (and do not steal any claim) until the path is fixed."
    return 1
  fi
}

cmd_check() {
  [ "${1:-}" = "--self" ] && { self_check; return $?; }
  local sc="${1:?scope}" c by sess live t age
  c="$(read_claim "$sc")"
  [ -z "$c" ] && { echo "FREE $sc"; return 0; }
  by="$(field "$c" by)"; sess="$(field "$c" session)"; live="$(alive "$sess")"
  t="$(field "$c" touched)"; age=$(( $(epoch) - $(epoch "$t") ))
  printf 'LOCKED %s | by=%s | session=%s | %s | loop=%s | touched=%ss ago%s\n' \
    "$sc" "$by" "$sess" "$live" "$(field "$c" loop)" "$age" \
    "$([ "$age" -gt "$STALE_SECS" ] && echo ' [STALE]')"
  if [ "$(foreign "$by" "$sess" "$live")" = 1 ]; then
    if [ "$live" = "DEAD" ] && [ "$age" -gt "$STALE_SECS" ]; then
      echo "  -> STALE + DEAD: free to take (CLAIM_FORCE=1)."
    else
      echo "  -> someone else's. Do NOT take it; leave your note on the bus for @$by."
      [ "$age" -gt "$STALE_SECS" ] && echo "  -> STALE but ALIVE = working without checking in. Still not yours."
    fi
    return 3
  fi
}

cmd_take() {
  local sc="${1:?scope}" note="${2:-}" c by sess live age
  c="$(read_claim "$sc")"
  if [ -n "$c" ]; then
    by="$(field "$c" by)"; sess="$(field "$c" session)"; live="$(alive "$sess")"
    age=$(( $(epoch) - $(epoch "$(field "$c" touched)") ))
    if [ "$(foreign "$by" "$sess" "$live")" = 1 ] && [ "${CLAIM_FORCE:-0}" != 1 ]; then
      if [ "$live" = "DEAD" ] && [ "$age" -gt "$STALE_SECS" ]; then
        echo "held by $by but STALE+DEAD — re-run with CLAIM_FORCE=1 to take it."
      else
        echo "held by $by ($live). Not taking it."; fi
      return 3
    fi
  fi
  mkdir -p "$CLAIM_DIR"
  printf 'LOCKED|by=%s|since=%s|touched=%s|session=%s|loop=%s|note=%s\n' \
    "$WHO" "$(now)" "$(now)" "$SESSION" "${CLAIM_LOOP:-}" "$note" > "$CLAIM_DIR/$sc.claim"
  echo "took $sc as $WHO"
}

cmd_touch() {
  local sc="${1:?scope}" c loop
  c="$(read_claim "$sc")"; [ -z "$c" ] && { echo "no claim on $sc"; return 1; }
  # Keep the DECLARED loop unless this shell actually declares one (see the trap in the header).
  if [ "$LOOP_DECLARED" = "set" ]; then loop="${CLAIM_LOOP:-}"; else loop="$(field "$c" loop)"; fi
  printf 'LOCKED|by=%s|since=%s|touched=%s|session=%s|loop=%s|note=%s\n' \
    "$(field "$c" by)" "$(field "$c" since)" "$(now)" "$SESSION" "$loop" "$(field "$c" note)" \
    > "$CLAIM_DIR/$sc.claim"
  echo "touched $sc"
}

cmd_release() {
  local sc="${1:?scope}" c by sess
  c="$(read_claim "$sc")"; [ -z "$c" ] && { echo "$sc was free"; return 0; }
  by="$(field "$c" by)"; sess="$(field "$c" session)"
  if [ "$(foreign "$by" "$sess" "$(alive "$sess")")" = 1 ] && [ "${CLAIM_FORCE:-0}" != 1 ]; then
    echo "held by $by — not releasing someone else's claim."; return 3; fi
  rm -f "$CLAIM_DIR/$sc.claim"; echo "released $sc"
}

cmd_list() {
  local filt="${1:-}" f sc c live lp age
  [ -d "$CLAIM_DIR" ] || { echo "(no claims)"; return 0; }
  printf '%-26s %-14s %-6s %-14s %s\n' SCOPE OWNER STATE LOOP NOTE
  for f in "$CLAIM_DIR"/*.claim; do
    [ -e "$f" ] || continue
    sc="$(basename "$f" .claim)"; [ -n "$filt" ] && case "$sc" in *"$filt"*) ;; *) continue ;; esac
    c="$(cat "$f")"; live="$(alive "$(field "$c" session)")"; lp="$(field "$c" loop)"
    [ -z "$lp" ] && lp="-"; [ "$live" = DEAD ] && [ "$lp" != "-" ] && lp="$lp!"
    age=$(( $(epoch) - $(epoch "$(field "$c" touched)") ))
    printf '%-26s %-14s %-6s %-14s %s%s\n' "$sc" "$(field "$c" by)" "$live" "$lp" \
      "$(field "$c" note)" "$([ "$age" -gt "$STALE_SECS" ] && echo ' [STALE]')"
  done
}

case "${1:-list}" in
  check)   shift; cmd_check   "$@" ;;
  take)    shift; cmd_take    "$@" ;;
  touch)   shift; cmd_touch   "$@" ;;
  release) shift; cmd_release "$@" ;;
  list)    shift; cmd_list    "${1:-}" ;;
  mine)    shift; cmd_list    "${1:-}" | awk -v w="$WHO" 'NR==1||$2==w' ;;
  owner)   shift; field "$(read_claim "${1:?scope}")" by ;;
  *) sed -n '2,20p' "$0"; exit 2 ;;
esac
