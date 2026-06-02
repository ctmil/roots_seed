# roots_seed - Diary

> Bitácora del toolkit. Primera persona, reflexivo.

---

**02 Junio** - Toolkit sistematizado: scripts/ + skills/ + tools/ (seed v1.8).

Sistematizamos el concepto de "memoria persistente con herramientas adecuadas". Copié los `.sh` a `scripts/` (montaje de flota bare+worktrees) y arranqué `skills/` como **biblioteca compartida** de estrategias bien diseñadas — distinta del `skills/` local de cada `.roots`. Primeras dos: `odoo-module-merging` (merge hacia repos oficiales: revisión por capas, patrones de conflicto cross-versión Odoo, promoción del `.roots`) y `md-to-pdf-reporting` (manual/documentation → PDF vía pandoc / HTML+CSS / QWeb Odoo, base del reporting de odoo_moldeo_sync). Bumpeé el seed a **v1.8** con la sección "Toolkit complementario" (referencia, no inlinea código) y regeneré la copia del workspace. Decisión consciente: NO pisar los 74 `roots_seed.md` que viven en `.roots` de otros repos (sería modificar working trees ajenos); esa redistribución, si se quiere, es un merge explícito aparte.

**02 Junio** - fleet-dashboard: feed agregado, recursivo, con íconos Odoo.

Reestructuré la vista principal del dashboard a un **feed agregado de la flota** en orden de lectura: ① Cambios (journal) → ② Tareas → ③ Docs (markdown renderizado, lazy) → ④ Skills/Hooks/Debug (colapsados). El descubrimiento de `.roots` ahora es **recursivo** (cualquier profundidad, no solo raíz+subdir), y cada módulo muestra su **ícono** `static/description/icon.png` + link a su `index.html`. Lo más recién modificado arranca expandido; el resto, colapsado/lazy. Sumé al server un endpoint `/file` con guarda anti-traversal para servir íconos/md/html, y un render de markdown propio (sin deps) en la vista. Corre contra el workspace real: 79 módulos con memoria, 249 cambios, 538 tareas abiertas.

**02 Junio** - Primer tool ejecutable del seed: fleet-dashboard.

Arranqué el `.roots` propio de `roots_seed` (modo flat) y sumé `tools/fleet-dashboard/`: un visor web del estado de la flota (git + `.roots`) en tiempo real, todo con stdlib. Lo importante de diseño es que quedó en 3 capas (colector → `state.json` → vista) para que el `state.json` sea un contrato portable: la idea es que `odoo_moldeo_sync` produzca el mismo JSON desde sus modelos y reuse la vista, con la jerarquía Flota→repo→worktree→.roots mapeando a `odoo_moldeo_htree`. También lo pensamos para correr remoto (túnel SSH), despegándonos del IDE/Antigravity. El colector ya corre contra el workspace real y detecta los repos en vivo (24, no los 17 del snapshot viejo de fleet.json).

---
