# Recipe — Narrative, script and game (RPG / interactive stories)

> Case: using `.roots` to **design a game based on script + scenarios** (or a branching book/series/story). Documents, lore, character sheets, NPCs, scenarios, concept association, and **forking of script and of logic**. It is modeled as a **domain pack** over the standard seed (`working_mode: narrative`) — reuses the skeleton, adds domain.

## Why it fits without inventing anything

The same three Forest primitives cover narrative:
- **`relations[]`** = the **narrative and concept graph** (character→ally→NPC, scene→leads-to→scene, item→unlocks→door, concept↔concept RPG-style).
- **branch** = **script arc / route**: a fork of the story *and of the code logic* is a branch with `branch_type: canon | what-if | playtest`, `merged_into`, `created_by: human|AI` (just like `folio.prototype.branch`).
- **vendor** = author/scriptwriter (profile with voice, tone, canon constraints).

And your key intuition: **AI skill ≡ character skill**. Both are *capability definitions*. A PC's ability sheet is an entry in `skills/` with mechanics; an NPC is a person+prompt in `skills/` (internal tools that define its behavior).

## `.roots` structure (narrative domain pack)

```
.roots/                    (_meta.json → working_mode: "narrative")
├── context.md             ← premise / logline + world overview
├── worldbible/            ← the world bible
│   ├── lore/              · cosmology, factions, history, world rules
│   ├── characters/        · PC and NPC sheets (one per file = "entity card")
│   ├── scenarios/         · scenes / locations / encounters
│   └── items/             · objects, artifacts, mechanics
├── arcs/                  ← script branches = branches (canon | what-if | playtest)
├── design/decisions.md    ← canon ADRs ("what is canonical and why")
├── skills/                ← ⚡ character skills (stats/traits/abilities) + NPC-personas + AI skills
├── journal/               ← writing / playtest log
└── relations.json         ← narrative graph {from, to, type}
```

## Entity sheet ("card" template)

```markdown
---
id: npc-mara
kind: NPC            # PC | NPC | scene | item | faction | concept
arc: canon
---
# Mara, the cartographer
- **Role:** Act I guide · **Faction:** Map Guild
- **Skills:** [[skill-leer-mapas]], [[skill-regateo]]   (→ skills/)
- **Relations:** ally-of [[pj-protagonista]] · fears [[npc-el-vigia]]
- **Persona (AI):** see [[skills/persona-mara]] (voice, motivations, what it would never say)
- **Lore:** [[lore/gremio-de-mapas]]
```

## The graph (`relations.json`) — concepts and plot

```jsonc
[
  { "from": "pj-protagonista", "to": "npc-mara",       "type": "allies" },
  { "from": "escena-puerto",   "to": "escena-mercado", "type": "leads-to" },
  { "from": "item-brujula",    "to": "escena-faro",    "type": "unlocks" },
  { "from": "concepto-deuda",  "to": "npc-el-vigia",   "type": "embodies" }
]
```
Suggested types: `allies` · `enemy` · `knows` · `leads-to` · `unlocks` · `requires` · `embodies` · `foreshadows`. It is the **same `relations[]`** that in code models `depends-on`.

## Script forking (= branch model)

```
arcs/
├── canon/            ← the official line (branch_type: canon)
├── what-if/sin-mara/ ← what if Mara dies in Act I? (variant, not merged)
└── playtest/ruta-b/  ← test branch with players (stage: testing)
```
Each arc records `merged_into` (what became canon) and `created_by`. **The fork of the game's code logic travels in the same branch** as the script's: the arc contains both the text and the rule/logic changes it implies.

## Skills: character ↔ AI (the bridge)

```
skills/
├── skill-leer-mapas.md     # PC mechanic: roll, effect, cost  (capability sheet)
├── persona-mara.md         # NPC as prompt: voice, goals, limits (internal behavior tool)
└── ai-techniques.md        # how the AI agent generates scenes/dialogue (model techniques)
```
A "skill" is a **capability definition** regardless of whether it is executed by a character (game mechanic) or the agent (how it reasons). The same `skills/` format serves both.

## Forest mapping for a game

| Forest | In the game |
|---|---|
| **Roots** | the canon / world memory (`.roots`) |
| **Forest** | the IP / entire universe |
| **Grove** | a saga / season / faction |
| **Tree** | a story, a character line, a campaign module |
| **Branch** | an arc / route / alternate ending |

> The same engine that coordinates software repos coordinates a narrative universe: entities as cards, plot as graph, routes as branches, capabilities as skills.
