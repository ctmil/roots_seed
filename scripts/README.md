# scripts

> `roots_seed` toolkit scripts to mount and operate a **Forest workspace** (several repos as bare+worktrees) on which the persistent `.roots/` memory lives. They are **templates**: copied to the workspace root and run from there.

---

## Concept

The `.roots/` memory does not live in thin air: it lives in repos. These scripts build the physical substrate (repos as **bare + worktrees**, one `.bare` per repo and one worktree per version/branch) and provide tools to coordinate it. They complement `tools/forest-dashboard/` (the viewer).

## Scripts

| Script | What it does |
|--------|----------|
| `setup-module.sh` | Clones a repo as **bare** and adds worktrees per branch. `./setup-module.sh <name> <git_url> <branch...>` |
| `setupbranch.sh` | Adds a worktree for a specific branch in an already-mounted repo (auto-detects: checkout if it exists local/origin, creates it otherwise). `./setupbranch.sh <module>[/<folder>] -b <branch> [<base>]` |
| `dashboard.sh` | Brings up `tools/forest-dashboard` pointing at the workspace and opens the browser. `./dashboard.sh` (see flags in the script header) |

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
