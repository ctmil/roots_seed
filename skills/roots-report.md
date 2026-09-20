---
name: roots-report
description: Read the state of a whole roots workspace at once — every Tree x every Branch — and get the order in which to land things, ranked by what can still be LOST rather than by what is biggest. Invoke it when arriving at a forest you have not seen today, before a batch, or when you need to know which branches are rotting. NOT for a single repo (that is `git status`) and NOT for the distributed copies of the seed (that is `roots-seed-audit`).
---

# roots-report

> **`git status` answers for one worktree. A forest is N Trees x M Branches**, and the thing a
> session needs on arrival is the opposite question: *where is work that can still be lost, and in
> what order do I land it?* Nobody holds that in their head, so it is held nowhere — and branches rot
> until the merge is expensive.

## Run it

```bash
scripts/roots-report.py --forest .            # the whole forest
scripts/roots-report.py --repo <tree>         # one Tree, all its branches
scripts/roots-report.py --top 15              # only what is urgent
scripts/roots-report.py --json                # for another tool
```

Read-only: only `git` queries, no fetch, no commit, no merge, no push.

## The three buckets, and why they are not equally urgent

A dirty worktree is not one fact but three, and the seed's own contracts are what separate them:

| bucket | what it is | why it ranks where it does |
|---|---|---|
| **`.roots/` uncommitted** (excluding `workbench/`) | **memory** at risk | The rule the whole seed rests on: *what is not written down before being done is not recoverable.* Memory that exists on one disk is one disk away from being re-derived from nobody's recollection. **Ranks first, always.** |
| **code/docs uncommitted** | work at risk | Usually reproducible by the same head that wrote it. Real, but recoverable. |
| **`.roots/workbench/` uncommitted** | the **local bench** | Weight **zero**. The spec puts this folder entirely outside git, `leaves/` included — it is *designed* to be thrown away. Counting it as memory is not a rounding error: on the first forest this ran against, the #1 row scored 507 on "42 uncommitted memory files" and **43 of those 45 were bench**. The real exposure was **two files**. A ranking is only worth acting on if its #1 is really #1. |

> And a **separate** finding, listed on its own: `workbench/` files that are **tracked**. That is the
> pre-1.19 contract still live, and it is precisely what breaks in silence when the seed is updated —
> the new spec says the folder is not versioned, and nothing raises an error when it is.

## Two numbers, never one

`LOSS` and `fric` are **not comparable, so they are never summed** — and the ranking is lexicographic:
anything that can be **lost** outranks everything that merely gets **more expensive**.

| | is | examples |
|---|---|---|
| **LOSS** | can this disappear? | uncommitted work · commits that are on no remote |
| **fric** | is this getting costlier? | divergence from deploy · age of the tip · `workbench/` still versioned |

> Summed into a single score, friction won: six branches whose tips were **6 to 9 years old**, all
> committed and all pushed — therefore at zero risk of loss — outranked a row holding an uncommitted
> memory file. **An old landed branch cannot be lost; it only costs more to merge.** Two numbers keep
> that distinction visible instead of averaging it away.

## How to read the ranking

Both numbers are **relative** — they order *this* forest today, they are not grades. So:

- **Every row shows WHY it scored**, and **every row is listed**, not only the top one. A ranking
  whose reasoning is hidden gets argued with; one that shows its terms gets corrected.
- **The weights are printed on the first line.** If they are wrong for your forest, say so — do not
  quietly re-rank in your head and act on a different order than the one on screen.
- `behind` is computed against the **local** deploy branch, because fetching is a network action and
  this tool takes none. A stale local deploy branch makes `behind` **optimistic**. If that number is
  going to drive a decision, fetch first, and look at the fetch's exit code before believing it.

## It works on an ordinary repo too, and that took fixing
Simulated on a throwaway forest of plain `git init` repos — which is what most installs look like —
three assumptions broke, all of them silently:

- **`git worktree list` returns exactly one entry** in an ordinary repo, so the tool showed **one
  branch per Tree** while claiming to show every Tree x Branch. Branches with no worktree are now
  scanned for divergence and marked *"rama sin worktree"* (they cannot be dirty — nothing is checked
  out). On the real forest this took the count from **626 to 1109**: nearly half the branches were
  invisible.
- **A repo with no remote at all** counted every commit as "unpushed", so the whole *land it* block
  came out empty and the advice was *push these* — which you cannot do. That case is the **higher**
  risk (nothing is backed up anywhere) and now says so in its own words.
- Run it from **inside a standalone clone of the seed** and the companion audit reported *"0 copies,
  0% need a human"*, because the canonical and the forest were the same directory. A confident empty
  answer reads as good news; it now says the empty result **is a finding**.

## Verification
- The Tree count and branch count match what you expect; a Tree with zero branches listed means it
  was not detected as a repo (or as a bare+worktrees container) — not that it is clean.
- Spot-check one branch by hand (`git rev-list --left-right --count <deploy>...<branch>`). A report
  that says *up to date* when it is not is worse than no report: that exact bug shipped once here,
  from splitting a branch name like `feature/x` on the last `/`.

## Notes
- Pair it with **`roots-seed-audit.py`**, which answers the fourth plane this tool deliberately does
  not touch: the **distributed copies of the seed** across those same `.roots/`.
- Acting on the output (landing a branch, pushing) stays a decision, not a side effect. The work
  branch is yours to push; **the merge into a deploy branch is confirmed with a human.**
