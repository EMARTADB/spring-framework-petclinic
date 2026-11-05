---
project_name: 'spring-framework-petclinic'
user_name: 'mduenasb'
date: '2026-11-05'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'code_quality_rules', 'workflow_rules', 'critical_rules']
existing_patterns_found: 12
---

# Project Context for AI Agents

_Critical rules and patterns AI agents must follow when implementing code in this project. Focus on unobvious details._

---

## Technology Stack & Versions

- Java 17 (`java.version`), Maven (wrapper `mvnw`, enforcer plugin 3.6.2), packaging **war** (artifact version 7.0.3)
- Spring Framework 7.0.7 (XML + annotation config, Spring MVC, JSP views with JSTL 3.0.2)
- Jakarta EE: Servlet API 6.1.0 (provided), JPA API 3.2.0, Tomcat 11.0.18 (jasper-el, provided), JAXB 4.0.x
- Persistence: Spring Data 2025.1.5 (BOM), Hibernate 7.3.2.Final, Hibernate Validator 9.1.0.Final, Caffeine 3.2.3
- Databases: H2 2.4.240 (default profile), HSQLDB 2.7.4, MySQL driver 8.1.0, PostgreSQL driver 42.7.11
- JSON: Jackson 3 (`tools.jackson`, 3.1.2); AspectJ 1.9.25.1
- Logging: SLF4J 2.0.17 + Logback 1.5.32
- Web assets: Bootstrap 5.3.8, Font Awesome 4.7.0, Flatpickr 4.6.13 (webjars); SCSS via libsass plugin (`css` profile)
- Test: JUnit Jupiter 6.0.2, Mockito 5.23.0, AssertJ 3.27.7, Hamcrest 3.0, JsonPath 2.10.0, JaCoCo 0.8.14, Surefire 3.5.5
- Run: Jetty maven plugin 11.0.26; container image via Jib 3.5.1

## Critical Implementation Rules

### Language-Specific Rules

- Java 17 source/target; UTF-8 sources.
- Jackson 3 uses the `tools.jackson.*` package namespace (not `com.fasterxml.jackson`); do not mix.
- Use `jakarta.*` imports (never `javax.*`).
- Constructor injection is used (e.g. `ClinicServiceImpl`); keep dependencies `final`.

### Framework-Specific Rules

- Package root: `org.springframework.samples.petclinic` with layers `model`, `repository` (+ `jdbc`, `jpa`, `springdatajpa` sub-packages), `service`, `web`, `util`.
- Configuration is **XML-driven** in `src/main/resources/spring/` (`business-config.xml`, `datasource-config.xml`, `mvc-core-config.xml`, `mvc-view-config.xml`, `tools-config.xml`); the root context is bootstrapped by `PetclinicInitializer` (no web.xml). Add beans/scans there, not via new Java config unless following existing pattern.
- Three mutually exclusive persistence **Spring profiles**: `jdbc`, `jpa` (default, set in `PetclinicInitializer`), `spring-data-jpa`. Every repository interface (`OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository`) must have an implementation per profile; a change to a repository contract must be applied to all three. Override with `-Dspring.profiles.active=...`.
- Controllers talk only to `ClinicService` (facade, owner of `@Transactional`/`@Cacheable`), never directly to repositories.
- Views are JSP under `src/main/webapp/WEB-INF/jsp` with custom tags in `WEB-INF/tags`; i18n via `messages/messages*.properties` (default, de, en, es) — add keys to all locales.
- Database selection by Maven profile (`H2` default, `HSQLDB`, `MySQL`, `PostgreSQL`) which fills `${db.script}`, `jdbc.*`, `jpa.database` placeholders in `data-access.properties`; schema/data scripts live in `src/main/resources/db/<db>/`. Keep SQL scripts in sync across all four DBs.
- `CallMonitoringAspect` (AspectJ/AOP) is in `util`; keep AOP wiring in `tools-config.xml`.

### Testing Rules

- Tests under `src/test/java` mirroring packages: `model`, `service`, `web`.
- Service tests extend `AbstractClinicServiceTests`, with concrete subclasses per profile (`ClinicServiceJdbcTests`, `ClinicServiceJpaTests`, `ClinicServiceSpringDataJpaTests`) selected via `@ActiveProfiles`. New service behaviour must be covered by the abstract class so all profiles are verified.
- Web controllers tested with Spring MVC test + Mockito (`*ControllerTests`); naming suffix `Tests` (plural).
- Run with `./mvnw test`; JaCoCo coverage is configured.

### Code Quality & Style Rules

- `.editorconfig`: UTF-8, LF, final newline, spaces; 4-space indent and trimmed trailing whitespace for `*.java`/`*.xml`.
- Class names PascalCase; implementation suffixes: `*RepositoryImpl` (jdbc/jpa), `SpringData*Repository`; `package-info.java` per package.
- Javadoc with `@author` tags is the existing convention for classes.

### Development Workflow Rules

- CI: GitHub Actions (`maven-build-main.yml`, `maven-build-pull-request.yml`); Dependabot enabled.
- Maven enforcer enforces build tool/Java constraints; use the `mvnw` wrapper.
- Build artifact is a WAR deployed to Tomcat/Jetty; container image through Jib (`docker.image.prefix=springcommunity`).

### Critical Don't-Miss Rules

- Do not introduce `javax.*` or Jackson 2 imports.
- Do not hard-code DB settings; use Maven-profile-filtered placeholders in `data-access.properties`.
- Do not set both a persistence unit and `packagesToScan` expectations: in `business-config.xml` the persistence unit name wins.
- Do not bypass `ClinicService` from the web layer or add `@Transactional` outside the service/repository conventions.
- Keep the Bootstrap version in sync with the footer tag (see `pom.xml` comment on `webjars-bootstrap.version`).
- `readme.md` / `LICENSE.txt` (Apache 2.0) apply; no secrets in properties files committed.
