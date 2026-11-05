# Development Guide

## Prerequisites
JDK 17 (CI also tests 21); Maven wrapper provided. Docker optional.

## Run
```
./mvnw jetty:run-war        # http://localhost:8080/
```
Dev container available in `.devcontainer/`.

## Database profiles (pom.xml)
`H2`, `HSQLDB`, `MySQL`, `PostgreSQL` select `db.script` and JDBC properties filtered into `data-access.properties`. Activate with `-P<name>`; the default activation is defined in pom.xml.

## Build / test
```
./mvnw clean package        # builds WAR
./mvnw verify               # tests + JaCoCo
```
Tests: JUnit 6 / Mockito / AssertJ; service tests run against Jdbc, Jpa and SpringDataJpa implementations.

## CSS
Profile `css` compiles SCSS (libsass-maven-plugin) in `src/main/webapp/resources/scss` to `css/petclinic.css`.

## Conventions
`.editorconfig` governs formatting; maven-enforcer plugin is configured. No CONTRIBUTING file found.
