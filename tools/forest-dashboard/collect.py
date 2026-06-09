#!/usr/bin/env python3
"""Colector de estado de un Forest de repos (Trees, bare+worktrees) + su memoria .roots.

Produce el MODELO de estado (state.json) que es el contrato reusable: el mismo
shape que un backend Odoo (odoo_moldeo_sync) debería emitir desde sus modelos
para reusar la misma vista. Trae el FEED AGREGADO (CAMBIOS → TAREAS → DOCS →
skills/hooks/debug) y los ejes Forest (groves/vendors/relations + grove/vendor/
kind/org por Tree) leídos de forest.json. Vocabulario: Roots > Forest > Grove >
Tree > Branch.

Root configurable:  FOREST_ROOT=/path (ó FLEET_ROOT, compat)  ó  --root /path  ó  cwd
Uso:  python3 collect.py --root /workspace [-o state.json]

Sin dependencias externas (stdlib + git en PATH).
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.environ.get("FOREST_ROOT") or os.environ.get("FLEET_ROOT") or os.getcwd())
VERSION_RE = re.compile(r"^\d+\.\d+$")
YEAR_NOW = datetime.now().year

MONTHS = {m: i + 1 for i, m in enumerate([
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
    "septiembre", "octubre", "noviembre", "diciembre"])}
MONTHS["setiembre"] = 9


def run(args, cwd=None, timeout=30):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except Exception:
        return ""


def rel(path):
    return os.path.relpath(path, ROOT)


# --------------------------------------------------------------------------- #
# Lectura de .roots
# --------------------------------------------------------------------------- #
def _first_match(path, pattern, group=0):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.search(pattern, line)
                if m:
                    return m.group(group).strip()
    except OSError:
        pass
    return None


def _parse_date_key(text, fallback_mtime=0.0):
    """De 'DD Mes [YYYY]' a una clave ordenable (year, month, day)."""
    m = re.search(r"(\d{1,2})\s+([A-Za-zÁÉÍÓÚáéíóú]+)(?:\s+(\d{4}))?", text or "")
    if m:
        day = int(m.group(1))
        month = MONTHS.get(m.group(2).lower(), 0)
        year = int(m.group(3)) if m.group(3) else YEAR_NOW
        if month:
            return (year, month, day, fallback_mtime)
    return (0, 0, 0, fallback_mtime)


def parse_journal(roots_dir, cap=12):
    """Entradas del diary (header '**fecha** - resumen' + cuerpo)."""
    diary = os.path.join(roots_dir, "journal", "diary.md")
    if not os.path.isfile(diary):
        diary = os.path.join(roots_dir, "diary.md")
    if not os.path.isfile(diary):
        return []
    mtime = os.path.getmtime(diary)
    entries, cur = [], None
    try:
        with open(diary, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                h = re.match(r"^\*\*(.+?)\*\*\s*[-–—]?\s*(.*)$", line)
                if h:
                    if cur:
                        entries.append(cur)
                    cur = {"date_raw": h.group(1).strip(),
                           "summary": h.group(2).strip(), "body": ""}
                elif cur and line.strip() and not cur["summary"]:
                    cur["summary"] = line.strip()
                elif cur and line.strip():
                    if len(cur["body"]) < 280:
                        cur["body"] += (" " if cur["body"] else "") + line.strip()
    except OSError:
        return []
    if cur:
        entries.append(cur)
    for e in entries:
        e["date_key"] = _parse_date_key(e["date_raw"], mtime)
    entries.sort(key=lambda e: e["date_key"], reverse=True)
    return entries[:cap]


def parse_tasks(roots_dir, cap=30):
    """Tareas abiertas '- [ ]' y conteo de hechas '- [x]' en tasks/."""
    files = []
    td = os.path.join(roots_dir, "tasks")
    if os.path.isdir(td):
        files = [os.path.join(td, f) for f in os.listdir(td) if f.endswith(".md")]
    else:
        files = [os.path.join(roots_dir, f) for f in ("todo.md", "tasks.md")]
    open_t, done = [], 0
    for p in files:
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    mo = re.match(r"\s*-\s\[ \]\s+(.*)", line)
                    if mo:
                        open_t.append(mo.group(1).strip())
                    elif re.match(r"\s*-\s\[[xX]\]", line):
                        done += 1
        except OSError:
            pass
    return {"open": open_t[:cap], "open_total": len(open_t), "done": done}


def index_md(dirpath):
    """Lista de {path, title, name} de los .md de un directorio."""
    out = []
    if not os.path.isdir(dirpath):
        return out
    for f in sorted(os.listdir(dirpath)):
        if not f.endswith(".md"):
            continue
        p = os.path.join(dirpath, f)
        out.append({"path": rel(p), "name": f,
                    "title": _first_match(p, r"^#\s+(.*)", 1) or f})
    return out


def parse_collective(roots_dir, cap=60):
    """Lee collective/ (memoria permanente de influencias/referencias, ≠ workbench):
    familias = subcarpetas, cada una con su README (título) + fichas .md. Devuelve
    {path, title, description, families:[{name,title,description,entries:[...]}], entries:[...]}.
    Ignora README/_modelo*/assets. La biblioteca (library/bibliografia.md, etc.) entra como una familia más."""
    cdir = os.path.join(roots_dir, "collective")
    if not os.path.isdir(cdir):
        return None
    readme = os.path.join(cdir, "README.md")
    out = {
        "path": rel(cdir),
        "title": _first_match(readme, r"^#\s+(.*)", 1) or "Collective",
        "description": _first_match(readme, r"^>\s+(.*)", 1),
        "families": [], "entries": [],
    }
    skip = PRUNE_DIRS | {"assets"}
    for name in sorted(os.listdir(cdir)):
        p = os.path.join(cdir, name)
        if os.path.isfile(p) and name.endswith(".md") and name != "README.md":
            out["entries"].append({"path": rel(p), "name": name,
                                   "title": _first_match(p, r"^#\s+(.*)", 1) or name})
        elif os.path.isdir(p) and name not in skip:
            fam = {"name": name, "path": rel(p),
                   "title": _first_match(os.path.join(p, "README.md"), r"^#\s+(.*)", 1) or name,
                   "description": _first_match(os.path.join(p, "README.md"), r"^>\s+(.*)", 1),
                   "entries": []}
            for dp, dns, fns in os.walk(p):
                dns[:] = [d for d in dns if d not in skip]
                for f in sorted(fns):
                    if (f.endswith(".md") and f != "README.md"
                            and not f.startswith("_modelo")):
                        fp = os.path.join(dp, f)
                        fam["entries"].append({"path": rel(fp), "name": f,
                                               "title": _first_match(fp, r"^#\s+(.*)", 1) or f})
                if len(fam["entries"]) >= cap:
                    break
            out["families"].append(fam)
    return out


def summarize_roots(roots_dir):
    if not os.path.isdir(roots_dir):
        return None
    ctx = os.path.join(roots_dir, "context.md")
    err = os.path.join(roots_dir, "debug", "errors-log.md")
    if not os.path.isfile(err):
        err = os.path.join(roots_dir, "errors-log.md")
    s = {
        "path": rel(roots_dir),
        "title": _first_match(ctx, r"^#\s+(.*)", 1),
        "description": _first_match(ctx, r"^>\s+(.*)", 1),
        "errors_active": 0,
    }
    if os.path.isfile(err):
        try:
            with open(err, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if re.search(r"\*\*Estado:\*\*.*(Activo|Investigando|En progreso)", line):
                        s["errors_active"] += 1
        except OSError:
            pass
    meta_p = os.path.join(roots_dir, "_meta.json")
    if os.path.isfile(meta_p):
        try:
            with open(meta_p, encoding="utf-8") as fh:
                s["meta"] = json.load(fh)
        except (OSError, json.JSONDecodeError):
            s["meta"] = None
    return s


def roots_mtime(roots_dir):
    """mtime más reciente dentro de un .roots (para ordenar por modificación)."""
    latest = 0.0
    for dp, _, fns in os.walk(roots_dir):
        for f in fns:
            try:
                latest = max(latest, os.path.getmtime(os.path.join(dp, f)))
            except OSError:
                pass
    return latest


# --------------------------------------------------------------------------- #
# Git — worktrees
# --------------------------------------------------------------------------- #
def list_worktrees(repo_dir):
    out = run(["git", "-C", repo_dir, "worktree", "list", "--porcelain"])
    wts, cur = [], {}
    for line in out.splitlines():
        if line.startswith("worktree "):
            cur = {"path": line[len("worktree "):]}
        elif line.startswith("branch "):
            cur["branch"] = line[len("branch "):].replace("refs/heads/", "")
        elif line == "bare":
            cur["bare"] = True
        elif line == "":
            if cur and not cur.get("bare"):
                wts.append(cur)
            cur = {}
    if cur and not cur.get("bare"):
        wts.append(cur)
    return wts


def worktree_state(wt):
    path = wt["path"]
    branch = wt.get("branch", "(detached)")
    st = {"path": rel(path), "dir": os.path.basename(path), "branch": branch,
          "is_version": bool(VERSION_RE.match(branch)) or branch == "main"}
    log = run(["git", "-C", path, "log", "-1", "--format=%h%x1f%s%x1f%an%x1f%cr"])
    if log and "\x1f" in log:
        h, subj, an, cr = (log.split("\x1f") + ["", "", "", ""])[:4]
        st["head"], st["commit"] = h, {"subject": subj, "author": an, "date": cr}
    ab = run(["git", "-C", path, "rev-list", "--left-right", "--count", "@{upstream}...HEAD"])
    if ab and len(ab.split()) == 2:
        behind, ahead = ab.split()
        st["behind"], st["ahead"] = int(behind), int(ahead)
    status = run(["git", "-C", path, "status", "--porcelain"], timeout=60)
    st["dirty"] = len([l for l in status.splitlines() if l.strip()])
    return st


# --------------------------------------------------------------------------- #
# Memorias de módulo (unidad de agregación)
# --------------------------------------------------------------------------- #
def odoo_assets(module_dir):
    """icon.png e index.html de static/description/ si existen."""
    desc = os.path.join(module_dir, "static", "description")
    icon = os.path.join(desc, "icon.png")
    idx = os.path.join(desc, "index.html")
    return (rel(icon) if os.path.isfile(icon) else None,
            rel(idx) if os.path.isfile(idx) else None)


PRUNE_DIRS = {".git", ".bare", "node_modules", "__pycache__"}


def is_ns_container(roots):
    """True si el .roots es un contenedor namespaced (deployment): sin context.md
    y con subdirs que tienen _meta.json (= namespaces de cliente). Esos alimentan
    la sección de proyectos, no la de módulos. Todo otro .roots es módulo."""
    if os.path.isfile(os.path.join(roots, "context.md")):
        return False
    try:
        for sub in os.listdir(roots):
            d = os.path.join(roots, sub)
            if os.path.isdir(d) and os.path.isfile(os.path.join(d, "_meta.json")):
                return True
    except OSError:
        pass
    return False


def _record_module(module_dir, roots, repo, version, git):
    """Registro de una memoria de módulo (un .roots con context.md)."""
    icon, index_html = odoo_assets(module_dir)
    is_root = os.path.abspath(module_dir) == os.path.join(ROOT, repo, version) if version else False
    return {
        "module": repo if is_root else os.path.basename(module_dir),
        "repo": repo,
        "version": version,
        "path": rel(module_dir),
        "icon": icon,
        "index_html": index_html,
        "git": git,
        "mtime": roots_mtime(roots),
        "summary": summarize_roots(roots),
        "journal": parse_journal(roots),
        "tasks": parse_tasks(roots),
        "docs": ([d for d in [_ctx_as_doc(roots)] if d]
                 + index_md(os.path.join(roots, "docs"))),
        "skills": index_md(os.path.join(roots, "skills")),
        "hooks": index_md(os.path.join(roots, "hooks")),
        "debug": index_md(os.path.join(roots, "debug")),
        "collective": parse_collective(roots),
    }


def find_module_memories(repos):
    """RECURSIVO: encuentra toda .roots de módulo en la flota, a cualquier
    profundidad (un .roots en la raíz de un worktree y/o uno por subcarpeta
    anidada). Un .roots cuenta como 'memoria de módulo' si tiene context.md;
    las .roots namespaced de deployment (sin context.md) alimentan la sección
    de proyectos, no esta. No se desciende dentro de un .roots (su interior es
    memoria, no módulos).
    """
    wt_git = {}
    for r in repos:
        for wt in r["worktrees"]:
            wt_git[wt["path"]] = {
                "branch": wt["branch"], "is_version": wt["is_version"],
                "ahead": wt.get("ahead"), "behind": wt.get("behind"),
                "dirty": wt.get("dirty"), "head": wt.get("head"),
            }

    mems = []
    for repo in sorted(r["name"] for r in repos):
        repo_dir = os.path.join(ROOT, repo)
        for version in sorted(os.listdir(repo_dir)):
            wt = os.path.join(repo_dir, version)
            if version.startswith(".") or not os.path.isdir(wt):
                continue
            git = wt_git.get(f"{repo}/{version}")
            for dirpath, dirnames, filenames in os.walk(wt):
                dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
                if ".roots" in dirnames:
                    roots = os.path.join(dirpath, ".roots")
                    if not is_ns_container(roots):
                        mems.append(_record_module(dirpath, roots, repo, version, git))
                    dirnames.remove(".roots")  # no descender dentro del .roots
    return mems


def _ctx_as_doc(roots_dir):
    p = os.path.join(roots_dir, "context.md")
    if os.path.isfile(p):
        return {"path": rel(p), "name": "context.md",
                "title": _first_match(p, r"^#\s+(.*)", 1) or "context.md"}
    return None


# --------------------------------------------------------------------------- #
# Flota / proyectos / agregación
# --------------------------------------------------------------------------- #
def load_forest():
    """Lee forest.json (fallback fleet.json/symlink). Devuelve roles por Tree
    (con ejes grove/vendor/kind/org) + groves[]/vendors[]/relations[]."""
    forest = {"roles": {}, "groves": [], "vendors": [], "relations": []}
    p = os.path.join(ROOT, ".roots", "forest.json")
    if not os.path.isfile(p):
        p = os.path.join(ROOT, ".roots", "fleet.json")  # compat
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as fh:
                data = json.load(fh)
            for r in data.get("repos", []):
                forest["roles"][r["name"]] = {
                    "role": r.get("role"), "notes": r.get("notes"),
                    "grove": r.get("grove"), "vendor": r.get("vendor"),
                    "kind": r.get("kind"), "org": r.get("org"),
                }
            forest["groves"] = data.get("groves", [])
            forest["vendors"] = data.get("vendors", [])
            forest["relations"] = data.get("relations", [])
        except (OSError, json.JSONDecodeError, KeyError):
            pass
    return forest


def du_human(path):
    out = run(["du", "-sh", path])
    return out.split("\t")[0] if out else None


def collect_repos(roles):
    repos = []
    for name in sorted(os.listdir(ROOT)):
        repo_dir = os.path.join(ROOT, name)
        if not os.path.isdir(os.path.join(repo_dir, ".bare")):
            continue
        meta = roles.get(name, {})
        repos.append({
            "name": name,
            "role": meta.get("role") or "source",
            # ejes Forest (None si el Tree no está en forest.json todavía)
            "grove": meta.get("grove"),
            "vendor": meta.get("vendor"),
            "kind": meta.get("kind"),
            "org": meta.get("org"),
            "upstream": run(["git", "-C", repo_dir, "config", "--get", "remote.origin.url"]) or None,
            "bare_size": du_human(os.path.join(repo_dir, ".bare")),
            "worktrees": [worktree_state(wt) for wt in list_worktrees(repo_dir)],
        })
    return repos


def collect_projects():
    projects = []
    for repo in sorted(os.listdir(ROOT)):
        repo_dir = os.path.join(ROOT, repo)
        if not os.path.isdir(os.path.join(repo_dir, ".bare")):
            continue
        for ver in sorted(os.listdir(repo_dir)):
            roots = os.path.join(repo_dir, ver, ".roots")
            if not os.path.isdir(roots):
                continue
            for ns in sorted(os.listdir(roots)):
                d = os.path.join(roots, ns)
                if not os.path.isdir(d) or not os.path.isfile(os.path.join(d, "_meta.json")):
                    continue
                s = summarize_roots(d) or {}
                meta = s.get("meta") or {}
                t = parse_tasks(d)
                projects.append({
                    "source": f"{repo}/{ver}", "namespace": ns,
                    "kind": meta.get("mode") or meta.get("working_mode") or "client",
                    "client": meta.get("client"), "module": meta.get("module"),
                    "description": meta.get("description") or s.get("description"),
                    "tasks_open": t["open_total"], "errors_active": s.get("errors_active", 0),
                })
    camp = os.path.join(ROOT, ".roots", "campaigns")
    if os.path.isdir(camp):
        for ns in sorted(os.listdir(camp)):
            d = os.path.join(camp, ns)
            if not os.path.isdir(d):
                continue
            s = summarize_roots(d) or {}
            t = parse_tasks(d)
            projects.append({
                "source": "workspace", "namespace": ns, "kind": "campaign",
                "client": None, "module": None,
                "description": (s.get("meta") or {}).get("description") or s.get("description"),
                "tasks_open": t["open_total"], "errors_active": s.get("errors_active", 0),
            })
    return projects


def compute_metrics(repos, modules, forest):
    coverage, wip, wt_total = {}, 0, 0
    for r in repos:
        for wt in r["worktrees"]:
            wt_total += 1
            if wt["is_version"]:
                coverage.setdefault(wt["branch"], []).append(r["name"])
            else:
                wip += 1
    return {
        # nomenclatura Forest (trees/branches/groves) + alias legacy por compat
        "trees": len(repos), "repos": len(repos),
        "branches_total": wt_total, "worktrees_total": wt_total,
        "wip_branches": wip,
        "groves": len(forest.get("groves", [])),
        "vendors": len(forest.get("vendors", [])),
        "relations": len(forest.get("relations", [])),
        "modules_with_memory": len(modules),
        "open_tasks_total": sum(m["tasks"]["open_total"] for m in modules),
        "version_coverage": {k: sorted(v) for k, v in sorted(coverage.items())},
    }


def aggregate(modules):
    """Construye el feed agregado: cambios, tareas, docs, colapsados."""
    cambios = []
    for m in modules:
        for e in m["journal"]:
            cambios.append({
                "date_raw": e["date_raw"], "summary": e["summary"], "body": e.get("body", ""),
                "date_key": e["date_key"], "module": m["module"], "version": m["version"],
                "repo": m["repo"], "icon": m["icon"], "path": m["path"],
            })
    cambios.sort(key=lambda e: e["date_key"], reverse=True)
    for e in cambios:
        del e["date_key"]

    tareas = [{
        "module": m["module"], "version": m["version"], "repo": m["repo"],
        "icon": m["icon"], "path": m["path"], "mtime": m["mtime"],
        "open": m["tasks"]["open"], "open_total": m["tasks"]["open_total"],
        "done": m["tasks"]["done"],
    } for m in modules if m["tasks"]["open_total"] > 0]
    tareas.sort(key=lambda x: x["mtime"], reverse=True)

    docs = [{
        "module": m["module"], "version": m["version"], "repo": m["repo"],
        "icon": m["icon"], "index_html": m["index_html"], "files": m["docs"],
        "mtime": m["mtime"],
    } for m in modules if m["docs"]]
    docs.sort(key=lambda x: x["mtime"], reverse=True)

    collapsed = [{
        "module": m["module"], "version": m["version"], "icon": m["icon"],
        "skills": m["skills"], "hooks": m["hooks"], "debug": m["debug"],
        "mtime": m["mtime"],
    } for m in modules if (m["skills"] or m["hooks"] or m["debug"])]
    collapsed.sort(key=lambda x: x["mtime"], reverse=True)

    return {"cambios": cambios, "tareas": tareas, "docs": docs, "collapsed": collapsed}


def collect_state():
    forest = load_forest()
    repos = collect_repos(forest["roles"])
    modules = find_module_memories(repos)
    # incluir la memoria de coordinación del workspace (./.roots) si existe
    ws_roots = os.path.join(ROOT, ".roots")
    if os.path.isdir(ws_roots) and os.path.isfile(os.path.join(ws_roots, "context.md")):
        modules.insert(0, _record_module(ROOT, ws_roots, "workspace", "", None))
    agg = aggregate(modules)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "workspace": os.path.basename(ROOT),
        "root": ROOT,
        "vocabulary": "Roots > Forest > Grove > Tree > Branch",
        "metrics": compute_metrics(repos, modules, forest),
        # ejes Forest
        "groves": forest["groves"],
        "vendors": forest["vendors"],
        "relations": forest["relations"],
        "repos": repos,          # = Trees (clave 'repos' por compat de contrato)
        "projects": collect_projects(),
        "modules": modules,
        **agg,
    }


def main():
    global ROOT
    argv = sys.argv[1:]
    if "--root" in argv:
        ROOT = os.path.abspath(argv[argv.index("--root") + 1])
    text = json.dumps(collect_state(), indent=2, ensure_ascii=False)
    if "-o" in argv:
        with open(argv[argv.index("-o") + 1], "w", encoding="utf-8") as fh:
            fh.write(text)
        print("✓ estado escrito", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
