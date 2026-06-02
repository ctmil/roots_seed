#!/bin/bash
set -e

# Levanta el forest-dashboard apuntando a ESTE workspace y abre el browser.
#
# Uso:
#   ./dashboard.sh                  # puerto 8787, abre el navegador
#   PORT=9000 ./dashboard.sh        # otro puerto
#   ./dashboard.sh --host 0.0.0.0 --token X   # flags extra van a serve.py
#
# El server queda en primer plano; Ctrl-C lo corta.

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
SERVE="$SCRIPT_DIR/roots_seed/main/tools/forest-dashboard/serve.py"
PORT="${PORT:-8787}"
URL="http://127.0.0.1:$PORT/"

if [ ! -f "$SERVE" ]; then
  echo "✗ No encuentro el visor en: $SERVE"
  exit 1
fi

# Abrir el navegador cuando el server ya esté arriba (en segundo plano).
( sleep 1.5
  if   command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
  elif command -v open     >/dev/null 2>&1; then open "$URL"
  else echo "→ Abrí manualmente: $URL"
  fi ) >/dev/null 2>&1 &

echo "▶ Abriendo dashboard de flota Moldeo → $URL"
exec python3 "$SERVE" --root "$SCRIPT_DIR" --port "$PORT" "$@"
