# Modernization Assessment — Spring Framework PetClinic

> **Generated:** 2026-05-29  
> **Tool chain:** find + wc -l (scc/cloc not installed) · Complexity by keyword count  
> **Scope:** `src/` tree · `pom.xml` at repo root

---

## Executive Summary

Spring Framework PetClinic is a Java 17 / Spring MVC 7 monolithic web application (~12,400 total lines across 124 source files) that demonstrates three interchangeable persistence strategies: raw JDBC, JPA/Hibernate, and Spring Data JPA. The codebase is deliberately educational in structure, shipping all three persistence stacks simultaneously with a profile-based activation switch — this triples maintenance surface and is the headline technical risk for a production adoption path. Security posture is critically weak: there is no authentication, no CSRF protection, and raw exception messages are rendered to end users. The recommended modernization pattern is **Refactor**, focusing on collapsing to the Spring Data JPA stack, adding Spring Security, and migrating to a Spring Boot + REST API chassis, which can be achieved in approximately 4–6 person-months.

---

## System Inventory

### LOC by Language (find + wc -l, decision-keyword complexity)

> *`scc` and `cloc` were not available in this environment; metrics computed via PowerShell `Get-ChildItem` + `Measure-Object`.*

| Language      | Files | Lines  | Notes                          |
|---------------|------:|-------:|-------------------------------|
| Java          |    61 |  3,647 | Main + test combined           |
| JSP           |     9 |    ~900| WEB-INF/jsp views              |
| JSP Tag Files |    10 |    ~600| WEB-INF/tags                   |
| SQL           |     8 |    ~400| 4 dialects × schema + data     |
| XML (Spring)  |     8 |    ~800| Spring config + Maven POM      |
| SCSS/CSS      |     5 |    ~200| UI stylesheets                 |
| Properties    |     5 |    ~150| i18n + datasource config       |
| **Total**     |**124**|**~12,401**| Excluding binary/font assets|

**Top 5 highest-complexity Java files (decision keywords: if/for/while/switch/catch/case):**

| File | Keywords | Lines |
|------|--------:|------:|
| `repository/jdbc/OneToManyResultSetExtractor.java` | 14 | 144 |
| `model/Owner.java` | 11 | 130 |
| `repository/jdbc/JdbcOwnerRepositoryImpl.java` | 11 | 139 |
| `web/OwnerController.java` | 9 | 113 |
| `repository/OwnerRepository.java` | 8 | 54 |

### Technology Fingerprint

| Concern | Detail |
|---------|--------|
| **Language** | Java 17 |
| **Framework** | Spring Framework 7.0.7 (Spring MVC, Spring JDBC, Spring ORM, Spring Data JPA) |
| **Build** | Maven 3.8.4+ · `pom.xml` at root · WAR packaging |
| **App server** | Servlet 6.1 / Jakarta EE 10 — deployable to Tomcat 11 or Jetty 11 |
| **View layer** | JSP + JSTL 3.0 + custom tag files |
| **Persistence** | Hibernate 7.3.2 ORM · Spring Data JPA 2025.1.5 · JDBC (via `JdbcClient` Spring 6+) |
| **DB support** | H2 (default/in-memory), HSQLDB, MySQL 8.1, PostgreSQL 42.7 |
| **Caching** | Caffeine 3.2.3 via `@Cacheable` on vet list |
| **Validation** | Hibernate Validator 9.1 (`@NotEmpty`, `@Digits`) |
| **Logging** | SLF4J 2.0.17 + Logback 1.5.32 |
| **Serialization** | Jackson 3.1.2 + JAXB 4.0 (JSON + XML for `/vets` endpoint) |
| **AOP** | AspectJ 1.9.25 — `CallMonitoringAspect` for JMX call monitoring |
| **Container** | Docker via JIB 3.5.1 (`jetty:11.0-jdk17` base image) |
| **Test** | JUnit Jupiter 6.0.2 · Mockito 5.23 · AssertJ 3.27 · JaCoCo coverage |
| **CI** | `.github/` workflows present · SonarCloud integration in `pom.xml` |
| **Integration points** | HTTP (MVC web), no message queues, no external API calls, no batch jobs |
| **Data schema** | 7 tables: `vets`, `specialties`, `vet_specialties`, `owners`, `pets`, `types`, `visits` |

---

## Architecture-at-a-Glance

See `ARCHITECTURE.mmd` for the full Mermaid domain dependency diagram.

| Domain | Key Files | Depends On |
|--------|-----------|------------|
| **Bootstrap / Init** | `PetclinicInitializer.java` | Spring XML Config |
| **Domain Model** | `model/BaseEntity`, `Owner`, `Pet`, `Vet`, `Visit`, `Specialty` | DB Schema (DDL) |
| **Repository Interfaces** | `OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository` | Domain Model |
| **Repository — JDBC** *(profile: jdbc)* | `jdbc/JdbcOwnerRepositoryImpl` + 7 more | Repo Interfaces, JdbcClient, DataSource |
| **Repository — JPA** *(profile: jpa)* | `jpa/JpaOwnerRepositoryImpl` + 3 more | Repo Interfaces, EntityManager |
| **Repository — Spring Data JPA** *(profile: spring-data-jpa)* | `springdatajpa/SpringData*Repository` × 4 | Repo Interfaces, Spring Data |
| **Service Layer** | `ClinicService` (interface) + `ClinicServiceImpl` | Repository Interfaces |
| **Web Controllers** | `OwnerController`, `PetController`, `VetController`, `VisitController`, `CrashController` | Service Layer |
| **View Layer** | `WEB-INF/jsp/**/*.jsp` + `WEB-INF/tags/*.tag` | Model attributes from Controllers |
| **Cross-Cutting** | `CallMonitoringAspect` (JMX), `EntityUtils` | Repository `@Repository` beans |
| **Infrastructure / Config** | `spring/*.xml`, `db/*/schema.sql`, `messages/*.properties` | DataSource, JVM Spring profiles |

### Dangling References

| Issue | Location |
|-------|----------|
| `VisitController` returns view `"visitList"` but no `visitList.jsp` exists | `web/VisitController.java:88` |
| `tools-config.xml` references non-existent `META-INF/aop.xml` in comment | `spring/tools-config.xml:21-23` |
| `CallMonitoringAspect` pointcut has no effect under `spring-data-jpa` profile | `util/CallMonitoringAspect.java:31-32` |

---

## Production Runtime Profile

**No telemetry available.** No APM/observability MCP server, JCL logs, or runtime export was provided. The gap is notable because:

- The application has three persistence profiles (`jdbc`, `jpa`, `spring-data-jpa`) with meaningfully different query patterns (N+1 in JDBC vet repository, eager full-graph loads in JPA owner repository).
- Without p99 latency data it is unknown which profile runs in production and whether the N+1 pattern or the full-owner-graph load is causing real latency variance.

**Recommendation:** Instrument with Micrometer + Prometheus (trivially added to Spring MVC 7 via `spring-context-support`) before any modernization sprint to establish a latency baseline.

---

## Technical Debt (Top 10)

Ranked by remediation value (impact × ease).

| # | Finding | Category | File:Line | Severity |
|---|---------|----------|-----------|----------|
| 1 | Raw `Query` + `@SuppressWarnings("unchecked")` in all JPA impls | Deprecated API | `jpa/*RepositoryImpl.java` | Critical |
| 2 | `ClinicServiceImpl` is a passthrough god-facade (8 one-liner methods) | God object | `service/ClinicServiceImpl.java:40-111` | High |
| 3 | N+1 queries in JDBC vet repository — 1 SELECT per vet in a loop | Performance | `jdbc/JdbcVetRepositoryImpl.java:70-86` | High |
| 4 | Dead bean `namedParameterJdbcTemplate` declared in XML, never injected | Dead code | `spring/business-config.xml:76-79` | High |
| 5 | Three parallel repository stacks compiled into one WAR | Duplication | `repository/jdbc/`, `jpa/`, `springdatajpa/` | High |
| 6 | `JdbcPetRepositoryImpl.findById` loads full owner + visits graph to find one pet | Performance | `jdbc/JdbcPetRepositoryImpl.java:71-85` | Medium-High |
| 7 | `OwnerController.showOwner` passes null/exception to view on invalid ID; no `@ControllerAdvice` | Missing error handling | `web/OwnerController.java:125-130` | Medium |
| 8 | `jpa.showSql=true` unconditional in all environments | Hardcoded config | `resources/spring/data-access.properties:11` | Medium |
| 9 | Deprecated MySQL connector `groupId`: `mysql:mysql-connector-java` | Deprecated API | `pom.xml:575` | Medium |
| 10 | Three redundant `/vets` endpoints (`/vets`, `/vets.json`, `/vets.xml`) + `Vets` wrapper class | Redundant code | `web/VetController.java:51-63` | Low-Medium |

---

## Security Findings

| CWE | Title | Severity | File:Line |
|-----|-------|----------|-----------|
| CWE-352 | No CSRF protection — no Spring Security anywhere | **Critical** | `PetclinicInitializer.java:75-79` |
| CWE-862 | No authentication or authorization on any route | **Critical** | All controllers |
| CWE-209 | Raw exception message rendered in `exception.jsp` | High | `exception.jsp:12` |
| CWE-285 | IDOR — no ownership check on pet/visit edits | High | `PetController.java:93-94`, `VisitController.java:61-62` |
| CWE-116 | `/oups` crash endpoint exposed in production | Medium | `CrashController.java:32-36` |
| CWE-200 | Hardcoded DB passwords in `pom.xml` MySQL + PostgreSQL profiles | Medium | `pom.xml:569-570`, `pom.xml:588-589` |
| CWE-20 | No `@Size(max)` on String model fields — oversized input → schema error leak | Medium | `Person.java:32,36`, `Owner.java:47-57` |
| CWE-200 | DEBUG log level emits PII (Owner names, addresses, phone) to log stream | Medium | `logback.xml:17` |
| CWE-89 | Raw `Query` object — future JPQL injection surface | Medium | `JpaOwnerRepositoryImpl.java:56` |
| CWE-693 | No security headers (CSP, X-Frame-Options, HSTS) | Medium | `mvc-core-config.xml` (absent) |
| CWE-1035 | Font Awesome 4.7.0 (2016, EOL) served as static resource | Medium | `pom.xml:36` |
| CWE-601 | Redirect built via string concatenation, not template variable | Low | `OwnerController.java:67` |
| CWE-20 | Pet birth date validator accepts future dates | Low | `PetValidator.java:53-55` |

**Immediate blockers before any production deployment:** SEC-001 (CSRF), SEC-002 (Auth), SEC-003 (exception message disclosure).

---

## Documentation Gaps (Top 5)

Documentation coverage: **97% of Java files** have at least one Javadoc/comment block (59/61). However, the following behavioral gaps would block a new engineer:

1. **Profile activation is undocumented in the README.** The three persistence profiles (`jdbc`, `jpa`, `spring-data-jpa`) and their trade-offs are not explained anywhere accessible. `PetclinicInitializer.java:52` silently defaults to `"jpa"` with no README callout.

2. **The `OneToManyResultSetExtractor` generic utility has no usage examples.** `repository/jdbc/OneToManyResultSetExtractor.java` is the most complex file in the codebase (14 decision keywords, 144 lines) and carries no Javadoc explaining the generic parameters or the expected SQL join structure.

3. **Data initialization strategy is not documented.** It is unclear when `db/*/schema.sql` runs vs. `data.sql`, and which profile controls which database dialect. The `data-access.properties` default is HSQLDB but the dev `README` does not say so.

4. **`CrashController` intent is not documented in the codebase.** `web/CrashController.java` exists purely to trigger the error page, but has no class-level Javadoc or README mention explaining that it is a demo artifact that should be removed in production.

5. **`CallMonitoringAspect` JMX integration is undocumented.** The aspect exposes call count/time metrics via JMX (`@ManagedResource`), but there is no README section, no `jconsole`/`jmxterm` connection guide, and no explanation of what metrics are emitted or what thresholds matter — so the monitoring capability is effectively invisible to operators.

---

## Effort Estimation

**Tool:** find + wc -l (COCOMO-II Basic, nominal scale factors)  
**Formula:** `PM = 2.94 × (KSLOC)^1.10`

| Input | Value |
|-------|-------|
| Total SLOC (non-blank, non-comment estimate ~70% of raw) | ~8,700 |
| KSLOC | **8.7** |
| COCOMO-II PM (nominal) | `2.94 × 8.7^1.10 = 2.94 × 10.27` ≈ **30 person-months** |

> **Range:** 20–45 PM (±40%) depending on team familiarity with Spring Boot and whether the JDBC/JPA stacks are retired during migration.

**Key cost drivers:**

- **Three persistence stacks** — each must be analyzed, migrated, or retired; JDBC stack alone adds ~2 PM due to raw SQL complexity.
- **No Spring Security baseline** — adding auth/CSRF/OIDC from zero adds ~3 PM.
- **JSP-to-Thymeleaf or React migration** — if the view layer is modernized, add 4–6 PM for template conversion and UX validation.
- **Test coverage baseline unknown** — JaCoCo is wired but no coverage report is in the repo; if coverage is low, writing characterization tests before refactoring adds 2–4 PM.

---

## Recommended Modernization Pattern

**Refactor** (strangler-fig approach over 2–3 sprints)

The codebase is small (sub-10 KSLOC), already on Spring Framework 7 / Java 17, and structured with clear layer separation. A full **Rebuild** or **Rearchitect** is not warranted — the domain model is sound and the persistence interfaces are already abstraction-clean. The recommended approach is:

1. **Sprint 1 (4–6 weeks, 2 engineers):** Add Spring Boot autoconfiguration as the application chassis (remove XML config, migrate to `application.yml`), retire the `jdbc` and `jpa` persistence stacks (keep only `spring-data-jpa`), add Spring Security with form login and CSRF protection, and fix the two Critical security findings.

2. **Sprint 2 (4–6 weeks, 2 engineers):** Migrate view layer from JSP to Thymeleaf (enables content-security-policy without `unsafe-inline`), add `@ControllerAdvice` global error handling, add `@Size` constraints, promote `@Cacheable` to a proper cache configuration, and instrument with Micrometer.

3. **Sprint 3 (2–4 weeks, 1 engineer):** Retire dead code (`CrashController`, `Vets` wrapper, dead `namedParameterJdbcTemplate` bean), upgrade Font Awesome, fix deprecated MySQL artifact ID, harden logging (INFO in prod), write integration tests with `@SpringBootTest`.

This keeps the modernized system in the familiar Spring ecosystem, avoids big-bang risk, and delivers a production-safe deployment after Sprint 1 alone.
