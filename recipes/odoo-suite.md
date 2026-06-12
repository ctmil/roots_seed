# Recipe — Suite of Odoo extension modules

> Real case: the **Meli** suite (`meli_oerp*`) — a product made up of a core module + extension modules that depend on it and on shared platforms (OCAPI). How to structure `.roots` for this.

## Mapping to the Forest model

- **Grove** = the suite (`meli`). It has a `vendor` (moldeo-interactive) and `kind: producto-suite`.
- **Tree** = each module-repo (`meli_oerp`, `meli_oerp_accounting`, …). Each one with its `.roots` in **source/flat mode**.
- **`relations[]`** = the real `depends` from the manifests (truthful, not invented).
- Shared platform (`odoo_connector_api`, OCAPI) = another Grove with `kind: plataforma`; the suite **depends** on it via edges (it does not "contain" it).

```
meli/  (Grove · vendor: moldeo-interactive · kind: producto-suite)
├── meli_oerp/.roots/              ← Tree core
├── meli_oerp_accounting/.roots/     depends-on → meli_oerp
├── meli_oerp_stock/.roots/          depends-on → meli_oerp
└── meli_oerp_multiple/.roots/       depends-on → meli_oerp, meli_oerp_stock,
                                                  meli_oerp_accounting, odoo_connector_api
```

## What each module-Tree puts in its `.roots` (Odoo-specific)

| File | Content for an Odoo module |
|---|---|
| `context.md` | What the module does, **what it extends** (`_inherit` of which models), target Odoo version, which deployment it lives in. |
| `design/decisions.md` | Odoo ADRs: why `_inherit` vs `_inherits`, computed vs stored fields, view inheritance (`xpath`). |
| `docs/migration.md` | Backport/forward-port cheatsheet **16 ↔ 17 ↔ 18 ↔ 19** (what changes between API versions). |
| `debug/errors-log.md` · `fixes-log.md` | ORM gotchas, name-clashes, `depends`/load-order issues. |
| `docs/commits.md` | SOURCE commit log per feature. |

## In `forest.json` (at the Forest level)

```jsonc
{
  "groves": [ { "id": "meli", "kind": "producto-suite", "vendor": "moldeo-interactive" } ],
  "repos": [
    { "name": "meli_oerp",            "grove": "meli", "kind": "producto-suite", "role": "source" },
    { "name": "meli_oerp_multiple",   "grove": "meli", "kind": "producto-suite", "role": "source" }
  ],
  "relations": [
    { "from": "meli_oerp_accounting", "to": "meli_oerp",          "type": "depends-on" },
    { "from": "meli_oerp_multiple",   "to": "odoo_connector_api", "type": "depends-on" }
  ]
}
```

## Golden rule applied

`meli_oerp_multiple` **is** part of the `meli` Grove (single membership), and **uses** `odoo_connector_api` (a `depends-on` edge). It is NOT tagged as Grove `ocapi` nor nested under it — that would conflate "is part of" with "depends on". The OCAPI platform is a hub depended on by modules of several Groves (Meli, Fulfillment, GeoEcon, Moldeo): that's why the dependency is an **edge**, not membership.

## Setup (toolkit)

```bash
./setup-module.sh meli_oerp git@github.com:ctmil/meli_oerp.git 16.0 17.0 18.0 19.0
```
Each Odoo version is mounted as a sibling worktree/Branch (bare+worktrees). The module's `.roots` can use **Migration Mode** (temporarily forking to `.roots/17.0/` + `.roots/19.0/`) during a backport and collapse back to flat.
