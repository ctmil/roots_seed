# roots_seed - Context

> Toolkit del seed agentic: la spec maestra (`roots_seed.md`) + `tools/` con utilidades reusables y tool-agnostic. Espejo open-source de `github.com/ctmil/roots_seed`.

---

## Qué es

`roots_seed` es la **fuente de verdad** de la estructura `.roots/` (memoria persistente para agentes IA y humanos). Contiene:

- **`roots_seed.md`** — la spec/plantilla maestra (**v1.19**). Define modos, estructura, estándares y protocolos.
- **`tools/`** — utilidades que operan sobre `.roots/` y flotas de repos. Tool-agnostic, sin dependencias pesadas.
- **`.roots/`** (este) — memoria del propio toolkit, en modo **flat**.

## Estado actual

Spec en **v1.19** — *la capa de entrega*. El seed dejó de ser sólo un formato de memoria: además de
cómo se GUARDA, ahora define cómo se ENTREGA (inbox, manifiesto, acta de pre-compactación, guard de
contexto) y trae los dos semáforos (`sync-lock` sobre worktrees, `work-claim` sobre el trabajo).

⚠️ Este `context.md` **se quedó en "v1.7" durante doce versiones** — el propio repo del seed no se
estaba aplicando el seed. Corregido el 13-sep-2026 junto con el README (decía v1.14). Vale como
recordatorio: la memoria desactualizada no avisa que lo está, y responde con total seguridad.

Tools: **`tools/forest-dashboard/`** (visor web de una flota bare+worktrees y su memoria `.roots`) —
con una propuesta abierta de **capa de pulso** (`PROPOSAL-pulse-layer.md`): hoy ve la memoria, no la vida.

## Convenciones clave

- **Flat**: este `.roots` lleva los archivos directo (un repo, un proyecto, una memoria).
- **Canonical del seed**: `../roots_seed.md` (raíz del repo). Este `.roots` no lo duplica.
- **Tools self-contained**: cada tool bajo `tools/<nombre>/` trae su README y corre solo con stdlib + binarios comunes.

## Tools

Ver [docs/tools.md](./docs/tools.md). Hoy: `fleet-dashboard` (colector → state.json → vista HTML; pensado como base para los dashboards de `odoo_moldeo_sync` / `odoo_moldeo_htree`).

---
