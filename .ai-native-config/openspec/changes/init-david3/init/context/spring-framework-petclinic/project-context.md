---
project_name: spring-framework-petclinic
sections_completed: [technology_stack, language_rules, framework_rules, testing_rules, quality_rules, workflow_rules, anti_patterns]
---

# Project Context for AI Agents — spring-framework-petclinic

Critical rules for implementing code in this repository. Focus on unobvious details.

## Technology Stack & Versions

- Java 17; Maven (wrapper `mvnw`); packaging **WAR** (Tomcat 11 / Jetty 11 plugin), artifact version 7.0.3
- Spring Framework 7.0.7 (plain Spring, **NOT Spring Boot**), Spring MVC, Spring Data JPA 2025.1.5
- Hibernate 7.3.2.Final, Hibernate Validator 9.1.0.Final, JPA API 3.2.0
- Jakarta EE namespace (`jakarta.*`): Servlet 6.1, JSTL 3.0; views are **JSP + custom tags**
- Databases: HSQLDB 2.7.4 (default), H2 2.4.240, MySQL 8.1.0, PostgreSQL 42.7.11 via Maven profiles; Caffeine cache
- Logging SLF4J 2.0 + Logback 1.5; Jackson 3.x (`tools.jackson`)
- Tests: JUnit Jupiter 6, AssertJ, Mockito 5, Hamcrest, JSON-path; JaCoCo coverage; JMeter plan in `src/test/jmeter`
- Frontend: Bootstrap 5.3.8, Font Awesome, flatpickr (webjars); SCSS compiled by libsass plugin under profile `css`

## Critical Implementation Rules

### Language / Java
- Base package `org.springframework.samples.petclinic`; subpackages `model`, `repository` (`jdbc`, `jpa`, `springdatajpa`), `service`, `web`, `util`.
- Use `jakarta.*` imports only; never `javax.*`.
- Constructor injection (see `OwnerController`); each source file carries the Apache 2.0 header and `@author` javadoc.
- 4-space indentation; `package-info.java` exists in packages.

### Framework / Architecture
- Configuration is **XML-based** in `src/main/resources/spring/` (`business-config`, `datasource-config`, `mvc-core-config`, `mvc-view-config`, `tools-config`); bootstrapped by `PetclinicInitializer` (servlet initializer). Prefer extending these over adding Boot-style config.
- Layering: Controller (`web`) -> `ClinicService`/`ClinicServiceImpl` (transactional) -> repository interfaces (`OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository`).
- **Three interchangeable persistence implementations selected by Spring profile**: `jdbc`, `jpa`, `spring-data-jpa`. Any repository change must be implemented/kept consistent in all three packages and component-scan/profile wiring in `business-config.xml` respected.
- DB selection via Maven profiles (H2, HSQLDB, MySQL, PostgreSQL) which filter `data-access.properties` placeholders (`db.script`, `jdbc.*`, `jpa.database`); schema/data scripts live in `src/main/resources/db/<db>/schema.sql|data.sql` — update every DB variant when changing schema.
- Controllers disallow binding of `id` through `@InitBinder`; keep this pattern. Validation uses Bean Validation plus `PetValidator`.
- Views: JSP in `WEB-INF/jsp/<area>/`, reusable tags in `WEB-INF/tags`; controllers return view-name constants. i18n through `messages/messages_{en,es,de}.properties` — add keys to all locales.
- Entities extend `BaseEntity` / `NamedEntity` / `Person`.

### Testing
- Tests in `src/test/java` mirroring packages: `model`, `service`, `web`. Service tests use an abstract base (`AbstractClinicServiceTests`) with concrete Jdbc/Jpa/SpringDataJpa subclasses — new service behavior must pass for all three.
- Web tests use Spring test MVC config `src/test/resources/spring/mvc-test-config.xml`.
- Run: `./mvnw test`; run app: `./mvnw jetty:run-war` (check pom for exact plugin config).

### Code Quality & Style
- Keep controllers thin; business logic in service layer; naming `XxxController`, `XxxRepository`, `JdbcXxxRepositoryImpl`, `JpaXxxRepositoryImpl`, `SpringDataXxxRepository`, `XxxTests`.
- Maven enforcer plugin is configured; do not bypass dependency/version rules. Versions are centralized as pom properties.

### Workflow
- Branching/commit conventions not defined in repo (unknown); do not commit unless asked.

### Anti-Patterns / Don'ts
- Don't introduce Spring Boot, auto-configuration, or `javax.*`.
- Don't change schema for one database only.
- Don't hardcode DB credentials; use profile-filtered properties.
- Don't add repository logic to just one persistence profile.
- Don't bind `id` from request data.

## Usage Guidelines
- Read this before implementing; prefer the more restrictive option when unsure; update when the stack changes.
