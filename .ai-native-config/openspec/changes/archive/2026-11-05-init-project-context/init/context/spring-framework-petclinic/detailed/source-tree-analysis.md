# Source Tree Analysis

```
spring-framework-petclinic/
├── pom.xml                      # Maven build, WAR, DB profiles (H2/HSQLDB/MySQL/PostgreSQL, css)
├── mvnw, mvnw.cmd, .mvn/        # Maven wrapper
├── readme.md, LICENSE.txt
├── .github/                     # workflows (main, pull request), dependabot
├── .devcontainer/               # devcontainer.json
├── src/main/java/.../petclinic/
│   ├── PetclinicInitializer.java  # ENTRY POINT: servlet/web app initializer
│   ├── model/                   # domain entities
│   ├── service/                 # ClinicService + impl
│   ├── repository/              # interfaces + jpa/, jdbc/, springdatajpa/
│   ├── web/                     # Spring MVC controllers, validator, formatter
│   └── util/                    # EntityUtils, CallMonitoringAspect
├── src/main/resources/
│   ├── spring/                  # XML bean configs + data-access.properties
│   ├── db/{h2,hsqldb,mysql,postgresql}/  # schema.sql, data.sql
│   ├── messages/                # i18n bundles (en, es, de)
│   └── logback.xml
├── src/main/webapp/             # WEB-INF/jsp, tags, jetty-web.xml; resources/ css, scss, fonts
└── src/test/                    # java tests, spring/mvc-test-config.xml, jmeter plan
```
Also present (not project source): `_bmad/`, `ai-docs/`, `graphify-out/`, `.ai-native-config/`.
