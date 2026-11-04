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
    python3 htree.py comment [-p P] <ID> [-f file | text] [--yes]  # DRY-RUN unless --yes
    python3 htree.py set [-p P] <ID> field=value ... [--yes]       # DRY-RUN unless --yes

-p is optional when there is a single profile. Exit codes: 0 ok · 1 error · 2 dry-run (nothing sent).
Standard library only. Safe on a Windows console (cp1252).
"""
import argparse
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
    gateway answers 'missing client_id/secret_key' even with correct credentials."""
    req = urllib.request.Request(
        base.rstrip("/") + route, headers={"Content-Type": "application/json"},
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
            "user": me.get("user")}


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
    c = sub.add_parser("comment", help="comment on a task (dry-run unless --yes)")
    c.add_argument("id", type=int)
    c.add_argument("text", nargs="*")
    c.add_argument("-f", "--file")
    c.add_argument("--yes", action="store_true")
    s = sub.add_parser("set", help="write fields on a task (dry-run unless --yes)")
    s.add_argument("id", type=int)
    s.add_argument("pairs", nargs="+")
    s.add_argument("--yes", action="store_true")
    for p in sub.choices.values():  # accept -p after the subcommand too
        p.add_argument("-p", "--profile", dest="profile_sub", help=argparse.SUPPRESS)
    args = ap.parse_args()
    args.profile = args.profile or getattr(args, "profile_sub", None)
    return {"credentials": cmd_credentials, "check": cmd_check, "whoami": cmd_whoami,
            "projects": cmd_projects, "tasks": cmd_tasks, "comment": cmd_comment,
            "set": cmd_set}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  (cancelled — nothing changed)")
        sys.exit(1)
