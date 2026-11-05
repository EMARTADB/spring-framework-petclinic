# Component Inventory (quick scan, from file names)

**Controllers:** OwnerController, PetController, VisitController, VetController, CrashController
**Validators/Formatters:** PetValidator, PetTypeFormatter
**Services:** ClinicService, ClinicServiceImpl
**Repositories:** Owner/Pet/Vet/Visit interfaces; JPA, JDBC (with row mappers/extractors: JdbcPetRowMapper, JdbcVisitRowMapper, JdbcPetVisitExtractor, OneToManyResultSetExtractor, JdbcPet), Spring Data JPA variants
**JSP views:** welcome, exception, owners/{findOwners, ownersList, ownerDetails, createOrUpdateOwnerForm}, pets/{createOrUpdatePetForm, createOrUpdateVisitForm}, vets/vetList
**JSP tags (reusable UI):** layout, htmlHeader, bodyHeader, menu, menuItem, footer, pivotal, localDate, selectField, inputField
**Styling:** SCSS (petclinic, header, typography, responsive) → CSS; Bootstrap webjar
