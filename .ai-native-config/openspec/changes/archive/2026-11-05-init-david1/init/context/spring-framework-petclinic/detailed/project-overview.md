# Project Overview

**Spring Framework Petclinic** (`org.springframework.samples:spring-framework-petclinic:7.0.3`, WAR) is a sample clinic-management app using plain Spring Framework XML/Java configuration (no Spring Boot), a 3-layer architecture (web -> service -> repository), JSP views, and switchable persistence.

## Tech stack
| Area | Technology |
|---|---|
| Language | Java 17 |
| Framework | Spring Framework 7.0.7, Spring MVC, Spring Data JPA 2025.1.5 |
| ORM / DB | Hibernate 7.3.2, JDBC (JdbcClient / NamedParameterJdbcTemplate), H2 (default), HSQLDB, MySQL, PostgreSQL |
| Views | JSP + JSTL, custom tags, Bootstrap 5.3.8 webjar, SCSS (`css` profile via libsass) |
| Container | Jakarta Servlet 6.1, Tomcat 11 / Jetty 11 plugin |
| Other | Caffeine cache, AspectJ (call monitoring), Jackson 3, JAXB, Logback |
| Test | JUnit Jupiter 6, Mockito, AssertJ, Hamcrest, JaCoCo, JMeter plan |
| Build | Maven (wrapper), Jib Docker image (`springcommunity`), GitHub Actions, Dependabot, SonarCloud |

## Features
Find/create/edit owners, add/edit pets, add/list visits, list vets (HTML, `/vets.json`, `/vets.xml`), error page (`/oups`), i18n (en, es, de).
