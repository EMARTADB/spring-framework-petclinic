# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->

## Build & Run Commands

```bash
# Run application (default: H2 in-memory database)
./mvnw jetty:run-war

# Run with external databases
./mvnw jetty:run-war -P MySQL
./mvnw jetty:run-war -P PostgreSQL

# Build & run all tests
./mvnw verify

# Run a single test class
./mvnw test -Dtest=OwnerControllerTests

# Run a single test method
./mvnw test -Dtest=OwnerControllerTests#testInitCreationForm

# Compile CSS from SCSS
./mvnw generate-resources -P css

# Build Docker image (requires Docker Hub credentials)
mvn jib:build
```

## Architecture

3-layer Spring MVC web application packaged as a WAR, deployed to Jetty.

**Main packages under `org.springframework.samples.petclinic`:**
- `model/` — Domain entities (`Owner`, `Pet`, `Vet`, `Visit`, `PetType`, `Specialty`). Hierarchy: `BaseEntity` → `NamedEntity` → `Person` → `Owner`/`Vet`.
- `repository/` — Data access with three swappable implementations: `jpa/`, `jdbc/`, `springdatajpa/`.
- `service/` — `ClinicService` interface + single transactional implementation wiring repositories.
- `web/` — Spring MVC controllers and formatters.

**Spring configuration is entirely XML-based** (no `application.properties`):
- `src/main/resources/spring/mvc-core-config.xml` — Web tier, component scan, resource mapping, i18n.
- `src/main/resources/spring/mvc-view-config.xml` — JSP view resolver, content negotiation.
- `src/main/resources/spring/business-config.xml` — Repository layer profiles, transaction management.
- `src/main/resources/spring/datasource-config.xml` — Tomcat JDBC pool, SQL init scripts.
- `src/main/resources/spring/data-access.properties` — Externalised JDBC/JPA properties (populated by Maven profiles).

`PetclinicInitializer.java` is the programmatic web.xml replacement (`WebApplicationInitializer`).

## Profiles

**Database (Maven `-P` flag):**
| Profile | Database |
|---------|----------|
| `H2` (default) | In-memory H2 |
| `HSQLDB` | In-memory HSQL |
| `MySQL` | `jdbc:mysql://localhost:3306/petclinic` |
| `PostgreSQL` | `jdbc:postgresql://localhost:5432/petclinic` |

**Persistence layer (`-Dspring.profiles.active=`):**
| Value | Implementation |
|-------|---------------|
| `jpa` (default) | Hibernate JPA with `EntityManagerFactory` |
| `jdbc` | `NamedParameterJdbcTemplate` |
| `spring-data-jpa` | Spring Data JPA repositories |

These two profiles are orthogonal and can be combined:
```bash
./mvnw jetty:run-war -P MySQL -Dspring.profiles.active=jdbc
```

## Key Technology Versions

- Java 17+ required (enforced by `maven-enforcer-plugin`)
- Spring Framework 7.0.x
- Hibernate 7.x (Jakarta EE — uses `jakarta.*` not `javax.*`)
- JUnit 5 (test file pattern: `**/*Tests.java`)
- Bootstrap 5 via WebJars; views in `src/main/webapp/WEB-INF/`

