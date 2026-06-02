# Evaluación de modernización — Spring Framework PetClinic

> **Generado:** 2026-05-29  
> **Cadena de herramientas:** `find` + `wc -l` (`scc`/`cloc` no instalados) · Complejidad por recuento de palabras clave  
> **Alcance:** árbol `src/` · `pom.xml` en la raíz del repositorio

---

## Resumen ejecutivo

Spring Framework PetClinic es una aplicación web monolítica Java 17 / Spring MVC 7 (~12.400 líneas totales en 124 ficheros fuente) que demuestra tres estrategias de persistencia intercambiables: JDBC directo, JPA/Hibernate y Spring Data JPA. La base de código tiene una estructura deliberadamente educativa, ya que incluye simultáneamente las tres pilas de persistencia con un selector de activación basado en perfiles; esto triplica la superficie de mantenimiento y es el principal riesgo técnico si se quiere adoptar un camino hacia producción. La postura de seguridad es críticamente débil: no hay autenticación, no hay protección CSRF y los mensajes de excepción sin filtrar se muestran a los usuarios finales. El patrón de modernización recomendado es **Refactorizar**, centrándose en consolidar todo en la pila de Spring Data JPA, añadir Spring Security y migrar hacia una base de Spring Boot + API REST, lo que puede lograrse aproximadamente en 4–6 persona-meses.

---

## Inventario del sistema

### LOC por lenguaje (`find` + `wc -l`, complejidad por palabras clave de decisión)

> *`scc` y `cloc` no estaban disponibles en este entorno; las métricas se calcularon mediante PowerShell `Get-ChildItem` + `Measure-Object`.*

| Lenguaje | Ficheros | Líneas | Notas |
|---------------|------:|-------:|-------------------------------|
| Java | 61 | 3.647 | Código principal + tests combinados |
| JSP | 9 | ~900 | Vistas en `WEB-INF/jsp` |
| Ficheros de etiquetas JSP | 10 | ~600 | `WEB-INF/tags` |
| SQL | 8 | ~400 | 4 dialectos × esquema + datos |
| XML (Spring) | 8 | ~800 | Configuración Spring + POM de Maven |
| SCSS/CSS | 5 | ~200 | Hojas de estilo de la UI |
| Properties | 5 | ~150 | i18n + configuración de datasource |
| **Total** | **124** | **~12.401** | Excluyendo assets binarios/fuentes |

**Top 5 de ficheros Java con mayor complejidad (palabras clave de decisión: `if`/`for`/`while`/`switch`/`catch`/`case`):**

| Fichero | Palabras clave | Líneas |
|------|--------:|------:|
| `repository/jdbc/OneToManyResultSetExtractor.java` | 14 | 144 |
| `model/Owner.java` | 11 | 130 |
| `repository/jdbc/JdbcOwnerRepositoryImpl.java` | 11 | 139 |
| `web/OwnerController.java` | 9 | 113 |
| `repository/OwnerRepository.java` | 8 | 54 |

### Huella tecnológica

| Área | Detalle |
|---------|--------|
| **Lenguaje** | Java 17 |
| **Framework** | Spring Framework 7.0.7 (Spring MVC, Spring JDBC, Spring ORM, Spring Data JPA) |
| **Build** | Maven 3.8.4+ · `pom.xml` en la raíz · empaquetado WAR |
| **Servidor de aplicaciones** | Servlet 6.1 / Jakarta EE 10 — desplegable en Tomcat 11 o Jetty 11 |
| **Capa de vistas** | JSP + JSTL 3.0 + ficheros de etiquetas personalizados |
| **Persistencia** | Hibernate 7.3.2 ORM · Spring Data JPA 2025.1.5 · JDBC mediante `JdbcClient` de Spring 6+ |
| **Soporte de BBDD** | H2 (por defecto/en memoria), HSQLDB, MySQL 8.1, PostgreSQL 42.7 |
| **Caché** | Caffeine 3.2.3 mediante `@Cacheable` en la lista de veterinarios |
| **Validación** | Hibernate Validator 9.1 (`@NotEmpty`, `@Digits`) |
| **Logging** | SLF4J 2.0.17 + Logback 1.5.32 |
| **Serialización** | Jackson 3.1.2 + JAXB 4.0 (JSON + XML para el endpoint `/vets`) |
| **AOP** | AspectJ 1.9.25 — `CallMonitoringAspect` para monitorización de llamadas vía JMX |
| **Contenedor** | Docker vía JIB 3.5.1 (imagen base `jetty:11.0-jdk17`) |
| **Test** | JUnit Jupiter 6.0.2 · Mockito 5.23 · AssertJ 3.27 · cobertura JaCoCo |
| **CI** | Workflows en `.github/` · integración con SonarCloud en `pom.xml` |
| **Puntos de integración** | HTTP (web MVC), sin colas de mensajes, sin llamadas a APIs externas, sin procesos batch |
| **Esquema de datos** | 7 tablas: `vets`, `specialties`, `vet_specialties`, `owners`, `pets`, `types`, `visits` |

---

## Arquitectura de un vistazo

Consulta `ARCHITECTURE.mmd` para ver el diagrama Mermaid completo de dependencias por dominio.

| Dominio | Ficheros clave | Depende de |
|--------|-----------|------------|
| **Bootstrap / inicialización** | `PetclinicInitializer.java` | Configuración XML de Spring |
| **Modelo de dominio** | `model/BaseEntity`, `Owner`, `Pet`, `Vet`, `Visit`, `Specialty` | Esquema de BBDD (DDL) |
| **Interfaces de repositorio** | `OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository` | Modelo de dominio |
| **Repositorio — JDBC** *(perfil: `jdbc`)* | `jdbc/JdbcOwnerRepositoryImpl` + 7 más | Interfaces de repositorio, JdbcClient, DataSource |
| **Repositorio — JPA** *(perfil: `jpa`)* | `jpa/JpaOwnerRepositoryImpl` + 3 más | Interfaces de repositorio, EntityManager |
| **Repositorio — Spring Data JPA** *(perfil: `spring-data-jpa`)* | `springdatajpa/SpringData*Repository` × 4 | Interfaces de repositorio, Spring Data |
| **Capa de servicio** | `ClinicService` (interfaz) + `ClinicServiceImpl` | Interfaces de repositorio |
| **Controladores web** | `OwnerController`, `PetController`, `VetController`, `VisitController`, `CrashController` | Capa de servicio |
| **Capa de vistas** | `WEB-INF/jsp/**/*.jsp` + `WEB-INF/tags/*.tag` | Atributos del modelo procedentes de los controladores |
| **Transversal** | `CallMonitoringAspect` (JMX), `EntityUtils` | Beans de repositorio `@Repository` |
| **Infraestructura / configuración** | `spring/*.xml`, `db/*/schema.sql`, `messages/*.properties` | DataSource, perfiles Spring de la JVM |

### Referencias colgantes

| Problema | Ubicación |
|-------|----------|
| `VisitController` devuelve la vista `"visitList"`, pero no existe `visitList.jsp` | `web/VisitController.java:88` |
| `tools-config.xml` referencia en un comentario un `META-INF/aop.xml` inexistente | `spring/tools-config.xml:21-23` |
| El pointcut de `CallMonitoringAspect` no tiene efecto bajo el perfil `spring-data-jpa` | `util/CallMonitoringAspect.java:31-32` |

---

## Perfil de ejecución en producción

**No hay telemetría disponible.** No se proporcionó ningún servidor MCP de APM/observabilidad, logs JCL ni exportación de runtime. La carencia es relevante porque:

- La aplicación tiene tres perfiles de persistencia (`jdbc`, `jpa`, `spring-data-jpa`) con patrones de consulta significativamente diferentes: N+1 en el repositorio JDBC de veterinarios y cargas eager del grafo completo en el repositorio JPA de propietarios.
- Sin datos de latencia p99, se desconoce qué perfil se ejecuta en producción y si el patrón N+1 o la carga completa del grafo de propietarios están causando variabilidad real de latencia.

**Recomendación:** instrumentar con Micrometer + Prometheus —algo que se puede añadir de forma sencilla a Spring MVC 7 mediante `spring-context-support`— antes de cualquier sprint de modernización para establecer una línea base de latencia.

---

## Deuda técnica (Top 10)

Ordenada por valor de remediación (impacto × facilidad).

| # | Hallazgo | Categoría | Fichero:Línea | Severidad |
|---|---------|----------|-----------|----------|
| 1 | `Query` sin tipar + `@SuppressWarnings("unchecked")` en todas las implementaciones JPA | API deprecada | `jpa/*RepositoryImpl.java` | Crítica |
| 2 | `ClinicServiceImpl` es una fachada todopoderosa de puro passthrough (8 métodos de una línea) | God object | `service/ClinicServiceImpl.java:40-111` | Alta |
| 3 | Consultas N+1 en el repositorio JDBC de veterinarios: 1 `SELECT` por veterinario dentro de un bucle | Rendimiento | `jdbc/JdbcVetRepositoryImpl.java:70-86` | Alta |
| 4 | Bean muerto `namedParameterJdbcTemplate` declarado en XML, nunca inyectado | Código muerto | `spring/business-config.xml:76-79` | Alta |
| 5 | Tres pilas de repositorio paralelas compiladas dentro de un único WAR | Duplicación | `repository/jdbc/`, `jpa/`, `springdatajpa/` | Alta |
| 6 | `JdbcPetRepositoryImpl.findById` carga el grafo completo propietario + visitas para encontrar una sola mascota | Rendimiento | `jdbc/JdbcPetRepositoryImpl.java:71-85` | Media-alta |
| 7 | `OwnerController.showOwner` pasa `null`/excepción a la vista cuando el ID no es válido; no hay `@ControllerAdvice` | Gestión de errores ausente | `web/OwnerController.java:125-130` | Media |
| 8 | `jpa.showSql=true` incondicional en todos los entornos | Configuración hardcoded | `resources/spring/data-access.properties:11` | Media |
| 9 | `groupId` de conector MySQL deprecado: `mysql:mysql-connector-java` | API deprecada | `pom.xml:575` | Media |
| 10 | Tres endpoints `/vets` redundantes (`/vets`, `/vets.json`, `/vets.xml`) + clase wrapper `Vets` | Código redundante | `web/VetController.java:51-63` | Baja-media |

---

## Hallazgos de seguridad

| CWE | Título | Severidad | Fichero:Línea |
|-----|-------|----------|-----------|
| CWE-352 | Sin protección CSRF: no hay Spring Security en ningún sitio | **Crítica** | `PetclinicInitializer.java:75-79` |
| CWE-862 | Sin autenticación ni autorización en ninguna ruta | **Crítica** | Todos los controladores |
| CWE-209 | Mensaje de excepción sin filtrar mostrado en `exception.jsp` | Alta | `exception.jsp:12` |
| CWE-285 | IDOR: no hay comprobación de propiedad en ediciones de mascotas/visitas | Alta | `PetController.java:93-94`, `VisitController.java:61-62` |
| CWE-116 | Endpoint de crash `/oups` expuesto en producción | Media | `CrashController.java:32-36` |
| CWE-200 | Contraseñas de BBDD hardcodeadas en los perfiles MySQL + PostgreSQL del `pom.xml` | Media | `pom.xml:569-570`, `pom.xml:588-589` |
| CWE-20 | Sin `@Size(max)` en campos String del modelo: una entrada sobredimensionada puede provocar fuga de errores de esquema | Media | `Person.java:32,36`, `Owner.java:47-57` |
| CWE-200 | El nivel DEBUG emite PII (nombres, direcciones, teléfonos de propietarios) al flujo de logs | Media | `logback.xml:17` |
| CWE-89 | Objeto `Query` sin tipar: superficie futura de inyección JPQL | Media | `JpaOwnerRepositoryImpl.java:56` |
| CWE-693 | Sin cabeceras de seguridad (CSP, X-Frame-Options, HSTS) | Media | `mvc-core-config.xml` (ausente) |
| CWE-1035 | Font Awesome 4.7.0 (2016, EOL) servido como recurso estático | Media | `pom.xml:36` |
| CWE-601 | Redirección construida mediante concatenación de strings, no con variable de plantilla | Baja | `OwnerController.java:67` |
| CWE-20 | El validador de fecha de nacimiento de mascotas acepta fechas futuras | Baja | `PetValidator.java:53-55` |

**Bloqueantes inmediatos antes de cualquier despliegue en producción:** SEC-001 (CSRF), SEC-002 (autenticación), SEC-003 (divulgación de mensajes de excepción).

---

## Lagunas de documentación (Top 5)

Cobertura documental: **el 97% de los ficheros Java** tienen al menos un bloque Javadoc/comentario (59/61). Sin embargo, las siguientes lagunas de comportamiento bloquearían a un nuevo ingeniero:

1. **La activación de perfiles no está documentada en el README.** Los tres perfiles de persistencia (`jdbc`, `jpa`, `spring-data-jpa`) y sus trade-offs no se explican en ningún lugar accesible. `PetclinicInitializer.java:52` usa silenciosamente `"jpa"` como valor por defecto sin mencionarlo en el README.

2. **La utilidad genérica `OneToManyResultSetExtractor` no tiene ejemplos de uso.** `repository/jdbc/OneToManyResultSetExtractor.java` es el fichero más complejo de la base de código (14 palabras clave de decisión, 144 líneas) y no incluye Javadoc que explique los parámetros genéricos ni la estructura esperada del `JOIN` SQL.

3. **La estrategia de inicialización de datos no está documentada.** No está claro cuándo se ejecuta `db/*/schema.sql` frente a `data.sql`, ni qué perfil controla cada dialecto de base de datos. El valor por defecto de `data-access.properties` es HSQLDB, pero el `README` de desarrollo no lo indica.

4. **La intención de `CrashController` no está documentada en la base de código.** `web/CrashController.java` existe únicamente para disparar la página de error, pero no tiene Javadoc a nivel de clase ni mención en el README que explique que es un artefacto de demo que debería eliminarse en producción.

5. **La integración JMX de `CallMonitoringAspect` no está documentada.** El aspect expone métricas de recuento/tiempo de llamadas vía JMX (`@ManagedResource`), pero no hay una sección en el README, ni guía de conexión con `jconsole`/`jmxterm`, ni explicación de qué métricas se emiten o qué umbrales importan; por tanto, la capacidad de monitorización es prácticamente invisible para operadores.

---

## Estimación de esfuerzo

**Herramienta:** `find` + `wc -l` (COCOMO-II Basic, factores de escala nominales)  
**Fórmula:** `PM = 2.94 × (KSLOC)^1.10`

| Entrada | Valor |
|-------|-------|
| SLOC total (estimación de líneas no vacías y sin comentarios: ~70% del bruto) | ~8.700 |
| KSLOC | **8,7** |
| PM COCOMO-II (nominal) | `2.94 × 8.7^1.10 = 2.94 × 10.27` ≈ **30 persona-meses** |

> **Rango:** 20–45 PM (±40%) dependiendo de la familiaridad del equipo con Spring Boot y de si las pilas JDBC/JPA se retiran durante la migración.

**Principales drivers de coste:**

- **Tres pilas de persistencia**: cada una debe analizarse, migrarse o retirarse; la pila JDBC por sí sola añade ~2 PM debido a la complejidad del SQL directo.
- **Sin línea base de Spring Security**: añadir auth/CSRF/OIDC desde cero añade ~3 PM.
- **Migración de JSP a Thymeleaf o React**: si se moderniza la capa de vistas, añadir 4–6 PM para la conversión de plantillas y la validación UX.
- **Línea base de cobertura de tests desconocida**: JaCoCo está cableado, pero no hay informe de cobertura en el repositorio; si la cobertura es baja, escribir tests de caracterización antes de refactorizar añade 2–4 PM.

---

## Patrón de modernización recomendado

**Refactorizar** (enfoque *strangler fig* durante 2–3 sprints)

La base de código es pequeña —menos de 10 KSLOC—, ya está en Spring Framework 7 / Java 17 y está estructurada con una separación clara por capas. No se justifica un **Rebuild** ni un **Rearchitect** completos: el modelo de dominio es sólido y las interfaces de persistencia ya están limpias como abstracción. El enfoque recomendado es:

1. **Sprint 1 (4–6 semanas, 2 ingenieros):** añadir la autoconfiguración de Spring Boot como chasis de la aplicación —eliminar configuración XML y migrar a `application.yml`—, retirar las pilas de persistencia `jdbc` y `jpa` —mantener solo `spring-data-jpa`—, añadir Spring Security con login por formulario y protección CSRF, y corregir los dos hallazgos de seguridad críticos.

2. **Sprint 2 (4–6 semanas, 2 ingenieros):** migrar la capa de vistas de JSP a Thymeleaf —lo que permite una Content Security Policy sin `unsafe-inline`—, añadir gestión global de errores con `@ControllerAdvice`, añadir restricciones `@Size`, promover `@Cacheable` a una configuración de caché adecuada e instrumentar con Micrometer.

3. **Sprint 3 (2–4 semanas, 1 ingeniero):** retirar código muerto (`CrashController`, wrapper `Vets`, bean muerto `namedParameterJdbcTemplate`), actualizar Font Awesome, corregir el artifact ID de MySQL deprecado, endurecer el logging (INFO en producción) y escribir tests de integración con `@SpringBootTest`.

Esto mantiene el sistema modernizado dentro del ecosistema Spring conocido, evita el riesgo de un cambio big-bang y permite entregar un despliegue seguro para producción tras el Sprint 1.
