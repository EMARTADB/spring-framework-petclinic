# Component Inventory

## Controllers (web)
OwnerController, PetController, VisitController, VetController, CrashController (`/oups`).
Support: PetValidator, PetTypeFormatter.

## Services
ClinicService (interface), ClinicServiceImpl.

## Repositories
| Interface | JPA | JDBC | Spring Data JPA |
|---|---|---|---|
| OwnerRepository | JpaOwnerRepositoryImpl | JdbcOwnerRepositoryImpl | SpringDataOwnerRepository |
| PetRepository | JpaPetRepositoryImpl | JdbcPetRepositoryImpl | SpringDataPetRepository |
| VetRepository | JpaVetRepositoryImpl | JdbcVetRepositoryImpl | SpringDataVetRepository |
| VisitRepository | JpaVisitRepositoryImpl | JdbcVisitRepositoryImpl | SpringDataVisitRepository |

JDBC helpers: JdbcPet, JdbcPetRowMapper, JdbcVisitRowMapper, JdbcPetVisitExtractor, OneToManyResultSetExtractor.

## Views (JSP)
owners: findOwners, ownersList, ownerDetails, createOrUpdateOwnerForm; pets: createOrUpdatePetForm, createOrUpdateVisitForm; vets: vetList; welcome, exception.

## JSP tags
layout, htmlHeader, bodyHeader, menu, menuItem, footer, pivotal, localDate, inputField, selectField.

## Cross-cutting
CallMonitoringAspect (AOP), EntityUtils.
