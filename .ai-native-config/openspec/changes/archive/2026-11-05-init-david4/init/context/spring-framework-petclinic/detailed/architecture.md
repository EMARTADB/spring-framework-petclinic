# Architecture

## Executive Summary
Layered Spring MVC WAR application. Configuration via XML files in `src/main/resources/spring/` and `PetclinicInitializer` bootstrap.

## Layers
- **Presentation** (`web`): controllers `OwnerController`, `PetController`, `VisitController`, `VetController`, `CrashController`; `PetValidator`, `PetTypeFormatter`; JSP views in `WEB-INF/jsp`, JSP tags in `WEB-INF/tags`.
- **Service** (`service`): `ClinicService` / `ClinicServiceImpl`.
- **Repository** (`repository`): interfaces `OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository` with three implementations: `jpa`, `jdbc`, `springdatajpa` (selected via Spring config/profile).
- **Model** (`model`): `BaseEntity`, `NamedEntity`, `Person`, `Owner`, `Pet`, `PetType`, `Visit`, `Vet`, `Vets`, `Specialty`.
- **Util**: `CallMonitoringAspect` (AOP monitoring), `EntityUtils`.

## Configuration files
`mvc-core-config.xml`, `mvc-view-config.xml`, `business-config.xml`, `datasource-config.xml`, `tools-config.xml`, `data-access.properties` (placeholders filled by Maven profiles), `logback.xml`.

## Data Architecture
See [data-models.md](./data-models.md). DB chosen by Maven profile (H2 default, HSQLDB, MySQL, PostgreSQL) which sets `db.script`, `jpa.database`, `jdbc.*`.

## API Design
See [api-contracts.md](./api-contracts.md).

## Testing Strategy
JUnit tests in `src/test/java`: model tests, service tests per repository flavor (`ClinicServiceJdbcTests`, `...JpaTests`, `...SpringDataJpaTests` over `AbstractClinicServiceTests`), controller tests with Spring MVC test config (`src/test/resources/spring/mvc-test-config.xml`); JMeter plan `src/test/jmeter/petclinic_test_plan.jmx`. JaCoCo coverage; SonarCloud on main.

## Deployment
See [deployment-guide.md](./deployment-guide.md).
