---
project_name: 'spring-framework-petclinic'
user_name: 'david1'
date: '2026-11-05'
sections_completed: ['technology_stack', 'critical_implementation_rules']
existing_patterns_found: 9
---

# Project Context for AI Agents

_Critical rules and patterns AI agents must follow when implementing code in this project. Focus on unobvious details._

---

## Technology Stack & Versions

- Java 17 (`java.version`), Maven (wrapper `mvnw`), packaging **WAR** (`7.0.3`)
- Spring Framework 7.0.7 (XML + annotation config, **no Spring Boot**), Spring Data 2025.1.5 (BOM)
- Servlet API 6.1.0 / Jakarta namespace (`jakarta.*`), JSP + JSTL 3.0, custom `.tag` files; Tomcat 11.0.18 (provided), Jetty plugin 11.0.26
- Hibernate 7.3.2.Final, JPA API 3.2.0, Hibernate Validator 9.1.0.Final
- Databases: HSQLDB 2.7.4 (default), H2 2.4.240, MySQL driver 8.1.0, PostgreSQL driver 42.7.11; Caffeine 3.2.3 cache
- Jackson 3.1.2 (`tools.jackson.*` packages), AspectJ 1.9.25.1
- Logging: SLF4J 2.0.17 + Logback 1.5.32
- Tests: JUnit Jupiter 6.0.2, Mockito 5.23.0, AssertJ 3.27.7, Hamcrest 3.0, JsonPath 2.10.0; JaCoCo 0.8.14; JMeter plan in `src/test/jmeter`
- Front end: WebJars Bootstrap 5.3.8, Font Awesome 4.7.0, flatpickr 4.6.13; SCSS compiled via `css` Maven profile (libsass plugin)
- Docker via Jib plugin 3.5.1; Maven Enforcer enforced

## Critical Implementation Rules

### Language & Style
- Base package `org.springframework.samples.petclinic`; sub-packages `model`, `repository` (+ `jdbc`, `jpa`, `springdatajpa`), `service`, `util`, `web`.
- `.editorconfig`: UTF-8, LF, spaces, 4-space indent for Java/XML, trim trailing whitespace, final newline.
- Use `jakarta.*` imports only (never `javax.*`). Constructor injection (see `ClinicServiceImpl`).
- Each package has `package-info.java`; Apache-2.0 license header and `@author` Javadoc on classes.

### Architecture & Configuration
- Layering: `web` controllers -> `ClinicService` facade (`ClinicServiceImpl`, holds `@Transactional` / `@Cacheable`) -> repository interfaces.
- Configuration is **XML-based** in `src/main/resources/spring/` (`business-config.xml`, `datasource-config.xml`, `mvc-core-config.xml`, `mvc-view-config.xml`, `tools-config.xml`); the servlet is bootstrapped programmatically by `PetclinicInitializer` (no `web.xml`).
- Persistence is selected by Spring **profile**: `jpa` (default, hardcoded in `PetclinicInitializer`), `jdbc`, `spring-data-jpa`. Override with `-Dspring.profiles.active=...`.
- Every new repository operation must be added to the repository interface AND implemented in all three variants (`repository/jdbc`, `repository/jpa`, `repository/springdatajpa`).
- Controllers should depend on `ClinicService`, never on repositories directly.

### Database
- DB selected by Maven profile (`H2`, `HSQLDB`, `MySQL`, `PostgreSQL`) which filters `data-access.properties` placeholders (`${db.script}`, `${jdbc.*}`, `${jpa.database}`).
- Schema changes must be applied to every `src/main/resources/db/<db>/schema.sql` and `data.sql` (h2, hsqldb, mysql, postgresql).

### Web / UI
- Views are JSP under `WEB-INF/jsp/<area>/` with reusable tags in `WEB-INF/tags/`; i18n via `messages/messages*.properties` (default, de, en, es) - add keys to all locales.
- Bootstrap version in `footer.tag` must match `webjars-bootstrap.version` in `pom.xml`.
- Edit `.scss` sources, not generated CSS, when styling.

### Testing
- Tests live in `src/test/java` mirroring main packages. Service tests: `AbstractClinicServiceTests` with one subclass per profile (`ClinicServiceJdbcTests`, `ClinicServiceJpaTests`, `ClinicServiceSpringDataJpaTests`) using `@SpringJUnitConfig` + `@ActiveProfiles`; new service behavior must pass under all three.
- Controller tests use `src/test/resources/spring/mvc-test-config.xml`.
- Run: `./mvnw test`; CI in `.github/workflows/maven-build-*.yml`.

### Don't-Miss
- Do not introduce Spring Boot or `javax.*` dependencies; keep versions managed via `pom.xml` properties.
- Jackson 3 uses `tools.jackson` packages.
- Do not commit secrets; DB credentials come from Maven profile properties.
