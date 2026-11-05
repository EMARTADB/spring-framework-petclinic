---
project_name: spring-framework-petclinic
repository: ./spring-framework-petclinic
change: init-david4
---

# Project Context: Spring Framework Petclinic

Critical rules for AI agents. Derived from `pom.xml`, `src/main`, `src/test`, `.editorconfig`.

## Technology Stack & Versions

- Java 17 (`java.version`), Maven (wrapper `mvnw`), packaging **WAR** (version 7.0.3).
- Spring Framework 7.0.7; Spring Data BOM 2025.1.5; Hibernate 7.3.2.Final; Hibernate Validator 9.1.0.Final; JPA API 3.2.0.
- Jakarta namespace (`jakarta.*`): Servlet 6.1.0, JSTL 3.0.x, Tomcat 11 (jasper-el, provided); Jetty maven plugin 11.0.26.
- Jackson 3.x (`tools.jackson.*` group/packages, not `com.fasterxml`).
- DBs: H2 2.4.240 (default profile), HSQLDB 2.7.4, MySQL 8.1.0, PostgreSQL 42.7.11 drivers.
- Caffeine 3.2.3 cache; AspectJ 1.9.25.1; Logback 1.5.32 / SLF4J 2.0.17.
- Tests: JUnit Jupiter 6.0.2, Mockito 5.23.0, AssertJ 3.27.7, Hamcrest 3.0, json-path 2.10.0; JaCoCo 0.8.14.
- Frontend: JSP + JSP tag files, Bootstrap 5.3.8 / Font Awesome / flatpickr via WebJars; SCSS compiled by libsass plugin (Maven profile `css`).

## Language & Framework Rules

- **No Spring Boot.** Plain Spring Framework with XML configuration: `src/main/resources/spring/{business,tools,datasource,mvc-core,mvc-view}-config.xml`. Do not introduce Boot, auto-configuration, or `application.properties`.
- Bootstrap is `PetclinicInitializer` (`AbstractAnnotationConfigDispatcherServletInitializer`-style, Java servlet 3+ initializer, no web.xml). Root context: `business-config.xml` + `tools-config.xml`; servlet context: `mvc-core-config.xml`; mapping `/`; UTF-8 `CharacterEncodingFilter`.
- Package root: `org.springframework.samples.petclinic` with `model`, `repository` (+`jdbc`, `jpa`, `springdatajpa`), `service`, `web`, `util`.
- Layering: Controller (`web`) -> `ClinicService`/`ClinicServiceImpl` -> repository interfaces (`OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository`). Controllers must not use repositories directly.
- **Three interchangeable persistence implementations**, selected by Spring profile: `jpa` (default, set in `PetclinicInitializer.SPRING_PROFILE`), `jdbc`, `spring-data-jpa`. Any repository change/new method must be implemented in all three packages and kept behavior-equivalent. Override via `-Dspring.profiles.active=...`.
- Transactions via `@Transactional` (`tx:annotation-driven`); repositories use `@Repository` for exception translation.
- Caching: `@Cacheable` with Caffeine cache names `default` and `vets` (declared in `tools-config.xml`; new cache names must be added there).
- AOP/JMX: `CallMonitoringAspect` registered in `tools-config.xml`.
- Property placeholders in `data-access.properties` (`${db.script}`, `${jdbc.*}`, `${jpa.database}`) are filtered by Maven profiles at build time.

## Database Rules

- Maven DB profiles: `H2` (activeByDefault), `HSQLDB`, `MySQL`, `PostgreSQL`; schema/data scripts per DB in `src/main/resources/db/<db>/{schema,data}.sql`. Schema changes must be applied to **all** DB script sets.

## Code Style

- `.editorconfig`: UTF-8, LF, final newline, spaces; 4-space indent for Java/XML, trim trailing whitespace.
- i18n: user-visible text goes in `messages/messages*.properties` (default, en, es, de); add keys to every bundle.
- Entities extend `BaseEntity`/`NamedEntity`/`Person` in `model`; keep `package-info.java` per package.

## Testing Rules

- Tests under `src/test/java/.../{model,service,web}`; web tests use Spring MVC test config `src/test/resources/spring/mvc-test-config.xml`.
- Service tests: `AbstractClinicServiceTests` with concrete subclasses per implementation (`ClinicServiceJdbcTests`, `ClinicServiceJpaTests`, `ClinicServiceSpringDataJpaTests`). New service behavior must pass under all three.
- Controller tests: `*ControllerTests` (MockMvc style). Run with `./mvnw test`.
- JMeter plan at `src/test/jmeter/petclinic_test_plan.jmx`.

## Build & Run

- Build: `./mvnw package`; run: `./mvnw jetty:run` (per Jetty plugin); CI in `.github/workflows/maven-build-{main,pull-request}.yml`; Docker image via Jib (`springcommunity` prefix); Maven enforcer is configured.

## Critical Don'ts

- Don't use `javax.*` packages; use `jakarta.*`.
- Don't add Boot starters or annotation-only config that bypasses the XML files without reason.
- Don't edit only one persistence implementation or one DB script set.
- Don't hand-edit generated `petclinic.css`; edit SCSS (`resources/scss`).
- JSPs live in `WEB-INF/jsp` and reuse tags in `WEB-INF/tags`; keep that structure.
