# 1. Introduction and Scope

## 1.1 Purpose

**Spring Framework PetClinic** is a web-based veterinary clinic management application that demonstrates a reference implementation of a 3-layer enterprise architecture using plain Spring Framework (not Spring Boot). The application showcases enterprise-grade patterns and practices for managing pet owners, their animals, veterinary staff, and clinic visits.

The primary purpose is to serve as a **sample application and educational resource** for:
- Spring Framework development patterns (version 7.0.7)
- Layered architecture design with separation of concerns
- Multiple persistence layer implementations (JPA, JDBC, Spring Data JPA)
- Integration with various relational databases
- Test-driven development practices

## 1.2 Overview of the Application

### 1.2.1 Core Domain

The application manages the following key domain entities:

- **Owner**: Represents pet owners in the clinic system, with contact information and associated pets
- **Pet**: Represents individual animals owned by clinic patrons, with attributes such as name, birth date, and pet type
- **PetType**: Enumeration of pet classifications (e.g., dog, cat, bird)
- **Vet**: Represents veterinary professionals on staff with associated specialties
- **Specialty**: Enumeration of veterinary specialties (e.g., surgery, radiology, dentistry)
- **Visit**: Records individual clinic visits for specific pets, tracking visit dates and descriptions

### 1.2.2 Business Capabilities

The application provides the following user-facing capabilities:

1. **Owner Management**
   - Find owners by last name (search functionality)
   - Create new owner records
   - View owner details and associated pets
   - Update owner information

2. **Pet Management**
   - Register new pets for existing owners
   - Update pet information (name, birth date, pet type)
   - View pet history and associated visits

3. **Veterinarian Management**
   - Browse available veterinarians
   - View veterinarian specialties
   - Display veterinarians in multiple formats (HTML, XML/JSON)

4. **Visit Management**
   - Schedule new visits for pets
   - Record visit descriptions
   - Associate visits with appropriate veterinarians
   - View visit history for specific pets

### 1.2.3 Technical Presentation

The application is delivered as:
- A **WAR-packaged web application** deployable on Jetty 11+ or Tomcat 11+
- **JSP-based views** with custom tag libraries (not Thymeleaf)
- **Spring MVC** for request handling and view resolution
- **Bootstrap 5** and **Font Awesome** for responsive UI styling

## 1.3 System Architecture

### 1.3.1 Layered Architecture

The application implements a classic 3-layer architecture:

```
┌─────────────────────────────────────────┐
│    Presentation Layer (Spring MVC)      │
│  - Controllers (Owner, Pet, Vet, Visit) │
│  - JSP Views                            │
│  - Request Handling & Validation        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Service Layer (Business Logic)         │
│  - ClinicService (Primary Service)      │
│  - Transaction Management               │
│  - Caching (Caffeine-based)             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Repository Layer (Persistence Access)  │
│  - OwnerRepository                      │
│  - PetRepository                        │
│  - PetTypeRepository                    │
│  - VetRepository                        │
│  - VisitRepository                      │
└─────────────────────────────────────────┘
```

### 1.3.2 Persistence Layer Implementations

The application supports **three pluggable persistence implementations**, selectable via Spring profiles:

1. **JPA (Default)**
   - Location: `src/main/java/org/springframework/samples/petclinic/repository/jpa/`
   - Implementation: Hibernate 7.3.2 with Jakarta EE JPA API 3.2
   - Approach: ORM-based persistence using entity annotations

2. **JDBC**
   - Location: `src/main/java/org/springframework/samples/petclinic/repository/jdbc/`
   - Implementation: Spring JDBC Template and Named Parameter JDBC Template
   - Approach: Template-based SQL execution with manual mapping

3. **Spring Data JPA**
   - Location: `src/main/java/org/springframework/samples/petclinic/repository/springdatajpa/`
   - Implementation: Spring Data JPA 2025.1.5
   - Approach: Interface-based repository definitions with automatic implementation

**Default Profile**: `jpa` (hardcoded in `PetclinicInitializer.java:52`)

**Activation**: Profiles can be switched via Maven property `-Dspring.profiles.active=<profile>`

### 1.3.3 Data Access Layer

All persistence implementations conform to a common repository interface contract:
- `OwnerRepository`: CRUD operations for Owner entities
- `PetRepository`: CRUD operations for Pet entities
- `PetTypeRepository`: Read-only access to pet types
- `VetRepository`: Read-only access to veterinarian records
- `VisitRepository`: CRUD operations for Visit records

## 1.4 Technology Stack

### 1.4.1 Core Framework

| Component | Version | Purpose |
|-----------|---------|---------|
| **Spring Framework** | 7.0.7 | Core dependency injection, MVC, transactions |
| **Java** | 17+ | Language runtime (enforced by maven-enforcer-plugin) |
| **Maven** | 3.8.4+ | Build automation and dependency management |

### 1.4.2 Web & Presentation

| Component | Version | Purpose |
|-----------|---------|---------|
| **Spring MVC** | 7.0.7 | Request handling, controller framework |
| **JSP** | 3.x (via Jakarta Servlet 6.1) | View technology |
| **Bootstrap** | 5.3.8 | CSS framework (WebJar dependency) |
| **Font Awesome** | 4.7.0 | Icon library (WebJar dependency) |
| **Flatpickr** | 4.6.13 | Date picker library (WebJar dependency) |

### 1.4.3 Persistence & Database

| Component | Version | Purpose |
|-----------|---------|---------|
| **Hibernate** | 7.3.2.Final | JPA implementation |
| **Spring Data** | 2025.1.5 | Data access abstractions |
| **H2 Database** | 2.4.240 | Default in-memory database |
| **MySQL Connector** | 8.1.0 | Optional MySQL driver |
| **PostgreSQL Driver** | 42.7.11 | Optional PostgreSQL driver |

### 1.4.4 Jakarta EE & Web Standards

| Component | Version | Purpose |
|-----------|---------|---------|
| **Jakarta Servlet API** | 6.1.0 | Servlet specification |
| **Jakarta EE JPA API** | 3.2.0 | Persistence specification |
| **Jakarta EE JAXB** | 4.0.5 | XML binding |
| **Jakarta EE JSTL** | 3.0.2 | JSP Standard Tag Library |

### 1.4.5 Supporting Libraries

| Component | Version | Purpose |
|-----------|---------|---------|
| **Jackson** | 3.1.2 | JSON serialization |
| **SLF4J** | 2.0.17 | Logging facade |
| **Logback** | 1.5.32 | Logging implementation |
| **AspectJ** | 1.9.25.1 | AOP framework |
| **Caffeine** | 3.2.3 | Caching library |
| **Hibernate Validator** | 9.1.0.Final | Bean validation |

### 1.4.6 Testing

| Component | Version | Purpose |
|-----------|---------|---------|
| **JUnit Jupiter** | 6.0.2 | Test framework |
| **Mockito** | 5.23.0 | Mocking library |
| **AssertJ** | 3.27.7 | Fluent assertions |
| **Hamcrest** | 3.0 | Matcher library |

### 1.4.7 Build & Deployment

| Component | Version | Purpose |
|-----------|---------|---------|
| **Jetty Maven Plugin** | 11.0.26 | Embedded web server for development |
| **Maven Surefire Plugin** | 3.5.5 | Test execution (requires `*Tests.java` suffix) |
| **Google Jib** | 3.5.1 | Docker image building |
| **LibSass Maven Plugin** | 0.3.4 | CSS generation from SCSS |

## 1.5 Deployment & Runtime Environments

### 1.5.1 Local Development

**Default Command:**
```bash
./mvnw jetty:run-war
# Windows: ./mvnw.cmd jetty:run-war
```

Accessible at: `http://localhost:8080/`

### 1.5.2 Database Profiles

The application supports three database configurations via Maven profiles:

| Profile | Database | Default | Configuration |
|---------|----------|---------|---|
| (none) | H2 (in-memory) | ✓ | Auto-initialized at startup |
| `MySQL` | MySQL 8+ | | Requires MySQL running on localhost:3306 |
| `PostgreSQL` | PostgreSQL 9.6+ | | Requires PostgreSQL on localhost:5432 |

**Activation Examples:**
```bash
./mvnw jetty:run-war -P MySQL
./mvnw jetty:run-war -P PostgreSQL
```

### 1.5.3 Persistence Profile Selection

Independent of the database, the persistence layer implementation is selected via:
```bash
./mvnw jetty:run-war -Dspring.profiles.active=jdbc
./mvnw jetty:run-war -Dspring.profiles.active=spring-data-jpa
./mvnw jetty:run-war -Dspring.profiles.active=jpa  # default
```

### 1.5.4 Production Deployment

**WAR Package:**
```bash
./mvnw install
# Output: target/petclinic.war
```

**Docker Image:**
```bash
mvn jib:build
# Image: springcommunity/spring-framework-petclinic
# Uses distroless Jetty base image
```

## 1.6 Scope

### 1.6.1 Included in This System

1. **Web-based User Interface**
   - Owner and pet management workflows
   - Veterinarian and specialty browsing
   - Visit scheduling and history

2. **Domain Model**
   - Core entities: Owner, Pet, PetType, Vet, Specialty, Visit
   - Relationships and constraints as implemented

3. **Persistence Layer**
   - Three pluggable repository implementations
   - Support for H2, MySQL, PostgreSQL databases
   - Transaction management and caching

4. **Service Layer**
   - `ClinicService` providing business logic
   - Cache integration for frequently accessed data

5. **Spring MVC Presentation**
   - Request mapping and controller logic
   - View resolution and JSP rendering
   - Form validation and error handling

6. **Testing Infrastructure**
   - Unit tests for domain entities (entity-level logic)
   - Service layer tests (business logic)
   - Controller tests (HTTP interactions)
   - Repository tests (data access layer)

### 1.6.2 Excluded from This System

1. **External Systems Integration**
   - No payment processing
   - No email notifications or messaging systems
   - No external inventory management
   - No third-party authentication (basic HTTP authentication context only)

2. **Advanced Features**
   - Multi-tenancy or organization isolation (not implemented)
   - Real-time notifications (WebSocket, Server-Sent Events)
   - Mobile applications or REST API for third-party consumers
   - Audit logging or compliance reporting (beyond basic transaction logging)
   - Advanced billing or accounting features

3. **Infrastructure**
   - Monitoring, metrics, or observability (OpenTelemetry, Prometheus)
   - Load balancing or clustering configuration
   - Security hardening beyond Spring Framework defaults
   - Custom authentication/authorization policies

4. **Content Management**
   - Localization/internationalization (i18n) – application uses English only
   - CMS integration
   - Document management

## 1.7 Configuration Management

### 1.7.1 Spring Configuration Files

The application uses **XML-based Spring configuration** (not Spring Boot or Java Config):

- `src/main/resources/spring/business-config.xml` – Service and repository layer beans, profile-based persistence configuration
- `src/main/resources/spring/mvc-core-config.xml` – Spring MVC core configuration
- `src/main/resources/spring/mvc-view-config.xml` – View resolvers (JSP, XML/JSON content negotiation)
- `src/main/resources/spring/datasource-config.xml` – DataSource configuration per database profile
- `src/main/resources/spring/tools-config.xml` – Caching and AOP configuration

### 1.7.2 Programmatic Configuration

**Application Entry Point**: `PetclinicInitializer.java` (Servlet 3.0+ programmatic initialization, replaces `web.xml`)

### 1.7.3 CSS Generation

- **Source**: `src/main/webapp/resources/scss/petclinic.scss`
- **Generated Output**: `src/main/webapp/resources/css/petclinic.css`
- **Regeneration Required**: After SCSS changes, run `./mvnw generate-resources -P css`

⚠️ **Important**: The CSS file is generated; direct edits to `.css` will be overwritten.

## 1.8 Code Organization

### 1.8.1 Directory Structure

```
src/main/java/org/springframework/samples/petclinic/
├── model/              # Domain entities (Owner, Pet, Vet, Visit, etc.)
├── service/            # Business logic (ClinicService)
├── repository/         # Repository interfaces
│   ├── jpa/            # JPA implementation
│   ├── jdbc/           # JDBC implementation
│   └── springdatajpa/  # Spring Data JPA implementation
├── web/                # Spring MVC controllers
├── util/               # Utility classes

src/main/webapp/
├── WEB-INF/
│   ├── jsp/            # JSP view templates
│   └── tags/           # Custom tag libraries
└── resources/
    ├── css/            # Generated CSS (from SCSS)
    └── scss/           # SCSS source files
```

### 1.8.2 Naming Conventions

- **Test Files**: Must end with `Tests.java` (e.g., `OwnerControllerTests.java`) – enforced by maven-surefire-plugin
- **Code Indentation**: 4 spaces for Java and XML (per `.editorconfig`)
- **Line Endings**: LF (Unix-style)
- **Encoding**: UTF-8

## 1.9 Quality & CI/CD

### 1.9.1 Testing Requirements

- All changes must pass test suite: `./mvnw verify`
- Test execution includes unit tests, integration tests, and SonarCloud analysis (main branch)

### 1.9.2 Build Verification

- Java 17 and Java 21 compatibility (enforced by CI/CD)
- Maven 3.8.4+ required

### 1.9.3 Code Quality

- SonarCloud integration for main branch (code coverage and quality gates)
- Pull requests include test execution (no SonarCloud analysis for PRs)

## 1.10 Document Scope & Applicability

### 1.10.1 Version Coverage

This document covers **Spring Framework PetClinic version 7.0.3** and the technology stack versions listed in Section 1.4.

### 1.10.2 Target Audience

- **Architects**: Understanding layered architecture and Spring patterns
- **Developers**: Implementation details, code organization, and development workflow
- **Maintainers**: Configuration, deployment, and operational considerations
- **DevOps/Platform Teams**: Build, containerization, and deployment procedures

### 1.10.3 Assumptions

- Java 17+ is installed and configured
- Maven 3.8.4+ is available in the build environment
- Readers have basic familiarity with Spring Framework concepts
- Target deployment environments support WAR packaging (Jetty 11+, Tomcat 11+)
- For persistent databases (MySQL, PostgreSQL), appropriate DBMS instances are available and properly initialized

### 1.10.4 Known Limitations & Not Identified

The following aspects are **not fully detailed in the code graph** and may require additional investigation:

- **Caching Strategy**: Cache invalidation rules and TTL configurations are not exhaustively documented in the graph
- **Transaction Boundaries**: Specific transaction demarcation rules at the service level are noted but not comprehensively modeled
- **Error Handling**: Global exception handling and error recovery mechanisms are partially visible in the graph
- **Security**: Authentication and authorization implementation details are minimal in the codebase (basic servlet context only)
- **Performance Tuning**: Query optimization, N+1 prevention strategies, and lazy loading policies are implementation-specific

---

**End of Section 1: Introduction and Scope**
