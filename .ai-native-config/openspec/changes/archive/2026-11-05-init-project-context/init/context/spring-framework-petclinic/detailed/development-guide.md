# Development Guide

**Prerequisites:** JDK 17+, Maven (or `./mvnw`). Docker optional.

- Run: `./mvnw jetty:run-war` → http://localhost:8080/ (default in-memory H2).
- Other DBs: `./mvnw jetty:run-war -P MySQL` (or `PostgreSQL`, `HSQLDB`); check properties in the profile in `pom.xml` (`jpa.database`, `jdbc.driverClassName`, `jdbc.url`...).
- Persistence layer: default Spring profile `jpa`; use `-Dspring.profiles.active=jdbc` or `spring-data-jpa`.
- Build/test: `./mvnw -B verify` (surefire + JaCoCo; Enforcer checks Maven version).
- CSS: SCSS compiled with the `css` Maven profile (libsass).
- Docker: `docker run -p 8080:8080 springcommunity/spring-framework-petclinic`; image built with Jib.
- Dev container: `.devcontainer/devcontainer.json`.
- Conventions: `.editorconfig`; UTF-8 sources. No CONTRIBUTING file found.
