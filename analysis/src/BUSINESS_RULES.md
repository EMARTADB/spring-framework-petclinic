# Business Rules Specification — Spring PetClinic

> **Generated:** 2026-05-29  
> **Source:** `src/main/java` · `src/main/webapp/WEB-INF` · `src/main/resources`  
> **Method:** Three parallel business-rules-extractor agents (Calculations lens · Validation lens · Lifecycle lens) + source verification  
> **Audience:** Engineers inheriting this system, QA writing acceptance tests, architects planning a rewrite

---

## Summary Table

| ID | Name | Category | Priority | Source | Confidence |
|----|------|----------|----------|--------|------------|
| RULE-001 | Entity identity: new vs. persisted | Lifecycle | P0 | `BaseEntity.java:43-45` | High |
| RULE-002 | Owner telephone: digits-only, max 10 | Validation | P0 | `Owner.java:54-57` | High |
| RULE-003 | Owner required fields (5 fields) | Validation | P1 | `Person.java:31-36`, `Owner.java:46-57` | High |
| RULE-004 | Pet name is required | Validation | P1 | `PetValidator.java:43-45` | High |
| RULE-005 | Pet name unique per owner on create | Validation | P1 | `PetController.java:79-81`, `Owner.java:125-137` | High |
| RULE-006 | Pet type required on create only | Validation | P1 | `PetValidator.java:48-50` | High |
| RULE-007 | Pet birth date is required | Validation | P1 | `PetValidator.java:53-55` | High |
| RULE-008 | Visit description is required | Validation | P1 | `Visit.java:47` | High |
| RULE-009 | Visit date defaults to today | Calculation | P1 | `Visit.java:62-64` | High |
| RULE-010 | Owner pets sorted A-Z case-insensitive | Calculation | P2 | `Owner.java:99-102` | High |
| RULE-011 | Pet visits sorted newest-first | Calculation | P2 | `Pet.java:100-103` | High |
| RULE-012 | Vet specialties sorted A-Z case-insensitive | Calculation | P2 | `Vet.java:64-66` | High |
| RULE-013 | Vet specialty count derived | Calculation | P2 | `Vet.java:69-71` | High |
| RULE-014 | "none" displayed when vet has zero specialties | Calculation | P2 | `vetList.jsp:28` | High |
| RULE-015 | Owner search: prefix (starts-with) match | Policy | P1 | `JpaOwnerRepositoryImpl.java:56-58` | High |
| RULE-016 | Empty last-name search returns ALL owners | Policy | P1 | `OwnerController.java:80-82` | High |
| RULE-017 | Single-result search auto-redirects | Policy | P1 | `OwnerController.java:90-93` | High |
| RULE-018 | Owner search: no results → validation error | Validation | P1 | `OwnerController.java:86-89` | High |
| RULE-019 | Pet types are data-driven, ordered by name | Policy | P1 | `JdbcOwnerRepositoryImpl.java:139` | High |
| RULE-020 | Vet list cached; never evicted | Policy | P0 | `ClinicServiceImpl.java:100-103` | High |
| RULE-021 | INSERT vs UPDATE decided by id nullability | Lifecycle | P0 | `BaseEntity.java:43`, `JdbcOwnerRepositoryImpl.java:124` | High |
| RULE-022 | `id` field blocked from web binding | Validation | P0 | `OwnerController.java:49-51`, `PetController.java:61` | High |
| RULE-023 | Pet linked to owner via addPet() | Lifecycle | P1 | `Owner.java:104-107` | High |
| RULE-024 | Visit is write-once (no update path) | Lifecycle | P1 | `JdbcVisitRepositoryImpl.java:62` | High |
| RULE-025 | Vets are read-only at runtime | Lifecycle | P1 | `VetController.java:42-71` | High |
| RULE-026 | Owner cascade-deletes all pets (JPA only) | Lifecycle | P0 | `Owner.java:59` | Medium |
| RULE-027 | Pet cascade-deletes all visits (JPA only) | Lifecycle | P0 | `Pet.java:55` | Medium |
| RULE-028 | No soft-delete exists for any entity | Lifecycle | P1 | schema.sql (absence) | High |
| RULE-029 | No optimistic locking / no versioning | Lifecycle | P1 | All models (absence) | High |
| RULE-030 | Date format: `yyyy/MM/dd` input, `yyyy-MM-dd` display | Calculation | P2 | `Pet.java:49`, `ownerDetails.jsp:54` | High |
| RULE-031 | Telephone max length 10 digits, no min | Validation | P1 | `Owner.java:55-57` | High |
| RULE-032 | Pet name duplicate check skipped on update | **Suspected defect** | P1 | `PetController.java:79` | High |
| RULE-033 | Pet type not re-validated on update | **Suspected defect** | P0 | `PetValidator.java:48-50` | High |
| RULE-034 | Visit date: no past/future constraint | **Suspected defect** | P1 | `VisitController.java` (absence) | High |
| RULE-035 | Owner last name stored case-insensitively | Policy | P1 | `h2/schema.sql:39` | High |
| RULE-036 | Seed reference data: 6 pet types, 3 specialties | Policy | P2 | `db/h2/data.sql` | High |

---

## CALCULATIONS

### RULE-009: Visit date defaults to today
**Category:** Calculation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Visit.java:62-64`  
**Plain English:** When a new visit is created, its date is automatically set to the current calendar day; the clinician can change it before saving.

**Specification:**
```
Given a new Visit object is instantiated
When the Visit() no-arg constructor executes
Then this.date = LocalDate.now()
And the date field is editable on the form before submission
And no minimum or maximum date boundary is enforced
```

**Parameters:**
- Date source: `LocalDate.now()` — JVM system clock, no timezone override
- Format for binding: `yyyy/MM/dd` (`@DateTimeFormat(pattern="yyyy/MM/dd")`)

**Edge cases handled:** None. `null` date is accepted by the validator (no `@NotNull` on `Visit.date`).

**Suspected defect:** The validator does not reject `null`, future dates, or dates before the pet's birth date. A visit scheduled for 2099-01-01 saves without error.

**Confidence:** High

---

### RULE-010: Owner's pets displayed sorted A-Z (case-insensitive)
**Category:** Calculation  
**Priority:** P2  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:99-102`  
**Plain English:** Whenever an owner's pets are listed — on the detail page, in forms — they appear alphabetically by pet name regardless of the order they were registered.

**Specification:**
```
Given an Owner with pets ["Zara", "basil", "Leo"] in insertion order
When owner.getPets() is called
Then the returned list is ["basil", "Leo", "Zara"] (case-insensitive A-Z)
And the list is immutable (Collections.unmodifiableList)
```

**Parameters:**
- Comparator: `Comparator.comparing(Pet::getName, String.CASE_INSENSITIVE_ORDER)`
- Return type: `Collections.unmodifiableList` — callers cannot mutate

**Edge cases handled:** Case-insensitive comparison (`"basil"` sorts before `"Leo"`).

**Confidence:** High

---

### RULE-011: Pet's visits displayed newest-first
**Category:** Calculation  
**Priority:** P2  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Pet.java:100-103`  
**Plain English:** A pet's visit history is always shown with the most recent visit at the top.

**Specification:**
```
Given a Pet with visits on 2024-01-10, 2023-06-15, 2025-03-01
When pet.getVisits() is called
Then the returned list is [2025-03-01, 2024-01-10, 2023-06-15] (descending by date)
And the list is immutable
```

**Parameters:**
- Comparator: `Comparator.comparing(Visit::getDate).reversed()`
- Storage: internal `Set<Visit>` (unordered); sorting happens on every `getVisits()` call

**Edge cases handled:** None for same-date ties (order between same-day visits is non-deterministic).

**Confidence:** High

---

### RULE-012: Vet specialties displayed A-Z (case-insensitive)
**Category:** Calculation  
**Priority:** P2  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Vet.java:64-66`  
**Plain English:** A vet's specialties appear in alphabetical order in the vet list view.

**Specification:**
```
Given a Vet with specialties ["surgery", "Dentistry", "radiology"]
When vet.getSpecialties() is called
Then the returned list is ["Dentistry", "radiology", "surgery"] (case-insensitive A-Z)
And the list is immutable
```

**Parameters:**
- Comparator: `Comparator.comparing(Specialty::getName, String.CASE_INSENSITIVE_ORDER)`

**Confidence:** High

---

### RULE-013: Vet specialty count derived from set size
**Category:** Calculation  
**Priority:** P2  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Vet.java:69-71`  
**Plain English:** The number of specialties a vet has is computed by counting the specialty set, not stored as a column.

**Specification:**
```
Given a Vet with 2 entries in the vet_specialties join table
When vet.getNrOfSpecialties() is called
Then 2 is returned (getSpecialtiesInternal().size())
```

**Parameters:** No hardcoded threshold. Zero specialties is a valid state.

**Edge cases handled:** Zero returns 0 (not null). No maximum specialty count enforced.

**Confidence:** High

---

### RULE-014: Zero specialties displayed as "none"
**Category:** Calculation  
**Priority:** P2  
**Source:** `src/main/webapp/WEB-INF/jsp/vets/vetList.jsp:28`  
**Plain English:** When a vet has no specialties, the UI shows the literal word "none" rather than a blank cell.

**Specification:**
```
Given a Vet where getNrOfSpecialties() == 0
When the vet list page renders
Then the specialties cell displays "none"

Given a Vet where getNrOfSpecialties() > 0
When the vet list page renders
Then each specialty name is displayed, comma-separated
```

**Confidence:** High

---

### RULE-030: Date formats — input vs. display differ
**Category:** Calculation  
**Priority:** P2  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Pet.java:49` (input) · `src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp:54` (display)  
**Plain English:** Dates are entered in `yyyy/MM/dd` format (slash-separated) but displayed in `yyyy-MM-dd` format (hyphen-separated) — two different formats for the same data.

**Specification:**
```
Given a user types "2020/03/08" into the birth date field
When the form submits
Then the value binds to LocalDate 2020-03-08 (via @DateTimeFormat(pattern="yyyy/MM/dd"))

Given the owner detail page renders this pet
When <pet:localDate value="${pet.birthDate}" pattern="yyyy-MM-dd"/> fires
Then the display shows "2020-03-08"
```

**Parameters:**
- Input format: `yyyy/MM/dd`
- Display format: `yyyy-MM-dd`
- Error message on parse failure: `typeMismatch.birthDate` → `"invalid date"` (`messages.properties:8`)

**Suspected defect:** Inconsistent format between input and display is a UX confusion risk. A user who copies "2020-03-08" from the detail page and pastes it into the form gets a parse error.

**Confidence:** High

---

## VALIDATIONS

### RULE-001: Entity identity state machine
**Category:** Lifecycle  
**Priority:** P0  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java:43-45`  
**Plain English:** Every domain object is either NEW (never saved, `id` is null) or PERSISTED (has a DB-assigned integer id). This single bit drives the INSERT-vs-UPDATE decision across all persistence stacks.

**Specification:**
```
Given any domain object (Owner, Pet, Visit, Vet, Specialty, PetType)
When isNew() is called
Then return true if and only if this.id == null

Given a NEW entity is passed to save()
When save() executes
Then an INSERT SQL fires and the DB assigns a generated id to this.id
And subsequent calls to isNew() return false

Given a PERSISTED entity (id != null) is passed to save()
When save() executes
Then an UPDATE SQL fires
And the id is unchanged
```

**Parameters:** `GenerationType.IDENTITY` — DB-native sequence. No application-level id generation.

**Edge cases handled:** None explicitly. An object with `id` manually set to a non-existent PK value will attempt an UPDATE that silently affects 0 rows in JDBC mode.

**Suspected defect:** JPA repository implementations (`JpaOwnerRepositoryImpl.java:73`, `JpaPetRepositoryImpl.java:58`) check `id == null` directly rather than calling `isNew()`, creating a maintenance divergence.

**Confidence:** High

---

### RULE-002: Owner telephone — numeric digits only, max 10 digits
**Category:** Validation  
**Priority:** P0  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:54-57`  
**Plain English:** A telephone number may only contain digit characters and must be no longer than 10 digits total; no separators, no country codes.

**Specification:**
```
Given an Owner form submitted with telephone = "6085551023"
When @Digits(fraction=0, integer=10) validates
Then the value is accepted (10 digit characters, no decimal)

Given telephone = "608-555-1023"
When @Digits validates
Then rejected — non-digit characters not permitted
Error message: "numeric value out of bounds (<10 digits>.<0 digits> expected)"

Given telephone = "12345678901" (11 digits)
When @Digits validates
Then rejected — exceeds integer=10
```

**Parameters:**
- `integer = 10` — maximum digit count (hardcoded)
- `fraction = 0` — no decimal portion permitted
- DB column: `VARCHAR(20)` — note: DB column is wider than the validated max; DB will accept longer values if validation is bypassed

**Edge cases handled:** `null` and empty string caught by `@NotEmpty` (RULE-003) first.

**Suspected defect:** No minimum length is enforced. A single digit `"1"` passes both `@NotEmpty` and `@Digits`. No country-code format, no area-code structure. International numbers are rejected unless they happen to be ≤10 digits.

**Confidence:** High — rule is clear and intentional. The adequacy of 10-digit max for the business is a **SME question**.

---

### RULE-003: Owner required fields (5 fields)
**Category:** Validation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Person.java:31-36`, `src/main/java/org/springframework/samples/petclinic/model/Owner.java:46-57`  
**Plain English:** An owner record cannot be saved without first name, last name, address, city, and telephone — all five fields are mandatory.

**Specification:**
```
Given an Owner form submitted with any of the following blank:
  firstName, lastName, address, city, telephone
When @NotEmpty validates (triggered by @Valid in controller)
Then the form is rejected with field-level error "is required"
And no DB write occurs
And the form re-renders with the error alongside the blank field

Given all five fields are non-empty
When validation passes
Then the owner is saved (INSERT or UPDATE)
```

**Parameters:**
- Annotation: `@NotEmpty` (Jakarta Validation) — rejects `null`, `""`, and whitespace-only strings
- Error message key: none in `messages.properties` for `@NotEmpty` — uses Jakarta Validation default → **"must not be empty"**
- DB constraint: **None** — `first_name`, `last_name`, `address`, `city`, `telephone` columns are all nullable at DB level. Validation is application-only.

**Edge cases handled:** Whitespace-only strings (`"   "`) are rejected by `@NotEmpty`.

**Suspected defect:** No `@Size(max=30)` on `firstName`/`lastName` (DB columns are `VARCHAR(30)`). A 31-character name passes application validation but causes a DB truncation/error on save.

**Confidence:** High

---

### RULE-004: Pet name is required
**Category:** Validation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/PetValidator.java:43-45`  
**Plain English:** A pet cannot be created or updated without a name.

**Specification:**
```
Given a Pet form submitted with name = "" or name = null
When PetValidator.validate() executes
Then errors.rejectValue("name", "required", "required") fires
And the form re-renders with error "is required" on the Name field

Given name = "Basil"
When PetValidator validates
Then name check passes; further checks continue
```

**Parameters:**
- Validator: `PetValidator` (Spring `Validator` interface, not Bean Validation)
- Wired via: `@InitBinder("pet")` in `PetController.java:66`
- Error code: `required` → `messages.properties:2` → **"is required"**
- DB constraint: `pets.name VARCHAR(30)` — no NOT NULL

**Edge cases handled:** `null`, `""`, and whitespace-only strings all fail `StringUtils.hasLength()`.

**Confidence:** High

---

### RULE-005: Pet name must be unique per owner on creation (case-insensitive)
**Category:** Validation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/PetController.java:79-81`, `src/main/java/org/springframework/samples/petclinic/model/Owner.java:125-137`  
**Plain English:** An owner may not register two pets with the same name. The comparison is case-insensitive. This rule applies only when creating a new pet, not when editing an existing one.

**Specification:**
```
Given Owner "John" has an existing pet named "Basil" (persisted)
When a new Pet with name = "basil" is submitted for that owner
Then owner.getPet("basil", true) finds the existing "Basil" (ignoreNew=true skips unsaved pets)
And result.rejectValue("name", "duplicate", "already exists") fires
And no INSERT occurs

Given Owner "John" has no pet named "Basil"
When a new Pet with name = "Basil" is submitted
Then owner.getPet("Basil", true) returns null
And no duplicate error fires
And INSERT proceeds

Given a PERSISTED pet named "Basil" is edited with name = "Leo" (another pet's name)
When the update form submits
Then the duplicate check IS NOT performed (pet.isNew() == false → guard skips)
And the update proceeds, creating two pets with name "Leo" for this owner
```

**Parameters:**
- Comparison: `String.toLowerCase()` on both sides — locale-default lower-case
- `ignoreNew=true` in the `getPet()` call — new (unsaved) pets are excluded from the comparison, meaning the pet being created doesn't conflict with itself

**Suspected defect:** The `pet.isNew()` guard in `PetController.java:79` means duplicate-name checking is entirely absent on updates. An edit can rename a pet to clash with a sibling. This appears unintentional — **SME confirmation required.**

**Confidence:** High (the code is unambiguous). Intent on update behavior: **Medium** — see SME questions.

---

### RULE-006: Pet type is required on creation; not re-validated on update
**Category:** Validation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/PetValidator.java:48-50`  
**Plain English:** When registering a new pet, a pet type (cat, dog, etc.) must be selected. When editing an existing pet, the type field is not re-checked — it can be cleared.

**Specification:**
```
Given a new Pet form submitted with type = null
When pet.isNew() == true AND pet.getType() == null
Then errors.rejectValue("type", "required", "required") fires
And form re-renders with "is required" on Type field

Given an existing Pet form submitted with type = null
When pet.isNew() == false
Then the type check is skipped (condition: pet.isNew() && pet.getType() == null)
And save() fires with type = null
  → In JDBC mode: NullPointerException at JdbcPetRepositoryImpl.java:113 (pet.getType().getId())
  → In JPA mode: DB constraint violation (pets.type_id NOT NULL)
```

**Parameters:**
- DB constraint: `pets.type_id INTEGER NOT NULL` — enforced at DB level regardless of profile

**Suspected defect:** The `pet.isNew()` guard creates a window where type can be cleared on edit, causing a runtime crash (JDBC) or constraint violation (JPA) rather than a user-friendly form error. **This is a bug.** See SME questions.

**Confidence:** High

---

### RULE-007: Pet birth date is required
**Category:** Validation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/PetValidator.java:53-55`  
**Plain English:** A pet's birth date must be provided when creating or updating a pet record.

**Specification:**
```
Given a Pet form submitted with birthDate = null
When PetValidator validates
Then errors.rejectValue("birthDate", "required", "required") fires
And form re-renders with "is required" on Birth Date field

Given birthDate = "2020/03/08" (valid format)
When @DateTimeFormat(pattern="yyyy/MM/dd") parses successfully
Then the LocalDate value is bound and PetValidator receives a non-null birthDate
And no birth-date error fires
```

**Parameters:**
- Parse format: `yyyy/MM/dd` (slash-separated)
- Parse failure error: `typeMismatch.birthDate` → **"invalid date"**
- No past or future date boundary

**Suspected defect:** Future birth dates are accepted without error (e.g., `2099/12/31` is valid). Birth dates predating the database's seed data or before 1900 are also accepted.

**Confidence:** High

---

### RULE-008: Visit description is required
**Category:** Validation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Visit.java:47`  
**Plain English:** Every visit must have a description; blank visits cannot be saved.

**Specification:**
```
Given a Visit form submitted with description = "" or null
When @NotEmpty validates on Visit.description
Then the form is rejected with "must not be empty" on the Description field
And no INSERT occurs

Given description = "Annual checkup and vaccinations"
When validation passes
Then saveVisit() fires and the visit is persisted
```

**Parameters:**
- Annotation: `@NotEmpty` (Jakarta Bean Validation)
- DB column: `visits.description VARCHAR(255)` — no NOT NULL at DB level
- No maximum length enforced in application layer (DB caps at 255 chars silently truncating or erroring)

**Confidence:** High

---

### RULE-018: Owner search — no results produces field error
**Category:** Validation  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:86-89`  
**Plain English:** If a last-name search finds no owners, the form is re-displayed with an error on the Last Name field rather than showing an empty list.

**Specification:**
```
Given lastName = "Nonexistent"
When findOwnerByLastName("Nonexistent%") returns empty collection
Then result.rejectValue("lastName", "notFound", "not found") fires
And the Find Owners form re-renders
And the "Last name" field shows error "has not been found"
```

**Parameters:**
- Error code: `notFound` → `messages.properties:3` → **"has not been found"**

**Confidence:** High

---

### RULE-022: `id` field blocked from web form binding
**Category:** Validation  
**Priority:** P0  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:49-51`, `src/main/java/org/springframework/samples/petclinic/web/PetController.java:61`  
**Plain English:** A client cannot supply a primary key value through a form submission; the `id` field is always stripped from inbound requests to prevent mass-assignment attacks.

**Specification:**
```
Given a POST to /owners/new with a hidden field id=999 in the request body
When @InitBinder fires dataBinder.setDisallowedFields("id")
Then the id=999 value is silently discarded
And the Owner object bound from the form has id = null
And the DB assigns a genuine auto-generated id on INSERT

Given a POST to /owners/{ownerId}/edit
When id is stripped by binder
Then ownerId from the URL path is manually re-applied via owner.setId(ownerId) at OwnerController.java:114
```

**Parameters:** Applied to both `OwnerController` (owner binding) and `PetController` (owner binding via `@InitBinder("owner")`). Visit and Vet forms do not expose an `id` field, so no binder needed.

**Confidence:** High

---

## POLICIES

### RULE-015: Owner last-name search uses prefix (starts-with) match
**Category:** Policy  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaOwnerRepositoryImpl.java:56-58`, `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryImpl.java:76-77`  
**Plain English:** Searching for owners by last name matches any owner whose last name *starts with* the entered text — not an exact match, not a contains search.

**Specification:**
```
Given owners with last names: "Davis", "Davidson", "Smith"
When user searches lastName = "Dav"
Then findOwnerByLastName returns ["Davis", "Davidson"] (both start with "Dav")
And "Smith" is not returned

Given lastName = "" (empty string)
When OwnerController sets lastName = "" (RULE-016)
Then SQL executes WHERE last_name LIKE '%' → ALL owners returned
```

**Parameters:**
- SQL: `WHERE last_name like :lastName` with parameter `lastName + "%"` (appends wildcard)
- H2 column type: `VARCHAR_IGNORECASE(30)` → search is case-insensitive on H2
- MySQL/PostgreSQL: case-sensitivity depends on collation (not guaranteed case-insensitive)

**Suspected defect:** Case-insensitivity is a side-effect of the H2 column type, not an explicit application-level choice. On MySQL with a case-sensitive collation this search would become case-sensitive — a behavioral divergence across database profiles.

**Confidence:** High for H2 behavior. **Medium** for cross-DB consistency — SME must confirm intended case-sensitivity policy.

---

### RULE-016: Empty last-name search returns all owners (no pagination)
**Category:** Policy  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:80-82`  
**Plain English:** If a user submits the Find Owner form without typing anything, all owners in the database are returned.

**Specification:**
```
Given the Find Owner form is submitted with no lastName value
When OwnerController checks: if (owner.getLastName() == null) → setLastName("")
Then findOwnerByLastName("") is called
And SQL executes: WHERE last_name LIKE '%'
And ALL owners are returned in a single, unpaginated result set
```

**Parameters:** No page size limit. No row cap. Every owner in the database is loaded into memory.

**Suspected defect:** A clinic with thousands of owners will load all of them into the Java heap on a blank search. This is a scalability boundary — no pagination, no LIMIT clause.

**Confidence:** High

---

### RULE-017: Single search result auto-redirects to owner detail
**Category:** Policy  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/OwnerController.java:90-93`  
**Plain English:** If a search finds exactly one owner, the system navigates directly to that owner's detail page, skipping the list view.

**Specification:**
```
Given lastName = "Carter"
When findOwnerByLastName returns exactly 1 Owner
Then OwnerController returns "redirect:/owners/{id}" immediately
And no ownersList.jsp is rendered

Given lastName = "Davis"
When findOwnerByLastName returns 2+ Owners
Then model attribute "selections" is set
And ownersList.jsp is rendered showing all matching owners
```

**Confidence:** High

---

### RULE-019: Pet types are data-driven, fetched ordered by name
**Category:** Policy  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryImpl.java:139`  
**Plain English:** The list of available pet types is loaded from the database, not hardcoded. Types appear in the dropdown sorted alphabetically by name.

**Specification:**
```
Given the types table contains: cat, dog, hamster, lizard, snake, bird
When findPetTypes() is called
Then SQL: SELECT id, name FROM types ORDER BY name
Then types are returned sorted: [bird, cat, dog, hamster, lizard, snake]
And this list populates the Type dropdown on the Pet form
```

**Parameters:**
- Seed data (h2/data.sql): cat, dog, lizard, bird, hamster, snake (6 types)
- No application-level cache on `findPetTypes()` — DB hit on every pet form render

**Suspected defect:** `findPetTypes()` is not cached despite being effectively static reference data. Every pet form render issues a `SELECT` to the `types` table. Adding `@Cacheable("petTypes")` would eliminate this.

**Confidence:** High

---

### RULE-020: Vet list is cached indefinitely (no eviction)
**Category:** Policy  
**Priority:** P0  
**Source:** `src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java:100-103`  
**Plain English:** The full vet roster is loaded from the database once and cached in memory for the lifetime of the application; any change to vets in the database is invisible until the application restarts.

**Specification:**
```
Given the "vets" Caffeine cache is empty (cold start or first request)
When GET /vets is called
Then vetRepository.findAll() executes a full DB read (with EAGER-loaded specialties)
And the result list is stored in the "vets" cache

Given the "vets" cache is warm
When GET /vets is called again (any number of times)
Then the DB is NOT queried; the cached list is returned

Given a new Vet row is inserted directly into the DB while the app is running
When GET /vets is called
Then the new Vet is NOT visible — no @CacheEvict exists anywhere in the codebase
And the only way to see the new Vet is application restart
```

**Parameters:**
- Cache name: `"vets"` (string literal, `ClinicServiceImpl.java:100`)
- Cache provider: Caffeine (configured via `spring-context-support`)
- Eviction policy: **none** — no TTL, no `@CacheEvict`, no `@CachePut`

**Suspected defect:** The permanent cache makes sense only if Vets are truly immutable configuration. If a "create vet" feature is ever added, this cache must gain an eviction strategy. This is a latent defect in any modernization that expands vet management.

**Confidence:** High

---

### RULE-035: Owner last name stored case-insensitively in H2
**Category:** Policy  
**Priority:** P1  
**Source:** `src/main/resources/db/h2/schema.sql:39`  
**Plain English:** In the H2 database, owner last names are stored and searched without regard to case — `"Davis"` and `"davis"` are treated identically.

**Specification:**
```
Given an Owner saved with lastName = "Davis"
When a search for lastName = "davis" executes on H2
Then the owner IS found (VARCHAR_IGNORECASE column)

Given the same data on MySQL or PostgreSQL
When a search for lastName = "davis" executes
Then case-sensitivity depends on the database/collation configuration — not guaranteed
```

**Parameters:** H2 column type: `VARCHAR_IGNORECASE(30)`. MySQL/PostgreSQL use `VARCHAR` — collation-dependent.

**Suspected defect:** The case-insensitivity guarantee is DB-specific. A migration from H2 to MySQL without a case-insensitive collation changes observable search behavior.

**Confidence:** High

---

### RULE-036: Reference data seeded at startup
**Category:** Policy  
**Priority:** P2  
**Source:** `src/main/resources/db/h2/data.sql`  
**Plain English:** Six pet types and three vet specialties are inserted into the database at application startup.

**Specification:**
```
Given a fresh database
When the application starts with the H2 profile
Then the following 6 types are inserted: cat, dog, lizard, bird, hamster, snake
And the following 3 specialties are inserted: radiology, surgery, dentistry
And the following 6 vets are inserted: Carter, Leary, Douglas, Ortega, Stevens, Jenkins
And specialty assignments are: Leary→radiology, Douglas→surgery+dentistry, Ortega→surgery, Stevens→radiology
```

**Parameters:** All values are hardcoded in `data.sql`. There is no admin UI to add types or specialties.

**Confidence:** High

---

## LIFECYCLE

### RULE-021: INSERT vs. UPDATE decided by id nullability
**Category:** Lifecycle  
**Priority:** P0  
**Source:** `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryImpl.java:124`, `src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaOwnerRepositoryImpl.java:73-79`  
**Plain English:** Whether a save operation inserts a new row or updates an existing one is determined by whether the entity's `id` field is null.

**Specification:**
```
Given an entity with id == null
When save() is called
Then INSERT SQL executes
And the DB-generated integer id is assigned to entity.id

Given an entity with id != null
When save() is called
Then UPDATE SQL executes
And the row with the matching id is updated
And id is unchanged

Given an entity with id set to a value that does not exist in the DB
When save() is called (JDBC path)
Then UPDATE SQL executes but affects 0 rows
And no error is thrown — silent data loss
```

**Parameters:** Applies to Owner, Pet, Visit (JPA: `em.persist()` vs `em.merge()`; JDBC: `isNew()` check).

**Edge cases handled:** JPA handles this via `EntityManager.persist()` (new) vs `merge()` (existing). JDBC uses `isNew()` to branch between `SimpleJdbcInsert.executeAndReturnKey()` and a `JdbcClient` UPDATE.

**Suspected defect:** The JDBC path does not verify that an UPDATE affected at least 1 row. A stale `id` that no longer exists in the DB causes a silent no-op.

**Confidence:** High

---

### RULE-023: Pet must be linked to owner via `addPet()`
**Category:** Lifecycle  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:104-107`  
**Plain English:** A pet is connected to its owner through the `addPet()` method, which sets the bidirectional relationship — both the owner's pet collection and the pet's owner reference are updated atomically.

**Specification:**
```
Given an existing Owner and a new Pet
When owner.addPet(pet) is called
Then pet is added to owner.petsInternal (Set<Pet>)
And pet.owner is set to this owner (via pet.setOwner(this))
And both sides of the JPA bidirectional relationship are consistent

Given savePet(pet) is called without prior owner.addPet()
Then in JDBC mode: NullPointerException on pet.getOwner().getId() (JdbcPetRepositoryImpl.java:114)
Then in JPA mode: pet.owner is null → DB constraint violation (owner_id NOT NULL)
```

**Parameters:**
- JPA cascade: `Owner.pets` has `CascadeType.ALL` — saving Owner can cascade-save its pets
- JDBC: no cascade — pet must be explicitly saved

**Confidence:** High

---

### RULE-024: Visit is write-once — no update or delete path exists
**Category:** Lifecycle  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcVisitRepositoryImpl.java:62`  
**Plain English:** Once a visit is saved, it cannot be modified or deleted through the application. The JDBC implementation explicitly throws an exception if an update is attempted; no web endpoint exists for update or delete on any persistence path.

**Specification:**
```
Given a saved Visit with id=42
When any code calls JdbcVisitRepository.save(visit) with visit.isNew() == false
Then UnsupportedOperationException is thrown: "Visit update not supported"

Given a saved Visit
When the user looks for an "Edit Visit" link in the UI
Then no such link exists — VisitController has no GET/POST mapping for visit update
And no delete endpoint exists

Note: JpaVisitRepositoryImpl.save() uses em.merge() and WOULD support update
if a controller endpoint existed. This creates a behavioral divergence between profiles.
```

**Parameters:**
- JDBC: update throws `UnsupportedOperationException` at `JdbcVisitRepositoryImpl.java:62`
- JPA: update would succeed silently if triggered — no explicit guard
- Spring Data JPA: update would succeed via `save()` on a managed entity

**Suspected defect:** Behavioral divergence between profiles — the "visits are immutable" invariant is enforced only in the JDBC layer. A modernization that consolidates to JPA or Spring Data JPA without adding this guard would accidentally allow visit mutation.

**Confidence:** High

---

### RULE-025: Vets are read-only at runtime
**Category:** Lifecycle  
**Priority:** P1  
**Source:** `src/main/java/org/springframework/samples/petclinic/web/VetController.java:42-71`  
**Plain English:** There is no web endpoint to create, update, or delete a vet or specialty. Vets are configuration data managed outside the application (direct DB inserts, data migration scripts).

**Specification:**
```
Given the running application
When any HTTP client requests a URL to create or edit a Vet
Then no such route exists — VetController has only GET /vets, /vets.json, /vets.xml
And Vet.addSpecialty() exists in the model but is never called from any controller
```

**Confidence:** High

---

### RULE-026: Owner cascade-deletes all pets in JPA mode
**Category:** Lifecycle  
**Priority:** P0  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Owner.java:59`  
**Plain English:** In JPA/Spring Data JPA mode, deleting an Owner will automatically delete all their pets. This cascade does not exist in the JDBC stack, creating a behavioral divergence.

**Specification:**
```
Given Owner with id=1 and pets [Basil(id=5), Leo(id=6)]
When em.remove(owner) is called in JPA mode
Then pets Basil and Leo are also deleted (CascadeType.ALL includes REMOVE)
And all of Basil's and Leo's visits are deleted (Pet also has CascadeType.ALL on visits)

Given the same scenario in JDBC mode
When JdbcOwnerRepository.delete() is called (if such a method existed)
Then the DB FK constraint fk_pets_owners would PREVENT the owner row deletion
Unless pets are manually deleted first
```

**Parameters:** `@OneToMany(cascade = CascadeType.ALL, mappedBy = "owner")` on `Owner.pets` (`Owner.java:59`).

**Edge cases handled:** No delete endpoint exists in any controller — this cascade cannot be triggered through the UI. Risk materializes only if a delete endpoint is added in a rewrite.

**Confidence:** Medium — the cascade annotation is code-evident (High). Whether this cascade behavior is *intentional* for a production clinic system requires **SME confirmation**.

---

### RULE-027: Pet cascade-deletes all visits in JPA mode
**Category:** Lifecycle  
**Priority:** P0  
**Source:** `src/main/java/org/springframework/samples/petclinic/model/Pet.java:55`  
**Plain English:** In JPA mode, deleting a Pet will automatically delete all visit records associated with that pet.

**Specification:**
```
Given Pet with id=5 and visits [2024-01-10 "Checkup", 2023-06-15 "Vaccination"]
When em.remove(pet) is called in JPA mode
Then both visit records are deleted (CascadeType.ALL)
And visit history is permanently lost

Given the same scenario in JDBC mode
Then FK constraint fk_visits_pets would prevent pet deletion unless visits deleted first
```

**Parameters:** `@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)` on `Pet.visits` (`Pet.java:55`).

**Confidence:** Medium — annotation is clear. Whether deleting visit history is acceptable business behavior requires **SME confirmation** (a real veterinary clinic would likely want to preserve medical history even after a pet record is removed).

---

### RULE-028: No soft-delete exists for any entity
**Category:** Lifecycle  
**Priority:** P1  
**Source:** `src/main/resources/db/h2/schema.sql` (absence of status/deleted columns)  
**Plain English:** There is no way to deactivate, archive, or soft-delete any record — owners, pets, visits, or vets — through the application or at the schema level. All records, once created, exist forever unless deleted at the database level directly.

**Specification:**
```
Given any domain entity in the system
When a delete operation is needed
Then no "delete" HTTP endpoint exists in any controller
And no "active", "deleted", or "archived" column exists in any table
And direct DB deletion of an Owner would be blocked by FK constraint fk_pets_owners
```

**Confidence:** High (absence is confirmed by schema and controller inspection).

---

### RULE-029: No optimistic locking / concurrent-edit protection
**Category:** Lifecycle  
**Priority:** P1  
**Source:** All model files (absence of `@Version`, absence of `version` column in schema)  
**Plain English:** Two users can edit the same owner, pet, or vet record simultaneously; the last writer's changes silently overwrite the first writer's changes with no conflict detection.

**Specification:**
```
Given User A loads Owner{id=1, telephone="6085551023"} at T=0
And User B loads Owner{id=1, telephone="6085551023"} at T=1
When User A saves telephone="6085559999" at T=2
And User B saves telephone="6085557777" at T=3
Then User B's save succeeds and overwrites User A's change
And User A's change is permanently lost — no OptimisticLockException
```

**Confidence:** High (absence confirmed).

---

## SUSPECTED DEFECTS (Pre-existing bugs requiring SME sign-off)

| ID | Rule | Defect | Severity |
|----|------|--------|----------|
| RULE-005 | Pet name unique per owner | Duplicate name check skipped on update — two pets with same name allowed via edit | Medium |
| RULE-006 | Pet type required | Type not re-validated on update — null type causes NPE (JDBC) or DB error (JPA) instead of form error | **High** |
| RULE-009 | Visit date defaults to today | Future dates accepted without error; dates before pet birth accepted | Medium |
| RULE-015 | Owner search prefix match | Case-sensitivity differs between H2 and MySQL/PostgreSQL profiles | Medium |
| RULE-016 | Empty search returns all | No pagination or row limit — full table scan on blank search | Medium |
| RULE-024 | Visit write-once | Immutability enforced only in JDBC layer — JPA would silently allow update | Medium |
| RULE-030 | Date format inconsistency | Input format (`yyyy/MM/dd`) differs from display format (`yyyy-MM-dd`) | Low |
| RULE-003 | Owner required fields | No `@Size(max)` — names > 30 chars pass validation but fail at DB column length | Medium |

---

## RULES REQUIRING SME CONFIRMATION

The following rules have confidence below High, or contain behavioral questions that only a domain expert can answer. Every P0 rule here is a **blocker** for starting a rewrite.

| Rule | Question | Risk if Wrong |
|------|----------|---------------|
| **RULE-005** | Is it intentional that duplicate-pet-name checking is skipped on update? Or is this a bug that was never noticed? | Medium — two pets with the same name under one owner causes UI confusion and potential data integrity issues |
| **RULE-006** | Should pet type be re-validated on update (i.e., prevent clearing the type via edit)? | **High** — currently causes NPE in JDBC mode; silent constraint violation in JPA |
| **RULE-002** | Is a 10-digit maximum sufficient for the target market? Should there be a minimum (e.g., 7 digits)? Should international numbers be supported? | Medium — affects any clinic with international clients |
| **RULE-015** | Should owner last-name search be case-insensitive on all database backends, not just H2? If so, must specify collation in migration scripts for MySQL/PostgreSQL | Medium — different behavior in prod vs. dev |
| **RULE-020** | What is the intended policy for vet cache eviction? Should it expire on a TTL, or is the "restart to see new vets" behavior acceptable? | Medium — affects operational SLA for any clinic that adds/removes vets |
| **RULE-026** | Is cascading delete of all pets (and their visits) when an owner is deleted the correct business behavior? Should there be an archival step? | **High** — permanent data loss of medical records |
| **RULE-027** | Is cascading delete of all visit history when a pet is deleted acceptable? A real clinic might want to retain the medical record even after the pet is removed | **High** — permanent data loss of medical records |
| **RULE-024** | Should visits ever be editable or deletable? The current "write-once" behavior may reflect a regulatory intent (audit trail) or may simply be an unimplemented feature | Medium — shapes the entire visit data model |
| **RULE-025** | How are new vets and specialties added in production — direct DB inserts, a separate admin tool, or a planned but unimplemented admin UI? `Vet.addSpecialty()` exists but is never called | Medium — affects deployment runbook |
| **RULE-016** | Should the owner search have a maximum result cap or pagination to protect against full-table scans? | Medium — scalability risk at volume |
