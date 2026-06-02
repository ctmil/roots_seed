# Roots Seed — Manual completo

> Manual de uso del sistema `.roots` / **Forest model**. Es la **puerta de entrada**: explica el porqué, el vocabulario, los modos, el registro y las recetas, y enlaza al spec ([`roots_seed.md`](roots_seed.md)) y a las recetas ([`recipes/`](recipes/)) en vez de duplicarlos.

**Versión del seed:** 1.10 · **Vocabulario:** Roots → Forest → Grove → Tree → Branch

---

## 1. Qué es y por qué

`.roots/` es **memoria persistente que vive con el código**. En vez de re-explicarle a cada agente (o a cada humano nuevo) qué hace el proyecto, las decisiones, los errores resueltos y las tareas en curso, todo eso se escribe en una estructura estable que **cualquier herramienta de IA o persona puede leer y crecer**. Pensado para **agentes de IA y desarrolladores por igual**.

Tres principios:
1. **Indexar y apuntar, no duplicar** — la memoria real vive donde corresponde; las capas superiores referencian.
2. **Self-contained** — cada `.roots/` lleva una copia del seed que lo generó (`roots_seed.md`), así es reprocesable aunque se extraiga a otro repo.
3. **Tool-agnostic** — el formato es Markdown + JSON; no depende de ningún asistente concreto.

## 2. Vocabulario Forest y los 3 primitivos

Cuando `.roots` coordina **muchos repos** (working_mode `workspace`):

| Término | Es |
|---|---|
| 🌱 **Roots** (`.roots`) | la capa de memoria |
| 🌲 **Forest** | el workspace entero (todos los repos) |
| 🌳 **Grove** | un producto / suite (cluster de Trees) |
| 🪵 **Tree** | un repo |
| 🌿 **Branch** | un git branch / worktree |

Y **tres primitivos que se reusan en todo dominio** (ver `recipes/`):
- **vendor** — autoría: propiedad de cada Tree (`vendor: <slug>`) con perfil opcional en `vendors/<slug>.md`.
- **`relations[]`** — grafo dirigido `{from, to, type}`: dependencias de código, vínculos de diseño, o trama narrativa.
- **branch** — bifurcación con `stage`/`merged_into`/`created_by: human|AI`: branch git, variante de diseño o arco de guión.

**Regla de oro:** `grove` = *qué es* · arista = *qué usa* · tag (`also_groves`) = *también es de*. Las dependencias son **aristas**, nunca anidamiento ni tags.

## 3. Estructura de un `.roots/`

```
.roots/
├── _meta.json        estado: working_mode, layout, versión seed, current_feature
├── roots_seed.md     copia local del seed (self-contained)
├── context.md        briefing de 30s (qué/stack/estado/convenciones)
├── journal/          changelog · diary · notes · benchmarks
├── tasks/            todo · tasks (trabajo activo)
├── debug/            errors-log · fixes-log · migrations
├── design/           decisions (ADRs) · sketchbook
├── docs/             architecture · glossary · manual · commits · design-*
├── hooks/            session-start/end · on-error/fix/task-done/topic-shift · on-seed-*
├── skills/           prompts · workflows · patterns (+ técnicas de IA, skills de personaje)
└── workbench/        material de referencia del usuario
```
Detalle de cada archivo y los estándares de poblado: [`roots_seed.md`](roots_seed.md).

## 4. Modos de trabajo

| Modo | Cuándo | Layout |
|---|---|---|
| **Flat** (default) | un repo, un proyecto | `.roots/` directo |
| **Source** | repo source multi-módulo | `.roots/{module}/` |
| **Client branch** | branch de cliente que embebe sources | `.roots/{context}.{project}/` |
| **Workspace** | un `.roots/` que coordina N repos (el Forest) | raíz + `forest.json` + `<grove>/` |
| **+ domain pack** | overlay de dominio (ej. `narrative`) sobre cualquiera de los anteriores | carpetas de dominio extra |

El modo se decide al procesar el seed y se persiste en `_meta.json`. Detalle y regla de decisión: [`roots_seed.md` → Modos de trabajo](roots_seed.md).

## 5. El registro `forest.json` (modo workspace)

Fuente de verdad estructurada del Forest. Trae:
- `vocabulary`, `groves[]` (id, kind, vendor), `vendors[]` (id, profile).
- `repos[]` = Trees, cada uno con ejes `grove` / `vendor` / `kind` / `org` (+ `role`/`worktrees`/`upstream` legacy).
- `relations[]` = el grafo de dependencias.

> Compat: si renombrás `fleet.json`→`forest.json`, dejá `fleet.json` como **symlink** para no romper el `fleet-dashboard` (lee `repos[]`). Schema completo: [`docs/forest-model.md`](docs/forest-model.md) (en el `.roots` del workspace).

## 6. Recetas por dominio

El modelo no es solo para Odoo. Ver [`recipes/`](recipes/):
1. **[Suite Odoo](recipes/odoo-suite.md)** — `Grove = suite · Tree = módulo · relations = depends` (Meli).
2. **[Bosque de diseños](recipes/design-forest.md)** — `1 vendor (artista) > N trees > diseños`; puente `ai_context_md` ↔ `.roots` (Folio/Lab).
3. **[Narrativa / juego](recipes/narrative-game.md)** — fichas, lore, NPCs, arcos como branches, skills de personaje ≡ skills de IA.
4. **[Economía de tokens](recipes/token-economy.md)** — escalera de capas, fórmula CER/FS, benchmarking, técnicas por modelo.

## 7. Economía de tokens (resumen)

Leer **por capas, no todo**: L0 índice → L1 slice activo → L2 doc de dominio → L3 corpus. Medir con **CER** (`útiles/cargados`) y **FS** (`si_leo_todo/cargados`), por **tier** de tarea (trivial/normal/deep/full). Registrar en `journal/benchmarks.md`, destilar técnicas en `skills/model-techniques.md`. Detalle: [`recipes/token-economy.md`](recipes/token-economy.md).

## 8. Toolkit (`scripts/` · `skills/` · `tools/`)

El `.roots` vive sobre un sustrato de repos; el seed se distribuye con herramientas que lo montan y visualizan:
- **`scripts/`** — `setup-module.sh`, `setupbranch.sh`, `dashboard.sh` (patrón **bare + worktrees**: un `.bare` por Tree, un worktree por Branch).
- **`skills/`** — biblioteca **compartida** de estrategias (merging de módulos Odoo, reporting md→PDF).
- **`tools/fleet-dashboard/`** — visor navegable que lee los `.roots` y mapea a un backend Odoo.

El formato `.roots/` **no depende** del toolkit: cualquier repo único lo usa sin él.

## 9. Ciclo de vida (hooks)

- **`session-start`** — leer `context.md` → `forest.md`/registro → `tasks/` → `journal/`; chequear versión del seed y git state.
- **`on-task-done`** — al cerrar cada tarea, actualizar `tasks/` + `docs/commits.md` (+ logs si aplica).
- **`on-topic-shift`** — al cambiar de foco, re-escanear `docs/` antes de pedir aclaraciones (sube de capa).
- **`on-error` / `on-fix`** — registrar en `debug/`.
- **`on-seed-update` / `on-seed-process`** — al bumpear el seed, re-distribuir la copia local; al procesar por primera vez, detectar modo.

## 10. Distribución y sync del seed

Cada `.roots/` lleva `roots_seed.md` (copia del canónico). El canónico de un workspace es `roots_seed/main/roots_seed.md`, espejo del upstream `github.com/ctmil/roots_seed`. Al bumpear versión, re-distribuir (on-seed-update). **Chequear siempre el upstream** antes de asumir la versión.

## 11. Quick start

```bash
# 1. Montar un repo como Tree (bare + worktrees)
./setup-module.sh mi_modulo git@github.com:org/mi_modulo.git 17.0

# 2. Bootstrap del .roots (modo Flat por default)
#    copiar roots_seed.md al .roots/ del repo y dejar que el agente lo procese
#    (detecta modo, crea context.md/_meta.json/estructura)

# 3. Si coordinás varios repos: armar forest.json a nivel workspace
#    (groves[] + vendors[] + repos[] con grove/vendor/kind + relations[])

# 4. Visualizar
./dashboard.sh
```

---

> Este manual es el índice navegable; el **spec normativo** es [`roots_seed.md`](roots_seed.md) y el **detalle por dominio** está en [`recipes/`](recipes/).
