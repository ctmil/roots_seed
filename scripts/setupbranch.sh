#!/bin/bash
set -e

# Uso: ./setupbranch.sh <modulo>[/<carpeta_worktree>] -b <branch> [<base>]
#  ó:  ./setupbranch.sh <modulo>[/<carpeta_worktree>] <branch> [<base>]
#
# Agrega un worktree a un repo (montado con bare+worktrees por setup-module.sh).
# Auto-detecta el branch: si existe (local u origin) lo hace checkout;
# si no existe, lo crea a partir de <base> (o de HEAD si no se indica).
#
# Ej:  ./setupbranch.sh moldeomint/off -b claude/odooconnectorfullfillmentbranch
#       → crea moldeomint/off/ apuntando a ese branch
#      ./setupbranch.sh meli_oerp 19.0
#       → crea meli_oerp/19.0/ (carpeta = nombre del branch, '/' → '-')

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

# --- Parseo de argumentos ---------------------------------------------------
TARGET=""; BRANCH=""; BASE=""
while [ $# -gt 0 ]; do
  case "$1" in
    -b|--branch) BRANCH="$2"; shift 2 ;;
    -h|--help) sed -n '3,18p' "$0"; exit 0 ;;
    *)
      if   [ -z "$TARGET" ]; then TARGET="$1"
      elif [ -z "$BRANCH" ]; then BRANCH="$1"
      elif [ -z "$BASE"   ]; then BASE="$1"
      else echo "✗ Argumento de más: $1"; exit 1
      fi
      shift ;;
  esac
done

if [ -z "$TARGET" ] || [ -z "$BRANCH" ]; then
  echo "✗ Uso: ./setupbranch.sh <modulo>[/<carpeta_worktree>] -b <branch> [<base>]"
  exit 1
fi

# --- Resolver módulo y carpeta del worktree ---------------------------------
# TARGET puede ser "modulo" o "modulo/carpeta".
MODULE="${TARGET%%/*}"                      # parte antes del primer '/'
if [ "$TARGET" = "$MODULE" ]; then
  WT="${BRANCH//\//-}"                       # sin carpeta explícita: branch con '/' → '-'
else
  WT="${TARGET#*/}"                          # parte después del primer '/'
fi

ROOT="$SCRIPT_DIR/$MODULE"

if [ ! -e "$ROOT/.bare" ]; then
  echo "✗ '$MODULE' no está inicializado (no existe $ROOT/.bare)."
  echo "  Inicializalo primero con: ./setup-module.sh $MODULE <git_url> <branch...>"
  exit 1
fi

if [ -e "$ROOT/$WT" ]; then
  echo "✗ Ya existe '$ROOT/$WT'. Elegí otra carpeta o borrá el worktree existente."
  echo "  (Para listar: git -C '$ROOT' worktree list)"
  exit 1
fi

# --- Sincronizar refs (best-effort, no bloquea si está offline) -------------
echo "→ Fetch de origin en $MODULE…"
git -C "$ROOT" fetch origin --prune || echo "⚠ fetch falló (¿offline?); sigo con refs locales."

# --- Decidir cómo materializar el branch ------------------------------------
if git -C "$ROOT" show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "→ Branch local '$BRANCH' existe → checkout en worktree."
  git -C "$ROOT" worktree add "$WT" "$BRANCH"

elif git -C "$ROOT" show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  echo "→ Branch 'origin/$BRANCH' existe → creo local con tracking."
  git -C "$ROOT" worktree add --track -b "$BRANCH" "$WT" "origin/$BRANCH"

else
  START="${BASE:-HEAD}"
  echo "→ Branch '$BRANCH' no existe → lo creo nuevo desde '$START'."
  git -C "$ROOT" worktree add -b "$BRANCH" "$WT" "$START"
fi

echo "✓ Worktree listo: $MODULE/$WT  →  $BRANCH"
git -C "$ROOT" worktree list
