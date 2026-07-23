# agents — cross-project base library

> Subagents (Claude Code format) that are **generic enough to be worth carrying across projects**.
> This is the **base** layer of the three described in `roots_seed.md` § *Agents and skills*:
> **store** (`<repo>/.roots/agents/`, tracked) → **activation** (`<repo>/.claude/agents/`, local) →
> **base** (here, in the seed).

Nothing here is preloaded into a project. You **import on demand**: copy what a repo needs into its
`.roots/agents/` (where it lives, versioned and free to diverge), and activate in `.claude/agents/`
only what that machine will actually use.

---

## What belongs here (and what does not)

| Belongs | Does not belong |
|---|---|
| A **capability** any project could need (find a bug, migrate a version, design a UI) | An agent that only makes sense for one client/product |
| A **Forest primitive** operator (a grove, a tree, a branch) | An agent hardcoded to specific hostnames, repos or accounts |
| A **template** to derive project-specific agents from | Anything carrying credentials, client names, internal URLs or phone numbers |

> **Public-repo rule:** this seed is published. An agent promoted here must be scrubbed of client
> names, hostnames, IPs, account ids, paths outside the seed, and credential locations. See
> `roots_seed.md` § *Contributing to the upstream → Public hygiene*.

## Catalog

| Agent | For | Model |
|---|---|---|
| [`bug-hunter.md`](./bug-hunter.md) | Diagnose a concrete bug and land the **minimal** verified fix | sonnet |
| [`grove-keeper.md`](./grove-keeper.md) | Keep a **grove** (family of related repos) in sync across its branches, in dependency order | opus |
| [`designer.md`](./designer.md) | UI/UX: layouts, front-end components, design tokens, light/dark | sonnet |
| [`odoo-architect.md`](./odoo-architect.md) | Odoo module architecture: models, inheritance, ADRs | opus |
| [`odoo-migrator.md`](./odoo-migrator.md) | Odoo backport / forward-port between major versions | opus |
| [`domain-keeper.template.md`](./domain-keeper.template.md) | **Template** — derive one owner agent per domain of your Forest | opus |

> The Odoo pair is domain-specific on purpose: it is the reference implementation of the
> `odoo-suite` recipe (`recipes/odoo-suite.md`). Read them as a worked example of how a
> *domain pack* writes its agents, not as a dependency of the seed.

## Agent file format

```markdown
---
name: <kebab-case, matches the filename>
description: <one line: what it is for + WHEN to use it + what it is NOT for, routing to siblings>
tools: Read, Grep, Glob, Bash, Edit      # least privilege — omit to inherit everything
model: opus | sonnet | haiku             # optional
---
<system prompt: who it is, what it reads before acting, its procedure, its hard rules>
```

Two conventions that matter more than they look:

1. **Negative routing in `description`.** Past ~5 agents, the orchestrator's failure mode is not
   "no agent fits" but "several look plausible". Every description must close with what the agent is
   **not** for, naming the sibling that is: *"…NOT for version migrations — that is `odoo-migrator`."*
2. **Inputs before procedure.** The body starts with *what to read first* (`.roots/` docs, the grove
   playbook skill, `forest.json`), because a subagent boots with an empty context.

## Import into a project

```bash
cp roots_seed/agents/<name>.md <repo>/.roots/agents/     # store (tracked)
cp <repo>/.roots/agents/<name>.md <repo>/.claude/agents/ # activation (local)
```

Or both at once with `scripts/sync-agents-skills.sh` (see `scripts/README.md`).
