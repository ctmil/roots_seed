# scripts

> `roots_seed` toolkit scripts to mount and operate a **Forest workspace** (several repos as bare+worktrees) on which the persistent `.roots/` memory lives. They are **templates**: copied to the workspace root and run from there.

---

## Concept

The `.roots/` memory does not live in thin air: it lives in repos. These scripts build the physical substrate (repos as **bare + worktrees**, one `.bare` per repo and one worktree per version/branch) and provide tools to coordinate it. They complement `tools/forest-dashboard/` (the viewer).

## Scripts

| Script | What it does |
|--------|----------|
| `install-macos.sh` | **Bootstraps a whole workspace on macOS**: Command Line Tools, Homebrew, the terminal toolchain, Claude Code (optionally the Desktop app), the fleet scripts, a lazy `.roots/`, the `.gitignore` rules and the entry points. Idempotent; `--check` diagnoses without changing anything |
| `setup-module.sh` | Clones a repo as **bare** and adds worktrees per branch. `./setup-module.sh <name> <git_url> <branch...>` |
| `setupbranch.sh` | Adds a worktree for a specific branch in an already-mounted repo (auto-detects: checkout if it exists local/origin, creates it otherwise). `./setupbranch.sh <module>[/<folder>] -b <branch> [<base>]` |
| `sync-agents-skills.sh` | Moves agents/skills between **base → store → activation**, converting the skill layout (`<name>.md` ↔ `<name>/SKILL.md`). `check` reports drift and exits non-zero |
| `dashboard.sh` | Brings up `tools/forest-dashboard` pointing at the workspace and opens the browser. `./dashboard.sh` (see flags in the script header) |

## Bootstrap on macOS

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/ctmil/roots_seed/main/scripts/install-macos.sh)"
# or, from a checkout:
./install-macos.sh --workspace ~/forest --profile standard --desktop
./install-macos.sh --check          # what is installed / missing
```

It installs a GNU-ish toolchain on purpose (`coreutils`, `gnu-sed`, `gawk`, `bash` 5.x): stock macOS
ships **bash 3.2** and **BSD** sed/awk/date, which is where portable scripts silently break — on
macOS `sed -i` *requires* an argument. The script points this out and offers to put the `gnubin`
paths first in your shell.

> Linux/WSL need no installer: clone the seed and run `setup-module.sh` directly.

## Use

These templates assume being **at the workspace root** (the folder that contains the repos). For a new workspace:

```bash
cp roots_seed/main/scripts/*.sh .        # bring the tools to the root
./setup-module.sh meli_oerp git@github.com:ctmil/meli_oerp.git 17.0 19.0
./setupbranch.sh meli_oerp/feat -b claude/my-feature
./dashboard.sh                            # Forest viewer
```

> `dashboard.sh` expects to find the viewer at `roots_seed/main/tools/forest-dashboard/serve.py` relative to the workspace root. Adjust the path if your layout differs.

## bare + worktrees pattern

```
<repo>/
├── .bare/      ← bare git repo (objects shared across worktrees)
├── .git        ← "gitdir: ./.bare"
├── 17.0/       ← worktree of branch 17.0
└── 19.0/       ← worktree of branch 19.0
```

Advantage: git objects are shared across versions of the same repo (history is not duplicated), optimizing local space.
