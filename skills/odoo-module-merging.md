# Odoo module merging

> Estrategia para mergear branches de trabajo (`claude/*`) o branches de cliente hacia los repos oficiales Odoo, y para forward/back-portar entre versiones, minimizando roturas y preservando la memoria `.roots`.

---

## Cuándo usar

- Llevar un branch de feature/fix a la rama oficial de versión (`17.0`, `19.0`, …).
- Forward-port (16→17→18→19) o back-port de un cambio.
- Consolidar el `.roots` de un branch de cliente al source (ver "Promoción").

## Entradas / contexto requerido

- Repo montado bare+worktrees (ver `scripts/`), worktree del branch y de la rama destino.
- El cheatsheet de migración del proyecto si existe (ej. `moldeomint/17.0/.roots/migration.md`).
- El `.roots` del módulo (para registrar fixes/decisiones).

## Pasos

1. **Sincronizar**: `git -C <repo> fetch origin --prune`. Rebasar el branch sobre la base actual o preparar el merge.
2. **Revisar el diff por capas** (no todo junto) — cada capa tiene conflictos típicos distintos:
   - **`__manifest__.py`** — versión, `depends`, `data`. Conflicto casi seguro en `version`.
   - **`__init__.py` / imports** — orden de imports de modelos.
   - **Vistas XML** — ids duplicados, y diferencias de schema por versión (ver tabla).
   - **`security/ir.model.access.csv`** — líneas duplicadas/orden; merge por unión, sin duplicar `id`.
   - **Datos / `data/*.xml`** — `noupdate`, secuencias.
3. **Resolver con los patrones Odoo** (abajo). Ante `ParseError` al actualizar, sospechar siempre del schema de vistas de la versión destino.
4. **Actualizar el `.roots`**: registrar el fix en `debug/fixes-log.md`, decisiones de arquitectura en `design/decisions.md`, y migraciones de datos/campos en `debug/migrations.md`.
5. **Verificar** (ver abajo) antes de pushear.
6. **Promover descubrimientos**: si el merge reveló un patrón/decisión útil para todos, promoverlo al source (`design/decisions.md` / `skills/patterns.md`). El `diary` y `errors-log` quedan contextuales (no se promueven).

## Patrones de conflicto Odoo (cross-versión)

| Síntoma | Causa | Resolución |
|---------|-------|------------|
| `ParseError` al `-u` en v17+ | `edit="false"` en `<list>`/`<tree>` inline | quitar `edit`; usar `readonly="True"` por campo |
| `<tree>` deprecado | renombrado a `<list>` en v17 | migrar tag a `<list>` |
| `attrs={...}` ignorado/roto | eliminado en v17 (dep.) / v18 (out) | atributos directos (`invisible="..."`, `readonly="..."`) |
| Campo "no existe en el modelo padre" | `<list edit="false">` confunde el comodelo (v17) | quitar `edit="false"` |
| Conflicto en `version` del manifest | bump simultáneo | tomar el mayor; renumerar según convención del repo |

> Mantener esta tabla sincronizada con el `migration.md` del proyecto (es el cheatsheet detallado).

## Verificación

- `-u <module>` (o instalación limpia) sin `ParseError` ni tracebacks.
- Tests del módulo si existen.
- Smoke manual de las vistas tocadas.

## Notas / decisiones abiertas

- **Merge vs rebase**: rebase para branches de feature cortos (historia limpia); merge para integrar branches de cliente de larga vida (preserva contexto). Decidir por caso y anotar en `decisions.md`.
- La consolidación del `.roots` de un cliente al source es **explícita y por item** (decisions/patterns/glossary buenos candidatos; diary/errors-log no).
