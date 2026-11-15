# API del Moldeo Forest (gateway OCAPI tree)

> Generado desde `https://odoo.moldeointeractive.com/ocapi/tree/v1/docs` (htree 17.0.26.327). No editar a mano: se regenera de la fuente.

Base: `https://odoo.moldeointeractive.com/ocapi/tree/v1`

## Cómo se llama (leé esto primero)

Todos los endpoints son POST con un cuerpo JSON-RPC de Odoo: los parámetros van ENVUELTOS en "params": {"jsonrpc":"2.0","method":"call","params":{...}}. La respuesta viene en "result". Si mandás los parámetros sueltos (sin "params"), /auth contesta bad_request «Faltan client_id/secret_key» aunque la credencial sea correcta: no es la credencial, es el sobre.

Perfil en tu forest: `MOLDEOLAB` (`python htree.py credentials -p MOLDEOLAB`).

## De punta a punta

1. **Pedir un token** — dura 6 h; el resto de las llamadas lleva access_token

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/auth -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"client_id": "CLIENT_ID", "secret_key": "SECRETO"}}'
```

2. **Proponer una feature** — devuelve el id del hilo

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_propose", "kwargs": {"forum_id": 10, "name": "Exportar la pieza a PDF", "content": "Para un festival."}}}'
```

3. **Ver si se aceptó y qué tarea abrió** — triage y task

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_features", "kwargs": {"mine": true, "include_closed": true}}}'
```

4. **Crear la pieza** — devuelve ids

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/create -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "vals": {"name": "Ensayo de luz", "year": "2026"}}}'
```

5. **Publicarla**

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "studio_api_publish", "ids": [403]}}'
```

6. **Leer el feedback** — y lo mismo con res_model forum.post sobre tu hilo

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/messages/list -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "res_model": "moldeo.folio.work", "res_id": 403}}'
```

## 0 · Conectarse

Credencial, token y qué podés hacer.

### Pedir un token

`POST /auth`

Cambia tu credencial (client_id + secreto) por un token de 6 h. El resto de las llamadas lleva ese token.

| parámetro | tipo | | |
|---|---|---|---|
| `client_id` | str | obligatorio | el de tu credencial |
| `secret_key` | str | obligatorio | el secreto que viste UNA vez al crearla |

Devuelve: `{ok, access_token, expires, account, type, depth}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/auth -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"client_id": "CLIENT_ID", "secret_key": "SECRETO"}}'
```

Con htree.py: `python htree.py check -p MOLDEOLAB`

### Quién soy y qué puedo

`POST /whoami`

Identidad de la cuenta. En una cuenta Studio suma estado, plan, cuotas usadas, canales, repos y los permisos de la credencial.

| parámetro | tipo | | |
|---|---|---|---|
| `access_token` | str | obligatorio | de /auth |

Devuelve: `{ok, account, type, depth, user, … studio: {state, plan, usage, channels, repos, credential}}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/whoami -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN"}}'
```

Con htree.py: `python htree.py whoami -p MOLDEOLAB`

### Qué modelos y métodos alcanzo

`POST /models`

Lista los recursos que tu cuenta alcanza, con sus operaciones, métodos llamables y campos.

| parámetro | tipo | | |
|---|---|---|---|
| `access_token` | str | obligatorio | de /auth |

Devuelve: `{ok, models: [{model, ops, methods, fields}]}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/models -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN"}}'
```

### Esta documentación

`GET /docs`

Esta misma documentación, sin token. GET o POST. ?format=md la devuelve en markdown; ?audience=lab deja sólo lo de una cuenta Lab.

| parámetro | tipo | | |
|---|---|---|---|
| `format` | str | opcional | json (default) | md |
| `audience` | str | opcional | lab | tree |

Devuelve: `JSON (o markdown)`

```bash
curl -s 'https://odoo.moldeointeractive.com/ocapi/tree/v1/docs?format=md&audience=lab'
```

## 1 · Idea → Florum

Proponer una feature, votar y comentar.

### Ver los Florums de tus proyectos

`POST /forum.post/call → `florum_api_forums``

Cada proyecto tiene su Florum: lo que se acepta ahí se vuelve tarea de ESE proyecto. Sin mine_projects trae también los públicos (p. ej. el del Lab).

Permiso de la credencial: **Leer**

| parámetro | tipo | | |
|---|---|---|---|
| `mine_projects` | bool | opcional | sólo los Florums atados a proyectos que ves |

Devuelve: `[{id, name, proposal_kind, url, project: [id, nombre] | false}]`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_forums", "kwargs": {"mine_projects": true}}}'
```

### Proponer una feature

`POST /forum.post/call → `florum_api_propose``

Crea el hilo a tu nombre (texto plano: se escapa) y te suscribe para que te enteres cuando avanza. Tope por día.

Permiso de la credencial: **Participar en el Florum**

| parámetro | tipo | | |
|---|---|---|---|
| `forum_id` | int | obligatorio | de florum_api_forums |
| `name` | str | obligatorio | título, hasta 120 |
| `content` | str | opcional | texto plano; línea en blanco = párrafo |

Devuelve: `{id, name, forum, triage, vote_count, voted, mine, url, task}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_propose", "kwargs": {"forum_id": 10, "name": "Exportar la pieza a PDF", "content": "Para mandarla a un festival.\n\nCon la ficha técnica."}}}'
```

### Listar features con votos y estado

`POST /forum.post/call → `florum_api_features``

Hilos votables que ves: votos, si votaste, estado de triage y la tarea si se aceptó.

Permiso de la credencial: **Leer**

| parámetro | tipo | | |
|---|---|---|---|
| `forum_id` | int | opcional |  |
| `mine` | bool | opcional | sólo las que propusiste |
| `include_closed` | bool | opcional |  |

Devuelve: `[{id, name, vote_count, voted, triage, stage, mine, comments, url, task}]`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_features", "kwargs": {"forum_id": 10}}}'
```

Con htree.py: `python htree.py florum -p MOLDEOLAB`

### Votar (o quitar el voto)

`POST /forum.post/call → `florum_api_vote``

Idempotente: vote=true deja tu voto, vote=false lo saca. (florum_toggle_vote alterna.)

Permiso de la credencial: **Participar en el Florum**

Devuelve: `{voted, vote_count}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_vote", "ids": [1234], "kwargs": {"vote": true}}}'
```

Con htree.py: `python htree.py vote <id> --yes -p MOLDEOLAB`

### Comentar un hilo

`POST /forum.post/call → `florum_api_comment``

Comentario a tu nombre en un hilo que ves (texto plano). Tope por día.

Permiso de la credencial: **Participar en el Florum**

Devuelve: `{message_id, post_id, body_plain}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_comment", "ids": [1234], "kwargs": {"body": "Me sirve: lo necesito para el montaje."}}}'
```

## 2 · Aceptada → tarea

Ver si tu propuesta se aceptó y la tarea que abrió.

### Ver en qué quedó tu propuesta

`POST /forum.post/call → `florum_api_features``

triage = proposal | queued | accepted | rejected | duplicate. Al aceptarse, «task» trae la tarea que abrió (id, nombre, etapa).

Permiso de la credencial: **Leer**

Devuelve: `[{…, triage, task: {id, name, stage, priority}}]`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_features", "kwargs": {"mine": true, "include_closed": true}}}'
```

### Aceptar una feature de tu proyecto (abre la tarea)

`POST /forum.post/call → `florum_api_accept``

En el Florum de un proyecto TUYO aceptás vos: se crea la tarea en ese proyecto. En el Florum público del Lab acepta Moldeo (ahí da permission_denied).

Permiso de la credencial: **Gestionar mis Florums**

Devuelve: `{…, triage: accepted, task: {id, name, stage}}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/forum.post/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "florum_api_accept", "ids": [1234]}}'
```

### Comentar, adjuntar o mover la etapa de esa tarea *(pregunta abierta)*

`POST /project.task/…`

La tarea vive en un proyecto del equipo, no en tu cuenta Lab.

**Por qué no está:** Decisión de producto pendiente: ¿quien propuso puede comentar y adjuntar en la tarea, y mover su etapa (cuáles)? Mientras tanto se sigue en el hilo del Florum.

## 3 · Trabajo → Miciel

Tus agentes y skills asociados al trabajo.

### Subir tus agentes y skills (espejo del forest) *(próximamente)*

`POST /omr.agent/…`

htree.py agents push leería .claude/agents y skills de tu forest y los mostraría en la sección Miciel del Studio.

**Por qué no está:** Fase 1 de Miciel en el Studio (tarea #995): diseño escrito, espera el OK para construirse.

## 4 · Obra → Folio

Crear, editar y bajar la definición completa de tus piezas.

### Mis piezas

`POST /moldeo.folio.work/call → `studio_api_pieces``

Sólo las de tu cuenta (un search_read de moldeo.folio.work sin filtro trae todo lo publicado del sitio).

Permiso de la credencial: **Leer**

Devuelve: `[{id, name, year, published, states, channels, studio_url}]`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "studio_api_pieces"}}'
```

Con htree.py: `python htree.py pieces -p MOLDEOLAB  (seed v1.31)`

### Crear una pieza

`POST /moldeo.folio.work/create`

Nace en tu canal, en borrador y sin publicar; cuenta contra la cuota de piezas.

Permiso de la credencial: **Crear piezas**

| parámetro | tipo | | |
|---|---|---|---|
| `vals` | dict | obligatorio | name, year, technique, short_description, description, slug, subtitle, duration, dimensions; channel_id opcional |

Devuelve: `{ok, ids}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/create -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "vals": {"name": "Ensayo de luz", "year": "2026", "technique": "Instalación", "short_description": "Primer boceto"}}}'
```

Con htree.py: `python htree.py piece new "título" --yes -p MOLDEOLAB  (seed v1.31)`

### Editar una pieza

`POST /moldeo.folio.work/write`

Escribe campos de una pieza tuya.

Permiso de la credencial: **Editar mis piezas**

Devuelve: `{ok, ids}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/write -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "ids": [403], "vals": {"short_description": "Versión 2"}}}'
```

### Bajar la definición completa de una pieza

`POST /moldeo.folio.work/call → `studio_api_definition``

Obra (campos), publicaciones en tus canales, imágenes con URL y plantillas de imagen por capas con sus opciones.

Permiso de la credencial: **Leer**

Devuelve: `[{work, publications, images, image_templates}]`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "studio_api_definition", "ids": [403]}}'
```

### Listar y bajar las plantillas

`POST /moldeo.folio.work/call → `studio_api_templates``

Las plantillas de «Nueva pieza», cada una con su definición completa.

Permiso de la credencial: **Leer**

| parámetro | tipo | | |
|---|---|---|---|
| `with_definition` | bool | opcional | default true |

Devuelve: `[{id, name, short_description, definition}]`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "studio_api_templates"}}'
```

### Nueva pieza desde una plantilla

`POST /moldeo.folio.work/call → `studio_api_from_template``

Copia la plantilla (con sus plantillas de imagen) a tu canal, sin publicar. Cuenta contra la cuota.

Permiso de la credencial: **Crear piezas**

| parámetro | tipo | | |
|---|---|---|---|
| `template_id` | int | obligatorio | de studio_api_templates |
| `name` | str | obligatorio |  |
| `channel_id` | int | opcional | default: tu primer canal |

Devuelve: `{id, publication_id, studio_url}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "studio_api_from_template", "kwargs": {"template_id": 291, "name": "Mi obra nueva"}}}'
```

### Subir una imagen a una pieza

`POST /product.image.folio/create`

La imagen va en base64; cuenta contra el almacenamiento del plan.

Permiso de la credencial: **Subir assets**

Devuelve: `{ok, ids}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/product.image.folio/create -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "vals": {"work_id": 403, "name": "Vista general", "image_1920": "<base64>"}}}'
```

### Borrar una pieza *(pregunta abierta)*

`POST /moldeo.folio.work/unlink`



**Por qué no está:** Hoy no se puede ni por la API ni en el Studio web. Decisión de producto: ¿borrar o archivar, y qué pasa con lo ya publicado?

## 5 · Publicar → canal / Lab

Publicar o despublicar en tu canal.

### Publicar en tu canal

`POST /moldeo.folio.work/call → `studio_api_publish``

Publica la pieza y sus publicaciones en tus canales. La URL pública sale en la definición (work.public_url).

Permiso de la credencial: **Publicar en mi canal**

Devuelve: `{ok, result: true}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "studio_api_publish", "ids": [403]}}'
```

### Sacar de la vista pública

`POST /moldeo.folio.work/call → `studio_api_unpublish``

La pieza queda en tu Studio, sin borrar nada.

Permiso de la credencial: **Publicar en mi canal**

Devuelve: `{ok, result: true}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/call -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "method": "studio_api_unpublish", "ids": [403]}}'
```

## 6 · Repo → GitHub

Repos privados con memoria .roots.

### Tus repos

`POST /whoami`

En /whoami → studio.repos: nombre, URL, privado y si ya tiene la memoria .roots.

Devuelve: `studio.repos: [{id, full_name, url, private, roots_seeded}]`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/whoami -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN"}}'
```

### Crear un repo privado con .roots *(próximamente)*

`POST /my/studio/github`

Hoy se hace en Moldeo Studio → Repos.

**Por qué no está:** Por la API falta verificarlo con un token GitHub real de una cuenta de prueba (el del Studio web se probó contra GitHub sólo con un token rechazado).

### Vincular un repo a una pieza *(pregunta abierta)*

`POST `



**Por qué no está:** Decisión de producto: ¿un repo por pieza, por canal o por proyecto? Pide un campo nuevo.

## 7 · Vuelta → feedback

Leer lo que te contestaron y reabrir el ciclo.

### Leer los comentarios de tu pieza

`POST /messages/list`

El chatter de la pieza.

Permiso de la credencial: **Leer**

Devuelve: `{ok, records: [{id, date, author_id, body_plain}]}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/messages/list -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "res_model": "moldeo.folio.work", "res_id": 403}}'
```

### Leer las respuestas a tu propuesta

`POST /messages/list`

El chatter de tu hilo del Florum (respuestas del equipo, avisos de etapa).

Permiso de la credencial: **Leer**

Devuelve: `{ok, records: [...]}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/messages/list -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "res_model": "forum.post", "res_id": 1234}}'
```

### Reabrir el ciclo

`POST /forum.post/call`

Con lo que te contestaron, una propuesta nueva (florum_api_propose) o un voto a la que ya existe.

Permiso de la credencial: **Participar en el Florum**

## Referencia del gateway

Las llamadas genéricas que usan todas las etapas.

### Leer registros

`POST /<modelo>/search_read`

search_read de Odoo sobre un modelo expuesto, con los permisos de tu usuario.

Permiso de la credencial: **Leer**

| parámetro | tipo | | |
|---|---|---|---|
| `domain` | list | opcional | dominio de Odoo, p. ej. [["id","=",42]] |
| `fields` | list | opcional | campos; vacío = todos (puede fallar si alguno es de un modelo que no ves: pedí campos) |
| `limit` | int | opcional | default 80 |
| `offset` | int | opcional |  |
| `order` | str | opcional |  |

Devuelve: `{ok, records, count}`

```bash
curl -s https://odoo.moldeointeractive.com/ocapi/tree/v1/moldeo.folio.work/search_read -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "TOKEN", "domain": [["id", "=", 42]], "fields": ["name"]}}'
```

### Crear

`POST /<modelo>/create`

Crea uno o varios registros (vals = dict o lista de dicts).

Permiso de la credencial: **Crear piezas**

| parámetro | tipo | | |
|---|---|---|---|
| `vals` | dict|list | obligatorio |  |

Devuelve: `{ok, ids}`

### Editar

`POST /<modelo>/write`

Escribe campos en registros tuyos.

Permiso de la credencial: **Editar mis piezas**

| parámetro | tipo | | |
|---|---|---|---|
| `ids` | list | obligatorio |  |
| `vals` | dict | obligatorio |  |

Devuelve: `{ok, ids}`

### Llamar un método

`POST /<modelo>/call`

Dispara un método de la lista de llamables del modelo (ver /models). Sin ids = método de modelo.

| parámetro | tipo | | |
|---|---|---|---|
| `method` | str | obligatorio |  |
| `ids` | list | opcional |  |
| `args` | list | opcional |  |
| `kwargs` | dict | opcional |  |

Devuelve: `{ok, result}`

### Leer comentarios de un registro

`POST /messages/list`

El chatter (comentarios) de un registro que podés leer: tu pieza, un hilo del Florum, una tarea.

Permiso de la credencial: **Leer**

| parámetro | tipo | | |
|---|---|---|---|
| `res_model` | str | obligatorio |  |
| `res_id` | int | obligatorio |  |
| `message_types` | list | opcional | default ["comment","email"] |
| `limit` | int | opcional | default 80 |

Devuelve: `{ok, records: [{id, date, author_id, body, body_plain, …}]}`

### Listar / bajar adjuntos

`POST /attachments/list`

Adjuntos de un registro; include_data=true trae el contenido en base64.

Permiso de la credencial: **Leer**

| parámetro | tipo | | |
|---|---|---|---|
| `res_model` | str | obligatorio |  |
| `res_id` | int | obligatorio |  |
| `include_data` | bool | opcional |  |

Devuelve: `{ok, records}`

## Errores

| código | qué significa |
|---|---|
| `unauthorized` | Token inválido o vencido (dura 6 h: pedí otro con /auth), o credencial pausada/borrada. |
| `bad_request` | Falta un dato o el cuerpo no está envuelto en "params". |
| `permission_denied` | La credencial no tiene esa casilla (se cambia en Moldeo Studio → Credenciales), o el registro no te toca (p. ej. aceptar en un Florum que no es de tu proyecto). |
| `subscription_inactive` | La cuenta Studio no tiene una suscripción activa. |
| `subscription_readonly` | Suscripción vencida: sólo lectura, no se borró nada. |
| `quota_exceeded` | Cuota del plan superada (piezas, almacenamiento o llamadas por minuto/día). |
| `rate_limited` | Demasiadas llamadas desde tu IP; se libera solo. |
| `auth_locked` | Demasiados intentos fallidos de /auth; probá en unos minutos. |
| `below_horizon` | Ese recurso no está al alcance de tu cuenta. |
| `not_registered` | Ese modelo no está expuesto por el gateway. |
| `op_forbidden` | Esa operación no está habilitada en ese modelo. |
| `method_forbidden` | Ese método no está en la lista de llamables. |
| `orm_error` | El sistema rechazó la operación (permiso de registro o dato inválido); el mensaje dice por qué. |
| `call_error` | El método falló; el mensaje dice por qué. |
