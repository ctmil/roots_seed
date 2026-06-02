# md → PDF reporting

> Convertir documentación de la memoria (`docs/manual.md`, `docs/documentation.md`) a reportes PDF presentables. Tres enfoques según necesidad: rápido, branded, o integrado a Odoo.

---

## Cuándo usar

- Entregar un **manual de usuario** o **documentación técnica** como PDF a un cliente.
- Generar reportes desde la memoria `.roots` de un módulo.
- Sentar la base del **reporting de `odoo_moldeo_sync`** (mismo contenido md, render PDF desde el backend).

## Entradas / contexto requerido

- El/los `.md` fuente (siguen el formato del seed: título `#`, `>` descripción, secciones).
- Imágenes referenciadas (ej. `workbench/` o `static/`) con paths resolubles.
- Opcional: hoja de estilo / plantilla de branding.

## Enfoques

### A) Pandoc → PDF (rápido, técnico) — *default*

```bash
pandoc docs/manual.md -o manual.pdf \
  --toc --pdf-engine=tectonic -V geometry:margin=2.5cm
```
- Pros: una línea, TOC automático, buen tipografiado. Ideal para `documentation.md`.
- Requiere: `pandoc` + un engine LaTeX (`tectonic`/`xelatex`) o `--pdf-engine=weasyprint`.

### B) Markdown → HTML + CSS → PDF (branded)

```bash
pandoc docs/manual.md -o manual.html --standalone --css report.css
weasyprint manual.html manual.pdf     # respeta CSS, headers/footers @page
```
- Pros: control total de estilo (logo, colores Moldeo, portada). Ideal para **manual.md** orientado a cliente.
- El render HTML intermedio reusa el mismo motor markdown que el `fleet-dashboard` (coherencia).

### C) QWeb dentro de Odoo (integrado) — para `odoo_moldeo_sync`

- El md → HTML (server-side) se inyecta en un `report` QWeb (`<template>` con `t-raw` del HTML sanitizado) y Odoo emite el PDF con wkhtmltopdf.
- Pros: vive en el backend, hereda layout/branding de la compañía, se dispara desde un botón/acción. Es el camino para el reporting de dashboards.

## Pasos (genérico)

1. Resolver paths de imágenes (relativos al `.md`; copiar `static/`/`workbench/` junto al fuente si hace falta).
2. Elegir enfoque (A/B/C) según branding/integración.
3. Generar y **verificar** el PDF (TOC, imágenes, saltos de página).
4. Si es recurrente, encapsular en un script (`scripts/`) o en una acción Odoo.

## Verificación

- El PDF abre, tiene TOC/portada esperados, imágenes presentes, sin texto cortado.
- Para C: el reporte se dispara desde la acción y respeta el layout de la compañía.

## Notas / decisiones abiertas

- **Elección de motor**: A para velocidad/interno; B para entregables branded; C cuando deba vivir en Odoo. Documentar la elección en el `decisions.md` del módulo.
- Mantener `manual.md` (cómo USAR) y `documentation.md` (cómo FUNCIONA) separados — generan reportes con audiencias distintas.
- Futuro: una skill hermana podría generar `changelog.md` → notas de versión PDF para clientes.
