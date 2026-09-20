#!/usr/bin/env python3
"""roots-report — the state of a whole roots workspace, and what to merge FIRST.

WHY THIS EXISTS. A forest is N repos x M branches, and `git status` answers for exactly one of them.
What a session actually needs on arrival is the opposite: which of the M x N places is holding work
that can still be LOST, and in what order to land it. Nobody keeps that in their head, so it is kept
nowhere, and branches quietly rot until the merge is expensive.

TWO PLANES, and they are not the same urgency. The seed's whole premise is that memory lives beside
the code, so a dirty working tree is really two different facts:
  - uncommitted `.roots/` files = MEMORY at risk. The rule the seed is built on is that what is not
    written down before being done is not recoverable; memory that exists only on one disk is one
    disk failure away from being re-derived from nobody's recollection. This ranks FIRST.
  - uncommitted code/docs = work at risk, but usually reproducible from the same head that wrote it.

THE SCORE IS RELATIVE, AND THE REASON IS THE DATA. Weights are printed, every row shows WHY it
scored, and every row is listed — not just the top one. A ranking whose reasoning is hidden gets
argued with instead of acted on; one that shows its terms gets corrected.

READ-ONLY. It runs only `git` queries. It never fetches, commits, merges or pushes.

  roots-report.py [--forest DIR] [--repo NAME] [--deploy BRANCH] [--top N] [--json]

NOTE ON `behind`: computed against the LOCAL deploy branch, because fetching is a network action and
this tool does not take any. A local deploy branch that is itself stale makes `behind` optimistic —
run your fetch first if the number matters.
"""
import argparse, json, os, subprocess, sys, time
from collections import defaultdict

W = {"roots_dirty": 12, "unpushed": 6, "code_dirty": 3, "ahead": 2, "stale_day": 0.10,
     "behind": 0.05, "bench_dirty": 0.0, "bench_tracked": 0.5}

def git(repo, *a):
    r = subprocess.run(("git","-C",repo)+a, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""

def is_repo(p):
    """A Tree is a repo ROOT, not any directory inside one.
    `rev-parse --git-dir` succeeds from any subdirectory, because git walks UP. Using it directly
    made every plain subfolder of the forest repo look like its own Tree, and each one then
    reported the PARENT's status -- seven identical rows at the top of the ranking, all the same
    worktree. Duplicated noise at the top is how a report stops being read."""
    top = git(p, "rev-parse", "--show-toplevel")
    if top and os.path.realpath(top) == os.path.realpath(p): return True
    # a worktree of a bare repo: its toplevel IS itself, so the check above already covers it.
    return bool(git(p, "rev-parse", "--is-bare-repository") == "true")

def find_repos(forest):
    """A Tree is a git repo, or a directory holding a bare repo plus its worktrees."""
    out = []
    for name in sorted(os.listdir(forest)):
        p = os.path.join(forest, name)
        if not os.path.isdir(p) or name.startswith("."): continue
        if is_repo(p): out.append((name, p)); continue
        subs = [os.path.join(p, d) for d in sorted(os.listdir(p))
                if os.path.isdir(os.path.join(p, d)) and is_repo(os.path.join(p, d))]
        if subs: out.append((name, subs[0]))
    return out

def deploy_branch(repo, override):
    if override and git(repo, "rev-parse", "--verify", "--quiet", override): return override
    head = git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    if head: return head.rsplit("/", 1)[-1]
    for c in ("main", "master", "develop", "trunk"):
        if git(repo, "rev-parse", "--verify", "--quiet", c): return c
    return ""

def worktrees(repo):
    """path -> branch, for every checked-out worktree of this Tree."""
    out, cur = [], {}
    for line in git(repo, "worktree", "list", "--porcelain").splitlines() + [""]:
        if not line:
            if cur.get("worktree"):
                # Strip ONLY the refs/heads/ prefix. Splitting on the last "/" instead turns
                # `refs/heads/feature/x` into `x`, which resolves as no ref at all -- so
                # ahead/behind silently came back empty and every prefixed branch was reported
                # "up to date" while holding unlanded commits. A report that says clean when it
                # is not is worse than no report.
                br = cur.get("branch","")
                out.append((cur["worktree"], br[len("refs/heads/"):] if br.startswith("refs/heads/") else br))
            cur = {}
        else:
            k, _, v = line.partition(" "); cur[k] = v
    return out

def scan(name, repo, override):
    dep = deploy_branch(repo, override)
    has_remote = bool(git(repo, "remote").strip())
    rows = []
    wts = [(p, b) for p, b in worktrees(repo) if b]
    # Branches with NO worktree still hold commits. In the bare+worktrees layout every branch has
    # one, so this looked complete; in an ORDINARY repo `worktree list` returns exactly one, so the
    # tool silently reported a single branch per Tree while claiming to show "every Tree x Branch".
    # A branch with no worktree cannot be dirty -- there is nothing checked out -- so it is scanned
    # for divergence only, and marked so the reader knows why its dirty columns are empty.
    checked = {b for _, b in wts}
    for b in git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines():
        if b and b not in checked: wts.append((None, b))
    for path, br in wts:
        if not br: continue
        ahead = behind = 0
        if dep and br != dep:
            lr = git(repo, "rev-list", "--left-right", "--count", f"{dep}...{br}")
            if lr and len(lr.split()) == 2: behind, ahead = (int(x) for x in lr.split())
        # "Exists only on this disk" is `--not --remotes`: commits unreachable from ANY remote ref.
        # Falling back to `ahead of deploy` when a branch has no upstream OVERSTATES it -- those are
        # two different facts, and the commits may well be reachable from another pushed ref. On one
        # forest that fallback reported 1498 "unpushed" for a branch whose commits were all on a
        # remote under another name. Overstating risk burns the reader's trust just as fast as
        # understating it.
        up = git(repo, "rev-parse", "--abbrev-ref", "--quiet", f"{br}@{{upstream}}")
        unpushed = int(git(repo, "rev-list", "--count", br, "--not", "--remotes") or 0)
        ts = git(repo, "log", "-1", "--format=%ct", br)
        stale = int((time.time() - int(ts)) / 86400) if ts else 0
        # THREE buckets, not two. Everything under `.roots/` is NOT memory: `.roots/workbench/` is
        # the LOCAL BENCH and the spec puts it entirely outside git, `leaves/` included -- it is
        # designed to be thrown away. Counting it as memory-at-risk is not a rounding error: on the
        # first forest this ran against, the top row of the ranking scored 507 on "42 uncommitted
        # memory files" and 43 of those 45 files were bench. The real exposure was TWO files. A
        # ranking is only worth acting on if its #1 is really #1.
        rd = cd = bd = 0
        for l in (git(path, "status", "--porcelain").splitlines() if path else []):
            f = l[3:].strip('"')
            in_roots = f.startswith(".roots/") or "/.roots/" in f
            if in_roots and ("/workbench/" in f or f.startswith(".roots/workbench/")): bd += 1
            elif in_roots: rd += 1
            else: cd += 1
        # Bench files that are TRACKED are a different finding: that is the pre-1.19 contract still
        # live. Not urgent, but it is exactly what breaks silently when the seed is updated, because
        # the new spec says this folder is not versioned and nothing raises an error.
        bt = len([x for x in git(path, "ls-files", "--", ".roots/workbench").splitlines() if x]) if path else 0
        # TWO numbers, and they are not comparable -- which is why they are never summed.
        #   LOSS     = can this disappear? (uncommitted work, commits on no remote)
        #   FRICTION = is this getting more expensive? (divergence, age)
        # Summed into one score, friction won: six branches whose tips were 6-9 YEARS old, all
        # committed and all on a remote -- so with zero risk of loss -- outranked a row holding an
        # uncommitted memory file. An old landed branch cannot be lost; it only costs more to merge.
        # Ranking is lexicographic: anything that can be LOST outranks everything that merely costs.
        loss = (W["roots_dirty"]*rd + W["unpushed"]*min(unpushed,20) + W["code_dirty"]*min(cd,20)
                + W["bench_dirty"]*bd)
        fric = (W["ahead"]*min(ahead,30) + W["stale_day"]*min(stale,365) + W["behind"]*min(behind,500)
                + W["bench_tracked"]*min(bt,40))
        why = []
        if rd:       why.append(f"{rd} MEMORIA .roots sin commitear")
        if bt:       why.append(f"{bt} archivos de workbench VERSIONADOS (contrato pre-1.19)")
        if unpushed:
            # "Push these" is not advice you can follow when the repo has no remote at all. That case
            # is the HIGHER risk (nothing is backed up anywhere) but it needs a different sentence,
            # or the recommended order fills with actions that cannot be taken -- and on a local-only
            # forest the whole "land it" block came out empty for that reason alone.
            why.append(f"{unpushed} commits SIN REMOTO CONFIGURADO (no hay donde pushear)" if not has_remote
                       else f"{unpushed} en NINGUN remoto" + ("" if up else " (rama sin upstream)"))
        if not path: why.append("rama sin worktree (solo divergencia)")
        if cd:       why.append(f"{cd} archivos sucios")
        if ahead:    why.append(f"{ahead} ahead de {dep}")
        if behind:   why.append(f"{behind} behind")
        if stale > 30: why.append(f"tip de hace {stale}d")
        rows.append({"repo":name,"branch":br,"deploy":dep,"ahead":ahead,"behind":behind,
                     "unpushed":unpushed,"roots_dirty":rd,"code_dirty":cd,"stale":stale,
                     "bench_dirty":bd,"bench_tracked":bt,"has_remote":has_remote,"checked_out":bool(path),
                     "loss":round(loss,1),"fric":round(fric,1),
                     "why":"; ".join(why) or "al dia","path":path})
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forest", default=os.environ.get("FOREST", "."))
    ap.add_argument("--repo", action="append", default=[])
    ap.add_argument("--deploy", help="deploy branch name, if it is not detectable")
    ap.add_argument("--top", type=int, default=0, help="only the N most urgent (0 = all)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    forest = os.path.abspath(a.forest)

    rows = []
    for name, repo in find_repos(forest):
        if a.repo and name not in a.repo: continue
        rows += scan(name, repo, a.deploy)
    rows.sort(key=lambda r: (-r["loss"], -r["fric"]))
    if a.json: print(json.dumps(rows, indent=2, ensure_ascii=False)); return 0

    print("# weights: " + " ".join(f"{k}={v}" for k, v in W.items()))
    print("# LOSS = can disappear (uncommitted, or on no remote). fric = getting costlier (divergence,"
          " age). Sorted by LOSS first: they are not comparable, so they are never summed.")
    print(f"# {len({r['repo'] for r in rows})} trees, {len(rows)} branches. "
          "`behind` is vs the LOCAL deploy branch: fetch first if it matters.\n")
    hdr = (f"{'LOSS':>6}{'fric':>7}  {'TREE':<20}{'BRANCH':<28}{'a/b':>10}{'push':>6}{'.roots':>7}"
           f"{'bench':>6}{'code':>6}  why")
    print(hdr); print("-"*min(len(hdr)+40, 150))
    shown = rows[:a.top] if a.top else rows
    for r in shown:
        if r["loss"] == 0 and r["fric"] == 0 and a.top: continue
        print(f"{r['loss']:>6.1f}{r['fric']:>7.1f}  {r['repo'][:19]:<20}{r['branch'][:27]:<28}"
              f"{str(r['ahead'])+'/'+str(r['behind']):>10}{r['unpushed']:>6}{r['roots_dirty']:>7}"
              f"{r['bench_dirty']:>6}{r['code_dirty']:>6}  {r['why']}")

    mem  = [r for r in rows if r["roots_dirty"]]
    push = [r for r in rows if r["unpushed"] and r["has_remote"] and not r["roots_dirty"]]
    noremote = [r for r in rows if r["unpushed"] and not r["has_remote"]]
    land = [r for r in rows if r["ahead"] and not r["roots_dirty"]
            and not (r["unpushed"] and r["has_remote"])]
    print("\n# ORDEN RECOMENDADO — de lo que se pierde primero a lo que sólo se encarece")
    def block(n, title, items, fmt):
        print(f"\n{n}. {title}" + (" — nada" if not items else ""))
        for r in items[:12]: print("     " + fmt(r))
        if len(items) > 12: print(f"     … y {len(items)-12} más")
    block(1, "COMMITEAR LA MEMORIA (muere con el disco; es la regla que sostiene el seed)", mem,
          lambda r: f"{r['repo']}/{r['branch']}: {r['roots_dirty']} archivos en .roots/")
    block(2, "PUSHEAR (existe sólo en esta máquina)", push,
          lambda r: f"{r['repo']}/{r['branch']}: {r['unpushed']} commits")
    block("2b", "SIN REMOTO: no hay dónde pushear — crear uno, o aceptar que vive en un solo disco",
          noremote, lambda r: f"{r['repo']}/{r['branch']}: {r['unpushed']} commits, cero remotos")
    block(3, f"LANDEAR a su rama de deploy (cada día que pasa el merge cuesta más)", land,
          lambda r: f"{r['repo']}/{r['branch']}: {r['ahead']} ahead de {r['deploy']}"
                    + (f", tip de hace {r['stale']}d" if r['stale'] > 30 else ""))
    bench = [r for r in rows if r["bench_tracked"]]
    block(4, "REVISAR el contrato de workbench/ (versionado = contrato pre-1.19; el seed lo saca de git)",
          bench, lambda r: f"{r['repo']}/{r['branch']}: {r['bench_tracked']} archivos versionados")
    print("\n5. La memoria distribuida (copias del seed): eso lo mide `roots-seed-audit.py`.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
