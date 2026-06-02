# Modernization Brief — Spring Framework PetClinic

> **Status:** DRAFT — Awaiting steering-committee approval before any code transformation begins  
> **Date:** 2026-05-29  
> **Author:** AI-Native Modernization Assessment (OpenCode)  
> **Input artifacts:** `ASSESSMENT.md`, `BUSINESS_RULES.md`, `DATA_OBJECTS.md`, `TOPOLOGY.html`

---

## 1. Objective

Transform the Spring Framework PetClinic from a multi-stack educational monolith into a production-ready, single-stack Spring Boot 3 application that:

1. Eliminates the three parallel persistence stacks (JDBC, JPA, Spring Data JPA) — keeping **Spring Data JPA only**.
2. Adds authentication and authorization via **Spring Security 6**.
3. Exposes a **REST API** (JSON) alongside a **Thymeleaf** UI, replacing JSP/JSTL.
4. Closes all **8 P0 business rules** and **13 CWE security findings** before go-live.
5. Achieves **observability** via Micrometer + Actuator.

**Out of scope for this brief:** UI redesign, feature additions beyond existing functionality, data migration from legacy databases.

---

## 2. Target Architecture (C4 — Container Level)

```
┌─────────────────────────────────────────────────────────────────┐
│  Browser / Mobile Client                                        │
│  HTTP/S → Thymeleaf pages  |  HTTP/S → REST JSON API           │
└────────────────┬────────────────────────┬───────────────────────┘
                 │                        │
     ┌───────────▼────────────────────────▼────────────┐
     │          Spring Boot 3 Application               │
     │  ┌──────────────┐   ┌───────────────────────┐   │
     │  │ Web Layer     │   │ REST API Layer         │   │
     │  │ (Thymeleaf)   │   │ (@RestController)      │   │
     │  └──────┬───────┘   └────────────┬──────────┘   │
     │         │                        │               │
     │  ┌──────▼────────────────────────▼──────────┐   │
     │  │         Service Layer                     │   │
     │  │  OwnerService · PetService · VisitService │   │
     │  │  VetService                               │   │
     │  └──────────────────────┬────────────────────┘   │
     │                         │                        │
     │  ┌──────────────────────▼────────────────────┐   │
     │  │      Spring Data JPA Repositories          │   │
     │  │  OwnerRepository · PetRepository           │   │
     │  │  VisitRepository · VetRepository           │   │
     │  └──────────────────────┬────────────────────┘   │
     │                         │                        │
     │  ┌──────────────────────▼────────────────────┐   │
     │  │    Spring Security 6 (Cross-cutting)       │   │
     │  │  Form login · CSRF · Method security       │   │
     │  └───────────────────────────────────────────┘   │
     │                                                   │
     │  ┌───────────────────┐  ┌────────────────────┐   │
     │  │  Caffeine Cache    │  │  Micrometer/        │   │
     │  │  (VetService)      │  │  Actuator           │   │
     │  └───────────────────┘  └────────────────────┘   │
     └─────────────────────────────────┬────────────────┘
                                       │
                          ┌────────────▼───────────┐
                          │   RDBMS                 │
                          │  PostgreSQL (prod)       │
                          │  H2 (test / local)       │
                          └────────────────────────┘
```

**Key changes from current state:**

| Concern | Current | Target |
|---------|---------|--------|
| Boot chassis | Servlet WAR (Tomcat 11) | Spring Boot 3 executable JAR |
| Persistence | JDBC + JPA + Spring Data JPA | Spring Data JPA only |
| View layer | JSP/JSTL + custom tags | Thymeleaf 3 |
| Security | None | Spring Security 6 (form login + CSRF) |
| API | None | REST JSON (`/api/v1/…`) |
| Observability | AspectJ no-op (`CallMonitoringAspect`) | Micrometer + `/actuator` |
| Database (prod) | MySQL / PostgreSQL / HSQLDB | PostgreSQL |
| Config | `applicationContext.xml` + profiles | `application.yml` + Spring Boot auto-config |

---

## 3. Phased Delivery Sequence

### Phase 0 — Safety Net (2 weeks, 1 engineer)

**Goal:** Pin existing behavior with characterization tests before any transformation.

| Task | Owner | Exit Criterion |
|------|-------|---------------|
| Write `@SpringBootTest` smoke tests against all 4 controller endpoints | BE | Green CI |
| Capture all P0 business rules as `@ParameterizedTest` unit tests | BE | 8 tests passing against current code |
| Freeze `BUSINESS_RULES.md` P0 list with product owner sign-off | PM | Signed document |
| Resolve 10 SME questions (see §6) | PM + Dev | Decision log updated |

### Phase 1 — Spring Boot Migration (3 weeks, 2 engineers)

**Goal:** Replace WAR chassis with Spring Boot 3, keep all three persistence stacks temporarily.

| Task | Notes |
|------|-------|
| Add `spring-boot-starter-web`, remove `web.xml`, `DispatcherServlet` XML config | Replace `applicationContext.xml` with auto-config |
| Keep JSP views temporarily (Spring Boot supports JSP with `tomcat-embed-jasper`) | Avoids big-bang risk |
| Replace `applicationContext-*.xml` datasource beans with `application.yml` | Per-profile YAML blocks |
| Validate all P0 characterization tests still pass | Gate |

### Phase 2 — Collapse to Spring Data JPA (2 weeks, 2 engineers)

**Goal:** Delete JDBC and plain-JPA stacks.

| Task | Notes |
|------|-------|
| Set `spring-data-jpa` as the only active profile | Remove JDBC + JPA profile activations |
| Delete `repository/jdbc/` and `repository/jpa/` packages (8 + 6 files) | ~800 lines removed |
| Delete `JdbcClinic`, `JpaClinic` XML configs | |
| Fix RULE-033 (pet type null on update) in `PetController` + `VisitController` | P0 crash path |
| Fix RULE-021 (silent 0-row UPDATE) — add `@Modifying(clearAutomatically=true)` guard | P0 data integrity |
| Re-run P0 test suite | Gate |

### Phase 3 — Spring Security (2 weeks, 1 engineer)

**Goal:** Close CWE-352 (CSRF Critical) and CWE-862 (Auth Critical).

| Task | Notes |
|------|-------|
| Add `spring-boot-starter-security` | |
| Implement `SecurityFilterChain`: form login, logout, CSRF enabled | |
| Protect all write endpoints (`POST /owners`, `POST /pets`, `POST /visits`) with `ROLE_STAFF` | |
| Add `UserDetailsService` backed by in-memory / DB users | Scope: single role for MVP |
| Remove hardcoded DB passwords from `pom.xml` (lines 569-570, 588-589) → `application.yml` / env vars | CWE-259 |
| Validate CSRF token present on all form submissions | |

### Phase 4 — Thymeleaf + REST API (3 weeks, 2 engineers)

**Goal:** Replace JSP with Thymeleaf; expose JSON REST API.

| Task | Notes |
|------|-------|
| Add `spring-boot-starter-thymeleaf` | |
| Migrate 9 JSP views + 10 tag files to Thymeleaf templates | 1:1 feature parity |
| Fix dangling `"visitList"` view reference in `VisitController` | Bug: view not found at runtime |
| Add `@RestController` API layer (`/api/v1/owners`, `/api/v1/pets`, `/api/v1/visits`, `/api/v1/vets`) | |
| Replace `CallMonitoringAspect` no-op with Micrometer `@Timed` annotations | |
| Add pagination to owner search (fix full-table-scan on blank query) | |

### Phase 5 — Hardening & Go-Live (2 weeks, 1 engineer)

| Task | Notes |
|------|-------|
| Remove H2/HSQLDB dependencies from production POM profile | |
| Add Flyway migrations for schema management | Replace SQL init scripts |
| Add `spring-boot-starter-actuator` with health + metrics endpoints | |
| Address remaining CWEs: XSS output encoding, error message suppression, input validation | |
| Performance test: owner search with 10k rows | Validate pagination fix |
| Update Docker image build (JIB config) | |

### Gantt (calendar weeks, single-team execution)

```
Week:   1  2  3  4  5  6  7  8  9 10 11 12
P0      ██ ██
P1            ██ ██ ██
P2                     ██ ██
P3                           ██ ██
P4                                 ██ ██ ██
P5                                          ██ ██
```

**Total elapsed: ~12 weeks (3 months) · Total effort: ~24 person-weeks (~6 PM)**

---

## 4. Behavior Contract — P0 Rules (Must Not Break)

These 8 rules must pass characterization tests before, during, and after every phase gate.

| Rule ID | Description | Test Type |
|---------|-------------|-----------|
| RULE-001 | `isNew()` controls INSERT vs UPDATE — never mix | Unit: `BaseEntity.isNew()` with null/non-null id |
| RULE-002 | Telephone field: digits only, 10 chars exact | Unit: `@Digits` constraint validator |
| RULE-020 | Vet list cached; cache never evicts during application lifetime | Integration: call twice, assert single DB query |
| RULE-021 | 0-row UPDATE must surface as error, not silent success | Integration: update non-existent owner id, assert exception |
| RULE-022 | `id` field must not be bindable from HTTP request | Unit: `@InitBinder` blocks `id` field |
| RULE-026 | Deleting an Owner cascade-deletes all Pets (JPA cascade) | Integration: delete owner, assert pet rows gone |
| RULE-027 | Deleting a Pet cascade-deletes all Visits (JPA cascade) | Integration: delete pet, assert visit rows gone |
| RULE-033 | Pet type must be re-validated on update (not assumed from form) | Integration: submit update with blank type, assert 400 / validation error (not NPE) |

---

## 5. Validation Strategy

### Test Pyramid

```
         /\
        /  \   E2E (Playwright/Selenium) — 5 smoke flows
       /────\  Integration (@SpringBootTest) — controller + repo round-trips
      /──────\ Unit (JUnit Jupiter) — service, model, validator
     /────────\ Characterization — P0 rules pinned against legacy behavior
```

### Gate Criteria per Phase

| Phase | Must Pass |
|-------|-----------|
| P0 → P1 | 8 P0 characterization tests green |
| P1 → P2 | All existing controller integration tests green on Spring Boot chassis |
| P2 → P3 | P0 suite + RULE-033 / RULE-021 fixes verified |
| P3 → P4 | Security: CSRF token test, auth-required endpoints return 401 when unauthenticated |
| P4 → P5 | All API endpoints return correct JSON; Thymeleaf views render without JSP engine |
| P5 → Go-live | No P0/P1 Sonar issues; Actuator `/health` UP; load test passes |

### Regression Safety

- Feature branch per phase; PR requires 2 reviewers + CI green.
- `BUSINESS_RULES.md` serves as the acceptance test specification document.
- Any deviation from P0 rules requires explicit product-owner sign-off before merge.

---

## 6. Open Questions (SME Blockers)

The following 10 questions must be resolved before the corresponding phase begins. Items marked **CRITICAL** block the phase gate.

| # | Question | Blocks | Criticality |
|---|----------|--------|-------------|
| Q1 | Should deleting an Owner hard-delete their Pets and Visits, or soft-delete / archive? (RULE-026/027 — potential medical record loss) | P2 | **CRITICAL** |
| Q2 | Are Visits immutable after creation? Can a vet update/delete a scheduled visit? (RULE-024) | P4 | **CRITICAL** |
| Q3 | Is duplicate pet name under the same owner a bug or intentional? (RULE-005) | P2 | High |
| Q4 | Should owner search be case-insensitive on all DBs, or is H2 behavior acceptable to drop? | P1 | High |
| Q5 | Is pagination required on owner search, or is the full-table-scan acceptable for current data volumes? | P4 | Medium |
| Q6 | What authentication model is required for Phase 3? (Single role vs. RBAC; SSO/OIDC vs. form login) | P3 | **CRITICAL** |
| Q7 | Should the REST API (Phase 4) be versioned from day one, or is `/api/v1` over-engineering for current consumers? | P4 | Medium |
| Q8 | Is the `CallMonitoringAspect` JMX feature required in the target system, or can it be replaced entirely by Micrometer? | P4 | Low |
| Q9 | What is the target database for production? (PostgreSQL assumed — confirm collation and character set) | P1 | High |
| Q10 | Are there downstream consumers of the current WAR artifact (CI/CD, deployment scripts) that must be updated in lockstep? | P1 | High |

---

## 7. Approval Block

By signing below, the steering committee authorizes the engineering team to begin **Phase 0** work as described in this brief. No code transformation will be committed to the main branch until Phase 0 characterization tests are written and passing.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Engineering Lead | | | |
| Security Lead | | | |
| Architecture Lead | | | |

---

*This document is generated from static analysis only. No production traffic data was available. Estimates carry ±40% uncertainty. All decisions in §6 must be resolved before the corresponding phase gate.*
