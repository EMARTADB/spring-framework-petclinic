# Development Guide

- Prereqs: JDK 17+, Maven (wrapper provided; Maven enforcer active).
- Run: `./mvnw jetty:run-war` -> http://localhost:8080/
- DB profiles: `-P H2` (default), `HSQLDB`, `MySQL`, `PostgreSQL` (setup notes in `src/main/resources/db/<db>/*setup*.txt`); `-P css` compiles SCSS.
- Persistence layer: choose Spring profile `jdbc`, `jpa` or `spring-data-jpa`.
- Test: `./mvnw test` (JaCoCo coverage; service tests run per persistence variant; controller tests use `mvc-test-config.xml`).
- Docker: `docker run -p 8080:8080 springcommunity/spring-framework-petclinic`; image built with Jib.
- CI: GitHub Actions (`.github/workflows`), Dependabot, SonarCloud.
