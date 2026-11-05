# Spring Framework Petclinic — Modernization Assessment

## Executive Summary

Spring Framework Petclinic is a Java 17, Maven-built WAR sample application for managing owners, pets, visits, and veterinarians through a classic Spring MVC/JSP three-layer design. SCC counted 135 files and 26,559 code lines across the checkout; the primary executable code is 2,291 Java lines in 61 Java files, with material web assets and documentation included in the aggregate. The principal modernization risks are an unauthenticated write-capable web surface, client-controlled pet update identity, embedded database credentials, and maintaining three selectable persistence implementations. Prefer **Refactor**: retain the bounded business domain and current Java/Spring baseline, while consolidating persistence and applying security, validation, configuration, and delivery improvements incrementally.

## System Inventory

### Quantitative inventory

**Method.** `scc .` and `scc --by-file -s complexity . | head -25` were run at the repository root. SCC’s aggregate includes source, JSP, SQL, stylesheets, SVGs, Markdown, XML, JSON, and build scripts; it should not be interpreted as Java-only application SLOC.

| Measure | Observation |
|---|---:|
| Files counted by SCC | 135 |
| Total lines | 31,625 |
| Code lines | 26,559 |
| Java | 61 files / 2,291 code lines / complexity 91 |
| Markdown | 18 files / 4,584 code lines |
| CSS + SVG | 3 files / 16,289 code lines |
| JSP | 9 files / 367 code lines |
| SQL | 8 files / 414 code lines |
| Production Java files | 47 |
| Test Java files | 14 |
| Highest SCC file complexity | `src/main/java/org/springframework/samples/petclinic/repository/jdbc/OneToManyResultSetExtractor.java` — 18 |
| Other high-complexity files | `web/OwnerController.java` — 9; `web/PetValidator.java`, `model/Owner.java`, `web/PetController.java`, and `repository/jdbc/JdbcOwnerRepositoryImpl.java` — 6 each |
| SCC organic estimates | $845,313 cost; 12.90-month schedule; 5.82 people (about 75 person-months when multiplied) |

### Technology fingerprint

| Area | Evidence |
|---|---|
| Language and packaging | Java 17 and Maven WAR (`pom.xml:10`, `pom.xml:17-21`). |
| Web/runtime | Servlet 6.1, Spring MVC 7.0.7, JSP/JSTL; runs with Maven Jetty or a servlet container, with Docker image instructions (`pom.xml:31`, `:43-45`, `readme.md:17-32`, `:114-120`). |
| Business/data frameworks | Spring transactions, JPA/Hibernate, JDBC, Spring Data JPA, Caffeine, AspectJ and Logback (`pom.xml:48-58`, `:167-203`; `business-config.xml:18-26`). |
| Presentation | Annotated controllers, JSP views/custom tags, static resources, internationalized messages (`mvc-core-config.xml:17-54`; `mvc-view-config.xml:25-28`). |
| Persistence/data stores | H2 default; HSQLDB, MySQL, and PostgreSQL profile configurations; vendor schema and seed SQL (`readme.md:41-45`; `src/main/resources/db/`; `datasource-config.xml:28-37`). |
| Persistence invocation | Interfaces are implemented by profile-selected handwritten JPA, JDBC, or Spring Data JPA repositories (`business-config.xml:29-96`). |
| Interfaces/integration | Browser HTTP routes, JSP/JSON/XML representations, JNDI datasource option, JMX call monitoring, and relational database only; no repository evidence of message brokers or outbound service clients. |
| Build/test/quality | Maven Wrapper; JUnit Jupiter, Mockito, AssertJ; Surefire and JaCoCo configuration; CI runs `verify` for Java 17/21 and Sonar on main (README badge is not an inline coverage figure) (`pom.xml:60-85`; `readme.md:3-5`). |

## Architecture-at-a-Glance

The application follows the documented presentation → service → repository structure (`readme.md:7-10`). `PetclinicInitializer` creates the root and DispatcherServlet contexts; requests enter MVC controllers, flow through the transactional `ClinicService`, and reach a repository implementation selected by active Spring profile. The relational schema supplies owners, pets, visits, vets, specialties, and types; JSPs render the server-side web UI.

| Domain/component | Main artifacts | Dependencies and observations |
|---|---|---|
| Servlet bootstrap | `PetclinicInitializer.java` | Registers root/MVC contexts and encoding filter; active profile selects persistence path. |
| Web/MVC | `web/*Controller.java`, `mvc-core-config.xml`, `mvc-view-config.xml` | Routes browser requests to service calls and logical JSP views. |
| Owner management | `model/Owner.java`, `web/OwnerController.java`, `WEB-INF/jsp/owners/` | Owner owns pets; supports search/create/edit/detail. |
| Pet/type management | `model/Pet.java`, `PetType.java`, `web/PetController.java`, `PetValidator.java`, `PetTypeFormatter.java` | Pet belongs to an owner and type; creates/edits pets. |
| Visits | `model/Visit.java`, `web/VisitController.java` | Visit belongs to a pet and is displayed from owner detail. |
| Veterinarians | `model/Vet.java`, `Specialty.java`, `web/VetController.java` | Many-to-many specialties; supports HTML, JSON, and XML representations. |
| Service/cross-cutting | `service/ClinicService*.java`, `tools-config.xml`, `CallMonitoringAspect.java` | Transactional façade delegates to repository ports; cache and JMX monitoring configured. |
| Persistence ports/implementations | `repository/*.java`, `repository/{jpa,jdbc,springdatajpa}/` | Exactly one implementation family is activated by `jpa`, `jdbc`, or `spring-data-jpa`; inactive families are not dead code merely from static reachability. |
| Data initialization | `datasource-config.xml`, `spring/data-access.properties`, `db/*/{schema,data}.sql` | Configures Tomcat JDBC pool then applies vendor schema and seed scripts. |
| Presentation assets | `WEB-INF/jsp/`, `WEB-INF/tags/`, `resources/`, `messages/` | JSP resolver and static mappings bind views/assets to controllers. |

See [`ARCHITECTURE.mmd`](ARCHITECTURE.mmd) for the component dependency diagram.

Static-review follow-ups: `namedParameterJdbcTemplate` in `business-config.xml:76-79` and the XML `vets/vetList.xml` view appear unused; confirm that no external configuration selects them before removal. `findVisitsByPetId` is test-supported but is not used by the inspected production visit route. The JPA context simultaneously sets `persistenceUnitName` and `packagesToScan` (`business-config.xml:48-50`); the comment says the persistence unit wins, and no `persistence.xml` was found, so deployed behavior warrants a smoke test.

## Production Runtime Profile

No production telemetry, APM data, request logs, batch logs, or operational export was provided or discovered. Consequently, no p50/p95/p99 timing, p99/p50 variance, or production execution-cost tagging is asserted. The repository does contain JMX call-monitoring configuration (`tools-config.xml`) and a `CallMonitoringAspect`, which are potential collection points rather than evidence of runtime performance.

## Technical Debt

| Rank | Finding | Evidence | Remediation value |
|---:|---|---|---|
| 1 | Container API-version compatibility requires verification | WAR compiles against Servlet 6.1, while Jib references Jetty 11 (`pom.xml:43`, `:471-490`). | Align target container/image with the Servlet API, then smoke-test the built image. The incompatibility is a hypothesis pending deployment validation. |
| 2 | Three persistence paths duplicate maintenance | JDBC, handwritten JPA, and Spring Data JPA are selectable (`business-config.xml:29-96`); owner query logic exists in multiple forms. | Confirm supported deployment profiles and retire the unneeded implementations. |
| 3 | Visit save contract differs by profile | Interface promises insert/update; JPA uses persist/merge while JDBC rejects update (`VisitRepository.java:34-40`; `JpaVisitRepositoryImpl.java:47-54`; `JdbcVisitRepositoryImpl.java:55-64`). | Define create-only versus upsert semantics and enforce a cross-profile contract test. |
| 4 | Owner search over-fetches visit data | JPA repository documents unnecessary visit loading and fetches pets; `Pet.visits` is eager (`JpaOwnerRepositoryImpl.java:45-58`; `Pet.java:60-61`). | Add search projections/DTOs and fetch only data used by list views. |
| 5 | JDBC vet retrieval is N+1 | A specialty-link query runs inside the vet loop (`JdbcVetRepositoryImpl.java:57-85`). | Use a bulk/join query and assemble results in memory. |
| 6 | Security is absent from application configuration | Write handlers exist but POM/MVC config show no Spring Security integration (`OwnerController.java:60-68`; `PetController.java:77-89`; `VisitController.java:75-82`). | Establish an application or verified platform security boundary; see Security Findings. |
| 7 | Deliberate crash route is exposed | `/oups` throws, menu links it, and exception JSP displays its message (`CrashController.java:32-36`; `menu.tag:30-34`; `exception.jsp:10-12`). | Remove or restrict it outside development and present a generic error response. |
| 8 | Vet cache has no declared expiry/invalidation | `findVets()` is cacheable and cache manager only names caches (`ClinicServiceImpl.java:98-103`; `tools-config.xml:37-47`). | Set TTL/size and eviction behavior, or remove cache; stale data is an operational hypothesis. |
| 9 | Unused-looking visit service operation | `findVisitsByPetId` is service/test-used, but inspected MVC visit display uses `Pet.getVisits()` (`ClinicService.java:48-50`; `VisitController.java:85-88`). | Verify non-MVC callers and remove or route through it consistently. |
| 10 | Source/build hygiene issues | CSS profile emits into source tree; some JUnit/Mockito dependencies lack test scope (`pom.xml:277-281`, `:294-298`, `:629-646`). | Emit generated assets under `target/`, scope test libraries correctly, and inspect resulting WAR contents. |

## Security Findings

| ID | CWE | Severity | Evidence | Finding and direction |
|---|---|---:|---|---|
| SEC-001 | CWE-306, CWE-862 | High | `PetclinicInitializer.java:75-79`; `pom.xml:112-338`; write/read controllers under `web/` | No Spring Security dependency, filter chain, or authorization evidence accompanies public owner/pet/visit routes. Require authentication, role/ownership authorization, and restrict personal data. External gateway controls remain unverified. |
| SEC-002 | CWE-915, CWE-639 | High | `PetController.java:64-67`, `:99-108`; `createOrUpdatePetForm.jsp:21`; `JdbcPetRepositoryImpl.java:88-114` | Pet update accepts a form-bound entity and does not compare `{petId}` with its ID or prove it belongs to `{ownerId}`. Use a constrained DTO, load by path ID, verify ownership/authorization, and copy allowed fields. |
| SEC-003 | CWE-798 | Medium | `pom.xml:563-570`, `:581-589`; `datasource-config.xml:28-30` | MySQL/PostgreSQL profile credentials are in source and feed the datasource. Move secrets to protected deployment configuration and rotate any non-local use. |
| SEC-004 | CWE-20 | Low | `Owner.java:46-57`; `NamedEntity.java:30-40`; `Visit.java:47-49`; `PetValidator.java:39-55`; `db/h2/schema.sql:36-62` | Domain inputs lack server-side size constraints matching SQL columns. Add Bean Validation and binder request limits. |
| SEC-005 | CWE-209 | Low | `CrashController.java:32-35`; `mvc-core-config.xml:60-66`; `exception.jsp:12` | Global exception view renders exception message. Use generic client errors, server-side correlated logging, and output encoding; current explicit message alone is not a proven sensitive disclosure. |

No confirmed SQL/JPQL injection was found in the reviewed repositories: examined JDBC and JPA paths use bound parameters. No repository evidence showed command execution, outbound HTTP clients, deserialization, or custom XML parsing. CSRF, transport headers, cookie settings, and proxy TLS configuration are not configured in this repository; their runtime absence is not asserted.

## Documentation Gaps

1. **Operational security model:** README documents local launch but not authentication, authorization, CSRF, TLS/proxy headers, or ownership boundaries for owner information and writes.
2. **Persistence-profile support policy:** Three profiles are documented, but no decision states which is supported in a deployed environment, how parity is maintained, or a retirement path.
3. **Deployment compatibility:** The runtime/container matrix does not reconcile Servlet 6.1, Jetty 11, Tomcat 11, and the Jib image configuration.
4. **Production operations:** No documented observability dashboard, log/metric collection, cache-freshness policy, backup/recovery process, or database migration approach was found.
5. **Data and error contracts:** Schema scripts exist but no concise data dictionary or HTTP/form error-handling contract explains field constraints, data ownership, or user-safe error semantics.

## Effort Estimation

SCC’s all-file organic output is **$845,313**, **12.90 months**, and **5.82 people** (approximately **75 person-months** by schedule × people). To make the COCOMO calculation independently reproducible, applying the requested nominal basic COCOMO-II-style formula to SCC’s aggregate code count gives:

```text
KSLOC = 26.559
PM = 2.94 × (KSLOC ^ 1.10)
PM = 2.94 × (26.559 ^ 1.10) = 108.39 person-months
Indicative ±25% range = 81.29–135.48 person-months
```

This is a sizing estimate, not a delivery commitment. It is deliberately shown separately from SCC’s own estimate because SCC’s input includes substantial Markdown, SVG, CSS, and other non-executable assets. Key cost drivers are selecting/consolidating persistence, security remediation and test additions, JSP/XML/WAR delivery compatibility, database deployment choices, and the lack of runtime performance evidence.

## Recommended Modernization Pattern

**Refactor.** The domain is compact, its architecture is already layered, Java 17 and Spring 7 are current baseline technologies, and the code has a working test suite spanning web and all three persistence profiles. A rebuild would discard useful behavior without evidence of a business need; instead, first establish authentication/authorization and safe binding, make database configuration secret-managed, choose and contract-test one persistence strategy, remove retired configuration, and gradually modernize delivery/configuration only after container compatibility and runtime requirements are measured.
