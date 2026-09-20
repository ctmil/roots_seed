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

## The two planes, and why they are not equally urgent

A dirty worktree is really two different facts, and the seed's premise (memory lives beside the code)
is what separates them:

| plane | what it is | why it ranks where it does |
|---|---|---|
| **`.roots/` uncommitted** | **memory** at risk | The rule the whole seed rests on: *what is not written down before being done is not recoverable.* Memory that exists on one disk is one disk away from being re-derived from nobody's recollection. **Ranks first, always.** |
| **code/docs uncommitted** | work at risk | Usually reproducible by the same head that wrote it. Real, but recoverable. |

## How to read the ranking

The score is **relative** — it orders *this* forest today, it is not a grade. So:

- **Every row shows WHY it scored**, and **every row is listed**, not only the top one. A ranking
  whose reasoning is hidden gets argued with; one that shows its terms gets corrected.
- **The weights are printed on the first line.** If they are wrong for your forest, say so — do not
  quietly re-rank in your head and act on a different order than the one on screen.
- `behind` is computed against the **local** deploy branch, because fetching is a network action and
  this tool takes none. A stale local deploy branch makes `behind` **optimistic**. If that number is
  going to drive a decision, fetch first, and look at the fetch's exit code before believing it.

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
