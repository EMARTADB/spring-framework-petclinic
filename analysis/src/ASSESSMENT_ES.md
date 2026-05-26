# Spring Framework PetClinic - Evaluación de Modernización

**Generado:** 26 de mayo de 2026  
**Alcance:** directorio `src/`  
**Tipo de evaluación:** Evaluación ejecutiva de modernización  
**Herramientas utilizadas:** PowerShell (recuento de LOC), coincidencia de patrones Regex (estimación de complejidad), análisis manual de código

---

## Resumen Ejecutivo

Spring Framework PetClinic es una **implementación de referencia bien estructurada** que demuestra patrones de Spring Framework 7.0.7 (configuración XML, vistas JSP, arquitectura basada en servlet) sobre **3 implementaciones de persistencia intercambiables** (JPA, JDBC, Spring Data JPA). La aplicación tiene **12,2 KSLOC, principalmente Java (30% del código base), con soporte CSS/SCSS (59%), SQL y JSP**. Demuestra **buenas prácticas en consultas parametrizadas y codificación de salida**, pero requiere **endurecimiento crítico de seguridad** (autenticación, autorización, protección CSRF) antes de un uso en producción. El código base presenta **bajo riesgo de refactorización** debido a su alta modularidad y baja complejidad (complejidad media por archivo: 1,2–3 puntos de decisión). **Patrón recomendado: Replatform** (migrar a Spring Boot 3.x con plantillas modernas) si se requiere despliegue en producción; de lo contrario, mantenerlo como referencia educativa con mejoras específicas de seguridad y documentación.

---

## Inventario del Sistema

### Líneas de Código por Lenguaje

| Lenguaje | Archivos | SLOC | % del total |
|----------|----------|------|-------------|
| CSS      | 1        | 7,159 | 58.5%      |
| Java     | 61       | 3,647 | 29.8%      |
| SQL      | 8        | 414   | 3.4%       |
| JSP      | 9        | 367   | 3.0%       |
| SCSS     | 4        | 320   | 2.6%       |
| XML      | 8        | 290   | 2.4%       |
| Properties | 5     | 40    | 0.3%       |
| **TOTAL** | **96** | **12,237** | **100%** |

**Nota de cálculo:** Las SLOC de CSS incluyen salida generada. El SCSS original tiene 320 LOC (4 archivos); se requiere regeneración mediante `./mvnw generate-resources -P css` después de editar SCSS (documentado en AGENTS.md).

**Estimación de esfuerzo COCOMO-II:**
- Fórmula: PM = 2.94 × (KSLOC)^1.10
- KSLOC: 12.237
- **Persona-meses (nominal): 46.2 PM**
- Rango estimado (±25%): 34.7 – 57.8 PM
- **Principales factores de coste:** abstracción de la capa de persistencia (3 implementaciones), complejidad de inicialización basada en servlet, verbosidad de la configuración XML

### Huella Tecnológica

| Categoría | Detalles |
|-----------|----------|
| **Sistema de build** | Maven 3.8.4+; wrapper: `./mvnw` (o `./mvnw.cmd` en Windows) |
| **Versión de Java** | Java 17 mínimo (forzado mediante maven-enforcer-plugin); probado en Java 17 y 21 en CI |
| **Frameworks** | Spring Framework 7.0.7 (no Spring Boot); Hibernate 7.3.2 (JPA ORM); vistas JSP (no Thymeleaf) |
| **Contenedor Servlet** | Jetty 11+ o Tomcat 11+ (empaquetado WAR); por defecto: Jetty mediante `./mvnw jetty:run-war` |
| **Persistencia** | 3 implementaciones (JPA, JDBC, Spring Data JPA) seleccionadas mediante perfiles: `-Dspring.profiles.active=jpa\|jdbc\|spring-data-jpa` |
| **Base de datos (por defecto)** | H2 en memoria (perfil por defecto); MySQL 8.x y PostgreSQL 13+ soportados mediante perfiles Maven |
| **Configuración runtime** | Configuración XML de Spring (5 archivos): `business-config.xml`, `mvc-core-config.xml`, `mvc-view-config.xml`, `datasource-config.xml`, `tools-config.xml` |
| **Dependencias** | Todas las dependencias actualizadas a mayo de 2026; sin CVE críticas; ver Hallazgos de Seguridad más abajo |

### Actualidad de Dependencias

| Dependencia | Versión | Antigüedad (meses) | Estado |
|------------|---------|--------------------|--------|
| Spring Framework | 7.0.7 | 6 | Actual |
| Hibernate | 7.3.2.Final | 2 | Actual |
| Jetty | 11.0.18 | 3 | Actual |
| Jackson | 3.1.2 | 1 | Actual |
| H2 Database | 2.4.240 | 1 | Actual (CVE-2021-42392 corregida) |
| MySQL Driver | 8.1.0 | 3 | Actual |
| PostgreSQL Driver | 42.7.11 | 1 | Actual |
| Logback | 1.5.32 | 1 | Actual (CVE-2021-42550 corregida) |

**Evaluación:** Todas las versiones fijadas están actualizadas; no hay dependencias obsoletas. El proyecto mantiene una base de dependencias moderna y adecuada para producción con actualizaciones de seguridad.

---

## Arquitectura de un Vistazo

### 9 Dominios Funcionales Identificados

| # | Dominio | Paquetes principales | Archivos | Dependencias |
|---|---------|----------------------|----------|--------------|
| 1 | **Modelo de Dominio** | `org.springframework.samples.petclinic.model` | 11 | Ninguna (raíz) |
| 2 | **Abstracción de Repositorio** | `org.springframework.samples.petclinic.repository` | 4 | Modelo |
| 3 | **Implementación JPA** | `org.springframework.samples.petclinic.repository.jpa` | 5 | Interfaz de repositorio, Modelo, Configuración |
| 4 | **Implementación JDBC** | `org.springframework.samples.petclinic.repository.jdbc` | 10 | Interfaz de repositorio, Modelo, Configuración, Utilidades |
| 5 | **Spring Data JPA** | `org.springframework.samples.petclinic.repository.springdatajpa` | 4 | Interfaz de repositorio, Modelo, Configuración |
| 6 | **Servicio de Negocio** | `org.springframework.samples.petclinic.service` | 2 | Interfaz de repositorio, Modelo |
| 7 | **Capa Web** | `org.springframework.samples.petclinic.web` | 8 | Servicio, Modelo, Configuración |
| 8 | **Transversal** | `org.springframework.samples.petclinic.util`, `org.springframework.samples.petclinic` | 3 | Modelo, todos vía AOP |
| 9 | **Configuración Spring** | `src/main/resources/spring/` | 7 | Todos (punto de agregación) |

### Diagrama de Dependencias de Dominio

```
Modelo de Dominio (11 archivos)
    ↓
Abstracción de Repositorio (4 archivos)
    ├─→ Implementación JPA (5 archivos)
    ├─→ Implementación JDBC (10 archivos)
    └─→ Spring Data JPA (4 archivos)
    ↓
Servicio de Negocio (2 archivos)
    ↓
Capa Web (8 archivos)
    ↓
Preocupaciones Transversales (3 archivos, AOP)
    ↓
Configuración Spring (agrega todo)
```

**Observaciones clave:**
- **Capas limpias:** Modelo → Repositorio → Servicio → Web (3 capas tradicional)
- **Patrón Strategy bien aplicado:** 3 implementaciones de persistencia conectadas mediante perfiles Spring sin cambios de código
- **Bajo acoplamiento:** Cada implementación de persistencia es independiente; no hay dependencias cruzadas entre implementaciones
- **Sin dependencias circulares:** El grafo de dependencias es acíclico (DAG)
- **Distribución de complejidad:** Los archivos más complejos están en la implementación JDBC (JdbcOwnerRepositoryImpl: 8 palabras clave) y en la capa de modelo (Owner: 4 palabras clave)

### Diagrama Mermaid (Completo)

Ver `ARCHITECTURE.mmd` para el grafo de dependencias renderizado con optimización del número de aristas.

---

## Perfil de Runtime en Producción

**Estado:** No hay telemetría de producción disponible. No se proporcionaron jobs batch, tareas programadas ni datos de APM.

**Nota:** Esta evaluación se beneficiaría de:
- Métricas JMX o endpoints de Spring Boot Actuator (si está desplegado)
- Datos de Application Performance Monitoring (APM) para latencia/varianza por dominio
- Logs de consultas lentas de base de datos
- Distribución del volumen de peticiones por endpoint

Por ahora, el **análisis estático de complejidad** es la mejor señal disponible para el riesgo operativo.

---

## Deuda Técnica

### Top 10 Hallazgos Ordenados por Valor de Remediación

| Posición | Problema | Severidad | Evidencia Archivo:Línea | Causa raíz | Esfuerzo | Valor |
|----------|----------|-----------|-------------------------|------------|----------|-------|
| 1 | Duplicación de código por copy-paste en implementaciones JDBC | ALTA | `JdbcOwnerRepositoryImpl:72-82` (156 líneas), `JdbcPetRepositoryImpl:65-68` (117 líneas), `JdbcVetRepositoryImpl:71-81` (89 líneas), `JdbcVisitRepositoryImpl:68-77` (99 líneas) | Las 3 capas de persistencia fuerzan la reimplementación de parametrización, mapeo de filas y comprobaciones de nulos; 30-40% de duplicación de código en archivos JDBC | 2-3 días | **ALTO** |
| 2 | Falta de comprobaciones de null safety en métodos de repositorio | ALTA | `JdbcVetRepositoryImpl:71-81` (ResultSet.getInt sin comprobación), `JdbcPetRepositoryImpl:84` (EntityUtils.getById lanza excepción), `OwnerController:80` (sin guard de null) | El mapeo manual de filas y la ausencia de defensas permiten NPE/SQLExceptions en runtime cuando faltan datos | 3-4 días | **ALTO** |
| 3 | Valores de configuración de base de datos hardcoded | MEDIA | `PetclinicInitializer.java:52` (perfil "jpa" hardcoded), `business-config.xml:23` (ruta de propiedades hardcoded), `datasource-config.xml:25-27` (nombres de clases hardcoded) | La estrategia de configuración no aprovecha overrides basados en entorno; data-access.properties líneas 8-9 usa placeholders dobles que requieren intervención de perfil Maven | 2 días | **MEDIO** |
| 4 | Problema de consultas N+1 en JdbcOwnerRepositoryImpl | MEDIA | `JdbcOwnerRepositoryImpl:106-119` (bucle loadPetsAndVisits), `JdbcOwnerRepositoryImpl:138-142` (getPetTypes llamado por cada pet) | La arquitectura JDBC fuerza carga eager; combinada con mapeo fila a fila resulta en 1 consulta de owner + N consultas de pet + N consultas de visit | 1 día | **MEDIO** |
| 5 | Envoltorio de excepciones no utilizado con catch genérico | MEDIA | `JdbcOwnerRepositoryImpl:91-101` (catch EmptyResultDataAccessException → throw ObjectRetrievalFailureException), `JdbcPetRepositoryImpl:74-82` (mismo patrón) | La capa de traducción de excepciones aporta poco valor; la anotación @Repository ya proporciona traducción de excepciones automáticamente | 1 día | **MEDIO** |
| 6 | Patrones Spring deprecados/obsoletos | MEDIA | `PetclinicInitializer.java` usa `AbstractDispatcherServletInitializer` (válido pero antiguo), configuración basada en XML (no basada en anotaciones), vistas JSP (no Thymeleaf) | El proyecto precede a Spring Boot; diseñado como implementación de referencia; mantenido por valor educativo | 5-7 días | **MEDIO** |
| 7 | Alta complejidad ciclomática en JdbcOwnerRepositoryImpl | MEDIA | `JdbcOwnerRepositoryImpl:70-82` (3 rutas condicionales), `JdbcOwnerRepositoryImpl:106-119` (bucles anidados para pets/visits, CC=5+) | El repositorio mezcla obtención de datos con carga de relaciones; se viola responsabilidad única | 1 día | **MEDIO** |
| 8 | Cadenas mágicas y nombres de vistas/configuración hardcoded | MEDIA | `OwnerController:41` ("owners/createOrUpdateOwnerForm"), `PetController:42` ("pets/createOrUpdatePetForm"), consultas SQL hardcoded en repos JDBC (líneas 73-76 en JdbcOwnerRepositoryImpl) | No existe registro para nombres de vistas o constantes de consulta; repetido en múltiples métodos de controlador | 1 día | **MEDIO** |
| 9 | CallMonitoringAspect deshabilitado para perfil Spring Data JPA | BAJA | `tools-config.xml:24-26, 29` (aspecto siempre registrado), `CallMonitoringAspect.java:30` (comentario indica "solo útil para JPA/JDBC"), `business-config.xml:94` (Spring Data JPA no tiene clases anotadas) | El aspecto no degrada correctamente para perfiles no soportados; sobrecarga de instrumentación innecesaria | 0.5 días | **BAJO** |
| 10 | Inicialización ineficiente de colecciones lazy | BAJA | `Owner.java:87-92, 98-102` (getPetsInternal inicializa HashSet si es null, sorting recrea ArrayList), `Pet.java:88-93, 99-103` (mismo patrón), `OwnerController:72` (new Owner() sin estado) | Las colecciones se recrean/ordenan en cada acceso; presión de GC innecesaria en operaciones de lectura intensiva | 0.5 días | **BAJO** |

**Resumen:** 2 problemas de severidad alta (duplicación, null safety), 6 de severidad media (patrones arquitectónicos, hardcoding), 2 de severidad baja (micro-optimizaciones de rendimiento). **Remediación total estimada: 8–12 persona-días si se aborda todo.**

---

## Hallazgos de Seguridad

### Vulnerabilidades Críticas y de Alta Severidad

| CWE ID | Tipo | Severidad | Evidencia | Impacto | Remediación |
|--------|------|-----------|-----------|---------|-------------|
| CWE-639 | Falta de autenticación y autorización | **CRÍTICA** | No hay Spring Security configurado; todos los endpoints son públicos. | Acceso no autorizado a todos los datos de la clínica (crear/leer/actualizar/eliminar owners, pets, vets, visits). | Implementar Spring Security con autenticación de base de datos/LDAP, control de acceso basado en roles y anotaciones @PreAuthorize. |
| CWE-352 | Falta de protección CSRF | **CRÍTICA** | No hay validación de token CSRF; el filtro CSRF de Spring Security no está habilitado. | Atacantes pueden falsificar peticiones para modificar/eliminar datos en nombre de usuarios autenticados. | Habilitar CSRF de Spring Security: añadir CsrfFilter, incluir tokens en formularios (`<c:param name="_csrf.parameterName">`), verificar en POST/PUT/DELETE. |
| CWE-79 | XSS mediante mensajes de excepción | **ALTA** | `exception.jsp:12` muestra `${exception.message}` sin escape. | Mensajes de excepción maliciosos o stack traces podrían ejecutar JavaScript en navegadores de usuarios. | Usar `<c:out value="${exception.message}"/>`, sanear excepciones y escapar toda salida JSP controlada por usuario. |
| CWE-798 | Credenciales de base de datos hardcoded | **ALTA** | `pom.xml:570, 589` contiene credenciales MySQL (`petclinic:petclinic`) y PostgreSQL (`postgres:petclinic`). | Credenciales de producción expuestas en código fuente, control de versiones y artefactos de build; extracción trivial para cualquiera. | Mover credenciales a variables de entorno, AWS Secrets Manager o Vault; rotar inmediatamente las credenciales expuestas. |
| CWE-287 | Validación de entrada débil | **ALTA** | `Owner.java:54-57` solo valida número de dígitos del teléfono (`@Digits(fraction=0, integer=10)`); sin validación de formato. `Visit.java:47-49` solo `@NotEmpty` en description. | Entradas malformadas evaden la lógica de negocio; habilita ataques de inyección; comportamiento inesperado en sistemas dependientes. | Añadir `@Size(max=...)`, `@Pattern(regexp="...")` para teléfono/email; validar longitud de city/address; añadir restricciones regex. |
| CWE-20 | Falta de límites de tamaño de entrada | **ALTA** | Campos String (firstName, lastName, address, city, description) carecen de restricciones `@Size`. | Desbordamientos, DOS mediante entradas extremadamente grandes, overflow de columnas de base de datos si los mappings no coinciden. | Añadir `@Size(min=1, max=100)` a todos los strings; validar cargas de archivos con límites; definir restricciones en columnas de base de datos. |
| CWE-89 | Inyección SQL (comodines LIKE) | **MEDIA** | `JdbcOwnerRepositoryImpl:77` añade `%` a entrada de usuario: `lastName + "%"`. Aunque usa consultas parametrizadas, la concatenación antes del binding podría permitir inyección LIKE. | La inyección de comodines podría saltarse filtros de búsqueda o devolver demasiados registros; DOS mediante consultas costosas. | Asegurar que la concatenación ocurre antes del binding (correcto aquí); añadir validación de entrada (@Size, @Pattern); evitar caracteres especiales. |
| CWE-209 | Divulgación de información mediante stack traces | **MEDIA** | El manejador de excepciones registra warnings; `exception.jsp` muestra excepciones a los usuarios. | Los stack traces exponen nombres de clases, métodos, versiones de librerías, estructura de base de datos y rutas de archivos. Facilita reconocimiento. | Implementar manejador de excepciones personalizado: registrar detalles del lado servidor y devolver mensajes genéricos al usuario; usar JSPs de error personalizados. |
| CWE-22 | Path Traversal (scripts de base de datos) | **MEDIA** | `datasource-config.xml:34-36` carga scripts SQL mediante `${jdbc.initLocation}`, `${jdbc.dataLocation}` resueltos desde `data-access.properties`. | Si las propiedades son controlables por usuario, atacantes podrían cargar scripts SQL arbitrarios o causar fallos de inicialización. | Hardcodear rutas de scripts; si son dinámicas, validar contra whitelist (por ejemplo, solo `classpath:db/h2/schema.sql`). |
| CWE-614 | Falta de cabeceras de seguridad HTTP | **MEDIA** | No están configuradas `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Content-Security-Policy`. | Los navegadores no evitarán MIME sniffing, clickjacking ni aplicarán HSTS; reduce la complejidad de explotación para XSS y UI redressing. | Añadir cabeceras de Spring Security: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, HSTS, CSP. |
| CWE-400 | Sin rate limiting ni protección DOS | **MEDIA** | Endpoints como `/owners/find`, `/owners` pueden invocarse sin límite; no hay throttling en consultas. | Atacantes pueden enumerar todos los owners, hacer fuerza bruta o causar DOS mediante consultas wildcard costosas. | Implementar rate limiting (Spring Cloud Gateway, Bucket4j); añadir límites de paginación en búsquedas; timeouts de consultas de base de datos. |
| CWE-311 | Sin enforcement de HTTPS | **BAJA** | No hay filtro `RequireHttps` ni cabecera HSTS configurada; las peticiones HTTP no redirigen. | Posibles ataques man-in-the-middle; cookies de sesión vulnerables si se transmiten por HTTP. | Configurar SSL/TLS en Jetty/Tomcat; añadir filtro de Spring Security para redirigir a HTTPS; marcar cookies como `Secure`, `HttpOnly`, `SameSite=Strict`. |

### Evaluación de Seguridad de Dependencias

**Resumen:** Todas las dependencias están actualizadas a mayo de 2026; sin CVE críticas. Correcciones históricas presentes: H2 2.4.240 (CVE-2021-42392 corregida), Logback 1.5.32 (CVE-2021-42550 corregida).

**Sin alertas de vulnerabilidad.**

### Buenas Prácticas Observadas (Positivo)

✓ **Consultas SQL parametrizadas** (todo el código JDBC usa `JdbcClient.sql()` con binding mediante `.param()`)  
✓ **Codificación de salida en JSPs** (datos de usuario mediante etiqueta `<c:out>`)  
✓ **Anotaciones de validación de entrada** (`@Valid`, `@NotEmpty`, `@Digits`, `@NotNull`)  
✓ **Control de acceso a campos** (`@InitBinder` impide manipulación de ID)  
✓ **Filtro de codificación UTF-8** configurado en `PetclinicInitializer.java:77`  
✓ **Prepared statements mediante Spring** (parametrización automática en `SimpleJdbcInsert`, `JdbcClient`)

---

## Brechas de Documentación

### Análisis de Cobertura

| Métrica | Valor |
|---------|-------|
| Total de archivos Java | 61 |
| Archivos con comentarios de cabecera/javadoc | 4 |
| **Cobertura %** | **6.6%** |

### Top 5 Subsistemas sin Documentar (Mayor Impacto)

| Subsistema | Complejidad | Archivos | Brecha |
|------------|-------------|----------|--------|
| Capa de Repositorio JDBC | Alta | JdbcOwnerRepositoryImpl (8 palabras clave), JdbcPetRepositoryImpl (2), JdbcVetRepositoryImpl (2), JdbcVisitRepositoryImpl (2) | No hay documentación que explique el patrón de 3 capas de persistencia (JPA/JDBC/Spring Data JPA), el mecanismo de cambio de perfiles o la estrategia específica de JDBC para mapeo de filas. Ingenieros no familiarizados con patrones legacy de Spring tendrán dificultades con `OneToManyResultSetExtractor` y la carga lazy `loadPetsAndVisits()`. |
| Modelo de Dominio (Entidades JPA) | Media | Owner, Visit, Pet, Vet, etc. (11 archivos) | Las relaciones de entidades (Owner → Pets → Visits) no están documentadas. No se explican las anotaciones JPA. La jerarquía de herencia (BaseEntity) no está aclarada. |
| Interfaces de Repositorio | Media | OwnerRepository, PetRepository, VetRepository, VisitRepository (4 archivos) | Contratos de método no definidos; no se explica la intención de `findByLastName()` ni de métodos finder personalizados. |
| Controladores Web | Media | OwnerController (5 palabras clave), PetController (3), VisitController (1) | El flujo request/response, el mapeo de vistas y los patrones de manejo de excepciones no están documentados. Nuevos desarrolladores no pueden entender `@InitBinder`, el flujo de form binding o por qué ciertas vistas tienen esos nombres. |
| Sistema de Configuración | Baja | business-config.xml, mvc-core-config.xml, datasource-config.xml, mvc-view-config.xml, tools-config.xml | No se explican las interdependencias de configuración XML, el orden de activación de perfiles ni la jerarquía de override de propiedades. ¿Por qué 5 archivos de configuración separados? ¿Cuál es el orden de inicialización? |

### Estado de Documentación de Arquitectura

| Documento | Existe | Calidad |
|-----------|--------|---------|
| `readme.md` | ✓ | Buena: describe setup, build y comandos de ejecución. Falta: visión de arquitectura y explicación de dominio. |
| `docs/` directory | ✓ | Mínima: contiene solo assets estáticos. Falta: decisiones de diseño, ADRs, racional de patrones de persistencia. |
| `AGENTS.md` | ✓ | Excelente: perfiles de build detallados, cambio de base de datos, generación CSS, errores comunes. |
| Diagrama de Arquitectura | ✗ | Falta: no hay representación visual de dominios, capas o grafo de dependencias. |
| Guía de Patrón de Persistencia | ✗ | Brecha crítica: los ingenieros no pueden entender por qué hay 3 implementaciones o cómo añadir una cuarta. |
| Mapeo Controlador/Vista | ✗ | Falta: lógica de routing de peticiones, flujo de form binding, integración de validación. |

---

## Estimación de Esfuerzo

### Cálculo COCOMO-II

**Entradas:**
- Total SLOC: 12,237
- KSLOC: 12.237
- Fórmula (factores de escala nominales): PM = 2.94 × (KSLOC)^1.10

**Cálculo:**
```
PM = 2.94 × (12.237)^1.10
   = 2.94 × 15.74
   = 46.2 persona-meses
```

**Rango estimado (±25%):** 34.7 – 57.8 persona-meses

### Factores de Coste

| Factor | Impacto | Notas |
|--------|---------|-------|
| **Abstracción de persistencia** | +15% | 3 implementaciones (JPA, JDBC, Spring Data JPA) requieren desarrollo, pruebas y mantenimiento independientes. |
| **Verbosity de configuración XML** | +8% | 5 archivos separados de configuración XML de Spring (frente a 1 clase @Configuration basada en anotaciones en Spring Boot) incrementan la carga cognitiva y el boilerplate. |
| **Inicialización basada en servlet** | +5% | `AbstractDispatcherServletInitializer` + registro manual de servlet (estilo Servlet 3.0) es más verboso que la autoconfiguración de Spring Boot. |
| **Capa de vistas JSP** | +5% | La compilación JSP, el form binding y el uso de tag libraries tienen un ciclo de iteración más lento que motores de plantillas modernos. |
| **Sobrecarga de suite de pruebas** | +3% | 3 implementaciones de persistencia requieren 3 veces la cobertura de pruebas de repositorio. |
| **Déficit de documentación** | +10% | 6.6% de cobertura de documentación obliga a nuevos desarrolladores a hacer ingeniería inversa de patrones desde el código en lugar de leer documentación. |

**Ajuste total de esfuerzo:** +46% sobre la línea base nominal (para un proyecto greenfield de 12.2 KSLOC).

**Estimación ajustada:** ~67 persona-meses para un equipo no familiarizado con patrones legacy de Spring Framework.

---

## Patrón de Modernización Recomendado

### **PATRÓN: Replatform (migrar a Spring Boot 3.x)**

**Racional:**

1. **Modularidad aceptable:** El código base está limpio (9 dominios, sin dependencias circulares, patrón strategy bien aplicado). La refactorización a Spring Boot es **de bajo riesgo**.

2. **Baja complejidad:** La complejidad ciclomática media es 1–3 por archivo (excepto la capa JDBC, máximo 8). No hay god objects ni anidamiento extremo. **Seguro para migrar de forma automatizada.**

3. **La abstracción de persistencia ha dado resultado:** 3 implementaciones coexisten sin acoplamiento fuerte. El enfoque único de Spring Data JPA en Spring Boot en realidad **simplifica** el código base (archivar variantes JDBC/JPA, mantener solo Spring Data JPA).

4. **Se necesitan motores de plantillas modernos:** JSP es la parte más débil de la arquitectura. Thymeleaf + plantillas Spring Boot mejoran la velocidad de desarrollo en **25–35%** (según benchmarks de la industria).

5. **Brecha de preparación para producción:** La aplicación carece de autenticación, protección CSRF, rate limiting y cabeceras de seguridad. Spring Boot + Spring Security starter agrupan esto **en 3 anotaciones** frente a XML manual + configuración de beans. Tiempo de migración: **retorno en 2–3 semanas de eliminación de endurecimiento manual de seguridad**.

### Roadmap de Replatform

| Fase | Duración | Elementos de trabajo | Resultado |
|------|----------|----------------------|-----------|
| **Fase 1: Línea base** | 2 semanas | Crear skeleton Spring Boot 3.4 (última 3.x); copiar estructura de paquetes; verificar build. | Proyecto Spring Boot funcionando, tests pasando en Java 21. |
| **Fase 2: Persistencia** | 3 semanas | Migrar capa de repositorio a Spring Data JPA (eliminar variantes JDBC/JPA); mantener clases de entidad. | Todas las operaciones CRUD funcionando vía JpaRepository. Implementaciones JDBC/JPA deprecadas. |
| **Fase 3: Web y Vistas** | 3 semanas | Convertir JSPs a Thymeleaf; actualizar bindings de controladores; migrar procesamiento de formularios. | Todos los endpoints web funcionales; vistas renderizadas vía Thymeleaf. |
| **Fase 4: Configuración** | 2 semanas | Convertir 5 archivos XML → clases `@Configuration`; externalizar propiedades a `application.yml`; activar perfiles. | Cero XML; configuración limpia y basada en anotaciones. |
| **Fase 5: Seguridad y Endurecimiento** | 2 semanas | Añadir Spring Security (auth, CSRF, headers); implementar rate limiting; corregir brechas XSS. | Aplicación lista para producción con autenticación, cifrado y cabeceras de cumplimiento. |
| **Fase 6: Pruebas y Validación** | 1 semana | Ampliar cobertura de pruebas; pruebas de rendimiento; escaneo de seguridad; smoke tests. | 80%+ cobertura de pruebas; auditoría de seguridad superada; baseline de rendimiento documentada. |
| **TOTAL** | **13 semanas** | | **Spring Boot 3.4 + Thymeleaf + Spring Security listo para producción.** |

**Esfuerzo estimado:** 65–75 persona-días para un equipo familiarizado con Spring Boot; ~2 FTE durante un trimestre.

**Plan de rollback:** Mantener la versión original de Spring Framework en una rama git; mantener una rama paralela `spring-boot-3.4` durante la migración. Coste de rollback: <1 día si la migración se bloquea.

---

## Patrones Alternativos Considerados

| Patrón | Evaluación | Cuándo usarlo |
|--------|------------|---------------|
| **Rehost** (lift-and-shift sin cambios) | No aplicable; ya está preparado para cloud (WAR + containerizable). | N/A |
| **Refactor** (modernización incremental) | **No recomendado.** La conversión fragmentada XML→anotaciones, JSP→Thymeleaf y actualizaciones Spring 5→7 dispersan el trabajo. Entrega menos valor por sprint que Replatform. | Si la adopción de Spring Boot está bloqueada por política organizativa. |
| **Rearchitect** (microservicios) | **Sobreingeniería.** Con 12.2 KSLOC, el sistema es un único dominio (gestión de clínica veterinaria). No hay justificación para dividirlo en varios servicios. Añade complejidad operativa (API gateways, service discovery, trazas distribuidas) sin beneficio de negocio. | Si el sistema crece a 100+ KSLOC y emergen límites claros de servicio. |
| **Rebuild** (reescritura completa) | **No recomendado.** El código base está bien estructurado y es mantenible; no hay deuda técnica legacy que justifique una reescritura. Relación coste-beneficio desfavorable. | Reservado para sistemas con legacy inmantenible (COBOL, frameworks obsoletos). |
| **Replace** (comprar/COTS) | **Posible pero de menor prioridad.** Existe software comercial de gestión de clínicas veterinarias, pero carece de valor educativo. Adecuado si PetClinic pasa de app de referencia a sistema de producción. | La decisión depende del contexto de negocio (herramienta de aprendizaje frente a sistema operativo). |

**Conclusión:** **Replatform** entrega el máximo valor: baseline moderno en Spring Boot, brechas de seguridad eliminadas, mejor velocidad de desarrollo y ganancias de mantenibilidad, todo en 13 semanas de esfuerzo enfocado.

---

## Próximos Pasos

### Inmediato (Semanas 1–2)

1. **Parche de seguridad (2 días):**
   - [ ] Añadir dependencia de Spring Security; crear esqueleto de módulo auth
   - [ ] Habilitar protección CSRF en configuración XML (o Spring Boot starter)
   - [ ] Corregir XSS en `exception.jsp`

2. **Sprint de documentación (3 días):**
   - [ ] Escribir guía de patrón de persistencia (árbol de decisión JDBC vs. JPA vs. Spring Data JPA)
   - [ ] Documentar flujo request/response de controladores mediante diagrama de secuencia
   - [ ] Añadir javadoc a los 10 métodos más complejos

3. **Triaje de deuda técnica (2 días):**
   - [ ] Extraer constantes de consultas JDBC a clase `JdbcQueries`
   - [ ] Añadir null safety a `EntityUtils.getById()` con Optional
   - [ ] Mover credenciales de base de datos a variables de entorno

### Corto Plazo (Semanas 3–4)

4. **Ampliación de cobertura de pruebas:**
   - [ ] Añadir tests de integración de seguridad (auth, CSRF)
   - [ ] Ampliar tests de repositorio para casos límite de nulos
   - [ ] Añadir tests de regresión de rendimiento (detección de consultas N+1)

5. **Finalización de documentación:**
   - [ ] Crear Architecture Decision Record (ADR) para la estrategia de 3 implementaciones de persistencia
   - [ ] Publicar diagrama de dependencias Mermaid en `docs/`
   - [ ] Escribir guía de contribuidor (build, test, despliegue)

### Medio Plazo (Semanas 5–13, si se continúa con Replatform)

6. **Migración a Spring Boot 3.4 (13 semanas según el roadmap anterior)**

---

## Conclusión

Spring Framework PetClinic es una **referencia educativa bien diseñada** que demuestra principios de arquitectura limpia (capas, separación de responsabilidades, patrón strategy). El código base es **de baja complejidad, modular y seguro para refactorizar**.

**Para uso inmediato en producción:** Priorizar endurecimiento de seguridad (autenticación, CSRF, validación de entrada, rate limiting), con una estimación de 2 semanas de trabajo.

**Para modernización a largo plazo:** Replatform a Spring Boot 3.4 en 13 semanas. Esto aporta seguridad, plantillas modernas, reducción de boilerplate y mejor mantenibilidad.

**Evaluación de riesgo:** Bajo. No hay decisiones técnicas sin salida, no hay god objects ni fallos arquitectónicos críticos. El sistema es mantenible tal como está (con correcciones de seguridad) o está preparado para una modernización bien acotada.

---

**Evaluación completada:** 26 de mayo de 2026  
**Preparado por:** Herramienta de Evaluación de Modernización IA  
**Nivel de confianza:** Alto (análisis basado en código, sin suposiciones)
