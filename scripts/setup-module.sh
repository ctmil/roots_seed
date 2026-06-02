#!/bin/bash
set -e

# Uso: ./setup-module.sh <nombre> <git_url> <branch1> [branch2] ...
# Ej:  ./setup-module.sh meli_oerp git@github.com:ctmil/meli_oerp.git 19.0 18.0 17.0 16.0

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

NAME="$1"; URL="$2"; shift 2
BRANCHES=("$@")
ROOT="$SCRIPT_DIR/$NAME"

if [ -e "$ROOT/.bare" ]; then
  echo "✗ '$ROOT' ya está inicializado (.bare existe)."
  echo "  Si querés agregar branches, usá: git -C '$ROOT' worktree add <branch> <branch>"
  exit 1
fi

mkdir -p "$ROOT" && cd "$ROOT"
git clone --bare "$URL" .bare
echo "gitdir: ./.bare" > .git
git --git-dir=.bare config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
git --git-dir=.bare fetch origin

for b in "${BRANCHES[@]}"; do
  git worktree add "$b" "$b"
  echo "✓ worktree $NAME/$b"
done

echo "Listo: $ROOT"
git worktree list
