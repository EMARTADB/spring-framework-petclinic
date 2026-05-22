# Graph Report - .  (2026-05-22)

## Corpus Check
- 90 files · ~84,437 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 384 nodes · 597 edges · 29 communities (22 shown, 7 thin omitted)
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 192 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Owner Management & Model|Owner Management & Model]]
- [[_COMMUNITY_Pet Repository & Service|Pet Repository & Service]]
- [[_COMMUNITY_Named Entity Model|Named Entity Model]]
- [[_COMMUNITY_Visit Management|Visit Management]]
- [[_COMMUNITY_Web Controllers|Web Controllers]]
- [[_COMMUNITY_Pet Web Layer|Pet Web Layer]]
- [[_COMMUNITY_Vet Repository & Service|Vet Repository & Service]]
- [[_COMMUNITY_Owner Repository Implementations|Owner Repository Implementations]]
- [[_COMMUNITY_Repository Interfaces|Repository Interfaces]]
- [[_COMMUNITY_Vet Model|Vet Model]]
- [[_COMMUNITY_JPA Implementation|JPA Implementation]]
- [[_COMMUNITY_JDBC Implementation|JDBC Implementation]]
- [[_COMMUNITY_Spring Data JPA|Spring Data JPA]]
- [[_COMMUNITY_Service Layer|Service Layer]]
- [[_COMMUNITY_Web Validation|Web Validation]]
- [[_COMMUNITY_Database Configuration|Database Configuration]]
- [[_COMMUNITY_Test Infrastructure|Test Infrastructure]]
- [[_COMMUNITY_Model Validation|Model Validation]]
- [[_COMMUNITY_Web Formatters|Web Formatters]]
- [[_COMMUNITY_Exception Handling|Exception Handling]]
- [[_COMMUNITY_Specialty Model|Specialty Model]]
- [[_COMMUNITY_Visit Model|Visit Model]]
- [[_COMMUNITY_Pet Type Model|Pet Type Model]]

## God Nodes (most connected - your core abstractions)
1. `Owner` - 14 edges
2. `OwnerControllerTests` - 13 edges
3. `Pet` - 12 edges
4. `ClinicServiceImpl` - 12 edges
5. `AbstractClinicServiceTests` - 12 edges
6. `ClinicService` - 10 edges
7. `OwnerController` - 10 edges
8. `PetController` - 10 edges
9. `Visit` - 9 edges
10. `JdbcOwnerRepositoryImpl` - 9 edges

## Surprising Connections (you probably didn't know these)
- `NamedEntity` --extends--> `BaseEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java →   _Bridges community 2 → community 8_
- `Person` --extends--> `BaseEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/Person.java →   _Bridges community 8 → community 0_
- `Visit` --extends--> `BaseEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/Visit.java →   _Bridges community 8 → community 3_
- `Owner` --extends--> `Person`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/Owner.java →   _Bridges community 2 → community 9_
- `Pet` --extends--> `NamedEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/Pet.java →   _Bridges community 2 → community 18_

## Communities (29 total, 7 thin omitted)

### Community 0 - "Owner Management & Model"
Cohesion: 0.07
Nodes (4): BaseEntity, Person, ValidatorTests, OwnerController

### Community 1 - "Pet Repository & Service"
Cohesion: 0.06
Nodes (10): JdbcPet, JdbcPetRepositoryImpl, JdbcPetRowMapper, JpaPetRepositoryImpl, Pet, PetRepository, ClinicService, SpringDataPetRepository (+2 more)

### Community 2 - "Named Entity Model"
Cohesion: 0.09
Nodes (5): NamedEntity, Owner, OwnerTests, Pet, AbstractClinicServiceTests

### Community 3 - "Visit Management"
Cohesion: 0.08
Nodes (5): JdbcVisitRepositoryImpl, JdbcVisitRowMapper, PetTests, Visit, VisitController

### Community 4 - "Web Controllers"
Cohesion: 0.10
Nodes (5): name, CrashControllerTests, OwnerControllerTests, PetControllerTests, VisitControllerTests

### Community 5 - "Pet Web Layer"
Cohesion: 0.08
Nodes (5): ClinicService, PetController, PetTypeFormatter, PetTypeFormatterTests, VetControllerTests

### Community 6 - "Vet Repository & Service"
Cohesion: 0.10
Nodes (5): JdbcVetRepositoryImpl, JpaVetRepositoryImpl, ClinicServiceImpl, SpringDataVetRepository, VetRepository

### Community 7 - "Owner Repository Implementations"
Cohesion: 0.15
Nodes (4): JdbcOwnerRepositoryImpl, JpaOwnerRepositoryImpl, OwnerRepository, SpringDataOwnerRepository

### Community 8 - "Repository Interfaces"
Cohesion: 0.11
Nodes (5): BaseEntity, OwnerRepository, PetRepository, VisitRepository, EntityUtils

### Community 9 - "Vet Model"
Cohesion: 0.22
Nodes (3): Vet, VetTests, Person

### Community 11 - "JDBC Implementation"
Cohesion: 0.25
Nodes (7): extensions, features, ghcr.io/devcontainers/features/java:1, installMaven, mavenVersion, version, image

### Community 12 - "Spring Data JPA"
Cohesion: 0.32
Nodes (3): JpaVisitRepositoryImpl, SpringDataVisitRepository, VisitRepository

### Community 16 - "Test Infrastructure"
Cohesion: 0.29
Nodes (4): AbstractClinicServiceTests, ClinicServiceJdbcTests, ClinicServiceJpaTests, ClinicServiceSpringDataJpaTests

### Community 18 - "Web Formatters"
Cohesion: 0.40
Nodes (3): PetType, Specialty, NamedEntity

### Community 19 - "Exception Handling"
Cohesion: 0.40
Nodes (5): 3-Layer Architecture Pattern, H2 In-Memory Database, MySQL Database Support, PostgreSQL Database Support, Spring PetClinic Application

### Community 20 - "Specialty Model"
Cohesion: 0.83
Nodes (4): Agent Build Instructions, JDBC Persistence Implementation, JPA Persistence Implementation, Spring Data JPA Implementation

## Knowledge Gaps
- **5 isolated node(s):** `image`, `version`, `installMaven`, `mavenVersion`, `extensions`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `name` connect `Web Controllers` to `JDBC Implementation`, `Pet Web Layer`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `ClinicServiceImpl` connect `Vet Repository & Service` to `Pet Web Layer`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `OwnerControllerTests` connect `Web Controllers` to `Owner Management & Model`, `Pet Web Layer`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `name` (e.g. with `.testTriggerException()` and `.testInitCreationForm()`) actually correct?**
  _`name` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `image`, `version`, `installMaven` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Owner Management & Model` be split into smaller, more focused modules?**
  _Cohesion score 0.07198228128460686 - nodes in this community are weakly interconnected._
- **Should `Pet Repository & Service` be split into smaller, more focused modules?**
  _Cohesion score 0.06025641025641026 - nodes in this community are weakly interconnected._