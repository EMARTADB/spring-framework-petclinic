# Project Overview — Spring Framework Petclinic

- **Repository:** spring-framework-petclinic (monolith, single part, type: backend/web MVC, WAR)
- **Purpose:** Spring community sample of the Petclinic app using plain Spring Framework XML/Java configuration (no Spring Boot) and a 3-layer architecture (presentation → service → repository). Source: `readme.md`, `pom.xml`.
- **Scan level:** quick (manifests, config, directory structure only; no source bodies read)

## Tech stack

| Category | Technology | Version |
|---|---|---|
| Language | Java | 17 |
| Build | Maven (wrapper `mvnw`), packaging `war` | artifact 7.0.3 |
| Framework | Spring Framework (MVC) | 7.0.7 |
| Data | Spring Data JPA (BOM 2025.1.5), Hibernate 7.3.2.Final, JDBC, JPA API 3.2.0 | |
| Validation | Hibernate Validator | 9.1.0.Final |
| View | JSP + JSTL + custom tags, Bootstrap 5.3.8 (webjar), Font Awesome 4.7.0, flatpickr | |
| DB | H2 (default, in-memory), HSQLDB, MySQL, PostgreSQL | h2 2.4.240 |
| Cache | Caffeine | 3.2.3 |
| JSON | Jackson (tools.jackson) | 3.1.2 |
| AOP | AspectJ | 1.9.25.1 |
| Servlet | Jakarta Servlet 6.1.0, Tomcat 11.0.18 (jasper-el), Jetty plugin 11.0.26 | |
| Logging | SLF4J / Logback | 2.0.17 / 1.5.32 |
| Test | JUnit Jupiter 6.0.2, Mockito 5.23.0, AssertJ 3.27.7, Hamcrest 3.0, JsonPath 2.10.0 | |
| Quality | JaCoCo 0.8.14, SonarCloud, Maven Enforcer | |
| Container | Jib Maven plugin 3.5.1 (image prefix `springcommunity`) | |

## Architecture
Layered monolith: `web` (controllers) → `service` (`ClinicService`) → `repository` (3 interchangeable implementations selected by Spring profile: `jpa` (default), `spring-data-jpa`, `jdbc`).

See: [index](./index.md), [architecture](./architecture.md), [source tree](./source-tree-analysis.md), [development guide](./development-guide.md), [deployment guide](./deployment-guide.md), [API contracts](./api-contracts.md), [data models](./data-models.md), [component inventory](./component-inventory.md).
