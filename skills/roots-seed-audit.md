---
name: roots-seed-audit
description: Before re-distributing a bumped seed, find out which local copies are merely STALE and which are FORKS carrying content nobody sent upstream — so the update does not delete contributions. Invoke it whenever the canonical version is bumped, before any `cp` over a `.roots/`, and when a copy's version number looks wrong. NOT for branch/merge state (that is `roots-report`).
---

# roots-seed-audit

> **`on-seed-update` reads like `cp`, and on a live forest it is not.** A deployment that used the
> seed for months may have **written into** its local copy — a convention it invented, a hook it
> wrote, a section it needed. Those are contributions, and a blind copy deletes them in silence.

## Run it

```bash
scripts/roots-seed-audit.py --forest .                  # the whole forest
scripts/roots-seed-audit.py --exclude vendor            # skip a subtree (whole path components)
scripts/roots-seed-audit.py --detail <tree>             # every non-clean file of that Tree
```

Read-only. It hashes each copy — **normalized**, with the distribution banner stripped — against
every historical version of the canonical in git history.

## The four verdicts

| verdict | meaning | what to do |
|---|---|---|
| **FIEL** | byte-identical to some historical canonical | update is **lossless**: copy away |
| **BANNER** | identical except the distribution banner | safe; re-paste the banner after copying |
| **DIVERGE** *(n lines)* | carries its own content | **send it UP first** (`roots-suggest` / `roots-pr`), then bring the new canonical down |
| **ORPHAN** | declares a version the canonical never had | predates this canonical, or came from another lineage — a human looks |

## Two lessons this tool has baked in, because each one cost a wrong answer first

1. **No depth limit.** A walk capped at four levels deep counted 617 copies where there were
   **6406** — and the small number made the job look like something you could do by hand.
2. **A binary fork/no-fork verdict is worse than none.** In one measured forest, 185 of the flagged
   "forks" differed **only by a 5-line HTML banner the distributor itself pastes on top**. A tool
   that sends a human to review 185 healthy files **buries the handful that actually matter.** Hence:
   normalize the banner away, and report the **magnitude**, never merely the existence, of a
   difference.

## Verification
- Run it twice with different `--exclude` values and compare the totals. If a Tree **disappears**,
  your exclusion matched more than you meant: exclusions are matched on whole path components here
  precisely because a substring match once dropped 4674 copies of a Tree whose name merely
  *contained* the excluded word — and the total still looked plausible.
- **If your sweep reports a problem in something already measured as healthy, suspect the sweep.**

## Notes
- The percentage that updates mechanically is the useful headline; the count that needs a human is
  the actual work. In the measured forest it was 98% / ~8 blocks.
- Client or downstream deployments living under the same roof are usually **out of scope** for a
  re-distribution: they are someone else's memory. Decide that explicitly rather than by omission.
