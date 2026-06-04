# Recetas de uso por dominio

> Patrones aplicados del modelo `.roots` / Forest a dominios concretos. Cada receta muestra **cómo estructurar `.roots`** para un caso real. El spec vive en [`../roots_seed.md`](../roots_seed.md); el manual completo en [`../manual.md`](../manual.md).

## La idea de fondo: 3 primitivos, N dominios

Todas las recetas reusan los mismos tres primitivos del modelo, más la capa transversal de tokens:

| Primitivo | Qué es | Se reusa como… |
|---|---|---|
| **vendor** | autoría (propiedad + perfil opcional `vendors/<slug>.md`) | quién mantiene un módulo · el artista · el autor del guión |
| **`relations[]`** | grafo dirigido `{from, to, type}` | `depends-on` entre módulos · prototype→layout · personaje→NPC, escena→escena |
| **branch** | bifurcación con `stage`/`merged_into`/`created_by: human\|AI` | branch git · variante de diseño (`folio.prototype.branch`) · arco de guión |
| *(transversal)* **escalera de capas** | leer por capas, no todo | la economía de tokens (receta #4) mide y optimiza |

## Recetas

1. **[odoo-suite.md](./odoo-suite.md)** — Suite de módulos de extensión Odoo (ej. Meli). `Grove = suite · Tree = módulo · relations = depends`.
2. **[design-forest.md](./design-forest.md)** — Bosque de diseños (Folio/Lab): `1 vendor (artista) > N trees > diseños`. Puente `ai_context_md` ↔ `.roots`.
3. **[narrative-game.md](./narrative-game.md)** — Guión + escenarios + RPG: fichas, lore, NPCs, arcos como branches, skills de personaje ≡ skills de IA.
4. **[token-economy.md](./token-economy.md)** — Economía de tokens: escalera de capas, fórmula (CER/FS), benchmarking interno y repo de técnicas por modelo de IA.
5. **[live-ai-game.md](./live-ai-game.md)** — Juego de rol vivo con backend IA (ej. Goblin Overlord): split canon/live (git vs Fly.io), wagons como commits, entity spines con LOD, subagentes Forest-aware, migración incremental en 4 fases.
