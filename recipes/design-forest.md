# Receta — Bosque de diseños (plataforma creativa)

> Caso real: **Moldeo Folio + Lab** (moldeo.org) — una plataforma donde cada **artista/usuario** tiene repos con **diseños personalizados** (layouts, prototipos, obras). El objetivo: `1 vendor (artista) > N trees (repos) > diseños`, con memoria persistente por-artista que un agente IA puede crecer.

## El hallazgo: Folio ya modela el bosque en datos

| Modelo Odoo | Forest |
|---|---|
| `work_author` / `moldeo.portal.profile` / `res.partner` | **vendor** (artista) |
| `moldeo.folio.prototype` — *"Portfolio Prototype Repository"* (`repo_url`, `default_branch`, `repo_owner`, **`ai_context_md`**, `manifest_yaml`, `spec_yaml`) | **Tree** (un repo) |
| `moldeo.folio.prototype.branch` (`branch_type`, **`created_by: human\|AI`**, `commit_sha`, `stage`, `is_merged`, `merged_into`, `preview_url`) | **Branch** (variante de diseño) |
| `moldeo.folio.layout` (+`layout.section`, `template_body`, `scss_custom`) · `moldeo.folio.work` | **diseños** |

> El campo **`ai_context_md` de un prototype es un `.roots/context.md` embebido**: el puente entre el patrón `.roots` y el dato de runtime.

## Dos planos (puenteados)

**Plano DEV** — `.roots` para *desarrollar* folio/lab (modo source, Grove `moldeo`):
```
moldeo/  (Grove · vendor moldeo-interactive)
├── odoo_moldeo_folio/.roots/   ← sistema de layouts/prototipos/obras
└── odoo_moldeo_lab/.roots/       depends-on → folio, portal · plataforma creativa pública
```

**Plano PRODUCTO** — el bosque de artistas en runtime:
```
🌲 moldeo.org (Forest de artistas)
└── 🎨 artista "ada" (vendor · perfil = portal.profile / vendors/ada.md)
    ├── 🪵 prototype "neon-folio"  (Tree · ai_context_md ≡ .roots/context.md)
    │   ├── 🌿 branch main         (canon)
    │   ├── 🌿 branch ai/hero-v2   (created_by: AI · stage: preview · preview_url)
    │   └── 🌿 branch what-if/dark (variante de diseño, sin mergear)
    │   └── diseños: layout "split-hero", work "obra-01", sketchbook…
    └── 🪵 prototype "vr-room-01"  (Tree)
```

## Cómo `.roots` aporta acá

1. **Memoria por-artista-por-prototipo:** el `ai_context_md` del prototype hace de `.roots/context.md` — el agente IA recuerda el brief, las decisiones de diseño y el estado entre sesiones, por cada repo de cada artista.
2. **Bifurcación de diseño = branch:** explorar una variante (un hero distinto, modo dark) es un `prototype.branch` con `created_by: AI`, `stage: preview`, y se mergea (`merged_into`) o se descarta — igual que un branch git, pero de *diseño*.
3. **Vendor profile:** cada artista tiene `vendors/<slug>.md` (su "raíz propia"): estilo, paleta, links, restricciones de marca — que el agente lee antes de generar.
4. **El Forest agrega:** la plataforma lista artistas (vendors) → prototipos (trees) → branches (variantes) → layouts/obras (diseños). Mismo vocabulario que coordina repos de dev, ahora coordinando creadores.

## Regla de oro aplicada

Un prototype **es** del artista (vendor) y **usa** un `layout` base (arista `depends-on`/`extends`). Una variante no "pertenece a dos artistas": es un **branch** del prototype original (con `created_by` y `merged_into`). El grafo de quién-deriva-de-quién son aristas, no anidamiento.
