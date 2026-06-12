# Recipe — Design forest (creative platform)

> Real case: **Moldeo Folio + Lab** (moldeo.org) — a platform where each **artist/user** has repos with **custom designs** (layouts, prototypes, works). The goal: `1 vendor (artist) > N trees (repos) > designs`, with per-artist persistent memory that an AI agent can grow.

## The finding: Folio already models the forest in data

| Odoo model | Forest |
|---|---|
| `work_author` / `moldeo.portal.profile` / `res.partner` | **vendor** (artist) |
| `moldeo.folio.prototype` — *"Portfolio Prototype Repository"* (`repo_url`, `default_branch`, `repo_owner`, **`ai_context_md`**, `manifest_yaml`, `spec_yaml`) | **Tree** (a repo) |
| `moldeo.folio.prototype.branch` (`branch_type`, **`created_by: human\|AI`**, `commit_sha`, `stage`, `is_merged`, `merged_into`, `preview_url`) | **Branch** (design variant) |
| `moldeo.folio.layout` (+`layout.section`, `template_body`, `scss_custom`) · `moldeo.folio.work` | **designs** |

> A prototype's **`ai_context_md` field is an embedded `.roots/context.md`**: the bridge between the `.roots` pattern and the runtime data.

## Two planes (bridged)

**DEV plane** — `.roots` to *develop* folio/lab (source mode, Grove `moldeo`):
```
moldeo/  (Grove · vendor moldeo-interactive)
├── odoo_moldeo_folio/.roots/   ← layouts/prototypes/works system
└── odoo_moldeo_lab/.roots/       depends-on → folio, portal · public creative platform
```

**PRODUCT plane** — the forest of artists at runtime:
```
🌲 moldeo.org (Forest of artists)
└── 🎨 artist "ada" (vendor · profile = portal.profile / vendors/ada.md)
    ├── 🪵 prototype "neon-folio"  (Tree · ai_context_md ≡ .roots/context.md)
    │   ├── 🌿 branch main         (canon)
    │   ├── 🌿 branch ai/hero-v2   (created_by: AI · stage: preview · preview_url)
    │   └── 🌿 branch what-if/dark (design variant, unmerged)
    │   └── designs: layout "split-hero", work "obra-01", sketchbook…
    └── 🪵 prototype "vr-room-01"  (Tree)
```

## How `.roots` contributes here

1. **Per-artist-per-prototype memory:** the prototype's `ai_context_md` acts as `.roots/context.md` — the AI agent remembers the brief, the design decisions and the state between sessions, for each repo of each artist.
2. **Design fork = branch:** exploring a variant (a different hero, dark mode) is a `prototype.branch` with `created_by: AI`, `stage: preview`, and gets merged (`merged_into`) or discarded — just like a git branch, but for *design*.
3. **Vendor profile:** each artist has `vendors/<slug>.md` (their "own root"): style, palette, links, brand constraints — which the agent reads before generating.
4. **The Forest aggregates:** the platform lists artists (vendors) → prototypes (trees) → branches (variants) → layouts/works (designs). The same vocabulary that coordinates dev repos, now coordinating creators.

## Golden rule applied

A prototype **is** the artist's (vendor) and **uses** a base `layout` (a `depends-on`/`extends` edge). A variant does not "belong to two artists": it is a **branch** of the original prototype (with `created_by` and `merged_into`). The who-derives-from-whom graph is edges, not nesting.
