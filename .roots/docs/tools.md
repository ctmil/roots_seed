# roots_seed - Tools

> Índice de las utilidades del toolkit: `scripts/` (montaje/operación de la flota) y `tools/` (apps). Cada una es self-contained con su README.

---

## scripts/

Plantillas `.sh` que se copian a la raíz del workspace. Arman el sustrato físico de la memoria (repos como **bare+worktrees**) y la operan:

- `setup-module.sh` — clona un repo bare + worktrees por branch.
- `setupbranch.sh` — agrega un worktree para un branch (auto-detecta existente/nuevo).
- `dashboard.sh` — levanta el fleet-dashboard y abre el navegador.

Ver `scripts/README.md`.

---

## fleet-dashboard

**Path:** `tools/fleet-dashboard/`
**Qué hace:** dashboard web en tiempo real del estado de una flota de repos montados con **bare+worktrees** y su memoria `.roots`. Muestra estado git por worktree (branch, ahead/behind, dirty, último commit), resumen de `.roots` por módulo (tasks abiertas, errores activos, diary), proyectos/campañas cross-módulo y métricas de flota.

**Arquitectura (3 capas):** `collect.py` (colector → `state.json`, el contrato) → `serve.py` (server liviano stdlib, cache TTL) → `index.html` (vista htree colapsable). Sin dependencias externas (stdlib + `git`).

**Correr:**
```bash
python3 tools/fleet-dashboard/serve.py --root /ruta/al/workspace
# remoto: bind 127.0.0.1 + túnel SSH (recomendado), o --host 0.0.0.0 --token X
```

**Propósito de diseño:** es la **base** para los dashboards del backend `odoo_moldeo_sync`. El `state.json` es el contrato reusable; la jerarquía Flota→repo→worktree→.roots mapea al patrón `odoo_moldeo_htree`. Ver `tools/fleet-dashboard/README.md` → "Mapeo a Odoo".

---
