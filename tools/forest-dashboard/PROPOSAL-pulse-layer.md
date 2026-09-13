# Proposal — the *pulse* layer: the dashboard sees the memory, not the life

> Status: **proposal, nothing implemented**. Written 13 Sep 2026 against the current collector
> (599 lines) so the discussion is about *what to add*, not about what it already does.

## What it does today (measured, not remembered)

`collect.py` emits `state.json` with: `journal` (changes), `tasks` (`- [ ]` counts), `docs`,
`skills`/`hooks`/`debug`, `collective`, per-Tree `git` (`branch`, `ahead`, `behind`, `dirty`),
the Forest axes (`grove`, `vendor`, `kind`, `org`), `relations[]`, and aggregate `metrics`.

That is a complete and honest picture of **the memory**: what was written, and what is pending.

## What it cannot show

Everything in that list is a **file on disk**. None of it answers the question somebody actually
opens the dashboard with:

> **Who is working on what right now, and what has stopped moving?**

Since 1.15–1.19 the Forest grew a whole layer of *live* state that the collector does not read:

| Live state | Where it lives | The question it answers |
|---|---|---|
| **Claims** | one file per scope (`<scope>.claim`) | who owns this front — and is that session **alive**? |
| **Loops** | `loop=<name>@<interval>` inside the claim | does this front **get looked at again by itself**, and how often? |
| **Bus** | `state/comms.md` | what was said to whom and is **still open** |
| **Leaves** | `workbench/leaves/` + the Forest floor | how much evidence is lying around **undigested** |
| **Plans** | `tasks/PLAN-<date>-<slug>.md` | the real unit of work since 1.17 — a `- [ ]` count cannot see it |

## The idea that makes it worth building

A dashboard that lists *"most recently modified first"* shows **activity**. It cannot show
**anomaly** — and those are not the same thing. A front that used to beat every 20 minutes and has
been silent for 60 looks, on today's screen, exactly like a front that was never busy: a bit further
down the list. The information is there and it is **invisible, because nothing compares a front
against itself**.

> **A gap is judged against the front's OWN cadence, never against a global threshold.**

This is the single most valuable thing the pulse layer adds. A fixed staleness threshold (say 8 h) is
useless in both directions: it fires 24 times too late for a 20-minute loop, and cries wolf on a
front that legitimately moves once a day. The cadence has to be *derived per front* from its own
heartbeat series — and the deviation, not the age, is what gets surfaced.

Two corollaries, both learned the expensive way:

- **Stale ≠ abandoned.** A claim with no recent heartbeat whose **session is still alive** means
  *someone is working and did not check in* — surfacing that as "free to take" is how two sessions
  end up answering the same thing. Liveness must be a **verifiable fact** (does the session's socket
  exist?), never an inference from elapsed time.
- **A detector must detect itself first.** Any liveness probe has to show **the session running the
  probe** as alive. A wrong probe path once reported *16 of 16 dead* — including its own caller —
  which reads as "16 abandoned fronts" and invites stealing work from people who are mid-task.
  ⇒ ship a **self-check**: if the collector cannot see itself, it reports `unknown`, never `dead`.

## Proposed contract (additive — the Odoo port must not break)

The 3-layer architecture is the asset here: adding a **top-level `pulse` key** leaves every existing
consumer untouched, and gives the eventual backend port one clear thing to produce.

```jsonc
"pulse": {
  "generated_at": "…",
  "claims": [{
    "scope": "…", "owner": "…", "note": "…",
    "taken_at": "…", "touched_at": "…",
    "session": {"id": "…", "alive": true, "probe": "socket|unknown"},
    "loop": {"name": "…", "interval_s": 900},
    "cadence": {"median_s": 1180, "gap_s": 3600, "ratio": 3.05},   // ratio = gap / own median
    "flag": "ok | quiet | silent | orphan"                          // see below
  }],
  "bus":    {"open": 12, "oldest_s": 950400, "by_addressee": {"…": 4}},
  "leaves": {"floor_files": 0, "floor_bytes": 0, "piles": 7, "oldest_pile_days": 31},
  "plans":  [{"path": "…", "title": "…", "checked": 6, "total": 11, "mtime": "…"}]
}
```

**The four flags** (the whole point of the layer):

| Flag | Condition | Reading |
|---|---|---|
| `ok` | beating within its own cadence | nothing to see |
| `quiet` | `ratio` ≥ 2 and session **alive** | working, not checking in — **do not touch** |
| `silent` | `ratio` ≥ 2 and session **dead** | free to take, with no guilt |
| `orphan` | no claim, but the front moved recently | someone is working **without a claim** |

## What to build, in order

1. **Collector** — `pulse` for claims + liveness self-check. Smallest piece, biggest payoff.
2. **View** — one strip at the top: *N fronts · M quiet · K silent*, each row showing its own cadence
   (`every ~20m, last beat 1h ago`) rather than a raw timestamp.
3. **Bus + leaves counters** — cheap, and they turn two invisible piles into two numbers.
4. **Plans** — read the `PLAN-*.md` headers and show progress per front instead of a global `- [ ]` count.

## Open questions (decide before coding)

- **Where do claims live in a generic deployment?** This deployment keeps them outside git (runtime
  state, no merge conflicts). The collector should take the path as config, defaulting to
  `.claims/` under the workspace root, and **degrade silently** when the folder does not exist —
  most users of the seed will never have one, and a dashboard that shows an error for an unused
  feature is worse than one that shows nothing.
- **Liveness probing is OS-specific.** Keep it behind one function with a declared `probe` field, so
  a deployment that cannot probe reports `unknown` instead of guessing.
- **Does `pulse` belong in `collect.py` or in a sibling collector?** Arguments for splitting: the
  memory scan is slow and cacheable (TTL 15 s), the pulse is fast and wants a shorter TTL.
