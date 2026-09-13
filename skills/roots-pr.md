---
name: roots-pr
description: Take an improvement already written in your local canonical up to a PR on the public seed, splitting what generalizes from what is yours. Invoke it when the sync protocol answered 'Local > Upstream'. NOT for an idea you have not written yet (that is `roots-suggest`) and NOT for a defect report (that is `roots-issue`).
---

# roots-pr

> **Take an improvement that is already written in your local canonical all the way up to a PR** on
> the public seed — separating what generalizes from what is yours.

## When to use
When your local `roots_seed.md` (or `scripts/`, `skills/`, `agents/`, `recipes/`) has moved ahead of
the upstream and the delta contains something the community should have. Typical trigger: you bumped
your local version and the § *Sync* protocol answered **"Local > Upstream"**.

## Inputs
- The **diff** between your canonical and the upstream copy.
- For each hunk, a verdict: **generic** (goes up) or **local extension** (stays).

## Steps
1. **Fetch the upstream and diff.** Compare against the *published* file, not against your memory of
   it: `curl -s https://raw.githubusercontent.com/<upstream>/main/roots_seed.md > /tmp/up.md`
   then `diff -u /tmp/up.md roots_seed.md`.
2. **Split the diff in two, hunk by hunk.** The test is the same as in `roots-suggest`: strip the
   specifics — if nothing is left, it is a local extension. **Most first-time contributions fail
   here**, because the material most worth promoting (a battle-tested playbook, a real agent) is
   exactly the material that carries the most traces of the environment that produced it.
3. **Branch and commit only the generic half.** One branch per subject: a PR that carries three
   unrelated improvements gets reviewed at the speed of its slowest one.
4. **Scrub the whole diff, not just the prose** — `scripts/roots-upstream.sh scrub` over the patch.
   Code comments, example paths and script defaults are where the workspace leaks.
5. **Write the PR description** as the *why*: what the seed says today, what real use converged to,
   and the measurement. The diff shows the what.
6. **Push and open the PR** with whatever rung the machine has (`scripts/roots-upstream.sh check`).
   With no `gh` and no token, push the branch and hand over the compare URL:
   `https://github.com/<upstream>/compare/<branch>?expand=1`.
7. **Record it** in `.roots/journal/notes.md`: what went up, what stayed local, and why. That note is
   what keeps the next sync from re-proposing the same hunks.

## Verification
- `git diff --cached` passes the scrub.
- The branch contains **only** the generic half — no local extension slipped in.
- Your local canonical still works after the split (you did not move something you depend on).
- The PR says which upstream version it is based on.

## Notes
- ⚠️ **Publishing a repo publishes its memory.** `.roots/` is tracked wholesale: `state/`, `journal/`
  and any tracked `workbench/` leftovers go with it. Before making anything public, grep the memory
  for hostnames, client names, account ids and tokens.
- A PR the upstream declines is not wasted: it belongs in your local canonical, and the reason it
  was declined is worth a line in `journal/notes.md`.
