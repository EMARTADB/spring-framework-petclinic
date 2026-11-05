# Source Tree

```
pom.xml, mvnw*            Maven build (profiles H2, HSQLDB, MySQL, PostgreSQL, css)
src/main/java/org/springframework/samples/petclinic/
  PetclinicInitializer    Servlet container bootstrap
  model/                  Entities: BaseEntity, NamedEntity, Person, Owner, Pet, PetType, Visit, Vet, Vets, Specialty
  web/                    Controllers (Owner, Pet, Visit, Vet, Crash), PetValidator, PetTypeFormatter
  service/                ClinicService + ClinicServiceImpl (transactional facade)
  repository/             Owner/Pet/Visit/Vet repository interfaces
    jpa/                  Plain JPA implementations
    jdbc/                 JDBC implementations + row mappers/extractors
    springdatajpa/        Spring Data JPA repositories
  util/                   EntityUtils, CallMonitoringAspect
src/main/resources/
  spring/                 business-config, datasource-config, mvc-core-config, mvc-view-config, tools-config, data-access.properties
  db/{h2,hsqldb,mysql,postgresql}/  schema.sql, data.sql
  messages/               i18n bundles (default, en, es, de); logback.xml
src/main/webapp/          WEB-INF/jsp (owners, pets, vets, welcome, exception), WEB-INF/tags, resources (css, scss, fonts, images)
src/test/java/            model, service (JDBC/JPA/Spring Data variants), web controller tests
src/test/resources/spring/mvc-test-config.xml; src/test/jmeter/ load test plan
.github/                  workflows, dependabot
```
