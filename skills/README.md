# skills — biblioteca compartida del toolkit

> Skills cross-cutting, bien diseñadas y reutilizables, que viven en el seed para mejorar estrategias comunes (merging, reporting, etc.). Tool-agnostic: las ejecuta cualquier agente IA o humano.

---

## skills/ del toolkit vs skills/ de cada `.roots`

| | Toolkit `roots_seed/skills/` (este) | `.roots/skills/` (por módulo) |
|---|---|---|
| Alcance | **compartido** — aplica a muchos módulos/proyectos | **local** — específico de ese módulo |
| Contenido | estrategias canónicas (merging Odoo, reporting…) | `prompts.md`, `workflows.md`, `patterns.md` propios |
| Uso | se **referencia** o se **copia/adapta** dentro de un `.roots/skills/` | se mantiene junto al módulo |

Cuando un módulo necesita una de estas estrategias, la referencia desde su `.roots` (o copia la parte relevante a su `skills/workflows.md` y la adapta). Si un módulo descubre una mejora general, se **promueve** acá (mismo espíritu que la promoción de descubrimientos del seed).

## Formato de una skill

Cada skill es un `.md` con:

```markdown
# {Nombre de la skill}

> Una línea: qué resuelve.

## Cuándo usar
## Entradas / contexto requerido
## Pasos
## Verificación
## Notas / decisiones abiertas
```

## Índice

| Skill | Para qué |
|-------|----------|
| [odoo-module-merging.md](./odoo-module-merging.md) | Estrategia de merge de branches/clientes hacia repos oficiales Odoo (cross-versión, resolución de conflictos típicos, promoción de `.roots`) |
| [md-to-pdf-reporting.md](./md-to-pdf-reporting.md) | Convertir `docs/manual.md` y `documentation.md` a reportes PDF (pandoc / HTML+CSS / QWeb Odoo) |

> Próximas candidatas: revisión de seguridad de access rights, generación de `changelog.md` desde commits, smoke-test de instalación de módulo.
