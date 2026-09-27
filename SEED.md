# SEED — The Biomimetic Manifesto of Roots

**Version:** 0.1 · 27 September 2026 · canonical (English) · translations: [`SEED.es.md`](SEED.es.md) · `SEED.fr.md` (pending)
**Author:** Fabricio Costa Alisedo (Moldeo Interactive) — harmonized with the implemented vocabulary by the Roots agents.

> `SEED.md` holds **what must remain recognizable** — purpose, principles, invariants.
> [`roots_seed.md`](roots_seed.md) holds **how** — the operational spec. When the two disagree, the spec is wrong or the Seed must change *consciously*: the Seed is historical, not immutable.

---

## 1. Purpose of the Seed

The Seed preserves the **generative identity** of Roots.

It is not only a functional description of a product. It holds the principles that must stay recognizable even when implementations, versions, modules or deployment contexts change.

The Seed defines:

- purpose;
- principles;
- invariants;
- a way of understanding **growth**;
- a way of understanding **memory**;
- a way of understanding **circulation**;
- a way of understanding **participation**;
- a way of understanding **governance**;
- the relationship between **diversity, evolution and continuity**.

Roots understands projects as organisms that grow, accumulate memory, receive signals from their environment, transform, and live inside larger ecosystems.

## 2. Biomimetic design

Roots adopts a **biomimetic** design approach.

Its correspondences with trees, forests, seeds, roots, wood, rings, cambium, branches, leaves, flowers, fruits, rays, mycelium, circulation and regeneration do not attempt to reproduce biology literally. They are abstractions of strategies observable in living systems and real ecosystems, translated into design rules for technological, social and organizational systems.

**Roots does not copy nature. It learns from its strategies.**

Observed, inspiring principles: diversity · memory · adaptation · circulation · regeneration · reserve · cooperation · resilience · limits to growth · decentralization · transformation.

Cases such as the Irati forest serve as concrete references for thinking how production, conservation, governance and regeneration can coexist within the same territory.

> ### Central biomimetic principle
> **GROW WITHOUT DESTROYING THE CAPACITY TO GROW AGAIN.**

The analogy is **not point-to-point**. A term enters the model only when it names something that exists (or must exist) and would otherwise stay unnamed.

## 3. Conceptual anatomy — two scales

Every term lives at **one** scale. Using the same word at both scales is how a vocabulary stops meaning anything.

### 3.1 Ecosystem scale — the organs of the Forest

| Organ | Is | Implemented by |
|---|---|---|
| **Seed** | Generative identity: purpose, principles, invariants — the genome that propagates | `roots_seed` (this repo) |
| **Forest** | The ecosystem that **perceives**: the organisms it observes, their health, their signals | `odoo_moldeo_htree` (+ the modules it connects) |
| **Micielo** (mycelium) | The network **between** Trees: agents and connections that carry learning from one organism to another | `odoo_moldeo_roots` |
| **Flores** (flowers) | The **reproductive** organ: propagates growth between Trees (pollination, grafting, planting the Seed) **and** exposes possibilities to the community for participation | `odoo_moldeo_sync` (+ its public proposal layer, to be built) |
| **Folio** (leaves) | The surface of daily exchange with the outside: what the organism shows and what comes back | `odoo_moldeo_folio` |

### 3.2 Tree scale — the anatomy of one organism

A **Tree** is a unit of **product identity** with its own history — usually one repository. It can cross many technological generations and remain the same organism.

| Part | Is |
|---|---|
| **Roots** | The Tree's persistent **memory** (`.roots/`): decisions, errors, learnings, context |
| **Soil** | The concrete environment where an installation lives: organization, culture, market, infrastructure, constraints, needs |
| **Trunk** | Consolidated, persistent structure — *what the Tree has learned to be* |
| **Grain** | The principles and decisions that shape the internal engineering |
| **Rings** | Historical memory: *how the organism came to be what it is* — consolidated episodes, not copies of code |
| **Cambium** | The zone of active growth, where a signal can become new structure — and where it is **decided** whether it does |
| **Rays** | Radial circulation **inside** the Tree: between periphery, memory and growth zones, in both directions |
| **Branches** | Living lines of growth — a git branch, a generation (Odoo 13, 17, 19…) |
| **Buds · Features · Fruits** | A candidate capability · a capability that grew · mature, usable value (a release) |
| **Wounds · Scars** | An open disturbance (incident, breaking change) · its healed, recorded memory |
| **Grafts** | Growth taken from another Tree or generation and adapted to the receiver |

## 4. Memory and circulation

Roots distinguishes **memory** from **circulation**.

**Memory** is what remains: git, decisions, documentation, relations, historical tickets, versions, features, rings, learnings — and the database, as part of that memory.

**Circulation** is what is happening: events, queries, agents, votes, messages, active tickets, synchronizations, processes, interpretations, transformations.

**The database is not the living organism. It is part of its memory.** Roots becomes alive when that memory is traversed, related to the present, and produces transformation.

> *Git preserves what happened. Roots interprets what it meant. The database coordinates what is happening now.*

Basic cycle:

```
PERCEIVE → CIRCULATE → RELATE TO MEMORY → INTERPRET → DELIBERATE
         → DECIDE → TRANSFORM → RETURN TO THE ENVIRONMENT → KEEP THE LEARNING
```

## 5. Signals, rays and features

Tickets are not rays. **Tickets are signals that circulate.** A ticket may carry a need, a failure, an observation, an adaptation, a proposal or a local experience. Rays are the mechanism that lets those signals travel from the periphery inward, meet prior memory, and eventually modify growth.

```
NEED / TICKET / USE / ERROR → SIGNAL → RAYS → MEMORY + CONTEXT → EVALUATION
    → CAMBIUM → BUD → FEATURE → BRANCH → FRUIT → NEW RING
```

Not every ticket becomes a feature. Not every local adaptation should become common structure.

## 6. Flowers, participation and practical democracy

Flowers are not features. **A flower is the interface through which a possibility of the organism becomes visible and seeks interaction with its environment**: a proposal, a candidate feature, an improvement, a direction, an open question.

The community can vote, rate, comment, argue, prioritize and add context. **A vote does not guarantee the fruit.** The signal returns to the organism and mixes with memory, constraints, compatibility, regeneration capacity, strategy and other experiences. **The final decision remains human.**

> **DEMOCRACY BECOMES PRACTICAL WHEN ITS EFFECTS ARE VISIBLE AND TRACEABLE WITHIN THE LIFE CYCLE OF THE ECOSYSTEM.**

Participating is not only giving an opinion. It gains meaning when a person can follow the path of their intervention:

```
PROPOSAL → EXPOSURE → PARTICIPATION → DELIBERATION → DECISION
         → DEVELOPMENT → RESULT → RETURN TO THE ECOSYSTEM
```

Roots seeks to move from a platonic, idealist democracy to an **ecosystemic democratic pragmatism**: everyday participation must let people see *what* changed, *how*, and *why*.

## 7. Collective intelligence

Collective intelligence is neither a sum of opinions nor an average. Diversity produces knowledge only under certain conditions: initial autonomy of perception · plurality · context · arguments · memory · evidence · visible relations · deliberation · explicit uncertainty.

Three moments:

- **Perceive** — express a first reading from one's own experience.
- **Deliberate** — enter into relation with other perspectives, arguments, data, precedents and scenarios.
- **Decide** — take a conscious direction after widening the understanding of the system.

The goal is not to avoid debate. It is to avoid consensus appearing **before there is enough diversity to produce collective knowledge**.

> **DEBATING DOES NOT ERASE DIVERSITY. IT PUTS IT INTO RELATION.**
> **COLLECTIVE INTELLIGENCE DOES NOT REPLACE COLLECTIVE DECISION. IT INFORMS IT.**
> **ROOTS DOES NOT SEEK TO ELIMINATE DIVERSITY TO PRODUCE CONSENSUS. IT SEEKS TO PRESERVE ENOUGH DIVERSITY FOR THE ECOSYSTEM TO UNDERSTAND ITSELF.**

Minority positions are part of the memory too. An alternative discarded today may become relevant in another context.

## 8. Governance

Governance is not only control. In Roots it means how the capacity to decide, responsibility, memory, care and the ability to intervene in the system's evolution are **distributed**.

> **GOVERNING AN ECOSYSTEM IS NOT CONTROLLING ITS GROWTH. IT IS CARING FOR THE CONDITIONS THAT LET DIFFERENT PARTS TAKE PART IN ITS EVOLUTION WITHOUT DESTROYING ITS COHERENCE OR ITS CAPACITY TO REGENERATE.**

Possible roles:

| Role | Does |
|---|---|
| **Community / clients** | Express needs, experiences, priorities and effects |
| **Contributors** | Develop adaptations and proposals |
| **Specialists** | Evaluate technical, economic, social and ecological consequences |
| **Local responsibles** | Decide what each concrete organism integrates |
| **Stewards** | Care for continuity, memory, identity, compatibility and regeneration capacity |
| **Roots** | Makes visible signals, relations, precedents, consequences and decision paths |

The steward's authority does not come from closure or exclusive control. It comes from memory, responsibility, capacity for integration, and care of the lineage.

## 9. Regeneration

An ecosystem can produce value without consuming itself — on the condition that **every extraction stays subordinate to the regeneration capacity of the whole**.

Roots introduces the **regeneration budget**. It may consider: human capacity · maintainability · technical debt · architectural stability · operational load · economic resources · available knowledge · compatibility · ecosystem health.

> **NO ORGANISM SHOULD GROW FASTER THAN IT CAN REGENERATE.**
> When the demand for growth exceeds the capacity to regenerate: **CONSOLIDATE BEFORE EXPANDING.**

Not all growth is healthy. Not all expansion is progress.

## 10. Circulation, concentration, extraction and reserve

| | |
|---|---|
| **Circulation** | lets information, value, resources and decision capacity travel the ecosystem |
| **Functional concentration** | accumulation that keeps memory, stabilizes, coordinates, or prepares resources to circulate again |
| **Extractive accumulation** | concentration that cuts the cycle and turns accumulation into an end |
| **Extraction** | value or resources leaving the system |
| **Reserve** | what is deliberately kept to sustain identity, diversity, memory or future capacity |

> CONCENTRATE TO REMEMBER. · DISTRIBUTE TO CIRCULATE. · TRANSFORM TO REGENERATE. · RESERVE TO PRESERVE. · EXTRACT WITHOUT EXHAUSTING. · GROW WITHOUT DESTROYING THE CAPACITY TO GROW AGAIN.

## 11. Obsolescence and transition

Roots replaces **obsolescence as forced disposal** with **regenerative transition**. A structure may leave its former shape when another configuration better integrates its function, when its resources can be reused, its learning kept, or its matter and knowledge returned to the cycle.

> **EVOLVING DOES NOT MEAN REPLACING EVERYTHING THAT CAME BEFORE. EVOLVING IS ALSO KNOWING WHAT TO KEEP, WHAT TO ADAPT AND WHAT TO LET CHANGE.**

## 12. Reserve zones and selective permeability

An update is not a top-down order from the canonical product. **Each installation is an organism with its own history**: it can accept, adapt, postpone or reject.

| Zone | |
|---|---|
| **Reserve zone** | not modified automatically |
| **Transition zone** | allows testing, adapting and evaluating |
| **Adaptive zone** | absorbs changes more freely |

Not all legacy is reserve. **Legacy** is something old not yet replaced. **Reserve** is something consciously preserved because it still has value, or because changing it would harm the organism.

> **A non-update must be able to become explicit memory, not invisible debt.**

## 13. Grafting and adaptation

An organism may incorporate only part of another's growth. A **graft** is a feature or learning from another Tree or Ring, adapted to the receiving organism:

```
ORIGIN → EVALUATION → ADAPTATION → LOCAL INTEGRATION → FOLLOW-UP → MEMORY
```

**Compatibility does not require sameness.**

## 14. Open source and lineage

Open source makes explicit a central trait of Roots: **the lineage can be distributed**. There is not necessarily a single center. Repositories, forks, mirrors, branches and multiple origins let knowledge replicate, diverge and survive — and resilience also emerges from that distribution.

A fork can be understood as a local adaptation. Some divergences stay local; others return to the common trunk; others give rise to new species.

**Open source turns the product into a shared lineage, not a closed object.**

## 15. The temporal archipelago and corridors between generations

Not all clients live in the same generation. Odoo 13, 15, 17, 19, forks, customizations and divergent implementations can coexist — **each one a temporal island in an archipelago of the same lineage**. An old version is not necessarily an error: it may be a stable adaptation to a particular context. The problem appears when isolation completely breaks the common learning.

Roots understands backward compatibility as maintaining **temporal ecological corridors**. An improvement developed in a new generation can travel backward — not necessarily as the same code, but as **function, intention, learning, pattern and design criterion**. Likewise, an adaptation born in an old generation may hold knowledge useful for a new one. **The flow is bidirectional.**

> *Keep different ages of the same organism alive without losing the memory that connects them.*

## 16. Stewardship of the lineage

Organizations such as Moldeo Interactive can take the role of **lineage steward**: custodian of the lineage's continuity. Responsibilities:

- preserve historical memory;
- keep compatibility between generations;
- tell local adaptation apart from generalizable improvement;
- recover learnings from clients and forks;
- canonicalize improvements;
- backport when reasonable;
- maintain corridors between generations;
- preserve identity and resilience;
- evaluate regeneration costs;
- propose transitions when isolation is no longer sustainable.

> **CARING FOR A LINEAGE DOES NOT MEAN PREVENTING ITS INDIVIDUALS FROM DIVERGING. IT MEANS KEEPING PATHS OPEN SO THEY CAN GO ON LEARNING FROM EACH OTHER.**

Accumulated experience does not work as an argument from authority. It works as memory: what survived, what failed, which patterns came back, which decisions aged well, which transformations proved resilient.

## 17. The shared field

The forest is connected. Roots can work as a **common field of memory and circulation** — and **Micielo** is the organ that carries it:

- **Shared memory** — trees, species, tickets, features, decisions, versions, relations, history.
- **Shared circulation** — events, agents, queries, patterns, signals, propagation, feedback.

Each organism interprets the field according to its own state. **The field does not impose an identical answer on everyone.**

## 18. Humans

Agents can greatly widen the capacity to observe, remember, relate and explore. **Structural decisions remain human.** People carry *embodied memory* — why a decision was taken, which alternative failed, which client originated a need, which part looks simple but is fragile — that is not fully contained in any commit. Roots does not try to replace it: it lets part of it become collective memory.

> The system can detect. Agents can interpret. **Humans decide.**

## 19. Synthetic manifesto

> **ROOTS STARTS FROM A SIMPLE IDEA: A LIVING SYSTEM IS NOT DEFINED ONLY BY WHAT IT STORES, BUT BY HOW IT CIRCULATES, TRANSFORMS AND REGENERATES WHAT IT KNOWS.**

Memory lets us remember. Circulation lets us learn. Diversity lets us adapt. Deliberation lets us understand. Decision lets us orient. Regeneration lets us continue.

Roots seeks to build systems able to:

- produce without exhausting themselves;
- grow without losing identity;
- distribute without fragmenting;
- preserve without freezing;
- debate without erasing differences;
- decide without hiding consequences;
- evolve without destroying their memory;
- incorporate innovation without breaking their capacity for continuity.

**Its biomimetic design is not decoration.** It is a method for thinking architecture, governance, memory, evolution, participation and sustainability as parts of one ecosystem.

## 20. Core phrases

- **Democracy becomes practical when its effects are visible and traceable within the life cycle of the ecosystem.**
- **Debating does not erase diversity. It puts it into relation.**
- **Collective intelligence does not replace collective decision. It informs it.**
- **No organism should grow faster than it can regenerate.**
- **Evolving does not mean replacing everything that came before. Evolving is also knowing what to keep, what to adapt and what to let change.**
- **Caring for a lineage does not mean preventing its individuals from diverging. It means keeping paths open so they can go on learning from each other.**
- *Git preserves what happened. Roots interprets what it meant. The database coordinates what is happening now.*
- *Keep different ages of the same organism alive without losing the memory that connects them.*
- **Concentrate to remember. Distribute to circulate. Transform to regenerate. Reserve to preserve. Extract without exhausting. Grow without destroying the capacity to grow again.**

---

### Note

The biological and ecological terms in this document belong to a **biomimetic design model**. The correspondences between natural elements and Roots components are **design analogies, not claims of scientific equivalence**. Roots uses real ecosystems as a source of strategies and principles, abstracts them, and translates them into technological, social and organizational systems.

Design rationale, source texts and the harmonization with the implemented vocabulary: [`design/biomimetic/`](design/biomimetic/).
