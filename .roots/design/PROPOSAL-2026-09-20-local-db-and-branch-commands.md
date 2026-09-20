# PROPOSAL 2026-09-20 — the local index (and the branch commands that need it)

> Status: **PROPOSAL**. Nothing here is built. Two of the commands it builds on already exist and are
> tested (`roots-report.py`, `roots-seed-audit.py`); everything below is the ladder that starts there.

## The measurement that motivates it

One live forest, measured today with the two read-only commands:

| | |
|---|---:|
| Trees (repos) | **72** |
| Branches / worktrees | **626** |
| Distributed copies of the seed | **6407** |
| …byte-identical to a canonical | 5876 |
| …identical but for the distribution banner | 417 |
| …carrying their own content | **114** |
| Time for one full answer | **~60–150 s** |

That last row is the whole argument. Sixty seconds is fine for a human once a day. It is **far too
slow for an agent to consult mid-task**, so no agent consults it — each one re-derives a partial
answer from `git status` in whatever worktree it happens to be standing in, and then acts on it.

And coordination today is hand-rolled files: a claim per scope, a `.SYNCING` flag per module, an
append-only markdown bus. They work, and their limits are structural: **no queries, no transactions,
and identity is declared rather than enforced** (a claim's `by=` field is a role — several sessions
share one, so the file cannot say *who*).

## The contract, before the design (this is the part that must not bend)

The seed's premise is that memory is **plain files that live beside the code**, readable by any tool
or human. A database that becomes the source of truth breaks that, and with it the portability that
is the reason anyone adopts this.

So, three rules that outrank convenience:

1. ⛔ **The index is DERIVED and DISPOSABLE.** Delete it and nothing is lost: one command rebuilds it
   from the files. If ever a fact lives only in the database, the design has failed.
2. ⛔ **It is never a requirement.** Someone who installs the seed and wants no database keeps
   everything: rung 0 is the two commands that already exist and read the filesystem directly.
3. ⛔ **No new dependency per rung.** SQLite is in the standard library. Postgres is optional. Odoo is
   optional. A rung nobody can reach is a feature nobody has.

> This is the **capability ladder** the seed already uses for contributions (`gh` → token → prefilled
> URL), and for the same reason: the tool must degrade to what the reader actually has, **and declare
> which rung it used**. Reusing the idiom is not decoration — it is what keeps the seed coherent.

## The ladder

### Rung 0 — already here
`roots-report.py` and `roots-seed-audit.py`. They walk the filesystem and query git. They are the
thing the index persists; there is nothing to invent, only to store.

### Rung 1 — `roots-index` → SQLite (stdlib, zero install)
`.roots/state/roots.db`, gitignored. One walk fills it: `trees`, `branches`, `roots_copies`
(path, normalized hash, verdict, divergence lines), `runs` (when, by what version).

- **What it buys:** the same two commands gain `--from-db` and answer in **milliseconds**. That is
  what makes them usable *inside* a task instead of once a day.
- **The failure mode to design against first:** a stale index that answers confidently. Therefore
  every row stores the file mtime and hash, the DB stores `built_at`, **every read path prints the
  age**, and `--max-age` **refuses** rather than answering from a stale index. An index that lies is
  worse than a slow scan, because the scan is at least honest about being the filesystem.
- **The acceptance test is a number, declared up front:** if `--from-db` does not take the full
  report under **one second**, rung 1 is not worth its complexity and gets dropped.

### Rung 2 — `claims` and `comms` as transactions (still SQLite, still local)
Move the coordination primitives into tables: a claim becomes an atomic transaction instead of a
file plus a hand-rolled staleness heuristic, and the message bus becomes a **queryable inbox**
instead of an append-only log that has to be pushed into an agent's face to get read.

- **Write-through, not migration.** The markdown log stays the human-readable record; the table is
  the index over it. One writer path (`roots-claim`, `roots-msg`), never hand edits, or you get two
  sources of truth — which is rule 1 violated by a different door.

### Rung 3 — Postgres, and only now credentials
The moment there is more than one machine, identity stops being declarable and has to be enforced:
a role per agent, so *who wrote this* is a fact rather than a convention. Same schema as rung 1 —
that is the point of defining it at rung 1.

### Rung 4 — the canopy: the Odoo layer
The ecosystem already has modules that read `.roots/` and map it to a backend. Pointed at the same
schema they give what no local file can: an admin UI, users and access rules, the cross-forest view,
and the deeper module-level synchronization — **shareable without handing anyone a shell.**

> **From the roots to the canopy**, and in that order. Each rung is useful alone, and every rung
> keeps working if the one above it is never built. Built top-down instead, the whole thing would
> require the canopy to get any value at all.

## The branch commands, which are what rung 0/1 is actually for

Measured: **626 branches over 72 trees**; one Tree alone holds branches with **1727 commits never
pushed** and tips **107 days** old. That is not a hygiene problem, it is work that exists on one disk.

| command | does | does NOT |
|---|---|---|
| **`roots-branches`** | per Tree: which branches are already merged into deploy (**safe to prune**), which are stale, which have no upstream. Proposes; prints the command. | delete anything on its own |
| **`roots-land`** | takes ONE branch to its deploy branch: fast-forward if possible, rebase if not, **never force**. **Refuses while `.roots/` is dirty** — commit the memory first. | touch more than the branch named |

Both encode a discipline that today lives only in prose, and the asymmetry is deliberate: **pushing
your own work branch is automatic; merging into a deploy branch is confirmed with a human.** A tool
that blurs those two is a tool that eventually lands something nobody read.

## Recommended order
1. **Rung 1**, with its one-second acceptance test and the staleness refusal. If it fails the test, stop.
2. **`roots-branches`** (read-only, proposes prunes) — it needs nothing but rung 0.
3. **Rung 2**, because the claim/bus limits are already costing coordination today.
4. **`roots-land`**, once rung 1 can tell it cheaply whether memory is dirty.
5. **Rungs 3 and 4** when a second machine or a second organization actually needs them — not before.

## What would make me wrong
If rung 1 does not clear one second, or if the index needs manual repair more than once, the honest
conclusion is that the filesystem **is** the database for a forest this size, and the right move is
to make the two existing commands faster instead of adding a layer.
