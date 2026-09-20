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
| [roots-refresh.md](./roots-refresh.md) | **Closing step of a batch**: bring `changelog`/`fixes-log`/`documentation`/`migrations` up to date consistently across every module·version |
| [allowlist-sync.md](./allowlist-sync.md) | Keep the agent's permission allowlist in step with real usage and with the evolving `.roots`/workspace structure |
| [odoo-module-merging.md](./odoo-module-merging.md) | Strategy for merging branches/clients into official Odoo repos (cross-version, typical conflict resolution, `.roots` promotion) |
| [md-to-pdf-reporting.md](./md-to-pdf-reporting.md) | Convert `docs/manual.md` and `documentation.md` to PDF reports (pandoc / HTML+CSS / Odoo QWeb) |

### Community — the two-way relationship with the public seed

The seed had the *policy* for contributing (§ *Contributing to the upstream*, § *Public hygiene*) and
no **invocable surface** for it, so it did not happen. These four are that surface; all of them run
on `scripts/roots-upstream.sh` (capability ladder: `gh` → `$GITHUB_TOKEN` → prefilled URL, which
needs no credentials — and only a real publish counts as published).

| Skill | What for |
|-------|----------|
| [roots-report.md](./roots-report.md) | **See the forest**: every Tree x Branch at once, ranked by what can still be LOST (uncommitted `.roots/` memory first), with the order to land it. Read-only. |
| [roots-seed-audit.md](./roots-seed-audit.md) | **Before re-distributing a bumped seed**: which local copies are merely stale and which are forks carrying content nobody sent upstream. Read-only. |
| [roots-suggest.md](./roots-suggest.md) | **Propose**: something this deployment learned should be in the seed (carries the measurement) |
| [roots-issue.md](./roots-issue.md) | **Report**: the seed's own text is wrong, ambiguous or silently harmful |
| [roots-pr.md](./roots-pr.md) | **Merge**: an improvement already written locally, split generic-vs-local, up as a PR |
| [roots-triage.md](./roots-triage.md) | **Receive**: read what the community opened and decide what enters (the hand coming back) |

> Next candidates: security review of access rights, generating `changelog.md` from commits, module installation smoke-test, changelog→client-facing digest.

## Skill file format: store vs activation

In the **store** (`roots_seed/skills/`, `<repo>/.roots/skills/`) a skill is a **flat `<name>.md`**.
Claude Code's **activation** layer expects a **directory**: `.claude/skills/<name>/SKILL.md`, whose
front-matter (`name`, `description`) is what makes it invocable as `/<name>`. The conversion is
mechanical — `scripts/sync-agents-skills.sh` does it in both directions. Agents are simpler: a flat
`<name>.md` in both layers.

> Consequence worth knowing: a skill written **only** in the store is documentation; it becomes a
> capability the moment it is activated. Drift between the two layers is the normal failure mode —
> run the sync script's `--check` in a session-close hook.
