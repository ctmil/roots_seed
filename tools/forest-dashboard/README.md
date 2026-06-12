# forest-dashboard

> Real-time web dashboard of the state of a **Forest** of repos (Trees) mounted with **bare+worktrees** and their `.roots` memory. Module of the `roots_seed` toolkit. Vocabulary: **Roots → Forest → Grove → Tree → Branch**.

Designed to **detach from the IDE / Antigravity**: it is a control panel in the browser, running the same locally or on a remote server over SSH. The scraping logic is portable and the JSON contract is meant to be reused from an Odoo backend (`odoo_moldeo_sync`).

---

## Architecture (3 layers)

```
collect.py   →   state.json   →   index.html
(collector)      (contract)       (view)
```

- **`collect.py`** — scans the workspace (git + `.roots`) and emits the **state model** (`state.json`). No dependencies (stdlib + `git`). It is the reusable contract: the same *shape* that Odoo should produce from its models.
- **`serve.py`** — lightweight server (stdlib `http.server`) that regenerates the state live (cached with TTL) and serves the view. Equivalent to an Odoo controller.
- **`index.html`** — single view (HTML+CSS+vanilla JS), auto-refresh. Its structure maps to Odoo views (see below).

## Local use

```bash
# from the root of the workspace to monitor:
python3 roots_seed/main/tools/forest-dashboard/serve.py --root .
# → http://127.0.0.1:8787/
```

Or a static snapshot of the model:

```bash
python3 .../forest-dashboard/collect.py --root . -o state.json
```

## Remote use

**Recommended — SSH tunnel (zero exposure, zero auth):**

```bash
# on the server:
python3 .../forest-dashboard/serve.py --root /srv/workspace      # bind 127.0.0.1
# on your machine:
ssh -L 8787:127.0.0.1:8787 user@server
# open http://localhost:8787
```

**Exposed LAN (with token):**

```bash
python3 .../forest-dashboard/serve.py --root . --host 0.0.0.0 --token MYSECRET
# open http://<server>:8787/?token=MYSECRET
```

### `serve.py` options

| Flag | Default | What it does |
|------|---------|----------|
| `--root` | cwd | workspace to scan |
| `--host` | `127.0.0.1` | bind; `0.0.0.0` = exposed |
| `--port` | `8787` | port |
| `--ttl` | `15` | state cache seconds (avoids re-scanning on each poll) |
| `--token` | — | protects `/state.json` when you expose on LAN |

## What it shows

The dashboard has **two views** (switch in the header): **Feed** (aggregate of the whole Forest) and **Forest map** (Groves → Trees → Branches + SVG graph of `relations`, with `vendor`/`kind` badges).

The **Feed** view, in human reading order:

1. **① Changes** — timeline of every module's `journal` (diary entry with date, icon and module), most recent first.
2. **② Tasks** — pending items (`- [ ]`) grouped by module, ordered by recent modification.
3. **③ Docs** — each module's markdown, **rendered** inline (lazy-loaded via `/file`), with a **"view description ↗"** link to the Odoo module's `static/description/index.html`.
4. **④ Skills · Hooks · Debug** — always collapsed, lazy-loaded on open.

At the top, a strip of **metrics** (Trees · Groves · vendors · relations) + a **Forest · git** dropdown (status per Branch: branch, ahead/behind, dirty).

Reading behavior:
- **Recursive discovery**: finds every `.roots` with a `context.md` at any depth (root worktree and/or nested subfolders).
- **Expand what's recent**: the most recently modified modules start expanded (first screen); the rest, collapsed + lazy.
- **Odoo icons**: if the module has `static/description/icon.png`, it is shown next to its name.
- The expand/collapse you do is preserved across refreshes.

### File endpoint

`serve.py` exposes `GET /file?path=<rel>` to serve workspace files (icons, `.md`, description `index.html`) with an **anti-traversal guard** (the real target must stay inside `--root`). The `.md` files are served as plain text and the front-end renders them with its own markdown parser (no dependencies).

## Mapping to Odoo (odoo_moldeo_sync / odoo_moldeo_htree)

The `state.json` is the bridge. Each part of the view has its Odoo equivalent:

| View (this module) | Odoo |
|---------------------|------|
| `metrics` | dashboard cards / `ir.actions.client` |
| `Tree` (repo, tree node) | kanban card / **htree** grouper |
| `Branch` (worktree, row) | list line (`one2many`) with badges |
| `Grove` (product/suite) | kanban group / category |
| `relations[]` (graph) | dependency diagram / `ir.actions` |
| collapsible Forest→Grove→Tree→Branch→.roots hierarchy | the **htree** pattern |

To port: `odoo_moldeo_sync` produces the same JSON from its models (an endpoint/controller), and the OWL/QWeb view consumes the identical contract. The scraping part (`collect.py`) can live as a service/cron feeding those models.

## Requirements

- Python 3.8+ (stdlib only)
- `git` in PATH
- Repos mounted with bare+worktrees (e.g. via `setup-module.sh` / `setupbranch.sh`)
