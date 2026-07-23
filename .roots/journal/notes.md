# roots_seed - Notes

> Ideas y observaciones del toolkit.

---

### Documentar `tools/` en la spec del seed (02 Junio)

`roots_seed.md` describe la estructura `.roots/` pero no menciona un directorio `tools/` para utilidades ejecutables reusables. Si el patrón crece, agregar una sección al seed (y eventualmente promover al upstream).
**Estado:** Nueva.

### Portar fleet-dashboard a Odoo (02 Junio)

El `state.json` es el contrato; el siguiente paso natural es que `odoo_moldeo_sync` lo emita desde modelos y `odoo_moldeo_htree` renderice la jerarquía. `collect.py` podría correr como servicio/cron que alimenta esos modelos.
**Estado:** En evaluación → tasks/todo.md.

### Los "dos ejes" de sources — extender `odoo-module-merging.md` (13 Junio)

Operando la flota aparecieron **dos ejes ortogonales** sobre los repos source, hoy resueltos por
skills privados del workspace (`/sources` y `/sources-align`):
- **SYNC vertical** — cada rama `<ver>` ↔ `origin/<ver>` (pull/push, por versión).
- **ALIGN horizontal** — todas las versiones de un grove funcionalmente idénticas entre sí
  (`16.0 ≡ 17.0 ≡ 18.0 ≡ 19.0`), difiriendo solo en sintaxis de versión: cherry-pick cross-versión
  (forward-port + backport), regla **"migrar ≠ refactor"**, allowlist de divergencias intencionales,
  y gotchas de versión Odoo (`attrs` vs modifiers nativos 17+, `_sql_constraints` fallback solo 16.0,
  `company_dependent` por ORM nunca SQL crudo, CRLF).

**Mejora futura (NO ahora):** el eje ALIGN es conocimiento técnico genérico y valioso → **extender el
skill `skills/odoo-module-merging.md`** del seed con ese playbook (en vez de skills nuevos). Requisitos
antes de publicar (el seed es upstream **público**): traducir a inglés-canónico, **scrubear la
topología ctmil** (tabla de groves/clientes/aggregators, rutas absolutas del workspace privado, links `[[...]]` a
memorias privadas). El eje SYNC vertical y la tabla de la flota se quedan en el workspace privado.
**Estado:** Anotada como mejora futura.

---
