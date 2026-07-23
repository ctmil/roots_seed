# 🌳 roots_seed

> **Moldeo Roots Seed** — Agentic Persistent Memory.
> A template + toolkit for giving AI agents and human developers a durable, structured memory that lives *with the code* — and turning a set of repos into a **living, observable ecosystem** you can supervise as it evolves.

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

> **Language:** the spec is **canonical in English**; each deployment keeps its own working language. See **[Language & glossary](#language--glossary-i18n)** below.

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

Three **primitives** carry across every domain (code, design, narrative): **`vendor`** (authorship), **`relations[]`** (a directed dependency/relationship graph), and **`branch`** (a fork with `stage`/`merged_into`/`created_by: human|AI`).

See **[`roots_seed.md` → Forest Model](roots_seed.md)** for the full schema (`forest.json`, relations DAG, vendor profiles).

---

## Working modes

A `.roots/` adapts to what it documents. The mode is chosen once on bootstrap and persisted in `_meta.json`:

| Mode | When | Layout |
|---|---|---|
| **Flat** (default) | one repo, one project | `.roots/` directly |
| **Source** | a multi-module source repo | `.roots/{module}/` |
| **Client branch** | a client branch that embeds sources | `.roots/{context}.{project}/` + `sources/` + `_sources.json` |
| **Workspace** | a `.roots/` that coordinates N repos (the Forest) | root + `forest.json` |
| **+ domain pack** | a domain overlay (e.g. `narrative`) on any of the above | extra domain folders |

The namespaced modes (Source / Client branch) share the multi-source machinery — embedded sources, a **precedence cascade** (client > embedded > original), a **conflict namespace**, and semi-automatic **discovery promotion** back to the source. A **migration** can temporarily fork a flat repo into namespaced and collapse back. Detail: **[`roots_seed.md` → Working modes](roots_seed.md)**.

---

## A living ecosystem (Odoo platforms & community)

`roots_seed` is built for **maintaining platforms as suites of Odoo module extensions** — a core module plus extension modules that depend on shared platforms (OCAPI, OCA, Odoo core). These are modeled as **Groves** related by **dependency edges**, never by nesting (`meli_oerp_multiple` *is part of* the `meli` Grove and *depends on* `odoo_connector_api` — two different axes).

What makes it an **ecosystem and not a pile of drifting forks** is that the source ↔ deployment flow is **bidirectional**:

- a deployment (a client branch) **embeds** the `.roots/` of every source it consumes — carrying that source's docs, fixes, patterns and decisions with it;
- a useful discovery made downstream (a fix, a reusable pattern, an architectural decision) is **promoted back** to the original source — semi-automatically, with the human deciding what graduates;
- the public **upstream** (`ctmil/roots_seed`) is checked before processing, and generic improvements can be contributed back the same way.

So **community and per-client contributions don't drift away — they flow into the sources and back out**, keeping the whole thing a living, self-healing ecosystem. (And the **language-lock** guarantees this never costs you noise: updating the shared seed never rewrites the memory a deployment already wrote.)

---

## Observable

The Forest is meant to be **watched as it evolves**. The bundled **[`forest-dashboard`](tools/forest-dashboard/)** is an internal control panel — in the browser, run **locally or on a remote server over SSH** — that scans `git` + every `.roots/` and surfaces the live state of the ecosystem: **Groves → Trees → Branches**, the `relations` dependency graph, `vendor`s, and the `collective/` lineage.

```bash
python3 tools/forest-dashboard/serve.py --root .   # → http://127.0.0.1:8787/
```

Its collector emits a **portable JSON contract** (`state.json`) — the *same shape* an Odoo backend can produce from its own models — so the panel runs identically off a local workspace or off a deployed instance, and the supervision layer isn't tied to any one IDE or tool. Detail: **[`tools/forest-dashboard/`](tools/forest-dashboard/)**.

---

## Language & glossary (i18n)

The **canonical seed is written in English** — a single source that evolves. But the language of the *memory you write into a `.roots/`* is a **per-deployment** choice, recorded in `_meta.json.lang` (`"en"` default · `"es"` · `"fr"` · …). Code and technical identifiers stay English regardless.

> **No-noise rule:** updating or re-distributing the seed **never** translates or rewrites existing memory. On `on-seed-process` the agent **auto-detects** the language of an already-deployed `.roots/` and keeps it — a Spanish project stays Spanish. Switching a deployment's language is explicit and rare.

The cross-language **Forest vocabulary** lives in **[`glossary/`](glossary/)**:

| File | Role |
|---|---|
| `glossary.json` | **canonical** source of truth (English key + `es`/`fr` term + definition, `category`, `see_also`) |
| `gen.py` | generator → emits `GLOSSARY.{en,es,fr}.md` (English primary; missing translations fall back, flagged) |
| `GLOSSARY.<lang>.md` | **generated** tables — never edited by hand |

Edit `glossary.json`, run `python3 gen.py`, commit the regenerated tables. This is distinct from a project's own `docs/glossary.md` (domain terms, in that deployment's `lang`). Detail: **[`roots_seed.md` → Language & glossary (i18n)](roots_seed.md)**.

---

## Layout

```
roots_seed/
├── roots_seed.md          ← the canonical spec (normative)
├── manual.md              ← navigable front door (start here)
├── glossary/              ← multilingual Forest vocabulary (glossary.json → GLOSSARY.{en,es,fr}.md)
├── recipes/               ← applied patterns per domain (odoo / design / narrative / tokens)
├── scripts/               ← mount & operate the Forest (install-macos, setup-module, setupbranch,
│                            sync-agents-skills, dashboard)
├── skills/                ← shared, well-designed strategies (roots-refresh, allowlist-sync,
│                            Odoo module merging, md→PDF)
├── agents/                ← base subagent library + the domain-keeper template (import on demand)
├── tools/
│   └── forest-dashboard/   ← browsable viewer that reads the .roots
└── .roots/                ← this repo's own memory (dogfooding)
```

## Get started on macOS

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/ctmil/roots_seed/main/scripts/install-macos.sh)"
```

Installs the terminal toolchain (Homebrew, GNU coreutils/sed/awk, bash 5, git, jq, ripgrep, gh…),
Claude Code, and a ready workspace with its `.roots/` memory. `--check` diagnoses an existing setup;
`--desktop` also installs the Claude Desktop app, where **Cowork** runs. Re-running is safe.

> Linux/WSL need no installer — clone and run `scripts/setup-module.sh`.

## License

See [`LICENSE`](LICENSE).
