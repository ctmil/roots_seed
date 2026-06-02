# Receta — Narrativa, guión y juego (RPG / historias interactivas)

> Caso: usar `.roots` para **diseñar un juego basado en guión + escenarios** (o un libro/serie/historia ramificada). Documentos, lore, fichas de personajes, NPCs, escenarios, asociación de conceptos, y **bifurcación de guión y de lógica**. Se modela como **domain pack** sobre el seed estándar (`working_mode: narrative`) — reusa el esqueleto, agrega dominio.

## Por qué encaja sin inventar nada

Los mismos tres primitivos del Forest cubren la narrativa:
- **`relations[]`** = el **grafo narrativo y de conceptos** (personaje→aliado→NPC, escena→lleva-a→escena, ítem→desbloquea→puerta, concepto↔concepto estilo RPG).
- **branch** = **arco de guión / ruta**: una bifurcación de la historia *y de la lógica de código* es un branch con `branch_type: canon | what-if | playtest`, `merged_into`, `created_by: human|AI` (igual que `folio.prototype.branch`).
- **vendor** = autor/guionista (perfil con voz, tono, restricciones de canon).

Y tu intuición clave: **skill de IA ≡ skill de personaje**. Ambas son *definiciones de capacidad*. Una ficha de habilidades de un PJ es una entrada en `skills/` con mecánicas; un NPC es una persona+prompt en `skills/` (tools internas que definen su comportamiento).

## Estructura `.roots` (domain pack narrative)

```
.roots/                    (_meta.json → working_mode: "narrative")
├── context.md             ← premisa / logline + overview del mundo
├── worldbible/            ← la biblia del mundo
│   ├── lore/              · cosmología, facciones, historia, reglas del mundo
│   ├── characters/        · fichas PJ y NPC (una por archivo = "carta de entidad")
│   ├── scenarios/         · escenas / locaciones / encuentros
│   └── items/             · objetos, artefactos, mecánicas
├── arcs/                  ← ramas de guión = branches (canon | what-if | playtest)
├── design/decisions.md    ← ADRs de canon ("qué es canónico y por qué")
├── skills/                ← ⚡ skills de personaje (stats/traits/abilities) + personas-NPC + skills de IA
├── journal/               ← bitácora de escritura / playtests
└── relations.json         ← grafo narrativo {from, to, type}
```

## Ficha de entidad (template de "carta")

```markdown
---
id: npc-mara
kind: NPC            # PJ | NPC | escena | ítem | facción | concepto
arc: canon
---
# Mara, la cartógrafa
- **Rol:** guía del Acto I · **Facción:** Gremio de Mapas
- **Skills:** [[skill-leer-mapas]], [[skill-regateo]]   (→ skills/)
- **Relaciones:** aliada-de [[pj-protagonista]] · teme-a [[npc-el-vigia]]
- **Persona (IA):** ver [[skills/persona-mara]] (voz, motivaciones, qué nunca diría)
- **Lore:** [[lore/gremio-de-mapas]]
```

## El grafo (`relations.json`) — conceptos y trama

```jsonc
[
  { "from": "pj-protagonista", "to": "npc-mara",       "type": "allies" },
  { "from": "escena-puerto",   "to": "escena-mercado", "type": "leads-to" },
  { "from": "item-brujula",    "to": "escena-faro",    "type": "unlocks" },
  { "from": "concepto-deuda",  "to": "npc-el-vigia",   "type": "embodies" }
]
```
Tipos sugeridos: `allies` · `enemy` · `knows` · `leads-to` · `unlocks` · `requires` · `embodies` · `foreshadows`. Es el **mismo `relations[]`** que en código modela `depends-on`.

## Bifurcación de guión (= branch model)

```
arcs/
├── canon/            ← la línea oficial (branch_type: canon)
├── what-if/sin-mara/ ← ¿y si Mara muere en el Acto I? (variante, no mergeada)
└── playtest/ruta-b/  ← rama de prueba con jugadores (stage: testing)
```
Cada arco registra `merged_into` (qué se volvió canon) y `created_by`. **La bifurcación de lógica de código del juego viaja en el mismo branch** que la del guión: el arco contiene tanto el texto como los cambios de reglas/lógica que implica.

## Skills: personaje ↔ IA (el puente)

```
skills/
├── skill-leer-mapas.md     # mecánica de PJ: tirada, efecto, costo  (ficha de capacidad)
├── persona-mara.md         # NPC como prompt: voz, objetivos, límites (tool interna de comportamiento)
└── ai-techniques.md        # cómo el agente IA genera escenas/diálogos (técnicas de modelo)
```
Una "skill" es una **definición de capacidad** sin importar si la ejecuta un personaje (mecánica de juego) o el agente (cómo razona). El mismo formato `skills/` sirve para ambos.

## Mapeo Forest para un juego

| Forest | En el juego |
|---|---|
| **Roots** | el canon / memoria del mundo (`.roots`) |
| **Forest** | la IP / universo entero |
| **Grove** | una saga / temporada / facción |
| **Tree** | una historia, una línea de personaje, un módulo de campaña |
| **Branch** | un arco / ruta / final alternativo |

> El mismo motor que coordina repos de software coordina un universo narrativo: entidades como cartas, trama como grafo, rutas como branches, capacidades como skills.
