# Spring Framework Petclinic — Business Rules Map

## Scope and evidence

This is a source-derived map of the business behavior implemented by the sole
repository discovered in this workspace, `spring-framework-petclinic`. It covers
the browser-facing owner, pet, visit, and veterinarian workflows and their
persisted relationships. It does not assert production runtime behavior,
authentication policy, or externally imposed controls.

The map is based on the prior discovery assessment and map plus the controllers,
domain objects, service façade, repositories, and H2 schema cited below. Rules
are stated only where the source enforces or directly implements them.

## Domain vocabulary and relationships

| Term | Implemented meaning | Relationship / evidence |
|---|---|---|
| Owner | A person with required first name, last name, address, city, and telephone. Telephone must contain at most ten integer digits according to Bean Validation. | An owner has zero or more pets; adding a pet establishes the pet's owner. `model/Owner.java:43-60,104-107`; `model/Person.java:27-36`. |
| Pet | A named animal with a birth date and a pet type. | A pet belongs to one owner, references one type, and has zero or more visits. `model/Pet.java:44-61`; `db/h2/schema.sql:46-54`. |
| Pet type | A persisted classification selected for a pet. | A pet's type is required by the database and by new-pet validation. `schema.sql:30-34,46-54`; `web/PetValidator.java:47-50`. |
| Visit | A dated description associated with one pet. | A new visit defaults to the current local date and must have a non-empty description; the database requires a pet reference. `model/Visit.java:33-64`; `schema.sql:57-63`. |
| Veterinarian | A person listed with zero or more specialties. | Specialty membership is many-to-many through `vet_specialties`; returned specialties are sorted case-insensitively by name. `model/Vet.java:42-75`; `schema.sql:17-28`. |

## Implemented business rules

### Owners

| ID | Rule | Behavior / outcome | Evidence |
|---|---|---|---|
| BR-OWN-01 | Owner creation requires a valid owner. | A failed `@Valid` binding re-displays the owner form; a valid owner is saved and the client is redirected to that owner's detail page. | `web/OwnerController.java:53-68`; `model/Owner.java:46-57`; `model/Person.java:30-36`. |
| BR-OWN-02 | Owner identity is server controlled. | Form binding disallows `id` for owner requests. On edit, the path `ownerId` is assigned to the submitted owner before saving. | `web/OwnerController.java:48-51,108-116`. |
| BR-OWN-03 | Owner search is by last name, including a broad search. | A missing last name is changed to an empty string before lookup. No results produce a `notFound` field error; one result redirects to its detail page; multiple results produce a selection list. | `web/OwnerController.java:76-98`. |
| BR-OWN-04 | Owner pets are presented consistently. | The owner-facing pet collection is sorted case-insensitively by pet name and returned as an unmodifiable list. | `model/Owner.java:98-102`. |

### Pets and pet types

| ID | Rule | Behavior / outcome | Evidence |
|---|---|---|---|
| BR-PET-01 | A new pet requires name, type, and birth date. | The pet validator rejects missing name, missing type for a new pet, and missing birth date. | `web/PetValidator.java:39-55`. |
| BR-PET-02 | Pet names must be unique per owner at creation time, case-insensitively. | On new-pet submission, a non-empty name matching an existing persisted pet of the loaded owner is rejected as `duplicate`. New, unsaved pets are ignored for this check. | `web/PetController.java:77-85`; `model/Owner.java:125-136`. |
| BR-PET-03 | Creating a pet attaches it to the requested owner. | The new pet is added to the loaded owner before save; `addPet` establishes the bidirectional association. A valid save redirects to that owner's detail page. | `web/PetController.java:69-89`; `model/Owner.java:104-107`. |
| BR-PET-04 | Pet types must be an existing exact-name type. | Form conversion scans the available types and returns the matching type only when its name equals the submitted text; otherwise conversion fails. | `web/PetTypeFormatter.java:54-63`. |
| BR-PET-05 | Pet visits are displayed newest first. | The pet-facing visit collection is sorted in descending visit date order and returned as an unmodifiable list. | `model/Pet.java:99-108`. |

### Visits

| ID | Rule | Behavior / outcome | Evidence |
|---|---|---|---|
| BR-VIS-01 | A visit is created for the pet named in the route. | Before each visit route handler, the application loads the `petId`, creates a new visit, and attaches that visit to the pet. | `web/VisitController.java:50-66`. |
| BR-VIS-02 | A visit description is mandatory. | A blank description fails Bean Validation and returns the visit form; valid visits are saved then redirect to the owning owner's detail page. | `model/Visit.java:44-49`; `web/VisitController.java:75-83`. |
| BR-VIS-03 | A new visit starts with today's local date. | The visit constructor assigns `LocalDate.now()`; the submitted date may subsequently be bound through the form. | `model/Visit.java:60-83`. |
| BR-VIS-04 | Visit persistence semantics must be profile-compatible. | The repository contract says save may insert or update, and JPA persists new visits or merges existing ones. The JDBC implementation explicitly rejects updates; therefore update behavior is not uniform across selectable profiles. | `repository/VisitRepository.java:34-40`; `repository/jpa/JpaVisitRepositoryImpl.java:47-54`; `repository/jdbc/JdbcVisitRepositoryImpl.java:55-64`. |

### Veterinarians

| ID | Rule | Behavior / outcome | Evidence |
|---|---|---|---|
| BR-VET-01 | Veterinarian information is a read-only listing in this application. | The available endpoints return the same wrapped veterinarian collection as HTML, JSON, or XML; no vet create or edit controller was found in the inspected web layer. | `web/VetController.java:42-70`. |
| BR-VET-02 | Veterinarian list retrieval is cached. | `findVets` is read-only transactional and cacheable under `vets`. No expiry or invalidation rule is declared in the inspected service/configuration evidence. | `service/ClinicServiceImpl.java:98-103`; discovery `assessment/ASSESSMENT.md:78`. |

## Cross-cutting execution rules

| ID | Rule | Behavior / outcome | Evidence |
|---|---|---|---|
| BR-X-01 | Web controllers use one clinic service façade. | Owner, pet, visit, and veterinarian handlers delegate persistence operations to `ClinicService`; lookup operations are declared read-only transactional and save operations transactional. | `service/ClinicServiceImpl.java:54-103`; discovery `map/MAP.md:59-68`. |
| BR-X-02 | One persistence implementation family is active per run. | `jpa` is the default; `jdbc` and `spring-data-jpa` are alternatives selected by Spring profile. Functional rules that persist data are intended to use the common repository ports, but parity must be verified where implementations differ. | discovery `map/MAP.md:70-80`; `readme.md:95-103`. |
| BR-X-03 | Relational integrity requires valid ownership/type/visit links. | The H2 schema requires `pets.owner_id`, `pets.type_id`, and `visits.pet_id` and enforces foreign keys for them. | `db/h2/schema.sql:46-64`. |

## Deliberate boundaries and unresolved policy questions

These are not requirements inferred from absence; they identify points that source inspection cannot resolve or where behavior is inconsistent.

| ID | Question / gap | Why it remains unresolved | Evidence |
|---|---|---|---|
| Q-01 | Who may view or change owner, pet, and visit data? | The inspected application declares write routes but no authentication, role, or owner-authorization rule. Any gateway or container protection is outside repository evidence. | discovery `assessment/ASSESSMENT.md:84-92`; discovery `map/MAP.md:17`. |
| Q-02 | Must pet update identity and owner relationship be verified against the route? | The update handler binds a `Pet`, does not set its ID from `petId`, and does not compare the loaded owner with the submitted pet's ownership. This is an observed safety gap, not an authorization policy. | `web/PetController.java:92-108`; discovery `assessment/ASSESSMENT.md:87`. |
| Q-03 | Are field lengths and date constraints part of the intended validation contract? | SQL defines column widths, while the inspected domain rules generally enforce presence rather than matching length limits; no past/future date rule was found. | `db/h2/schema.sql:36-62`; `model/Owner.java:46-57`; `web/PetValidator.java:39-55`. |
| Q-04 | Which persistence profile is supported in deployment and how is parity maintained? | Three profiles are documented, and visit updates behave differently in JDBC and JPA. Support policy and cross-profile contract tests were not identified. | `readme.md:95-103`; BR-VIS-04 above. |
| Q-05 | What cache freshness is required for veterinarian data? | The service caches the list but the discovered configuration has no expiry or invalidation rule. | BR-VET-02 above. |

## Traceability notes

- The repository is a Spring MVC/JSP sample with an observed presentation → service → repository structure, not a separately deployed multi-repository system. See discovery `map/MAP.md:3-17,45-80`.
- Rule identifiers in this document are documentation identifiers only; they do not claim corresponding runtime telemetry, test coverage, or external business approval.
