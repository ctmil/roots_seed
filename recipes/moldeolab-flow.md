# Moldeo Lab — Ciclo de vida de proyectos, experimentos y publicación

```mermaid
flowchart TD

  %% ─────────────────────────────────────────
  %% ACTOR
  %% ─────────────────────────────────────────
  ARTISTA(["🎨 Artista / Usuario\n(vendor · portal.profile)"])

  %% ─────────────────────────────────────────
  %% 1. CREACIÓN DE PROYECTO
  %% ─────────────────────────────────────────
  subgraph CREACION["① Creación de proyecto (Prototype = Tree)"]
    direction TB
    P_NEW["Nuevo Prototype\nmoldeo.folio.prototype"]
    P_PARAM["Parametrización\n───────────────\nrepo_url · repo_owner\ndefault_branch\nmanifest_yaml  ← dependencias/stack\nspec_yaml       ← spec funcional\nai_context_md   ← memoria IA (.roots/context.md)"]
    P_MAIN["branch: main\n(canon · stage: published)"]
    P_NEW --> P_PARAM --> P_MAIN
  end

  %% ─────────────────────────────────────────
  %% 2. DISEÑO BASE (layouts + works)
  %% ─────────────────────────────────────────
  subgraph DISENIO["② Diseño base"]
    direction TB
    LY["moldeo.folio.layout\n───────────────\nlayout.section\ntemplate_body\nscss_custom"]
    WK["moldeo.folio.work\n(obra · publicación)"]
    SK["sketchbook\n(bocetos libres)"]
  end

  %% ─────────────────────────────────────────
  %% 3. EXPERIMENTOS (branches)
  %% ─────────────────────────────────────────
  subgraph EXPERIMENTO["③ Experimentos (Branch = variante)"]
    direction TB
    BR_NEW["Nueva rama\nmoldeo.folio.prototype.branch\n───────────────\nbranch_type: what-if | ai | feature\ncreated_by: human | AI\ncommit_sha\nstage: draft"]
    BR_ITER["Iteración\n(edits · IA genera · humano revisa)"]
    BR_PREV["stage: preview\npreview_url activa\n(acceso temporal por link)"]
    BR_DEC{"¿Aceptar?"}
    BR_MERGE["merged_into → main\nis_merged: true\nstage: published"]
    BR_DROP["Branch descartado\n(stage: archived)"]

    BR_NEW --> BR_ITER --> BR_PREV --> BR_DEC
    BR_DEC -- "✅ sí" --> BR_MERGE
    BR_DEC -- "❌ no" --> BR_DROP
  end

  %% ─────────────────────────────────────────
  %% 4. PUBLICACIÓN
  %% ─────────────────────────────────────────
  subgraph PUBLICACION["④ Lógica de publicación"]
    direction LR
    VIS_PRIV["🔒 PRIVADO\n─────────────\nSolo el artista ve\nel prototype y sus branches.\nNingún URL público activo."]
    VIS_PREV["🔗 PREVIEW\n─────────────\nURL temporal por branch.\nAcceso por link directo.\nNo indexado.\nUsa stage: preview\n+ preview_url"]
    VIS_PUB["🌐 PÚBLICO\n─────────────\nVisible en moldeo.org.\nIndexado y navegable\nbajo el perfil del artista.\nUsa stage: published\n(branch main o merge)"]

    VIS_PRIV -- "crear branch\n+ preview_url" --> VIS_PREV
    VIS_PREV -- "merge a main\n+ aprobar" --> VIS_PUB
    VIS_PUB -- "archivar /\nretirar" --> VIS_PRIV
    VIS_PREV -- "descartar branch" --> VIS_PRIV
  end

  %% ─────────────────────────────────────────
  %% 5. MEMORIA IA (transversal)
  %% ─────────────────────────────────────────
  subgraph IA["⑤ Memoria IA (transversal)"]
    direction TB
    AI_CTX["ai_context_md\n≡ .roots/context.md\n─────────────\nBrief del artista\nDecisiones de diseño\nEstado entre sesiones"]
    AI_VND["vendors/slug.md\n─────────────\nEstilo · paleta\nRestricciones de marca\nLinks de referencia"]
    AI_GEN["Agente IA genera\nbranch con created_by: AI\nstage: draft → preview"]
  end

  %% ─────────────────────────────────────────
  %% CONEXIONES PRINCIPALES
  %% ─────────────────────────────────────────
  ARTISTA --> CREACION
  CREACION --> DISENIO
  DISENIO --> EXPERIMENTO
  P_MAIN -. "base de\nexperimentos" .-> BR_NEW
  LY -. "extends /\ndepends-on" .-> BR_NEW
  BR_MERGE --> PUBLICACION
  P_MAIN --> VIS_PRIV

  AI_CTX -. "leído por IA\nantes de generar" .-> AI_GEN
  AI_VND -. "perfil del artista" .-> AI_GEN
  AI_GEN --> BR_NEW
  P_PARAM -. "ai_context_md" .-> AI_CTX
  ARTISTA -. "vendors/slug.md" .-> AI_VND
```

---

## Resumen de estados (stage)

| stage | Visibilidad | URL activa | ¿Mergeable? |
|---|---|---|---|
| `draft` | Solo artista | No | No |
| `preview` | Por link directo | Sí (`preview_url`) | Sí |
| `published` | Público en moldeo.org | Sí (perfil artista) | — (ya es canon) |
| `archived` | Ninguna | No | No |

## Regla de propiedad

```
prototype  ──── pertenece-a ────▶  vendor (artista)
prototype  ──── extends ─────────▶ layout base  (arista, no anidamiento)
branch     ──── bifurca-de ──────▶ prototype (main)
branch     ──── created_by ──────▶ human | AI
branch     ──── merged_into ─────▶ main  (cuando se aprueba)
```

> Un branch **nunca** pertenece a dos artistas.  
> Una variante que deriva del trabajo de otro artista es un nuevo **prototype** (fork), no un branch del original.
