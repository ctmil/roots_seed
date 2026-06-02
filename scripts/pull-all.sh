#!/bin/bash
set -e

# Uso: ./pull-all.sh <modulo> [<modulo2> ...]
#  ó:  ./pull-all.sh --all          # todos los módulos bare+worktree del workspace
#
# Hace "pull de TODAS las ramas" de un repo montado con bare+worktrees
# (ver setup-module.sh). Es fast-forward ONLY: nunca crea merge commits ni
# reescribe historia. Si una rama divergió o el worktree tiene cambios sin
# commitear, la saltea con aviso y sigue con las demás.
#
# Cómo funciona (mismo método para cada módulo):
#   1. Un único  `git fetch --all --prune`  (actualiza refs remotos, no toca disco).
#   2. Ramas CON checkout (worktrees):  `git merge --ff-only origin/<b>` en su worktree.
#   3. Ramas SIN checkout:              `git fetch . origin/<b>:<b>`  (ff del ref, sin checkout).
#
# Ej:  ./pull-all.sh meli_oerp_stock
#      ./pull-all.sh --all

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

# --- Resolver lista de módulos ----------------------------------------------
if [ "$1" = "--all" ]; then
  MODULES=()
  for d in "$SCRIPT_DIR"/*/; do
    [ -e "$d/.bare" ] && MODULES+=("$(basename "$d")")
  done
  [ ${#MODULES[@]} -eq 0 ] && { echo "✗ No hay módulos bare+worktree en $SCRIPT_DIR"; exit 1; }
elif [ $# -ge 1 ]; then
  MODULES=("$@")
else
  echo "✗ Uso: ./pull-all.sh <modulo> [<modulo2> ...]   |   ./pull-all.sh --all"
  exit 1
fi

# --- Pull de un módulo ------------------------------------------------------
pull_module() {
  local NAME="$1"
  local ROOT="$SCRIPT_DIR/$NAME"

  if [ ! -e "$ROOT/.bare" ]; then
    echo "✗ '$NAME' no es un repo bare+worktree (falta $ROOT/.bare)"; return 1
  fi

  echo "══ $NAME ══"
  git -C "$ROOT" fetch --all --prune --quiet

  # Mapa rama -> ruta del worktree que la tiene en checkout.
  declare -A WT
  local wt="" br=""
  while IFS= read -r line; do
    case "$line" in
      worktree\ *) wt="${line#worktree }" ;;
      branch\ refs/heads/*) br="${line#branch refs/heads/}"; WT["$br"]="$wt" ;;
      "") wt=""; br="" ;;
    esac
  done < <(git -C "$ROOT" worktree list --porcelain)

  local up=0 ok=0 skip=0
  local b
  for b in $(git -C "$ROOT" for-each-ref --format='%(refname:short)' refs/heads); do
    # ¿Existe la rama en origin?
    if ! git -C "$ROOT" rev-parse --verify -q "origin/$b" >/dev/null; then
      printf "  ~ %-12s (sin rama remota, se omite)\n" "$b"; skip=$((skip+1)); continue
    fi
    # ¿Ya está al día?
    local behind
    behind=$(git -C "$ROOT" rev-list --count "$b..origin/$b")
    if [ "$behind" -eq 0 ]; then
      printf "  · %-12s al día\n" "$b"; ok=$((ok+1)); continue
    fi

    if [ -n "${WT[$b]+x}" ]; then
      # Rama con checkout: ff-merge dentro de su worktree.
      if git -C "${WT[$b]}" merge --ff-only "origin/$b" >/dev/null 2>&1; then
        printf "  ✓ %-12s +%s (worktree)\n" "$b" "$behind"; up=$((up+1))
      else
        printf "  ✗ %-12s no se pudo ff (¿cambios locales o divergió?), se omite\n" "$b"; skip=$((skip+1))
      fi
    else
      # Rama sin checkout: ff del ref directamente.
      if git -C "$ROOT" fetch --quiet . "origin/$b:$b" 2>/dev/null; then
        printf "  ✓ %-12s +%s\n" "$b" "$behind"; up=$((up+1))
      else
        printf "  ✗ %-12s no se pudo ff (divergió), se omite\n" "$b"; skip=$((skip+1))
      fi
    fi
  done
  echo "  → actualizadas:$up  al-día:$ok  omitidas:$skip"
}

# --- Recorrer módulos -------------------------------------------------------
rc=0
for m in "${MODULES[@]}"; do
  pull_module "$m" || rc=1
done
exit $rc
