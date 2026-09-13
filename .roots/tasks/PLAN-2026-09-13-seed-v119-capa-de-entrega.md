# PLAN 2026-09-13 — seed v1.19: la capa de ENTREGA de la memoria

> **Módulo · versión · branch:** `roots_seed` · spec v1.18 → **v1.19** · branch base
> `claude/seed-v1.17-plan-antes-de-cada-accion` (contiene v1.17 + v1.18; **`main` está en v1.16**).
> **Pedido (FCA, 13-sep-2026):** *"poner un poco al día el roots_seed en base a los usos que
> venimos dándole en el último tiempo"*.
> **Criterio de terminado:** cada gap de abajo queda (a) escrito en `roots_seed.md` con su § y su
> entrada de changelog, o (b) descartado por escrito con motivo. Nada queda "implícito".

---

## Diagnóstico (read-only, medido hoy)

La spec quedó en **v1.18 (3-ago-2026)**. Desde entonces el Forest produjo 6 semanas de uso. Medido
con `grep` sobre `roots_seed.md` (2949 líneas):

| concepto en uso hoy | ocurrencias en la spec |
|---|---|
| `workbench` | 33 — **pero con el contrato INVERTIDO** (ver G1) |
| `leaves` / `leaf-fall.sh` | 8 (todas sobre *folio*) / **0** |
| `work-claim` / `claim` | **0** / 1 (y es "un agente reclama un pedido", otra cosa) |
| `sync-lock` | 1 ✔ (es lo único del par de semáforos que sí está) |
| `outbox` · `inbox` · `UserPromptSubmit` · `socket` · `heartbeat` | **0** |

Y el `.roots/context.md` del propio repo todavía dice **"Spec en v1.7"**: el seed no se aplica a sí mismo.

### El hilo conductor (la tesis de v1.19)

Los tres hooks ejecutables que el Forest escribió entre el 25-ago y el 10-sep dicen lo mismo en su
propio docstring:

- `manifiesto-proyecto.py`: *"⇒ El manifiesto no se busca: **LLEGA**. Mismo patrón que `soporte-tab.py`."*
- `soporte-tab.py`: *"hasta ahora el bus se escribía y nadie lo leía — `comms-inbox.sh` existe, pero
  nada obliga a correrlo."*
- ambos: *"**INYECTA, NO BLOQUEA**. Un hook que bloquea termina esquivado."*

⇒ **La spec hasta v1.18 resuelve el ALMACENAMIENTO de la memoria y da por resuelta su ENTREGA.**
Sus hooks son *protocolos escritos* ("on session start, READ `state/comms.md`") — y eso es
exactamente el modo de falla que se midió: una sesión entera violó cinco reglas escritas, fechadas
y reafirmadas, **con los documentos abiertos**, porque los documentos se eligen por TEMA y los
normativos no compiten en esa selección. **Una regla en un `.md` que nadie carga no ocurre.**
v1.19 agrega la capa que faltaba: **delivery**.

---

## Gaps (ordenados por costo de no arreglarlos)

- [ ] **G1 · `workbench/` tiene el contrato al revés — es una CONTRADICCIÓN, no una ausencia.**
  La spec dice *"el usuario es quien llena el workbench, el agente no inventa contenido acá"* y
  *"gitignore selectivo: los archivos livianos se commitean"*. El uso real (regla dura del 27-ago)
  es el opuesto: **`workbench/` es la mesa de trabajo del AGENTE y está ENTERA fuera de git**.
  Quien siga la spec de hoy commitea la mesa de trabajo. Es el único gap que hace daño activo.
- [ ] **G2 · `leaves/` — el sexto sustantivo del vocabulario.** `Roots > Forest > Grove > Tree >
  Branch > **Leaf**`. Hoy la spec usa "leaf" para **Folio** (v1.16, lo que se publica) y no tiene
  nombre para **lo efímero** (evidencia de sesión). Hay que resolver la colisión, no sumar el término
  al lado: *folio* = la hoja **hacia la luz**; *leaf/`leaves/`* = la hoja **que cae**. Portar
  `docs/leaves.md` + `forest-model.md` §1.1 (medición: 1929 archivos / 246 MB en el suelo,
  invisibles a `git status` porque `.gitignore` arranca con `/*`) + `leaf-fall.sh`
  (`status`·`sweep`·`compost`) + **higiene AVISA, no bloquea**.
- [ ] **G3 · El segundo semáforo: `work-claim.sh`.** La spec tiene `sync-lock` (protege *worktrees*)
  y le falta el que protege **el trabajo** (dos sesiones contestando la misma tarea). Con las dos
  capas que el uso agregó: `session=<tab>/<pid>/<uuid8>` → **VIVA/MUERTA verificable** por el socket
  de la sesión, y `loop=<nombre>@<intervalo>` → si el frente **se vuelve a mirar solo**. La regla que
  eso cambia: **STALE ya no significa abandonado** (STALE+MUERTA se roba; STALE+VIVA **no se toca**).
- [ ] **G4 · El bus que se lee solo (`UserPromptSubmit`).** `state/comms.md` ya está en la spec, pero
  con el protocolo que falló. Agregar el patrón de **inyección** y su regla de ruteo: un mensaje llega
  a la sesión que tiene el **claim del scope**, sin saber cómo se llama su pestaña.
- [ ] **G5 · Hooks ejecutables ≠ hooks-protocolo.** Sección nueva: el catálogo de v1.18 son contratos
  en prosa; falta decir **cómo se hacen ocurrir** en un harness (`UserPromptSubmit`, `PreCompact`),
  y las tres invariantes medidas: *inyecta, no bloquea* · *todo en try/except (un hook que rompe es
  peor que un hook que falta)* · *el registro es un JSON, no el script* (`manifiesto-map.json`).
- [ ] **G6 · El acta de pre-compactación.** *"cuando compactás la conversación no tengo idea de lo que
  hiciste"*: el resumen lo escribe el agente, así que es justo lo que el humano no puede auditar.
  **El acta no es un resumen, es un registro** (hechos verificables del transcript), se **apendea**
  por sesión y gana sobre lo que el agente cuente. Encaja como primitiva de `state/`.
- [ ] **G7 · Guard de contexto.** El único aviso de que el contexto se llenó era la compactación **ya
  ocurrida** — el aviso llegaba después del daño. Dos escalones (aviso/corte), la medición delegada
  a un script, y **no bloquea**.
- [ ] **G8 · La versión del manifest nunca baja** → va al recipe `recipes/odoo-suite.md`, no al core:
  Odoo compara versión campo a campo, si no sube **el `-u` no corre** y el código queda muerto **sin
  error y sin log**. Es el bug mudo más caro del último mes y es específico del dominio.
- [ ] **G9 · Higiene del propio repo:** `.roots/context.md` dice "Spec en v1.7" (real: v1.18/v1.19) y
  el `README.md` dice "currently v1.14" (real: v1.18). El seed no se está aplicando a sí mismo.
- [ ] **G11 · Comandos `/` para la relación con la COMUNIDAD (pedido de FCA, 13-sep, en sesión).**
  *"que dentro de la semilla tenga algunos comandos que empiecen por `/` para sugerir cambios o
  publicar issues al repositorio de GitHub de roots_seed… para ir mejorando la relación con la
  comunidad y construir una herramienta más colaborativa"*.
  **No es un agregado suelto: es la MISMA tesis de v1.19 aplicada a la comunidad.** La spec ya tiene
  § *Contributing to the upstream* (4 pasos) y § *Public hygiene* (la tabla de scrub) — o sea que la
  política **ya está escrita y no ocurre**, exactamente como el bus que nadie leía. Falta la
  **superficie invocable**.
  Comandos a escribir en `skills/` (se activan a `.claude/skills/` con `sync-agents-skills.sh`):
  - `/roots-suggest` — "esto que aprendimos debería estar en el seed": toma el aprendizaje local,
    lo **generaliza y scrubea** con la tabla de Public hygiene, y redacta un issue de **propuesta**
    (incidente medido → convención propuesta → § de la spec que toca → scrub declarado).
  - `/roots-issue` — bug/ambigüedad de la spec (no propuesta): versión, sección, qué dice vs. qué falta.
  - `/roots-pr` — lleva una mejora ya escrita en el canonical local hasta un PR: diff, separar
    extensiones privadas de lo genérico, correr el **chequeo mecánico** de secretos, branch, push.
  - `/roots-triage` — la **mano de vuelta**: leer los issues abiertos del upstream y proponer qué entra.
    Sin esto "colaborativo" es de una sola dirección.
  ⚠️ **Restricción medida hoy, y es la que define el diseño:** en esta máquina **no hay `gh`**
  (`command not found`), no hay token de GitHub en el entorno ni `~/.config/gh`. Y el seed es
  público: quien lo use tendrá otro setup. ⇒ los comandos **detectan la capacidad antes de prometer**
  y degradan en tres escalones: `gh` si existe → API con token si hay → **URL de issue prellenada**
  (`/issues/new?title=…&body=…`), que **funciona siempre y sin credenciales**.
  ⇒ Y **publicar es una acción hacia afuera: se redacta y se muestra; se publica sólo con OK explícito.**

- [ ] **G12 · Mejorar el `forest-dashboard` del repo (pedido de FCA, 13-sep).** Hoy el dashboard lee
  lo **persistente** (journal · tareas · docs · skills) — es un visor de la MEMORIA. Lo que no ve es
  **lo vivo**, que es justo lo que v1.19 formaliza: quién tiene tomado qué (`claims`), qué sesión
  sigue **VIVA**, qué frentes corren en `loop` y cada cuánto, y cuánta **hojarasca** hay en el suelo
  (`leaf-fall status`). Propuesta = una **capa de pulso** sobre el visor de memoria, con el mismo
  contrato de 3 capas que ya tiene (colector → `state.json` → vista) para no romper el portable.
  Detalle a redactar en `tools/forest-dashboard/` (propuesta antes de codear).

- [ ] **G10 (descartar o diferir) · patrones de agentes que el Forest convergió después de v1.15:**
  el **coordinador** (único punto de entrada/salida hacia un externo) y el **manager read-only que
  devuelve un tablero** (mira el conjunto, no un caso; no actúa hacia afuera). Son genéricos y
  encajan en § *Agents and skills*, pero **no** son "uso nuevo de la memoria" — decidir si entran.

---

## Orden de trabajo

0. **G11** entra en la tanda (pedido en vivo) — va junto al bloque 2, porque comparte la tesis.
1. **G1** primero y solo — es el que hace daño y es corto. Verificar que la contradicción quede
   resuelta en los 33 lugares donde `workbench` aparece, no solo en la § dedicada.
2. **G2 + G3 + G4 + G5** — el bloque con tesis común (delivery). Es el corazón de v1.19.
3. **G6 + G7** — las dos primitivas de `state/` que salieron del pedido del 10-sep.
4. **G8** (recipe) y **G9** (higiene) al cierre, con el bump de versión y el changelog.

## Modo de trabajo acordado (FCA, 13-sep, en sesión)

> *"avanzá o entrá en loop preguntándome directamente qué mejorar… te voy contestando por WhatsApp
> vía el grupo Moldeo Micielo"*.
**CORREGIDO (FCA, mismo día, 2 mensajes después):** *"estaré fuera del laptop por unas horas… enfocate
en hacer loop cada 15 min y esperá mis respuestas directas desde el Moldeo Micielo"* + *"no te trabes
acá ni esperes interacción local"*.
⇒ **Modo: `/loop` 15 min.** Cada vuelta: leer el grupo → aplicar lo que conteste → avanzar un gap →
reportar. **Nada bloquea esperando la laptop.**

**Capacidad verificada ANTES de prometerla** (memoria `no-prometer-lo-que-esta-sesion-no-puede-entregar`):
- **Escribir:** Outbox + drenador `domain-whatsapp-loop` **VIVO** (`wasap@15m`) — un `approved` sin
  drenador no sale, y acá sí hay. Formato del grupo: `--to "Moldeo Micielo" --account 0`, **sin
  `--country`** (el gate de ventana horaria vive en `country`; interno ⇒ sin gate).
- **Leer:** `wa-web/dump-cdp.mjs "Moldeo Micielo"` contra la ventana CDP **ya abierta** (no abrir otra:
  el perfil tiene mutex con el wa-loop). Probado hoy: devuelve el hilo.

**Elegido originalmente: AVANZAR.** Las preguntas no bloquean la tanda — se juntan y salen por WhatsApp al grupo
**Moldeo Micielo** (`--to "Moldeo Micielo" --account 0`, interno) al cerrar el bloque, con el avance.

## Avance del 13-sep (segunda tanda)

- **✅ G12** — `tools/forest-dashboard/PROPOSAL-pulse-layer.md` (propuesta, **nada implementado**),
  enlazada desde el README del tool y anotada en `todo.md`. Medida contra el colector real (599
  líneas), no de memoria. Núcleo: **listar "lo más reciente primero" muestra ACTIVIDAD, no ANOMALÍA**
  — un frente que latía cada 20 min y lleva 60 callado se ve igual que uno que nunca estuvo activo.
  Contrato **aditivo** (`pulse`) para no romper el porte a Odoo. Commit `916c2a4`.
- **✅ G3 + G4 + G5 + G6 + G7** — § *The delivery layer* + § *Work semaphore*, y `work-claim.sh`
  portado y **probado con 4 controles** (incluido el self-check del detector de vivos y la trampa
  del `touch` que borraba el `loop` declarado). Bump a **1.19** con su changelog. Commit `b12b7ff`.
- **✅ G8** — `recipes/odoo-suite.md`: el bug mudo de la versión que no sube. Commit `052ae92`.
- **✅ G9** — README (decía v1.14) y `context.md` (decía **v1.7**, doce versiones atrás) corregidos, y
  el hecho queda anotado: **el repo del seed no se estaba aplicando el seed**. Commit `052ae92`.
- **Branch pusheado** a `origin/claude/seed-v1.19-capa-de-entrega` (respaldo; el merge a `main` NO).

### Control de coherencia (13-sep, tercera tanda — no estaba en la lista, salió de verificar)

- **✅ `manual.md`** (la puerta navegable) estaba sin el 6º término, sin los scripts de coordinación,
  sin la familia de comunidad y **sin `on-task-start`**, que existe desde la 1.17. Si la puerta no lo
  nombra, nadie llega a la sección.
- **✅ Referencia interna rota, y era mía**: la § nueva apuntaba a un `§ *Hooks*` inexistente.
  Control: barrer las referencias `§ *…*` contra los H2/H3 reales — **7 de 8** estaban bien.
- **✅ `sync-lock.sh` se referenciaba en la spec y NO existía en el repo** (referencia rota
  preexistente, que yo amplifiqué al listarlo en el toolkit). Portado y probado (exclusión mutua
  entre dos sesiones). Control: barrer **todos** los `.sh` que los docs nombran — **8 de 9** estaban.
- **✅ El bootstrap deshacía el arreglo de G1**: `init_roots.sh` creaba `workbench/` y **nunca
  escribía su ignore** (y el `echo` final decía *"not tracked"*). Ahora crea carpeta + `leaves/` +
  la regla, idempotente, y declara 1.19 en vez de 1.17.
  ⚠️ **Y mi primer control estaba mal**: dio que git ignoraba **todo** y parecía un patrón roto en la
  spec; le faltaba `!.roots/` (git no desciende en un directorio excluido, así que `**` solo no
  re-incluye nada). *Si tu barrido rompe algo ya medido como sano, el roto es el barrido.* El
  snippet de la spec ahora muestra el bloque completo y usa `.roots/**/workbench/`, verificado con
  `git check-ignore -v` y `git add -A -n`: entra el `changelog`, no entran ni el borrador ni la hoja.

### Cuarta tanda — el vocabulario y sus restos (13-sep)

- **✅ Glosario** (el contrato i18n del seed, 3 idiomas): entraron **10 términos** de la v1.19
  (`leaf` al lado de `folio`, `leaf-fall`, `work-semaphore`, `session-liveness`, `declared-loop`,
  `delivery-layer`, `inbox-delivery`, `session-minutes`, `context-guard`, `capability-ladder`).
  Y lo importante: **la entrada `workbench` repetía en en/es/fr la definición vieja** — *"el usuario
  lo llena, el agente sólo consulta"*. Una contradicción **en el glosario viaja más lejos** que una
  en la prosa, porque el glosario es lo que alguien lee para entender el modelo. 56 → 66 términos,
  tablas regeneradas, `gen.py --check` pasa; verificado además lo que `gen.py` **no** mira: cero
  `see_also` rotos, cero idiomas faltantes, cero categorías inválidas.
- **✅ Dos restos del contrato viejo en `skills/`**: `md-to-pdf-reporting` mandaba a referenciar
  imágenes desde `workbench/` (con el contrato nuevo = **enlace roto en todo otro clone**), y
  `roots-issue` usaba como ejemplo una frase que la spec ya no dice, lo que la hacía parecer vigente.
- **Diario del propio seed** con la entrada de la v1.19 (lo que costó entender, no la lista de commits).

### Quinta tanda — probar el camino real, y el molde (13-sep)

- **✅ Probado `roots-upstream.sh issue` por el camino que la gente va a usar** (sin `gh`, sin token):
  dice bien *"NOT opened, acá está el link"* … **y salía con `exit 0`**. Un humano leía la frase y
  entendía; un script leía el código y **no podía distinguir "te di una URL" de "publiqué"** — la
  misma confusión que la regla prohíbe, sobreviviendo en el contrato de salida. Ahora `0` publicado ·
  `3` podría y no se confirmó · `4` **no publicado, URL entregada** · `5` rehusado por el scrub.
  Los 4 caminos probados.
- **✅ El scrub ahora BLOQUEA en el camino de publicación** (en el resto del seed la higiene sólo
  avisa, porque un barrido se repite; **un issue público no se despublica** y una credencial está
  filtrada apenas se renderiza). Forzable con `--scrubbed`, después de leer cada hit.
- **✅ `domain-keeper.template.md`**: el molde describía un agente *"dueño declarado"* de su dominio
  que **no tomaba el claim en ningún lado**. Paso 0 = el semáforo; + declarar el `loop`; + la
  evidencia a `leaves/`.
- **✅ `_meta.json` del propio seed**: estaba mal en casi todos los campos (`seed_version` 1.7,
  descripción citando la v1.8, 4 scripts de 9, 2 skills de 8, y `tools` nombrando *fleet*-dashboard,
  que ya no se llama así).

**Queda sólo G10** (patrones de agentes: coordinador · manager read-only de tablero), que es una
decisión de alcance suya.

## Decisiones que NO son mías (pendientes de FCA)

- [ ] **`main` está en v1.16**; v1.17 y v1.18 viven sin mergear en `claude/seed-v1.17-…`. ¿v1.19 sale
      sobre esa rama y después se mergea todo junto a `main`? (el merge/push a `main` se confirma).
- [ ] ¿Entra **G10** en v1.19 o queda para una v1.20 de "biblioteca de agentes"?

## Bitácora (se marca A MEDIDA, no al final)

- **13-sep** — diagnóstico read-only terminado; plan escrito. Nada tocado todavía.
- **13-sep** — FCA suma **G11** (comandos `/` hacia la comunidad) y fija el modo (avanzar + WhatsApp).
  Medido en el acto: **no hay `gh` ni token** ⇒ el diseño degrada a URL prellenada.
- **13-sep** — branch de trabajo creado: **`claude/seed-v1.19-capa-de-entrega`** (desde v1.18).
- **13-sep ✅ G1 HECHO** — § *Workbench* reescrita: de "carpeta del usuario, gitignore selectivo" a
  **mesa de trabajo local, entera fuera de git**, con el corolario *"no se excepciona el ignore, se
  MUDA"*. Corregidos además los 5 lugares del resto del doc que repetían el contrato viejo
  (estructura base ×2, best-practice #16, `state/` vs `workbench/`, el `init_roots.sh`).
- **13-sep ✅ G2 HECHO** — `leaves/` entra como **sexto término** del vocabulario Forest (+ la nota de
  que los 5 primeros nombran lo que se queda y el 6º lo que se va), § propia con la medición
  (1929/246 MB), el naming por fecha+frente, la trampa del **nombre relativo pelado**, y la tabla
  **Leaf vs Folio** que resuelve la colisión de v1.16 (folio = hoja **guardada**, leaf = hoja
  **soltada**). `scripts/leaf-fall.sh` portado al inglés, generalizado (`FOREST`/`LEAF_KEEP` por env,
  sin rutas del workspace privado) y **probado** con un control positivo.
- **13-sep ✅ G11 HECHO** — `scripts/roots-upstream.sh` (`check`·`scrub`·`issue`·`url`) con la
  **escalera de capacidad declarada** y probado con control positivo y negativo del scrub; las 4
  skills `roots-{suggest,issue,pr,triage}.md`; § *Contributing to the upstream* de la spec ampliada
  con los comandos, la escalera y las dos reglas (no decir "abierto" si sólo se imprimió una URL ·
  publicar exige `--yes`); índices de `skills/README.md` y del toolkit al día. Commit `10b2c8c`.
  **Hallazgo de fondo:** la política existía desde la **v1.4** y quedó en prosa **quince versiones**.
- **13-sep** — FCA suma **G12** (mejoras al `forest-dashboard`) y fija el **modo loop 15 min**.
  Encolado y aprobado el 1er reporte al grupo (`ob-micielo-seed-v119-20260913-1`, `queued`, sin gate).
