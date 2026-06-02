# Receta — Economía de tokens, benchmarking y técnicas por modelo

> Cómo `.roots` ahorra tokens: **leer por capas, no todo cada turno**. Más una fórmula legible, un benchmark interno, y un repo de técnicas para optimizar el uso de distintos modelos de IA. Capa transversal a todas las recetas.

## El mecanismo: la escalera de capas

El ahorro NO es comprimir texto: es **no recargar el corpus entero en cada turno**. `.roots` está pensado en capas; el agente sube de capa solo cuando hace falta.

```
L0  índice barato     MEMORY.md · context.md · forest.json · _meta.json     (casi siempre)
L1  slice activo      tasks/todo.md + _meta.current_feature + 1–2 docs       (la tarea)
L2  doc de dominio    drill on-demand: UN archivo de docs/ o worldbible/      (cuando hace falta)
L3  corpus completo   leer todo / muchos archivos                            (raro, explícito)
```

**Regla:** quedate en la capa más baja que resuelva la tarea. Los `hooks/` (session-start, on-topic-shift) y el `current_feature` de `_meta.json` existen justo para cargar el slice correcto sin barrer todo.

## Fórmula (dos números legibles)

- **CER — Context Efficiency Ratio** = `tokens_útiles / tokens_cargados`
  *(de lo que cargué, cuánto realmente usé. Bajo CER = leíste de más.)*
- **FS — Frugality Score** = `tokens_si_leo_todo / tokens_cargados`
  *("leí 1/N del corpus". FS 10 = usaste 1/10 del total disponible.)*

**Tiers de presupuesto por tarea** (tokens cargados, orientativo):

| Tier | Presupuesto | Capas típicas | Ejemplo |
|---|---|---|---|
| trivial | ≤ 5k | L0 | "¿qué versión es el seed?" |
| normal | ≤ 20k | L0 + L1 | implementar un fix acotado |
| deep | ≤ 80k | L0 + L1 + L2 | feature nuevo, refactor de un subsistema |
| full | sin tope | L3 | auditoría / migración masiva (justificar) |

Elegís tier → te mantenés en la capa más baja que lo cumpla. Si te pasás de tier, registralo (no truncar en silencio).

## Benchmark interno — `journal/benchmarks.md`

Una fila por sesión/tarea relevante:

| fecha | modelo | tarea | tokens_in | tokens_out | capas | FS | calidad (1–5) | nota |
|---|---|---|---|---|---|---|---|---|
| 2026-06-02 | opus-4.8 | fix ORM | 18k | 3k | L0+L1 | 8 | 5 | bastó context+1 doc |
| 2026-06-02 | haiku-4.5 | clasificar módulos | 6k | 1k | L0 | 14 | 4 | índice alcanzó |

Con el tiempo es un **dataset de "qué funcionó"**: qué modelo + qué capas + qué tier rindió mejor por tipo de tarea.

## Repo de técnicas por modelo — `skills/model-techniques.md`

Destilado del benchmark. Por modelo (Opus / Sonnet / Haiku y otros vendors):
- **Cuándo usar cuál:** Haiku para clasificar/extraer barato (L0); Sonnet para implementación media; Opus para diseño/razonamiento profundo.
- **Patrones de prompt** que rinden con cada uno.
- **Caché:** la TTL de caché del prompt (~5 min) — no romper el prefijo cacheado con lecturas innecesarias; agrupar trabajo dentro de la ventana.
- **Delegación:** cuándo tirar a subagentes (fan-out de búsqueda/lectura) en vez de cargar todo en el contexto principal.
- **Cuándo subir a L3:** señales de que el índice no alcanza.

## El loop de mejora

```
medir (benchmarks.md) → destilar técnica (model-techniques.md) → aplicar (escalera de capas) → medir…
```

> Mismo espíritu que el resto del seed: el conocimiento operativo (acá: cómo gastar tokens bien) se **persiste y se mejora**, no se reaprende cada sesión. Promovido al seed v1.10 porque aplica a cualquier `.roots`, no solo a este workspace.
