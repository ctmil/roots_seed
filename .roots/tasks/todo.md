# roots_seed - TODO

> Backlog del toolkit.

---

## fleet-dashboard

- [ ] Portar a Odoo: `odoo_moldeo_sync` emite `state.json` desde modelos; `odoo_moldeo_htree` renderiza la jerarquía.
- [ ] Evaluar correr `collect.py` como servicio/cron que alimente los modelos Odoo.
- [ ] Cachear `du -sh` de los `.bare` grandes (moldeomint ~862M) si el scan se siente lento.

## Seed

- [ ] Agregar sección `tools/` a `roots_seed.md` (spec) si el patrón se consolida; eventual PR al upstream.
- [ ] **Extender `skills/odoo-module-merging.md`** con el eje **ALIGN horizontal** (convergencia cross-versión de un suite: forward/backport, "migrar ≠ refactor", recipe de cherry-pick, gotchas de versión Odoo). Mejora futura, NO ahora — genérico + inglés, scrubeado de la topología ctmil. Ver `journal/notes.md`.

---
