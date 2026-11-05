# Architecture - Spring Framework Petclinic

## Executive Summary
Single deployable WAR: server-rendered Spring MVC web app over a service layer and a swappable repository layer. Configuration is XML-based (`src/main/resources/spring/`), bootstrapped by `PetclinicInitializer`.

## Architecture Pattern
Layered (presentation -> service -> repository), pattern inferred from package names and readme.

| Layer | Package (`org.springframework.samples.petclinic`) | Contents |
|---|---|---|
| Web | `web` | OwnerController, PetController, VisitController, VetController, CrashController, PetValidator, PetTypeFormatter |
| Service | `service` | ClinicService, ClinicServiceImpl |
| Repository | `repository` | Interfaces OwnerRepository, PetRepository, VetRepository, VisitRepository; implementations in `jpa`, `jdbc`, `springdatajpa` |
| Model | `model` | BaseEntity, NamedEntity, Person, Owner, Pet, PetType, Visit, Vet, Vets, Specialty |
| Util | `util` | EntityUtils, CallMonitoringAspect (AOP monitoring) |

## Configuration (XML)
- `business-config.xml` - services, repositories, transactions
- `datasource-config.xml` - data source and schema/data init (`jdbc.initLocation`, `jdbc.dataLocation`)
- `mvc-core-config.xml`, `mvc-view-config.xml` - MVC and view resolution
- `tools-config.xml` - tooling (e.g. monitoring aspect)
- `data-access.properties` - placeholders filled by Maven profile (`db.script`, `jdbc.*`, `jpa.database`)
- `logback.xml`, `messages/messages*.properties` (default, en, es, de - i18n)

## Data Architecture
7 tables; see [Data Models](./data-models.md). Per-DB scripts under `src/main/resources/db/{h2,hsqldb,mysql,postgresql}`.

## API Design
Server-rendered HTML routes plus `/vets.json` and `/vets.xml`; see [API Contracts](./api-contracts.md).

## Source Tree
See [Source Tree Analysis](./source-tree-analysis.md).

## Development / Deployment
See [Development Guide](./development-guide.md), [Deployment Guide](./deployment-guide.md).

## Testing Strategy
JUnit tests in `src/test/java` mirroring packages: `model`, `service` (AbstractClinicServiceTests with Jdbc, Jpa, SpringDataJpa variants), `web` (controller tests using `src/test/resources/spring/mvc-test-config.xml`). JMeter plan: `src/test/jmeter/petclinic_test_plan.jmx`. JaCoCo coverage and SonarCloud analysis.
