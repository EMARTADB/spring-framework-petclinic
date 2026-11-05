# Spring Framework Petclinic — Functional Documents

## Scope and evidence

This document describes business-visible behavior implemented by the sole
repository discovered in this workspace, `spring-framework-petclinic`. It is
a source-derived description of the currently implemented server-rendered web
application; it does not assert production usage, user roles, external gateway
controls, or intended future behavior.

Evidence was taken from the existing discovery assessment, map, and business
rules artifacts, and from the MVC controllers, domain model, service façade,
validation, and message resources. Routes below are HTTP browser endpoints
unless a JSON or XML representation is explicitly stated.

## Functional overview

The application supports a veterinary-clinic register in which a user can:

- search for and view animal owners;
- create and update owner records;
- register and update pets under an owner;
- record and view a pet's visits; and
- view veterinarians and their specialties in HTML, JSON, or XML.

The system stores the clinic register in one configured relational database.
The default launch profile uses an in-memory H2 database populated with schema
and sample data. JPA, JDBC, and Spring Data JPA are selectable persistence
implementations; the functional surface is shared through `ClinicService`,
but profile-specific differences are noted where observed.

## Actors and system boundary

| Actor or system | Current interaction |
|---|---|
| Browser user | Uses JSP pages and HTML forms to search, view, create, and update owners, pets, and visits; views veterinarian information. |
| API consumer | Can retrieve the veterinarian list as JSON or XML. No other JSON/XML business API was observed. |
| Servlet container | Hosts the WAR and routes requests to the Spring MVC application. |
| Relational database | Holds clinic records and initializes from vendor-specific schema and data scripts. |
| Operator or JMX client | May access exported call-monitoring data when the configured JMX integration is enabled; no repository consumer was observed. |

No authentication, authorization, roles, ownership policy, outbound service,
queue, scheduled job, or separate application repository was observed. Thus a
distinct staff, owner, or administrator actor model is not established by this
repository.

## Domain model

| Concept | Business meaning and relationships |
|---|---|
| Owner | A person with first name, last name, address, city, and telephone. An owner can have zero or more pets. |
| Pet | A named animal owned by one owner, classified by one pet type, with zero or more visits. |
| Pet type | A persisted classification selected for a pet. |
| Visit | A dated description recorded for one pet. New visits initially use the current local date. |
| Veterinarian | A person listed with zero or more specialties. |
| Specialty | A veterinarian capability/classification. Veterinarians and specialties have a many-to-many relationship. |

Owner-facing pets are displayed case-insensitively by name. A pet's visits are
displayed newest first. Veterinarian specialties are displayed
case-insensitively by name.

## Functional use cases

### UC-01 — Find owners

**Actor:** Browser user
**Routes:** `GET /owners/find`, `GET /owners`

1. The user opens the owner search form.
2. The user can submit a last name or request `/owners` without a last name.
   A missing last name is treated as an empty search string, which requests the
   broadest lookup supported by the repository.
3. The system searches owners by last name.
4. The outcome depends on the result count:
   - no match: return the search form with a `notFound` validation error;
   - one match: redirect to the owner's detail page;
   - multiple matches: show the selection list.

**Output:** Search form, a list of matching owners, or an owner-detail
redirect.
**Exceptions/limits:** Search matching semantics beyond the provided last-name
value depend on the active repository implementation; no user authorization
rule is implemented in this codebase.

### UC-02 — View owner and pet history

**Actor:** Browser user
**Route:** `GET /owners/{ownerId}`

1. The user requests a known owner identifier.
2. The system loads the owner and returns an owner-detail page.
3. The detail view receives the owner's pets and their associated information;
   pets are ordered by name and their visits are ordered by descending date.

**Output:** Owner detail page containing owner information, pets, and their
recorded visits as supplied by the selected persistence implementation.

### UC-03 — Register a new owner

**Actor:** Browser user
**Routes:** `GET /owners/new`, `POST /owners/new`

1. The user opens a blank owner form.
2. The user supplies first name, last name, address, city, and telephone.
3. The system validates that these fields are not empty; telephone must be
   numeric with no fractional part and up to ten integer digits.
4. On validation failure, the same form is returned with field errors.
5. On success, the system saves the owner and redirects to the new owner's
   detail page.

**Input handling:** Form-supplied owner `id` is disallowed, so identity is not
accepted from this form.

### UC-04 — Update an owner

**Actor:** Browser user
**Routes:** `GET /owners/{ownerId}/edit`, `POST /owners/{ownerId}/edit`

1. The user opens the existing owner's edit form.
2. The user changes owner fields and submits the form.
3. The system applies the same validation as owner creation.
4. If valid, the system assigns the route's `ownerId` to the submitted owner,
   saves it, and redirects to the owner detail page.

**Exception:** Invalid input returns the edit form. The repository provides no
observed authorization or ownership verification around the update.

### UC-05 — Register a pet for an owner

**Actor:** Browser user
**Routes:** `GET /owners/{ownerId}/pets/new`,
`POST /owners/{ownerId}/pets/new`

1. The system loads the owner and the available pet types before rendering the
   form.
2. The user supplies a pet name, pet type, and birth date (`yyyy/MM/dd`).
3. The system requires all three fields for a new pet.
4. The system rejects a non-empty name that duplicates an existing persisted
   pet name for that owner, using a case-insensitive comparison.
5. On success, the system connects the pet to the loaded owner, saves it, and
   redirects to the owner's detail page.

**Exceptions:** Missing required fields or a duplicate name return the form
with field errors. The submitted pet type must convert to an existing exact
type name.

### UC-06 — Update a pet

**Actor:** Browser user
**Routes:** `GET /owners/{ownerId}/pets/{petId}/edit`,
`POST /owners/{ownerId}/pets/{petId}/edit`

1. The user opens a pet edit form after the system loads the pet by `petId`.
2. The user submits the edited pet fields.
3. The system validates pet name and birth date; type is required only for a
   pet considered new by the bound object.
4. When valid, it adds the submitted pet to the loaded owner, saves the pet,
   and redirects to the owner detail page.

**Observed gap:** Unlike owner editing, the handler does not assign the route
`petId` to the submitted pet or verify that the loaded owner owns that pet.
This documents current behavior, not an authorization policy.

### UC-07 — Record a pet visit

**Actor:** Browser user
**Routes:** `GET /owners/*/pets/{petId}/visits/new`,
`POST /owners/{ownerId}/pets/{petId}/visits/new`

1. Before rendering or processing either visit route, the system loads the pet
   identified by the route, creates a new visit, and associates the visit with
   that pet.
2. A newly created visit starts with the current local date.
3. The user supplies the visit date and a description.
4. Description is mandatory. On failure, the system returns the visit form.
5. On success, it saves the visit and redirects to the owner's detail page.

**Profile-dependent behavior:** The common repository contract allows an
insert or update, but the JDBC implementation rejects updates while the JPA
implementation persists new visits or merges existing ones. The exposed route
only creates a new visit.

### UC-08 — View pet visits

**Actor:** Browser user
**Route:** `GET /owners/*/pets/{petId}/visits`

1. The user requests the visit list for a pet.
2. The system loads the pet and provides its visit collection to the visit-list
   view.
3. The collection is sorted with newest dates first.

### UC-09 — View veterinarians and specialties

**Actors:** Browser user; API consumer
**Routes:** `GET /vets`, `GET /vets.json`, `GET /vets.xml`

1. The system retrieves veterinarians and wraps them in a `Vets` collection.
2. It returns the same list as an HTML JSP, JSON, or XML response according to
   the requested endpoint.
3. Each veterinarian's specialties are included as available from persistence
   and ordered by specialty name.

**Read-only scope:** No veterinarian create, update, or delete web workflow was
found. Retrieval is cached under the `vets` cache name; no cache expiration or
invalidation behavior is declared.

### UC-10 — Deliberately demonstrate exception handling

**Actor:** Browser user
**Route:** `GET /oups`

The route always throws a runtime exception. MVC exception mapping directs an
unhandled exception to the application error view. This is an intentionally
implemented demonstration route, not a clinic-management workflow.

## Inputs, outputs, and validation outcomes

| Input area | Accepted/required behavior | User-visible outcome on failure |
|---|---|---|
| Owner fields | First name, last name, address, city, and telephone are required; telephone is numeric and limited to ten integer digits. | Owner creation/edit form is redisplayed with binding errors. |
| Owner search | Last name may be omitted, which becomes a broad search. | No result produces `notFound`; multiple results produce a list. |
| Pet fields | Name and birth date are required; type is required for a new pet; birth dates use `yyyy/MM/dd`. | Pet form is redisplayed with required/type/date binding errors. |
| New-pet name | Must not duplicate a persisted pet name for the requested owner, case-insensitively. | `duplicate` error on the pet name. |
| Visit fields | Description is required; date is initialized to the current local date and may be submitted in the configured date format. | Visit form is redisplayed with validation or date conversion errors. |
| Veterinarian representation | No request body; endpoint selects HTML, JSON, or XML by path. | No source-defined business error behavior was found. |

The message catalogue defines user-facing messages for required fields, not
found, duplicate values, non-numeric input, duplicate form submission, and
invalid dates. SQL column widths and any database exceptions are not fully
translated into an explicit application-level validation contract in the
reviewed sources.

## State and lifecycle

| Entity | Observable lifecycle |
|---|---|
| Owner | Blank form → validated submission → persisted owner → view/edit/searchable owner. No delete workflow was observed. |
| Pet | Blank form under an existing owner → validation and duplicate check → associated with owner and persisted → viewable/editable pet. No delete workflow was observed. |
| Visit | New visit attached to a route-selected pet with current date → description validation → persisted visit → appears in visit history. No delete workflow was observed. |
| Veterinarian | Persisted/reference information → retrieved and cached for presentation. No maintenance lifecycle was observed. |

## Cross-cutting behavior and dependencies

- Controllers delegate all domain persistence operations to the transactional
  `ClinicService` façade.
- Exactly one repository implementation family is active in a running profile:
  default `jpa`, alternative `jdbc`, or `spring-data-jpa`.
- H2 is the default in-memory database. HSQLDB, MySQL, and PostgreSQL profiles
  are available, with vendor-specific schema and seed scripts.
- The application is server-rendered using JSP views and custom tags. Static
  assets and WebJars supply UI resources.
- Owner, pet, and visit data are subject to relational foreign-key links in the
  provided schema: pet → owner, pet → type, and visit → pet.

## Explicit functional limits and unresolved questions

1. The repository contains no implemented user authentication, authorization,
   or owner-data access policy. External platform enforcement is not visible.
2. There are no observed delete workflows for owners, pets, visits, or
   veterinarians.
3. No source-derived policy constrains pet or visit dates to past or future
   ranges, or fully aligns form validation with database column lengths.
4. Persistence-profile support policy and full behavioral parity are not
   documented; the visit update difference is a known example.
5. Veterinarian cache freshness and invalidation are not specified.
6. Missing-record behavior for direct detail/edit paths depends on repository
   behavior and MVC exception handling; no dedicated not-found route outcome
   was established from the reviewed controllers.

## Traceability

- Existing discovery context: `assessment/ASSESSMENT.md`, `map/MAP.md`, and
  `business-rules/BUSINESS_RULES.md` in this change's discovery directory.
- Owner workflows: `web/OwnerController.java`; domain: `model/Owner.java` and
  `model/Person.java`.
- Pet workflows: `web/PetController.java`, `web/PetValidator.java`, and
  `model/Pet.java`.
- Visit workflows: `web/VisitController.java` and `model/Visit.java`.
- Veterinarian representations: `web/VetController.java` and `model/Vet.java`.
- Cross-cutting delegation and caching: `service/ClinicServiceImpl.java`.
- User-facing validation message keys: `messages/messages.properties`.
