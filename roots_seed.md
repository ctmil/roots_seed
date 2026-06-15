# Roots Seed - Agentic Memory Structure

> Master template for creating a development documentation and memory structure. This file defines the formatting standards, style, and population protocols.

> ⚠️ **Before using or processing this seed, ALWAYS check the latest changes of the upstream source
> [`github.com/ctmil/roots_seed`](https://github.com/ctmil/roots_seed).** This file may be a
> **distributed copy** and out of date with respect to the canonical (compare the `Version` field /
> changelog). The seed evolves — do not assume this copy is the latest. See § "Sync with the canonical upstream".

**Version:** 1.14

**Changelog:**
- **1.14** (12 June 2026) — **English becomes the canonical language of the seed** + a multilingual **glossary system** + a **language-lock**. The spec (`roots_seed.md`, `manual.md`) is now maintained in English (single evolving source). New section **Language & glossary (i18n)**: each `.roots/` deployment carries its own working language in `_meta.json.lang` (`"en"` default, `"es"`, `"fr"`, …) — **independent** of the seed's language; code/technical identifiers stay English regardless. **No-noise rule:** updating/re-distributing the seed NEVER translates or rewrites existing memory; `on-seed-process` gains step **0b** that **auto-detects** the language of an already-deployed `.roots/` and persists it (a Spanish project stays Spanish), and `on-seed-update` only refreshes the canonical `roots_seed.md` copy. New **`glossary/`** subsystem: `glossary.json` (canonical, English key + `es`/`fr` term+def + `category`/`see_also`) → `gen.py` generates `GLOSSARY.{en,es,fr}.md` tables (English primary; missing translations fall back to English, flagged). The per-module `docs/glossary.md` (domain terms, in the deployment's `lang`) is distinct from this Forest-vocabulary glossary. The `**Language**` style rows are now `lang`-driven. Does not change the `.roots/` format.
- **1.13** (08 June 2026) — New folder **`collective/`**: **permanent** memory of third-party influences/references that nourish the project (people, ideas, sites, works, organizations, books). It is the permanent counterpart of `workbench/` (ephemeral) — the difference is **permanence**; whatever in the workbench deserves to stay is **promoted** to collective. It branches inward into emergent subfolders (`code/inspiration` is not forced): for code it works as a **contrib**, for creative projects as attributed **inspiration sources**. First-class **`library/`** subfolder (annotated bibliography as a corpus + graduation to a per-book entry). Each entry carries **attribution/copyright**, **Contact** (email/phone/WhatsApp/IG) and **Media** (images/videos, local or remote) with a privacy rule. The `.roots/` as a **new writing format**: the entry is living text with a follow-up log. The **`forest-dashboard`** surfaces the collective (new **Collective** tab: families → per-project entries, with inline opening of the `.md` + **contact preview** —email/IG— **and image** per entry). Reinforcement of the directive to always check the upstream `ctmil/roots_seed`.
- **1.12** (04 June 2026) — New section **Agents and skills — importable library (on-demand)**. Two layers + base: **store** in `<repo>/.roots/{agents,skills}/` (**tracked** → versioned, evolves, copyable), **activation** in `<repo>/.claude/{agents,skills}/` (local, **not tracked** → you copy there what you want to use generally), and a cross-client **base** in `roots_seed/{agents,skills}/`. Rule: **do not preload everything** — the seed reports what exists; you import on demand. Cycle: design in the workspace's `.roots/agents/` → activate in `.claude/` and test → promote to `roots_seed/` → reference here. Forest-aware subagents by *concern* (e.g. `odoo-architect`, `bug-hunter`, `odoo-migrator`, `designer`).
- **1.11** (03 June 2026) — **`forest-dashboard`** (re-framing of the viewer with the Forest nomenclature; formerly `fleet-dashboard`). The collector reads the new axes of `forest.json` (`groves[]`/`vendors[]`/`relations[]` + `grove`/`vendor`/`kind`/`org` per Tree) and emits them in `state.json`. The view adds a **Forest map** tab (Groves → Trees → Branches with `vendor`/`kind` badges) and an **SVG graph of `relations`** (arc-diagram, edges colored by type). Rebrand: *fleet→Forest · repo→Tree · worktree→Branch*. `fleet.json` remains a symlink→`forest.json` (compat). The `state.json` contract keeps `repos[]` (Odoo port intact).
- **1.10** (02 June 2026) — **Per-domain recipes** + **full manual** + **token economy**. New folder `recipes/` with 4 applied recipes of the `.roots`/Forest model: (1) suite of Odoo extension modules (Grove=suite, Tree=module, relations=depends), (2) design forest (1 vendor-artist > N trees > designs; bridge `ai_context_md`↔`.roots`), (3) narrative/game as a **domain pack** (`working_mode: narrative`: worldbible, entries, arcs=branches, character skills ≡ AI skills), (4) token economy. Cross-cutting thesis: **3 primitives (vendor · `relations[]` · branch) are reused across N domains**. New `manual.md` (navigable front door). New section **Token economy & model benchmarking**: layer ladder L0–L3, readable **CER** formula (useful/loaded) + **FS** (if_I_read_everything/loaded) + budget tiers, internal benchmark (`journal/benchmarks.md`) and a repo of per-AI-model techniques (`skills/model-techniques.md`). Does not change the `.roots/` format.
- **1.9** (02 June 2026) — New section **Forest Model** that formalizes and promotes to canonical the `workspace` working_mode (a coordination layer above N repos, formerly a local extension). Defines the vocabulary **Roots → Forest → Grove → Tree → Branch** and a multi-axis schema: each Tree (repo) carries `grove` (primary product/suite), `also_groves` (tags of genuine co-membership), `vendor` (author/maker — **ownership** with an optional profile in `.roots/vendors/<slug>.md`), `kind` (`producto-suite`/`plataforma`/`agregador`/`external-upstream`/`seed`) and `org` (hosting). **Dependencies are modeled as edges** of a directed graph (`relations[]`: `depends-on`/`extends`/`integrates`/`relates`), NEVER as nesting or tags — golden rule: *grove = what it is · edge = what it uses · tag = also belongs to*. `forest.json` is the structured registry (rename of `fleet.json`, which remains as a symlink for compat with the `forest-dashboard`; keeps the `repos[]` array). Does not change the per-repo `.roots/` format.
- **1.8** (02 June 2026) — New section **Complementary toolkit (`scripts/` + `skills/` + `tools/`)**: systematizes that the `.roots/` memory lives on a substrate of repos and that the seed is distributed alongside tools that mount, improve and visualize it. `scripts/` (mounting/operating the fleet: `setup-module.sh`, `setupbranch.sh`, `dashboard.sh` — bare+worktrees pattern), `skills/` (a **shared** library of well-designed strategies: Odoo module merging, md→PDF reporting — distinct from the local `skills/` of each `.roots`) and `tools/` (apps; first: `forest-dashboard`, a navigable viewer that reads the `.roots` and maps to an Odoo backend). Code is **referenced**, not inlined: each element is self-contained with its README. Does not change the `.roots/` format.
- **1.7** (30 May 2026) — New **Flat mode** (simplified): `.roots/` directly at the root, no namespace, for single-source projects with few/no embedded remote sources — the common case. **Decoupling of two axes** that v1.6 conflated: the *directory layout* (`flat` vs `namespaced`) is now independent of the *context metadata* (`context_format`/`context_parsed`) — a flat repo can declare its context (e.g. Odoo 17.0, dev) in `_meta.json` without encoding it in the path (register without namespacing). New layout **decision rule**: it is defined by "do I need concurrent multi-context memory?" (embed N sources / parallel multi-version-client / migration), NOT "is it Odoo?". New **Migration mode**: a flat repo can *temporarily fork* to namespaced during a migration (e.g. `.roots/17.0/` + `.roots/19.0/` side by side) and *collapse back to flat* on the new version. `_meta.json` extended with `layout`. **Flat is the bootstrap default** — the mode question is only triggered by signals of multi-source/multi-client. Initialization script bumped to v1.7.
- **1.6** (10 May 2026) — Working modes reframed as a hybrid multi-source model. New **Context Format Registry** with per-domain structured context (Odoo as the first format: `{major}.{minor}.{infra}.{project}`). New **embedded sources** system: the client copies the `.roots/` of each source into `sources/`, with `_sources.json` as the linking manifest. **Precedence cascade** formalized: root client > embedded source > original source. **Conflict namespace** with the `source.skill_name` pattern and client overrides. **Semi-automatic promotion** of client discoveries to the original source. New section **Tool Compatibility** with a tool-agnostic philosophy, 5 main tools as a reference and merging strategies. `_meta.json` extended with `context_format`, `context_parsed`, `sources`. Initialization script updated to v1.6.
- **1.5** (30 April 2026) — New "Working modes" section with two modes: **client branch** (`.roots/{version}.{client}/`) and **source** (`.roots/{module}/`). The mode is asked of the user when processing the seed for the first time and persisted in `_meta.json.working_mode`. Updated "Base structure" with both layouts. `on-seed-process` extended with step 0 of mode detection. New merge protocol between namespaces of different clients/branches. `_meta.json` extended with the `working_mode`, `odoo_version`, `repo` fields.
- **1.4** (24 April 2026) — New `workbench/` folder for user reference materials. New section "Sync with the canonical upstream (ctmil/roots_seed)" with a version-comparison protocol and contribution rules. New section "Integration with CLAUDE.md and Claude Code (.claude/)" with a context hierarchy, no-duplication rules, a CLAUDE.md template, and a future-compatibility table. New hook `on-seed-process.md` that consolidates full bootstrap: upstream sync, distribution, CLAUDE.md verification, and workbench creation. `session-start` extended to list `workbench/` at startup.
- **1.3** (18 April 2026) — Seed distribution rule inside each `.roots/`. Each module/project carries a **local copy** of the seed that generated it, so it is self-contained and reprocessable even if extracted to another repo. New hook `on-seed-update` to re-distribute when the canonical bumps version. `session-start` now compares the local copy vs the canonical and warns if they are out of sync.
- **1.2** (18 April 2026) — Added three protocols to the seed, tool-agnostic (applicable to any AI assistant or human developer):
  - Hook `on-topic-shift`: when shifting focus mid-session to a file/system not covered by the bootstrap, re-scan `.roots/docs/` before asking for clarification or deciding.
  - Hook `on-task-done`: when completing each individual task and before reporting it, update at minimum `tasks/todo.md` + `tasks/tasks.md` + `docs/commits.md`. Conditionally `errors-log.md`, `fixes-log.md`, `decisions.md`, `notes.md`, `glossary.md`, `migrations.md`.
  - `session-start` extended: check the seed version against the agent's memory, check git state (`git branch --show-current`, `git log`, `git status`) vs `_meta.json.active_branch`, warn the human if out of sync, read `notes.md` and design docs of the current feature.
- **1.1** — Base version.

---

## Concept

The `.roots/` folder works as the project's **persistent memory**, organized to:
- Document decisions and progress
- Keep logs of errors and fixes
- Record ideas and reflections
- Track pending tasks
- Define reusable skills and workflows per module

This structure is designed to be used by **AI agents** and **human developers** alike.

---

## Working modes

**Rule:** when processing the seed for the first time in a repo, the agent determines the mode. The **default is Flat** (the simplest — `.roots/` directly). The agent only **asks** if it detects signals of a multi-source / multi-client setup (see "When flat vs namespaced?"). The mode determines whether `.roots/` carries an internal namespace and how merges behave. It is persisted in `_meta.json` (`layout` + `working_mode`) and is not asked again.

### The modes

| Mode | Layout | Namespace | When to use | Example |
|------|--------|-----------|-------------|---------|
| **Flat** (default) | `flat` | none — `.roots/` directly | Single project, few/no embedded remote sources. The common case. | `.roots/context.md`, `.roots/tasks/` |
| **Source** | `namespaced` | `.roots/{module}/` | Multi-module source repo (source of truth of several modules) | `.roots/meli_oerp/` |
| **Client branch** | `namespaced` | `.roots/{context}.{project}/` | Client branch that consumes/embeds one or more sources | `.roots/17.0.sh.acme/` |
| **Workspace** | `flat` root + `geoecon/` etc. | coordinates N repos | The `.roots/` lives in the folder that **contains** several repos and indexes/relates them (it does not document a project). | `.roots/forest.json`, `.roots/<grove>/` |

> The **Source** and **Client branch** modes are both `namespaced` and share the multi-source machinery described below (embedded sources, `_sources.json`, precedence cascade, conflict namespace, promotion). The **Flat** mode does NOT use any of that — jump to "Flat mode" if your repo is a single project. The **Workspace** mode operates *above* the repos (each with its own mode) — see "Forest Model".

### Flat mode (simplified — default)

The most common case: **one repo, one project, one memory**. `.roots/` carries the files directly, without a namespace subdirectory:

```
.roots/
├── _meta.json
├── roots_seed.md
├── context.md
├── journal/        (diary, notes, changelog)
├── tasks/          (todo, tasks)
├── debug/          (errors-log, fixes-log, migrations)
├── design/         (decisions, sketchbook)
├── docs/           (architecture, glossary, commits, ...)
├── hooks/
├── skills/
└── workbench/
```

**When to use Flat:**
- The repo is a bespoke project/product, not a source module consumed by N clients.
- You won't **embed the `.roots/` of other sources** (`sources/`) — or there are very few and you reference them by hand.
- You don't maintain **multiple versions/clients in parallel** in the same working tree.

**What Flat does NOT bring** (and doesn't need): the `{context}.{project}/` subdir, the `sources/` + `_sources.json` system, the precedence cascade, the conflict namespace. All that is machinery for multi-source; in flat it is ceremony without value.

**Context in Flat:** a flat repo **can still declare** its `context_format` / `context_parsed` in `_meta.json` (e.g. "Odoo 17.0, dev") so the agent can reason about the environment — **without** encoding it in the path. Context is *metadata*, not *layout* (see "Context Format Registry").

`_meta.json` includes `"layout": "flat"` + `"working_mode": "source"` (a flat is a source collapsed to a single project).

### When flat vs namespaced? — the rule

The layout is NOT decided by the framework ("it's Odoo → namespaced"). It is decided by **a single question: do I need to keep the memory of multiple contexts alive at the same time?**

- **No** → **Flat.** A project that evolves forward. The old version becomes history (git + `journal/changelog` + `debug/migrations.md`), not a parallel namespace you keep consulting.
- **Yes** → **Namespaced.** Three typical triggers:
  1. **Multi-source:** you embed the `.roots/` of N source modules (hybrid client).
  2. **Parallel multi-version/client:** the same code maintained on Odoo 16 for client A and 17 for B, simultaneously.
  3. **Migration** (see "Migration mode"): during the window, two versions coexist.

Most bespoke repos (one product, one version, going forward) are **Flat**. Namespaced is for reusable sources and for software houses that maintain many clients/versions in parallel.

### Migration mode (flat → temporary namespaced → collapse)

A migration (e.g. Odoo 17 → 19) is a *temporary* case of "concurrent multi-context memory". A normally **flat** repo can **temporarily fork** to namespaced for the transition, and **collapse back** when finished:

```
# Before (flat, in production on 17):
.roots/                          ← live project memory on 17

# During the migration (temporary namespaced):
.roots/17.0.{infra}/             ← fork of the 17 memory (reference: "how it works today")
.roots/19.0.{infra}/             ← new memory accumulated while migrating

# After (collapse to flat on 19):
.roots/                          ← 19 promoted to flat; 17 archived (git history + migrations.md)
```

**Why the namespace helps here:** `{major}.{minor}` is exactly the axis the migration changes. Splitting the memory along that axis lets you:
- Keep `.roots/17.0/` **intact as the source-of-truth of the current behavior** while you build 19.
- Let the agent read **both** without confusing them (don't apply a 17 fix to a 19 case; the ADRs stay tagged by version).
- Treat the migration as a **memory fork**: the decisions that survive are migrated, the version-specific ones are re-evaluated.

When closing the migration, **you collapse back to flat**: you promote `19.0/` to the `.roots/` root and archive `17.0/` (its historical value lives in git + `debug/migrations.md`). You don't stay namespaced forever if you have no other trigger (multi-source / multi-client).

### Hybrid multi-source model

> Applies to the **namespaced** modes (Source / Client branch). It does NOT apply to **Flat**.

A client project is always a **hybrid of one or more sources**. The client's `.roots/` is not an island — it references and embeds the `.roots/` of each source it consumes:

```
.roots/17.0.sh.acme/                    ← client branch
    _meta.json                           ← client manifest
    _sources.json                        ← registry of linked sources
    roots_seed.md                        ← self-contained seed
    journal/                             ← client's own journal
    tasks/                               ← client's own tasks
    debug/                               ← errors of the client context
    sources/                             ← copies of each source's .roots/
        meli_oerp/                       ← copy of .roots/meli_oerp/
            context.md
            journal/
            debug/
            skills/
            docs/                        ← manuals, technical documentation
        odoo_moldeo_sync/                ← copy of another source
            context.md
            journal/
            ...
```

**Why embed the sources?** Because the client's agent has full access to the source's knowledge:
- Reads `docs/` → knows how the module works for the end user
- Reads `debug/errors-log.md` → knows already-diagnosed errors and their fixes
- Reads `skills/patterns.md` → knows which patterns to follow and which anti-patterns to avoid
- Reads `tasks/` → sees whether there is work in progress in the source that could collide
- Reads `journal/diary.md` → knows whether a recurring topic was already discussed and what was decided
- Reads `design/decisions.md` → understands WHY an architecture decision was made

### `_sources.json` — Manifest of linked sources

Each client branch maintains a `_sources.json` file that registers its sources:

```json
{
  "sources": [
    {
      "source_id": "meli_oerp",
      "source_version": "1.6",
      "linked_at": "2026-05-10",
      "linked_by": "claude",
      "upstream_url": "github.com/ctmil/meli_oerp",
      "roots_path": "sources/meli_oerp/",
      "sync_include": ["docs/", "debug/", "journal/", "tasks/", "skills/", "design/"],
      "sync_exclude": ["workbench/"],
      "last_sync": "2026-05-10"
    },
    {
      "source_id": "odoo_moldeo_sync",
      "source_version": "1.6",
      "linked_at": "2026-05-08",
      "linked_by": "claude",
      "upstream_url": "github.com/ctmil/odoo_moldeo_sync",
      "roots_path": "sources/odoo_moldeo_sync/",
      "sync_include": ["docs/", "debug/", "skills/"],
      "sync_exclude": ["workbench/", "journal/"],
      "last_sync": "2026-05-10"
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `source_id` | Name/path of the source module |
| `source_version` | Seed version of the source at the time of linking |
| `linked_at` | Linking date |
| `linked_by` | Who linked it (agent or user) |
| `upstream_url` | Public repository of the source (if any) |
| `roots_path` | Relative path inside the client `.roots/` where the copy lives |
| `sync_include` | Folders to sync (empty = all) |
| `sync_exclude` | Folders to exclude from the sync |
| `last_sync` | Last synchronization date |

### Precedence cascade

When there are conflicts between the client and its sources, precedence is top to bottom:

```
Level 1 (highest priority):  .roots/17.0.sh.acme/            ← root client
Level 2:                      .roots/17.0.sh.acme/sources/X/  ← embedded source
Level 3 (base):               X/.roots/                       ← original source
```

The client **always wins**. If the client defines a pattern or skill that contradicts the source, the client's applies.

### Conflict namespace

When two sources define hooks, skills or patterns with the same name, a **namespace prefixed with the source** is used:

```
meli_oerp.discount_pattern        → PAT-001 of meli_oerp
meli_oerp_accounting.tax_rule     → pattern of the invoicing module
odoo_moldeo_sync.git_workflow     → workflow of the sync module
```

The agent that processes the repo's root `.roots/` (meta level) can:
1. **Compare** — did the `meli_oerp.patterns` of one client and another diverge?
2. **Promote** — if a client discovered a useful pattern, push it up to the original source
3. **Detect** — if a client skill overrides one from the source, the agent warns

### Discovery promotion

When the client discovers something valuable (pattern, fix, decision) that applies to all users of the source:

```
source .roots/  ──→  client .roots/sources/  ──→  client uses and adapts
                                                        │
                                                        ▼
root repo .roots/ ← aggregates all clients ← reviews with namespace
        │
        ▼
    worth it?  ──yes──→  promotes to the original source .roots/
               ──no──→   stays as a client override
```

**Rule:** promotion is **semi-automatic**. The agent suggests ("this pattern from acme applies to all clients, should I promote it to the source?"), the user decides.

When the client overrides a skill or pattern from the source, the agent records the override in the client's journal with the reason.

### Client Branch mode

The developer works on a branch derived from the source, adapting and configuring it for a specific client. The namespace isolates that client's history.

**Characteristics:**
- The namespace `{context}.{project}` follows the Context Format Registry format (see § below)
- Multiple clients can coexist: `.roots/17.0.sh.acme/`, `.roots/17.0.premise.farmacia/`
- When merging to the source, each client brings its `.roots/` without overwriting others'
- `_meta.json` includes `"working_mode": "client"`, `"context_format"`, `"context_parsed"`

**When it is used:**
- Implementation branches for specific clients
- Forks with customizations
- Testing/staging branches that capture environment context

### Source mode

The developer works directly on the module's source. It is the source of truth.

**Structure:**
```
.roots/
├── _meta.json
├── roots_seed.md
├── {module_a}/
│   ├── context.md
│   ├── journal/
│   ├── debug/
│   └── ...
└── {module_b}/
    └── ...
```

**Characteristics:**
- No extra namespace — modules go directly under `.roots/`
- It is the project's canonical `.roots/`
- `_meta.json` includes `"working_mode": "source"`
- Can receive contributions promoted from client branches

**When it is used:**
- Main development branch (e.g.: `19.0`, `main`)
- Canonical repository of the module
- Source maintenance without client context

### Mode detection on seed-process

When running `on-seed-process` for the first time (bootstrap), the agent determines the layout. **The default is Flat** — it does NOT ask if the repo is a single project. The agent only asks when it detects **namespaced signals**:
- The repo is a **reusable source module** (consumed by other projects/clients), or
- It will **embed the `.roots/` of other sources** (`sources/`), or
- It maintains **multiple versions/clients in parallel**, or
- It is entering a **migration** (see Migration mode).

Without those signals → Flat directly, without asking. With signals, the agent asks:

```
I detected signals of a multi-source/multi-client setup. Which layout do I use?

0. Flat (default) — One project, one memory. .roots/ directly, no namespace.
   → No subdir is created. (Optional: declare context_format in _meta.json.)

1. Source — Multi-module source repo (source of truth of several modules).
   → .roots/{module}/ is created per module.

2. Client branch — Client branch that consumes/embeds sources.
   → .roots/{context}.{project}/ is created with an isolated namespace.
   → It will ask: context_format (Odoo/generic/custom) + sources to link.
```

The answer is persisted in `_meta.json` (`layout` + `working_mode`) and **is not asked again** in later sessions. A Flat repo can become namespaced later (e.g. when starting a migration) — see Migration mode.

### Merge between modes

| Scenario | Behavior |
|-----------|----------------|
| Client A → Source | `.roots/{context}.{client_a}/` coexists with `.roots/{module}/` — they don't overwrite each other |
| Client A + Client B | Each client has its namespace, they coexist without conflict |
| Client → Client (same namespace) | Standard git merge — the append-only files (diary, errors-log) resolve naturally |
| Source → Client | The client embeds the source's `.roots/` in `sources/` — it is a reference copy |
| Source updates → Client | The agent detects a diff between the embedded source and the original source, proposes a sync |

**Merge rule:** when detecting multiple namespaces in `.roots/`, **do not consolidate automatically**. Each namespace is an independent history. If the user wants to consolidate (e.g.: close a client branch and bring the learnings to the source), it must be explicit:

```
"Consolidate .roots/17.0.sh.acme/ → .roots/meli_oerp/"
```

The agent then:
1. Reads both `.roots/`
2. Proposes what to migrate (decisions, patterns, glossary are good candidates; diary and errors-log are contextual)
3. The user approves item by item
4. The selected content is merged
5. The client's namespace can be archived or deleted

---

## Context Format Registry

The `{context}` in `.roots/{context}.{project}/` (**namespaced** layout) is not a free string — it has **semantic structure per domain**, which agents parse to reason about the environment.

> **Layout vs metadata (v1.7):** the Context Format describes TWO independent things — (1) how the subdir is *named* when the layout is `namespaced`, and (2) the `context_format`/`context_parsed` *metadata* of `_meta.json`. A **Flat repo does NOT use the subdir**, but **can still declare** `context_format`/`context_parsed` in its `_meta.json` so the agent knows "this is Odoo 17.0, dev" without encoding it in the path. In other words: context can be **registered without namespacing**. The Registry below defines the formats; they apply to the metadata in any layout and to the subdir name only in namespaced.

### Registered formats

#### Odoo Context

**Pattern:** `{major}.{minor}.{infra}`

| Segment | Values | Description |
|----------|---------|-------------|
| `major` | `16`, `17`, `18`, `19` | Odoo major version |
| `minor` | `0`, `1`, ... | Odoo minor version |
| `infra` | `sh`, `premise`, `cp`, `vps`, `docker`, `dev` | Deployment infrastructure |

**Recommended infrastructure codes:**

| Code | Meaning |
|--------|-------------|
| `sh` | Odoo.sh (official PaaS) |
| `premise` | On-premise (client's own server) |
| `cp` | CloudPepper (third-party PaaS) |
| `vps` | Generic VPS |
| `docker` | Docker / containers |
| `dev` | Development / local |

**Examples:**
```
.roots/17.0.sh.acme/              → Odoo 17.0, SH, client Acme
.roots/16.0.premise.farmacia/     → Odoo 16.0, on-premise, client Farmacia
.roots/17.0.cp.tienda/            → Odoo 17.0, CloudPepper, client Tienda
.roots/18.0.vps.coop/             → Odoo 18.0, VPS, client Coop
.roots/19.0.dev.testing/          → Odoo 19.0, development, testing environment
```

The infrastructure codes are **semi-open**: the common ones are defined above, but the user can use custom ones (e.g.: `aws`, `gcp`, `hetzner`).

#### Generic Context (default)

**Pattern:** `{version}`

For non-Odoo projects or projects without a domain-specific structure:
```
.roots/v2.acme/                   → Version 2, project Acme
.roots/main.internal/             → main branch, internal project
```

#### Custom Contexts

Domains can register their own context format in `_meta.json`. The seed does not pretend to cover all frameworks — the community can contribute formats for Django, Rails, Next.js, etc.

### `context_parsed` in `_meta.json`

The `_meta.json` of each `.roots/` explicitly declares its context format so the agent can parse it:

```json
{
  "context_format": "odoo",
  "context_parsed": {
    "major": 17,
    "minor": 0,
    "infra": "sh",
    "project": "acme"
  }
}
```

This way the agent can reason about the environment (it knows it is Odoo 17 on SH) without guessing.

---

## Extended _meta.json

**Flat (default)** — the simple case; `context_format`/`context_parsed` are optional (metadata to reason about the environment, without namespacing):

```json
{
  "seed_version": "1.7",
  "created_at": "2026-05-30T00:00:00",
  "layout": "flat",
  "working_mode": "source",
  "lang": "en",
  "context_format": "odoo",
  "context_parsed": { "major": 17, "minor": 0, "infra": "dev" },
  "project": "mi_proyecto",
  "modules": ["mi_proyecto"]
}
```

**Namespaced (Client branch / multi-module Source)** — uses the subdir + multi-source machinery:

```json
{
  "seed_version": "1.7",
  "created_at": "2026-05-10T00:00:00",
  "layout": "namespaced",
  "working_mode": "client",
  "lang": "es",
  "context_format": "odoo",
  "context_parsed": {
    "major": 17,
    "minor": 0,
    "infra": "sh",
    "project": "acme"
  },
  "project": "17.0.sh.acme",
  "modules": ["meli_oerp", "meli_oerp_stock", "odoo_moldeo_sync"],
  "sources": ["meli_oerp", "odoo_moldeo_sync"]
}
```

| Field | Flat (default) | Source | Client branch |
|-------|----------------|--------|---------------|
| `layout` | `"flat"` | `"namespaced"` | `"namespaced"` |
| `working_mode` | `"source"` | `"source"` | `"client"` |
| `lang` | working language (default `"en"`; **auto-detected** on existing deployments) | same | same |
| `context_format` | optional (metadata) | optional | `"odoo"`/`"generic"`/custom |
| `context_parsed` | optional (metadata) | optional | parsed object |
| `project` | project name | project name | `"{context}.{project}"` |
| `modules` | project modules | source modules | client modules |
| `sources` | usually absent / `[]` | not applicable (it is the source) | linked source_ids (ref. `_sources.json`) |

> `layout` absent ⇒ assume `"flat"` (back-compat: pre-v1.7 `.roots/` without `layout` that have files directly under `.roots/` are already flat in fact).

---

## Language & glossary (i18n)

> **The canonical seed is written in English.** But the language of the *memory you write into a `.roots/`* is a **per-deployment** choice that the seed must never override. This section defines that contract. The goal is **zero noise**: updating the seed must not change the language a project already writes in.

### Two separate things

1. **The seed's language** — `roots_seed.md`, `manual.md` and the rest of the toolkit are **canonical in English** (single source that evolves; one language to maintain).
2. **A deployment's working language** — each `.roots/` writes its memory (context, journal, decisions, glossary…) in **one** working language, recorded in `_meta.json.lang` (BCP-47 short code: `"en"` default, `"es"`, `"fr"`, …). **Code and technical identifiers are always English regardless of `lang`** (field names, module names, commands).

These are independent: an English canonical seed can drive a `.roots/` that is written entirely in Spanish.

### The language-lock rule (no noise)

- **New deployments** are born in **`en`** by default (the seed is English). The agent only asks if the user signals another language up front.
- **Existing deployments** keep their language. On seed-process the agent **auto-detects** the language of the existing `.roots/` content and **persists** it to `_meta.json.lang` if absent. A `.roots/` already written in Spanish stays `"es"` — the agent keeps writing Spanish in that project.
- **Updating / re-distributing the seed NEVER translates or rewrites existing memory.** `on-seed-update` only refreshes the canonical `roots_seed.md` copy (English) and the `glossary/` tables. Prose already written in a project is left untouched. The English-ification of the canonical seed is **not** a migration of your projects.
- **Switching language** of a deployment is **explicit and rare** (`"set this .roots/ to en"`); it is never implied by a seed bump.

### Auto-detection (on seed-process, step 0b)

```
if _meta.json.lang exists        → use it, do not ask, do not re-detect
elif .roots/ already has content → detect dominant language of existing
                                    *.md prose (context.md, journal/, decisions…)
                                    → persist to _meta.json.lang  (NO rewrite of content)
else (brand-new .roots/)         → default "en"  (ask only if the user signals otherwise)
```

The detection is a one-time stamp: once `lang` is set it is authoritative and the content is never machine-translated as a side effect.

### The glossary system (`glossary/`)

The cross-language **Forest vocabulary** lives in the seed's `glossary/`:

| File | Role |
|---|---|
| `glossary.json` | **Canonical** source of truth. Key = English slug; each term has `en`/`es`/`fr` (`term` + `def`), a `category`, and `see_also`. |
| `gen.py` | Generator (stdlib only) → emits one `GLOSSARY.<lang>.md` table per language. `--check` guards staleness. |
| `GLOSSARY.{en,es,fr}.md` | **Generated** tables — do not edit by hand. |

English is primary (the key); `es`/`fr` are translations and may lag (a missing one falls back to the English term, flagged). This gives an agent or human writing a project's `.roots/` in any `lang` a **consistent rendering of the model's terms** (Roots, Grove, Tree, modes, axes…). It is distinct from a project's own `docs/glossary.md`, which holds **domain** terms in that deployment's `lang`.

> **To add/curate vocabulary:** edit `glossary/glossary.json`, run `python3 gen.py`, commit the regenerated tables. To add a language: extend `meta.languages` + `gen.py` headings.

---

## Tool Compatibility

### Philosophy

`.roots/` is **tool-agnostic by design**. The structure is plain files and directories — any AI tool that can read files can use it. Portability comes from the **simplicity and clarity of the description**, not from automatic translations.

### Main tools with known compatibility

| Tool | Integration point | Merge strategy |
|-------------|---------------------|---------------------|
| **Claude Code** | `.claude/` + `CLAUDE.md` | File-based — reads `.roots/` directly. Bridge via `CLAUDE.md` (see § Integration) |
| **Codex** | `codex.md` / `.codex/` | Hybrid — map `context.md` → `codex.md`, has native support + config |
| **Antigravity** | native | File-based — direct support of `.roots/` |
| **VS Code + Copilot** | `.github/copilot-instructions.md` | Instruction-based — reference `.roots/` from instructions |
| **Cursor** | `.cursorrules` | Instruction-based — reference `.roots/` from rules |

### Merging Strategies

Each tool integrates context differently:

- **File-based**: The tool reads files from `.roots/` directly at session start (Claude Code, Antigravity)
- **Instruction-based**: The tool needs a pointer file that references `.roots/` (Copilot, Cursor)
- **Hybrid**: The tool has native support + a configuration file (Codex)

### Extensibility

- **Maximum 5 main tools**, 10 cap in the seed — the rest is community
- Additional integrations can be contributed as skills in the upstream (`ctmil/roots_seed`)
- The idea is that the description be so clear and simple that any new AI understands it without translation
- Always think in terms of an **infinite progression of AIs** — the references to the 5 main ones serve to situate future tools

---

## Complementary toolkit (`scripts/` + `skills/` + `tools/`)

The `.roots/` structure is **tool-agnostic** and stands on its own, but persistent memory does not live in thin air: it lives in **repos**. The seed is published alongside a toolkit that mounts that substrate, improves it and visualizes it. These tools are **complementary and optional** — they don't change the `.roots/` format; they operate it, enrich it and expose it.

> **Principle:** the toolkit is **referenced, not inlined**. Each tool is self-contained, with its own README, and evolves apart from the spec. This section systematizes the concept and points to the directories; the code lives in them.

### `scripts/` — mount and operate the fleet

`.sh` templates copied to the root of a **workspace** (the folder that contains the repos) that build the physical substrate of the memory with the **bare + worktrees** pattern (one `.bare` per repo, one worktree per version/branch — shared git objects, optimized local space):

| Script | Role |
|--------|-----|
| `setup-module.sh` | Clones a repo as bare + worktrees per branch |
| `setupbranch.sh` | Adds a worktree for a branch (auto-detects existing/new) |
| `dashboard.sh` | Launches the viewer (`tools/forest-dashboard`) pointing at the workspace |

See `scripts/README.md`.

### `skills/` — reusable strategies (shared library)

**Cross-cutting** and well-designed skills that live in the seed to improve common strategies. They are the **shared** library, distinct from the `skills/` that each `.roots` has locally (`prompts.md`/`workflows.md`/`patterns.md` specific to the module): a module references or copies/adapts from here, and promotes back whatever turns out to be general.

First skills:

| Skill | For what |
|-------|----------|
| `odoo-module-merging.md` | Merge of branches/clients toward official Odoo repos: layered review, cross-version conflict patterns, `.roots` promotion |
| `md-to-pdf-reporting.md` | `manual.md` / `documentation.md` → PDF (pandoc / HTML+CSS / Odoo QWeb) — reporting base |

See `skills/README.md`.

### `tools/` — apps on top of the memory

Applications that **read the `.roots`** and expose them. First of the toolkit:

- **`forest-dashboard/`** — navigable web viewer (cards → recursive drill-down, changes HERO + tabs for tasks/docs). Architecture in 3 layers: collector → `state.json` (reusable contract) → view. Designed as a **base to port to an Odoo backend** (e.g. `odoo_moldeo_sync`), where the same `state.json` is emitted from models and the hierarchy maps to a tree pattern (`odoo_moldeo_htree`).

See `tools/<name>/README.md`.

### Relationship with the spec

The toolkit assumes the bare+worktrees pattern, but the **`.roots/` format does not depend on it**: any project (a single repo, a single dir) uses the same memory structure without needing the toolkit. Adopt the tools if they help you; ignore them if your setup is simpler.

---

## Forest Model — workspace coordination (multi-repo)

> This section formalizes the **`workspace`** working_mode: a `.roots/` that does not document *a* project but **coordinates N repos** from the folder that contains them. It is the layer used by the toolkit's `scripts/` and the `forest-dashboard`. It **does not replace** the per-repo modes (Flat/Source/Client-branch) — it lives *above* them.

### When it applies

When you mount several repos together (bare+worktrees pattern) and need a place that **indexes and relates** the fleet without duplicating the memories that already live in each repo. The golden rule of the workspace level: **index and point, don't duplicate** — the root `.roots/` coordinates; the real memories stay in `<repo>/<worktree>/.roots`.

### Vocabulary (grows from the roots)

The metaphor starts at `.roots` and goes up:

| Term | Is | Example |
|---|---|---|
| **Roots** (`.roots`) | the memory/knowledge layer | `context.md`, `decisions.md`, `journal/` |
| **Forest** | the whole workspace — all coordinated repos | the folder that contains the repos |
| **Grove** | a **product/suite**: a cluster of Trees with a common function | Meli · OCAPI · GeoEcon |
| **Tree** | a **repo** (mounted bare+worktrees) | `meli_oerp`, `geoecon_map` |
| **Branch** | a git branch / worktree of the Tree | `17.0`, `mapdev` |

> Fits git: a worktree contains a *working **tree*** and the branches are *branches*.

### Axes of each Tree (orthogonal)

A Tree is described with **independent** labels; don't confuse "what it is" with "who makes it", "where it lives" or "what it uses":

| Axis | Question | Cardinality | Values |
|---|---|---|---|
| `grove` | which **product** is it part of? | **1 primary** | Meli, OCAPI, Fulfillment, GeoEcon… |
| `also_groves` | does it co-belong to another product? (rare) | 0..N tags | only genuine co-membership, **NOT** dependency |
| `vendor` | who **creates/maintains** it? | 1 (ownership) | `moldeo-interactive`, `oca`, `odoo-sa`, `3rd-party` |
| `kind` | what **nature** does it have? | 1 | enum below |
| `org` | where does the repo **live**? (hosting) | 1 | the hosting org/namespace |

**`kind` enum:** `producto-suite` (end-user product) · `plataforma` (abstract base that others depend on) · `agregador` (deployment that nests modules from many Groves) · `external-upstream` (vendored, not authored by us: Odoo core, OCA) · `seed` (roots tooling/seed).

**`vendor` = ownership + optional profile:** `vendor` is a field of the Tree, NOT a structural node. Optionally each vendor/author/person has a profile in `.roots/vendors/<slug>.md` (its descriptive "own root") that ownership references. The same actor can be a vendor (author) and a Grove (product) without clashing.

### Relations = graph (the golden rule)

> **`grove` = "what it is" · edge = "what it uses" · `also_groves` = "also belongs to" (rare).**

**Dependencies are NOT modeled as membership or as nesting** — they are **edges** of a directed graph (DAG). A shared base (e.g. a `connector_api` platform) is **depended on by Trees of different products**; if the dependency were membership/hierarchy we would break the products (a node can't have two parents; a platform tag would mean both "is part of" and "depends on" at once).

`relations[]`: `{ "from": <tree/module>, "to": <tree/module/service>, "type": <type> }` — types: `depends-on`, `extends`, `integrates`, `relates`.

### `forest.json` — structured registry

It is the rename of `fleet.json`. The `forest-dashboard` reads `forest.json` (with fallback to `fleet.json`); **`fleet.json` is kept as a symlink** for compat with old tools or upstream forks. The array is still `repos[]` with `name`/`role`/`notes`; the new axes (`grove`/`vendor`/`kind`/`org`) are added as additional fields (an old tool ignores what it doesn't know).

```jsonc
{
  "vocabulary": "Roots > Forest > Grove > Tree > Branch",
  "groves":  [ { "id": "ocapi", "label": "OCAPI", "kind": "plataforma", "vendor": "moldeo-interactive" } ],
  "vendors": [ { "id": "moldeo-interactive", "label": "Moldeo Interactive", "profile": "vendors/moldeo-interactive.md" } ],
  "repos": [               // = Trees ('repos' key for compat with the dashboard)
    { "name": "meli_oerp_multiple", "org": "...", "grove": "meli", "vendor": "moldeo-interactive",
      "kind": "producto-suite", "role": "source", "worktrees": ["17.0"], "bare_size": "4.3M" }
  ],
  "relations": [
    { "from": "meli_oerp_multiple",       "to": "connector_api", "type": "depends-on" },
    { "from": "connector_api_fulfillment","to": "connector_api", "type": "extends" }
  ]
}
```

> The workspace level is registered in `_meta.json` with `working_mode: "workspace"`. The `forest-dashboard` **draws `relations[]` as a graph** in its *Forest map* tab.

### Sync semaphore (multi-session over the same source)

When several sessions (agentic or human) work over the **same worktrees** of a Tree
(a bare module + N branches/versions), one can overwrite **uncommitted** changes of another. To
coordinate without git commits or locks, the seed defines a **lightweight per-module semaphore**:

- **One flag per Tree, in the CONTAINER of its branches** (NOT recursive per branch — it would be slow and
  would leave *stale* flags if a session dies): `<wt_container>/<module>/.SYNCING`.
- **Content** (instant read/write): `FREE` (released) | `LOCKED|by=…|since=ISO8601|scope=…|task=…`.
- **Flow**: before porting/syncing a module cross-version → `check`; if `LOCKED` by another and
  recent, **wait**; if `FREE` → `acquire`, do the sync, `release` (leaves `FREE`).
- **Forest view**: `list` scans all the `.SYNCING` (there is no aggregate file to keep
  in sync — the per-module flags ARE the source of truth).
- **Stale**: a `LOCKED` older than a threshold (def. 2h) is considered abandoned and can be taken
  (`SYNC_FORCE=1`). Session identity via `SYNC_WHO`.
- The `.SYNCING` are **runtime** (out of git, not committed). Reference helper:
  `scripts/sync-lock.sh {check|acquire|release|list}`.

> Why container and not per-branch: a cross-version sync touches **all** the branches of the module,
> so the natural flag is at the module level (one file, fast), not 1-per-branch (N files, stale).

### Inter-session comms (`state/comms.md` — point-to-point fallback)

The semaphore is a **mutex** (prevents two sessions from colliding on a module); it carries **no
information**. When a session or agent needs to *tell another* something durable and async — there
is **no live IPC between Claude sessions** — the seed defines a **file-based message bus**, the
**fallback channel** that always works because it is just a file in the repo:

- **One append-only log per repo/workspace**: `state/comms.md` (committed — survives sessions; lives
  beside the other `state/` docs). At the **workspace** level it coordinates the Forest; inside a
  Tree it is local to that repo.
- **Each message is a block, newest on top:**
  ```
  ## <ISO-8601> · from: <who> · to: <who|@all> · re: <topic> · status: open
  <body: what happened / what to keep in mind / what is requested>
  ```
- **Fields:** `from`/`to` = session/agent identity (reuse `SYNC_WHO`, or the branch/worktree it runs
  on). `to: @all` = broadcast. `status`: `open` → `ack` (read/seen) → `done` (resolved/obsolete).
- **Etiquette:**
  - On session start, and **before any push/sync**, READ `state/comms.md`; act on messages addressed
    `to: me | @all` with `status: open`.
  - To acknowledge, flip `status` to `ack` (or append a reply block under it); mark `done` when resolved.
  - Keep messages short and **link** to the detail (commit SHAs, files, other `state/` docs) — don't
    inline it. Prune `done` messages older than ~2 weeks to keep the log light.
- **Semaphore vs comms (complementary):** `.SYNCING` = *mutual exclusion* ("don't both touch module
  X"); `state/comms.md` = *information* ("here's what you need to know / a heads-up / a hand-off").
  Use the lock to avoid collisions, the bus to pass context.
- **Fallback discipline:** prefer a live channel (the human relaying, a shared ticket) when one
  exists; `comms.md` is the durable async default. It is point-to-point (`to: <who>`) **and**
  broadcast (`to: @all`); a hand-off between agents is just a message whose `body` says what was left
  half-done and where.

---

## Per-domain recipes (`recipes/` + `manual.md`)

The `.roots`/Forest model is not only for Odoo: the same primitives apply to software, design and narrative. The applied detail lives in `recipes/` (referenced, not inlined); the navigable front door is `manual.md`.

**Thesis:** three primitives are reused across N domains →

| Primitive | Code (Odoo) | Design (Folio) | Narrative/game |
|---|---|---|---|
| **vendor** | who maintains the module | the artist/user | the author/screenwriter |
| **`relations[]`** | `depends-on` between modules | prototype→layout, work→author | character→NPC, scene→scene, concept↔concept |
| **branch** | git branch | design variant (`prototype.branch`) | script arc (canon/what-if/playtest) |

Recipes (`recipes/`):
1. **odoo-suite** — `Grove = suite · Tree = module · relations = depends`.
2. **design-forest** — `1 vendor (artist) > N trees > designs`; bridge `ai_context_md` ↔ `.roots/context.md`.
3. **narrative-game** — domain pack `working_mode: narrative` (worldbible, entries, arcs=branches, **character skills ≡ AI skills**).
4. **token-economy** — see the next section.

> **Domain pack:** a domain overlay (extra folders like `worldbible/`, `arcs/`) on top of any base mode, marked in `_meta.json` (e.g. `working_mode: "narrative"`). Reuses the seed skeleton; does not replace it.

---

## Token economy & model benchmarking

The `.roots` saves tokens by design: **read by layers, don't reload the corpus every turn**. Applies to any `.roots`.

### Layer ladder

```
L0  cheap index       context.md · _meta.json · forest.json · MEMORY    (almost always)
L1  active slice      tasks/todo.md + _meta.current_feature + 1–2 docs   (the task)
L2  domain doc        drill on-demand: ONE file from docs/               (when needed)
L3  full corpus       read everything                                    (rare, explicit)
```
Rule: stay at the lowest layer that solves the task. `hooks/` and `_meta.current_feature` exist to load the right slice without sweeping everything.

### Formula (two readable numbers)

- **CER** (Context Efficiency Ratio) = `useful_tokens / loaded_tokens` — density of what was read.
- **FS** (Frugality Score) = `tokens_if_I_read_everything / loaded_tokens` — "I read 1/N of the corpus".
- **Tiers** (loaded tokens): trivial ≤5k (L0) · normal ≤20k (L0+L1) · deep ≤80k (L0+L1+L2) · full no cap (L3, justify).

### Benchmark + techniques

- `journal/benchmarks.md` — one row per session: `date · model · task · tokens_in/out · layers · FS · quality(1–5) · note`.
- `skills/model-techniques.md` — per-model distillate (when to use Opus/Sonnet/Haiku, prompt patterns, cache ~5min, when to delegate to subagents, when to move up to L3).
- Loop: **measure → distill technique → apply → measure**. The knowledge of how to spend tokens well is persisted, not relearned.

Detail: `recipes/token-economy.md`.

---

## Agents and skills — importable library (on-demand)

> The **skills** and the **subagents** (Claude Code format) form a **canonical library that grows** in `roots_seed/{skills,agents}/` and is **referenced** from this `roots_seed.md`. Each repo keeps its copy in **`.roots/{skills,agents}/`** — because **`.roots` always goes tracked/committed** (versioned, evolves, travels with the seed's distribution). `.claude/{skills,agents}/` is **activation only**: you copy there what you want Claude Code to use **generally**; it is local and **does not need to be tracked**.

**Two layers + base (don't confuse them):**

| Layer | Where | Tracked? | Role |
|---|---|---|---|
| **Store** | `<repo>/.roots/{agents,skills}/` | **yes** (with the repo) | where they **live** and evolve; local source of truth; copyable |
| **Activation** | `<repo>/.claude/{agents,skills}/` | no (local) | you copy here what you want to use; Claude Code reads from here |
| **Base** | `roots_seed/{agents,skills}/` | yes (seed) | cross-client library everyone draws from |

**Why import on-demand:** the base can become huge. Not everything is preloaded in each client: the seed reports *what exists and where*; you copy to `.roots/` what that repo needs and **activate in `.claude/`** what you are going to use (fits the *layer ladder* of Token economy: the library is L2/L3, not L0).

**Lifecycle:**
1. **Design** in the workspace's `.roots/agents/` (or `.roots/skills/`); **activate** by copying to `.claude/` and test in real use.
2. **Promote** the tested version to the seed base (`roots_seed/{agents,skills}/`).
3. **Reference** here so every client discovers it.
4. In each client: the copy lives in its `.roots/` (tracked) and is **activated on-demand** in `.claude/` when needed.

**Subagent** (`<name>.md`): an expert persona with **its own context**, restricted `tools` and `model`. Initial catalog (Forest-aware: they read `forest.json`/`.roots`, respect `grove`/`vendor` and the read-only sources):

| Agent | For | Model |
|---|---|---|
| `odoo-architect` | architecture: models, inheritance, ADRs | opus |
| `bug-hunter` | diagnosis + minimal bug fix | sonnet |
| `odoo-migrator` | backport/forward-port 16↔17↔18↔19 | opus |
| `designer` | UI/UX: Folio layouts, geoecon_map, dark theme (Figma MCP) | sonnet |

**Skill** (`<name>/SKILL.md`): a reusable procedure/knowledge; an agent can use skills (e.g. `odoo-migrator` uses `odoo-module-merging`).

> The `forest-dashboard` and the toolkit already follow this pattern (referenced, not inlined). Agents are **designed in `.roots/agents/`** and, once tested, promoted to the seed.

---

## Seed distribution (mandatory)

**Rule:** each `.roots/` carries a copy of the seed that generated it, as `.roots/roots_seed.md`. It is not optional — it is the mechanism that makes the module self-contained and reprocessable.

### Why

1. **Self-contained:** if the module is extracted to another repo, the seed travels with it. Any AI/human who opens the isolated module has the spec to interpret and maintain the `.roots/`.
2. **Reprocessable:** when in doubt about conventions, the agent can re-read the local seed and reapply without depending on the canonical (which may have moved or not be accessible).
3. **Versionable:** the local copy reflects which seed version this `.roots/` was generated with. It allows detecting desync and migrating conventions when the canonical evolves.
4. **Auditable:** diff between the local copy and canonical = delta pending to apply to the module.

### Where the canonical lives

The seed's canonical lives in the module that maintains it. In this repo:

```
odoo_moldeo_roots/roots_seed.md   ← canonical (editable)
```

Every distributed copy carries the header:

```html
<!-- CANONICAL: odoo_moldeo_roots/roots_seed.md -->
<!-- This is a distributed COPY of the seed so the module is self-contained. -->
<!-- For permanent changes: edit the canonical and re-distribute to all .roots/. -->
<!-- For local experimental changes: add a footnote to this file. -->
```

### When to re-distribute

- **When creating a new `.roots/`** → copy the canonical with header (part of the module bootstrap).
- **When bumping the canonical version** → run `hooks/on-seed-update.md` → re-distribute to all the repo's copies.
- **When bringing in an external module that already has `.roots/`** → compare embedded seed vs canonical, resolve the delta.

### Distribution command (one-shot, tool-agnostic)

```bash
SEED="odoo_moldeo_roots/roots_seed.md"  # adjust per repo
HEADER='<!-- CANONICAL: '"$SEED"' -->
<!-- This is a distributed COPY of the seed so the module is self-contained. -->
<!-- For permanent changes: edit the canonical and re-distribute to all .roots/. -->
<!-- For local experimental changes: add a footnote to this file. -->

'
find . -type d -name ".roots" -not -path "*/node_modules/*" | while read -r dir; do
    { printf '%s' "$HEADER"; cat "$SEED"; } > "$dir/roots_seed.md"
done
```

---

## Workbench — Reference materials

**Rule:** each `.roots/{module}/` includes a `workbench/` folder as free space for reference materials the user shares during work.

### What goes in workbench/

- Images, screenshots, mockups
- PDFs, analysis documents
- Videos or links to videos
- Sample datasets, CSVs
- Third-party files for study
- Any material the user passes as reference

### Rules

1. **The user is the one who fills the workbench** — the agent does not invent content here; it only consults it.
2. **The agent MUST review `workbench/`** at session start (see `session-start`) and on topic shift (see `on-topic-shift`). If there are new files, read them or mention their existence.
3. **There is no mandatory format** — it is free space, it does not require internal structure.
4. **Files can be temporary** — the user can delete obsolete materials without consequences.
5. **It is not redistributed** — unlike the seed, the workbench content is local to the module and is not copied between `.roots/`.
6. **If a material inspires a decision** → reference it in `design/decisions.md` (e.g.: "see `workbench/mockup-v3.png`").
7. **Selective gitignore** — heavy files (videos, large datasets) can be added to the module's `.gitignore`; the light ones (screenshots, notes) are committed.

---

## Collective — project influences and references (permanent)

**Rule:** each `.roots/{module}` (and/or the grove/project level) can include a `collective/` folder:
the **permanent memory** of the **third-party references** that nourish the project — people, ideas,
sites, works, organizations, books. It is the record of *who/what we draw from*, with attribution.

**`collective` ≠ `workbench` — the difference is PERMANENCE:**

| | `workbench/` | `collective/` |
|---|---|---|
| Nature | work surface | memory / lineage / contrib |
| Permanence | **ephemeral** (deleted systematically) | **kept** |
| Content | material the user drops for a task | curated and attributed references |
| Redistribution | local to the module, not copied | part of the repo's versioned memory |

What in `workbench/` inspires something and **deserves to stay** → is **promoted** to an entry in `collective/`.

### Branching (emergent categories)
`collective/` **branches inward** into subfolders according to what the author needs to track closely.
There are **no** fixed categories (`code/`/`inspiration/` are not forced): they emerge from the project. Each subfolder
is a *family* of references with its `README.md` (what it groups + naming format) + `.md` entries.
For **code**, `collective/` works as a **contrib** (third-party reference contributions/implementations);
for **creative** projects, as attributed **inspiration sources**. Same format.

### `library/` — library (first-class)
References to **books/publications** are foundation, not decoration. Recommendation:
- **Single spine `library/bibliografia.md`**: *annotated* bibliography (numbered corpus; per entry:
  a table `Author · Publisher · Year · Discipline · Link · Cover` + **Summary** + **Connection with the
  project**). It is kept as **a single text** because the books **dialogue with each other**; it renders
  to PDF (md→PDF pipeline).
- **Graduation**: a book moves to `library/<slug>.md` (its own entry) only when it accumulates a reading
  log / quotes / essay, and the bibliography **links** it.

### Attribution, contact and media (mandatory)
Since `.roots/` is **versioned and pushed**, everything in `collective/` is public in the repo:
1. **Each entry credits authorship and rights** (author, source, use/license). The author **chooses the
   citation/name format** and keeps it consistent per subfolder.
2. **Contact + media** are part of the entry (to return to the source and sustain the link):
   a `Contact` block (email · phone/WhatsApp · Instagram/social · web) and a `Media and references` block
   (images · videos · works/links). **Local or remote**: `![alt](assets/…)` or `![alt](https://…)`.
3. **Privacy** — project handles/emails are public (they go without issue). Sensitive personal
   data (private phone/WhatsApp) → the author decides: **omit**, **`gitignore`**, or note
   "ask". Do not expose third parties' private contact without agreement.
4. **Heavy binaries** (video, high resolution) → selective `gitignore` or only the link; the `.md`
   entries and light thumbnails are committed. Local media: `collective/<family>/assets/`.

### Entries (reference formats)
It is not a rigid form — the `.roots/` is a **new writing format**: the entry is living text
that grows with the author's follow-up (a "Follow-up (live)" log-style section, latest on top).
Base models:
- **Person / idea / site / work** — identity · contact · media · what it contributes to the project · links · follow-up.
- **Organization / studio / friendly project** — what it is and does · contact · media · what it contributes · follow-up.
- **Book** — bibliographic data · rights · summary · connection with the project · quotes · log.

> When a collective reference inspires a decision → link it from `design/decisions.md`.

---

## Sync with the canonical upstream (ctmil/roots_seed)

**Rule:** the seed's canonical is published as an open-source copy at:

```
https://github.com/ctmil/roots_seed/blob/main/roots_seed.md
```

This public upstream is the **parity reference**. The private repo's canonical (`odoo_moldeo_roots/roots_seed.md`) may have its own extensions, but the core conventions must stay aligned with the upstream.

### Canonical hierarchy

| Level | Location | Role |
|-------|-----------|-----|
| **Public upstream** | `github.com/ctmil/roots_seed/main/roots_seed.md` | Open-source reference, core conventions |
| **Repo canonical** | `odoo_moldeo_roots/roots_seed.md` | Local source of truth, can extend the upstream |
| **Distributed copies** | `.roots/roots_seed.md` (each module) | Self-contained, reflects the repo's canonical |

### Sync protocol on seed-process

Every time an agent or human **processes the seed** (bootstrap, session-start, version bump), it must:

1. **Get the upstream version** — fetch `https://raw.githubusercontent.com/ctmil/roots_seed/main/roots_seed.md`, read the `**Version:**` field.
2. **Compare with the local canonical version** — read `odoo_moldeo_roots/roots_seed.md`, same field.
3. **Resolve per case:**

| Case | Action |
|------|--------|
| Local < Upstream | Review the upstream changelog, apply new changes to the local canonical, bump the version, re-distribute |
| Local = Upstream | No action — at parity |
| Local > Upstream | The local canonical has its own extensions. Evaluate whether the extensions should go up to the upstream (PR to `ctmil/roots_seed`) |
| Diff without version change | Cosmetic or local change. Document in `journal/notes.md` |

4. **If there is a substantial delta** → warn the human before applying. Don't merge blindly.
5. **If the upstream is not accessible** (offline, rate limit) → continue with the local canonical, note in `journal/notes.md` that it could not be verified.

### When to sync with the upstream

- **When bootstrapping a new `.roots/`** → verify that the local canonical is up to date with the upstream.
- **When bumping the local canonical version** → evaluate whether the bump includes things that should go up to the public upstream.
- **At session start** (optional, non-blocking) → if the agent has internet access, do a quick check. Don't block the session if it fails.

### Contributing to the upstream

If the local canonical evolves with conventions useful to the community:

1. Prepare the diff between the local canonical and upstream.
2. Separate private extensions (repo-specific) from generic improvements.
3. Generic improvements → PR to `github.com/ctmil/roots_seed`.
4. Private extensions → stay only in the local canonical.

---

## Integration with CLAUDE.md and Claude Code (.claude/)

**Principle:** `.roots/` is tool-agnostic — any agent or human must be able to read it. `CLAUDE.md` and `.claude/` are specific to Claude Code. When both coexist, `.roots/` is the **source of truth** and `CLAUDE.md`/`.claude/` are **bridges**.

### Context hierarchy

| File | Scope | Who reads it | Role |
|---------|---------|--------------|-----|
| `CLAUDE.md` (root) | Global project | Claude Code (auto-loads) | Index and top-level directives |
| `.roots/{module}/context.md` | Specific module | Any agent/human | Module detail |
| `.claude/` (root) | Claude Code config | Only Claude Code | Optional bridge — settings, json hooks |

### No-duplication rules

1. **`CLAUDE.md` indexes, it does not repeat.** If `.roots/` exists, `CLAUDE.md` lists the active modules and points to each `.roots/{module}/context.md`. It does not copy the content of context.md or other `.roots/` files.
2. **`.claude/hooks/*.json` can bridge.** Claude Code hooks can trigger reading/execution of the tool-agnostic protocols in `.roots/*/hooks/*.md`. The logic lives in `.roots/`, the trigger in `.claude/`.
3. **Without `.roots/`, `CLAUDE.md` is autonomous.** If a project has no `.roots/` (it is legacy or simple), `CLAUDE.md` documents stack and directives directly. The creation of `.roots/` is not forced on projects that don't need it.
4. **With `.roots/`, `CLAUDE.md` is light.** It only contains: (a) global directives that apply to the whole project (e.g.: Odoo routing rules), (b) index of modules with `.roots/`, (c) reference to the seed.

### Permissions allowlist (`.claude/settings.json`)

So the agent can run without attending permission prompts, the project's `.claude/settings.json`
keeps a `permissions.allow` of **broad patterns per family** (`Bash(git *)`,
`Bash(python3 *)`, fleet scripts, `Read` of read-only sources), **not** exact commands
(hyper-specific entries make each variant ask again).

- **It evolves with the `.roots`/workspace structure:** when adding scripts (e.g. in `.roots/*/scripts/`),
  read-only source paths or new flows, the allowlist is updated accordingly.
- **Skill `allowlist-sync`** (`.claude/skills/allowlist-sync/`): scans real usage + the structure
  and merges generalized patterns into `settings.json`. Invoke it when prompts reappear or the
  structure changes.
- **Explicit trade-off:** patterns like `Bash(python3 *)`/`Bash(curl *)`/`Bash(rm *)` enable
  broad execution/deletion — a conscious decision of the workspace owner; document it, don't hide it.

### Rule on seed-process (mandatory)

When bootstrapping or bumping the seed, verify `CLAUDE.md`:

| Situation | Action |
|-----------|--------|
| `CLAUDE.md` does not exist | Create with a minimal template (see below) |
| Exists but does not list modules with `.roots/` | Add a module index section |
| Exists and lists modules | Verify the listed modules match the current `.roots/` — add new ones, mark removed ones |
| `.claude/` exists | Verify its hooks reference `.roots/` without duplicating logic |

### Minimal CLAUDE.md template

When `CLAUDE.md` is created from the seed, use this template as a base:

```markdown
# {Project} - Development Directives

## Modules with persistent memory (.roots/)

| Module | Context | Status |
|--------|---------|--------|
| `{module_a}` | [context.md](.roots/{module_a}/context.md) | Active |
| `{module_b}` | [context.md](.roots/{module_b}/context.md) | Active |

## Seed

**Version:** {X.Y}
**Canonical:** `odoo_moldeo_roots/roots_seed.md`
**Upstream:** `github.com/ctmil/roots_seed`

## Global project directives

(Rules that apply to the whole project, not to a specific module.
Example: Odoo multi-website routing conventions, JS standards, etc.)
```

### Future compatibility

Anticipated problems and how to resolve them:

| Problem | Resolution |
|----------|------------|
| Another agent (Cursor, Copilot) ignores `CLAUDE.md` | Doesn't matter — `.roots/` is self-contained and tool-agnostic, the other agent reads it directly |
| Claude Code ignores `.roots/` | `CLAUDE.md` points to `.roots/` — Claude Code follows the links. Alternatively, a `session-start` hook in `.claude/hooks/` can force the read |
| A module extracted to another repo loses `CLAUDE.md` | The module carries its `.roots/` with the embedded seed — it is reprocessable without `CLAUDE.md`. The new repo can generate its own `CLAUDE.md` from the seed |
| `CLAUDE.md` grows too much | A sign that content should migrate to `.roots/`. `CLAUDE.md` must stay a light index |

---

## Base structure

The structure varies according to the layout (see § "Working modes"):

**Flat mode (default):** files directly under `.roots/`, no namespace subdir.
```
.roots/
├── _meta.json          ← "layout": "flat"
├── roots_seed.md
├── context.md
├── journal/  (diary, notes, changelog)
├── tasks/    (todo, tasks)
├── debug/    (errors-log, fixes-log, migrations)
├── design/   (decisions, sketchbook)
├── docs/     (architecture, glossary, commits, manual, ...)
├── hooks/
├── skills/
├── workbench/   ← ephemeral work materials
└── collective/  ← permanent influences/references (≠ workbench)
```

**Source mode (namespaced multi-module):**
```
.roots/
├── _meta.json
├── roots_seed.md
└── {module_name}/
```

**Client Branch mode:**
```
.roots/
└── {context}.{project}/
    ├── _meta.json
    ├── _sources.json
    ├── roots_seed.md
    ├── sources/                    ← copies of each source's .roots/
    │   ├── {source_module_a}/
    │   │   ├── context.md
    │   │   ├── journal/
    │   │   ├── debug/
    │   │   ├── skills/
    │   │   ├── docs/
    │   │   └── ...
    │   └── {source_module_b}/
    │       └── ...
    └── {module_name}/              ← client's own modules
```

Inside each module, the internal structure is identical in both modes:

```
{module_name}/
    ├── context.md             # Quick module briefing (30 sec)
    │
    ├── workbench/             # User reference materials (ephemeral, deleted)
    │   └── (free files)       # Images, PDFs, videos, analysis, etc.
    │
    ├── collective/           # Permanent influences/references (≠ workbench)
    │   ├── README.md          # concept + branching + contact/media + attribution
    │   ├── {family}/          # emergent subfolders (people, orgs, ...) w/README + entries
    │   │   └── assets/        # local media (selective gitignore for heavy ones)
    │   └── library/           # library: bibliografia.md (annotated corpus) + graduated entries
    │
    ├── journal/               # Log - temporal records
    │   ├── changelog.md       # Version history (for clients)
    │   ├── diary.md           # Daily reflections, what happened, thoughts
    │   └── notes.md           # Precise ideas, pre-features, observations
    │
    ├── debug/                 # Debugging and troubleshooting
    │   ├── errors-log.md      # Errors found, analysis, status
    │   ├── fixes-log.md       # What was fixed, how, when
    │   └── migrations.md      # Data, field, schema migrations
    │
    ├── design/                # Design and architecture
    │   ├── decisions.md       # ADRs (Architecture Decision Records)
    │   └── sketchbook.md      # Sketches, diagrams, visual ideas
    │
    ├── docs/                  # Documentation
    │   ├── README.md          # Documentation index
    │   ├── manual.md          # User manual (how to USE)
    │   ├── documentation.md   # Technical documentation (how it WORKS)
    │   ├── architecture.md    # System architecture
    │   ├── glossary.md        # Domain terms and conventions
    │   └── commits.md         # Detailed commit history
    │
    ├── tasks/                 # Task management
    │   ├── tasks.md           # Tasks in progress
    │   └── todo.md            # Backlog and pending
    │
    ├── hooks/                 # Session hooks and automation
    │   ├── session-start.md   # What to run at session start
    │   ├── session-end.md     # What to run at session end
    │   ├── on-error.md        # Protocol when detecting an error
    │   ├── on-fix.md          # Protocol when committing a fix
    │   └── on-seed-process.md # Seed bootstrap/reprocessing
    │
    └── skills/                # Module skills and workflows
        ├── prompts.md         # Reusable module-specific prompts
        ├── workflows.md       # Common module workflows
        └── patterns.md        # Module patterns and conventions
```

---

## Style standards

### General rules

| Aspect | Standard |
|---------|----------|
| **Language** | per `_meta.json.lang` (see "Language & glossary (i18n)"); English for code/technical names |
| **Headings** | Use hierarchical `#`: `#` title, `##` section, `###` subsection |
| **Dates** | Format: `DD Month YYYY` (e.g.: `23 March 2026`) |
| **IDs** | Prefix + sequential number: `ADR-001`, `ERROR-001`, `WF-001` |
| **Separators** | Use `---` between main sections |
| **Lists** | Use `-` for bullets, `1.` for numbered, `- [ ]` for checkboxes |
| **Emphasis** | `**bold**` for key terms, `code` for technical |
| **Links** | Relative within .roots: `[text](./file.md)` |

### Document structure

Every `.md` file in `.roots/` MUST follow this structure:

```markdown
# {Module} - {Document Title}

> One-line brief description of the document's purpose.

---

## Main Section

Content...

---
```

### Voice and tone

| Document | Voice | Tone |
|-----------|-----|------|
| `context.md` | Impersonal | Concise, essential |
| `changelog.md` | Third person | Professional, client-oriented |
| `diary.md` | First person | Reflective, informal |
| `notes.md` | Impersonal | Concise, technical |
| `errors-log.md` | Impersonal | Precise, analytical |
| `fixes-log.md` | Impersonal | Descriptive, technical |
| `migrations.md` | Impersonal | Precise, with versions |
| `decisions.md` | First person plural (we) | Formal, justificatory |
| `manual.md` | Second person (you) | Instructive, friendly |
| `documentation.md` | Impersonal | Technical, detailed |
| `glossary.md` | Impersonal | Definitional, with examples |
| `prompts.md` | Imperative | Direct, clear |
| `workflows.md` | Imperative | Step by step, precise |
| `patterns.md` | Impersonal | Technical, with examples |
| `hooks/*.md` | Imperative | Procedural, executable |

---

## Population protocols

### General protocol

```
┌─────────────────────────────────────────────────────────────┐
│  BEFORE any work session:                                   │
│  → Run hooks/session-start.md                        │
│  1. Read context.md (module briefing)                       │
│  2. Read diary.md (last 5 entries)                          │
│  3. Read notes.md (pending ideas)                           │
│  4. Review tasks/todo.md (backlog)                          │
│  5. Review errors-log.md (active errors)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  DURING the work:                                           │
│  - Found an error → hooks/on-error.md → errors-log.md      │
│  - Fixed something → hooks/on-fix.md → fixes-log.md        │
│  - Made an important decision → decisions.md                │
│  - Had an idea → notes.md                                   │
│  - Completed a task → tasks/tasks.md (mark done)            │
│  - New term → glossary.md                                   │
│  - Changed schema/data → migrations.md                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  AT THE END of the session:                                 │
│  → Run hooks/session-end.md                          │
│  1. Update diary.md with the day's summary                  │
│  2. If there was a release → changelog.md                   │
│  3. If there were significant commits → commits.md          │
│  4. If I created a reusable pattern → patterns.md           │
│  5. If the stack/state changed → update context.md          │
└─────────────────────────────────────────────────────────────┘
```

---

### Protocol per document

#### context.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (when initializing or changing direction) |
| **When** | When creating the module, when changing the stack or significant architecture |
| **Purpose** | 30-second briefing for any new agent or dev |
| **What to include** | What it is, stack, current state, key conventions, dependencies |
| **What NOT to include** | History, implementation details (that goes in docs/) |
| **Size** | Maximum 50 lines — if longer, it doesn't fulfill its purpose |

**Entry format:**
```markdown
# {Module} - Context

> One line describing what the module does.

---

## Stack

- **Framework:** Odoo 17 / Django / etc.
- **Language:** Python 3.10+
- **Database:** PostgreSQL
- **External APIs:** MercadoLibre API v2

## Current State

Brief description of the state: in development, production, maintenance.
Main features working, what's missing.

## Key Conventions

- Convention 1: brief explanation
- Convention 2: brief explanation

## Critical Dependencies

- `module_a`: what it is used for
- `module_b`: what it is used for

---
```

---

#### changelog.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human (final review) or AI (draft) |
| **When** | When releasing a version |
| **Human trigger** | "Prepare changelog for version X.Y" |
| **AI trigger** | Detect commits with a version tag |
| **What to include** | Changes grouped by functional area |
| **What NOT to include** | Technical details, individual commits |
| **Language** | per `_meta.json.lang`; no technical jargon |

**Entry format:**
```markdown
## Version X.Y
DD Month YYYY

**Changes:**

1. **Functional area:** Description of the change in 1-3 user-oriented sentences.
   Explain the benefit, not the technical how.

2. **Another area:** Description...
```

---

#### diary.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (based on the session) |
| **When** | At the end of each work session |
| **Human trigger** | "Update diary" or implicit when closing |
| **AI trigger** | End of session with significant changes |
| **What to include** | What was done, problems, decisions, reflections |
| **What NOT to include** | Code, excessive details |
| **Language** | per `_meta.json.lang`; personal tone |

**Entry format:**
```markdown
**DD Month** - One-line summary.

Development of the day: what was worked on, what problems arose,
what decisions were made and why. Personal reflections
on the code or architecture. Maximum 5-7 lines.
```

---

#### notes.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (idea capture) |
| **When** | Any time an idea arises |
| **Human trigger** | "Note idea: ..." |
| **AI trigger** | Detect an improvement suggestion during work |
| **What to include** | Ideas, observations, things to investigate |
| **What NOT to include** | Concrete tasks (those go to tasks/) |
| **Processing** | Review weekly, move to tasks/ or discard |

**Entry format:**
```markdown
### Idea title (DD Month)

Brief description. Why it could be useful.
References or context if applicable.

**Status:** New | Under evaluation | Discarded | → tasks/todo.md
```

---

#### errors-log.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (when finding an error) |
| **When** | Immediately when detecting an error |
| **Human trigger** | "Log error: ..." |
| **AI trigger** | Exception, failed test, unexpected behavior |
| **What to include** | Symptoms, context, analysis, severity |
| **Lifecycle** | Active → In progress → Resolved (move to fixes-log) |

**Entry format:**
```markdown
### ERROR-XXX: Descriptive title

**Reported:** DD Month YYYY
**Severity:** High | Medium | Low
**Status:** Active | Investigating | In progress | Resolved

**Symptoms:**
What is observed, how the error manifests.

**Context:**
When it occurs, what triggers it, frequency.

**Analysis:**
Possible causes, hypotheses, investigation findings.

**Resolution:** (when resolved)
See fixes-log.md → FIX-XXX
```

---

#### fixes-log.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (when resolving an error) |
| **When** | After committing the fix |
| **Human trigger** | "Document fix for ERROR-XXX" |
| **AI trigger** | Commit that references an error |
| **What to include** | What was fixed, how, commit, files |
| **What NOT to include** | Full code (only relevant snippets) |

**Entry format:**
```markdown
### DD Month - Fix title

**Commit:** `abc1234`
**Resolves:** ERROR-XXX (if applicable)
**Files:** file1.py, file2.py

Description of what was fixed and how. Explain the root cause
and the implemented solution. If there is an impact on performance or
behavior, mention it.
```

---

#### migrations.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (when modifying schema/data) |
| **When** | When renaming fields, changing types, migrating data |
| **Human trigger** | "Document migration of field X" |
| **AI trigger** | Detect a schema change in models |
| **What to include** | Old field → new, migration script, affected version |
| **What NOT to include** | Changes that don't affect existing data |
| **Lifecycle** | Pending → Applied → Verified |

**Entry format:**
```markdown
### MIG-XXX: Migration title

**Date:** DD Month YYYY
**Version:** X.Y → X.Z
**Status:** Pending | Applied | Verified

**Change:**
Description of what changed in the schema or data.

**Migration:**
```python
# Script or steps to migrate existing data
```

**Rollback:**
How to revert if something fails (if applicable).

**Verification:**
How to confirm the migration was successful.
```

---

#### decisions.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human (important decisions) |
| **When** | When making a significant architecture/design decision |
| **Human trigger** | "Document decision: ..." |
| **AI trigger** | Suggest documenting when it detects an important decision |
| **What to include** | Context, options considered, decision, consequences |
| **Immutability** | Do NOT delete, mark as Deprecated/Replaced |

**Entry format:**
```markdown
## ADR-XXX: Decision title

**Date:** DD Month YYYY
**Status:** Proposed | Accepted | Deprecated | Replaced by ADR-YYY

**Context:**
Situation that motivated the decision. Problem to solve.

**Options considered:**
1. Option A - pros and cons
2. Option B - pros and cons

**Decision:**
What we decided to do and why we chose this option.

**Consequences:**
What this decision implies. Accepted trade-offs.
```

---

#### sketchbook.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (visualization of ideas) |
| **When** | When designing UI, flows, visual architecture |
| **Human trigger** | "Sketch: ..." |
| **AI trigger** | Create a diagram to explain a concept |
| **Visual format** | ASCII art, mermaid (if supported), descriptions |

**Entry format:**
```markdown
## Design name (DD Month)

**Purpose:** What this sketch is for.

```
┌─────────────────┐
│  ASCII diagram  │
│  of the concept │
└─────────────────┘
```

**Notes:** Additional explanation, alternatives, visual decisions.
```

---

#### manual.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human (structure) + AI (content) |
| **When** | When adding features, when releasing |
| **Audience** | End users, non-technical |
| **Structure** | Installation → Configuration → Daily use → Troubleshooting |
| **Style** | Step by step, with screenshots if possible |

**Mandatory sections:**
1. Installation/Requirements
2. Initial configuration
3. Common operations (with numbered steps)
4. Troubleshooting

---

#### documentation.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (technical documentation) |
| **When** | When creating/modifying models, APIs, important functions |
| **Audience** | Developers |
| **Structure** | Models → Methods → Cycles → Extension |
| **Style** | Technical, with example code |

**Suggested sections:**
1. Module architecture
2. Main models (fields, methods)
3. Cycles and flows (sequence diagrams)
4. API/Endpoints
5. Hooks and extension
6. Diagnosis/Debugging

---

#### glossary.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (when using an ambiguous term) |
| **When** | When introducing a new concept, when detecting term confusion |
| **Human trigger** | "Add to the glossary: ..." |
| **AI trigger** | Technical or domain term used without prior definition |
| **What to include** | Term, definition, usage example, synonyms if any |
| **Ordering** | Alphabetical |
| **Language** | per `_meta.json.lang` (this is a **domain** glossary) |

> This is the module's **domain** glossary, written in the deployment's `lang`. For the **Forest vocabulary** (Roots, Grove, Tree, modes, axes…) across languages, see the seed's `glossary/` — § "Language & glossary (i18n)".

**Entry format:**
```markdown
### term

**Definition:** What it is, in the context of this module.
**Example:** `field.binding_id` — reference to the MercadoLibre binding.
**Synonyms:** other names used for the same thing (if applicable).
**See also:** related terms.
```

---

#### prompts.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (after using a successful prompt) |
| **When** | When identifying a repetitive task that benefits from a prompt |
| **Trigger** | "Save this prompt as reusable" |
| **What to include** | Use, required context, exact prompt |
| **Test** | The prompt must have been tested and work |

**Entry format:**
```markdown
## PROMPT-XXX: Descriptive name

**Use:** In what situation to use this prompt.
**Required context:** What information the agent needs.
**Variables:** {variable1}, {variable2} (if any)

```
Prompt text here.
Use {variables} for parts that change.
```

**Usage example:**
Show a concrete example with variables replaced.
```

---

#### workflows.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human (defines) + AI (can execute) |
| **When** | When identifying a repetitive multi-step process |
| **Requirement** | Each step must be executable and verifiable |
| **What to include** | Trigger, steps, expected result, notes |

**Entry format:**
```markdown
## WF-XXX: Workflow name

**Trigger:** When/why to run this workflow.
**Expected result:** What is obtained on completion.
**Estimated time:** X minutes/hours.

### Steps

1. **Step name** — Description. Specific command or action.
2. **Next step** — Description. Success verification.
3. ...

### Verification

How to confirm the workflow completed correctly.

### Rollback

What to do if something fails (if applicable).
```

---

#### patterns.md

| Aspect | Protocol |
|---------|-----------|
| **Who writes** | Human or AI (when identifying a pattern) |
| **When** | When establishing a convention or detecting a repeated pattern |
| **What to include** | Correct example + anti-pattern |
| **Mandatory** | Include the reason for the pattern |

**Entry format:**
```markdown
## PAT-XXX: Pattern name

**Applies to:** Models | Views | Controllers | JS | CSS | Tests
**Reason:** Why we use this pattern.

### Correct example

```python
# Code to DO follow
```

### Anti-pattern

```python
# Code NOT to do and why
```

### Exceptions

When it is allowed not to follow this pattern (if applicable).
```

---

#### hooks/

Hooks are **executable protocols** that define what to do automatically on specific events. Each hook is a `.md` file that describes the steps to follow — it can be executed by an AI agent, by a script, or by a real hook of tools like Claude Code (`.claude/hooks/`).

##### session-start.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Load context at session start |
| **Executor** | AI agent or tool hook |
| **Mandatory** | Yes — without context, the agent works blind |

**Entry format:**
```markdown
# Hook: Session Start

> Development session start protocol.

## Steps

1. Check the seed version:
   - Read `.roots/roots_seed.md` (local copy, self-contained) → `**Version:**` field
   - Read the canonical (if accessible in the repo) → same field
   - If the local copy and canonical differ → trigger `hooks/on-seed-update.md` before continuing
   - If the version differs from the last one known by the agent's
     memory → re-read the full seed and apply the new conventions.
   - If `.roots/roots_seed.md` does NOT exist → copy the canonical with the
     distribution header (mandatory rule § "Seed distribution").
2. Read `context.md` — understand what the project is.
3. Read `journal/diary.md` — last 5 entries.
4. Read `journal/notes.md` — pending ideas and technical observations.
5. Read `tasks/todo.md` — pending backlog.
6. Read `tasks/tasks.md` — work in progress (if any, resume).
7. Read `debug/errors-log.md` — active unresolved errors.
8. List `workbench/` — if there are new or recent files, read or
   mention their existence to the human. They are reference materials.
9. Read `_meta.json` — `active_branch` and `current_feature`.
10. Verify git state:
    - `git branch --show-current`
    - `git log --oneline -10`
    - `git status`
11. If `_meta.json.active_branch` or `tasks/tasks.md` do not reflect the
    current branch → the `.roots/` is out of sync. Warn the human before
    making assumptions; don't decide blindly.
12. If there is an active feature, look for design docs in `docs/design-*.md` and
    read the relevant section before touching code.

## Expected output

Internal summary of: project state, pending tasks,
active errors, context of the last session, git state synced
with `.roots/`, reference materials available in workbench.
```

##### session-end.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Persist what was learned before closing the session |
| **Executor** | AI agent or tool hook |
| **Mandatory** | Yes — always update `.roots/` before closing; prevents loss of context |

**Entry format:**
```markdown
# Hook: Session End

> Session close protocol.

## Steps

1. Add an entry to `journal/diary.md` with a summary of the work
2. If there were new errors → add to `debug/errors-log.md`
3. If something was fixed → add to `debug/fixes-log.md`
4. If a task was completed → mark in `tasks/tasks.md`
5. If a pattern was identified → propose for `skills/patterns.md`
6. If there were commits → update `docs/commits.md`

## Expected output

`.roots/` files updated with the session's work.
```

##### on-error.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Document an error in a structured way when detected |
| **Trigger** | Exception, failed test, unexpected behavior |

**Entry format:**
```markdown
# Hook: On Error

> Protocol when detecting an error.

## Steps

1. Determine the next ID: review the last ERROR-XXX in errors-log.md
2. Add an entry with the standard format to `debug/errors-log.md`
3. If the error is critical → add to `tasks/tasks.md` as a task
4. If there is a cause hypothesis → document in the Analysis section

## Template

Use the ERROR-XXX format defined in the errors-log.md protocol.
```

##### on-fix.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Document the fix and close the error cycle |
| **Trigger** | Commit that resolves a known error |

**Entry format:**
```markdown
# Hook: On Fix

> Protocol when committing a fix.

## Steps

1. Add an entry to `debug/fixes-log.md` with the standard format
2. If it resolves an ERROR-XXX → update status to "Resolved" in errors-log.md
3. If the fix introduces a reusable pattern → propose for patterns.md
4. If the fix requires a data migration → add to migrations.md

## Template

Use the format defined in the fixes-log.md protocol.
```

##### on-seed-update.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Re-distribute the canonical seed to all the repo's local copies (`.roots/roots_seed.md`) when the canonical version changes |
| **Executor** | AI agent or human developer |
| **Trigger** | (a) The canonical seed version is bumped, (b) a `session-start` detects desync between the local copy and canonical, (c) a new `.roots/` is created and must be populated |
| **Mandatory** | Yes — without this the modules stop being self-contained and the seed stops being reprocessable locally |

**Entry format:**
```markdown
# Hook: On Seed Update

> Protocol when bumping the canonical seed or detecting desync with local copies.

## Steps

1. Identify the canonical (a single source of truth in the repo).
2. For each `.roots/` directory in the repo:
    - Write `<dir>/roots_seed.md` with the distribution header
      followed by the canonical's content.
3. Verify with `diff` (or equivalent) that all copies match
   in content (ignoring the distribution header).
4. Record the re-distribution in `journal/diary.md` or `docs/commits.md`.
5. If any `.roots/` had local modifications to the seed → preserve them
   as a footnote in the local copy before overwriting. Warn the
   human if there is a conflict.
6. **Language-lock (no noise):** this hook updates ONLY the `roots_seed.md` copy
   (canonical, English) — it does **NOT** touch, translate or rewrite any other
   file in the `.roots/`. Each deployment keeps writing in its `_meta.json.lang`.
   See § "Language & glossary (i18n)".

## Reference command (bash, tool-agnostic)

SEED="odoo_moldeo_roots/roots_seed.md"
find . -type d -name ".roots" -not -path "*/node_modules/*" | while read -r dir; do
    cp "$SEED" "$dir/roots_seed.md"
done

## Expected output

All `.roots/roots_seed.md` copies aligned with the canonical.
Each module is again self-contained and reprocessable in isolation.
```

##### on-task-done.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Properly close each individual task (not at the end of the session) keeping `.roots/` in sync |
| **Executor** | AI agent or human developer |
| **Trigger** | A task listed in `tasks/tasks.md` or `tasks/todo.md` is completed and is about to be reported to the human |
| **Mandatory** | Yes — avoids leaving the `.roots/` out of date between tasks of the same session |

**Entry format:**
```markdown
# Hook: On Task Done

> Protocol when completing a task, before reporting it to the human.

## Minimum steps (always)

1. `tasks/todo.md` — mark the task as `[x]` or move it to "Completed"
2. `tasks/tasks.md` — move the task from "In Progress" to "Recently Completed"
3. `docs/commits.md` — if there was a commit, add an entry with hash, motivation and changes

## Conditional steps

- If an error was found during the task → `debug/errors-log.md` (ERROR-XXX)
- If a fix was applied → `debug/fixes-log.md` (FIX-XXX)
- If an architectural decision was made → `design/decisions.md` (ADR-XXX)
- If an idea arose → `journal/notes.md`
- If a new domain term appears → `docs/glossary.md`
- If schema/data changed → `debug/migrations.md`

## Expected output

`.roots/` synced with the completed task BEFORE reporting to the human.
A human reading only `.roots/` should be able to reconstruct what was done and why.
```

##### on-topic-shift.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Ensure the agent does not work blind when the conversation pivots to a file/system not covered by the bootstrap |
| **Executor** | AI agent, developer or any code assistance tool |
| **Trigger** | A file, module or system not touched in the last steps appears in the conversation |
| **Mandatory** | Yes — avoids redundant questions and decisions without context |

**Entry format:**
```markdown
# Hook: On Topic Shift

> Protocol when shifting focus to a file/system not covered by the session bootstrap.

## Steps

1. List `.roots/docs/` (`ls` or equivalent).
2. Look for a doc with a name related to the new focus.
3. If it exists, read the relevant section BEFORE asking for clarification
   or proposing a design.
4. Review `.roots/journal/notes.md` and `.roots/design/decisions.md` for
   observations or ADRs about the same system.
5. Review `.roots/workbench/` for related reference materials.
6. Only ask the human what remains genuinely undocumented.
7. If on finishing the task you discover information that should have
   been in `.roots/docs/` but wasn't → add it or propose a
   new doc.

## Expected output

Context of the new system loaded before writing code or asking for
clarification. Questions to the human reduced to the undocumented.

## Compatibility

This protocol is tool-agnostic. It applies to any AI assistant
(Claude Code, Cursor, Copilot Workspace, Aider, etc.) or human
developer who picks up the repo.
```

##### on-seed-process.md

| Aspect | Protocol |
|---------|-----------|
| **Purpose** | Consolidate all the seed bootstrap/reprocessing steps into a single executable hook |
| **Executor** | AI agent or human developer |
| **Trigger** | (a) A new `.roots/` is initialized, (b) the seed version is bumped, (c) desync with upstream or canonical is detected, (d) the human explicitly asks to "process the seed" |
| **Mandatory** | Yes — it is the entry point for any operation on the seed |

**Entry format:**
```markdown
# Hook: On Seed Process

> Master protocol when processing/reprocessing the seed. Consolidates upstream
> sync, distribution, and CLAUDE.md verification.

## Steps

0. **Detect working mode (only on initial bootstrap):**
   - If `_meta.json` already exists and has `working_mode` → use that mode, don't ask
   - If `_meta.json` does not exist or has no `working_mode` → ask the user:
     - Client branch → ask for the context format (see § Context Format Registry),
       context data, and sources to link → create `.roots/{context}.{project}/`
     - Source → create `.roots/{module}/` directly
   - Persist the answer in `_meta.json.working_mode`, `context_format`, `context_parsed`
   - This step is NOT repeated in later sessions

0b. **Detect working language (language-lock — see § "Language & glossary (i18n)"):**
   - If `_meta.json.lang` exists → use it, do NOT ask, do NOT re-detect
   - Else if `.roots/` already has content → detect the dominant language of the
     existing `*.md` prose (`context.md`, `journal/`, `design/decisions.md`…) and
     **persist it** to `_meta.json.lang`. **Do NOT translate or rewrite any content.**
   - Else (brand-new `.roots/`) → default `"en"`; only ask if the user signals another language
   - **Hard rule:** this is a one-time stamp. From here on, all memory in this `.roots/`
     is written in `_meta.json.lang`. Code/technical identifiers stay English regardless.
   - This step is NOT repeated in later sessions

1. **Sync with the public upstream:**
   - Fetch `https://raw.githubusercontent.com/ctmil/roots_seed/main/roots_seed.md`
   - Compare the upstream version vs the local canonical version
   - If local < upstream → warn the human, propose applying changes
   - If local > upstream → evaluate whether there are generic improvements for a PR
   - If there is no access to the upstream → note in `journal/notes.md`, continue

2. **Verify the repo's canonical:**
   - Read `odoo_moldeo_roots/roots_seed.md` (or the configured canonical path)
   - Confirm the `**Version:**` field matches what is expected
   - If there are local un-bumped edits → warn the human

3. **Distribute to all copies:**
   - Run `hooks/on-seed-update.md`
   - Each `.roots/roots_seed.md` ends up aligned with the canonical
   - Verify with diff that no copies were left out of sync

4. **Link/sync sources (client mode only):**
   - If `_sources.json` exists → for each registered source:
     - Compare the embedded `sources/{source_id}/` vs the original source
     - If there is a diff → propose a sync to the human (don't merge blindly)
     - Update `last_sync` in `_sources.json`
   - If `_sources.json` does not exist and it is client mode → ask the human
     which sources to link, create `_sources.json` and `sources/` with copies
   - Respect `sync_include`/`sync_exclude` from the manifest

5. **Verify/create CLAUDE.md:**
   - If `CLAUDE.md` does not exist at the root → create it with the template
     defined in § "Integration with CLAUDE.md"
   - If it exists → verify that the list of modules with `.roots/`
     is up to date (add new ones, mark removed ones)
   - If `.claude/` exists → verify that its hooks reference
     `.roots/` without duplicating logic

6. **Verify workbench/:**
   - For each `.roots/{module}/` that has no `workbench/` → create it
   - Don't add content — it is the user's space

7. **Record:**
   - Add an entry in `journal/diary.md` or `docs/commits.md`
     documenting the seed processing, version, and actions taken

## Expected output

- Local canonical aligned (or with documented delta) with the upstream
- All `.roots/roots_seed.md` copies synced
- Embedded sources synced (client mode)
- `CLAUDE.md` updated with the module index
- `workbench/` folders existing in all modules
- Record of the processing in journal or commits
```

---

#### tasks.md and todo.md

| Aspect | tasks.md | todo.md |
|---------|----------|---------|
| **Content** | Active work | Backlog |
| **Item status** | In progress, Blocked | Pending |
| **Limit** | 3-5 tasks max | No limit |
| **Movement** | todo.md → tasks.md → Completed |

**tasks.md format:**
```markdown
## In Progress

### TASK-XXX: Title
**Assigned:** Name or "AI"
**Start:** DD Month
**Status:** In progress | Blocked by XXX

Brief description of the task.

- [ ] Subtask 1
- [x] Subtask 2 (completed)
```

**todo.md format:**
```markdown
## High Priority

- [ ] Important task 1
- [ ] Important task 2

## Medium Priority

- [ ] Normal task

## Ideas / Backlog

- [ ] Something we could do someday
```

---

## Use with AI Agents

### Instructions for the Agent

When starting a session in a project with `.roots/`:

```
1. READ context (follow hooks/session-start.md):
   - .roots/{module}/context.md (quick briefing)
   - .roots/{module}/journal/diary.md (last 5 entries)
   - .roots/{module}/tasks/todo.md
   - .roots/{module}/debug/errors-log.md (active errors)

2. DURING the work:
   - When finding an error: follow hooks/on-error.md → errors-log.md
   - When fixing something: follow hooks/on-fix.md → fixes-log.md
   - When having an improvement idea: ADD to notes.md
   - When making an important decision: ASK whether to document in decisions.md
   - When using a new domain term: ADD to glossary.md
   - When changing schema/fields: ADD to migrations.md

3. WHEN ENDING the session (follow hooks/session-end.md):
   - ADD an entry to diary.md summarizing the work
   - If there was a reusable pattern: PROPOSE adding it to patterns.md
   - If I created a useful prompt: PROPOSE adding it to prompts.md
   - If the project state changed: UPDATE context.md

4. NEVER:
   - Delete existing content without asking
   - Modify decisions.md (only add or mark deprecated)
   - Invent IDs that already exist (review the last number)
   - Ignore hooks/ — they are the standard protocol
```

### Automatic Triggers for AI

| Situation | Action |
|-----------|--------|
| Session start | → Run hooks/session-start.md |
| Exception in code | → Run hooks/on-error.md → errors-log.md |
| Commit with a fix | → Run hooks/on-fix.md → fixes-log.md |
| User says "version X.Y ready" | → Propose updating changelog.md |
| Code pattern repeated 3+ times | → Propose documenting in patterns.md |
| Complex explanation given | → Propose saving in documentation.md |
| Undefined domain term | → Propose adding to glossary.md |
| Schema/field change | → Propose adding to migrations.md |
| End of a long session | → Run hooks/session-end.md |
| Bootstrap or seed bump | → Run hooks/on-seed-process.md |
| New material in workbench/ | → Read/mention to the human |

---

## Initialization Script

```bash
#!/bin/bash
# init_roots.sh - Initializes the .roots structure for a module

MODULE_NAME=${1:-"module"}
BASE_PATH=".roots/$MODULE_NAME"
SEED_VERSION="1.7"

mkdir -p "$BASE_PATH"/{journal,debug,design,docs,tasks,hooks,skills,workbench}

# Meta — flat layout by default (v1.7). For namespaced (multi-module Source
# or Client branch) see "Working modes": change layout + add subdir.
cat > ".roots/_meta.json" << EOF
{
  "seed_version": "$SEED_VERSION",
  "created_at": "$(date -Iseconds)",
  "layout": "flat",
  "working_mode": "source",
  "project": "$MODULE_NAME",
  "modules": ["$MODULE_NAME"]
}
EOF

# Context
cat > "$BASE_PATH/context.md" << 'EOF'
# {MODULE} - Context

> Brief description of what the module does.

---

## Stack

- **Framework:** ...
- **Language:** ...
- **Database:** ...

## Current State

In development / production / maintenance.

## Key Conventions

- ...

## Critical Dependencies

- ...

---
EOF

# Journal
cat > "$BASE_PATH/journal/changelog.md" << 'EOF'
# {MODULE} - Changelog

> Version and change history.

---

*No releases yet*

---
EOF

cat > "$BASE_PATH/journal/diary.md" << 'EOF'
# {MODULE} - Development Diary

> Daily reflections on the development.

---

## $(date +%Y)

*Start documenting here*

---
EOF

cat > "$BASE_PATH/journal/notes.md" << 'EOF'
# {MODULE} - Notes

> Ideas and notes that could become features.

---

## Pending ideas

*Add ideas here*

---
EOF

# Debug
cat > "$BASE_PATH/debug/errors-log.md" << 'EOF'
# {MODULE} - Errors Log

> Log of errors found.

---

## Active Errors

*None currently*

---

## Resolved Errors

See [fixes-log.md](./fixes-log.md)

---
EOF

cat > "$BASE_PATH/debug/fixes-log.md" << 'EOF'
# {MODULE} - Fixes Log

> History of implemented fixes.

---

*No fixes documented yet*

---
EOF

cat > "$BASE_PATH/debug/migrations.md" << 'EOF'
# {MODULE} - Migrations

> Log of data, field and schema migrations.

---

*No migrations documented yet*

---
EOF

# Design
cat > "$BASE_PATH/design/decisions.md" << 'EOF'
# {MODULE} - Architecture Decisions

> Design and architecture decisions (ADRs).

---

*No decisions documented yet*

---
EOF

cat > "$BASE_PATH/design/sketchbook.md" << 'EOF'
# {MODULE} - Sketchbook

> Sketches, diagrams and visual ideas.

---

*No sketches yet*

---
EOF

# Docs
cat > "$BASE_PATH/docs/README.md" << 'EOF'
# {MODULE} - Documentation

> Documentation index.

---

## Documents

| File | Description |
|---------|-------------|
| [manual.md](./manual.md) | User manual |
| [documentation.md](./documentation.md) | Technical documentation |
| [architecture.md](./architecture.md) | System architecture |

---
EOF

touch "$BASE_PATH/docs/manual.md"
touch "$BASE_PATH/docs/documentation.md"
touch "$BASE_PATH/docs/architecture.md"

cat > "$BASE_PATH/docs/glossary.md" << 'EOF'
# {MODULE} - Glossary

> Domain terms and naming conventions.

---

*Add terms in alphabetical order*

---
EOF

# Tasks
cat > "$BASE_PATH/tasks/tasks.md" << 'EOF'
# {MODULE} - Tasks

> Tasks in progress.

---

## In Progress

*No active tasks*

---
EOF

cat > "$BASE_PATH/tasks/todo.md" << 'EOF'
# {MODULE} - TODO

> Backlog and pending tasks.

---

## High Priority

*No pending tasks*

---

## Medium Priority

---

## Ideas / Backlog

---
EOF

# Skills
cat > "$BASE_PATH/skills/prompts.md" << 'EOF'
# {MODULE} - Prompts

> Reusable prompts for frequent tasks.

---

*No prompts documented yet*

---
EOF

cat > "$BASE_PATH/skills/workflows.md" << 'EOF'
# {MODULE} - Workflows

> Common workflows.

---

*No workflows documented yet*

---
EOF

cat > "$BASE_PATH/skills/patterns.md" << 'EOF'
# {MODULE} - Patterns

> Code patterns and conventions.

---

*No patterns documented yet*

---
EOF

# Hooks
cat > "$BASE_PATH/hooks/session-start.md" << 'EOF'
# Hook: Session Start

> Development session start protocol.

---

## Steps

1. Read `context.md` — understand what the project is
2. Read `journal/diary.md` — last 5 entries
3. Read `tasks/todo.md` — pending backlog
4. Read `debug/errors-log.md` — active errors
5. If there is `tasks/tasks.md` with tasks in progress → resume

## Expected output

Internal summary of: project state, pending tasks,
active errors, context of the last session.

---
EOF

cat > "$BASE_PATH/hooks/session-end.md" << 'EOF'
# Hook: Session End

> Session close protocol.

---

## Steps

1. Add an entry to `journal/diary.md` with a summary of the work
2. If there were new errors → add to `debug/errors-log.md`
3. If something was fixed → add to `debug/fixes-log.md`
4. If a task was completed → mark in `tasks/tasks.md`
5. If a pattern was identified → propose for `skills/patterns.md`
6. If there were commits → update `docs/commits.md`
7. If the project state changed → update `context.md`

## Expected output

`.roots/` files updated with the session's work.

---
EOF

cat > "$BASE_PATH/hooks/on-error.md" << 'EOF'
# Hook: On Error

> Protocol when detecting an error.

---

## Steps

1. Determine the next ID: review the last ERROR-XXX in errors-log.md
2. Add an entry with the standard format to `debug/errors-log.md`
3. If the error is critical → add to `tasks/tasks.md` as a task
4. If there is a cause hypothesis → document in the Analysis section

## Template

Use the ERROR-XXX format defined in the errors-log.md protocol.

---
EOF

cat > "$BASE_PATH/hooks/on-fix.md" << 'EOF'
# Hook: On Fix

> Protocol when committing a fix.

---

## Steps

1. Add an entry to `debug/fixes-log.md` with the standard format
2. If it resolves an ERROR-XXX → update status to "Resolved" in errors-log.md
3. If the fix introduces a reusable pattern → propose for patterns.md
4. If the fix requires a data migration → add to migrations.md

## Template

Use the format defined in the fixes-log.md protocol.

---
EOF

# Replace placeholder
find "$BASE_PATH" -type f -name "*.md" -exec sed -i "s/{MODULE}/$MODULE_NAME/g" {} \;

echo "✓ Created .roots/$MODULE_NAME structure (seed v$SEED_VERSION)"
echo "  - context.md: module briefing"
echo "  - journal/: changelog, diary, notes"
echo "  - debug/: errors-log, fixes-log, migrations"
echo "  - design/: decisions, sketchbook"
echo "  - docs/: README, manual, documentation, architecture, glossary"
echo "  - tasks/: tasks, todo"
echo "  - skills/: prompts, workflows, patterns"
echo "  - workbench/: reference materials (empty)"
echo "  - hooks/: session-start, session-end, on-error, on-fix"
echo "  - _meta.json: initialization metadata"
```

---

## Best practices

1. **context.md is the front door** — The first thing any new agent or dev reads
2. **diary.md is short-term memory** — Update at the end of each session
3. **changelog.md is for clients** — No technical jargon, focused on benefits
4. **decisions.md is immutable** — Do not delete, only deprecate or replace
5. **errors-log.md is temporary** — Move to fixes-log.md when resolved
6. **notes.md is free** — Quick ideas, process weekly
7. **glossary.md avoids ambiguities** — Define domain terms only once
8. **migrations.md prevents data loss** — Document every schema change
9. **hooks/ are the standard protocol** — Following them guarantees consistency between sessions
10. **skills/ is module-specific** — Do not duplicate generic patterns
11. **patterns.md includes anti-patterns** — What NOT to do is equally important
12. **workflows.md must be executable** — Clear steps an agent can follow
13. **Keep IDs unique** — Review the last number before creating a new one
14. **Format consistency** — Follow the templates in this document
15. **_meta.json is automatic** — Don't edit it manually, it is for tools
16. **workbench/ is the user's** — The agent consults but does not invent content there; review at the start of each session
17. **Embedded sources are reference** — In client mode, `sources/` is a consultation copy; changes are made in the original source and synced
18. **Namespace avoids conflicts** — Use `source.skill_name` when two sources define the same concept
19. **Promotion is explicit** — The agent suggests, the user decides whether a client discovery goes up to the source
20. **Context format is parseable** — The `.roots/` directory name has semantic structure, it is not a free string

---
