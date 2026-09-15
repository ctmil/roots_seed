# PLAN 2026-09-14 — el scrub bloquea el escalón que casi nadie tiene, y no el que usa todo el mundo

> **Módulo · versión · branch:** `roots_seed` · spec **v1.19 → v1.20** · branch
> **`claude/seed-manual-al-dia`** (sigue el mismo frente), worktree `roots_seed/seed-manual`.
> **Pedido (FCA, 14-sep-2026):** confirmar que el seed ofrece publicar issues al repo público
> **de forma sanitizada**, sin desvelar información privada del usuario. *"Es importantísimo."*
> **Criterio de terminado:** el camino del escalón 3 refuse igual que el 1 y el 2, **probado con
> control positivo y negativo**; y que encontrar un defecto del seed **dispare** la oferta de
> reportarlo, en vez de depender de que alguien se acuerde de invocar el comando.

---

## Lo que SÍ está (verificado hoy, no leído del plan de ayer)

- `scripts/roots-upstream.sh` (137 líneas, ejecutable) con `check` · `scrub` · `url` · `issue`.
- Las cuatro skills con **front-matter** ⇒ los comandos `/roots-{suggest,issue,pr,triage}` existen
  de verdad. La cuarta (`roots-triage`) es la mano de vuelta.
- La **escalera de capacidad** declarada (1 `gh` → 2 `$GITHUB_TOKEN` → 3 URL prellenada) y los
  **exit codes que distinguen** publicar (0) de haber impreso una URL (4).
- El **scrub anda**. Probado hoy:
  - control **positivo** (ruta absoluta + nombre de cliente + host + IP + mail + archivo de
    credenciales) → marca las 3 líneas, `exit=1`.
  - control **negativo** (el mismo hallazgo redactado en genérico) → `clean`, `exit=0`.

## El agujero (medido, no inferido)

`cmd_issue` corre el scrub y **bloquea** si marcó… pero **sólo dentro de la rama que puede
publicar** (`if have_gh || have_token`). La rama `else` —sin `gh` y sin token— **no mira `dirty`**:
imprime igual la URL prellenada y devuelve 4.

Corrido en esta máquina, que no tiene ninguno de los dos:

```
No publishing capability on this machine. NOT opened — here is the link, a human presses it:
https://github.com/ctmil/roots_seed/issues/new?title=test&body=…%2Fmedia%2FDATA%2F0_DEV%2F…
…Enerpoint…erp.enerpoint.com.mx%20%28203.0.113.44%29…miguel%40enerpoint.com.mx…htree.env
```

**El nombre del cliente, su host, su IP, el mail de su empleado y el archivo de credenciales, todo
dentro de la query string**, y esa URL es la **última línea** de la salida — la que se copia.

Y hay dos razones por las que esto es peor de lo que parece:

1. **El escalón 3 es el estado por defecto de cualquiera que clone el seed** (y de esta máquina).
   O sea: el gate protege el camino que casi nadie tiene y deja abierto el que usa todo el mundo.
2. **La spec afirma lo contrario.** § *Contributing to the upstream* dice textual: *"on its own it
   warns without blocking, **but on the publishing path it blocks**"*. El escalón 3 **es** un camino
   de publicación — es el que termina en el issue publicado. Spec y código no dicen lo mismo, y el
   que miente es el código, en el camino más usado.

> `cmd_url` invocado directo (`roots-upstream.sh url`) **no corre el scrub en absoluto**. Es el
> mismo vector: la URL *es* la carga.

## La segunda mitad del pedido: que se DISPARE

Hoy los cuatro comandos **hay que invocarlos**. La propia spec ya nombró ese modo de falla para este
caso (*"nothing invoked them, so contributions happened when someone remembered, which is the same
failure mode as a bus that gets written and never read"*) — y lo resolvió creando el comando, que es
la mitad. La tesis de la v1.19 es justamente esa: **protocolo ≠ entrega**. Falta el disparo.

## Pasos
- [x] **B1** — el gate del scrub sale de la rama que publica y pasa a ser **uno solo**, antes de
      bifurcar: si marcó y no vino `--scrubbed`, **refuse con 5 en los tres escalones**.
- [x] **B2** — `cmd_url` también pasa por el gate (es el vector, no un printer inocente).
- [x] **B3** — controles: positivo (sucio ⇒ 5, y **ninguna URL impresa**) y negativo (limpio ⇒ 4 con
      URL). El control que cierra es **que no aparezca la URL**, no el exit code.
- [x] **B4** — el disparo: entra en la tabla de *automatic triggers* de la spec — *encontraste que el
      texto del seed está mal, se contradice o hace daño si se sigue literal ⇒ ofrecé `roots-issue`*.
- [x] **B5** — changelog de la spec: **v1.20**, y arreglar la frase de § *Contributing* que hoy
      describe un bloqueo que el código no hacía.
- [x] **B6** — la redistribución **sigue frenada** (este workspace está en v1.10). El bump no la
      dispara sola.

## Bitácora (se marca A MEDIDA)
- **14-sep** — verificación read-only + los dos controles del scrub + la corrida que expone el
  agujero. Plan escrito. **Script sin tocar todavía.**
- **14-sep ✅ B1·B2·B3 HECHO** — el gate sale a `gate_scrub()`, corre **antes** de bifurcar la
  escalera y cubre `url`. Cuatro controles: sucio por `issue` ⇒ **5 / 0 URLs** · sucio por `url` ⇒
  **5 / 0 URLs** · limpio ⇒ **4 / 1 URL** · sucio + `--scrubbed` ⇒ **4 / 1 URL**. El control que
  cierra es **que no se imprima la URL**, no el exit code.
- **14-sep ✅ B4 HECHO** — dos triggers automáticos nuevos: *el texto del seed está mal* ⇒ ofrecé
  `roots-issue` · *el uso enseñó algo que la spec no dice* ⇒ ofrecé `roots-suggest`. **Ofrecer**,
  nunca publicar como efecto colateral.
- **14-sep ✅ B5 HECHO** — changelog **v1.20**, y corregida la frase de § *Contributing* que
  describía un bloqueo que el código no hacía. Las dos skills dicen ahora lo mismo que el código.
- **14-sep ✅ B6** — redistribución **sigue frenada**. El bump a 1.20 no la dispara.
- **15-sep** — **FCA autoriza el merge a `main`** ("go"). Va por fast-forward si `main` no se movió;
  si se movió, rebase sobre `origin/main`, nunca `--force`. La redistribución **sigue frenada**.
