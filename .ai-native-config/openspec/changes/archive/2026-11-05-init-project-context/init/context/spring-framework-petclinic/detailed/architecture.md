# Architecture — spring-framework-petclinic

## Executive summary
Servlet-container WAR application using classic Spring Framework configuration. Bootstrapped by `PetclinicInitializer` (code-based servlet initializer) which loads XML contexts from `src/main/resources/spring/`.

## Pattern
3-layer monolith (presentation → service → repository), server-side rendered JSP.

## Layers (package `org.springframework.samples.petclinic`)
- `web` — `OwnerController`, `PetController`, `VisitController`, `VetController`, `CrashController`, `PetValidator`, `PetTypeFormatter`.
- `service` — `ClinicService` interface, `ClinicServiceImpl`.
- `repository` — interfaces `OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository`; implementations in `jpa/`, `jdbc/`, `springdatajpa/`.
- `model` — entities: `BaseEntity`, `NamedEntity`, `Person`, `Owner`, `Pet`, `PetType`, `Visit`, `Vet`, `Vets`, `Specialty`.
- `util` — `EntityUtils`, `CallMonitoringAspect` (AOP call monitoring).

## Spring configuration (`src/main/resources/spring/`)
- `business-config.xml` — profile-driven beans: `jpa`, `spring-data-jpa`, `jdbc` (shared section for jpa/spring-data-jpa).
- `datasource-config.xml` — data source (incl. `javaee` profile for JNDI), `data-access.properties` for JDBC/JPA properties.
- `mvc-core-config.xml`, `mvc-view-config.xml` — MVC, view resolution.
- `tools-config.xml` — AOP/monitoring tools.
- Default persistence profile `jpa`; override with `-Dspring.profiles.active=jdbc` (per `PetclinicInitializer` comments).

## Data architecture
Relational schema per DB in `src/main/resources/db/{h2,hsqldb,mysql,postgresql}/` (`schema.sql`, `data.sql`). See [data-models](./data-models.md).

## Testing strategy
JUnit tests in `src/test/java` (model, service — JDBC/JPA/Spring Data variants sharing `AbstractClinicServiceTests`, web controller tests with `spring/mvc-test-config.xml`); JMeter plan `src/test/jmeter/petclinic_test_plan.jmx`; JaCoCo coverage.

## i18n
`messages/messages{,_en,_es,_de}.properties`.
