# Receta — Juego de rol vivo con backend IA (live-ai-game)

> Caso real: **Goblin Overlord** — RPG dark-fantasy por turnos donde Claude es el DM. Backend FastAPI en Fly.io, frontend SvelteKit PWA. El jugador escribe una acción; el backend ensambla el contexto correcto, Claude narra y elige efectos vía tools (~50 acciones), el estado se persiste en el volumen Fly. Hoy no usa git. Esta receta documenta **por qué vale la pena adoptarlo** y cómo hacerlo **sin romper nada**.

---

## Por qué `.roots` + git agregan valor real aquí

Si el juego **funciona y crece**, estos son los problemas que aparecen sin versionado — y que git + `.roots` resuelven antes de que duelan:

| Problema que aparece al crecer | Sin git | Con git + `.roots` |
|---|---|---|
| **Un NPC se comporta distinto de como era hace 3 semanas** | No hay forma de saber qué cambió | `git log -- worldbible/characters/fang.md` muestra cada evolución |
| **Quiero explorar "¿y si Elver muere en el Acto II?"** | Hay que editar los archivos y rezar | Branch `what-if/elver-muerte` — probás, descartás o mergeás al canon |
| **El DM empieza a contradecirse sobre el lore de los Sabertooth** | Solo el transcript (crudo) guarda la historia | `journal/spine/` tiene wagons sellados y revisables; ADRs de canon en `design/decisions.md` |
| **Quiero hacer un segundo juego / un segundo mundo** | Copiar archivos a mano y perder el hilo | Grove nuevo, Tree nuevo, el `.roots` viaja — todo el toolkit reutilizable |
| **Un agente nuevo empieza una sesión y no sabe nada del mundo** | Hay que releer transcript.jsonl entero | `session-start` lee L0 (`context.md` + `spine.md`) en segundos; L2 on-demand |
| **Quiero que un subagente revise la coherencia del lore** | El agente tiene que leer archivos raw sin estructura | El subagente `lore-keeper` lee `worldbible/` estructurada y `relations.json` |
| **El Fly volume se corrompe o se pierde** | Pérdida total del canon | Canon trackeado en git; solo `current_state.json` (live) está solo en Fly |

**La regla de oro:** Fly.io es excelente para estado *vivo* (lo que cambia cada turno). Git es excelente para *canon* (lo que define el mundo y vale la pena preservar). **No son competidores — son complementarios.**

---

## Mapeo al modelo Forest

```
SPINE (campaña entera)        →  Grove   (el universo / la IP del juego)
WAGON (capítulo / arco)       →  Tree    (un arco como unidad versionable)
BEAT (un turno narrado)       →  commit  (granularidad fina del canon)
ENTITY SPINE (NPC/facción)    →  carta de entidad en worldbible/characters/
what-if / playtest route      →  branch  git (ruta alternativa, mergeable)
DM-only (plot machinery)      →  dm-only/ (privado, en repo separado o rama)
current_state.json (live)     →  NO en git — queda solo en Fly volume
transcript.jsonl (beats raw)  →  NO en git — log crudo de Fly, no canon
```

El "cross TIME×DEPTH" del Selector **es** la escalera de capas L0→L3 de `token-economy.md`, implementada como lógica viva en el backend. La receta se apoya en ese mapeo directo.

### `working_mode` para este dominio

```
"working_mode": "narrative-live"
```

Extensión de `narrative` (ver `narrative-game.md`) que agrega la distinción **canon/live** y el concepto de wagon como unidad de commit. El resto del modelo Forest aplica sin cambios.

---

## Qué va a git y qué se queda en Fly

```
FLY VOLUME (efímero, live)          GIT + .roots (canon, versionado)
─────────────────────────           ─────────────────────────────────
current_state.json                  worldbible/characters/*.md
  HP, MP, XP, skills                worldbible/lore/*.md
  scene, calendar                   worldbible/dm-only/*.md
  corrections (law)                 spine/ (wagons sellados)
                                    relations.json (grafo narrativo)
transcript.jsonl                    design/decisions.md (ADRs de canon)
  raw beats                         journal/benchmarks.md
  replayed on connect               skills/ (agentes del juego)
```

**Regla de clasificación:** ¿cambia cada turno? → Fly. ¿Define el mundo? → git.

---

## Estructura `.roots` (domain pack narrative-live)

```
goblin-overlord-world/         ← repo del mundo (canon)
├── .roots/
│   ├── _meta.json             (working_mode: "narrative-live", seed_version: "1.12")
│   ├── context.md             ← logline + overview del mundo (L0 — siempre cargado)
│   ├── journal/
│   │   ├── spine.md           ← índice de wagons sellados (L0 — el "tren de la historia")
│   │   ├── benchmarks.md      ← CER/FS por sesión (¿qué cargó el selector y cuánto usó?)
│   │   └── diary.md           ← notas de diseño entre sesiones
│   ├── design/
│   │   └── decisions.md       ← ADRs de canon ("Mara es aliada, no NPC hostil — por qué")
│   ├── worldbible/
│   │   ├── characters/        ← entity spines (una carta por NPC/PJ/facción)
│   │   │   ├── elver.md       (PJ protagonista)
│   │   │   ├── fang.md        (NPC — Torondor, Saber-Tooth commander)
│   │   │   └── _index.md      (índice barato — L0)
│   │   ├── lore/              ← world-clock, geografía, facciones, crónica, reglas
│   │   │   ├── species.md
│   │   │   ├── factions.md
│   │   │   └── chronicle.md
│   │   └── dm-only/           ← plot machinery (foreshadowing, agendas ocultas)
│   │       ├── world-clock.md
│   │       └── seeds.md       ← "semillas" de futuros arcos
│   ├── spine/                 ← wagons sellados (historia canónica por capítulo)
│   │   ├── wagon-01-ironfang-parley.md
│   │   ├── wagon-02-dragon-flight.md
│   │   └── wagon-06-atarakua-combat.md   ← el más reciente
│   ├── arcs/                  ← ramas de guión (what-if, playtest)
│   │   └── what-if/
│   ├── relations.json         ← grafo narrativo {from, to, type}
│   └── agents/                ← subagentes del juego (lore-keeper, dm-assistant, etc.)
│       ├── lore-keeper.md
│       └── world-builder.md
└── forest.json                ← si hay múltiples mundos / IP (Grove por universo)
```

---

## Carta de entidad (entity spine como `.roots`)

Cada NPC/facción/lugar de importancia tiene su propia carta. El **header** es L0 (siempre cargado); el **deep card** es L1 (cargado si el personaje está en escena); **verbatim** es L2 (drill on-demand).

```markdown
---
id: npc-fang
kind: NPC
faction: saber-tooth-horde
arc: canon
lod: header        ← esta sección siempre cargada (~37 tok)
---
# Fang · Torondor, Saber-Tooth Commander

**Stats:** STR 18 · DEX 12 · leal al overlord hasta la muerte
**Voz:** lacónico, amenazante, nunca promete lo que no puede cumplir
**No haría jamás:** traicionar a Elver en público · mentir sobre su rango
**Relaciones:** [[elver]] (señor) · [[castlecave]] (hogar) · [[wolves-nine-wives]] (guardia personal)

---
lod: deep-card     ← cargado si Fang está en escena (~980 tok)
---

## Pasado reciente
- **Wagon 3, escena 2:** primera traición detectada en las filas — Fang la aplastó sin avisar a Elver.
- **Wagon 5:** recibió el escudo de los Atarakua como botín — lo usa como mesa de trabajo.

## Proyección (tentativa — nunca canon hasta que ocurra)
→ Tiene lealtades divididas con la facción Wolftooth que aún no reveló.
→ Cruce inevitable con [[npc-torondor-heir]] antes del arco 8.
```

> El campo `ai_context_md` de un prototype en Folio/Lab (ver `design-forest.md`) **es exactamente esto**: un context embebido por entidad. El mismo patrón, mismo propósito.

---

## Wagon sellado (unidad de commit)

Cuando el backend llama a `seal_scene` (el wagon cierra), el agente genera un **resumen canónico** del wagon y hace commit:

```bash
git add spine/wagon-06-atarakua-combat.md
git add worldbible/characters/fang.md   # si evolucionó en este wagon
git commit -m "canon: wagon-06 Atarakua combat sellado

Elver derrota al campeón Atarakua. Fang pierde el escudo (lo recupera en wagon-07).
Nuevo ADR: los Atarakua pasan a facción 'neutral-tensa' (ver decisions.md)."
git tag wagon-06-sealed
```

Esto da **tres cosas gratis**:
1. `git log --oneline` = tabla de contenidos navegable de la campaña.
2. `git show wagon-04-sealed:worldbible/characters/fang.md` = Fang tal como era en el wagon 4.
3. `git diff wagon-04-sealed wagon-06-sealed -- worldbible/` = qué evolucionó en el mundo entre capítulos.

---

## Grafo narrativo (`relations.json`)

El mismo `relations[]` del Forest Model, aplicado a entidades del juego:

```jsonc
[
  { "from": "elver",          "to": "fang",            "type": "commands" },
  { "from": "fang",           "to": "castlecave",      "type": "defends" },
  { "from": "wagon-05",       "to": "wagon-06",        "type": "leads-to" },
  { "from": "item-atarakua-shield", "to": "escena-faro", "type": "unlocks" },
  { "from": "faccion-wolftooth",    "to": "npc-fang",  "type": "pressures" },
  { "from": "concepto-deuda-sangre","to": "arco-canon-8", "type": "foreshadows" }
]
```

El `forest-dashboard` puede leer este `relations.json` y renderizar el grafo del mundo — mismo SVG que el arc-diagram de módulos Odoo, ahora como mapa narrativo.

---

## Subagentes del juego (biblioteca on-demand)

Siguiendo el patrón v1.12 (store en `.roots/agents/`, activar en `.claude/`):

| Agente | Para | Modelo |
|---|---|---|
| `lore-keeper` | verificar coherencia del worldbible antes de un wagon nuevo | opus |
| `world-builder` | diseñar nuevas facciones/locaciones con consistencia interna | opus |
| `dm-assistant` | revisar un draft de narración antes de enviarlo al jugador | sonnet |
| `arc-planner` | planificar el arco siguiente a partir del estado actual del canon | sonnet |

Todos son **Forest-aware**: leen `context.md` + `spine.md` (L0) y hacen drill en `worldbible/` solo si hace falta (L2 on-demand). Encaja con el modelo TOKEN de tres dials del selector: card-depth × time-resolution × model.

---

## Migración incremental — 4 fases sin romper nada

### Fase 0 — Espejo pasivo (1 día de trabajo)

El backend de Fly sigue operando exactamente igual. Se agrega un script `sync-canon.sh` que corre al terminar cada sesión (o manualmente):

```bash
#!/bin/bash
# sync-canon.sh — copia los archivos canon del Fly volume al repo git
rsync -av --exclude "current_state.json" --exclude "transcript.jsonl" \
  /data/world/ ./world-canon/
git add world-canon/
git commit -m "sync: sesion $(date +%Y-%m-%d)"
git push
```

**El creador gana desde el día 1:** backup real, historial de cómo evolucionó el lore, posibilidad de `git diff` entre sesiones. Zero cambios al backend.

### Fase 1 — Estructura `.roots` en el repo (1 semana)

Reorganizar los archivos copiados en la estructura `worldbible/` + `spine/` descripta arriba. Crear `_meta.json` con `working_mode: narrative-live`. Empezar a llenar `context.md` (el L0 del mundo).

El Selector del backend ahora puede leer desde el repo en lugar del volumen para los archivos canon — o seguir leyendo del volumen mientras se estabiliza la estructura.

### Fase 2 — Wagons como commits con tag (cuando se quiera)

Modificar el tool `seal_scene` del backend para que, además de cerrar el wagon en el volumen, haga `git commit` + `git tag wagon-N-sealed` en el repo. El transcript.jsonl sigue en el volumen; el resumen canónico va al repo.

El creador gana: `git log` como tabla de contenidos, capacidad de volver a cualquier wagon, `git diff` entre capítulos.

### Fase 3 — What-if branches y mundos múltiples (cuando el juego crezca)

Cuando quiera explorar rutas alternativas: `git checkout -b what-if/sin-mara`. El backend puede apuntar a ese branch para una sesión de prueba. Si resulta canon, se mergea; si no, se archiva.

Cuando quiera hacer un segundo mundo / segunda IP: nuevo Grove en `forest.json`, nuevo Tree (repo). Todo el toolkit (subagentes, skills, scripts) se reutiliza sin cambios.

---

## El loop completo con `.roots` activo

```
[turno del jugador]
       ↓
  SELECTOR (backend)
  lee cross TIME×DEPTH
  = escalera L0→L3 de .roots
       ↓
  WORLD NOW (briefing)
  L0: context.md + spine.md + _index.md de characters
  L1: deep card de NPCs en escena + wagon actual
  L2: drill on-demand (lore específico, dm-only si hace falta)
       ↓
  Claude — el DM
  narra + elige tools
       ↓
  tools (~50 acciones)
  roll · advance_time · npc_damage · award_xp
  update_scene · seal_scene → git commit + tag
       ↓
  WRITE al mundo
  Fly: current_state.json (live)
  git:  worldbible/ + spine/ (canon)
```

**La plomería ES el concepto** — igual que los diagramas del juego lo dicen: el backend READ = la escalera de capas; el WRITE = el commit al canon. `.roots` no agrega una capa burocrática — **formaliza lo que el juego ya hace**, y lo hace versionado, navegable y reutilizable.
