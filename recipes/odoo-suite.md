# Receta — Suite de módulos de extensión Odoo

> Caso real: la suite **Meli** (`meli_oerp*`) — un producto compuesto por un módulo core + módulos de extensión que dependen de él y de plataformas compartidas (OCAPI). Cómo estructurar `.roots` para esto.

## Mapeo al modelo Forest

- **Grove** = la suite (`meli`). Tiene `vendor` (moldeo-interactive) y `kind: producto-suite`.
- **Tree** = cada módulo-repo (`meli_oerp`, `meli_oerp_accounting`, …). Cada uno con su `.roots` en **modo source/flat**.
- **`relations[]`** = los `depends` reales de los manifests (verídicos, no inventados).
- Plataforma compartida (`odoo_connector_api`, OCAPI) = otro Grove con `kind: plataforma`; la suite **depende** de él vía aristas (no lo "contiene").

```
meli/  (Grove · vendor: moldeo-interactive · kind: producto-suite)
├── meli_oerp/.roots/              ← Tree core
├── meli_oerp_accounting/.roots/     depends-on → meli_oerp
├── meli_oerp_stock/.roots/          depends-on → meli_oerp
└── meli_oerp_multiple/.roots/       depends-on → meli_oerp, meli_oerp_stock,
                                                  meli_oerp_accounting, odoo_connector_api
```

## Qué pone cada módulo-Tree en su `.roots` (Odoo-específico)

| Archivo | Contenido para un módulo Odoo |
|---|---|
| `context.md` | Qué hace el módulo, **qué extiende** (`_inherit` de qué modelos), versión Odoo objetivo, en qué deployment vive. |
| `design/decisions.md` | ADRs Odoo: por qué `_inherit` vs `_inherits`, campos computados vs almacenados, herencia de vistas (`xpath`). |
| `docs/migration.md` | Cheatsheet de backport/forward-port **16 ↔ 17 ↔ 18 ↔ 19** (lo que cambia entre versiones de la API). |
| `debug/errors-log.md` · `fixes-log.md` | Gotchas de ORM, name-clashes, problemas de `depends`/orden de carga. |
| `docs/commits.md` | Bitácora de commits SOURCE por feature. |

## En `forest.json` (a nivel Forest)

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

## Regla de oro aplicada

`meli_oerp_multiple` **es** del Grove `meli` (membership único), y **usa** `odoo_connector_api` (arista `depends-on`). NO se taguea como Grove `ocapi` ni se anida bajo él — eso confundiría "es parte de" con "depende de". La plataforma OCAPI es un hub del que dependen módulos de varios Groves (Meli, Fulfillment, GeoEcon, Moldeo): por eso la dependencia es **arista**, no pertenencia.

## Montaje (toolkit)

```bash
./setup-module.sh meli_oerp git@github.com:ctmil/meli_oerp.git 16.0 17.0 18.0 19.0
```
Cada versión Odoo se monta como worktree/Branch hermano (bare+worktrees). El `.roots` del módulo puede usar **Modo Migración** (forkear temporalmente a `.roots/17.0/` + `.roots/19.0/`) durante un backport y colapsar de vuelta a flat.
