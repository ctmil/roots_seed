# Source text (es) — 2026-09-26-first-draft

> Author: Fabricio Costa Alisedo. Verbatim source; the canonical, harmonized version is [`SEED.md`](../../../SEED.md).

# roots_seed — Diseño biomimético de memoria, crecimiento y mantenimiento

## 1. Idea central

roots_seed puede entenderse no solo como un sistema de memoria persistente para agentes, sino como un modelo biomimético para sistemas de software que crecen, acumulan historia, atraviesan perturbaciones y necesitan mantener continuidad a lo largo del tiempo.

La analogía con árboles y bosques no debe funcionar únicamente como una nomenclatura visual. Puede convertirse en una guía de diseño:

qué se conserva;
qué se transforma;
qué se comparte;
qué se consolida;
qué se descarta;
cómo se distribuye el conocimiento;
cómo se mantiene una identidad a pesar del cambio.

El objetivo no es copiar literalmente la biología, sino inspirarse en dinámicas que los organismos y ecosistemas ya resuelven: crecimiento distribuido, memoria estratificada, adaptación, circulación, reparación, resiliencia y continuidad.

---

## 2. El Forest

La empresa puede pensarse como un *Forest*.

Un Forest contiene múltiples productos, repositorios, servicios, herramientas, proyectos y comunidades de trabajo. Cada uno puede tener su propia evolución, su propia memoria y su propia identidad.

En el caso de Moldeo Interactive, el Forest incluiría desarrollos muy diferentes entre sí:

conectores Odoo;
MercadoLibre;
Producteca;
Fulfillment;
herramientas de visualización;
proyectos interactivos;
productos internos;
proyectos artísticos y experimentales;
infraestructura y servicios compartidos.

El Forest no implica que todos esos elementos dependan jerárquicamente de un centro. Lo importante son las relaciones, intercambios y aprendizajes que circulan entre ellos.

---

## 3. Trees

Un *Tree* representa un producto o sistema que posee identidad propia y una historia evolutiva reconocible.

Por ejemplo:

meli_oerp puede ser un Tree;
Producteca puede ser otro Tree;
un sistema de Fulfillment puede ser otro Tree;
GeoEcon puede ser otro Tree.

Un Tree puede atravesar muchas versiones tecnológicas sin dejar de ser el mismo organismo.

El código puede cambiar radicalmente y, sin embargo, mantenerse una continuidad funcional, conceptual y arquitectónica.

---

## 4. Suites o Groves

Un *Suite* puede entenderse mejor como un *Grove*: un conjunto de Trees que crecen próximos porque comparten un nicho, recursos, infraestructura, usuarios, conocimiento o ciclos de mantenimiento.

No es necesario que sean "de la misma especie".

Por ejemplo, un Grove de comercio podría contener:

MercadoLibre;
Producteca;
Fulfillment;
conectores de pagos;
herramientas de catálogo o stock.

Cada Tree conserva autonomía, pero existe suficiente intercambio entre ellos como para que resulte útil tratarlos como una comunidad funcional.

El Grove no debe ser simplemente otro nivel jerárquico. Debe representar una verdadera proximidad ecológica.

---

## 5. Roots

Las *Roots* representan memoria persistente.

No solamente datos, sino contexto que puede volver a ser relevante:

decisiones;
errores;
aprendizajes;
tareas;
documentos;
hipótesis;
explicaciones;
conocimiento histórico.

Las raíces permiten que el presente se alimente de experiencias anteriores.

Pero almacenar información no es suficiente.

Una memoria que nunca llega al punto donde se necesita tiene poco valor operativo.

---

## 6. Trunk

El *Trunk* representa aquello que se consolidó como estructura estable.

No es simplemente código antiguo ni una carpeta central.

El Trunk está formado por invariantes que sobrevivieron suficiente tiempo como para condicionar el crecimiento futuro:

decisiones arquitectónicas aceptadas;
contratos;
límites;
convenciones;
abstracciones estables;
criterios de diseño;
patrones que demostraron ser útiles.

Una formulación posible:

*The Trunk preserves what the Tree has learned to be.*

El Trunk es histórico, no inmutable.

Puede cambiar, pero sus transformaciones deberían ser conscientes y trazables.

---

## 7. Cambium

El *Cambium* es la zona activa donde el pasado se encuentra con el presente y se produce nueva estructura.

No necesita corresponder a un directorio concreto.

Puede entenderse como el conjunto formado por:

sesiones activas;
agentes;
tareas;
contexto;
propuestas;
decisiones;
revisiones humanas.

En el cambium ocurre la transformación:

*memoria + condiciones actuales → crecimiento posible*

No todo lo que ocurre en el cambium debe convertirse en Trunk.

---

## 8. Branches

Las *Branches* representan exploraciones, adaptaciones y futuros posibles.

En un proyecto Odoo, las ramas 16, 17, 18 o 19 pueden entenderse como líneas vivas adaptadas a ambientes tecnológicos distintos.

Una Branch puede:

evolucionar;
quedar inactiva;
reactivarse;
recibir mantenimiento muchos años después;
divergir sin dejar de pertenecer al mismo Tree.

Una rama vieja no está necesariamente muerta.

Si un cliente continúa utilizando Odoo 13, esa Branch sigue formando parte del organismo y puede volver a necesitar crecimiento activo.

---

## 9. Rings

Los *Rings* representan memoria histórica estratificada.

Un Ring no es una Branch.

Tampoco es una simple copia del código de una versión anterior.

Representa un *episodio de aprendizaje consolidado*.

Por ejemplo, un Ring podría corresponder a una migración importante de Odoo y registrar:

qué condiciones externas cambiaron;
qué problemas aparecieron;
qué soluciones se intentaron;
qué soluciones se descartaron;
qué decisiones quedaron;
qué abstracciones sobrevivieron;
qué aprendió el sistema.

Git conserva el detalle de lo ocurrido.

Roots debería ayudar a conservar *qué significó lo ocurrido*.

Una fórmula útil:

**Git conserva lo que pasó.
Roots interpreta lo que significó.
La base de datos coordina lo que está pasando ahora.**

Los Rings no tienen por qué limitarse a períodos anuales ni a versiones.

También pueden representar:

una crisis;
una migración;
una transformación organizacional;
un cambio de arquitectura;
una modificación profunda del modo de trabajo.

---

## 10. Rays

Los *Rays* representan circulación transversal.

En un árbol, los radios medulares conectan regiones que no quedarían vinculadas únicamente por el crecimiento axial.

En roots_seed, los Rays representan mecanismos mediante los cuales memoria, decisiones y aprendizajes llegan al lugar donde son necesarios.

Pueden incluir:

relaciones entre Trees;
delivery de contexto;
mensajes;
sincronización;
knowledge sharing;
proyecciones de base de datos;
reglas compartidas;
promoción de aprendizajes.

Los Rays no son almacenamiento.

Son *movilidad del conocimiento*.

La circulación es bidireccional:

*Trunk → Rays → Cambium → Branch*

La estructura acumulada llega al crecimiento activo.

Y:

*Branch → Cambium → Rays → Trunk*

Una experiencia local puede viajar, generalizarse y terminar convertida en estructura estable.

Una formulación posible:

*The Rays ensure that what the Tree has learned can reach where new growth is happening — and that discoveries made at the edges can return to reshape the Tree.*

---

## 11. Wounds, Scars y structural events

Los cambios destructivos de una API externa, una dependencia o una plataforma pueden pensarse como *perturbaciones ambientales*.

Por ejemplo, MercadoLibre puede modificar una API de manera incompatible y producir una ruptura importante.

El ciclo puede modelarse como:

*perturbación → herida → contención → reparación → aprendizaje → transformación estructural*

La respuesta inmediata puede incluir:

hotfixes;
adaptadores;
compatibilidad temporal;
aislamiento del daño.

Pero algunos incidentes producen algo más profundo: fuerzan nuevas abstracciones o cambios de arquitectura.

Ese aprendizaje puede incorporarse a Rings posteriores y eventualmente al Trunk.

La memoria del incidente no debería quedar reducida a:

fix API error

sino registrar:

qué ocurrió;
qué se rompió;
por qué;
cómo se respondió;
qué cambio estructural produjo;
qué debe hacerse diferente en el futuro.

---

## 12. Knots

Un *Knot* puede reservarse para otra idea.

Botánicamente, un nudo suele estar relacionado con una rama que quedó incorporada al crecimiento del tronco.

En software puede representar una integración histórica importante:

un subsistema que comenzó como rama y quedó incorporado;
una funcionalidad inicialmente periférica que terminó formando parte de la identidad;
una integración que modificó permanentemente la geometría del sistema.

Esto permite distinguir:

*Rings* = memoria del tiempo;
*Scars* = memoria de perturbaciones y heridas;
*Knots* = memoria de integraciones;
*Trunk* = estructura que sobrevivió a todo ello.

---

## 13. Caso meli_oerp

meli_oerp es un buen ejemplo porque acumula muchos años de evolución.

El Tree ha atravesado múltiples generaciones de Odoo y cambios continuos de MercadoLibre.

Sus diferentes versiones pueden entenderse así:

Branches: Odoo 13, 16, 17, 18, 19, etc.;
Rings: los aprendizajes generados al atravesar esas generaciones;
Trunk: las abstracciones e identidad funcional que sobrevivieron;
Rays: conocimiento que viaja entre versiones y hacia otros conectores;
Scars: cambios destructivos de APIs y crisis de compatibilidad;
Cambium: el trabajo actual de mantenimiento y evolución.

Un cliente que sigue utilizando Odoo 13 muestra por qué la memoria histórica importa.

Cuando una Branch antigua se reactiva, el agente no debería encontrar únicamente código viejo.

Debería poder recuperar:

qué decisiones eran válidas en ese momento;
qué limitaciones existían;
qué problemas fueron resueltos;
qué soluciones posteriores pueden aplicarse;
qué conocimiento moderno no debe trasladarse ciegamente a esa generación.

Mantener versiones antiguas puede entenderse entonces como:

*mantener vivas distintas edades del mismo organismo sin perder la memoria que las conecta.*

Esta frase debería formar parte de los principios del Seed.

---

## 14. Base de datos

La base de datos cumple un papel diferente al de Git o Roots.

No debería convertirse en una segunda fuente de verdad histórica.

Su función principal es representar el *estado vivo y compartido del presente*.

Puede centralizar:

agentes activos;
decisiones vigentes;
tareas;
relaciones;
claims;
estado de procesos;
contexto compartido;
sincronización entre Trees.

En términos biomiméticos:

Git conserva estructura y detalle histórico;
Roots conserva memoria interpretada;
la base de datos mantiene el estado fisiológico compartido.

Esto es especialmente importante cuando múltiples agentes trabajan simultáneamente.

La base de datos les permite sincronizar no solo código, sino también:

conceptos;
patrones;
restricciones;
decisiones;
abstracciones;
contexto.

---

## 15. Institutional Tree

La empresa puede ser un Forest y, al mismo tiempo, contener un *Institutional Tree*.

Este Tree no debe ser "el jefe" de los demás.

Su función es conservar memoria e identidad organizacional.

Puede contener:

principios de diseño;
criterios arquitectónicos transversales;
políticas de mantenimiento;
convenciones;
historia de la empresa;
aprendizajes generales;
formas de relación con clientes;
decisiones estratégicas duraderas.

Un aprendizaje puede nacer en MercadoLibre, viajar mediante Rays y transformarse en principio institucional.

Por ejemplo:

*MercadoLibre Tree*

Una ruptura de API mostró que las dependencias externas estaban excesivamente acopladas.

Después de generalizar la experiencia:

*Institutional Tree*

Las dependencias externas críticas deben estar encapsuladas mediante contratos explícitos.

Ese principio puede volver después, mediante Rays, a Producteca, Fulfillment u otros Trees.

Así, la empresa *aprende como bosque*.

---

## 16. Los humanos

Los humanos deben ocupar un lugar central en este modelo.

La empresa no está constituida únicamente por software, repositorios y agentes.

Está constituida por personas que:

toman decisiones;
acumulan experiencia;
recuerdan contextos;
interpretan situaciones ambiguas;
definen prioridades;
construyen relaciones;
deciden qué debe consolidarse;
deciden qué puede desaparecer.

Los agentes pueden explorar y producir crecimiento.

Pero las decisiones estructurales significativas siguen siendo humanas.

Una persona que ha trabajado durante diez años en un sistema posee conocimiento que no está completamente contenido en los commits.

Puede recordar:

por qué una decisión se tomó;
qué alternativa fracasó;
qué cliente originó una necesidad;
qué parte del sistema parece simple pero es frágil;
qué solución "correcta" técnicamente resultó inviable en la práctica.

Ese conocimiento es *memoria encarnada*.

Roots no debería intentar reemplazarla.

Debería permitir que parte de esa experiencia pueda transformarse en memoria colectiva.

---

## 17. Tres capas de memoria

Podemos distinguir:

### Memoria encarnada

Está en las personas.

Incluye:

experiencia;
criterio;
intuición;
relaciones;
conocimiento tácito;
memoria narrativa.

### Memoria estructural

Está incorporada en los Trees.

Incluye:

código;
Trunks;
Rings;
ADRs;
documentos;
convenciones;
historia.

### Memoria activa compartida

Está en las herramientas de coordinación.

Incluye:

base de datos;
agentes;
Rays;
contexto;
tareas;
estado presente.

El objetivo no es reemplazar una capa por otra.

Es permitir circulación entre ellas.

---

## 18. Humanos dentro del ecosistema

También existen humanos que utilizan los productos generados por el Forest:

clientes;
usuarios finales;
colaboradores;
comunidades;
partners;
equipos externos.

En la analogía ecológica, pueden pensarse —con cuidado— como organismos que viven en relación con el bosque y utilizan recursos que éste produce.

Pero la analogía no debe reducir a las personas a "fauna".

Los humanos cumplen roles diferentes.

Algunos forman parte del propio Forest como cuidadores, diseñadores y tomadores de decisión.

Otros viven alrededor del Forest, utilizan sus productos y producen señales que vuelven hacia él.

El flujo puede ser:

*Forest → producto → usuario → experiencia → feedback → Forest*

Los usuarios externos no son pasivos.

Sus necesidades, errores, hábitos y respuestas modifican el ambiente en el que los Trees crecen.

Los humanos internos, en cambio, cumplen además un papel de *selección consciente*.

Deciden:

qué se convierte en estructura;
qué se mantiene experimental;
qué se poda;
qué aprendizaje se generaliza;
qué debe seguir formando parte de la identidad del sistema.

---

## 19. Conocimiento humano → memoria del Tree

Un recuerdo humano puede transformarse gradualmente en memoria colectiva.

Por ejemplo:

"En 2019 intentamos resolver este problema de MercadoLibre de determinada manera y tuvimos que abandonarla por estos motivos."

Quizás esa información no existe en ningún commit.

Puede estar distribuida entre:

memoria humana;
emails;
chats;
tickets;
commits;
documentos;
conversaciones con clientes.

Reconstruir el Ring significa reunir esas evidencias y producir una interpretación coherente:

qué ocurrió;
qué alternativas existieron;
qué se aprendió;
qué quedó estructuralmente modificado.

Entonces ocurre una transformación:

**experiencia individual  

→ evidencia y relato  

→ Ring de un Tree  

→ abstracción  

→ Rays  

→ aprendizaje institucional  

→ Trunk institucional**

Roots puede convertirse así en un puente entre:

*memoria humana + memoria de software + memoria organizacional*

---

## 20. Mantenimiento como ecología de resiliencia

Desde este punto de vista, mantenimiento no significa simplemente "corregir bugs".

Significa gestionar un organismo que vive en un ambiente cambiante.

Un sistema saludable no es el que nunca se rompe.

Es el que puede:

detectar perturbaciones;
contener daños;
mantener ramas antiguas;
reparar;
adaptarse;
aprender;
transferir conocimiento;
conservar identidad;
seguir creciendo.

El mantenimiento se convierte en una forma de *ecología de la resiliencia*.

---

## 21. Principios sintetizados

*Roots remember.*

*Rings preserve history.*

*Trunk preserves identity and structure.*

*Rays circulate memory and learning.*

*Cambium transforms memory into new growth.*

*Branches explore possible futures and preserve living pasts.*

*Scars preserve the memory of disruption.*

*Knots preserve the memory of integration.*

*The database synchronizes the living present.*

*Humans remain the primary structural decision-makers.*

*The Forest learns when local experience can become shared memory.*

---

## 22. Frases semilla

*Mantener vivas distintas edades del mismo organismo sin perder la memoria que las conecta.*

*Git conserva lo que pasó. Roots interpreta lo que significó. La base de datos coordina lo que está pasando ahora.*

*The Trunk preserves what the Tree has learned to be.*

*The Rays ensure that what the Tree has learned can reach where new growth is happening — and that discoveries made at the edges can return to reshape the Tree.*

*The Tree remains coherent not because every Branch is centrally controlled, but because accumulated structure can reach new growth, and new experience can return to modify accumulated structure.*

*La empresa no mantiene solamente distintas edades de sus sistemas. Mantiene una continuidad entre las personas que aprendieron, los productos que incorporaron ese aprendizaje y las estructuras que permiten transmitirlo a quienes llegan después.*

---

## 23. Síntesis

roots_seed puede evolucionar desde un sistema de memoria persistente para agentes hacia un modelo de *desarrollo, memoria y regulación de ecosistemas de software compuestos por humanos y agentes*.

La biomimética aporta una forma de pensar:

continuidad sin inmovilidad;
memoria sin centralización absoluta;
autonomía sin pérdida de coherencia;
crecimiento sin borrar el pasado;
mantenimiento como adaptación;
inteligencia como propiedad distribuida entre personas, agentes, software y estructura.

El punto central sigue siendo humano.

Los agentes pueden ampliar enormemente la capacidad de observar, recordar, relacionar y explorar.

Pero son las personas quienes dan sentido a esa memoria, deciden qué transformaciones importan y determinan qué debe seguir formando parte de la identidad del Forest.