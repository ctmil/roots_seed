# skills — toolkit shared library

> Cross-cutting, well-designed and reusable skills that live in the seed to improve common strategies (merging, reporting, etc.). Tool-agnostic: runnable by any AI agent or human.

---

## toolkit skills/ vs each `.roots` skills/

| | Toolkit `roots_seed/skills/` (this one) | `.roots/skills/` (per module) |
|---|---|---|
| Scope | **shared** — applies to many modules/projects | **local** — specific to that module |
| Content | canonical strategies (Odoo merging, reporting…) | its own `prompts.md`, `workflows.md`, `patterns.md` |
| Use | **referenced** or **copied/adapted** inside a `.roots/skills/` | kept alongside the module |

When a module needs one of these strategies, it references it from its `.roots` (or copies the relevant part into its `skills/workflows.md` and adapts it). If a module discovers a general improvement, it is **promoted** here (same spirit as promoting seed discoveries).

## Skill format

Each skill is a `.md` with:

```markdown
# {Skill name}

> One line: what it solves.

## When to use
## Inputs / required context
## Steps
## Verification
## Notes / open decisions
```

## Index

| Skill | What for |
|-------|----------|
| [odoo-module-merging.md](./odoo-module-merging.md) | Strategy for merging branches/clients into official Odoo repos (cross-version, typical conflict resolution, `.roots` promotion) |
| [md-to-pdf-reporting.md](./md-to-pdf-reporting.md) | Convert `docs/manual.md` and `documentation.md` to PDF reports (pandoc / HTML+CSS / Odoo QWeb) |

> Next candidates: security review of access rights, generating `changelog.md` from commits, module installation smoke-test.
