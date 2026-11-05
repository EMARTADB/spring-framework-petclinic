# Source Tree Analysis

```
spring-framework-petclinic/
├── pom.xml                      # Maven build, DB profiles (H2/HSQLDB/MySQL/PostgreSQL), css profile
├── mvnw, mvnw.cmd, .mvn/        # Maven wrapper
├── readme.md
├── .github/workflows/           # CI: maven-build-main.yml, maven-build-pull-request.yml
├── .devcontainer/               # devcontainer.json
└── src/
    ├── main/
    │   ├── java/org/springframework/samples/petclinic/
    │   │   ├── PetclinicInitializer.java   # ENTRY POINT (servlet bootstrap)
    │   │   ├── model/                      # JPA entities / domain
    │   │   ├── service/                    # ClinicService(+Impl)
    │   │   ├── repository/{jpa,jdbc,springdatajpa}/  # 3 repository implementations
    │   │   ├── web/                        # MVC controllers, validator, formatter
    │   │   └── util/                       # AOP aspect, helpers
    │   ├── resources/
    │   │   ├── spring/                     # XML Spring config + data-access.properties
    │   │   ├── db/{h2,hsqldb,mysql,postgresql}/  # schema.sql, data.sql
    │   │   ├── messages/                   # i18n bundles (en, es, de)
    │   │   └── logback.xml
    │   └── webapp/
    │       ├── WEB-INF/{jsp,tags}, jetty-web.xml
    │       └── resources/{css,scss,fonts}
    └── test/
        ├── java/.../{model,service,web}/
        ├── resources/spring/mvc-test-config.xml
        └── jmeter/petclinic_test_plan.jmx
```
