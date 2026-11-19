#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""htree.py — talk to one or more htree task boards (OCAPI htree gateway) from a forest.

A *board* is an Odoo backend exposing the htree gateway (`/ocapi/tree/v1`). You get there with a
**tree account** (`moldeo.tree.account`: Client ID + Secret Key), NOT with your Odoo user/password.
The gateway runs every call AS the user the account is bound to: you see what that user sees, and
whatever you comment is signed with that user's name.

ONE FILE, MANY BOARDS. Credentials live in `.htree.env` at the repo root (never versioned). Each board
is a **profile**: any prefix P with the three keys

    P_BASE=https://<host>/ocapi/tree/v1
    P_CLIENT_ID=...
    P_SECRET_KEY=...

so a person who works with two organisations keeps two profiles in the same file.

    python3 htree.py credentials [-p P]        # add / edit a profile (form; verifies before saving)
    python3 htree.py check                     # does every profile authenticate?
    python3 htree.py whoami [-p P]             # which account / user signs my comments
    python3 htree.py projects [-p P]           # projects I can see (with task counts)
    python3 htree.py tasks [-p P] [--project X] [--mine] [--all]   # list tasks
    python3 htree.py tasks [-p P] <ID>         # one task: description + conversation
    python3 htree.py new [-p P] --project <id|name> "title" [-f desc.md | --desc text] [--yes]  # DRY-RUN unless --yes
    python3 htree.py comment [-p P] <ID> [-f file | text] [--yes]  # DRY-RUN unless --yes
    python3 htree.py set [-p P] <ID> field=value ... [--yes]       # DRY-RUN unless --yes
    python3 htree.py attachments [-p P] <ID>                       # files attached to a task
    python3 htree.py attach [-p P] <ID> file [file ...] [-m text] [--yes]  # upload; DRY-RUN unless --yes
    python3 htree.py florum [-p P] [--forum N] [--all]   # Florum topics you can vote on (votes, ✓ = yours)
    python3 htree.py vote [-p P] <ID> [--yes]            # vote / un-vote a Florum topic; DRY-RUN unless --yes
    python3 htree.py pieces [-p P]                       # my Folio pieces on a Studio board: id, title, state, channel
    python3 htree.py piece new [-p P] "title" [--year Y] [--technique T] [--desc text | -f desc.md] [--yes]
                                                         # create a piece (draft, in my channel); DRY-RUN unless --yes

-p is optional when there is a single profile. Exit codes: 0 ok · 1 error · 2 dry-run (nothing sent).
Standard library only. Safe on a Windows console (cp1252).
"""
import argparse
import base64
import hashlib
import mimetypes
import getpass
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # a Windows console is cp1252: one accent would kill the run
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass


def _repo_root():
    """The repo this forest lives in: walk up from the cwd to the first `.git`/`.roots`."""
    p = Path.cwd().resolve()
    for d in [p, *p.parents]:
        if (d / ".git").exists() or (d / ".roots").is_dir():
            return d
    return p


ROOT = _repo_root()
ENV_FILE = Path(os.environ.get("HTREE_ENV") or (ROOT / ".htree.env"))  # override only for tests
KEYS = ("BASE", "CLIENT_ID", "SECRET_KEY")


def die(title, *lines, code=1):
    print(f"\n  X  {title}")
    for l in lines:
        print(f"     {l}")
    print()
    sys.exit(code)


# ---- the credentials file ------------------------------------------------------------------
def _read_text(p):
    """Tolerates what people have on disk: UTF-8, UTF-8 with BOM, UTF-16 (PowerShell `>`)."""
    if not p.exists():
        return ""
    raw = p.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "utf-8", "latin-1"):
        try:
            t = raw.decode(enc)
            if "\x00" not in t:
                return t
        except (UnicodeDecodeError, UnicodeError):
            continue
    return ""


def read_env(p=None):
    out = {}
    for line in _read_text(p or ENV_FILE).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def profiles(env=None):
    """{name: {BASE, CLIENT_ID, SECRET_KEY}} for every prefix that has a *_BASE key."""
    env = read_env() if env is None else env
    out = {}
    for k in env:
        if k.endswith("_BASE"):
            name = k[: -len("_BASE")]
            out[name] = {x: env.get(f"{name}_{x}", "") for x in KEYS}
    return out


def write_env(env, p=None):
    """Rewrites the file: UTF-8 without BOM, LF, grouped by profile, mode 600."""
    p = p or ENV_FILE
    lines = ["# htree board credentials (tree accounts). NEVER commit this file.",
             "# Edit with:  python3 htree.py credentials", ""]
    done = set()
    for name, vals in sorted(profiles(env).items()):
        for x in KEYS:
            lines.append(f"{name}_{x}={vals[x]}")
            done.add(f"{name}_{x}")
        lines.append("")
    rest = [f"{k}={v}" for k, v in env.items() if k not in done]
    if rest:
        lines += ["# other keys (kept as found)", *rest, ""]
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


def ensure_gitignored():
    """Makes sure `.htree.env` is in the repo's .gitignore. Returns a sentence for the user."""
    gi = ROOT / ".gitignore"
    txt = _read_text(gi)
    if any(l.strip() in (".htree.env", "/.htree.env", "*.env") for l in txt.splitlines()):
        return ".gitignore already blocks .htree.env"
    with open(gi, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(("" if not txt or txt.endswith("\n") else "\n") +
                 "# htree credentials — never versioned\n.htree.env\n")
    return "added .htree.env to .gitignore"


# ---- the gateway ---------------------------------------------------------------------------
class GatewayError(Exception):
    def __init__(self, code, msg):
        super().__init__(f"{code}: {msg}")
        self.code, self.msg = code, msg


def _post(base, route, params, timeout=60):
    """JSON-RPC POST. The body MUST be wrapped in `params` (Odoo JSON controller): sent flat the
    gateway answers 'missing client_id/secret_key' even with correct credentials.
    The body is ALWAYS UTF-8 bytes (json.dumps escapes non-ASCII anyway): a client that sent the
    console's codepage (cp1252 on Windows) had every accent replaced by U+FFFD on the server."""
    req = urllib.request.Request(
        base.rstrip("/") + route, headers={"Content-Type": "application/json; charset=utf-8"},
        data=json.dumps({"jsonrpc": "2.0", "method": "call", "params": params}).encode("utf-8"))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            raise GatewayError("http_%s" % e.code, str(e))
        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
            if attempt == 2:
                raise GatewayError("no_connection", f"{type(e).__name__}: {e}")
            time.sleep(2 * (attempt + 1))
    if "error" in resp:
        d = resp["error"].get("data") or {}
        raise GatewayError("server_error", d.get("message") or str(resp["error"])[:300])
    r = resp.get("result") or {}
    if isinstance(r, dict) and r.get("ok") is False:
        raise GatewayError(r.get("error", "?"), r.get("message", "(no detail)"))
    return r


def authenticate(base, client_id, secret_key):
    """Tries a pair against the REAL gateway. Returns {token, account, depth, user}."""
    r = _post(base, "/auth", {"client_id": client_id, "secret_key": secret_key})
    token = r.get("access_token")
    if not token:
        raise GatewayError("no_token", "the gateway returned no access_token")
    me = _post(base, "/whoami", {"access_token": token})
    return {"token": token, "account": me.get("account"), "depth": me.get("depth"),
            "user": me.get("user"), "type": me.get("type")}


def explain(e, base):
    """A failure that says WHERE it failed: 'never reached the server' is not 'the server said no'."""
    if e.code == "no_connection" or e.code.startswith("http_"):
        return ("Could not REACH the board — this is network/URL, not your credentials.",
                f"URL: {base}", e.msg)
    return ("The board REJECTED the request.", f"{e.code}: {e.msg}")


class Board:
    def __init__(self, name, vals):
        self.name, self.base = name, vals["BASE"]
        if not all(vals.values()):
            die(f"Profile {name} is incomplete", f"File: {ENV_FILE}",
                "Fix it with:  python3 htree.py credentials -p " + name)
        try:
            a = authenticate(self.base, vals["CLIENT_ID"], vals["SECRET_KEY"])
        except GatewayError as e:
            die(f"[{name}] " + explain(e, self.base)[0], *explain(e, self.base)[1:])
        self.token, self.account, self.depth, self.user = a["token"], a["account"], a["depth"], a["user"]
        self.type = a.get("type")  # "lab" = a Studio account; older boards do not say
        self.host = re.sub(r"/ocapi/.*$", "", self.base)

    def gw(self, route, **params):
        try:
            return _post(self.base, route, {"access_token": self.token, **params})
        except GatewayError as e:
            die(f"[{self.name}] the board refused {route}", f"{e.code}: {e.msg}")

    def search(self, model, domain, fields, limit=0, order=None):
        """search_read; the gateway treats limit=0 as 80, so no limit = paginate to the end."""
        if limit:
            return self.gw(f"/{model}/search_read", domain=domain, fields=fields,
                           limit=limit, order=order)["records"]
        out, step = [], 200
        while True:
            batch = self.gw(f"/{model}/search_read", domain=domain, fields=fields, limit=step,
                            offset=len(out), order=order or "id")["records"]
            out += batch
            if len(batch) < step:
                return out

    def task_link(self, tid):
        return f"{self.host}/my/tasks/{tid}"


def pick(args, need_one=True):
    ps = profiles()
    if not ps:
        die("No board credentials yet", f"Looked in: {ENV_FILE}",
            "Load them with:  python3 htree.py credentials")
    if args.profile:
        key = args.profile.upper()
        if key not in ps:
            die(f"There is no profile {args.profile}", "Profiles: " + ", ".join(sorted(ps)))
        return [(key, ps[key])]
    if need_one and len(ps) > 1:
        die("You have several boards — say which one with -p",
            *[f"-p {n}   ({v['BASE']})" for n, v in sorted(ps.items())])
    return sorted(ps.items())


def plain(txt):
    if not txt:
        return ""
    txt = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>", "\n", txt)
    txt = re.sub(r"(?i)<li[^>]*>", "  - ", txt)
    txt = html.unescape(re.sub(r"<[^>]+>", "", txt)).replace("\xa0", " ")
    return re.sub(r"\n{3,}", "\n\n", txt).strip()


def to_html(text):
    t = html.escape(text).replace("\r\n", "\n").replace("\r", "\n")
    return "<p>" + t.replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>"


def mask(s):
    return (s[:4] + "…" + s[-2:]) if s and len(s) > 8 else ("(set)" if s else "(empty)")


# ---- commands ------------------------------------------------------------------------------
def cmd_credentials(args):
    env = read_env()
    ps = profiles(env)
    print(f"\n  Credentials file: {ENV_FILE}")
    for n, v in sorted(ps.items()):
        print(f"   · {n:<22} {v['BASE']}  id={mask(v['CLIENT_ID'])}")
    name = (args.profile or input("\n  Profile name (e.g. ACME_TREE; existing name = edit): ")).strip().upper()
    name = re.sub(r"[^A-Z0-9_]", "_", name)
    if not name:
        die("No profile name given — nothing changed")
    cur = ps.get(name, {x: "" for x in KEYS})

    def ask(label, key, secret=False):
        shown = mask(cur[key]) if secret else (cur[key] or "")
        prompt = f"  {label} [{shown}] (Enter = keep): " if cur[key] else f"  {label}: "
        v = (getpass.getpass(prompt) if secret and sys.stdin.isatty() else input(prompt)).strip()
        return v or cur[key]

    base = ask("Gateway URL (https://<host>/ocapi/tree/v1)", "BASE")
    if base and "/ocapi/" not in base:
        base = base.rstrip("/") + "/ocapi/tree/v1"
    cid = ask("Client ID", "CLIENT_ID")
    sk = ask("Secret Key", "SECRET_KEY", secret=True)
    if not (base and cid and sk):
        die("URL, Client ID and Secret Key are all needed — nothing saved")
    print("\n  Checking against the board before saving…")
    try:
        a = authenticate(base, cid, sk)
    except GatewayError as e:
        die("NOT saved. " + explain(e, base)[0], *explain(e, base)[1:])
    env.update({f"{name}_BASE": base, f"{name}_CLIENT_ID": cid, f"{name}_SECRET_KEY": sk})
    write_env(env)
    print(f"  ✅ Saved profile {name}: account «{a['account']}», signs as «{a['user']}».")
    print(f"     {ensure_gitignored()}\n")
    return 0


def cmd_check(args):
    rc = 0
    for name, v in pick(args, need_one=False):
        try:
            a = authenticate(v["BASE"], v["CLIENT_ID"], v["SECRET_KEY"])
            print(f"  ✅ {name:<22} «{a['account']}» as «{a['user']}» (depth {a['depth']})")
        except GatewayError as e:
            rc = 1
            print(f"  X  {name:<22} {explain(e, v['BASE'])[0]}  [{e.code}]")
    return rc


def cmd_whoami(args):
    for name, v in pick(args, need_one=False):
        b = Board(name, v)
        print(f"\n  [{name}] {b.host}\n   account : {b.account}\n   signs as: {b.user}\n   depth   : {b.depth}")
    print()
    return 0


def cmd_projects(args):
    (name, v), = pick(args)
    b = Board(name, v)
    tasks = b.search("project.task", [], ["project_id"])
    count = {}
    for t in tasks:
        if t["project_id"]:
            count[tuple(t["project_id"])] = count.get(tuple(t["project_id"]), 0) + 1
    print(f"\n  [{name}] projects you can see (by tasks):")
    for (pid, pname), n in sorted(count.items(), key=lambda x: x[0][1]):
        print(f"   {pid:>5}  {pname}  ({n} tasks)")
    print()
    return 0


def _project_domain(b, proj):
    if not proj:
        return []
    if str(proj).isdigit():
        return [["project_id", "=", int(proj)]]
    # NOT ["project_id.name", "ilike", ...]: a portal user may not search on related fields
    # ("You cannot read project_id.name fields in task"). Resolve the ids client-side.
    ids = {t["project_id"][0] for t in b.search("project.task", [], ["project_id"])
           if t["project_id"] and proj.lower() in t["project_id"][1].lower()}
    if not ids:
        die(f"No project you can see matches '{proj}'", "List them with:  htree.py projects")
    return [["project_id", "in", sorted(ids)]]


def cmd_tasks(args):
    (name, v), = pick(args)
    b = Board(name, v)
    if args.id:
        t = b.search("project.task", [["id", "=", args.id]],
                     ["name", "project_id", "stage_id", "description", "date_deadline"], limit=1)
        if not t:
            die(f"Task {args.id} does not exist or you cannot see it")
        t = t[0]
        print(f"\n  #{t['id']}  {t['name']}")
        print(f"  project: {t['project_id'] and t['project_id'][1]} · stage: {t['stage_id'] and t['stage_id'][1]}"
              + (f" · deadline {t['date_deadline']}" if t.get("date_deadline") else ""))
        print(f"  {b.task_link(t['id'])}\n")
        if plain(t.get("description")):
            print("  ── description\n" + "\n".join("  " + l for l in plain(t["description"]).splitlines()) + "\n")
        msgs = b.gw("/messages/list", res_model="project.task", res_id=t["id"], limit=200,
                    order="date asc").get("records", [])
        print(f"  ── conversation ({len(msgs)})")
        for m in msgs:
            who = m["author_id"][1] if m.get("author_id") else (m.get("email_from") or "?")
            body = (m.get("body_plain") or plain(m.get("body"))).strip()
            if body:
                print(f"\n  {(m.get('date') or '')[:16].replace('T', ' ')} · {who}")
                print("\n".join("    " + l for l in body.splitlines()))
        print()
        return 0
    dom = _project_domain(b, args.project)
    if not args.all:
        dom = dom + [["state", "not in", ["1_done", "1_canceled"]]]  # not stage_id.fold: portal-safe
    rows = b.search("project.task", dom, ["name", "project_id", "stage_id", "user_ids"],
                    order="project_id, id desc")
    if args.mine:
        me = b.search("res.users", [["name", "=", b.user]], ["id"], limit=1)
        if not me:
            die("Could not resolve your own user on this board, so --mine cannot filter",
                "List without --mine, or ask the board admin to check your account.")
        uid = me[0]["id"]
        rows = [r for r in rows if uid in (r.get("user_ids") or [])]
    print(f"\n  [{name}] {len(rows)} task(s){'' if args.all else ' (open stages; --all for every stage)'}")
    proj = None
    for r in rows:
        p = r["project_id"] and r["project_id"][1]
        if p != proj:
            proj = p
            print(f"\n  ▸ {p}")
        print(f"   #{r['id']:<6} [{r['stage_id'] and r['stage_id'][1]}]  {r['name']}")
    print()
    return 0


def cmd_comment(args):
    (name, v), = pick(args)
    text = open(args.file, encoding="utf-8").read() if args.file else " ".join(args.text)
    if not text.strip():
        die("The comment is empty")
    if not args.yes:
        print(f"\n  DRY-RUN — nothing sent. [{name}] task #{args.id} would get:\n")
        print("\n".join("    " + l for l in text.splitlines()))
        print("\n  Re-run with --yes to publish (visible to everyone who follows the task).\n")
        return 2
    b = Board(name, v)
    r = b.gw("/messages/post", res_model="project.task", res_id=args.id, body=to_html(text),
             subtype="comment", source="other")
    print(f"  ✅ message {r.get('message_id')} on #{args.id}, signed «{(r.get('author') or ['', '?'])[1]}», "
          f"notified {r.get('notified')}")
    return 0


def cmd_new(args):
    (name, v), = pick(args)
    desc = open(args.file, encoding="utf-8").read() if args.file else (args.desc or "")
    if not args.yes:
        print(f"\n  DRY-RUN — nothing created. [{name}] project «{args.project}» would get a task:")
        print(f"    title: {args.title}")
        if desc.strip():
            print("\n".join("    | " + l for l in desc.splitlines()))
        print("\n  Re-run with --yes to create it.\n")
        return 2
    b = Board(name, v)
    dom = _project_domain(b, args.project)
    pid = dom[0][2] if dom[0][1] == "=" else None
    if pid is None:
        ids = dom[0][2]
        if len(ids) != 1:
            die(f"'{args.project}' matches {len(ids)} projects — use the project id",
                "List them with:  htree.py projects")
        pid = ids[0]
    vals = {"name": args.title, "project_id": pid}
    if desc.strip():
        vals["description"] = to_html(desc)
    # project_id goes in vals: a gateway that supports portal accounts moves it to the context
    # (an Odoo portal user may not write project_id). If it refuses, say what to do instead.
    try:
        r = _post(b.base, "/project.task/create", {"access_token": b.token, "vals": vals})
    except GatewayError as e:
        if "project_id" in e.msg:
            die(f"[{name}] this board does not let your account create tasks yet",
                "Propose it as a comment on the task the organisation gave you for requests.")
        die(f"[{name}] the board refused the new task", f"{e.code}: {e.msg}")
    tid = r["ids"][0]
    back = b.search("project.task", [["id", "=", tid]], ["name", "project_id", "stage_id"], limit=1)
    t = back and back[0]
    print(f"  ✅ task #{tid} created in «{t and t['project_id'] and t['project_id'][1]}» "
          f"[{t and t['stage_id'] and t['stage_id'][1]}]  {b.task_link(tid)}")
    return 0


def cmd_set(args):
    (name, v), = pick(args)
    vals = {}
    for kv in args.pairs:
        if "=" not in kv:
            die(f"'{kv}' is not field=value")
        k, _, val = kv.partition("=")
        vals[k.strip()] = int(val) if val.strip().isdigit() else val
    if not args.yes:
        print(f"\n  DRY-RUN — nothing written. [{name}] task #{args.id} would get: {vals}")
        print("  Re-run with --yes to write.\n")
        return 2
    b = Board(name, v)
    b.gw("/project.task/write", ids=[args.id], vals=vals)  # `vals`, not `values`: the latter is a silent no-op
    back = b.search("project.task", [["id", "=", args.id]], list(vals), limit=1)
    print(f"  ✅ #{args.id} re-read after write: {back and back[0]}")
    return 0


def _attachments(b, tid):
    # the gateway answers under `records` (not `attachments`): reading the wrong key gives an empty list
    return b.gw("/attachments/list", res_model="project.task", res_id=tid).get("records", [])


def cmd_attachments(args):
    (name, v), = pick(args)
    b = Board(name, v)
    rows = _attachments(b, args.id)
    print(f"\n  [{name}] task #{args.id}: {len(rows)} file(s)")
    for a in rows:
        print("    %-7s %-52s %9s B" % (a.get("id"), (a.get("name") or "?")[:52], a.get("file_size", "?")))
    return 0


MAX_BYTES = 20 * 1024 * 1024


def cmd_attach(args):
    """Upload files to a task, each one as a COMMENT carrying the file (the way the web portal does it:
    a portal account cannot attach to the record itself, only through the conversation). Everyone who
    follows the task can download them. The gateway has no delete — check the target before --yes."""
    (name, v), = pick(args)
    files = []
    for f in args.files:
        pth = Path(f)
        if not pth.is_file():
            die(f"Not a file: {f}")
        if pth.stat().st_size > MAX_BYTES:
            die(f"{f} is over {MAX_BYTES // 1048576} MB", "Compress it or split it.")
        files.append(pth)
    if not args.yes:
        print(f"\n  DRY-RUN — nothing uploaded. [{name}] task #{args.id} would get:")
        for pth in files:
            print(f"    {pth.name}  ({pth.stat().st_size} B)")
        print("\n  Attachments cannot be deleted from here. Re-run with --yes to upload.\n")
        return 2
    b = Board(name, v)
    before = {a.get("id") for a in _attachments(b, args.id)}
    sent = []
    for pth in files:
        raw = pth.read_bytes()
        b.gw("/attachments/add", res_model="project.task", res_id=args.id, name=pth.name,
             mimetype=mimetypes.guess_type(pth.name)[0] or "application/octet-stream",
             datas=base64.b64encode(raw).decode("ascii"), as_comment=True,
             body=to_html(args.message or pth.name))
        sent.append((pth.name, hashlib.sha1(raw).hexdigest()))
    # verify by re-reading: an ok:true from the POST does not prove the file is there
    new = [a for a in _attachments(b, args.id) if a.get("id") not in before]
    names = {a.get("name") for a in new}
    for n, _ in sent:
        print(("  ✅ " if n in names else "  ⛔ NOT FOUND after upload: ") + f"{n} on #{args.id}")
    # images are resized/re-compressed by Odoo on upload: a different size is normal there
    return 0 if all(n in names for n, _ in sent) else 1


# ---- Florum: vote on the features you asked for (gateway resource forum.post) -----------------
_FLORUM_FIELDS = ["id", "name", "forum_id", "state", "florum_vote_count", "florum_user_voted"]


def _florum_unavailable(name, e):
    die(f"[{name}] this board does not expose Florum to your account yet",
        f"{e.code}: {e.msg}",
        "Florum voting from a forest needs the board's htree gateway >= 26.293 with Florum installed.")


def _florum_pending(args):
    """Session-start nudge (v1.34): ONE line if there are open proposals you have not voted, else
    nothing. Never fails loudly (no board, no network, no Florum ⇒ silent, exit 0) and never votes."""
    import contextlib
    import io
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            (name, v), = pick(args)
            b = Board(name, v)
            dom = [["parent_id", "=", False], ["florum_kind", "!=", False], ["state", "=", "active"]]
            if args.forum:
                dom.append(["forum_id", "=", args.forum])
            rows = _post(b.base, "/forum.post/search_read", {
                "access_token": b.token, "domain": dom, "fields": _FLORUM_FIELDS, "limit": 200})["records"]
    except (SystemExit, Exception):
        return 0
    todo = [r for r in rows or [] if not r.get("florum_user_voted")]
    if todo:
        forums = sorted({(r["forum_id"] or [0, "?"])[1] for r in todo})
        print(f"🌱 Florum [{name}]: {len(todo)} proposal(s) waiting for your vote "
              f"({', '.join(forums)}) — see them with: htree.py florum")
    return 0


def cmd_florum(args):
    if getattr(args, "pending", False):
        return _florum_pending(args)
    (name, v), = pick(args)
    b = Board(name, v)
    dom = [["parent_id", "=", False], ["florum_kind", "!=", False]]
    if not args.all:
        dom.append(["state", "=", "active"])
    if args.forum:
        dom.append(["forum_id", "=", args.forum])
    try:
        rows = _post(b.base, "/forum.post/search_read", {
            "access_token": b.token, "domain": dom, "fields": _FLORUM_FIELDS, "limit": 200,
            "order": "florum_vote_count desc, id desc"})["records"]
    except GatewayError as e:
        _florum_unavailable(name, e)
    if not rows:
        print(f"\n  [{name}] no Florum topics to vote on" + (f" in forum {args.forum}" if args.forum else "") + ".\n")
        return 0
    forum = None
    for r in sorted(rows, key=lambda r: ((r["forum_id"] or [0, ""])[1], -(r["florum_vote_count"] or 0))):
        f = r["forum_id"] and r["forum_id"][1]
        if f != forum:
            forum = f
            print(f"\n  ▸ {f}  (forum {r['forum_id'][0]})")
        mark = "✓" if r.get("florum_user_voted") else " "
        print(f"   {mark} #{r['id']:<6} {r['florum_vote_count'] or 0:>3} votes  {r['name']}")
    print("\n  ✓ = you voted. Vote or un-vote:  htree.py vote <ID> --yes\n")
    return 0


def cmd_vote(args):
    (name, v), = pick(args)
    b = Board(name, v)
    try:
        rows = _post(b.base, "/forum.post/search_read", {
            "access_token": b.token, "domain": [["id", "=", args.id]], "fields": _FLORUM_FIELDS,
            "limit": 1})["records"]
    except GatewayError as e:
        _florum_unavailable(name, e)
    if not rows:
        die(f"[{name}] topic #{args.id} not found (or not visible to your account)",
            "List what you can vote on with:  htree.py florum")
    t = rows[0]
    now = bool(t.get("florum_user_voted"))
    if not args.yes:
        print(f"\n  DRY-RUN — nothing sent. [{name}] #{t['id']} «{t['name']}» has {t['florum_vote_count'] or 0} votes;")
        print(f"  you {'already voted' if now else 'have not voted'} ⇒ --yes would {'REMOVE your vote' if now else 'ADD your vote'}.\n")
        return 2
    try:
        r = _post(b.base, "/forum.post/call", {"access_token": b.token, "ids": [t["id"]],
                                                "method": "florum_toggle_vote"})["result"]
    except GatewayError as e:
        die(f"[{name}] the board refused the vote", f"{e.code}: {e.msg}")
    if not isinstance(r, dict) or "voted" not in r:
        die(f"[{name}] unexpected answer from the board", str(r)[:200])
    print(f"  ✅ #{t['id']} «{t['name']}»: {'voted' if r['voted'] else 'vote removed'} — "
          f"{r.get('vote_count')} votes now")
    return 0


# ---- Studio: my Folio pieces (gateway resources moldeo.folio.work + moldeo.folio.publication) --
# A piece is a `moldeo.folio.work`; where it shows (channel) and whether it is out (state) live on
# its `moldeo.folio.publication`. A Studio account reads ONLY the publications of its own channels,
# so "my pieces" is keyed on publications: listing works directly would also return every PUBLISHED
# work of other people (folio lets an author read what is public).
_PIECE_STATE = {"draft": "draft", "preview": "preview", "published": "published", "archived": "archived"}


def _studio_unavailable(name, e):
    if e.code == "permission_denied":  # a Studio credential without that box ticked
        die(f"[{name}] this credential is missing a permission", e.msg,
            "Tick it on your Studio's Credentials page (reading needs «read», creating «create pieces»).")
    die(f"[{name}] this account has no Studio pieces", f"{e.code}: {e.msg}",
        "Pieces need the credential of a Studio (its own profile), not a task-board one:",
        "create it on your Studio's Credentials page and load it with  htree.py credentials -p <NAME>")


def _my_pieces(b, name, work_ids=None):
    dom = [["work_id", "in", list(work_ids)]] if work_ids else []
    try:
        pubs = _post(b.base, "/moldeo.folio.publication/search_read", {
            "access_token": b.token, "domain": dom, "limit": 500, "order": "id desc",
            "fields": ["id", "work_id", "channel_id", "state", "website_published"]})["records"]
    except GatewayError as e:
        _studio_unavailable(name, e)
    rows = {}
    for p in pubs:
        if not p.get("work_id"):
            continue
        wid, title = p["work_id"][0], p["work_id"][1]
        r = rows.setdefault(wid, {"id": wid, "title": title, "states": [], "channels": []})
        st = _PIECE_STATE.get(p.get("state"), p.get("state") or "?")
        if st == "published" and not p.get("website_published"):
            st = "published (hidden)"
        if st not in r["states"]:
            r["states"].append(st)
        ch = p["channel_id"] and p["channel_id"][1]
        if ch and ch not in r["channels"]:
            r["channels"].append(ch)
    return sorted(rows.values(), key=lambda r: -r["id"])


def cmd_pieces(args):
    (name, v), = pick(args)
    b = Board(name, v)
    if b.type and b.type != "lab":
        die(f"[{name}] is a task-board account («{b.account}»), not a Studio",
            "Pieces live in your Studio, with its own credential and its own profile:",
            "create it on your Studio's Credentials page and load it with  htree.py credentials -p <NAME>")
    rows = _my_pieces(b, name)
    print(f"\n  [{name}] {len(rows)} piece(s) in your Studio")
    if rows:
        print("    %-7s %-18s %-30s %s" % ("id", "state", "channel", "title"))
    for r in rows:
        print("    %-7s %-18s %-30s %s" % (r["id"], ", ".join(r["states"])[:18],
                                         ", ".join(r["channels"])[:30], r["title"]))
    print(f"\n  Open one: {b.host}/my/studio/pieza/<id> · new one: htree.py piece new \"title\"\n")
    return 0


def _read_desc(path):
    """A description file as the person saved it: BOM'd UTF-8/UTF-16 (Notepad), plain UTF-8, or the
    Windows codepage. NOT `_read_text`: trying UTF-16 without a BOM turns cp1252 text into CJK noise.
    Whatever it was on disk, it is SENT as UTF-8."""
    pth = Path(path)
    if not pth.is_file():
        die(f"Not a file: {path}")
    raw = pth.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8", errors="replace")
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


def cmd_piece(args):
    if args.action != "new":
        die(f"Unknown piece action '{args.action}'", "Use:  htree.py piece new \"title\" [--yes]")
    (name, v), = pick(args)
    title = (args.title or "").strip()
    if not title:
        die("The piece needs a title", "Use:  htree.py piece new \"title\" [--year Y] [--technique T] [--yes]")
    desc = _read_desc(args.file) if args.file else (args.desc or "")
    vals = {"name": title}
    if args.year:
        vals["year"] = str(args.year)
    if args.technique:
        vals["technique"] = args.technique
    if desc.strip():
        vals["description"] = to_html(desc)
    if not args.yes:
        print(f"\n  DRY-RUN — nothing created. [{name}] your Studio would get a piece (draft, NOT published):")
        print(f"    title    : {title}")
        for k in ("year", "technique"):
            if k in vals:
                print(f"    {k:<9}: {vals[k]}")
        if desc.strip():
            print("\n".join("    | " + l for l in desc.splitlines()))
        print("\n  It counts against your plan's pieces. Re-run with --yes to create it.\n")
        return 2
    b = Board(name, v)
    try:
        r = _post(b.base, "/moldeo.folio.work/create", {"access_token": b.token, "vals": vals})
    except GatewayError as e:
        if e.code in ("permission_denied", "not_registered", "op_forbidden", "below_horizon"):
            _studio_unavailable(name, e)
        die(f"[{name}] the board refused the new piece", f"{e.code}: {e.msg}")
    wid = (r.get("ids") or [None])[0]
    if not wid:
        die(f"[{name}] unexpected answer from the board", str(r)[:200])
    # verify by re-reading: an ok:true from the create does not prove it landed in YOUR channel
    back = _my_pieces(b, name, [wid])
    if not back:
        print(f"  ⛔ piece #{wid} was created but is NOT in any of your channels — tell the board owner.")
        return 1
    p = back[0]
    print(f"  ✅ piece #{wid} «{p['title']}» [{', '.join(p['states'])}] in «{', '.join(p['channels'])}»")
    print(f"     {b.host}/my/studio/pieza/{wid}  (publish it from your Studio when it is ready)")
    return 0


# ---------------- agents push (Miciel F1) ----------------
# Your forest is the source; the board is the showcase. `agents push` mirrors the definitions of the
# agents and skills VERSIONED in your forest (git ls-files) into your Studio, read-only, private by
# default. Nothing runs on the board because it was pushed. Design: Moldeo Lab «Miciel en el Studio».
MICIEL_PUSH_METHOD = "studio_api_miciel_push"
# Where the Lab API exposes it: moldeo.lab.account (studio 26.348), the ONLY door for a Lab account.
MICIEL_PUSH_MODELS = ("moldeo.lab.account",)
MICIEL_GLOBS = (".claude/agents/*.md", ".claude/skills/*/SKILL.md", ".roots/agents/*.md")
MICIEL_MAX_ITEMS = 200
MICIEL_MAX_BYTES = 200 * 1024
# Same shapes the board rejects (odoo_moldeo_roots/models/omr_miciel.py): checked HERE first, so a
# secret never leaves your machine. On a hit we name the file, never the value.
MICIEL_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_\-]{20,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[abpr]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key|client[_-]?secret|password|passwd|token)\b"
               r"\s*[:=]\s*[\"']?[A-Za-z0-9/+_\-\.]{16,}"),
]


def _git(root, *a):
    import subprocess
    r = subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True)
    if r.returncode != 0:
        die(f"git {' '.join(a[:2])} failed in {root}", (r.stderr or r.stdout).strip()[:300],
            "agents push needs a git forest: run it from (or point --path to) your forest's root.")
    return r.stdout


def _miciel_items(root):
    root = Path(root).resolve()
    top = Path(_git(root, "rev-parse", "--show-toplevel").strip())
    commit = _git(top, "rev-parse", "--short", "HEAD").strip()
    files = [f for f in _git(top, "ls-files", "-z", "--", *MICIEL_GLOBS).split("\0") if f]
    dirty = set(f for f in _git(top, "status", "--porcelain", "-z", "--", *MICIEL_GLOBS).split("\0")
                for f in [f[3:]] if f)
    items, problems = [], []
    for f in sorted(files):
        pth = top / f
        if not pth.is_file():
            continue
        raw = pth.read_bytes()
        if len(raw) > MICIEL_MAX_BYTES:
            problems.append(f"{f}: {len(raw)//1024} KB (max {MICIEL_MAX_BYTES//1024} KB)")
            continue
        text = raw.decode("utf-8", errors="replace")
        if any(p.search(text) for p in MICIEL_SECRET_PATTERNS):
            problems.append(f"{f}: has something shaped like a key or secret")
            continue
        kind = "skill" if f.endswith("/SKILL.md") else "agent"
        items.append({"kind": kind, "path": f, "content": text,
                      "commit": commit + ("-dirty" if f in dirty else "")})
    return top, commit, items, problems, dirty


def cmd_agents(args):
    if args.action != "push":
        die(f"Unknown agents action '{args.action}'", "Use:  htree.py agents push [--path FOREST] [--yes]")
    top, commit, items, problems, dirty = _miciel_items(args.path or ".")
    if problems:
        die("Nothing was sent — fix these files first (the push goes all or nothing):",
            *["  " + p for p in problems],
            "Secrets never belong in an agent or skill: move them to an ignored .env and re-run.")
    if not items:
        die(f"No agents or skills versioned in {top}", "Looked for: " + ", ".join(MICIEL_GLOBS),
            "Only files tracked by git are pushed (git add + commit them first).")
    if len(items) > MICIEL_MAX_ITEMS:
        die(f"{len(items)} files: the board takes at most {MICIEL_MAX_ITEMS} per push")
    n_ag = sum(1 for i in items if i["kind"] == "agent")
    if not args.yes:
        print(f"\n  DRY-RUN — nothing sent. From {top} @ {commit}, your Studio would mirror "
              f"{n_ag} agent(s) and {len(items) - n_ag} skill(s), PRIVATE (only you see them):")
        for i in items:
            mark = "  (uncommitted changes: pushed as -dirty)" if i["commit"].endswith("-dirty") else ""
            print(f"    {i['kind']:<6} {i['path']}{mark}")
        print("\n  Pushing twice changes nothing; a new commit updates in place. Re-run with --yes.\n")
        return 2
    (name, v), = pick(args)
    b = Board(name, v)
    if b.type and b.type != "lab":
        die(f"[{name}] is a task-board account («{b.account}»), not a Studio",
            "Agents are pushed to your Studio, with the Studio's credential (its own profile).")
    try:
        r = None
        for model in MICIEL_PUSH_MODELS:  # the first door the board opens; the next only if this one is not there
            try:
                r = _post(b.base, f"/{model}/call", {
                    "access_token": b.token, "method": MICIEL_PUSH_METHOD, "kwargs": {"items": items}},
                    timeout=180)["result"]
                break
            except GatewayError as e:
                if e.code not in ("not_registered", "op_forbidden", "method_forbidden") or model == MICIEL_PUSH_MODELS[-1]:
                    raise
    except GatewayError as e:
        if e.code == "permission_denied":
            die(f"[{name}] this credential cannot publish agents",
                "Tick «Publicar agentes y skills» on your Studio's Credentials page.")
        die(f"[{name}] the board refused the push (nothing was written)", f"{e.code}: {e.msg}")
    r = r or {}
    print(f"  ✅ [{name}] created {r.get('created', 0)} · updated {r.get('updated', 0)} · "
          f"unchanged {r.get('unchanged', 0)} · agent→skill links {r.get('linked', 0)}  (from {commit})")
    print(f"     See them in your Studio: {b.host}/my/studio  (Miciel section)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-p", "--profile", help="which board (prefix in .htree.env)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("credentials", help="add / edit a profile (verifies before saving)")
    sub.add_parser("check", help="authenticate every profile")
    sub.add_parser("whoami", help="which account and user sign your actions")
    sub.add_parser("projects", help="projects you can see")
    t = sub.add_parser("tasks", help="list tasks, or show one")
    t.add_argument("id", nargs="?", type=int)
    t.add_argument("--project", help="project id or part of its name")
    t.add_argument("--mine", action="store_true", help="only tasks assigned to me")
    t.add_argument("--all", action="store_true", help="include closed/folded stages")
    n = sub.add_parser("new", help="create a task in a project (dry-run unless --yes)")
    n.add_argument("title")
    n.add_argument("--project", required=True, help="project id or part of its name")
    n.add_argument("--desc", help="description text")
    n.add_argument("-f", "--file", help="description from a file")
    n.add_argument("--yes", action="store_true")
    c = sub.add_parser("comment", help="comment on a task (dry-run unless --yes)")
    c.add_argument("id", type=int)
    c.add_argument("text", nargs="*")
    c.add_argument("-f", "--file")
    c.add_argument("--yes", action="store_true")
    s = sub.add_parser("set", help="write fields on a task (dry-run unless --yes)")
    s.add_argument("id", type=int)
    s.add_argument("pairs", nargs="+")
    s.add_argument("--yes", action="store_true")
    a = sub.add_parser("attachments", help="list the files attached to a task")
    a.add_argument("id", type=int)
    u = sub.add_parser("attach", help="upload files to a task (dry-run unless --yes)")
    u.add_argument("id", type=int)
    u.add_argument("files", nargs="+")
    u.add_argument("-m", "--message", help="comment text that goes with the file (default: its name)")
    u.add_argument("--yes", action="store_true")
    fl = sub.add_parser("florum", help="Florum topics you can vote on")
    fl.add_argument("--forum", type=int, help="only this forum id")
    fl.add_argument("--all", action="store_true", help="include closed topics")
    fl.add_argument("--pending", action="store_true",
                    help="session-start nudge: one line if open proposals wait for your vote, else nothing (never fails)")
    vo = sub.add_parser("vote", help="vote / un-vote a Florum topic (dry-run unless --yes)")
    vo.add_argument("id", type=int)
    vo.add_argument("--yes", action="store_true")
    sub.add_parser("pieces", help="my Folio pieces on a Studio board (id, title, state, channel)")
    pc = sub.add_parser("piece", help="piece new \"title\": create a draft piece (dry-run unless --yes)")
    pc.add_argument("action", choices=["new"])
    pc.add_argument("title")
    pc.add_argument("--year", help="year of the piece (e.g. 2026)")
    pc.add_argument("--technique", help="technique / medium")
    pc.add_argument("--desc", help="description text")
    pc.add_argument("-f", "--file", help="description from a file (UTF-8)")
    pc.add_argument("--yes", action="store_true")
    ag = sub.add_parser("agents", help="agents push: mirror your forest's agents and skills to your Studio (dry-run unless --yes)")
    ag.add_argument("action", choices=["push"])
    ag.add_argument("--path", help="your forest's root (default: current directory)")
    ag.add_argument("--yes", action="store_true")
    for p in sub.choices.values():  # accept -p after the subcommand too
        p.add_argument("-p", "--profile", dest="profile_sub", help=argparse.SUPPRESS)
    args = ap.parse_args()
    args.profile = args.profile or getattr(args, "profile_sub", None)
    return {"credentials": cmd_credentials, "check": cmd_check, "whoami": cmd_whoami,
            "projects": cmd_projects, "tasks": cmd_tasks, "new": cmd_new, "comment": cmd_comment,
            "set": cmd_set, "attachments": cmd_attachments, "attach": cmd_attach,
            "florum": cmd_florum, "vote": cmd_vote, "pieces": cmd_pieces,
            "piece": cmd_piece, "agents": cmd_agents}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  (cancelled — nothing changed)")
        sys.exit(1)
