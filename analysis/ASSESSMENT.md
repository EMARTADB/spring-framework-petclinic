# Modernization Assessment — Spring Framework PetClinic

> Generated: 2026-05-29 | Branch: `modernization` | Tool chain: Claude Code legacy-analyst + security-auditor (Claude Sonnet 4.6)

---

## Executive Summary

Spring PetClinic is a well-known Spring Framework reference application implementing a veterinary clinic management system. It is a small codebase (~3 KSLOC across 47 Java source files) but its complexity is disproportionate to its size: it ships **three parallel data-access implementations** (JDBC, JPA, Spring Data JPA) for the same four entities, is wired entirely through XML Spring configuration despite targeting Spring Framework 7 and Java 17, and carries **zero authentication or security controls**. The dominant modernization risk is not size — it is the accumulation of legacy patterns (XML config, JSP views, WAR packaging, hand-rolled JDBC) that create friction for every engineering touchpoint. The headline recommendation is a **Rearchitect** pattern: migrate to Spring Boot 3.x, Spring Data JPA exclusively, Thymeleaf or React views, and introduce Spring Security — transforming a teaching artefact into a production-ready baseline.

---

## System Inventory

### LOC Summary (measured with `find` + `wc -l`, no scc/cloc installed)

| Language | Files | LOC (including blanks/comments) |
|---|---|---|
| Java (main) | 47 | 3,110 |
| Java (test) | 14 | 1,185 |
| XML (Spring config) | 6 | ~350 |
| JSP views | 9 | ~400 |
| JSP tag files | 10 | ~200 |
| SQL (DDL + DML × 4 DBs) | 8 | ~320 |
| SCSS | 4 | ~200 |
| Properties | 5 | ~60 |
| **Total (approx.)** | **~100** | **~5,952** |

**Effective production SLOC (Java main only): ~2,400** (subtracting blanks/comments, estimated 22% overhead).

### COCOMO-II Effort Estimation

Using COCOMO-II basic formula: `PM = 2.94 × (KSLOC)^1.10`

- KSLOC = 2.4 (Java main) + 0.35 (XML) + 0.4 (JSP) ≈ **3.15 KSLOC**
- `PM = 2.94 × (3.15)^1.10 = 2.94 × 3.46 ≈ **10.2 person-months**`
- **±range: 7–14 person-months** (COCOMO-II ±40% without detailed scale factors)
- Key cost drivers: triple repository implementation, XML config migration, JSP→modern view migration, security uplift

*Note: these figures apply to a clean-room rewrite. Incremental modernization of the existing codebase would be lower; see Recommended Pattern.*

### Technology Fingerprint

| Dimension | Current State |
|---|---|
| Language | Java 17 (enforced via `maven-enforcer-plugin`) |
| Framework | Spring Framework 7.0.7 (MVC, JDBC, ORM, AOP, OXM, Context Support) |
| Persistence | Hibernate 7.3.2 / Spring Data JPA 2025.1.5 — three swappable profiles |
| Build | Maven 3.x + `mvnw` wrapper; WAR packaging deployed to embedded Jetty 11 |
| Views | JSP 3.x + JSTL / Jakarta tags — 9 JSPs, 10 tag files |
| Database | H2 (default), HSQLDB, MySQL 8.1, PostgreSQL — all via Tomcat JDBC pool 11.0.18 |
| Cache | Caffeine (vets list only, `@Cacheable`) |
| Observability | AspectJ AOP call monitor; JMX export; SLF4J + Logback |
| Test | JUnit Jupiter 6.0.2; Spring MVC Test; Mockito |
| Security | **None** — no Spring Security, no CSRF, no auth/authz of any kind |
| Serialization | Jackson + JAXB2 (vet list served as JSON/XML via content negotiation) |
| Frontend | Bootstrap 5 via WebJars; SCSS compiled via libsass-maven-plugin |
| CI | GitHub Actions (`.github/` present) |
| Container | Dockerfile present (Google Jib configured for Docker Hub push) |

**Build artefact:** WAR file deployed to embedded `jetty:run-war`; no Spring Boot autoconfiguration present.

**Data schema:** 6 tables (`owners`, `pets`, `pet_types`, `vets`, `vet_specialties`, `visits`). DDL maintained in 4 vendor-specific SQL files (`db/h2/`, `db/hsqldb/`, `db/mysql/`, `db/postgresql/`).

---

## Architecture at a Glance

See `analysis/ARCHITECTURE.mmd` for the full Mermaid domain dependency diagram.

| Domain | Files | Description | Key Dependencies |
|---|---|---|---|
| **A. Bootstrap** | `PetclinicInitializer.java` | `WebApplicationInitializer` — creates root + servlet `XmlWebApplicationContext`, loads all XML configs, sets default Spring profile to `jpa` | All XML configs |
| **B. Domain Model** | 11 files in `model/` | JPA entities + JAXB wrapper. Hierarchy: `BaseEntity → Person → Owner/Vet`, `BaseEntity → NamedEntity → Pet/PetType/Specialty`, `BaseEntity → Visit` | Jakarta Persistence, Validation, JAXB |
| **C. Repository Interfaces** | 4 files in `repository/` | Technology-neutral contracts for Owner, Pet, Vet, Visit | Domain Model |
| **D. JDBC Impl** | 10 files in `repository/jdbc/` | Active under `jdbc` profile. Uses Spring 6 `JdbcClient`. `OneToManyResultSetExtractor` copied from archived project. N+1 in vet specialty loading. | Repo Interfaces, `javax.sql.DataSource` |
| **E. JPA Impl** | 5 files in `repository/jpa/` | Active under `jpa` (default) profile. Direct `EntityManager` with JPQL. | Repo Interfaces, JPA |
| **F. Spring Data JPA** | 4 files in `repository/springdatajpa/` | Active under `spring-data-jpa` profile. Interface-only; Spring generates impls. JPQL queries duplicated from E. | Repo Interfaces, Spring Data |
| **G. Service Facade** | 2 files in `service/` | Pure pass-through; only value is `@Transactional` + `@Cacheable` decoration | Repo Interfaces |
| **H. MVC Controllers** | 8 files in `web/` | 5 controllers, 1 formatter, 1 validator. `VetController` serves HTML + JSON + XML. | Service Facade, Domain Model |
| **I. Cross-Cutting** | 2 files in `util/` | AspectJ call monitor (JMX), `EntityUtils` helper (JDBC only) | Repo implementations (AOP weave) |
| **J. XML Configuration** | 6 files in `resources/spring/` | Full Spring wiring via XML — no `@Configuration` classes exist | Composes everything |

**Default active stack on startup:** Profile `jpa` + H2 in-memory → `JpaOwnerRepositoryImpl` / `JpaPetRepositoryImpl` / `JpaVetRepositoryImpl` / `JpaVisitRepositoryImpl` → `ClinicServiceImpl` → MVC Controllers → JSP views.

---

## Production Runtime Profile

**No production telemetry available.** The application has no APM integration, no distributed tracing, and no metrics endpoint. The only runtime observability is the JMX `CallMonitoringAspect` (call count + total elapsed time per repository bean), which:

- Fires only for the `jpa` and `jdbc` profiles (Spring Data JPA proxies are not `@Repository`-annotated so the pointcut misses them)
- Has no persistence — counters reset on restart
- Has no alerting or export capability

**Gap:** Without baseline p50/p95/p99 data, effort estimates cannot be telemetry-grounded. Before any production modernization, instrument with Micrometer + a time-series backend (Prometheus/Grafana) to measure actual request latencies per route.

---

## Technical Debt — Top 10

Ranked by remediation value (highest first).

| # | Finding | Severity | Effort | File:Line Evidence |
|---|---|---|---|---|
| 1 | **XML-only Spring configuration** — entire app wired via 4 XML files despite Spring 7 / Java 17 | High | L | `resources/spring/business-config.xml`, `mvc-core-config.xml`, `datasource-config.xml`, `tools-config.xml` |
| 2 | **JSP view layer** — dead-end tech, untestable, no hot-reload, Jasper compiler dependency | High | L | `webapp/WEB-INF/jsp/*.jsp`, `pom.xml:44-45` |
| 3 | **`javax.sql` import in Jakarta EE 10 codebase** — namespace inconsistency, migration trap | High | S | `JdbcOwnerRepositoryImpl.java:32`, `JdbcPetRepositoryImpl.java:32`, `JdbcVisitRepositoryImpl.java:25` |
| 4 | **Dead route — `showVisits` has no backing JSP** — `GET /owners/*/pets/{petId}/visits` → 500 | High | S | `VisitController.java:85-89` (no `visitList.jsp` exists) |
| 5 | **`findVisitsByPetId` missing `@Transactional`** — only service method without transaction boundary | High | S | `ClinicServiceImpl.java:105-108` |
| 6 | **Passthrough service façade** — `ClinicServiceImpl` delegates 1:1 to repos with zero business logic | Medium | M | `service/ClinicServiceImpl.java:54-108` |
| 7 | **Triplicated JPQL queries** — identical queries in `JpaOwnerRepositoryImpl` and `SpringDataOwnerRepository` must stay in sync | Medium | M | `JpaOwnerRepositoryImpl.java:56,65`, `SpringDataOwnerRepository.java:35,39` |
| 8 | **N+1 SQL in JDBC vet repository** — one query per vet for specialty IDs | Medium | S | `JdbcVetRepositoryImpl.java:70-85` |
| 9 | **`jpa.showSql=true` hardcoded** — every SQL statement logged in all environments | Medium | S | `data-access.properties:11` |
| 10 | **Dead `namedParameterJdbcTemplate` bean** — registered in `business-config.xml` but no consumer after `JdbcClient` migration | Low | S | `business-config.xml:76-79` |

**Additional debt flags (not top-10):**
- `CallMonitoringAspect` pointcut silently misses `spring-data-jpa` profile repositories (noted in the aspect's own Javadoc, line 27-28)
- Stale comments reference `aop.xml` and `orm.xml` that no longer exist
- `javaee` JNDI DataSource profile in `datasource-config.xml:39` is functional but entirely undocumented

---

## Security Findings

| ID | CWE | Severity | File:Line | Title |
|---|---|---|---|---|
| SEC-001 | CWE-862 | **Critical** | All controllers | No authentication or authorization — every endpoint is open |
| SEC-002 | CWE-352 | **High** | `PetclinicInitializer.java` / all forms | No CSRF protection on any POST form |
| SEC-003 | CWE-639 | **High** | `OwnerController.java:109`, `PetController.java:93,100` | IDOR — no ownership check on edit operations |
| SEC-004 | CWE-209 | **High** | `exception.jsp:12` | Raw Java exception message rendered to browser |
| SEC-005 | CWE-79 | **High** | `inputField.tag:23`, `findOwners.jsp:19` | Unescaped validation error → reflected XSS |
| SEC-006 | CWE-200 | **Medium** | `data-access.properties:11`, `logback.xml:17` | SQL + DEBUG logging enabled by default |
| SEC-007 | CWE-798 | **Medium** | `pom.xml:570,589` | Database credentials hard-coded in source control |
| SEC-008 | CWE-284 | **Medium** | `CrashController.java:33` | Unauthenticated diagnostic crash endpoint |
| SEC-009 | CWE-116 | **Medium** | `PetclinicInitializer.java` | No HTTP security headers (X-Frame-Options, CSP, HSTS) |
| SEC-010 | CWE-79 | **Medium** | `exception.jsp:12` | Unescaped exception message — XSS via error path |
| SEC-011 | CWE-1188 | **Medium** | `pom.xml:531,549` | H2/HSQLDB default credentials are empty password |
| SEC-012 | CWE-330/613 | **Medium** | `PetclinicInitializer.java` | No session security (HttpOnly, Secure, SameSite, timeout) |
| SEC-013 | CWE-1104 | **Low** | `pom.xml:35,68` | Font Awesome 4.7.0 (EOL 2017); MySQL driver 8.1.0 (outdated) |
| SEC-014 | CWE-425 | **Low** | `mvc-core-config.xml:39` | Default servlet handler enables forced browsing of webapp root |

**Highest-priority remediation path:** SEC-001 + SEC-002 (add Spring Security) → SEC-005 (XSS in error messages) → SEC-003 (IDOR checks). Adding Spring Security resolves SEC-001, SEC-002, SEC-009, and SEC-012 in a single dependency addition.

---

## Documentation Gaps

Top 5 behaviors a new engineer would need explained — not derivable from README, XML comments, or inline Javadoc:

| # | Gap | Impact |
|---|---|---|
| 1 | **How to activate profiles** — The relationship between Maven `-P` (database) and `-Dspring.profiles.active=` (persistence layer) is orthogonal and non-obvious. CLAUDE.md documents it, but README does not. An engineer running `./mvnw jetty:run-war` without reading CLAUDE.md will always run H2+JPA with no indication that two independent profiles exist. | High — first-day friction |
| 2 | **`CallMonitoringAspect` scope limitation** — The class's own comment mentions it doesn't work with Spring Data JPA, but nothing in `tools-config.xml` (where it's registered) documents this or guards it with a profile. Observers monitoring the JMX bean under `spring-data-jpa` will see zero calls and assume instrumentation is broken. | Medium — ops confusion |
| 3 | **Why three repository implementations exist** — The project ships full JDBC, JPA, and Spring Data JPA implementations for the same four entities. The README mentions "repository layer profiles" but does not explain whether this is a teaching feature, a production choice, or a migration-in-progress. New engineers might spend time trying to unify them without understanding the pedagogical intent. | High — wasted engineering effort |
| 4 | **The `javaee` JNDI datasource profile** — A nested `<beans profile="javaee">` block in `datasource-config.xml:39` defines a JNDI `DataSource` that can only be activated by JVM system property. No documentation, no Maven profile, no README mention. Engineers deploying to an application server (e.g., JBoss, WebLogic) would not find this without reading all XML. | Medium — deployment knowledge gap |
| 5 | **`VisitController.showVisits` is a dead endpoint** — `GET /owners/*/pets/{petId}/visits` maps to view `"visitList"` but no `visitList.jsp` exists, so any request returns 500. The visit list is only shown via the inline `ownerDetails.jsp` table. No comment or test flags this as intentionally incomplete. | High — runtime failure surprise |

---

## Effort Estimation

### Base estimate (COCOMO-II basic)

| Scope | KSLOC | COCOMO PM | Calendar (4 devs) |
|---|---|---|---|
| Java main + XML + JSP | 3.15 | **10.2** | ~2.5 months |
| ±40% range | — | 7–14 PM | 2–4 months |

### Modernization scenario breakdown

| Work item | Relative effort |
|---|---|
| Spring Boot 3.x migration (remove XML configs, `application.yaml`) | M |
| Consolidate to Spring Data JPA (delete JDBC + plain JPA impls) | M |
| JSP → Thymeleaf migration (9 JSPs + 10 tags) | M |
| Spring Security (auth, CSRF, headers, session) | M |
| Jakarta namespace cleanup + fix `findVisitsByPetId` + fix dead route | S |
| Test coverage uplift (currently ~14 test files, no integration test for JDBC) | L |
| CI/CD hardening (credentials out of pom.xml, Docker, SBOM scan) | S |

**Total modernization estimate: 6–10 person-months** for a team of 2–3 engineers, assuming the domain model and business logic remain unchanged (they are solid). The triple-repository structure is the largest single deletion win.

---

## Recommended Modernization Pattern

**Rearchitect** — targeted modernization within the same domain, discarding legacy plumbing while preserving the business model.

The domain model (`Owner`, `Pet`, `Vet`, `Visit`) is clean, well-annotated, and requires no changes. The business logic is minimal and correct. What needs to change is the *plumbing layer*:

1. **Spring Boot 3.x autoconfiguration** replaces all four XML config files, `PetclinicInitializer`, and the WAR packaging in a single migration step — no functional change, dramatic reduction in wiring surface area.
2. **Consolidate to Spring Data JPA** and delete the JDBC and plain JPA implementations (~250 lines of imperative data-access code). The Spring Data JPA interfaces already exist and are the only production-appropriate choice at this framework version.
3. **Thymeleaf views** replace JSPs and JSTL, enabling server-side rendering with testable, hot-reloadable templates. The existing Bootstrap 5 UI can be ported 1:1.
4. **Spring Security** with a minimal `SecurityFilterChain` closes all four high-severity and the single critical security finding in one dependency addition. Role-based access (receptionist vs read-only) can follow.
5. **Micrometer + Actuator** replaces the hand-rolled JMX `CallMonitoringAspect` with industry-standard metrics, enabling Prometheus/Grafana integration.

This pattern avoids a full rewrite (no change to domain model, service contract, or UI structure), delivers production-ready security and observability, and reduces the codebase by an estimated 30–40% while upgrading every major framework component.

**Alternative considered:** *Rebuild as Spring Boot + REST API + React SPA.* This would be the greenfield-optimal choice for a new clinic system but represents a complete rewrite of the view layer, introduces a separate frontend build pipeline, and is disproportionate to the scale and scope of this application. Reserve for a future phase after the Rearchitect stabilizes the backend.

---

*Assessment produced by Claude Code modernization agents. Verify findings against current repository state before using in budget submissions.*
