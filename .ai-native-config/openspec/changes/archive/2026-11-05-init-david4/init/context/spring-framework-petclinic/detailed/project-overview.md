# Project Overview — Spring Framework Petclinic

Sample veterinary clinic app (fork of spring-projects/spring-petclinic) using plain Spring Framework configuration and a 3-layer architecture. Manage owners, pets, visits; list vets.

| Category | Technology | Version |
|---|---|---|
| Language | Java | 17 |
| Framework | Spring Framework | 7.0.7 |
| Web | Spring MVC, JSP/JSTL, Servlet API | 6.1.0 / JSTL 3.0 |
| Container | Tomcat (Jasper EL, provided) / Jetty plugin | 11.0.18 / 11.0.26 |
| Persistence | Spring Data (BOM) 2025.1.5, Hibernate 7.3.2, JPA 3.2.0, JDBC | |
| Databases | H2 2.4.240 (default), HSQLDB 2.7.4, MySQL driver 8.1.0, PostgreSQL 42.7.11 | |
| Cache | Caffeine | 3.2.3 |
| JSON | Jackson (tools.jackson) | 3.1.2 |
| AOP | AspectJ | 1.9.25.1 |
| Logging | SLF4J / Logback | 2.0.17 / 1.5.32 |
| Testing | JUnit Jupiter 6.0.2, Mockito 5.23, AssertJ 3.27.7, Hamcrest 3.0, JaCoCo 0.8.14 | |
| Build | Maven (wrapper), WAR packaging, version 7.0.3; Jib Docker image | |
| Front-end | Bootstrap 5.3.8, Font Awesome 4.7.0, flatpickr (webjars), SCSS via libsass plugin | |

Repository structure: monolith, single module. i18n: messages en/es/de.
