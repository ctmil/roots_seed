#!/usr/bin/env bash
# roots-upstream.sh — take a contribution UP to the public seed, with whatever this machine has.
#
# The seed already documented WHAT to contribute (§ Contributing to the upstream) and WHAT to scrub
# (§ Public hygiene). What it never had was a way to DO it, so it did not happen. This is that.
#
#   roots-upstream.sh check                      # what can this machine actually do?
#   roots-upstream.sh scrub <file>               # mechanical secret/specifics check (warns, never blocks)
#   roots-upstream.sh issue <title> <body.md> [label]   # open an issue, degrading gracefully
#   roots-upstream.sh url   <title> <body.md>    # print the prefilled URL (never publishes — but DOES scrub:
#                                                #   the body travels in the query string, so handing the
#                                                #   link over is already rendering it outward)
#
# THE CAPABILITY LADDER — always in this order, and always DECLARED in the output:
#   1. `gh` CLI            → publishes directly
#   2. $GITHUB_TOKEN       → publishes via the REST API
#   3. prefilled issue URL → works ALWAYS, with no credentials: a human presses the button
#
# Rule that outranks convenience: **publishing is an outward action.** This script prints what it is
# about to send and requires --yes before rung 1 or 2, and it never claims to have published when it
# only printed a URL.
#
# EXIT CODES — because "it printed a URL" and "it published" must not look alike to a caller:
#   0  published for real (rung 1 or 2)
#   3  not sent: it can publish, but --yes was not given
#   4  NOT PUBLISHED: no capability — a prefilled URL was handed over instead
#   5  refused: the scrub flagged the body and --scrubbed was not given (ALL three rungs, url included)
# A human reads the sentence; a script reads the code. Both must reach the same conclusion.
set -uo pipefail

UPSTREAM="${ROOTS_UPSTREAM:-ctmil/roots_seed}"
YES=0; SCRUBBED=0
for a in "$@"; do
  [ "$a" = "--yes" ] && YES=1
  [ "$a" = "--scrubbed" ] && SCRUBBED=1
done

have_gh()    { command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; }
have_token() { [ -n "${GITHUB_TOKEN:-${GH_TOKEN:-}}" ]; }

urlencode() { python3 -c 'import sys,urllib.parse;sys.stdout.write(urllib.parse.quote(sys.stdin.read(),safe=""))'; }

cmd_check() {
  echo "upstream: $UPSTREAM"
  if have_gh;    then echo "  [1] gh CLI ............ YES  -> can publish directly";
                 else echo "  [1] gh CLI ............ no"; fi
  if have_token; then echo "  [2] GITHUB_TOKEN ...... YES  -> can publish via API";
                 else echo "  [2] GITHUB_TOKEN ...... no"; fi
  echo "  [3] prefilled URL ..... YES  -> always available, no credentials"
  if have_gh || have_token; then return 0; fi
  echo
  echo "This machine cannot publish by itself: it will hand you a link. That is not a failure,"
  echo "it is the ladder working — do not report an issue as 'opened' when only a URL was printed."
}

# Mechanical check. WARNS, never blocks — a gate that blocks gets bypassed.
cmd_scrub() {
  local f="${1:?file}"
  # Absolute paths: match ANY plausible workspace root, not just the two everyone thinks of.
  # Found by using this script on itself — the pattern covered /home and /Users and would have
  # missed the workspace that wrote it, which lived under /media. A scrub with a hole in the
  # exact place you work is worse than none: it returns "clean" and you believe it.
  local pat='([a-z0-9-]+\.)+(com|net|org|ar|mx|io)|[0-9]{1,3}(\.[0-9]{1,3}){3}|BEGIN [A-Z ]*PRIVATE KEY|secret_key|api[_-]?key|passw|/(home|Users|media|mnt|srv|opt|data|workspace|repos|projects)/[A-Za-z0-9_.-]|@[a-z0-9.-]+\.[a-z]{2,}'
  echo "scrub: $f"
  if grep -nEi "$pat" "$f"; then
    echo
    echo "^ REVIEW before publishing. Replace with the role, not the name:"
    echo "  client/employer -> 'the client' · host/domain/IP -> 'the production host'"
    echo "  ids, phones, emails -> drop or <account-id> · absolute paths -> repo-relative"
    echo "  credentials: never the contents AND never the exact location"
    echo
    echo "Generalizing is not only redaction: if removing the specifics leaves nothing,"
    echo "the piece was never generic and belongs in your local canonical."
    return 1
  fi
  echo "  clean (mechanically — a human still reads it)"
}

# The gate, in ONE place. It used to live inside the branch that can publish, so a machine with
# neither `gh` nor a token — the DEFAULT state of anyone who clones this — got handed a prefilled
# URL with the client name, the host, the IP and the credential file inside the query string, and
# that URL was the last line printed: the one you copy. Rung 3 IS a publishing path; it is the one
# everybody actually uses. The gate guarded the door almost nobody walks through.
gate_scrub() {
  local f="${1:?file}"
  cmd_scrub "$f" && return 0
  [ "$SCRUBBED" -eq 1 ] && { echo; echo "(--scrubbed given: hits above accepted as false positives)"; return 0; }
  echo
  echo "REFUSED: the scrub flagged the body above, so nothing was printed — no URL either."
  echo "A prefilled URL carries the body in the query string: handing it over IS publishing it."
  echo "Fix the text, or re-run with --scrubbed if every hit is a false positive you have read."
  return 5
}

cmd_url() {
  local title="${1:?title}" body_file="${2:?body.md}" body enc_t enc_b
  # SCRUB_DONE=1 when called from cmd_issue, which already gated.
  [ "${SCRUB_DONE:-0}" -eq 1 ] || gate_scrub "$body_file" || return 5
  body="$(cat "$body_file")"
  enc_t="$(printf '%s' "$title" | urlencode)"
  enc_b="$(printf '%s' "$body"  | urlencode)"
  if [ "${#enc_b}" -gt 6000 ]; then
    echo "WARNING: the body is long (${#enc_b} encoded chars). Browsers/GitHub truncate long URLs." >&2
    echo "         Open the URL, then PASTE the body from $body_file instead of trusting the prefill." >&2
  fi
  echo "https://github.com/$UPSTREAM/issues/new?title=$enc_t&body=$enc_b"
}

cmd_issue() {
  local title="${1:?title}" body_file="${2:?body.md}" label="${3:-}"
  # Hygiene WARNS elsewhere; on ANY path that renders the body outward it BLOCKS — and that
  # includes rung 3. Leaf-fall can be re-run; a public issue cannot be unpublished, and a
  # credential is leaked the moment it renders, URL bar included.
  gate_scrub "$body_file" || return 5
  echo
  echo "--- about to send to $UPSTREAM ---"; echo "TITLE: $title"; sed 's/^/  /' "$body_file"; echo "---"
  if have_gh || have_token; then
    if [ "$YES" -ne 1 ]; then
      echo; echo "Not sent: publishing is an outward action. Re-run with --yes to publish,"
      echo "or use '$0 url \"$title\" $body_file' to hand a link to a human instead."
      return 3
    fi
    if have_gh; then
      # shellcheck disable=SC2086
      gh issue create -R "$UPSTREAM" -t "$title" -F "$body_file" ${label:+--label "$label"}
    else
      python3 - "$UPSTREAM" "$title" "$body_file" "$label" <<'PY'
import json,os,sys,urllib.request
repo,title,bf,label=sys.argv[1:5]
data={"title":title,"body":open(bf,encoding="utf-8").read()}
if label: data["labels"]=[label]
req=urllib.request.Request(f"https://api.github.com/repos/{repo}/issues",
    data=json.dumps(data).encode(),
    headers={"Authorization":"Bearer "+(os.environ.get("GITHUB_TOKEN") or os.environ["GH_TOKEN"]),
             "Accept":"application/vnd.github+json","User-Agent":"roots-upstream"})
print(json.load(urllib.request.urlopen(req))["html_url"])
PY
    fi
  else
    echo
    echo "No publishing capability on this machine. NOT opened — here is the link, a human presses it:"
    SCRUB_DONE=1 cmd_url "$title" "$body_file"
    return 4
  fi
}

case "${1:-check}" in
  check) cmd_check ;;
  scrub) cmd_scrub "${2:-}" ;;
  url)   cmd_url   "${2:-}" "${3:-}" ;;
  issue) cmd_issue "${2:-}" "${3:-}" "${4:-}" ;;
  *) sed -n '2,20p' "$0"; exit 2 ;;
esac
