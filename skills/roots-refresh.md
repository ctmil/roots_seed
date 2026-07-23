# roots-refresh

> **Mandatory closing step** of a batch: after porting/synchronizing a set of changes across a
> multi-module · multi-version grove, the code is in sync but the **`.roots/` memory is not**.
> This pass brings it up to date *consistently* across every module·version.

## When to use
Every time a batch closes — "we pushed the batch to the sources" is the trigger. It is the last step
of a grove sync playbook, before declaring the batch done.

**Why it needs to be its own step:** porting agents update `debug/migrations.md` (the file they are
forced to think about) and nothing else. Left alone, `journal/changelog.md` stays at zero forever
while the code moves, and the memory silently stops describing the product.

## Inputs
- The list of module·version pairs touched by the batch.
- What actually changed per module: fixes (symptom → cause), user-facing fields/config/modes, and
  any version-specific adaptation.

## Steps — per module·version
Use the seed's existing files. Do not invent new ones.

1. **`journal/changelog.md`** — a new entry: version heading + date + bullets of what changed **in
   that module** (not the whole suite). This is the one that matters most; it is usually the one at zero.
2. **`debug/fixes-log.md`** — the defects fixed in the batch (symptom → root cause → fix), each
   pointing at `file:function`.
3. **`docs/documentation.md`** (and `docs/manual.md` when it is user-visible) — new fields, modes and
   configuration introduced by the batch.
4. **`debug/migrations.md`** — **only** if the version needed an adaptation: what was done
   differently here versus the base version. Check it is *complete and even* across versions — a
   version left at zero is the tell that a port was done blind.

## Rules
- **Cross-version consistency:** changelog / fixes-log / documentation of a module are essentially
  the *same* text across versions (same behavior). The difference belongs in `migrations.md`.
- **Per module, only that module's changes.**
- **Do not duplicate:** if a version already recorded part of the batch, complete it, don't repeat it.
- One commit per worktree: `docs(roots): roots-refresh batch <id> — changelog/fixes/docs`. `.roots/`
  is tracked, so this commit ships. If the hosting platform builds on push, **pace the pushes**: one
  push → wait for the build → next.

## Verification
- No `changelog.md` left with zero references to the batch.
- `migrations.md` even across versions.
- One commit per worktree, pushed.

## Notes
Delegable to an agent that walks the N worktrees, given the per-module content. The human supplies
*what changed*; the agent supplies *consistency*.
