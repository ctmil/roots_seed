#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""folio_design.py — parametric design by layers on a Folio board, from a forest.

A Folio **layer template** is a parametric design: a canvas plus layers, each layer with
options. The board combines one option per layer and composes every combination into a PNG
variant. You design the rules; the system derives the variants. Each variant stays tied to
your work (`moldeo.folio.work`) and signed by you.

It rides on the same board credentials as `htree.py` (profiles in `.htree.env`), and runs
every call AS the user your tree account is bound to: you see and edit only YOUR works and
templates, plus the published works of others as reference.

    python3 folio_design.py works [-p P] [--all]                 # your (unpublished) works; --all adds the published ones
    python3 folio_design.py work-new [-p P] "Name" [--yes]       # a new work, saved UNPUBLISHED
    python3 folio_design.py spec [-p P] design.json [--work ID] [--yes]   # JSON -> layer template
    python3 folio_design.py templates [-p P]                     # your templates
    python3 folio_design.py generate [-p P] <TEMPLATE_ID> [--yes]         # compose every variant
    python3 folio_design.py results [-p P] <TEMPLATE_ID> [--out DIR]      # download the PNGs + params

  Scenes (moldeo js) and sketchbooks — v1.28:
    python3 folio_design.py scenes [-p P]                                  # your scenes (+ published ones with --all)
    python3 folio_design.py scene-new [-p P] "Name" [--work ID] [--config scene.json] [--yes]
    python3 folio_design.py scene-layer [-p P] <SCENE_ID> "Name" [--type T] [--config layer.json] [--image f.png] [--yes]
    python3 folio_design.py sketchbooks [-p P] [--work ID]
    python3 folio_design.py sketchbook-new [-p P] <WORK_ID> "Name" [--scene ID] [--yes]
    python3 folio_design.py page-new [-p P] <SKETCHBOOK_ID> "Name" [--type image|video|audio|document|text] [--file F] [--yes]

  A scene is a moldeo js composition (config JSON + layers: image|text|shape|video|animation|particle|3d).
  A sketchbook gathers the process of a work: pages with images, video, audio, documents, notes.
  Raw code (js/css/html/embed, a JS library by URL) is not loaded from a collaborator account yet:
  upload the result (image/video) or describe it in a scene. Everything stays unpublished.

Writes are DRY-RUN unless --yes (exit 2 = nothing sent). Standard library only.

THE SPEC (design.json) — one object:

    {"code": "my-poster-01", "name": "My poster", "canvas": [1200, 1200], "max_variants": 6,
     "layers": [
       {"type": "base", "source": "solid",
        "options": [{"name": "night", "color": "#111111"}, {"name": "moss", "color": "#0a5c36"}]},
       {"type": "subject", "source": "static", "box": [0.1, 0.1, 0.8, 0.6],
        "options": [{"name": "oak", "path": "assets/oak.png"}]},
       {"type": "text", "source": "text", "box": [0.1, 0.75, 0.8, 0.15],
        "options": [{"name": "a", "text": "A walk", "color": "#ffffff"},
                    {"name": "b", "text": "through the forest", "color": "#00ff9f"}]}]}

  type   : base | subject | text | data | brand | decor
  source : solid | gradient | text | badge | static        (all composed on the board at $0)
  box    : [x, y, w, h] relative 0..1
  path   : a file next to design.json (sent with it) — this is how an image YOUR AI made in your
           forest enters the design. Server-side AI generation (`ai_image`) is not open to
           collaborators: the AI runs in your forest, the board composes.
  code   : unique on the board — pick something of yours.

Publishing a work is done by the organisation, never from here.
"""
import argparse
import base64
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import htree  # same folder: roots_seed/scripts/ or the workspace root
except ImportError:  # pragma: no cover
    sys.exit("folio_design.py needs htree.py next to it (it reuses its credentials).")

die = htree.die


def board(args):
    (name, vals), = htree.pick(args)
    return htree.Board(name, vals)


def dry(args, what, payload):
    if args.yes:
        return False
    print("DRY-RUN — nothing sent. Would " + what + ":")
    print(json.dumps(payload, ensure_ascii=False, indent=2)[:3000])
    print("\nRepeat with --yes to send it.")
    sys.exit(2)


def call(b, model, method, ids=None, args=None, kwargs=None):
    r = b.gw(f"/{model}/call", method=method, ids=ids or [], args=args or [], kwargs=kwargs or {})
    return r.get("result")


def cmd_works(args):
    b = board(args)
    # The board already narrows this to YOUR works plus the published ones of others.
    rows = b.search("moldeo.folio.work", [] if args.all else [["website_published", "=", False]],
                    ["code", "name", "website_published"], order="id desc")
    if not rows:
        print("No works yet. Create one:  python3 folio_design.py work-new \"Name\" --yes")
    for r in rows:
        print(f"#{r['id']:<5} {r.get('code') or '':<12} {'PUBLISHED' if r.get('website_published') else 'draft    '}  {r['name']}")


def cmd_work_new(args):
    b = board(args)
    vals = {"name": args.name}
    dry(args, f"create a work on [{b.name}]", vals)
    r = b.gw("/moldeo.folio.work/create", vals=vals)
    wid = r["ids"][0]
    row = b.search("moldeo.folio.work", [["id", "=", wid]], ["code"], limit=1)[0]
    print(f"✓ work #{wid} {row.get('code')} — saved unpublished, signed by you.")


def _load_spec(path):
    p = Path(path)
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        die(f"Cannot read the spec {path}", str(e))
    for k in ("code", "layers"):
        if k not in spec:
            die(f"The spec has no '{k}'", "See the format with:  python3 folio_design.py -h")
    assets = {}
    for layer in spec["layers"]:
        if layer.get("source") == "ai_image":
            die("Layer source 'ai_image' is not open to collaborators",
                "Generate the image in your forest and use source 'static' with a 'path'.")
        for opt in layer.get("options") or []:
            if opt.get("path"):
                f = (p.parent / opt["path"])
                if not f.is_file():
                    die(f"Asset not found: {f}", "Paths are relative to the spec file.")
                assets[opt["path"]] = base64.b64encode(f.read_bytes()).decode()
    return spec, assets


def cmd_spec(args):
    b = board(args)
    spec, assets = _load_spec(args.file)
    summary = {"code": spec["code"], "layers": [
        {"type": l.get("type"), "source": l.get("source"), "options": len(l.get("options") or [])}
        for l in spec["layers"]], "assets": {k: f"{len(v)} b64 chars" for k, v in assets.items()},
        "work": args.work}
    dry(args, f"create/update the layer template on [{b.name}]", summary)
    tid = call(b, "moldeo.folio.image.template", "create_from_spec", args=[spec, assets])["ids"][0]
    if args.work:
        b.gw("/moldeo.folio.image.template/write", ids=[tid], vals={"work_id": int(args.work)})
    row = b.search("moldeo.folio.image.template", [["id", "=", tid]],
                   ["layer_count", "combination_count"], limit=1)[0]
    print(f"✓ template #{tid} '{spec['code']}' — {row['layer_count']} layers, "
          f"{row['combination_count']} possible combinations.")
    print(f"  Next:  python3 folio_design.py generate {tid} --yes")


def cmd_templates(args):
    b = board(args)
    rows = b.search("moldeo.folio.image.template", [],
                    ["code", "name", "work_id", "layer_count", "combination_count", "max_variants"])
    if not rows:
        print("No templates yet. Make one:  python3 folio_design.py spec design.json --yes")
    for r in rows:
        w = r.get("work_id")
        print(f"#{r['id']:<4} {r['code']:<24} {r['layer_count']} layers · {r['combination_count']} combos "
              f"(max {r['max_variants']})  work: {w[1] if w else '—'}")


def cmd_generate(args):
    b = board(args)
    dry(args, f"compose every variant of template #{args.template} on [{b.name}]", {"template": args.template})
    call(b, "moldeo.folio.image.template", "action_generate_variants", ids=[int(args.template)])
    ex = b.search("moldeo.folio.experiment", [["template_id", "=", int(args.template)]],
                  ["name", "state"], limit=1, order="id desc")
    if not ex:
        die("The board did not report a run")
    n = len(b.search("moldeo.folio.experiment.result", [["experiment_id", "=", ex[0]["id"]]], ["id"]))
    print(f"✓ run '{ex[0]['name']}' — {ex[0]['state']}, {n} variants.")
    print(f"  Download:  python3 folio_design.py results {args.template} --out out/")


def cmd_results(args):
    b = board(args)
    ex = b.search("moldeo.folio.experiment", [["template_id", "=", int(args.template)]],
                  ["name"], limit=1, order="id desc")
    if not ex:
        die(f"Template #{args.template} has no runs yet",
            f"Run:  python3 folio_design.py generate {args.template} --yes")
    rows = b.search("moldeo.folio.experiment.result", [["experiment_id", "=", ex[0]["id"]]],
                    ["name", "variant_params", "output_image_full", "output_image_filename"])
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for r in rows:
        name = r.get("output_image_filename") or (r["name"] + ".png")
        if r.get("output_image_full"):
            (out / name).write_bytes(base64.b64decode(r["output_image_full"]))
        (out / (Path(name).stem + ".json")).write_text(r.get("variant_params") or "{}", encoding="utf-8")
        print(f"✓ {out / name}")
    print(f"{len(rows)} variants of '{ex[0]['name']}' in {out}/")



def _b64(path):
    f = Path(path)
    if not f.is_file():
        die(f"File not found: {f}")
    return base64.b64encode(f.read_bytes()).decode(), f.name


def _json_file(path):
    try:
        return json.dumps(json.loads(Path(path).read_text(encoding="utf-8")))
    except (OSError, ValueError) as e:
        die(f"Cannot read the JSON {path}", str(e))


def cmd_scenes(args):
    b = board(args)
    # The board only shows you your scenes and the published ones; without --all, the unpublished (yours).
    dom = [] if args.all else [["website_published", "=", False], ["state", "!=", "published"]]
    rows = b.search("moldeo.scene", dom, ["code", "name", "state", "website_published"], limit=200)
    if not rows:
        print("No scenes yet. Create one:  python3 folio_design.py scene-new \"Name\" --yes")
    for r in rows:
        print(f"#{r['id']:<5} {r.get('code') or '':<16} {r.get('state') or '':<9} {r['name']}")


def cmd_scene_new(args):
    b = board(args)
    vals = {"name": args.name}
    if args.config:
        vals["scene_config"] = _json_file(args.config)
    dry(args, f"create a scene on [{b.name}]" + (f" and set it on work #{args.work}" if args.work else ""), vals)
    sid = b.gw("/moldeo.scene/create", vals=vals)["ids"][0]
    if args.work:
        b.gw("/moldeo.folio.work/write", ids=[int(args.work)], vals={"moldeo_scene_id": sid})
    row = b.search("moldeo.scene", [["id", "=", sid]], ["code"], limit=1)[0]
    print(f"✓ scene #{sid} {row.get('code')} — unpublished." + (f" Set on work #{args.work}." if args.work else ""))


def cmd_scene_layer(args):
    b = board(args)
    vals = {"name": args.name, "scene_id": int(args.scene), "layer_type": args.type}
    if args.config:
        vals["config_json"] = _json_file(args.config)
    shown = dict(vals)
    if args.image:
        vals["image"], fname = _b64(args.image)
        shown["image"] = f"{fname} ({len(vals['image'])} b64 chars)"
    dry(args, f"add a layer to scene #{args.scene}", shown)
    lid = b.gw("/moldeo.scene.layer/create", vals=vals)["ids"][0]
    print(f"✓ layer #{lid} on scene #{args.scene}.")


def cmd_sketchbooks(args):
    b = board(args)
    dom = [["work_id", "=", int(args.work)]] if args.work else []
    rows = b.search("moldeo.folio.sketchbook", dom, ["code", "name", "state", "work_id", "page_count"], limit=200)
    if not rows:
        print("No sketchbooks yet. Create one:  python3 folio_design.py sketchbook-new <WORK_ID> \"Name\" --yes")
    for r in rows:
        w = r.get("work_id")
        print(f"#{r['id']:<5} {r.get('code') or '':<12} {r.get('state') or '':<11} work {w[0] if isinstance(w, list) else w}  pages {r.get('page_count')}  {r['name']}")


def cmd_sketchbook_new(args):
    b = board(args)
    vals = {"name": args.name, "work_id": int(args.work)}
    if args.scene:
        vals["moldeo_scene_id"] = int(args.scene)
    dry(args, f"create a sketchbook on [{b.name}]", vals)
    sid = b.gw("/moldeo.folio.sketchbook/create", vals=vals)["ids"][0]
    row = b.search("moldeo.folio.sketchbook", [["id", "=", sid]], ["code"], limit=1)[0]
    print(f"✓ sketchbook #{sid} {row.get('code')} on work #{args.work} — unpublished.")


_PAGE_FILE = {"image": ("image_1920", None), "video": ("video_file", "video_filename"),
              "audio": ("audio_file", "audio_filename"), "document": ("document_file", "document_filename")}


def cmd_page_new(args):
    b = board(args)
    vals = {"name": args.name, "sketchbook_id": int(args.sketchbook), "page_type": args.type}
    shown = dict(vals)
    if args.file:
        if args.type not in _PAGE_FILE:
            die(f"--file goes with --type {'|'.join(_PAGE_FILE)}")
        field, fname_field = _PAGE_FILE[args.type]
        vals[field], fname = _b64(args.file)
        if fname_field:
            vals[fname_field] = fname
        shown[field] = f"{fname} ({len(vals[field])} b64 chars)"
    if args.notes:
        vals["notes"] = shown["notes"] = args.notes
    dry(args, f"add a page to sketchbook #{args.sketchbook}", shown)
    pid = b.gw("/moldeo.folio.sketchbook.page/create", vals=vals)["ids"][0]
    print(f"✓ page #{pid} in sketchbook #{args.sketchbook}.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-p", "--profile", help="board profile in .htree.env")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("works", parents=[common]); s.add_argument("--all", action="store_true")
    s = sub.add_parser("work-new", parents=[common]); s.add_argument("name"); s.add_argument("--yes", action="store_true")
    s = sub.add_parser("spec", parents=[common]); s.add_argument("file"); s.add_argument("--work"); s.add_argument("--yes", action="store_true")
    sub.add_parser("templates", parents=[common])
    s = sub.add_parser("generate", parents=[common]); s.add_argument("template"); s.add_argument("--yes", action="store_true")
    s = sub.add_parser("results", parents=[common]); s.add_argument("template"); s.add_argument("--out", default="out")
    s = sub.add_parser("scenes", parents=[common]); s.add_argument("--all", action="store_true")
    s = sub.add_parser("scene-new", parents=[common]); s.add_argument("name"); s.add_argument("--work"); s.add_argument("--config"); s.add_argument("--yes", action="store_true")
    s = sub.add_parser("scene-layer", parents=[common]); s.add_argument("scene"); s.add_argument("name")
    s.add_argument("--type", default="image", choices=["image", "text", "shape", "video", "animation", "particle", "3d"])
    s.add_argument("--config"); s.add_argument("--image"); s.add_argument("--yes", action="store_true")
    s = sub.add_parser("sketchbooks", parents=[common]); s.add_argument("--work")
    s = sub.add_parser("sketchbook-new", parents=[common]); s.add_argument("work"); s.add_argument("name"); s.add_argument("--scene"); s.add_argument("--yes", action="store_true")
    s = sub.add_parser("page-new", parents=[common]); s.add_argument("sketchbook"); s.add_argument("name")
    s.add_argument("--type", default="image", choices=["image", "video", "audio", "document", "text"])
    s.add_argument("--file"); s.add_argument("--notes"); s.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    {"works": cmd_works, "work-new": cmd_work_new, "spec": cmd_spec, "templates": cmd_templates,
     "generate": cmd_generate, "results": cmd_results,
     "scenes": cmd_scenes, "scene-new": cmd_scene_new, "scene-layer": cmd_scene_layer,
     "sketchbooks": cmd_sketchbooks, "sketchbook-new": cmd_sketchbook_new, "page-new": cmd_page_new}[args.cmd](args)


if __name__ == "__main__":
    main()
