# 🌳 roots_seed

> **Moldeo Roots Seed** — Agentic Persistent Memory.
> A template + toolkit for giving AI agents and human developers a durable, structured memory that lives *with the code*.

```
                    &&&  & &&&&&  &
                &&& &\&|/&//&|\&& &&&
              &&\&\_\&\|//_//&/_&&&&            🌲  F O R E S T
             &_\&\&\&\|/|//_/&%&/_&&&&          the whole workspace —
              && &&\\&\|///&&/ && &&&           a living canopy of Groves
                &&& &\\\|///& &&&&              (each Grove = a product / suite)
             &&    &&&\\\|///&&    &&
                       \\\|///
                        \\|//        ←  Branches   (git branches · ramas)
                         \|/
                         \|/
                          |
                          |          ←  Tree = one repo  (mounted bare + worktrees)
                          |
      ~~~~~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~~~~~~~   soil line  ·  .roots/
                        _/|\_
                      _/ /|\ \_
                    _/  / | \  \__
                  _/   /  |  \    \_
                 /    /   |   \     \
                R  O   O   T   S    reach down into memory:
            context · journal · decisions · tasks · skills · docs
```

> Like a bonsai: a small, deliberate tree whose **roots** are the point. (Art in the [cbonsai](https://gitlab.com/jallbrit/cbonsai) spirit, after Jane Street's [*TUI renaissance*](https://blog.janestreet.com/strace-ui-bonsai-term-and-the-tui-renaissance/).)

---

## What it is

`.roots/` is a **persistent memory** folder you drop into a repo: decisions, error/fix logs, design docs, tasks, reusable skills — written for **AI agents and humans alike**, in a stable format so any tool can read and grow it. The canonical spec is **[`roots_seed.md`](roots_seed.md)** (currently **v1.14**); the navigable front door is **[`manual.md`](manual.md)**.

> **Language:** the spec is **canonical in English**, but each `.roots/` deployment writes its memory in its own language (`_meta.json.lang`) — updating the seed never rewrites existing memory. The cross-language Forest vocabulary lives in **[`glossary/`](glossary/)**. See *Language & glossary (i18n)*.

Not just for code: the same model spans software, design and narrative. See **[`recipes/`](recipes/)** — Odoo suites, a forest of design repos, narrative/game worlds, and a token-economy playbook.

It ships with a small toolkit: **`scripts/`** mount the substrate (bare + worktrees), **`skills/`** are a shared library of well-designed strategies, and **`tools/`** are apps that read the memory — first among them the **`forest-dashboard`**.

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
├── roots_seed.md          ← the canonical spec (normative)
├── manual.md              ← navigable front door (start here)
├── glossary/              ← multilingual Forest vocabulary (glossary.json → GLOSSARY.{en,es,fr}.md)
├── recipes/               ← applied patterns per domain (odoo / design / narrative / tokens)
├── scripts/               ← mount & operate the Forest (setup-module, setupbranch, dashboard)
├── skills/                ← shared, well-designed strategies (Odoo module merging, md→PDF)
├── tools/
│   └── forest-dashboard/   ← browsable viewer that reads the .roots
└── .roots/                ← this repo's own memory (dogfooding)
```

## License

See [`LICENSE`](LICENSE).
