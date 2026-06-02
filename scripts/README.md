# scripts

> Scripts del toolkit `roots_seed` para montar y operar un **workspace de flota** (varios repos como bare+worktrees) sobre el que vive la memoria persistente `.roots/`. Son **plantillas**: se copian a la raíz del workspace y se ejecutan desde ahí.

---

## Concepto

La memoria `.roots/` no vive en el aire: vive en repos. Estos scripts arman el sustrato físico (repos como **bare + worktrees**, un `.bare` por repo y un worktree por versión/branch) y dan herramientas para coordinarlo. Complementan a `tools/forest-dashboard/` (el visor).

## Scripts

| Script | Qué hace |
|--------|----------|
| `setup-module.sh` | Clona un repo como **bare** y agrega worktrees por branch. `./setup-module.sh <nombre> <git_url> <branch...>` |
| `setupbranch.sh` | Agrega un worktree para un branch específico en un repo ya montado (auto-detecta: checkout si existe local/origin, crea si no). `./setupbranch.sh <modulo>[/<carpeta>] -b <branch> [<base>]` |
| `dashboard.sh` | Levanta `tools/forest-dashboard` apuntando al workspace y abre el navegador. `./dashboard.sh` (ver flags en el header del script) |

## Uso

Estas plantillas asumen estar **en la raíz del workspace** (la carpeta que contiene los repos). Para un workspace nuevo:

```bash
cp roots_seed/main/scripts/*.sh .        # traer las herramientas a la raíz
./setup-module.sh meli_oerp git@github.com:ctmil/meli_oerp.git 17.0 19.0
./setupbranch.sh meli_oerp/feat -b claude/mi-feature
./dashboard.sh                            # visor de la flota
```

> `dashboard.sh` espera encontrar el visor en `roots_seed/main/tools/forest-dashboard/serve.py` relativo a la raíz del workspace. Ajustá el path si tu layout difiere.

## Patrón bare + worktrees

```
<repo>/
├── .bare/      ← repo git bare (objetos compartidos entre worktrees)
├── .git        ← "gitdir: ./.bare"
├── 17.0/       ← worktree del branch 17.0
└── 19.0/       ← worktree del branch 19.0
```

Ventaja: los objetos git se comparten entre versiones del mismo repo (no se duplica historial), optimizando espacio local.
