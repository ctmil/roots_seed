# fleet-dashboard

> Dashboard web en tiempo real del estado de una flota de repos montados con **bare+worktrees** y su memoria `.roots`. Módulo del toolkit `roots_seed`.

Pensado para **despegarse del IDE / Antigravity**: es un panel de control en el browser, que corre igual en local o en un server remoto vía SSH. La lógica de scraping es portable y el contrato JSON está pensado para reusarse desde un backend Odoo (`odoo_moldeo_sync`).

---

## Arquitectura (3 capas)

```
collect.py   →   state.json   →   index.html
(colector)       (contrato)       (vista)
```

- **`collect.py`** — escanea el workspace (git + `.roots`) y emite el **modelo de estado** (`state.json`). Sin dependencias (stdlib + `git`). Es el contrato reusable: el mismo *shape* que Odoo debería producir desde sus modelos.
- **`serve.py`** — server liviano (stdlib `http.server`) que regenera el estado en vivo (cacheado con TTL) y sirve la vista. Equivale a un controller de Odoo.
- **`index.html`** — vista única (HTML+CSS+JS vanilla), auto-refresh. Su estructura mapea a vistas Odoo (ver abajo).

## Uso local

```bash
# desde la raíz del workspace a monitorear:
python3 roots_seed/main/tools/fleet-dashboard/serve.py --root .
# → http://127.0.0.1:8787/
```

O snapshot estático del modelo:

```bash
python3 .../fleet-dashboard/collect.py --root . -o state.json
```

## Uso remoto

**Recomendado — túnel SSH (cero exposición, cero auth):**

```bash
# en el server:
python3 .../fleet-dashboard/serve.py --root /srv/workspace      # bind 127.0.0.1
# en tu máquina:
ssh -L 8787:127.0.0.1:8787 user@server
# abrí http://localhost:8787
```

**LAN expuesta (con token):**

```bash
python3 .../fleet-dashboard/serve.py --root . --host 0.0.0.0 --token MISECRETO
# abrí http://<server>:8787/?token=MISECRETO
```

### Opciones de `serve.py`

| Flag | Default | Qué hace |
|------|---------|----------|
| `--root` | cwd | workspace a escanear |
| `--host` | `127.0.0.1` | bind; `0.0.0.0` = expuesto |
| `--port` | `8787` | puerto |
| `--ttl` | `15` | seg. de cache del estado (evita re-escaneo en cada poll) |
| `--token` | — | protege `/state.json` cuando exponés en LAN |

## Qué muestra

Vista principal = **feed agregado de toda la flota**, en orden de lectura humana:

1. **① Cambios** — timeline del `journal` de todos los módulos (entrada de diary con fecha, ícono y módulo), más reciente primero.
2. **② Tareas** — pendientes (`- [ ]`) agrupadas por módulo, ordenadas por modificación reciente.
3. **③ Docs** — markdown de cada módulo, **renderizado** inline (carga lazy vía `/file`), con link **"ver descripción ↗"** al `static/description/index.html` del módulo Odoo.
4. **④ Skills · Hooks · Debug** — siempre colapsados, carga lazy al abrir.

Arriba, una tira de **métricas** + un desplegable **Flota · git** (estado por worktree: branch, ahead/behind, dirty).

Comportamiento de lectura:
- **Descubrimiento recursivo**: encuentra cada `.roots` con `context.md` a cualquier profundidad (worktree raíz y/o subcarpetas anidadas).
- **Expandir lo reciente**: los módulos modificados más recientemente arrancan expandidos (primera pantalla); el resto, colapsados + lazy.
- **Íconos Odoo**: si el módulo tiene `static/description/icon.png`, se muestra junto a su nombre.
- El expand/colapso que hagas se preserva entre refrescos.

### Endpoint de archivos

`serve.py` expone `GET /file?path=<rel>` para servir archivos del workspace (íconos, `.md`, `index.html` de descripción) con **guarda anti-traversal** (el target real debe quedar dentro de `--root`). Los `.md` se sirven como texto plano y el front los renderiza con un parser markdown propio (sin dependencias).

## Mapeo a Odoo (odoo_moldeo_sync / odoo_moldeo_htree)

El `state.json` es el puente. Cada parte de la vista tiene su equivalente Odoo:

| Vista (este módulo) | Odoo |
|---------------------|------|
| `metrics` | tarjetas de dashboard / `ir.actions.client` |
| `repo` (nodo del árbol) | kanban card / agrupador **htree** |
| `worktree` (fila) | línea de lista (`one2many`) con badges |
| `project` | registro de "proyecto de desarrollo" cross-módulo |
| jerarquía colapsable Flota→repo→worktree→.roots | el patrón **htree** |

Para portar: `odoo_moldeo_sync` produce el mismo JSON desde sus modelos (un endpoint/controller), y la vista OWL/QWeb consume idéntico contrato. La parte de scraping (`collect.py`) puede vivir como servicio/cron que alimenta esos modelos.

## Requisitos

- Python 3.8+ (solo stdlib)
- `git` en PATH
- Los repos montados con bare+worktrees (ej. vía `setup-module.sh` / `setupbranch.sh`)
