# Development Guide

**Prerequisites:** JDK 17, Docker (optional). Maven via wrapper.

**Run:** `./mvnw jetty:run-war` (Windows: `./mvnw.cmd jetty:run-war`) → http://localhost:8080/
**Other DB:** `./mvnw jetty:run-war -P MySQL` (or `PostgreSQL`, `HSQLDB`; default `H2`). Check properties in the profile in `pom.xml` (jpa.database, jdbc.driverClassName, jdbc.url, ...). MySQL/PostgreSQL setup notes in `src/main/resources/db/<db>/petclinic_db_setup_*.txt`.
**Build/Test:** `./mvnw -B verify` (surefire + JaCoCo; enforcer plugin active).
**CSS:** SCSS compiled via the `css` profile (libsass plugin).
**Contributing:** no CONTRIBUTING file found; issues at the GitHub tracker referenced in readme.
