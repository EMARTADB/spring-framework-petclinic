# Spring Framework PetClinic - Agent Instructions

## Build & Run

**Run the application:**
```bash
./mvnw jetty:run-war
# Windows: ./mvnw.cmd jetty:run-war
```
Access at http://localhost:8080/

**Run tests:**
```bash
./mvnw verify
```
Test files must end with `*Tests.java` (configured in maven-surefire-plugin).

**Build WAR:**
```bash
./mvnw install
```
Output: `target/petclinic.war`

## Critical: CSS Generation

CSS is **generated** from SCSS. If you modify `src/main/webapp/resources/scss/petclinic.scss`, regenerate CSS:
```bash
./mvnw generate-resources -P css
```
Never edit `src/main/webapp/resources/css/petclinic.css` directly.

## Architecture: 3 Persistence Implementations

This project has **three different persistence layer implementations** that can be switched via Spring profiles:

1. **JPA** (default) - `src/main/java/org/springframework/samples/petclinic/repository/jpa/`
2. **JDBC** - `src/main/java/org/springframework/samples/petclinic/repository/jdbc/`
3. **Spring Data JPA** - `src/main/java/org/springframework/samples/petclinic/repository/springdatajpa/`

**Default profile:** `jpa` (hardcoded in `PetclinicInitializer.java:52`)

**Switch profiles:**
```bash
./mvnw jetty:run-war -Dspring.profiles.active=jdbc
./mvnw jetty:run-war -Dspring.profiles.active=spring-data-jpa
```

When modifying repository code, check which implementation(s) need changes. All three share the same repository interfaces in `src/main/java/org/springframework/samples/petclinic/repository/`.

## Database Profiles

**Default:** H2 in-memory database (active by default)

**Switch to MySQL:**
```bash
./mvnw jetty:run-war -P MySQL
```
Requires MySQL running on localhost:3306 with database `petclinic`, user `petclinic`, password `petclinic`.

**Switch to PostgreSQL:**
```bash
./mvnw jetty:run-war -P PostgreSQL
```
Requires PostgreSQL on localhost:5432 with database `petclinic`, user `postgres`, password `petclinic`.

Database profiles are defined in `pom.xml` profiles section (lines 520-651).

## Configuration Files

**Spring XML config** (not Spring Boot):
- `src/main/resources/spring/business-config.xml` - Service & repository layers, profile-based persistence config
- `src/main/resources/spring/mvc-core-config.xml` - Spring MVC configuration
- `src/main/resources/spring/mvc-view-config.xml` - View resolvers
- `src/main/resources/spring/datasource-config.xml` - DataSource configuration
- `src/main/resources/spring/tools-config.xml` - Caching configuration

**Application entry point:** `PetclinicInitializer.java` (Servlet 3.0+ programmatic config, replaces web.xml)

## Technology Stack

- **Java 17** minimum (enforced by maven-enforcer-plugin)
- **Maven 3.8.4+** minimum
- **Spring Framework 7.0.7** (NOT Spring Boot)
- **JSP** views (not Thymeleaf - that's the canonical Spring Boot version)
- **WAR** packaging for Jetty 11+ or Tomcat 11+
- **Hibernate 7.3.2** for JPA
- **Jakarta EE** (not javax)

## Code Style

- **Indentation:** 4 spaces for `.java` and `.xml` files (see `.editorconfig`)
- **Line endings:** LF (Unix-style)
- **Encoding:** UTF-8

## CI/CD

**Main branch:** Runs tests on Java 17 & 21, includes SonarCloud analysis
**Pull requests:** Runs tests on Java 17 & 21 (no SonarCloud)

Both workflows use `./mvnw -B verify`

## Docker

**Build and push image:**
```bash
mvn jib:build
```
Uses Google Jib with distroless Jetty base image. Image name: `springcommunity/spring-framework-petclinic`

## Common Pitfalls

1. **Don't confuse with Spring Boot PetClinic** - This is the plain Spring Framework version with XML config
2. **Profile confusion** - Persistence profile (`jpa`/`jdbc`/`spring-data-jpa`) is separate from database profile (`H2`/`MySQL`/`PostgreSQL`)
3. **CSS changes require regeneration** - Always run `./mvnw generate-resources -P css` after SCSS edits
4. **Test naming** - Tests must end with `Tests.java`, not `Test.java`
5. **Maven wrapper** - Use `./mvnw` (or `./mvnw.cmd` on Windows), not `mvn`

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, invoke the `skill` tool with `skill: "graphify"` before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
