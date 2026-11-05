# Source Tree Analysis

```
spring-framework-petclinic/
├── pom.xml                      # Maven build, WAR, DB profiles (H2/HSQLDB/MySQL/PostgreSQL), css profile
├── mvnw, mvnw.cmd, .mvn/        # Maven wrapper
├── readme.md, LICENSE.txt
├── .github/workflows/           # maven-build-main.yml, maven-build-pull-request.yml
├── .devcontainer/               # devcontainer.json
├── src/
│   ├── main/
│   │   ├── java/org/springframework/samples/petclinic/
│   │   │   ├── PetclinicInitializer.java   # ENTRY POINT: servlet/web app bootstrap
│   │   │   ├── web/             # Spring MVC controllers, validator, formatter
│   │   │   ├── service/         # ClinicService + impl
│   │   │   ├── repository/      # interfaces; jpa/, jdbc/, springdatajpa/ implementations
│   │   │   ├── model/           # JPA entities
│   │   │   └── util/            # EntityUtils, CallMonitoringAspect
│   │   ├── resources/
│   │   │   ├── spring/          # XML app context config + data-access.properties
│   │   │   ├── db/{h2,hsqldb,mysql,postgresql}/  # schema.sql, data.sql
│   │   │   ├── messages/        # i18n bundles
│   │   │   └── logback.xml
│   │   └── webapp/
│   │       ├── WEB-INF/jsp/     # owners/, pets/, vets/, welcome.jsp, exception.jsp
│   │       ├── WEB-INF/tags/    # reusable JSP tags (layout, inputField, selectField, menu...)
│   │       ├── WEB-INF/jetty-web.xml
│   │       └── resources/{css,scss}/  # petclinic.css, SCSS sources
│   └── test/
│       ├── java/.../{model,service,web}/
│       ├── resources/spring/mvc-test-config.xml
│       └── jmeter/petclinic_test_plan.jmx
```

Critical folders: `web`, `service`, `repository`, `model`, `resources/spring`, `resources/db`, `webapp/WEB-INF`.
