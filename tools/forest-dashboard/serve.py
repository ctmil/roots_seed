#!/usr/bin/env python3
"""Servidor liviano del forest-dashboard.

- GET /            → index.html (la vista)
- GET /state.json  → modelo de estado en vivo (cacheado con TTL)
- GET /state.json?fresh=1 → fuerza re-escaneo

Sin dependencias externas (stdlib). La lógica de scraping vive en collect.py;
este server solo orquesta + cachea, igual que haría un controller de Odoo.

Local:
  python3 serve.py --root /ruta/al/workspace

Remoto (recomendado: túnel SSH, cero exposición / cero auth):
  # en el server:
  python3 serve.py --root /srv/workspace          # bind 127.0.0.1
  # en tu máquina:
  ssh -L 8787:127.0.0.1:8787 user@server          # luego abrí http://localhost:8787

Remoto en LAN (expuesto — usar token):
  python3 serve.py --root . --host 0.0.0.0 --token MISECRETO
  # abrí http://<server>:8787/?token=MISECRETO
"""
import argparse
import json
import mimetypes
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import collect  # mismo directorio

HERE = os.path.dirname(os.path.abspath(__file__))
_cache = {"ts": 0.0, "data": None}
_lock = threading.Lock()


def get_state(ttl, fresh=False):
    now = time.time()
    with _lock:
        if not fresh and _cache["data"] is not None and (now - _cache["ts"]) < ttl:
            return _cache["data"], True
    data = collect.collect_state()  # scan fuera del lock
    with _lock:
        _cache["data"] = data
        _cache["ts"] = time.time()
    return data, False


class Handler(BaseHTTPRequestHandler):
    ttl = 15
    token = None

    def _send(self, code, body, ctype):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _ok_token(self, qs):
        if not self.token:
            return True
        return qs.get("token", [""])[0] == self.token

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        route = parsed.path

        if route in ("/", "/index.html"):
            try:
                with open(os.path.join(HERE, "index.html"), "rb") as fh:
                    self._send(200, fh.read(), "text/html; charset=utf-8")
            except OSError:
                self._send(404, "index.html no encontrado", "text/plain")
            return

        if route == "/state.json":
            if not self._ok_token(qs):
                self._send(403, "token inválido", "text/plain")
                return
            data, hit = get_state(self.ttl, fresh=qs.get("fresh", ["0"])[0] == "1")
            data = dict(data, _cache_hit=hit)
            self._send(200, json.dumps(data, ensure_ascii=False),
                       "application/json; charset=utf-8")
            return

        # Sirve archivos del workspace (íconos, .md, index.html de descripción)
        # con guarda anti-traversal: el target real debe quedar dentro de ROOT.
        if route == "/file":
            if not self._ok_token(qs):
                self._send(403, "token inválido", "text/plain")
                return
            relpath = qs.get("path", [""])[0]
            base = os.path.realpath(collect.ROOT)
            target = os.path.realpath(os.path.join(base, relpath))
            if not (target == base or target.startswith(base + os.sep)) or not os.path.isfile(target):
                self._send(404, "archivo no encontrado", "text/plain")
                return
            ctype, _ = mimetypes.guess_type(target)
            if target.endswith(".md"):
                ctype = "text/plain; charset=utf-8"   # el front renderiza el markdown
            elif ctype is None:
                ctype = "application/octet-stream"
            try:
                with open(target, "rb") as fh:
                    self._send(200, fh.read(), ctype)
            except OSError:
                self._send(404, "no se pudo leer", "text/plain")
            return

        self._send(404, "not found", "text/plain")

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd(), help="workspace a escanear (default: cwd)")
    ap.add_argument("--host", default="127.0.0.1", help="bind host (0.0.0.0 = expuesto)")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--ttl", type=int, default=15, help="segundos de cache del estado")
    ap.add_argument("--token", default=None, help="protege /state.json en exposición LAN")
    args = ap.parse_args()

    collect.ROOT = os.path.abspath(args.root)
    Handler.ttl = args.ttl
    Handler.token = args.token

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"▶ forest-dashboard  root={collect.ROOT}")
    print(f"  http://{args.host}:{args.port}/   (TTL={args.ttl}s)")
    if args.host == "0.0.0.0" and not args.token:
        print("  ⚠ bind 0.0.0.0 SIN token: cualquiera en la red ve el estado. Usá --token o túnel SSH.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ detenido")
        srv.shutdown()


if __name__ == "__main__":
    main()
