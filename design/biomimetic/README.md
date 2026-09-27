# design/biomimetic — why the metaphor is a design guide

This folder holds the **rationale** behind [`SEED.md`](../../SEED.md): the source texts, and how their
vocabulary was harmonized with what the Roots ecosystem already implements. The Seed states *what*;
this folder explains *why these words and not others*.

## Sources (Spanish, verbatim)

| File | What it adds |
|---|---|
| [`sources/2026-09-26-first-draft.es.md`](sources/2026-09-26-first-draft.es.md) | Memory of long-lived software: Trunk, Cambium, Rings, Rays, Wounds/Scars, humans as structural decision-makers, the three layers of memory |
| [`sources/2026-09-27-working-synthesis.es.md`](sources/2026-09-27-working-synthesis.es.md) | Scales (Forest/Grove/Tree), installations as individuals of a lineage, customization as local adaptation, one product definition with internal / public / agent views |
| [`sources/2026-09-27-manifesto-v0.1.es.md`](sources/2026-09-27-manifesto-v0.1.es.md) | **Governs.** Identity and governance: participation, practical democracy, regeneration budget, reserve zones, grafting, open-source lineage, temporal archipelago, lineage steward |

## The harmonization rule

Before the manifesto, the ecosystem's words were already **overloaded**, not missing: *Forest* named
the workspace, a fleet manifest, a health dashboard and a platform; *Tree* named a repo, a product,
the organization and a user account; *Roots* named the memory folder, the agents module, an access
depth and the root of the vocabulary. Adding new terms on top would have added ambiguity, not meaning.

So the rule is: **two scales, and each word lives in exactly one.**

- **Ecosystem scale** — the modules are the organs of the Forest: Seed · Forest · Micielo · Flores · Folio.
- **Tree scale** — the anatomy of one organism, kept in its `.roots/`: Roots · Soil · Trunk · Grain · Rings · Cambium · Rays · Branches · Buds/Features/Fruits · Wounds/Scars · Grafts.

And: **a term enters only when it names something that exists, or must exist, and would otherwise stay
unnamed.** The analogy is a design guide, not a point-to-point mapping.

## What was taken, renamed, or left out

| Source term | Decision | Why |
|---|---|---|
| Roots = "deep dependencies, connections, base resources" (v0.1) | **Roots stays the Tree's memory.** The connections are **Micielo** | In biology the network that connects different trees is the mycelium (mycorrhizae), not the roots of one tree. Micielo already carried the name |
| Rays between Trees | **Rays are inside one Tree**; between Trees → Micielo | Medullary rays are radial, intra-tree |
| Morphogenetic field / shared field | Kept as *shared field*, carried by **Micielo** | Same reason |
| Flowers = visible, votable possibility | **Flores = the whole reproductive organ**: propagation (pollination, grafting, planting the Seed) **and** its public proposal/vote layer | One organ, two faces — what spreads and what is exposed for selection |
| Branches = functional capabilities (v0.1) | **Branch = git branch / generation line.** Capabilities are **Features**; Buds = candidate features; Fruits = releases | Every implemented model already uses Branch as a git branch; capabilities and releases already have their own records |
| Tree | **Unit of product identity** (usually one repo) | An account that grants access to the Forest is not a Tree |
| Bark (public surface) | **Not an organ.** The outward surface is **Folio** (leaves); "public view" is a *view* of the product definition | It would have been the third word for the same thing |
| Wounds / Scars / Reaction wood | Kept: an open disturbance / its recorded memory / the structural change it forced | Trees do not repair damaged tissue — they **wall it off and grow around it**. Contain first, diagnose after |
| Knots, Institutional Tree, Sugar, Genotype/Phenotype | **Left out** (v0.1 dropped them) | Genotype/phenotype survives as *canonical Tree vs installation* |

## Open for the spec (`roots_seed.md` § Anatomy, next)

Each Tree-scale term needs a **place** (file/record) and a **trigger** (when it is written), otherwise it
stays decoration: Rings (consolidated episodes), Scars (closed wounds with their structural change),
Grafts (log), Zones (per installation: reserve / transition / adaptive — *a non-update becomes
explicit memory*), and the promotion criterion Cambium → Ring → Trunk (**structural change only by
explicit human decision**).
