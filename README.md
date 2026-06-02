# 🌳 roots_seed

> **Moldeo Roots Seed** — Agentic Persistent Memory.
> A template + toolkit for giving AI agents and human developers a durable, structured memory that lives *with the code*.

```
                              .-~~~~~-.
                       .-~ ~ -(         )~ -.
                     /                       \         F O R E S T
                    |      G  R  O  V  E  S    |        the whole workspace —
                     \   products  ·  suites  /        every repo, one canopy
                       `- . _________ . -~`
                            | | | | |
                            | | | | |        ← Branches  (git branches / ramas)
                            | | | | |
                            |       |
                            |  TREE |          Tree = one repo
                            |  one  |          (mounted bare + worktrees)
                            |  repo |
         ___________________|       |___________________
        (  ~ ~ ~ ~ ~  soil line  ·  .roots/  ~ ~ ~ ~ ~  )
         `----.____         |       |         ____.----'
                   `--.___  /|     |\  ___.--`
                      .-`-./ |     | \.-`-.
                   .-`     / |     | \     `-.
                .-`       /  |     |  \       `-.
                R  O  O  T  S    reach down into memory:
          context · journal · decisions · tasks · skills · docs
```

---

## What it is

`.roots/` is a **persistent memory** folder you drop into a repo: decisions, error/fix logs, design docs, tasks, reusable skills — written for **AI agents and humans alike**, in a stable format so any tool can read and grow it. The canonical spec is **[`roots_seed.md`](roots_seed.md)** (currently **v1.9**).

It ships with a small toolkit: **`scripts/`** mount the substrate (bare + worktrees), **`skills/`** are a shared library of well-designed strategies, and **`tools/`** are apps that read the memory — first among them the **`fleet-dashboard`**.

## The Forest vocabulary

Memory grows from roots, so the whole model does too. When `.roots/` coordinates **many repos at once** (working_mode `workspace`), it speaks this language:

| Term | Is | Example |
|---|---|---|
| 🌱 **Roots** (`.roots`) | the memory / knowledge layer | `context.md`, `decisions.md`, `journal/` |
| 🌲 **Forest** | the whole workspace — every repo, coordinated | the folder holding all repos |
| 🌳 **Grove** | a **product / suite**: a cluster of Trees | *Meli*, *OCAPI*, *GeoEcon* |
| 🪵 **Tree** | a **repo** (mounted bare + worktrees) | `meli_oerp`, `geoecon_map` |
| 🌿 **Branch** | a git branch / worktree of a Tree | `17.0`, `mapdev` |

Each Tree carries orthogonal tags — `grove` (what it *is*), `vendor` (who *makes* it), `kind` (its nature), `org` (where it *lives*) — and dependencies between Trees/Groves are **edges in a graph**, never nesting. The golden rule:

> **`grove` = what it is · edge = what it uses · tag = what it also belongs to.**

See **[`roots_seed.md` → Forest Model](roots_seed.md)** for the full schema (`forest.json`, relations DAG, vendor profiles).

---

## Layout

```
roots_seed/
├── roots_seed.md          ← the canonical spec (read this)
├── scripts/               ← mount & operate the Forest (setup-module, setupbranch, dashboard)
├── skills/                ← shared, well-designed strategies (Odoo module merging, md→PDF)
├── tools/
│   └── fleet-dashboard/   ← browsable viewer that reads the .roots
└── .roots/                ← this repo's own memory (dogfooding)
```

## License

See [`LICENSE`](LICENSE).
