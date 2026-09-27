# Source text (es) — 2026-09-27-working-synthesis

> Author: Fabricio Costa Alisedo. Verbatim source; the canonical, harmonized version is [`SEED.md`](../../../SEED.md).

ROOTS / ROOTS_SEED

Diseño biomimético de memoria, evolución y mantenimiento de software

Síntesis de trabajo — septiembre de 2026

IDEA CENTRAL

Roots no se plantea solamente como una metáfora de árboles aplicada al software.

La intención es avanzar hacia un diseño biomimético: observar cómo un organismo

vivo conserva identidad, memoria, estructura, crecimiento y capacidad de adaptación,

y utilizar esos principios para organizar software, agentes, productos, clientes y

decisiones humanas.

La idea de fondo es que un sistema de software longevo no es una colección de

archivos. Es un organismo histórico.

Crece.

Se ramifica.

Sufre perturbaciones.

Se repara.

Acumula memoria.

Conserva ciertas estructuras.

Abandona otras.

Se adapta a ambientes distintos.

Y puede dar origen a otros organismos relacionados.

ESCALAS DEL ECOSISTEMA

FOREST

La empresa puede pensarse como un bosque.

Moldeo Interactive no es un único Tree, sino un ecosistema compuesto por muchos

productos, repositorios, módulos, servicios y desarrollos que tienen historias,

clientes y funciones diferentes.

TREE

Cada producto o repositorio con identidad propia puede representarse como un Tree.

Un Tree posee:

una identidad;
una historia;
un Trunk;
Rings;
Branches;
Bark;
Rays;
heridas y reparaciones;
relaciones con otros Trees.

SUITE / GROVE

Un Suite es un pequeño bosque funcional: un conjunto de Trees relacionados que

comparten dominio, infraestructura, usuarios, modelos, conocimiento y ciclos de

mantenimiento.

Ejemplo:

Suite Meli

meli_oerp
módulos de fulfillment
extensiones específicas
servicios o conectores relacionados

No es necesario que todos sean el mismo Tree. Son organismos relacionados que

crecen próximos y comparten recursos y conocimiento.

CLIENT FOREST

La empresa cliente también constituye su propio bosque.

Cuando Moldeo instala un módulo en un cliente, ese producto deja de existir solamente

como repositorio canónico: comienza a vivir dentro de otro ecosistema, sometido a un

ambiente particular, otras versiones, otros módulos, otras necesidades y otras

presiones.

SEED — IDENTIDAD GENERATIVA

La Seed no debe ser una copia reducida del producto actual.

Una semilla no contiene un árbol adulto en miniatura.

Contiene las instrucciones, restricciones y potencialidades que hacen posible que el

organismo crezca sin dejar de pertenecer a su especie.

La Seed representa:

propósito;
problema fundamental que resuelve;
identidad;
abstracciones esenciales;
principios;
invariantes;
contratos fundamentales;
linaje;
condiciones que, si desaparecen, harían que ya no estemos hablando del mismo Tree.

Ejemplo conceptual para meli_oerp:

Es un conector entre Odoo y MercadoLibre.
Sincroniza sistemas que mantienen estados independientes.
Sus entidades centrales incluyen cuentas, productos/publicaciones, pedidos,
  stock, envíos y eventos.

Debe tolerar la evolución independiente de Odoo y MercadoLibre.
Las APIs externas no deberían determinar directamente el modelo interno.
Las operaciones importantes deben ser trazables y reconstruibles.
Debe poder evolucionar durante muchos años sin perder toda compatibilidad con
  generaciones anteriores.

La Seed funciona como genoma conceptual.

TRUNK — ESTRUCTURA CONSOLIDADA

El Trunk representa lo que el Tree ha aprendido a ser.

No es simplemente la branch principal de Git.

Es la estructura consolidada y vigente del producto:

arquitectura aceptada;
modelos centrales;
relaciones;
features estructurales;
contratos;
dependencias;
patrones;
restricciones;
principios aplicados;
decisiones que ya sobrevivieron suficiente experiencia como para considerarse
  parte estable del organismo.

El Trunk debe ser visible y navegable en Roots.

Un humano o agente debería poder preguntar:

“¿Cuál es el Trunk actual de este Tree?”

Y obtener una representación explícita de su estructura conceptual.

Es importante distinguir:

MERGE DE CÓDIGO != CAMBIO DEL TRUNK

Un bug puede producir muchos commits y no modificar la identidad estructural.

En cambio, un bug difícil puede revelar una fragilidad y generar un nuevo principio:

“Las APIs externas deben atravesar adapters versionados.”

Ese aprendizaje sí puede convertirse en madera estructural.

La decisión de promover algo al Trunk es importante y debe conservar su procedencia.

WOOD / GRAIN — MADERA Y VETA

La madera representa la ingeniería interna.

La veta representa los principios y decisiones que organizan esa ingeniería.

Dos productos pueden mostrar exactamente las mismas features públicamente y, sin

embargo, estar construidos con maderas completamente diferentes.

Ejemplo:

Dos conectores dicen:

sincroniza pedidos;
sincroniza stock;
administra productos;
procesa notificaciones.

Pero uno:

desacopla APIs externas;
conserva trazabilidad;
soporta varias generaciones de Odoo;
tiene mecanismos de recuperación;
contiene diez años de decisiones y reparaciones.

El otro puede no tener nada de eso.

Las features describen capacidad visible.

La veta revela calidad estructural e inteligencia acumulada.

BARK — CORTEZA

La Bark es la interfaz pública del Tree.

Es lo que el cliente puede tocar, mirar, evaluar y entender sin conocer toda la

ingeniería interna.

Puede expresarse mediante:

landing pages;
catálogo de features;
newsletters;
changelogs legibles;
documentación comercial;
descripciones de producto;
casos de uso.

La Bark NO es una segunda definición independiente del producto.

Debe ser una proyección del mismo Tree.

Ejemplo:

Internamente:

“meli.account gobierna credenciales y configuración de sincronización.”

Bark:

“Conectá y administrá múltiples cuentas de MercadoLibre desde Odoo.”

La corteza condensa y protege.

No reemplaza la madera.

Una arquitectura deseable sería:

TREE

  -> Internal View

  -> Public View

  -> Agent View

Todas las vistas derivan del mismo organismo.

RINGS — MEMORIA ESTRUCTURAL

Los Rings representan memoria acumulada.

No son snapshots de código.

Git ya conserva el código y su secuencia histórica.

Roots debe conservar el significado de lo ocurrido.

Un Ring responde preguntas como:

¿cómo entendíamos el producto en ese período?;
¿qué decisiones fueron tomadas?;
¿qué arquitectura estaba vigente?;
¿qué cambió?;
¿por qué cambió?;
¿qué problemas aparecieron?;
¿qué soluciones fueron descartadas?;
¿qué aprendizaje sobrevivió?;
¿qué heridas transformaron la estructura?;
¿qué parte de ese aprendizaje sigue presente en el Trunk actual?

Puede adoptarse una convención simple:

1 RING = 1 AÑO

Por ejemplo:

Ring 2022

Ring 2023

Ring 2024

Ring 2025

Ring 2026

Pero dentro de cada Ring pueden existir eventos estructurales:

features importantes;
migraciones;
crisis;
cambios de API;
heridas;
respuestas;
reorganizaciones;
nuevas abstracciones.

El Ring es el paisaje de una etapa.

Esto permitiría pedir:

“Mostrame meli_oerp conceptualmente como era en 2022.”

No solamente hacer checkout de Git, sino reconstruir cómo se concebía el producto.

BRANCHES — CRECIMIENTO ACTIVO

Las Branches representan crecimiento vivo y exploratorio.

Pueden surgir por:

features;
bugs;
adaptaciones;
experimentos;
migraciones;
tickets;
cambios solicitados por clientes.

Una branch todavía no es estructura consolidada.

Es una hipótesis de crecimiento.

Flujo:

Task

-> Branch

-> Agent / desarrollo

-> PR / Merge

-> evaluación

-> ¿qué aprendimos?

Resultados posibles:

cambio puramente local;
solución técnica puntual;
aprendizaje que entra en el Ring;
principio generalizable;
candidato a modificar el Trunk.

El paso entre crecimiento y estructura corresponde metafóricamente al Cambium.

CAMBIUM — ZONA DE DECISIÓN Y TRANSFORMACIÓN

El Cambium es la región viva donde el crecimiento nuevo puede convertirse en

estructura.

En Roots representa la instancia de evaluación:

¿esto fue solamente una corrección?;
¿es una adaptación local?;
¿es conocimiento reusable?;
¿debe entrar en el Ring?;
¿modifica una abstracción?;
¿merece formar parte del Trunk?;
¿debe generar un Tree nuevo?

Los agentes pueden detectar patrones y proponer interpretaciones.

Pero las decisiones estructurales importantes pertenecen a los humanos.

El Cambium es, por tanto, una zona socio-técnica:

software + agentes + memoria + criterio humano.

RAYS — CIRCULACIÓN RADIAL DE MEMORIA Y RECURSOS

Los Rays no son features.

Los rayos medulares inspiran el mecanismo por el cual información, memoria y recursos

circulan entre la periferia viva y el interior del Tree.

En Roots, los Rays pueden representar:

relaciones;
contexto;
recuperación de memoria;
referencias entre tickets;
conexiones entre decisiones;
inyección de contexto a agentes;
propagación de patrones;
vínculos entre Rings y Branches;
circulación de conocimiento entre zonas del Tree.

Un ticket aparece normalmente en la periferia:

un cliente necesita algo,

ocurre un error,

aparece un cambio de contexto.

Ese evento viaja hacia adentro.

Flujo conceptual:

señal del ambiente

-> ticket

-> Rays

-> contexto + memoria

-> interpretación

-> Cambium

-> branch / adaptación

-> resultado

-> nueva memoria

Los Rays hacen posible el ida y vuelta.

No todo lo que llega desde la periferia debe volverse estructura.

FEATURES — RESULTADO DEL CRECIMIENTO, NO CANAL DE TRANSPORTE

Un feature no es un Ray.

Un feature es una capacidad que emerge del proceso de crecimiento.

Puede surgir porque:

muchos clientes piden algo similar;
una customización demuestra ser generalizable;
varios tickets revelan un patrón;
una crisis obliga a crear una nueva abstracción;
una necesidad recurrente madura lo suficiente.

Flujo:

Cliente A -> ticket X

Cliente B -> ticket X

Cliente C -> ticket X

          ↓

patrón recurrente

          ↓

abstracción

          ↓

feature candidato

          ↓

decisión humana

          ↓

feature común / nueva estructura

Los Rays permiten que esa experiencia viaje.

El feature es una posible consecuencia del viaje.

AZÚCARES — VALOR METABOLIZABLE

En la analogía biomimética, los azúcares pueden representar valor que el organismo

puede utilizar para crecer.

No son literalmente features.

Pueden representar aquello que resulta metabolizable:

conocimiento reusable;
aprendizaje;
una necesidad claramente expresada;
una solución que genera valor;
patrones reconocibles;
feedback que permite orientar crecimiento;
señales de uso real.

El ambiente del cliente genera señales.

El sistema las metaboliza.

Algunas se transforman en crecimiento útil.

Esta imagen ayuda a distinguir entre:

información bruta

y

valor estructuralmente utilizable.

HERIDAS, CICATRICES Y MADERA DE REACCIÓN

Un cambio destructivo de MercadoLibre o de Odoo puede funcionar como una herida.

Por ejemplo:

desaparición de una API;
ruptura de compatibilidad;
eliminación de un mecanismo legacy;
cambio radical de modelo de datos;
modificación inesperada de comportamiento.

Secuencia:

herida

-> diagnóstico

-> respuesta

-> reparación

-> cicatriz

-> posible madera de reacción

-> aprendizaje

-> Ring

-> eventual cambio estructural

Una crisis puede dejar una marca permanente en generaciones posteriores.

Roots debería conservar no solamente la solución, sino también:

qué ocurrió;
qué fue afectado;
qué se intentó;
qué falló;
qué funcionó;
qué principio surgió.

Eso convierte mantenimiento en resiliencia.

INSTALACIONES EN CLIENTES COMO INDIVIDUOS

Cuando un producto se instala en un cliente, puede considerarse que se materializa

un nuevo individuo del mismo linaje.

Repositorio canónico:

linaje / genotipo de referencia.

Instalación Cliente A:

individuo.

Instalación Cliente B:

otro individuo.

Cada individuo puede:

vivir en otra versión de Odoo;
recibir customizaciones;
sufrir heridas propias;
utilizar features diferentes;
tener condiciones ambientales distintas;
seguir ciclos de mantenimiento diferentes.

Ejemplo:

Cliente A -> Odoo 13

Cliente B -> Odoo 17

Cliente C -> Odoo 19

Todos pueden pertenecer al mismo linaje meli_oerp, pero expresarlo de manera

diferente.

Esto introduce una distinción importante:

GENOTIPO CONCEPTUAL

identidad y capacidades potenciales del producto.

FENOTIPO

forma concreta que ese producto adopta dentro del ambiente de un cliente.

CUSTOMIZATIONS — ADAPTACIÓN LOCAL

Una customización es una respuesta a un ambiente específico.

No debe suponerse que toda customización debe pasar a la siguiente generación.

Puede:

permanecer local;
desaparecer;
ser reemplazada;
transformarse;
demostrar suficiente valor como para volverse feature general.

Esto es importante para Roots porque permite conservar la historia sin confundir:

adaptación local

con

evolución de la especie.

DIGITAL MORPHOGENETIC FIELD — CAMPO MORFOGENÉTICO DIGITAL

La base central de Roots puede representarse metafóricamente como un campo

morfogenético digital.

Debe quedar explícito que se trata de una construcción biomimética y conceptual,

no de afirmar que los árboles biológicos compartan una nube central de memoria.

En Roots, la base de datos central contiene y relaciona:

agentes;
tareas;
branches;
decisiones;
contexto;
versiones;
Trees;
clientes;
instalaciones;
Rings;
relaciones;
patrones;
dependencias;
estados;
conocimiento compartido.

Puede funcionar como un campo de información que distintos individuos interpretan

según su contexto.

Ejemplo:

Existe una nueva decisión arquitectónica.

Cliente Odoo 19:

“aplicable directamente”.

Cliente Odoo 13:

“requiere adaptación”.

Cliente sin esa feature:

“no relevante”.

La misma señal no produce necesariamente la misma respuesta.

El contexto local importa.

DATABASE — COORDINACIÓN DEL PRESENTE

La base de datos no es el Trunk.

La base de datos sincroniza el presente.

Roots destila el pasado.

Git conserva la secuencia material del código.

Una síntesis útil:

Git conserva lo que ocurrió.

Roots interpreta lo que significó.

La base de datos coordina lo que está ocurriendo ahora.

Los Rings mantienen legible la historia.

Los Rays hacen circular esa historia.

El Trunk conserva lo que el sistema aprendió a ser.

CIRCULACIÓN ENTRE CLIENTE Y TREE CANÓNICO

Ciclo completo:

BOSQUE DEL CLIENTE

-> presión ambiental

-> ticket

-> Rays

-> contexto

-> branch / adaptación

-> solución

-> resultado

-> base compartida

-> comparación con otros individuos

-> patrón emergente

-> interpretación por agentes

-> decisión humana

-> Ring

-> posible cambio del Trunk

-> siguiente generación

-> nuevas instalaciones / adaptaciones

La circulación tiene dos sentidos:

PERIFERIA -> CENTRO

La experiencia local puede transformarse en memoria colectiva.

CENTRO -> PERIFERIA

La memoria colectiva puede ayudar a nuevos desarrollos y adaptaciones locales.

NUEVOS TREES — ESPECIACIÓN

Cuando un cambio deja de ser una variación razonable del mismo organismo y desarrolla:

propósito propio;
ciclo de vida propio;
modelos independientes;
usuarios diferentes;
mantenimiento distinto;
autonomía suficiente;

puede nacer un nuevo Tree.

Roots debería conservar su genealogía.

Ejemplo conceptual:

Tree: meli_fulfillment

origin_tree: meli_oerp

derived_from_ring: 2025

reason:

  fulfillment became a sufficiently independent domain

  to require its own lifecycle

No se pierde el linaje.

Aparece una nueva especie o rama evolutiva del ecosistema.

PRODUCT DEFINITION COMO OBJETO CENTRAL

La definición de producto debería dejar de ser información dispersa entre:

código;
landing;
documentos;
newsletters;
memoria de personas;
tickets;
mensajes;
mails.

Roots puede convertirla en un objeto vivo.

Ese objeto debería alimentar diferentes proyecciones:

INTERNAL VIEW

arquitectura;
modelos;
decisiones;
Rings;
contratos;
constraints.

PUBLIC VIEW / BARK

features;
landing;
newsletter;
changelog;
beneficios;
capacidades.

AGENT VIEW

Trunk relevante;
Rings relacionados;
decisiones vigentes;
restricciones;
patrones;
contexto de la tarea.

No existen tres productos.

Existe un mismo Tree con diferentes capas de lectura.

EL PAISAJE INTERNO

La historia del Tree no debería pensarse únicamente como un libro lineal.

En la madera, la historia aparece como forma.

Rings.

Vetas.

Rayos.

Curvas.

Heridas.

Cambios de densidad.

Cicatrices.

Ramas incorporadas.

Eso produce un dibujo interno.

Roots podría aspirar a construir una representación equivalente:

una geometría de la memoria.

No solo:

“qué pasó primero y qué pasó después”.

Sino:

dónde hubo más crecimiento;
qué patrones atravesaron muchos años;
dónde aparecieron tensiones;
qué decisiones conectan distintos Rings;
qué adaptaciones quedaron locales;
cuáles se volvieron estructurales;
qué Trees nacieron de otros;
cómo circuló el aprendizaje.

La identidad del producto sería parcialmente legible como paisaje.

HUMANOS

Los humanos son parte constitutiva del ecosistema.

No son observadores externos.

Portan memoria encarnada:

experiencia;
intuición;
conocimiento tácito;
criterio;
historia;
comprensión de clientes;
prioridades;
sensibilidad respecto de riesgo y valor.

Roots no busca reemplazar esa memoria.

Busca evitar que toda la continuidad del sistema dependa exclusivamente de memoria

individual.

Cuando una persona recuerda:

“en 2019 hicimos esto por esta razón”,

ese conocimiento sigue siendo frágil.

Cuando esa experiencia se convierte en un Ring relacionado con decisiones, código,

tickets y contexto, pasa a formar parte de la memoria colectiva.

Pero hay un límite importante:

EL SISTEMA PUEDE DETECTAR.

LOS AGENTES PUEDEN INTERPRETAR.

LOS HUMANOS DECIDEN.

Los humanos son los verdaderos responsables de:

decidir qué crecimiento se consolida;
determinar qué pertenece al Trunk;
definir identidad;
aceptar o rechazar patrones;
decidir cuándo una adaptación debe generalizarse;
decidir cuándo un Tree necesita dar origen a otro.

MANTENIMIENTO COMO ECOLOGÍA

Mantener software deja de significar simplemente:

“actualizar versiones viejas”.

Significa mantener vivas distintas edades de un organismo.

Un cliente puede seguir en Odoo 13 mientras otro vive en Odoo 19.

La versión vieja no está necesariamente muerta.

Puede volver a necesitar atención.

Cuando un agente entra a mantener Odoo 13, no debería recibir únicamente código viejo.

Debería poder reconstruir:

el Ring correspondiente;
la arquitectura válida en esa época;
las decisiones vigentes;
incompatibilidades conocidas;
heridas históricas;
fixes importantes;
aprendizajes posteriores que puedan ser aplicados sin romper esa generación.

Frase central:

“Mantener vivas distintas edades del mismo organismo sin perder la memoria que las

conecta.”

CASO MELI_OERP

meli_oerp es un caso especialmente adecuado porque:

posee una historia larga;
atravesó muchas generaciones de Odoo;
atravesó cambios de MercadoLibre;
conserva clientes en versiones antiguas;
produjo extensiones y módulos relacionados;
acumula conocimiento que no está solamente en Git;
parte de su memoria vive en personas, mails, mensajes, tickets y decisiones.

Roots puede realizar una dendrocronología retrospectiva.

No se trata de guardar nuevamente Git.

Se trata de reconstruir significado.

Fuentes posibles:

commits;
branches;
PRs;
issues;
tickets;
mensajes;
mails;
documentación;
newsletters;
changelogs;
conversaciones humanas;
recuerdos transcritos;
decisiones registradas.

El objetivo es reconstruir Rings y Trunk histórico.

POSIBLE EVOLUCIÓN DE ODOO MOLDEO SYNC

El módulo originalmente pensado para mantener actualizado el branch de un cliente

puede evolucionar conceptualmente.

No sería solamente:

“sincronizar código”.

Podría vincular cada instalación real con:

Tree;
Seed;
versión;
Ring;
Trunk compatible;
features disponibles;
customizaciones;
decisiones aplicables;
branch;
historial;
dependencias.

Ejemplo:

Cliente X

Odoo 13

meli_oerp 13.0.2026.37

    |

    -> Tree: meli_oerp

    -> Ring histórico correspondiente

    -> Trunk compatible

    -> features disponibles

    -> customizaciones locales

    -> decisiones posteriores retrocompatibles

    -> restricciones

Así el agente recibe no solamente un checkout de código,

sino contexto histórico y estructural.

RESUMEN DE CONCEPTOS

SEED

Identidad generativa.

Qué puede llegar a ser y qué debe seguir siendo.

TREE

Organismo de software con identidad e historia propias.

SUITE / GROVE

Pequeño bosque funcional de Trees relacionados.

FOREST

Ecosistema organizacional mayor.

TRUNK

Lo que el organismo aprendió a ser.

WOOD

Ingeniería interna consolidada.

GRAIN

Principios y decisiones que dan forma a esa ingeniería.

BARK

Interfaz pública y legible del producto.

RING

Memoria estructural de una etapa.

BRANCH

Crecimiento activo, adaptación o experimento.

CAMBIUM

Zona donde se decide qué crecimiento se transforma en estructura.

RAYS

Circulación de información, memoria y recursos entre periferia e interior.

FEATURE

Capacidad que emerge y puede consolidarse como crecimiento del producto.

SUGAR

Valor metabolizable que alimenta crecimiento.

WOUND

Perturbación importante.

SCAR

Memoria visible de una perturbación.

REACTION WOOD

Reorganización estructural provocada por una presión o crisis.

CLIENT INSTALLATION

Individuo concreto de un linaje.

CUSTOMIZATION

Adaptación local al ambiente.

DIGITAL MORPHOGENETIC FIELD

Campo central de información compartida que cada individuo interpreta según su contexto.

HUMANS

Tomadores finales de decisiones estructurales.

FRASES SEMILLA

“Git conserva lo que ocurrió.

Roots interpreta lo que significó.

La base de datos coordina lo que está ocurriendo ahora.”

“Los Rings mantienen legible la historia.

Los Rays hacen circular esa historia.

El Trunk conserva lo que el sistema aprendió a ser.”

“Mantener vivas distintas edades del mismo organismo sin perder la memoria que las conecta.”

“La corteza muestra qué hace.

La madera revela cómo está construido.

La veta muestra qué principios lo estructuran.

Los anillos explican por qué terminó siendo así.”

“El cliente ve la corteza y las ramas.

El desarrollador puede leer la madera.

El agente necesita conocer la veta.

El sistema entero conserva los anillos.”

“El campo puede detectar.

Los agentes pueden interpretar.

Los humanos deciden.”

“Una customización es crecimiento local.

Un feature es crecimiento que demostró valor suficiente para formar parte del organismo común.”

“Roots no guarda solamente una historia.

Hace visible el paisaje interno que esa historia dibujó en el organismo.”