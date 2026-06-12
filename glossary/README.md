# `glossary/` — multilingual Forest vocabulary

The canonical, cross-language vocabulary of the `.roots` / Forest model.
**English is the primary language**; Spanish and French are translations (for now).

## Files

| File | Role |
|---|---|
| `glossary.json` | **Canonical source of truth.** Key = English slug; each term carries `en` / `es` / `fr` blocks (`term` + `def`), a `category`, and `see_also` cross-links. Edit this. |
| `gen.py` | Generator (stdlib only). Reads `glossary.json`, emits one `GLOSSARY.<lang>.md` table per language. |
| `GLOSSARY.en.md` | Generated — English table (reference). |
| `GLOSSARY.es.md` | Generated — Spanish table. |
| `GLOSSARY.fr.md` | Generated — French table. |

> `GLOSSARY.*.md` are **generated** — do not edit by hand. Edit `glossary.json` and run `gen.py`.

## Workflow

```bash
# 1. add or edit a term in glossary.json (always fill `en`; add es/fr when you can)
# 2. regenerate the tables
python3 gen.py
# 3. CI / pre-commit guard: fail if a table is stale
python3 gen.py --check
```

A term missing a translation falls back to its English term, flagged
`⚠ translation missing` in that language's table — so gaps stay visible
instead of silently reading as English.

## Why English-primary + a glossary (instead of full translated docs)

The seed (`roots_seed.md`, `manual.md`) is a **living spec** that bumps versions
often. Maintaining full parallel translations of every doc would drift and rot.
Instead:

- The **spec is canonical in English** (single source that evolves).
- The **glossary** carries the terminology across languages, so an agent or
  human writing a project's `.roots/` in any language uses consistent Forest
  vocabulary.

## Relation to per-module `glossary.md`

This `glossary/` holds the **Forest vocabulary** (Roots, Grove, Tree, modes,
axes…). It is different from a project's `docs/glossary.md`, which holds that
project's **domain terms**, written in the deployment's working language
(`_meta.json.lang`). See the **Language & glossary (i18n)** section of
`roots_seed.md`.

## Adding a language

1. Add the code to `meta.languages` in `glossary.json`.
2. Add a `HEADINGS[<code>]` block in `gen.py`.
3. Fill the `<code>` block per term (or let it fall back to English).
4. Run `gen.py`.
