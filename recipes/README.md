# Recipes by domain

> Applied patterns of the `.roots` / Forest model to concrete domains. Each recipe shows **how to structure `.roots`** for a real case. The spec lives in [`../roots_seed.md`](../roots_seed.md); the full manual in [`../manual.md`](../manual.md).

## The underlying idea: 3 primitives, N domains

Every recipe reuses the same three primitives of the model, plus the cross-cutting token layer:

| Primitive | What it is | Reused as… |
|---|---|---|
| **vendor** | authorship (ownership + optional profile `vendors/<slug>.md`) | who maintains a module · the artist · the script author |
| **`relations[]`** | directed graph `{from, to, type}` | `depends-on` between modules · prototype→layout · character→NPC, scene→scene |
| **branch** | fork with `stage`/`merged_into`/`created_by: human\|AI` | git branch · design variant (`folio.prototype.branch`) · script arc |
| *(cross-cutting)* **layer ladder** | read by layers, not everything | the token economy (recipe #4) measures and optimizes |

## Recipes

1. **[odoo-suite.md](./odoo-suite.md)** — Suite of Odoo extension modules (e.g. Meli). `Grove = suite · Tree = module · relations = depends`.
2. **[design-forest.md](./design-forest.md)** — Design forest (Folio/Lab): `1 vendor (artist) > N trees > designs`. Bridge `ai_context_md` ↔ `.roots`.
3. **[narrative-game.md](./narrative-game.md)** — Script + scenarios + RPG: sheets, lore, NPCs, arcs as branches, character skills ≡ AI skills.
4. **[token-economy.md](./token-economy.md)** — Token economy: layer ladder, formula (CER/FS), internal benchmarking and a repo of techniques per AI model.
