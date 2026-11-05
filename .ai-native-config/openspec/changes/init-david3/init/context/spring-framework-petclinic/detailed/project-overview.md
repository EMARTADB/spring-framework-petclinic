# Project Overview - Spring Framework Petclinic

**Purpose:** Sample veterinary clinic app (owners, pets, visits, vets) maintained by the Spring community with plain Spring Framework configuration (no Spring Boot) and a 3-layer architecture. Fork of spring-projects/spring-petclinic (source: readme.md).

## Summary
| Item | Value |
|---|---|
| Group / Artifact / Version | org.springframework.samples / spring-framework-petclinic / 7.0.3 |
| Packaging | war |
| Repository type | monolith, 1 part |
| Project type | web (server-rendered) |
| Java | 17 (CI matrix 17 and 21) |
| Build | Maven (wrapper `mvnw`) |

## Tech stack
| Category | Technology | Version |
|---|---|---|
| Framework | Spring Framework (MVC, tx, data) | 7.0.7 |
| Web/View | Jakarta Servlet 6.1.0, JSP, JSTL 3.0.x, custom tags, Bootstrap webjar | 5.3.8 |
| Persistence | Spring Data JPA, Hibernate, JDBC | 2025.1.5 / 7.3.2.Final |
| Databases | HSQLDB (default profile per pom profiles H2/HSQLDB/MySQL/PostgreSQL), H2, MySQL, PostgreSQL | 2.7.4 / 2.4.240 / 8.1.0 / 42.7.11 |
| Cache | Caffeine | 3.2.3 |
| AOP | AspectJ | 1.9.25.1 |
| Validation | Hibernate Validator | 9.1.0.Final |
| JSON | Jackson | 3.1.2 |
| Logging | SLF4J / Logback | 2.0.17 / 1.5.32 |
| Test | JUnit Jupiter, Mockito, AssertJ, Hamcrest, JsonPath | 6.0.2 / 5.23.0 / 3.27.7 / 3.0 / 2.10.0 |
| Container | Jib, base image jetty:11.0-jdk17 | 3.5.1 |

Links: [Architecture](./architecture.md), [Index](./index.md)
