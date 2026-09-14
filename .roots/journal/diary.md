# roots_seed - Diary

> Bitácora del toolkit. Primera persona, reflexivo.

---

**14 Septiembre** - La puerta de entrada decía 1.14, y el número era lo de menos.

Vine a cerrar las tres que la v1.19 dejó abiertas y arranqué mal: reporté que `manual.md` estaba
atrasado nueve versiones porque la línea 5 decía 1.14. Medido, era al revés — el manual **se había
tocado ayer mismo** (`b121b90`) y ya traía el sexto término del vocabulario. El contenido había
viajado y el número no. Si me quedaba en el número, bumpeaba la línea a 1.19 y ponía la etiqueta
fuerte encima de algo que no había mirado.

Leyendo las secciones aparecieron cuatro huecos de verdad, y el cuarto es el que vale: la línea 30
del manual ya usa el contrato NUEVO del `workbench/` (la mesa local, la hoja que se suelta) y la
línea 62, **treinta y dos líneas más abajo**, seguía con el viejo — *"user reference material"*. El
mismo archivo contradiciéndose a sí mismo, en la puerta de entrada, que es justo lo que lee el que
llega de afuera y no tiene con qué desempatar. Es la tesis de ayer otra vez, y más apretada: casi
nada era una ausencia, era **el arreglo hecho en un lado y el contrato viejo vivo en otro**. Ayer
eso pasó entre documentos; hoy pasó adentro de uno.

Los otros tres eran deudas de versiones que nunca bajaron al manual: la regla dura de la v1.18 (sin
precisión en un caso no se masifica), la biblioteca de agentes de la v1.15 — el repo **tiene**
`agents/` con seis archivos y un README de tres capas, y ni §3 ni §8 lo nombraban — y el hook
`session-end`, que la spec define en siete lugares y el manual no tenía en ninguno. Recién con los
cuatro tapados el número se movió a 1.19.

Queda una cosa dicha y no hecha, a propósito: la redistribución. Este workspace todavía corre con la
copia en **v1.10**, nueve atrás, y la flota está desparramada entre 1.1 y 1.13. El seed sigue sin
aplicarse a sí mismo, y eso no se arregla con un barrido: se arregla con uno.

---

**13 Septiembre** - v1.19: el seed sabía guardar la memoria y no sabía entregarla.

Seis semanas de uso separaron la spec de la práctica, y el diagnóstico no fue "faltan features":
fue que **la spec resuelve cómo se GUARDA la memoria y da por hecho que el lector va a ir a
buscarla**. Eso falló tres veces con la misma forma — el bus que se escribía y nadie leía (había un
comando lector y nada obligaba a correrlo), una sesión que violó cinco reglas fechadas *con los
documentos abiertos*, y la política de contribuir upstream que quedó en prosa **quince versiones**.
La causa no es descuido y es lo que más me sirvió entender: los documentos se eligen por **tema**, y
los normativos no compiten en esa selección porque no hablan del tema, hablan de la **forma** del
trabajo. El documento que habría evitado el error es justo el que no se abre mientras se comete.
De ahí la sección nueva: la memoria no se busca, **llega**.

Lo que más me sorprendió del día fue cuánto de esto era **contradicción, no ausencia**. El
`workbench/` estaba documentado al revés de como lo usamos (carpeta del usuario, agente que no
escribe ahí, gitignore selectivo) — quien siguiera la spec commiteaba la mesa de trabajo. Y arreglar
la prosa no alcanzaba: el `init_roots.sh` seguía creando la carpeta **sin** su regla de ignore, y el
`echo` final decía "not tracked" mintiendo. La lección que me llevo es esa: **un arreglo en la prosa
que deja el script haciendo lo otro no es un arreglo**.

Los controles encontraron tres cosas que no estaban en el plan: el `manual.md` sin la mitad de lo
que existe desde la 1.17, una referencia `§ *Hooks*` a una sección inexistente (mía, del mismo día),
y **`sync-lock.sh` nombrado por la spec y ausente del repo**. Los tres salieron de barrer en vez de
recordar: todas las referencias `§ *…*` contra los H2 reales (7 de 8), todos los `.sh` que los docs
nombran contra `scripts/` (8 de 9).

Y me equivoqué una vez de forma útil: mi primer control del `.gitignore` dio que git ignoraba
**todo** y parecía un patrón roto en la spec. El roto era el control — le faltaba `!.roots/`, porque
git no desciende en un directorio excluido y el `**` solo no re-incluye nada. Quedó escrito en la
spec junto al snippet, con `git check-ignore -v` como forma de verificarlo. *Si el barrido rompe algo
ya medido como sano, el roto es el barrido.*

Lo último, y es de FCA: los cuatro comandos de comunidad. `roots-suggest`, `roots-issue`, `roots-pr`
y `roots-triage` sobre un solo script con escalera de capacidad (`gh` → token → **URL prellenada**,
que anda sin credenciales, que es como lo va a usar quien baje el seed). El cuarto es el que importa
de verdad: sin mano de vuelta, "colaborativo" va en una sola dirección y el proyecto es una
transmisión.

**02 Junio** - Toolkit sistematizado: scripts/ + skills/ + tools/ (seed v1.8).

Sistematizamos el concepto de "memoria persistente con herramientas adecuadas". Copié los `.sh` a `scripts/` (montaje de flota bare+worktrees) y arranqué `skills/` como **biblioteca compartida** de estrategias bien diseñadas — distinta del `skills/` local de cada `.roots`. Primeras dos: `odoo-module-merging` (merge hacia repos oficiales: revisión por capas, patrones de conflicto cross-versión Odoo, promoción del `.roots`) y `md-to-pdf-reporting` (manual/documentation → PDF vía pandoc / HTML+CSS / QWeb Odoo, base del reporting de odoo_moldeo_sync). Bumpeé el seed a **v1.8** con la sección "Toolkit complementario" (referencia, no inlinea código) y regeneré la copia del workspace. Decisión consciente: NO pisar los 74 `roots_seed.md` que viven en `.roots` de otros repos (sería modificar working trees ajenos); esa redistribución, si se quiere, es un merge explícito aparte.

**02 Junio** - fleet-dashboard: feed agregado, recursivo, con íconos Odoo.

Reestructuré la vista principal del dashboard a un **feed agregado de la flota** en orden de lectura: ① Cambios (journal) → ② Tareas → ③ Docs (markdown renderizado, lazy) → ④ Skills/Hooks/Debug (colapsados). El descubrimiento de `.roots` ahora es **recursivo** (cualquier profundidad, no solo raíz+subdir), y cada módulo muestra su **ícono** `static/description/icon.png` + link a su `index.html`. Lo más recién modificado arranca expandido; el resto, colapsado/lazy. Sumé al server un endpoint `/file` con guarda anti-traversal para servir íconos/md/html, y un render de markdown propio (sin deps) en la vista. Corre contra el workspace real: 79 módulos con memoria, 249 cambios, 538 tareas abiertas.

**02 Junio** - Primer tool ejecutable del seed: fleet-dashboard.

Arranqué el `.roots` propio de `roots_seed` (modo flat) y sumé `tools/fleet-dashboard/`: un visor web del estado de la flota (git + `.roots`) en tiempo real, todo con stdlib. Lo importante de diseño es que quedó en 3 capas (colector → `state.json` → vista) para que el `state.json` sea un contrato portable: la idea es que `odoo_moldeo_sync` produzca el mismo JSON desde sus modelos y reuse la vista, con la jerarquía Flota→repo→worktree→.roots mapeando a `odoo_moldeo_htree`. También lo pensamos para correr remoto (túnel SSH), despegándonos del IDE/Antigravity. El colector ya corre contra el workspace real y detecta los repos en vivo (24, no los 17 del snapshot viejo de fleet.json).

---
