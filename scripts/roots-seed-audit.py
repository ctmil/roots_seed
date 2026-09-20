#!/usr/bin/env python3
"""roots-seed-audit — is each distributed copy of the seed a stale COPY or a local FORK?

WHY THIS EXISTS. The spec says: bump the canonical, re-distribute the copy to every `.roots/`
(`on-seed-update`). That reads like `cp`, and on a live forest it is not: a deployment that used the
seed for months may have WRITTEN INTO its local copy — a convention it invented, a hook it wrote, a
section it needed. Those are contributions, and `cp` deletes them silently.

Measured on one live forest of 6406 copies: 5874 byte-identical to some historical canonical, 414
identical except a distribution banner, and **118 carrying 78.589 lines of their own**. Two lessons
are baked in here because both cost a wrong answer first:

  1. A naive walk with a depth limit undercounted by 10x (617 vs 6406). No depth limit here.
  2. A binary fork/no-fork verdict is WORSE than no verdict. 185 of those "forks" differed only by a
     5-line HTML banner the distributor itself pastes on top. A tool that flags 185 healthy files
     buries the ~8 blocks that actually need a human. So: normalize the banner away, and report the
     MAGNITUDE of the divergence, never just its existence.

VERDICTS
  FIEL     byte-identical to a historical canonical         -> updating is lossless
  BANNER   identical except the distribution banner          -> safe, re-paste the banner
  DIVERGE  carries its own content (n lines)                 -> the local content goes UP first
                                                                (`roots-suggest` / `roots-pr`), then down
  ORPHAN   declares a version the canonical never had        -> predates this canonical, or came from
                                                                another lineage: a human must look

READ-ONLY. It writes nothing, anywhere. Exit 0 always unless it cannot find a canonical.

  roots-seed-audit.py [--forest DIR] [--canon DIR] [--exclude PAT ...] [--detail REPO] [--json]
"""
import argparse, hashlib, os, re, subprocess, sys, difflib, json
from collections import defaultdict

BANNER = re.compile(r'^\s*<!--.*-->\s*$')
VERRE  = re.compile(r'^\*\*(?:Versi[oó]n|Version):\*\*\s*([0-9]+\.[0-9]+)')

def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""

def normalize(text):
    """Drop the leading distribution banner and trailing whitespace.
    The banner is the distributor's own marker, not content: counting it as divergence is what
    turned 185 healthy files into false alarms."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) and (BANNER.match(lines[i]) or not lines[i].strip()):
        i += 1
    return [l.rstrip() for l in lines[i:]]

def version_of(lines):
    for l in lines[:60]:
        m = VERRE.match(l)
        if m: return m.group(1)
    return "?"

def find_canon(forest, given):
    if given: return given
    for cand in (os.path.join(forest, "roots_seed", "main"), os.path.join(forest, "roots_seed"), forest):
        if os.path.isfile(os.path.join(cand, "roots_seed.md")) and os.path.isdir(os.path.join(cand, ".git")) \
           or os.path.isfile(os.path.join(cand, "roots_seed.md")) and sh("git","-C",cand,"rev-parse","--git-dir"):
            return cand
    return None

def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--forest", default=os.environ.get("FOREST", "."))
    ap.add_argument("--canon",  default=os.environ.get("ROOTS_CANON"))
    ap.add_argument("--exclude", action="append", default=[],
                    help="path PREFIX to skip, matched on whole components (repeatable). "
                         "'--exclude vendor' skips vendor/ but NOT my_vendor_lib/ — measured the hard "
                         "way: a substring match silently dropped 4674 copies of a repo whose name "
                         "merely CONTAINED the excluded word, and the total looked plausible.")
    ap.add_argument("--detail", help="print every diverging file of this repo, with its line count")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    forest = os.path.abspath(a.forest)
    canon  = find_canon(forest, a.canon)
    if not canon:
        print("no canonical seed found: pass --canon DIR (a checkout of the seed repo)", file=sys.stderr)
        return 2

    # every historical version of the canonical, normalized -> {hash: version}
    by_hash, by_ver = {}, {}
    for c in sh("git","-C",canon,"log","--all","--format=%H","--","roots_seed.md").split():
        blob = sh("git","-C",canon,"show",f"{c}:roots_seed.md")
        if not blob: continue
        n = normalize(blob)
        by_hash.setdefault(hashlib.sha1("\n".join(n).encode()).hexdigest(), version_of(n))
        by_ver.setdefault(version_of(n), n)
    if not by_hash:
        print(f"{canon}: no history for roots_seed.md — is this the seed repo?", file=sys.stderr)
        return 2

    # The canonical's own masters are not distributed copies. But WHERE to exclude depends on the
    # layout, and getting it wrong is silent: when the canonical IS the forest (the likeliest case of
    # all -- a user clones the seed and runs this inside it), excluding the canonical *directory*
    # excluded the root, the walk skipped everything, and the tool reported "0 copies, 0% need a
    # human". A confident empty answer reads as good news.
    canon_rel = os.path.relpath(canon, forest)
    skip = [".git"] + ([] if canon_rel in (".", "") else [canon_rel]) + a.exclude
    master = os.path.realpath(os.path.join(canon, "roots_seed.md"))
    copies = []
    for root, dirs, files in os.walk(forest):
        rel = os.path.relpath(root, forest)
        # Component-wise, never substring: see --exclude help.
        if any(s and (rel == s or rel.startswith(s.rstrip(os.sep) + os.sep)) for s in skip):
            dirs[:] = []; continue
        if "roots_seed.md" in files:
            f = os.path.join(root, "roots_seed.md")
            if os.path.realpath(f) == master: continue   # the master itself, not a copy
            copies.append(f)

    per = defaultdict(lambda: {"n":0,"fiel":0,"banner":0,"div":0,"orphan":0,"lines":0,
                               "vers":set(),"worst":("",0),"files":[]})
    for f in copies:
        rel  = os.path.relpath(f, forest)
        repo = rel.split(os.sep)[0]
        try: raw = open(f, encoding="utf-8", errors="replace").read()
        except OSError: continue
        n = normalize(raw)
        h = hashlib.sha1("\n".join(n).encode()).hexdigest()
        v = version_of(n)
        r = per[repo]; r["n"] += 1; r["vers"].add(v)
        if h in by_hash:
            r["banner" if raw.lstrip().startswith("<!--") else "fiel"] += 1
            continue
        base = by_ver.get(v)
        if base is None:
            r["orphan"] += 1; r["files"].append((rel, -1))
            if r["worst"][1] == 0: r["worst"] = (rel, -1)
            continue
        d = sum(1 for l in difflib.unified_diff(base, n, lineterm="", n=0)
                if l[:1] in "+-" and l[:3] not in ("+++","---"))
        r["div"] += 1; r["lines"] += d; r["files"].append((rel, d))
        if d > r["worst"][1]: r["worst"] = (rel, d)

    if a.detail:
        r = per.get(a.detail)
        if not r: print(f"no copies under '{a.detail}'"); return 0
        print(f"# {a.detail}: files that are NOT a clean canonical copy\n")
        for rel, d in sorted(r["files"], key=lambda x: -x[1]):
            print(f"  {'ORPHAN (version not in canonical history)' if d < 0 else str(d)+' lines':<44} {rel}")
        return 0

    if a.json:
        out = {k: {kk: (sorted(vv) if isinstance(vv, set) else vv)
                   for kk, vv in v.items() if kk != "files"} for k, v in per.items()}
        print(json.dumps(out, indent=2)); return 0

    print(f"# canonical: {os.path.relpath(canon, forest)} — {len(by_hash)} historical blobs, "
          f"versions {','.join(sorted(by_ver, key=lambda s: [int(x) for x in s.split('.')]))}\n")
    hdr = f"{'REPO':<24}{'copies':>7}{'FIEL':>6}{'BANNER':>8}{'DIVERGE':>9}{'ORPHAN':>8}{'lines':>9}  versions"
    print(hdr); print("-" * len(hdr))
    tot = defaultdict(int)
    for repo in sorted(per):
        r = per[repo]
        for k in ("n","fiel","banner","div","orphan","lines"): tot[k] += r[k]
        print(f"{repo:<24}{r['n']:>7}{r['fiel']:>6}{r['banner']:>8}{r['div']:>9}{r['orphan']:>8}"
              f"{r['lines']:>9}  {','.join(sorted(r['vers']))}")
    print("-" * len(hdr))
    print(f"{'TOTAL':<24}{tot['n']:>7}{tot['fiel']:>6}{tot['banner']:>8}{tot['div']:>9}"
          f"{tot['orphan']:>8}{tot['lines']:>9}")
    if tot["n"] == 0:
        print("\nNO distributed copies found under this forest.\n"
              "That is a finding, not a clean bill: either nothing has the seed deployed\n"
              "yet, or --forest points somewhere that does not contain the deployments.\n"
              "Check the path before reading this as good news.")
        return 0
    mech = tot['fiel'] + tot['banner']
    print(f"\n{mech} of {tot['n']} copies ({100*mech//max(tot['n'],1)}%) update mechanically. "
          f"{tot['div']+tot['orphan']} need a human FIRST.")
    if tot['div'] or tot['orphan']:
        print("\n# worst case per repo — what a blind `cp` would overwrite:")
        for repo in sorted(per):
            rel, d = per[repo]["worst"]
            if rel: print(f"  {repo:<24} {'ORPHAN' if d < 0 else str(d)+' lines':<14} {rel}")
        print("\n# next: `--detail <repo>` lists its files; send the local content UP with\n"
              "#       `roots-suggest` / `roots-pr` BEFORE bringing the new canonical DOWN.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
