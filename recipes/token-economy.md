# Recipe — Token economy, benchmarking and techniques per model

> How `.roots` saves tokens: **read by layers, not everything each turn**. Plus a legible formula, an internal benchmark, and a repo of techniques to optimize the use of different AI models. A layer cross-cutting to all recipes.

## The mechanism: the layer ladder

The saving is NOT compressing text: it is **not reloading the whole corpus each turn**. `.roots` is designed in layers; the agent climbs a layer only when needed.

```
L0  cheap index      MEMORY.md · context.md · forest.json · _meta.json     (almost always)
L1  active slice     tasks/todo.md + _meta.current_feature + 1–2 docs       (the task)
L2  domain doc       on-demand drill: ONE file from docs/ or worldbible/     (when needed)
L3  full corpus      read everything / many files                           (rare, explicit)
```

**Rule:** stay at the lowest layer that solves the task. The `hooks/` (session-start, on-topic-shift) and the `current_feature` of `_meta.json` exist precisely to load the right slice without sweeping everything.

## Formula (two legible numbers)

- **CER — Context Efficiency Ratio** = `useful_tokens / loaded_tokens`
  *(of what I loaded, how much I actually used. Low CER = you read too much.)*
- **FS — Frugality Score** = `tokens_if_I_read_everything / loaded_tokens`
  *("I read 1/N of the corpus". FS 10 = you used 1/10 of the total available.)*

**Budget tiers per task** (loaded tokens, indicative):

| Tier | Budget | Typical layers | Example |
|---|---|---|---|
| trivial | ≤ 5k | L0 | "what version is the seed?" |
| normal | ≤ 20k | L0 + L1 | implement a scoped fix |
| deep | ≤ 80k | L0 + L1 + L2 | new feature, refactor of a subsystem |
| full | no cap | L3 | audit / massive migration (justify it) |

You pick a tier → you stay at the lowest layer that meets it. If you exceed the tier, log it (don't truncate silently).

## Internal benchmark — `journal/benchmarks.md`

One row per relevant session/task:

| date | model | task | tokens_in | tokens_out | layers | FS | quality (1–5) | note |
|---|---|---|---|---|---|---|---|---|
| 2026-06-02 | opus-4.8 | ORM fix | 18k | 3k | L0+L1 | 8 | 5 | context+1 doc was enough |
| 2026-06-02 | haiku-4.5 | classify modules | 6k | 1k | L0 | 14 | 4 | index was enough |

Over time it becomes a **dataset of "what worked"**: which model + which layers + which tier performed best per task type.

## Techniques repo per model — `skills/model-techniques.md`

Distilled from the benchmark. Per model (Opus / Sonnet / Haiku and other vendors):
- **When to use which:** Haiku for cheap classify/extract (L0); Sonnet for medium implementation; Opus for design/deep reasoning.
- **Prompt patterns** that perform with each one.
- **Cache:** the prompt cache TTL (~5 min) — don't break the cached prefix with unnecessary reads; group work within the window.
- **Delegation:** when to hand off to subagents (search/read fan-out) instead of loading everything into the main context.
- **When to climb to L3:** signals that the index is not enough.

## The improvement loop

```
measure (benchmarks.md) → distill technique (model-techniques.md) → apply (layer ladder) → measure…
```

> Same spirit as the rest of the seed: operational knowledge (here: how to spend tokens well) is **persisted and improved**, not relearned each session. Promoted to seed v1.10 because it applies to any `.roots`, not just this workspace.
