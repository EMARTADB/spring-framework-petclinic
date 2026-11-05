# Graph Report - spring-framework-petclinic  (2026-11-05)

## Corpus Check
- 97 files · ~85,383 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 585 nodes · 1144 edges · 27 communities (26 shown, 1 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 185 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_.createPetParameterSource()  .getId()|.createPetParameterSource() / .getId()]]
- [[_COMMUNITY_JdbcVisitRowMapper.java  JdbcVisitRowMa|JdbcVisitRowMapper.java / JdbcVisitRowMa]]
- [[_COMMUNITY_JdbcPetRepositoryImpl.java  JdbcPetRepo|JdbcPetRepositoryImpl.java / JdbcPetRepo]]
- [[_COMMUNITY_Model  BeforeEach|Model / BeforeEach]]
- [[_COMMUNITY_NamedEntity.java  NamedEntity|NamedEntity.java / NamedEntity]]
- [[_COMMUNITY_JdbcVisitRepositoryImpl.java  JdbcVisit|JdbcVisitRepositoryImpl.java / JdbcVisit]]
- [[_COMMUNITY_JpaOwnerRepositoryImpl.java  JpaOwnerRe|JpaOwnerRepositoryImpl.java / JpaOwnerRe]]
- [[_COMMUNITY_C  ExpectedResults|C / ExpectedResults]]
- [[_COMMUNITY_Cacheable  ClinicServiceImpl.java|Cacheable / ClinicServiceImpl.java]]
- [[_COMMUNITY_JdbcVetRepositoryImpl.java  JdbcVetRepo|JdbcVetRepositoryImpl.java / JdbcVetRepo]]
- [[_COMMUNITY_ModelMap  BindingResult|ModelMap / BindingResult]]
- [[_COMMUNITY_Maven DB profiles (H2, HSQLDB, MySQL, Po|Maven DB profiles (H2, HSQLDB, MySQL, Po]]
- [[_COMMUNITY_ModelAndView  BindingResult|ModelAndView / BindingResult]]
- [[_COMMUNITY_Locale  ClinicService|Locale / ClinicService]]
- [[_COMMUNITY_Vets.java  Vets|Vets.java / Vets]]
- [[_COMMUNITY_BindingResult  ClinicService|BindingResult / ClinicService]]
- [[_COMMUNITY_AfterEach  Errors|AfterEach / Errors]]
- [[_COMMUNITY_JdbcOwnerRepositoryImpl.java  JdbcOwner|JdbcOwnerRepositoryImpl.java / JdbcOwner]]
- [[_COMMUNITY_Around  ManagedAttribute|Around / ManagedAttribute]]
- [[_COMMUNITY_AbstractDispatcherServletInitializer  F|AbstractDispatcherServletInitializer / F]]
- [[_COMMUNITY_JdbcPetVisitExtractor.java  JdbcPetVisi|JdbcPetVisitExtractor.java / JdbcPetVisi]]
- [[_COMMUNITY_GetMapping  String|GetMapping / String]]
- [[_COMMUNITY_GitHub Actions Java CI main  GitHub Ac|GitHub Actions: Java CI main / GitHub Ac]]

## God Nodes (most connected - your core abstractions)
1. `Model` - 17 edges
2. `ClinicService` - 16 edges
3. `AbstractClinicServiceTests` - 15 edges
4. `Owner` - 14 edges
5. `Pet` - 14 edges
6. `OwnerControllerTests` - 13 edges
7. `Pet` - 12 edges
8. `ClinicServiceImpl` - 12 edges
9. `Test` - 12 edges
10. `Test` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Spring PetClinic README` --describes--> `3-layer architecture (presentation/service/repository)`  [EXTRACTED]
  readme.md → ai-docs/init/context/spring-framework-petclinic/detailed/architecture.md
- `NamedEntity` --inherits--> `BaseEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java → src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java
- `Person` --inherits--> `BaseEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/Person.java → src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java
- `Pet` --inherits--> `NamedEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/Pet.java → src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java
- `PetType` --inherits--> `NamedEntity`  [EXTRACTED]
  src/main/java/org/springframework/samples/petclinic/model/PetType.java → src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java

## Import Cycles
- None detected.

## Communities (27 total, 1 thin omitted)

### Community 0 - ".createPetParameterSource() / .getId()"
Cohesion: 0.06
Nodes (23): Owner, OwnerTests, Person, AbstractClinicServiceTests, ClinicServiceJdbcTests, ClinicServiceJpaTests, ClinicServiceSpringDataJpaTests, List (+15 more)

### Community 1 - "JdbcVisitRowMapper.java / JdbcVisitRowMa"
Cohesion: 0.09
Nodes (18): JdbcVisitRowMapper, BaseEntity, Pet, PetTests, Visit, Integer, List, LocalDate (+10 more)

### Community 2 - "JdbcPetRepositoryImpl.java / JdbcPetRepo"
Cohesion: 0.08
Nodes (25): JdbcPetRepositoryImpl, JpaPetRepositoryImpl, PetRepository, SpringDataPetRepository, DataSource, JdbcClient, List, MapSqlParameterSource (+17 more)

### Community 3 - "Model / BeforeEach"
Cohesion: 0.09
Nodes (12): Model, BeforeEach, Test, Test, BeforeEach, Test, BeforeEach, Test (+4 more)

### Community 4 - "NamedEntity.java / NamedEntity"
Cohesion: 0.09
Nodes (16): NamedEntity, PetType, Specialty, Vet, VetTests, Specialty, Override, String (+8 more)

### Community 5 - "JdbcVisitRepositoryImpl.java / JdbcVisit"
Cohesion: 0.10
Nodes (20): JdbcVisitRepositoryImpl, JpaVisitRepositoryImpl, VisitRepository, SpringDataVisitRepository, DataSource, Integer, JdbcClient, List (+12 more)

### Community 6 - "JpaOwnerRepositoryImpl.java / JpaOwnerRe"
Cohesion: 0.11
Nodes (17): JpaOwnerRepositoryImpl, OwnerRepository, SpringDataOwnerRepository, Collection, EntityManager, Override, Owner, String (+9 more)

### Community 7 - "C / ExpectedResults"
Cohesion: 0.12
Nodes (13): C, ExpectedResults, JdbcPet, JdbcPetRowMapper, OneToManyResultSetExtractor, K, R, RowMapper (+5 more)

### Community 8 - "Cacheable / ClinicServiceImpl.java"
Cohesion: 0.18
Nodes (15): Cacheable, ClinicServiceImpl, Collection, Override, Owner, OwnerRepository, Pet, PetRepository (+7 more)

### Community 9 - "JdbcVetRepositoryImpl.java / JdbcVetRepo"
Cohesion: 0.12
Nodes (15): JdbcVetRepositoryImpl, JpaVetRepositoryImpl, VetRepository, SpringDataVetRepository, Collection, JdbcClient, Override, Vet (+7 more)

### Community 10 - "ModelMap / BindingResult"
Cohesion: 0.17
Nodes (14): ModelMap, BindingResult, ClinicService, Collection, GetMapping, InitBinder, ModelAttribute, Owner (+6 more)

### Community 11 - "Maven DB profiles (H2, HSQLDB, MySQL, Po"
Cohesion: 0.14
Nodes (13): Maven DB profiles (H2, HSQLDB, MySQL, PostgreSQL), 3-layer architecture (presentation/service/repository), XML Spring configuration, PetClinic Architecture, Spring PetClinic README, ClinicService, Collection, Owner (+5 more)

### Community 12 - "ModelAndView / BindingResult"
Cohesion: 0.19
Nodes (12): ModelAndView, BindingResult, ClinicService, GetMapping, InitBinder, Map, Object, Owner (+4 more)

### Community 13 - "Locale / ClinicService"
Cohesion: 0.18
Nodes (11): Locale, ClinicService, Override, PetType, String, BeforeEach, Collection, PetType (+3 more)

### Community 14 - "Vets.java / Vets"
Cohesion: 0.18
Nodes (12): Vets, ResponseBody, List, Vet, XmlElement, ClinicService, GetMapping, Map (+4 more)

### Community 15 - "BindingResult / ClinicService"
Cohesion: 0.17
Nodes (12): BindingResult, ClinicService, GetMapping, InitBinder, Map, ModelAttribute, Object, PostMapping (+4 more)

### Community 16 - "AfterEach / Errors"
Cohesion: 0.17
Nodes (10): AfterEach, Errors, ValidatorTests, Class, Object, Override, BeforeEach, Test (+2 more)

### Community 17 - "JdbcOwnerRepositoryImpl.java / JdbcOwner"
Cohesion: 0.24
Nodes (9): JdbcOwnerRepositoryImpl, Collection, DataSource, JdbcClient, List, Override, Owner, PetType (+1 more)

### Community 18 - "Around / ManagedAttribute"
Cohesion: 0.24
Nodes (6): Around, ManagedAttribute, ManagedOperation, ProceedingJoinPoint, Object, CallMonitoringAspect

### Community 19 - "AbstractDispatcherServletInitializer / F"
Cohesion: 0.31
Nodes (6): AbstractDispatcherServletInitializer, Filter, PetclinicInitializer, Override, String, WebApplicationContext

### Community 20 - "JdbcPetVisitExtractor.java / JdbcPetVisi"
Cohesion: 0.29
Nodes (6): JdbcPetVisitExtractor, Integer, JdbcPet, Override, ResultSet, Visit

### Community 21 - "GetMapping / String"
Cohesion: 0.50
Nodes (3): GetMapping, String, CrashController

## Knowledge Gaps
- **42 isolated node(s):** `String`, `Override`, `Override`, `Vet`, `String` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Pet` connect `.createPetParameterSource() / .getId()` to `JdbcPetRepositoryImpl.java / JdbcPetRepo`, `Model / BeforeEach`, `C / ExpectedResults`, `BindingResult / ClinicService`, `AfterEach / Errors`, `JdbcOwnerRepositoryImpl.java / JdbcOwner`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Why does `ClinicService` connect `Maven DB profiles (H2, HSQLDB, MySQL, Po` to `Cacheable / ClinicServiceImpl.java`, `Model / BeforeEach`, `NamedEntity.java / NamedEntity`, `Locale / ClinicService`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `BaseEntity` connect `JdbcVisitRowMapper.java / JdbcVisitRowMa` to `.createPetParameterSource() / .getId()`, `JdbcPetRepositoryImpl.java / JdbcPetRepo`, `NamedEntity.java / NamedEntity`, `JdbcVisitRepositoryImpl.java / JdbcVisit`, `JpaOwnerRepositoryImpl.java / JpaOwnerRe`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Model` (e.g. with `.testTriggerException()` and `.testInitCreationForm()`) actually correct?**
  _`Model` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `String`, `Override`, `Override` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.createPetParameterSource() / .getId()` be split into smaller, more focused modules?**
  _Cohesion score 0.06103286384976526 - nodes in this community are weakly interconnected._
- **Should `JdbcVisitRowMapper.java / JdbcVisitRowMa` be split into smaller, more focused modules?**
  _Cohesion score 0.08748615725359911 - nodes in this community are weakly interconnected._