# roots_seed - Notes

> Ideas y observaciones del toolkit.

---

### Documentar `tools/` en la spec del seed (02 Junio)

`roots_seed.md` describe la estructura `.roots/` pero no menciona un directorio `tools/` para utilidades ejecutables reusables. Si el patrón crece, agregar una sección al seed (y eventualmente promover al upstream).
**Estado:** Nueva.

### Portar fleet-dashboard a Odoo (02 Junio)

El `state.json` es el contrato; el siguiente paso natural es que `odoo_moldeo_sync` lo emita desde modelos y `odoo_moldeo_htree` renderice la jerarquía. `collect.py` podría correr como servicio/cron que alimenta esos modelos.
**Estado:** En evaluación → tasks/todo.md.

---
