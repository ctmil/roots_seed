# Odoo module merging

> Strategy for merging work branches (`claude/*`) or client branches into the official Odoo repos, and for forward/back-porting across versions, minimizing breakage and preserving the `.roots` memory.

---

## When to use

- Bring a feature/fix branch into the official version branch (`17.0`, `19.0`, …).
- Forward-port (16→17→18→19) or back-port a change.
- Consolidate a client branch's `.roots` into the source (see "Promotion").

## Inputs / required context

- Repo mounted as bare+worktrees (see `scripts/`), worktree of the branch and of the target branch.
- The project's migration cheatsheet if it exists (e.g. `moldeomint/17.0/.roots/migration.md`).
- The module's `.roots` (to record fixes/decisions).

## Steps

1. **Sync**: `git -C <repo> fetch origin --prune`. Rebase the branch onto the current base or prepare the merge.
2. **Review the diff by layers** (not all at once) — each layer has its own typical conflicts:
   - **`__manifest__.py`** — version, `depends`, `data`. Conflict almost guaranteed in `version`.
   - **`__init__.py` / imports** — model import order.
   - **XML views** — duplicate ids, and per-version schema differences (see table).
   - **`security/ir.model.access.csv`** — duplicate/ordered lines; merge by union, without duplicating `id`.
   - **Data / `data/*.xml`** — `noupdate`, sequences.
3. **Resolve with the Odoo patterns** (below). On a `ParseError` when updating, always suspect the target version's view schema.
4. **Update the `.roots`**: record the fix in `debug/fixes-log.md`, architecture decisions in `design/decisions.md`, and data/field migrations in `debug/migrations.md`.
5. **Verify** (see below) before pushing.
6. **Promote discoveries**: if the merge revealed a pattern/decision useful for everyone, promote it to the source (`design/decisions.md` / `skills/patterns.md`). The `diary` and `errors-log` stay contextual (not promoted).

## Odoo conflict patterns (cross-version)

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `ParseError` on `-u` in v17+ | `edit="false"` in inline `<list>`/`<tree>` | drop `edit`; use `readonly="True"` per field |
| Deprecated `<tree>` | renamed to `<list>` in v17 | migrate the tag to `<list>` |
| `attrs={...}` ignored/broken | removed in v17 (dep.) / v18 (out) | direct attributes (`invisible="..."`, `readonly="..."`) |
| Field "does not exist on the parent model" | `<list edit="false">` confuses the comodel (v17) | drop `edit="false"` |
| Conflict in the manifest `version` | simultaneous bump | take the higher one; renumber per repo convention |

> Keep this table in sync with the project's `migration.md` (the detailed cheatsheet).

## Verification

- `-u <module>` (or clean install) without `ParseError` or tracebacks.
- Module tests if they exist.
- Manual smoke-test of the touched views.

## Notes / open decisions

- **Merge vs rebase**: rebase for short feature branches (clean history); merge to integrate long-lived client branches (preserves context). Decide per case and note it in `decisions.md`.
- Consolidating a client's `.roots` into the source is **explicit and per item** (decisions/patterns/glossary good candidates; diary/errors-log not).
