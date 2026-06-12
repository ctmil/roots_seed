# md → PDF reporting

> Convert memory documentation (`docs/manual.md`, `docs/documentation.md`) to presentable PDF reports. Three approaches depending on need: quick, branded, or Odoo-integrated.

---

## When to use

- Deliver a **user manual** or **technical documentation** as a PDF to a client.
- Generate reports from a module's `.roots` memory.
- Lay the groundwork for **`odoo_moldeo_sync` reporting** (same md content, PDF render from the backend).

## Inputs / required context

- The source `.md` file(s) (following the seed format: `#` title, `>` description, sections).
- Referenced images (e.g. `workbench/` or `static/`) with resolvable paths.
- Optional: style sheet / branding template.

## Approaches

### A) Pandoc → PDF (quick, technical) — *default*

```bash
pandoc docs/manual.md -o manual.pdf \
  --toc --pdf-engine=tectonic -V geometry:margin=2.5cm
```
- Pros: one line, automatic TOC, good typesetting. Ideal for `documentation.md`.
- Requires: `pandoc` + a LaTeX engine (`tectonic`/`xelatex`) or `--pdf-engine=weasyprint`.

### B) Markdown → HTML + CSS → PDF (branded)

```bash
pandoc docs/manual.md -o manual.html --standalone --css report.css
weasyprint manual.html manual.pdf     # respects CSS, headers/footers @page
```
- Pros: full style control (logo, Moldeo colors, cover page). Ideal for client-facing **manual.md**.
- The intermediate HTML render reuses the same markdown engine as the `fleet-dashboard` (consistency).

### C) QWeb inside Odoo (integrated) — for `odoo_moldeo_sync`

- The md → HTML (server-side) is injected into a QWeb `report` (`<template>` with `t-raw` of the sanitized HTML) and Odoo emits the PDF via wkhtmltopdf.
- Pros: lives in the backend, inherits the company layout/branding, triggered from a button/action. This is the path for dashboard reporting.

## Steps (generic)

1. Resolve image paths (relative to the `.md`; copy `static/`/`workbench/` next to the source if needed).
2. Choose an approach (A/B/C) depending on branding/integration.
3. Generate and **verify** the PDF (TOC, images, page breaks).
4. If recurring, encapsulate it in a script (`scripts/`) or in an Odoo action.

## Verification

- The PDF opens, has the expected TOC/cover, images present, no clipped text.
- For C: the report is triggered from the action and respects the company layout.

## Notes / open decisions

- **Engine choice**: A for speed/internal; B for branded deliverables; C when it must live in Odoo. Document the choice in the module's `decisions.md`.
- Keep `manual.md` (how to USE) and `documentation.md` (how it WORKS) separate — they generate reports for different audiences.
- Future: a sibling skill could generate `changelog.md` → PDF release notes for clients.
