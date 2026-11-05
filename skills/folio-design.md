---
name: folio-design
description: Design by layers on a Folio board (MoldeoLab parametric design) from the forest — create the person's works, turn a layered design (JSON + local images) into a template, compose every variant on the board and download the PNGs. Invoke when the person says "make a design / poster / series with variants", "try the layer generator", "generate variants of X", "download the variants", or wants to test MoldeoLab's parametric design. NOT for publishing (the organisation publishes) and NOT for server-side AI generation (the AI runs in this forest).
---

# folio-design

> A **layer template** is a parametric design: a canvas plus layers, each with options. The board
> combines one option per layer and composes every combination into a PNG **variant**, tied to the
> person's **work** and signed by them. The person designs the rules; the system derives the variants.
> Instrument: **`folio_design.py`** (stdlib), next to `htree.py` — it reuses its `.htree.env` profiles.
> If it is missing: `git -C roots_seed pull` and run `roots_seed/scripts/folio_design.py`.

## What the account can do (and cannot)
- ✅ Create and edit **their own** works and templates; read the **published** works of others as reference.
- ✅ Layer sources composed on the board at no cost: `solid` · `gradient` · `text` · `badge` · `static`.
- ⛔ **Publish** — the organisation does it. A work stays a draft.
- ⛔ **`ai_image`** (server-side generation) — **the AI runs in this forest**: generate the image here,
  save it next to the spec, and use it as a `static` layer with a `path`.
- If the board answers *"Modelo no expuesto"* or a permission error, the account is not enabled for
  design yet: say so and leave a comment in the requests task. Do not route around it.

## Steps
1. `python3 folio_design.py works` — what exists. New idea ⇒ `work-new "Name"` (dry-run, then `--yes`).
2. **Write the spec** `design/<code>/design.json` (format in `folio_design.py -h`). Images the AI made
   go in `design/<code>/assets/`. Keep `max_variants` small at first (4–6): **one design that works
   before a series**.
3. `python3 folio_design.py spec design/<code>/design.json --work <ID>` → dry-run shows layers and
   assets; `--yes` sends it. It prints how many combinations exist.
4. `python3 folio_design.py generate <TEMPLATE_ID> --yes` → composes the variants on the board.
5. `python3 folio_design.py results <TEMPLATE_ID> --out design/<code>/out` → PNG + params per variant.
   **Look at them** before saying "done" (open the PNGs).
6. **Write the experience down** — this is a betatest: in `.roots/` and as a comment on the MoldeoLab
   task: what was clear, what blocked, what was missing, what surprised. That record is the product.

## Scenes and sketchbooks (v1.28)
A **scene** is a moldeo js composition tied to a work (config JSON + layers); a **sketchbook** gathers
a work's process (pages: image · video · audio · document · text). Same rules: yours only, unpublished.
1. `scene-new "Name" --work <ID> [--config scene.json]` → the scene is set on the work.
2. `scene-layer <SCENE_ID> "Name" --type image|text|shape|video|animation|particle|3d [--config layer.json] [--image f.png]`.
3. `sketchbook-new <WORK_ID> "Name" [--scene <SCENE_ID>]` → `page-new <SKETCHBOOK_ID> "Name" --type image --file f.png [--notes "..."]`.
4. `scenes` · `sketchbooks --work <ID>` to see them.
- ⛔ **Raw code** (js/css/html/embed, a JS library by URL) is not loaded from a collaborator account yet:
  upload what the code produced (image/video) as a page, or describe it in the scene config.
- You can only attach to YOUR work, scene or sketchbook; published ones of others are read-only reference.

## Rules
- The design and its rules are the author's: propose, never overwrite someone else's work.
- `code` is unique on the board — prefix it with something of yours.
- Writes are dry-run unless `--yes`; show the dry-run to the person and wait for their "yes".
- `.htree.env` never goes to git, a task or a chat.
