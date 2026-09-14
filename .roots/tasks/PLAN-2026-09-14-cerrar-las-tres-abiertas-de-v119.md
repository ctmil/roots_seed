# PLAN 2026-09-14 — cerrar las tres abiertas que dejó la v1.19

> **Módulo · versión · branch:** `roots_seed` · spec **v1.19** (ya publicada) · branch de trabajo
> **`claude/seed-manual-al-dia`** desde `main` (`3bbff79`), worktree `roots_seed/seed-manual`.
> **Pedido (FCA, 14-sep-2026):** foco *"Seed: cerrar las 3 abiertas"* — las tres decisiones que el
> CIERRE del plan del 13-sep dejó listadas y sin resolver.
> **Criterio de terminado:** A queda hecho y verificado con `grep`; B y C quedan **puestas delante
> de FCA con los hechos medidos** y su recomendación — una decisión que es suya no se cierra sola,
> pero tampoco se deja implícita.

---

## Las tres, como las dejó el cierre del 13-sep

| # | abierta | quién decide | estado hoy |
|---|---|---|---|
| A | `manual.md` desfasado respecto de la spec | **yo** (es un hecho, no una opinión) | ✅ **HECHO** |
| B | **G10** — ¿entran al seed los patrones de agente `coordinador` y `manager read-only`? | FCA | a presentar |
| C | **`gh`** — ¿se instala, o queda el escalón 3 (URL prellenada)? | FCA | a presentar |

---

## A — `manual.md`: el número miente, pero NO como yo lo había reportado

**Lo que reporté primero y estaba mal:** *"`manual.md` dice 1.14 y la spec 1.19, el manual está
atrasado"*. Medido, la historia es otra: `manual.md` **se tocó ayer** en la tanda de la v1.19
(commit `b121b90`, *"la puerta de entrada también tenía que decirlo"*) y ya trae el sexto término
del vocabulario (Folio/Leaf), `state/` y `folios/`. O sea: **el contenido viajó y la línea 5 no.**

Y eso deja la trampa al revés de la que creí: bumpear la línea a 1.19 sin mirar el contenido sería
poner la **etiqueta fuerte sobre la fuente débil** — porque hay tres cosas que de verdad faltan.

### Los gaps medidos (`grep` + lectura de la sección, sobre `manual.md`, 154 líneas)

| gap | qué pasa | viene de |
|---|---|---|
| **A0** — `manual.md:62` dice `workbench/  user reference material` | **contrato VIEJO, ya invertido** | la v1.19 (G1) lo cambió a *mesa de trabajo local, entera fuera de git* |
| **A1** — la regla dura *"sin precisión en UN caso, no se masifica"* | ausente (`precision` 0 · `scaling` 0) | **v1.18** |
| **A2** — la **biblioteca de agentes** (`agents/`) | ausente en §3 y en §8; el repo **tiene** `agents/` con 6 archivos y README | **v1.15** |
| **A3** — el hook **`session-end`** | ausente en §9 (está `session-start` solo); la spec lo define en 7 lugares | v1.15 |

> **A0 es el hallazgo, y confirma la tesis del plan de ayer** — *"casi nada era una ausencia: era el
> arreglo hecho en un lado y el contrato viejo vivo en otro"*. Acá pasa **dentro del mismo archivo**:
> la línea 30 de `manual.md` ya usa el contrato nuevo (`workbench/leaves/`, la hoja que se suelta) y
> la línea 62, **32 líneas más abajo**, sigue con el viejo. El archivo se contradice a sí mismo, y es
> la puerta de entrada del que llega de afuera.

> Nota de método: un conteo bajo en `manual.md` **no** prueba ausencia — el manual está diseñado
> para *apuntar, no duplicar* (es su principio #1). Por eso los cuatro se verificaron **leyendo la
> sección**, no contando.

### Pasos
- [x] **A0** — §3: `workbench/` pasa al contrato nuevo (mesa local, fuera de git).
- [x] **A1** — la regla de v1.18 entra en §9, que es donde la spec la tiene (tabla de *automatic
      triggers*, línea 2861) — no en §7, porque su núcleo es método, no gasto.
- [x] **A2** — `agents/` entra en §3 (estructura) y en §8 (toolkit), con las tres capas del README
      (store → activation → base).
- [x] **A3** — `session-end` entra en §9, junto a `session-start`.
- [x] **A4** — recién entonces, línea 5: `**Seed version:** 1.14` → `1.19`.
- [x] **A5** — verificación: los cuatro conceptos vuelven > 0, y `grep -rnoE` de marcadores de
      versión en el repo entero da **un solo** número.

---

## B — G10: los dos patrones de agente que el Forest convergió

**Es decisión de FCA.** Lo que aporta esta sesión es el hecho: los dos patrones existen y están
en uso en el Forest (el **coordinador**, que es el único punto por donde entra y sale lo que el
cliente ve; y el **manager read-only**, que cruza fuentes y devuelve un tablero sin tocar nada
hacia afuera). La spec tiene biblioteca de agentes desde **v1.15** y no los tiene.

**Recomendación:** entran — pero **como recipe, no como core**, y de a uno: primero el
`manager read-only`, que es el más barato de describir y el que no tiene efectos hacia afuera.
Si ese queda bien escrito, entra el `coordinador`. (Regla dura: no se masifica sin un caso que
acierte.)

## C — `gh`: medido hoy, no supuesto

- `which gh` → **command not found**
- `GH_TOKEN` / `GITHUB_TOKEN` en el entorno → **0**
- `.github.env` en la raíz del workspace → **no existe**

O sea: el diagnóstico del 13-sep sigue valiendo tal cual. El escalón 3 (`roots-upstream.sh url`,
que imprime una URL prellenada y no necesita credenciales) **es lo único que funciona hoy**.

**Recomendación:** quedarse en el escalón 3 por ahora. Instalar `gh` sólo tiene sentido si va a
haber un flujo real de publicación a la comunidad; si no, agrega una credencial más que mantener
para algo que se usa una vez cada tanto. La regla que ya está escrita en la spec cubre el riesgo:
**no decir "abierto" si sólo se imprimió una URL.**

---

## Fuera de alcance (dicho explícitamente)
- **La redistribución del seed a la flota.** Sigue frenada, y con razón: este mismo workspace está
  en **v1.10** (9 versiones atrás) y la flota está desparramada (1.13 Comtrade · 1.5 geaiq_api/mdp/
  fop · 1.1 a2_urban_intel/yahoo_finance). Cuando se haga, va por **UNO** primero.

## Bitácora (se marca A MEDIDA, no al final)
- **14-sep** — diagnóstico read-only hecho (marcadores de versión, cobertura de conceptos, `gh`).
  Worktree y branch creados. Plan escrito. **Nada de contenido tocado todavía.**
- **14-sep** — leyendo las secciones aparece **A0** (el `workbench/` viejo vivo en §3): eran
  tres gaps y son **cuatro**. Plan reescrito antes de tocar nada.
- **14-sep ✅ A HECHO** — los cuatro gaps tapados en `manual.md` (154 → 171 líneas) y recién
  entonces la línea 5 a **1.19**. Verificado: `user reference material` → 0 · `agents/` → 2 ·
  `session-end` → 1 · `ONE case` / `spend ceiling` → 1. Marcadores de versión en los docs
  versionados: **los tres dicen 1.19**. Diary del repo con la entrada del día.
- **14-sep** — **B y C quedan en la mesa de FCA** con los hechos medidos y la recomendación escritos
  arriba. Ninguna de las dos es mía para cerrar.
