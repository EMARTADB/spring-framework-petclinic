# Graph Report - spring-framework-petclinic  (2026-11-05)

## Corpus Check
- 87 files · ~83,842 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 593 nodes · 1150 edges · 29 communities
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 184 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_.createPetParameterSource()  BaseEntity|.createPetParameterSource() / BaseEntity]]
- [[_COMMUNITY_JdbcPetRepositoryImpl.java  JdbcPetRepo|JdbcPetRepositoryImpl.java / JdbcPetRepo]]
- [[_COMMUNITY_JdbcVisitRowMapper.java  JdbcVisitRowMa|JdbcVisitRowMapper.java / JdbcVisitRowMa]]
- [[_COMMUNITY_Model  BeforeEach|Model / BeforeEach]]
- [[_COMMUNITY_JdbcVisitRepositoryImpl.java  JdbcVisit|JdbcVisitRepositoryImpl.java / JdbcVisit]]
- [[_COMMUNITY_.setName()  Vet.java|.setName() / Vet.java]]
- [[_COMMUNITY_Owner.java  Owner|Owner.java / Owner]]
- [[_COMMUNITY_JpaOwnerRepositoryImpl.java  JpaOwnerRe|JpaOwnerRepositoryImpl.java / JpaOwnerRe]]
- [[_COMMUNITY_C  ExpectedResults|C / ExpectedResults]]
- [[_COMMUNITY_Cacheable  ClinicServiceImpl.java|Cacheable / ClinicServiceImpl.java]]
- [[_COMMUNITY_JdbcVetRepositoryImpl.java  JdbcVetRepo|JdbcVetRepositoryImpl.java / JdbcVetRepo]]
- [[_COMMUNITY_ModelMap  BindingResult|ModelMap / BindingResult]]
- [[_COMMUNITY_ModelAndView  BindingResult|ModelAndView / BindingResult]]
- [[_COMMUNITY_Locale  ClinicService|Locale / ClinicService]]
- [[_COMMUNITY_Vets.java  Vets|Vets.java / Vets]]
- [[_COMMUNITY_BindingResult  ClinicService|BindingResult / ClinicService]]
- [[_COMMUNITY_AfterEach  Errors|AfterEach / Errors]]
- [[_COMMUNITY_ClinicService.java  ClinicService|ClinicService.java / ClinicService]]
- [[_COMMUNITY_JdbcOwnerRepositoryImpl.java  JdbcOwner|JdbcOwnerRepositoryImpl.java / JdbcOwner]]
- [[_COMMUNITY_Around  ManagedAttribute|Around / ManagedAttribute]]
- [[_COMMUNITY_Dependabot monthly maven updates  Docke|Dependabot monthly maven updates / Docke]]
- [[_COMMUNITY_AbstractDispatcherServletInitializer  F|AbstractDispatcherServletInitializer / F]]
- [[_COMMUNITY_JdbcPetVisitExtractor.java  JdbcPetVisi|JdbcPetVisitExtractor.java / JdbcPetVisi]]
- [[_COMMUNITY_GetMapping  String|GetMapping / String]]
- [[_COMMUNITY_GitHub workflow Java CI on main (JDK 17|GitHub workflow: Java CI on main (JDK 17]]

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
- `Dependabot monthly maven updates` --references--> `Spring PetClinic Sample Application`  [INFERRED]
  .github/dependabot.yml → readme.md
- `GitHub workflow: Java CI on pull request` --references--> `SonarCloud quality analysis`  [INFERRED]
  .github/workflows/maven-build-pull-request.yml → readme.md
- `MySQL Maven profile` --references--> `MySQL setup instructions`  [EXTRACTED]
  readme.md → src/main/resources/db/mysql/petclinic_db_setup_mysql.txt
- `PostgreSQL Maven profile` --references--> `PostgreSQL setup instructions`  [EXTRACTED]
  readme.md → src/main/resources/db/postgresql/petclinic_db_setup_postgresql.txt
- `GitHub workflow: Java CI on main (JDK 17/21, Sonar)` --references--> `SonarCloud quality analysis`  [EXTRACTED]
  .github/workflows/maven-build-main.yml → readme.md

## Import Cycles
- None detected.

## Communities (29 total, 0 thin omitted)

### Community 0 - ".createPetParameterSource() / BaseEntity"
Cohesion: 0.07
Nodes (19): BaseEntity, NamedEntity, Person, PetType, Specialty, AbstractClinicServiceTests, ClinicServiceJdbcTests, ClinicServiceJpaTests (+11 more)

### Community 1 - "JdbcPetRepositoryImpl.java / JdbcPetRepo"
Cohesion: 0.08
Nodes (25): JdbcPetRepositoryImpl, JpaPetRepositoryImpl, PetRepository, SpringDataPetRepository, DataSource, JdbcClient, List, MapSqlParameterSource (+17 more)

### Community 2 - "JdbcVisitRowMapper.java / JdbcVisitRowMa"
Cohesion: 0.09
Nodes (17): JdbcVisitRowMapper, Pet, PetTests, Visit, Integer, List, LocalDate, Set (+9 more)

### Community 3 - "Model / BeforeEach"
Cohesion: 0.09
Nodes (12): Model, BeforeEach, Test, Test, BeforeEach, Test, BeforeEach, Test (+4 more)

### Community 4 - "JdbcVisitRepositoryImpl.java / JdbcVisit"
Cohesion: 0.10
Nodes (20): JdbcVisitRepositoryImpl, JpaVisitRepositoryImpl, VisitRepository, SpringDataVisitRepository, DataSource, Integer, JdbcClient, List (+12 more)

### Community 5 - ".setName() / Vet.java"
Cohesion: 0.14
Nodes (11): Vet, VetTests, Specialty, List, Set, XmlElement, BeforeEach, Test (+3 more)

### Community 6 - "Owner.java / Owner"
Cohesion: 0.13
Nodes (10): Owner, OwnerTests, List, Override, Pet, Set, String, Owner (+2 more)

### Community 7 - "JpaOwnerRepositoryImpl.java / JpaOwnerRe"
Cohesion: 0.11
Nodes (17): JpaOwnerRepositoryImpl, OwnerRepository, SpringDataOwnerRepository, Collection, EntityManager, Override, Owner, String (+9 more)

### Community 8 - "C / ExpectedResults"
Cohesion: 0.12
Nodes (13): C, ExpectedResults, JdbcPet, JdbcPetRowMapper, OneToManyResultSetExtractor, K, R, RowMapper (+5 more)

### Community 9 - "Cacheable / ClinicServiceImpl.java"
Cohesion: 0.18
Nodes (15): Cacheable, ClinicServiceImpl, Collection, Override, Owner, OwnerRepository, Pet, PetRepository (+7 more)

### Community 10 - "JdbcVetRepositoryImpl.java / JdbcVetRepo"
Cohesion: 0.12
Nodes (15): JdbcVetRepositoryImpl, JpaVetRepositoryImpl, VetRepository, SpringDataVetRepository, Collection, JdbcClient, Override, Vet (+7 more)

### Community 11 - "ModelMap / BindingResult"
Cohesion: 0.17
Nodes (14): ModelMap, BindingResult, ClinicService, Collection, GetMapping, InitBinder, ModelAttribute, Owner (+6 more)

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

### Community 17 - "ClinicService.java / ClinicService"
Cohesion: 0.20
Nodes (8): ClinicService, Collection, Owner, Pet, PetType, String, Vet, Visit

### Community 18 - "JdbcOwnerRepositoryImpl.java / JdbcOwner"
Cohesion: 0.24
Nodes (9): JdbcOwnerRepositoryImpl, Collection, DataSource, JdbcClient, List, Override, Owner, PetType (+1 more)

### Community 19 - "Around / ManagedAttribute"
Cohesion: 0.24
Nodes (6): Around, ManagedAttribute, ManagedOperation, ProceedingJoinPoint, Object, CallMonitoringAspect

### Community 20 - "Dependabot monthly maven updates / Docke"
Cohesion: 0.17
Nodes (12): Dependabot monthly maven updates, Docker image springcommunity/spring-framework-petclinic, H2 in-memory default database, Run with mvnw jetty:run-war, MySQL Maven profile, MySQL setup instructions, Spring PetClinic Sample Application, PostgreSQL Maven profile (+4 more)

### Community 21 - "AbstractDispatcherServletInitializer / F"
Cohesion: 0.31
Nodes (6): AbstractDispatcherServletInitializer, Filter, PetclinicInitializer, Override, String, WebApplicationContext

### Community 22 - "JdbcPetVisitExtractor.java / JdbcPetVisi"
Cohesion: 0.29
Nodes (6): JdbcPetVisitExtractor, Integer, JdbcPet, Override, ResultSet, Visit

### Community 23 - "GetMapping / String"
Cohesion: 0.50
Nodes (3): GetMapping, String, CrashController

### Community 24 - "GitHub workflow: Java CI on main (JDK 17"
Cohesion: 0.67
Nodes (3): GitHub workflow: Java CI on main (JDK 17/21, Sonar), GitHub workflow: Java CI on pull request, SonarCloud quality analysis

## Knowledge Gaps
- **47 isolated node(s):** `String`, `Override`, `Override`, `Vet`, `String` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Pet` connect `Owner.java / Owner` to `.createPetParameterSource() / BaseEntity`, `JdbcPetRepositoryImpl.java / JdbcPetRepo`, `Model / BeforeEach`, `C / ExpectedResults`, `BindingResult / ClinicService`, `AfterEach / Errors`, `JdbcOwnerRepositoryImpl.java / JdbcOwner`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `ClinicService` connect `ClinicService.java / ClinicService` to `Cacheable / ClinicServiceImpl.java`, `.setName() / Vet.java`, `Model / BeforeEach`, `Locale / ClinicService`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `BaseEntity` connect `.createPetParameterSource() / BaseEntity` to `JdbcPetRepositoryImpl.java / JdbcPetRepo`, `JdbcVisitRowMapper.java / JdbcVisitRowMa`, `JdbcVisitRepositoryImpl.java / JdbcVisit`, `JpaOwnerRepositoryImpl.java / JpaOwnerRe`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Model` (e.g. with `.testTriggerException()` and `.testInitCreationForm()`) actually correct?**
  _`Model` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `String`, `Override`, `Override` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.createPetParameterSource() / BaseEntity` be split into smaller, more focused modules?**
  _Cohesion score 0.07039187227866474 - nodes in this community are weakly interconnected._
- **Should `JdbcPetRepositoryImpl.java / JdbcPetRepo` be split into smaller, more focused modules?**
  _Cohesion score 0.07781649245063879 - nodes in this community are weakly interconnected._