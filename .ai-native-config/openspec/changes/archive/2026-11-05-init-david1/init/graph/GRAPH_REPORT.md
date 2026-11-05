# Graph Report - spring-framework-petclinic  (2026-11-05)

## Corpus Check
- 93 files · ~84,839 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 589 nodes · 1148 edges · 27 communities
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 184 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_.getId()|.getId()]]
- [[_COMMUNITY_PetRepository|PetRepository]]
- [[_COMMUNITY_Model|Model]]
- [[_COMMUNITY_Pet|Pet]]
- [[_COMMUNITY_.setName()|.setName()]]
- [[_COMMUNITY_.setId()|.setId()]]
- [[_COMMUNITY_VisitRepository|VisitRepository]]
- [[_COMMUNITY_OwnerRepository|OwnerRepository]]
- [[_COMMUNITY_ClinicServiceImpl.java|ClinicServiceImpl.java]]
- [[_COMMUNITY_VetRepository|VetRepository]]
- [[_COMMUNITY_PetController|PetController]]
- [[_COMMUNITY_OwnerController|OwnerController]]
- [[_COMMUNITY_.parse()|.parse()]]
- [[_COMMUNITY_VetController.java|VetController.java]]
- [[_COMMUNITY_VisitController.java|VisitController.java]]
- [[_COMMUNITY_.validate()|.validate()]]
- [[_COMMUNITY_ClinicService|ClinicService]]
- [[_COMMUNITY_.loadPetsAndVisits()|.loadPetsAndVisits()]]
- [[_COMMUNITY_CallMonitoringAspect|CallMonitoringAspect]]
- [[_COMMUNITY_PetclinicInitializer|PetclinicInitializer]]
- [[_COMMUNITY_3-layer architecture (presentationservi|3-layer architecture (presentation/servi]]
- [[_COMMUNITY_JdbcPetVisitExtractor|JdbcPetVisitExtractor]]
- [[_COMMUNITY_.triggerException()|.triggerException()]]

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
- `Repository implementations: jdbc, jpa, spring-data-jpa` --conceptually_related_to--> `In-memory default database`  [INFERRED]
  ai-docs/init/context/spring-framework-petclinic/detailed/architecture.md → readme.md
- `Spring PetClinic readme` --references--> `MySQL setup guide`  [EXTRACTED]
  readme.md → src/main/resources/db/mysql/petclinic_db_setup_mysql.txt
- `Spring PetClinic readme` --references--> `PostgreSQL setup guide`  [EXTRACTED]
  readme.md → src/main/resources/db/postgresql/petclinic_db_setup_postgresql.txt
- `Spring PetClinic readme` --describes--> `3-layer architecture (presentation/service/repository)`  [EXTRACTED]
  readme.md → ai-docs/init/context/spring-framework-petclinic/detailed/architecture.md
- `Project context for AI agents` --conceptually_related_to--> `3-layer architecture (presentation/service/repository)`  [INFERRED]
  ai-docs/init/context/spring-framework-petclinic/project-context.md → ai-docs/init/context/spring-framework-petclinic/detailed/architecture.md

## Import Cycles
- None detected.

## Communities (27 total, 0 thin omitted)

### Community 0 - ".getId()"
Cohesion: 0.06
Nodes (23): BaseEntity, Owner, OwnerTests, Person, AbstractClinicServiceTests, ClinicServiceJdbcTests, ClinicServiceJpaTests, ClinicServiceSpringDataJpaTests (+15 more)

### Community 1 - "PetRepository"
Cohesion: 0.08
Nodes (25): JdbcPetRepositoryImpl, JpaPetRepositoryImpl, PetRepository, SpringDataPetRepository, DataSource, JdbcClient, List, MapSqlParameterSource (+17 more)

### Community 2 - "Model"
Cohesion: 0.09
Nodes (12): Model, BeforeEach, Test, Test, BeforeEach, Test, BeforeEach, Test (+4 more)

### Community 3 - "Pet"
Cohesion: 0.10
Nodes (14): Pet, PetTests, Visit, List, LocalDate, Owner, PetType, Set (+6 more)

### Community 4 - ".setName()"
Cohesion: 0.10
Nodes (15): NamedEntity, PetType, Specialty, Vet, VetTests, Specialty, Override, String (+7 more)

### Community 5 - ".setId()"
Cohesion: 0.09
Nodes (18): C, ExpectedResults, JdbcPet, JdbcPetRowMapper, JdbcVisitRowMapper, OneToManyResultSetExtractor, K, R (+10 more)

### Community 6 - "VisitRepository"
Cohesion: 0.10
Nodes (20): JdbcVisitRepositoryImpl, JpaVisitRepositoryImpl, VisitRepository, SpringDataVisitRepository, DataSource, Integer, JdbcClient, List (+12 more)

### Community 7 - "OwnerRepository"
Cohesion: 0.11
Nodes (17): JpaOwnerRepositoryImpl, OwnerRepository, SpringDataOwnerRepository, Collection, EntityManager, Override, Owner, String (+9 more)

### Community 8 - "ClinicServiceImpl.java"
Cohesion: 0.18
Nodes (15): Cacheable, ClinicServiceImpl, Collection, Override, Owner, OwnerRepository, Pet, PetRepository (+7 more)

### Community 9 - "VetRepository"
Cohesion: 0.12
Nodes (15): JdbcVetRepositoryImpl, JpaVetRepositoryImpl, VetRepository, SpringDataVetRepository, Collection, JdbcClient, Override, Vet (+7 more)

### Community 10 - "PetController"
Cohesion: 0.17
Nodes (14): ModelMap, BindingResult, ClinicService, Collection, GetMapping, InitBinder, ModelAttribute, Owner (+6 more)

### Community 11 - "OwnerController"
Cohesion: 0.19
Nodes (12): ModelAndView, BindingResult, ClinicService, GetMapping, InitBinder, Map, Object, Owner (+4 more)

### Community 12 - ".parse()"
Cohesion: 0.18
Nodes (11): Locale, ClinicService, Override, PetType, String, BeforeEach, Collection, PetType (+3 more)

### Community 13 - "VetController.java"
Cohesion: 0.18
Nodes (12): Vets, ResponseBody, List, Vet, XmlElement, ClinicService, GetMapping, Map (+4 more)

### Community 14 - "VisitController.java"
Cohesion: 0.17
Nodes (12): BindingResult, ClinicService, GetMapping, InitBinder, Map, ModelAttribute, Object, PostMapping (+4 more)

### Community 15 - ".validate()"
Cohesion: 0.17
Nodes (10): AfterEach, Errors, ValidatorTests, Class, Object, Override, BeforeEach, Test (+2 more)

### Community 16 - "ClinicService"
Cohesion: 0.20
Nodes (8): ClinicService, Collection, Owner, Pet, PetType, String, Vet, Visit

### Community 17 - ".loadPetsAndVisits()"
Cohesion: 0.24
Nodes (9): JdbcOwnerRepositoryImpl, Collection, DataSource, JdbcClient, List, Override, Owner, PetType (+1 more)

### Community 18 - "CallMonitoringAspect"
Cohesion: 0.24
Nodes (6): Around, ManagedAttribute, ManagedOperation, ProceedingJoinPoint, Object, CallMonitoringAspect

### Community 19 - "PetclinicInitializer"
Cohesion: 0.31
Nodes (6): AbstractDispatcherServletInitializer, Filter, PetclinicInitializer, Override, String, WebApplicationContext

### Community 20 - "3-layer architecture (presentation/servi"
Cohesion: 0.20
Nodes (11): Cross-cutting: AOP, validation, caching, i18n, Domain model Owner-Pet-Visit, Vet-Specialty, In-memory default database, MySQL setup guide, Spring PetClinic readme, PostgreSQL setup guide, Repository implementations: jdbc, jpa, spring-data-jpa, Project context for AI agents (+3 more)

### Community 21 - "JdbcPetVisitExtractor"
Cohesion: 0.29
Nodes (6): JdbcPetVisitExtractor, Integer, JdbcPet, Override, ResultSet, Visit

### Community 22 - ".triggerException()"
Cohesion: 0.50
Nodes (3): GetMapping, String, CrashController

## Knowledge Gaps
- **43 isolated node(s):** `String`, `Override`, `Override`, `Vet`, `String` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Pet` connect `.getId()` to `PetRepository`, `Model`, `.setId()`, `VisitController.java`, `.validate()`, `.loadPetsAndVisits()`?**
  _High betweenness centrality (0.159) - this node is a cross-community bridge._
- **Why does `ClinicService` connect `ClinicService` to `ClinicServiceImpl.java`, `Model`, `.parse()`, `.setName()`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `BaseEntity` connect `.getId()` to `PetRepository`, `Pet`, `.setName()`, `.setId()`, `VisitRepository`, `OwnerRepository`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Model` (e.g. with `.testTriggerException()` and `.testInitCreationForm()`) actually correct?**
  _`Model` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `String`, `Override`, `Override` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.getId()` be split into smaller, more focused modules?**
  _Cohesion score 0.06376811594202898 - nodes in this community are weakly interconnected._
- **Should `PetRepository` be split into smaller, more focused modules?**
  _Cohesion score 0.08130081300813008 - nodes in this community are weakly interconnected._