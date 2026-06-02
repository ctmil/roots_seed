# roots_seed - Context

> Toolkit del seed agentic: la spec maestra (`roots_seed.md`) + `tools/` con utilidades reusables y tool-agnostic. Espejo open-source de `github.com/ctmil/roots_seed`.

---

## Qué es

`roots_seed` es la **fuente de verdad** de la estructura `.roots/` (memoria persistente para agentes IA y humanos). Contiene:

- **`roots_seed.md`** — la spec/plantilla maestra (v1.7). Define modos, estructura, estándares y protocolos.
- **`tools/`** — utilidades que operan sobre `.roots/` y flotas de repos. Tool-agnostic, sin dependencias pesadas.
- **`.roots/`** (este) — memoria del propio toolkit, en modo **flat**.

## Estado actual

Estable. Spec en v1.7. Se acaba de incorporar el primer tool ejecutable: **`tools/fleet-dashboard/`** (visor web en tiempo real de una flota bare+worktrees y su memoria `.roots`).

## Convenciones clave

- **Flat**: este `.roots` lleva los archivos directo (un repo, un proyecto, una memoria).
- **Canonical del seed**: `../roots_seed.md` (raíz del repo). Este `.roots` no lo duplica.
- **Tools self-contained**: cada tool bajo `tools/<nombre>/` trae su README y corre solo con stdlib + binarios comunes.

## Tools

Ver [docs/tools.md](./docs/tools.md). Hoy: `fleet-dashboard` (colector → state.json → vista HTML; pensado como base para los dashboards de `odoo_moldeo_sync` / `odoo_moldeo_htree`).

---
