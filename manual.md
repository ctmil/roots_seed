# Roots Seed — Complete manual

> Usage manual for the `.roots` system / **Forest model**. It is the **front door**: it explains the why, the vocabulary, the modes, the registry and the recipes, and links to the spec ([`roots_seed.md`](roots_seed.md)) and the recipes ([`recipes/`](recipes/)) instead of duplicating them.

**Seed version:** 1.14 · **Vocabulary:** Roots → Forest → Grove → Tree → Branch · **Language:** English canonical, per-deployment `lang` (see §12)

---

## 1. What it is and why

`.roots/` is **persistent memory that lives with the code**. Instead of re-explaining to every agent (or every new human) what the project does, the decisions, the resolved bugs and the work in progress, all of that is written into a stable structure that **any AI tool or person can read and grow**. Designed for **AI agents and developers alike**.

Three principles:
1. **Index and point, don't duplicate** — the real memory lives where it belongs; the upper layers reference it.
2. **Self-contained** — each `.roots/` carries a copy of the seed that generated it (`roots_seed.md`), so it is reprocessable even if extracted into another repo.
3. **Tool-agnostic** — the format is Markdown + JSON; it does not depend on any specific assistant.

## 2. Forest vocabulary and the 3 primitives

When `.roots` coordinates **many repos** (working_mode `workspace`):

| Term | Is |
|---|---|
| 🌱 **Roots** (`.roots`) | the memory layer |
| 🌲 **Forest** | the whole workspace (all repos) |
| 🌳 **Grove** | a product / suite (cluster of Trees) |
| 🪵 **Tree** | a repo |
| 🌿 **Branch** | a git branch / worktree |
| 🍃 **Folio** (`folios/`) | the **leaf**: a document turned outward — published, exposed, seen |

> Roots absorb (inward, private), branches carry, **folios face the light** (outward, published).
> A folio is a *view* of a `.roots/` document, hanging from a branch; its reception (`reception.md`)
> is the only thing that enters a project from outside. See `roots_seed.md` § *Folios — the leaf*.

And **three primitives reused across every domain** (see `recipes/`):
- **vendor** — authorship: ownership of each Tree (`vendor: <slug>`) with an optional profile in `vendors/<slug>.md`.
- **`relations[]`** — directed graph `{from, to, type}`: code dependencies, design links, or narrative plot.
- **branch** — a fork with `stage`/`merged_into`/`created_by: human|AI`: git branch, design variant or script arc.

**Golden rule:** `grove` = *what it is* · edge = *what it uses* · tag (`also_groves`) = *also part of*. Dependencies are **edges**, never nesting or tags.

## 3. Structure of a `.roots/`

```
.roots/
├── _meta.json        state: working_mode, layout, seed version, current_feature
├── roots_seed.md     local copy of the seed (self-contained)
├── context.md        30s briefing (what/stack/state/conventions)
├── journal/          changelog · diary · notes · benchmarks
├── tasks/            todo · tasks (active work)
├── debug/            errors-log · fixes-log · migrations
├── design/           decisions (ADRs) · sketchbook
├── docs/             architecture · glossary · manual · commits · design-*
├── state/            where the work stands NOW · comms.md · secrets (gitignored)
├── folios/           the leaf: what faces outward (published) + reception.md
├── hooks/            session-start/end · on-error/fix/task-done/topic-shift · on-seed-*
├── skills/           prompts · workflows · patterns (+ AI techniques, character skills)
└── workbench/        user reference material
```
> Folders are created **lazily** — bootstrap writes only `_meta.json`, `context.md`, `roots_seed.md`.
Detail of each file and the populating standards: [`roots_seed.md`](roots_seed.md).

## 4. Working modes

| Mode | When | Layout |
|---|---|---|
| **Flat** (default) | one repo, one project | `.roots/` directly |
| **Source** | multi-module source repo | `.roots/{module}/` |
| **Client branch** | client branch that embeds sources | `.roots/{context}.{project}/` |
| **Workspace** | one `.roots/` coordinating N repos (the Forest) | root + `forest.json` + `<grove>/` |
| **+ domain pack** | domain overlay (e.g. `narrative`) on top of any of the above | extra domain folders |

The mode is decided when processing the seed and persisted in `_meta.json`. Detail and decision rule: [`roots_seed.md` → Working modes](roots_seed.md).

## 5. The `forest.json` registry (workspace mode)

Structured source of truth of the Forest. It carries:
- `vocabulary`, `groves[]` (id, kind, vendor), `vendors[]` (id, profile).
- `repos[]` = Trees, each with axes `grove` / `vendor` / `kind` / `org` (+ legacy `role`/`worktrees`/`upstream`).
- `relations[]` = the dependency graph.

> Compat: if you rename `fleet.json`→`forest.json`, leave `fleet.json` as a **symlink** so as not to break the `forest-dashboard` (it reads `repos[]`). Full schema: [`docs/forest-model.md`](docs/forest-model.md) (in the workspace's `.roots`).

## 6. Recipes by domain

The model is not just for Odoo. See [`recipes/`](recipes/):
1. **[Odoo suite](recipes/odoo-suite.md)** — `Grove = suite · Tree = module · relations = depends` (Meli).
2. **[Design forest](recipes/design-forest.md)** — `1 vendor (artist) > N trees > designs`; bridge `ai_context_md` ↔ `.roots` (Folio/Lab).
3. **[Narrative / game](recipes/narrative-game.md)** — sheets, lore, NPCs, arcs as branches, character skills ≡ AI skills.
4. **[Token economy](recipes/token-economy.md)** — layer ladder, CER/FS formula, benchmarking, per-model techniques.

## 7. Token economy (summary)

Read **by layers, not everything**: L0 index → L1 active slice → L2 domain doc → L3 corpus. Measure with **CER** (`useful/loaded`) and **FS** (`if_I_read_everything/loaded`), per task **tier** (trivial/normal/deep/full). Record in `journal/benchmarks.md`, distill techniques into `skills/model-techniques.md`. Detail: [`recipes/token-economy.md`](recipes/token-economy.md).

## 8. Toolkit (`scripts/` · `skills/` · `tools/`)

The `.roots` lives on top of a substrate of repos; the seed ships with tools that mount and visualize it:
- **`scripts/`** — `setup-module.sh`, `setupbranch.sh`, `dashboard.sh` (the **bare + worktrees** pattern: one `.bare` per Tree, one worktree per Branch).
- **`skills/`** — **shared** library of strategies (Odoo module merging, md→PDF reporting).
- **`tools/forest-dashboard/`** — navigable viewer that reads the `.roots` and maps them to an Odoo backend.

The `.roots/` format **does not depend** on the toolkit: any single repo uses it without it.

## 9. Lifecycle (hooks)

- **`session-start`** — read `context.md` → `forest.md`/registry → `tasks/` → `journal/`; check the seed version and git state.
- **`on-task-done`** — when closing each task, update `tasks/` + `docs/commits.md` (+ logs if applicable).
- **`on-topic-shift`** — when changing focus, re-scan `docs/` before asking for clarification (move up a layer).
- **`on-error` / `on-fix`** — record in `debug/`.
- **`on-seed-update` / `on-seed-process`** — when bumping the seed, re-distribute the local copy; when processing for the first time, detect the mode.

## 10. Seed distribution and sync

Each `.roots/` carries `roots_seed.md` (copy of the canonical one). The canonical for a workspace is `roots_seed/main/roots_seed.md`, a mirror of the upstream `github.com/ctmil/roots_seed`. When bumping the version, re-distribute (on-seed-update). **Always check the upstream** before assuming the version.

## 11. Quick start

```bash
# 1. Mount a repo as a Tree (bare + worktrees)
./setup-module.sh mi_modulo git@github.com:org/mi_modulo.git 17.0

# 2. Bootstrap the .roots (Flat mode by default)
#    copy roots_seed.md into the repo's .roots/ and let the agent process it
#    (detects mode, creates context.md/_meta.json/structure)

# 3. If you coordinate several repos: build forest.json at the workspace level
#    (groves[] + vendors[] + repos[] with grove/vendor/kind + relations[])

# 4. Visualize
./dashboard.sh
```

## 12. Language & glossary

The **canonical seed is English** (one evolving source). But every `.roots/` deployment writes its memory in **its own** working language, recorded in `_meta.json.lang` (`"en"` default, `"es"`, `"fr"`, …) — code and technical identifiers stay English regardless.

**No-noise rule:** updating or re-distributing the seed **never** translates or rewrites existing memory. On `on-seed-process` the agent **auto-detects** the language of an already-deployed `.roots/` and keeps it — a Spanish project stays Spanish. Switching a deployment's language is explicit and rare.

The cross-language **Forest vocabulary** lives in [`glossary/`](glossary/): edit `glossary.json` (English key + `es`/`fr`), run `python3 gen.py`, and the `GLOSSARY.{en,es,fr}.md` tables regenerate. This is distinct from a project's own `docs/glossary.md` (domain terms, in the deployment's `lang`). Detail: [`roots_seed.md` → Language & glossary (i18n)](roots_seed.md).

---

> This manual is the navigable index; the **normative spec** is [`roots_seed.md`](roots_seed.md) and the **per-domain detail** is in [`recipes/`](recipes/).
