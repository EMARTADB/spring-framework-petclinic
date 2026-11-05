# Architecture

Monolithic 3-layer WAR.

- **Presentation** (`web`): Spring MVC annotated controllers (`@GetMapping/@PostMapping`) rendering JSP.
  Routes: `/owners/find`, `/owners`, `/owners/new`, `/owners/{ownerId}` (+`/edit`), `/owners/{ownerId}/pets/new|{petId}/edit`, `/owners/{ownerId}/pets/{petId}/visits/new`, `/owners/*/pets/{petId}/visits`, `/vets`, `/vets.json`, `/vets.xml`, `/oups`.
- **Service**: `ClinicService` / `ClinicServiceImpl`, component-scanned, `@Transactional` (`tx:annotation-driven`).
- **Repository**: one interface per aggregate, three interchangeable implementations selected by Spring profile in `business-config.xml`: `jdbc`, `jpa`, `spring-data-jpa`. JPA profiles use `LocalContainerEntityManagerFactoryBean` + Hibernate + `JpaTransactionManager`; `jdbc` uses `DataSourceTransactionManager`.
- **Configuration**: XML (`spring/*.xml`); placeholders from `data-access.properties`, filled by Maven profile properties (`jpa.database`, `jdbc.*`, `db.script`).
- **Data**: schema/data scripts per DB under `db/`; default in-memory H2.
- **Cross-cutting**: AOP `CallMonitoringAspect`, Bean Validation, `SimpleMappingExceptionResolver`, Caffeine caching, i18n.
- Domain model: Owner 1-* Pet 1-* Visit; Pet -> PetType; Vet *-* Specialty.
