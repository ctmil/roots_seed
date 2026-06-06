# Moldeo Lab — Arquitectura y ciclo de vida completo

> Plataforma de creación, edición y publicación de contenidos interactivos para artistas,
> periodistas, creativos, diseñadores, analistas de datos, vendedores e inventores.
>
> **Principio central:** ctmil crea y custodia los repos privados; el usuario los opera
> con sus propias credenciales GitHub; moldeo.org es el único punto de renderizado público.

---

## Modelo de identidad y propiedad

```
ctmil (org GitHub)
  └── crea repo privado  ──────────────────────────────────────────────┐
        │                                                               │
        │  usuario conecta OAuth / token GitHub propio                 │
        │  → commits firmados por el usuario (autoría verificable)     │
        │  → ctmil mantiene ownership (protección del repo)            │
        │                                                               ▼
        └── moldeo.folio.prototype (Odoo)                    GitHub private repo
              repo_url · repo_owner: ctmil                   /usuario/proyecto
              github_user_token: <token usuario>             └── .roots/
              spec_yaml · manifest_yaml                            ├── context.md
              ai_context_md  ←──── .roots/context.md              ├── journal/
                                                                   └── tasks/
```

---

## Ciclo de vida completo

```mermaid
flowchart TD

  %% ── ACTORES ──────────────────────────────────────────────────────
  CTMIL(["🏢 ctmil\n(org propietaria)"])
  USER(["👤 Usuario / Creador\n(vendor · portal.profile)\nartista · periodista · diseñador\nanalista · vendedor · inventor"])

  %% ── PLANO PRIVADO ────────────────────────────────────────────────
  subgraph PRIVADO["🔒 PLANO PRIVADO — GitHub + Odoo"]
    direction TB

    subgraph SETUP["① Setup de proyecto"]
      REPO_CREATE["ctmil crea repo privado\nen GitHub org"]
      OAUTH["Usuario conecta\ncredenciales GitHub\n(OAuth / PAT)"]
      PROTO["moldeo.folio.prototype\n────────────────\nrepo_url\nrepo_owner: ctmil\ngithub_user_token\nspec_yaml\nmanifest_yaml\nai_context_md"]
      ROOTS_INIT[".roots/ inicializado\nen el repo\ncontext.md · journal/\ntasks/ · _meta.json"]
      REPO_CREATE --> OAUTH --> PROTO --> ROOTS_INIT
    end

    subgraph EDICION["② Edición y versionado"]
      TREE["Tree = repo privado\n(prototype)"]
      LAYOUT["moldeo.folio.layout\ntemplate_body\nscss_custom\nlayout.section"]
      WORK["moldeo.folio.work\n(obra / pieza de contenido)"]
      ROOTS_MEM[".roots/ crece\ncon cada sesión IA\ncontexto · decisiones\nbriefs · changelog"]
      TREE --> LAYOUT & WORK
      TREE --> ROOTS_MEM
    end

    subgraph EXPERIMENTOS["③ Experimentos (branches)"]
      direction TB
      BR["prototype.branch\n────────────────\nbranch_type: what-if | ai | feature\ncreated_by: human | AI\nstage: draft\ncommit_sha"]
      ITER["Iteración\n(humano edita · IA genera)"]
      PREV_PRIV["stage: preview\npreview_url activa\n(link privado, solo invitados)"]
      DECISION{"¿Aprobar?"}
      MERGE["merged_into: main\nis_merged: true"]
      DISCARD["stage: archived"]

      BR --> ITER --> PREV_PRIV --> DECISION
      DECISION -- "✅" --> MERGE
      DECISION -- "❌" --> DISCARD
    end

    SETUP --> EDICION --> EXPERIMENTOS
  end

  %% ── PLANO PÚBLICO ────────────────────────────────────────────────
  subgraph PUBLICO["🌐 PLANO PÚBLICO — moldeo.org (renderer)"]
    direction TB

    RENDER["Renderer moldeo.org\n────────────────\nlee repo privado\ncon token read-only\nNUNCA expone el source"]

    subgraph PROTECCION["Capa de protección"]
      direction LR
      OBFUSC["Obfuscación\n(minify + ruido\nen HTML/CSS/JS)"]
      WATER["Watermark digital\n(fingerprint por viewer)"]
      CORS["CORS restrictivo\n(no embeddable\nfuera de moldeo.org)"]
    end

    PUB_PROFILE["Bosque público\ndel creador\n(perfil moldeo.org)"]
    PUB_URL["URL pública\nbajo el perfil\ndel artista/autor"]

    RENDER --> PROTECCION --> PUB_PROFILE --> PUB_URL
  end

  %% ── MEMORIA IA ───────────────────────────────────────────────────
  subgraph IA["🤖 Memoria IA (transversal)"]
    direction LR
    AI_CTX["ai_context_md\n≡ .roots/context.md\nbrief · decisiones\nestado entre sesiones"]
    AI_VND["vendors/slug.md\nestilo · paleta\nrestricciones de marca"]
    AI_OUT["IA genera branch\ncreated_by: AI\nstage: draft → preview"]
    AI_CTX & AI_VND --> AI_OUT
  end

  %% ── FLUJO DE PUBLICACIÓN ─────────────────────────────────────────
  subgraph PUBFLOW["④ Lógica de publicación"]
    direction LR
    S_PRIV["🔒 PRIVADO\nsolo el creador\nsin URL externa"]
    S_PREV["🔗 PREVIEW\nlink privado\ninvitados solamente\nno indexado"]
    S_PUB["🌐 PÚBLICO\nmoldeo.org renderer\nobfuscado · watermark\nindexado bajo perfil"]

    S_PRIV -- "crear branch\npreview_url" --> S_PREV
    S_PREV -- "merge a main\naprobar publicación" --> S_PUB
    S_PUB -- "retirar" --> S_PRIV
    S_PREV -- "descartar" --> S_PRIV
  end

  %% ── CONEXIONES PRINCIPALES ───────────────────────────────────────
  CTMIL --> REPO_CREATE
  USER --> OAUTH
  MERGE --> S_PUB
  ROOTS_MEM -. "leído por IA" .-> AI_CTX
  AI_OUT --> BR
  S_PUB --> RENDER
```

---

## Por qué el renderer centralizado (opción B) protege el copyright

| Aspecto | Opción A (repo público) | Opción C (bundle deployado) | **Opción B (renderer)** |
|---|---|---|---|
| Source accesible | ✅ GitHub público | ⚠️ Bundle descargable | ❌ Nunca sale del repo privado |
| Obfuscación efectiva | Baja (source visible) | Media (bundle copiable) | **Alta (output efímero)** |
| Watermark por viewer | Difícil | Parcial | **Sí, en cada render** |
| Control de acceso | Solo por repo settings | Parcial | **Total (moldeo.org es el choke point)** |
| CORS / no-embed | No aplica | Parcial | **Sí, controlado** |
| Autoría verificable | Git history | No | **Git history del repo privado** |

> Limitación honesta: quien controla el browser controla el render (igual que YouTube/Figma/Canva).
> B + obfuscación + watermark es el estándar de la industria para contenido protegido en web.

---

## Estados y transiciones (stage)

| stage | Visibilidad | URL | Indexado | Renderer activo |
|---|---|---|---|---|
| `draft` | Solo creador | No | No | No |
| `preview` | Invitados por link | Sí (privada) | No | No (sirve raw con auth) |
| `published` | Público moldeo.org | Sí (perfil) | Sí | **Sí (obfuscado)** |
| `archived` | Ninguna | No | No | No |

---

## Tipos de creador → tipo de Tree

| Persona | Tree (prototype) | Contenido principal | Canal de publicación |
|---|---|---|---|
| Artista | portfolio · instalación | obra · sketchbook | galería moldeo.org |
| Periodista | nota · reportaje interactivo | sección · visualización | artículo moldeo.org |
| Diseñador | sistema de diseño · mockup | componente · pantalla | showcase · handoff |
| Analista de datos | dashboard · infografía | chart · tabla · narrative | reporte · embed |
| Vendedor / Fabricante | catálogo · producto | ficha técnica · configurador | tienda · landing |

> Todos comparten el mismo modelo `prototype → branch → stage → renderer`.
> Lo que cambia es el `spec_yaml` (schema por dominio) y el `manifest_yaml` (stack/dependencias).

---

## Regla de propiedad (invariante del sistema)

```
repo privado   ──── owner ──────────▶  ctmil (org)         [protección estructural]
repo privado   ──── author/editor ──▶  usuario (sus credenciales GitHub)  [autoría]
prototype      ──── pertenece-a ────▶  vendor (usuario en Odoo)
prototype      ──── extends ────────▶  layout base  (arista, no anidamiento)
branch         ──── bifurca-de ─────▶  prototype main
branch         ──── created_by ─────▶  human | AI
branch         ──── merged_into ────▶  main  (cuando se aprueba)
Tree publicado ──── renderizado-por ▶  moldeo.org (nunca expone source)
```

> Un branch nunca pertenece a dos usuarios.
> Un Tree derivado del trabajo de otro usuario es un **nuevo prototype** (fork con arista `derived-from`), no un branch del original.
