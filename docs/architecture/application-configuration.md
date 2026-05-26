# Application Configuration

> Status: Reviewed  
> Audience: Developers / Operations / Architects  
> Scope: Application Initialization, Spring Configuration, Database Setup, Runtime Profiles  
> Last updated: 2026-05-22

---

## 1. Purpose

This document describes the configuration architecture of Spring Framework PetClinic, including how the application initializes, which configuration files are loaded, how Spring profiles control behavior, and how database selection works. Readers should understand how to:

- Start the application with different persistence and database backends
- Locate and modify configuration settings
- Understand the role of each configuration file
- Switch between JPA, JDBC, and Spring Data JPA implementations
- Configure database connections for H2, MySQL, or PostgreSQL

---

## 2. Scope

### In scope

- Application initialization via Servlet 3.0+ programmatic configuration (`PetclinicInitializer.java`)
- Spring XML configuration files (business, MVC, datasource, tools)
- Spring profile-based switching (persistence layer + database)
- Environment variables and Maven properties for configuration
- Logging configuration (Logback)
- Internationalization and message bundles
- Resource mapping and web layer setup

### Out of scope

- Individual bean definitions (beyond structural overview)
- Detailed Spring framework internals
- Production deployment considerations (clustering, load balancing)
- Security configuration

---

## 3. High-Level Overview

Spring Framework PetClinic uses **Servlet 3.0+ programmatic initialization** (no web.xml) to load Spring XML configuration files. The application supports **three switching dimensions**:

1. **Persistence Layer** (Spring profile: `jpa`, `jdbc`, `spring-data-jpa`)
2. **Database Backend** (Maven profile: `H2`, `MySQL`, `PostgreSQL`, `HSQLDB`)
3. **Web/Tools Configuration** (always loaded)

**Initialization Flow:**

```
PetclinicInitializer.java (Servlet 3.0+ entry point)
  ├─ Creates root application context
  │   ├─ Loads: business-config.xml (persistence setup)
  │   ├─ Loads: tools-config.xml (caching, monitoring)
  │   └─ Activates profile: "jpa" (default, can override with -Dspring.profiles.active)
  │
  └─ Creates servlet application context
      └─ Loads: mvc-core-config.xml
          └─ Imports: mvc-view-config.xml (view resolution, JSP setup)
```

**Key Fact:** At any moment, exactly one persistence profile is active, and exactly one database profile applies. The application does NOT require Spring Boot.

---

## 4. Main Components

| Component | Type | Main file/path | Responsibility | Confidence |
|---|---|---|---|---|
| `PetclinicInitializer` | Java class | `src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java` | Servlet 3.0+ entry point; creates root and servlet contexts; sets default profile | Confirmed |
| `business-config.xml` | Spring XML config | `src/main/resources/spring/business-config.xml` | Defines DataSource, JPA EntityManager, transaction managers; imports datasource-config.xml; declares three persistence profiles | Confirmed |
| `datasource-config.xml` | Spring XML config | `src/main/resources/spring/datasource-config.xml` | Defines JDBC DataSource bean (Tomcat connection pool); initializes database schema and data | Confirmed |
| `mvc-core-config.xml` | Spring XML config | `src/main/resources/spring/mvc-core-config.xml` | Web tier configuration: controller scanning, resource mapping, view controllers, exception resolution | Confirmed |
| `mvc-view-config.xml` | Spring XML config | `src/main/resources/spring/mvc-view-config.xml` | View resolution: JSP prefix/suffix, content negotiation, XML marshalling | Confirmed |
| `tools-config.xml` | Spring XML config | `src/main/resources/spring/tools-config.xml` | Caching (Caffeine), AOP monitoring, JMX export | Confirmed |
| `data-access.properties` | Properties file | `src/main/resources/spring/data-access.properties` | JDBC and JPA settings; references Maven properties (db.script, jpa.database, etc.) | Confirmed |
| `logback.xml` | Logging config | `src/main/resources/logback.xml` | Logging levels and appenders; scans for changes every 30 seconds | Confirmed |
| `messages*.properties` | I18n bundles | `src/main/resources/messages/messages.properties` (and `_de`, `_es`, `_en`) | Localization strings for web tier (views, validation messages) | Confirmed |
| `pom.xml` profiles | Maven profiles | Lines 520–651 in `pom.xml` | Define database-specific JDBC drivers, URLs, usernames, passwords, and scripts | Confirmed |

---

## 5. Processing Flow

### 5.1 Servlet Initialization → Application Context Creation

```
┌─────────────────────────────────────────────────────────────────┐
│ Servlet Container (Jetty/Tomcat) starts                         │
│  → Detects PetclinicInitializer (extends                        │
│     AbstractDispatcherServletInitializer)                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
  createRootApplicationContext()   createServletApplicationContext()
        │                             │
        ├─ new XmlWebApplicationContext()
        │  ├─ setConfigLocations(                    ├─ new XmlWebApplicationContext()
        │  │    "business-config.xml",               │  ├─ setConfigLocation(
        │  │    "tools-config.xml")                  │  │   "mvc-core-config.xml")
        │  │                                         │  │    (which imports
        │  ├─ getEnvironment()                       │  │     mvc-view-config.xml)
        │  │  .setDefaultProfiles("jpa")             │  │
        │  │  (can be overridden by                  │  └─ registerDispatcherServlet()
        │  │   -Dspring.profiles.active VM option)   │
        │  │                                         │
        │  └─ ROOT CONTEXT                           └─ SERVLET CONTEXT
        │     (Beans, repositories, services)           (Controllers, views)
        │
        └─ Returns
```

### 5.2 Business Context Initialization (Persistence Profile Activation)

When `business-config.xml` loads:

1. **Import datasource-config.xml** → DataSource bean created
2. **Load data-access.properties** → Placeholders resolved (jdbc.url, jpa.database, etc.)
3. **Scan for @Transactional annotation** (tx:annotation-driven)
4. **Activate persistence profile** (jpa, jdbc, or spring-data-jpa):
   - If profile = `jpa` or `spring-data-jpa`: Create `EntityManagerFactory` + `JpaTransactionManager`
   - If profile = `jdbc`: Create `DataSourceTransactionManager` + `JdbcClient` / `NamedParameterJdbcTemplate`
5. **Component scan** repository packages matching active profile

```
business-config.xml
├─ <import resource="datasource-config.xml"/>
├─ <context:property-placeholder location="data-access.properties" />
│  (Resolves ${jdbc.url}, ${jpa.database}, etc. from Maven properties)
│
├─ <tx:annotation-driven/>
│  (Enables @Transactional)
│
└─ <beans profile="jpa,spring-data-jpa">
   ├─ <bean id="entityManagerFactory" />
   │  (HibernateJpaVendorAdapter with ${jpa.database} dialect)
   ├─ <bean id="transactionManager" class="JpaTransactionManager" />
   └─ <bean class="PersistenceExceptionTranslationPostProcessor" />

   <beans profile="jdbc">
   ├─ <bean id="transactionManager" class="DataSourceTransactionManager" />
   ├─ <bean id="jdbcClient" factory-method="create" />
   └─ <bean id="namedParameterJdbcTemplate" />
   └─ <context:component-scan base-package=".repository.jdbc" />

   <beans profile="jpa">
   └─ <context:component-scan base-package=".repository.jpa" />

   <beans profile="spring-data-jpa">
   └─ <jpa:repositories base-package=".repository.springdatajpa" />
```

### 5.3 DataSource Initialization

```
datasource-config.xml
├─ <context:property-placeholder location="data-access.properties" />
│
└─ <bean id="dataSource" class="org.apache.tomcat.jdbc.pool.DataSource">
   ├─ driverClassName = ${jdbc.driverClassName}
   │  (e.g., org.h2.Driver, com.mysql.cj.jdbc.Driver)
   ├─ url = ${jdbc.url}
   │  (e.g., jdbc:h2:mem:petclinic, jdbc:mysql://localhost:3306/petclinic)
   ├─ username = ${jdbc.username}
   └─ password = ${jdbc.password}

   <jdbc:initialize-database data-source="dataSource">
   ├─ <jdbc:script location="${jdbc.initLocation}"/>
   │  (e.g., classpath:db/h2/schema.sql)
   └─ <jdbc:script location="${jdbc.dataLocation}"/>
      (e.g., classpath:db/h2/data.sql)
```

After DataSource creation, **database is initialized** from SQL scripts. Scripts are loaded from:
- `src/main/resources/db/{db.script}/schema.sql` (creates tables)
- `src/main/resources/db/{db.script}/data.sql` (inserts seed data)

Where `{db.script}` is set by Maven profile (e.g., `h2`, `mysql`, `postgresql`).

### 5.4 Web Layer Initialization

```
mvc-core-config.xml
├─ <import resource="mvc-view-config.xml"/>
├─ <context:component-scan base-package=".web" />
│  (Scans for @Controller, @RestController)
├─ <mvc:annotation-driven conversion-service="conversionService" />
├─ <mvc:resources mapping="/resources/**" location="/resources/" />
│  (Serves CSS, JS, images from src/main/webapp/resources/)
├─ <mvc:resources mapping="/webjars/**" location="classpath:/META-INF/resources/webjars/" />
│  (Serves Bootstrap, Font Awesome from Maven WebJars)
├─ <mvc:view-controller path="/" view-name="welcome" />
├─ <mvc:default-servlet-handler />
│  (Fallback for static resources)
│
└─ conversionService bean with PetTypeFormatter

mvc-view-config.xml
└─ View resolution:
   ├─ JSP prefix: /WEB-INF/jsp/
   ├─ JSP suffix: .jsp
   └─ Content negotiation (HTML vs XML based on path extension)
```

---

## 6. Data Structures

### 6.1 Configuration Properties Resolution

Properties are resolved in this order (later overrides earlier):

1. **Maven properties** from active database profile (pom.xml, lines 520–651)
   - Example: `<db.script>h2</db.script>` → `db.script = h2`
   - Example: `<jdbc.url>jdbc:h2:mem:petclinic</jdbc.url>` → `jdbc.url = jdbc:h2:mem:petclinic`

2. **System properties** (VM options: `-Dkey=value`)
   - Example: `-Dspring.profiles.active=jdbc` overrides default profile

3. **Property placeholders** in XML and properties files
   - `data-access.properties` uses `${key}` syntax to reference Maven properties
   - Spring resolves `${...}` at context initialization time

**Example Flow for MySQL Profile:**

```
$ mvn jetty:run-war -P MySQL

pom.xml (MySQL profile, lines 563–579)
├─ db.script = mysql
├─ jpa.database = MYSQL
├─ jdbc.driverClassName = com.mysql.cj.jdbc.Driver
├─ jdbc.url = jdbc:mysql://localhost:3306/petclinic?useUnicode=true
├─ jdbc.username = petclinic
└─ jdbc.password = petclinic

datasource-config.xml resolves ${...}
├─ driverClassName = com.mysql.cj.jdbc.Driver
├─ url = jdbc:mysql://localhost:3306/petclinic?useUnicode=true
├─ username = petclinic
└─ password = petclinic

data-access.properties
├─ jdbc.initLocation = classpath:db/mysql/schema.sql
└─ jdbc.dataLocation = classpath:db/mysql/data.sql
```

### 6.2 Spring Profile Resolution

At runtime, Spring reads:

1. **Default profile** set in `PetclinicInitializer.java` line 52: `SPRING_PROFILE = "jpa"`
2. **System property override**: `-Dspring.profiles.active=jdbc` or `-Dspring.profiles.active=spring-data-jpa`
3. **Active profile determines which repository implementation loads:**
   - `jpa`: Scans `org.springframework.samples.petclinic.repository.jpa`
   - `jdbc`: Scans `org.springframework.samples.petclinic.repository.jdbc`
   - `spring-data-jpa`: Scans `org.springframework.samples.petclinic.repository.springdatajpa`

---

## 7. Dependencies

### 7.1 Configuration File Dependencies

```
PetclinicInitializer.java (entry point)
  ├─ business-config.xml
  │   ├─ datasource-config.xml
  │   │   └─ data-access.properties (references Maven properties)
  │   ├─ tools-config.xml
  │   ├─ Persistence profiles (jpa, jdbc, spring-data-jpa)
  │   │   └─ Repository implementations at .repository.{jpa|jdbc|springdatajpa}
  │   └─ data-access.properties (JPA settings, db script locations)
  │
  └─ mvc-core-config.xml
      ├─ mvc-view-config.xml
      ├─ messages/messages*.properties (localization)
      └─ Web controllers, formatters, exception handlers
```

### 7.2 Runtime Dependencies

| Component | Purpose | Dependency Type |
|-----------|---------|-----------------|
| Spring Framework 7.0.7 | Core DI, AOP, MVC | compile |
| Hibernate 7.3.2 (JPA profile) | ORM, EntityManager | compile |
| Spring Data JPA | Query derivation, repository proxy (spring-data-jpa profile) | compile |
| Tomcat JDBC Pool | Connection pooling | compile |
| H2 / MySQL / PostgreSQL drivers | Database connectivity | runtime (profile-specific) |
| Jakarta EE (formerly javax) | Servlet API, persistence annotations | compile |
| Logback | Logging | compile |
| Caffeine | In-memory caching | compile |
| WebJars (Bootstrap, FontAwesome) | Frontend resources via Maven | runtime |

### 7.3 Profile-Specific Dependencies

| Profile | Database | Driver | Version | Scope |
|---------|----------|--------|---------|-------|
| H2 (default) | H2 in-memory | com.h2database:h2 | 2.1.214 | runtime |
| HSQLDB | HyperSQL in-memory | org.hsqldb:hsqldb | 2.5.1 | runtime |
| MySQL | MySQL 5.7+ | mysql:mysql-connector-java | 8.0.33 | runtime |
| PostgreSQL | PostgreSQL 10+ | org.postgresql:postgresql | 42.5.1 | runtime |

---

## 8. Design Notes

### 8.1 Separation of Concerns

The configuration is organized into three tiers:

- **Root Context (business-config.xml)**: Persistence, transactions, repository scanning
- **Servlet Context (mvc-core-config.xml)**: Web layer, controllers, views
- **Tools Context (tools-config.xml)**: Cross-cutting concerns (caching, AOP, monitoring)

This separation allows swapping implementations without affecting web or business logic.

### 8.2 Profile-Based Switching

The application uses **two independent profile dimensions**:

1. **Persistence Profile** (Spring profile):
   - Controls repository scanning
   - Determines transaction manager type
   - Switches between three implementations (JPA, JDBC, Spring Data JPA)
   - Set in code but overridable via VM option

2. **Database Profile** (Maven profile):
   - Controls JDBC driver, URL, username, password
   - Controls which SQL scripts are loaded
   - Baked into the WAR file at build time
   - Cannot be changed at runtime without rebuilding

**Inferred Design Intent:** Developers can experiment with persistence layer implementations without rebuilding (persistence profile via VM option), but database switching requires a rebuild (Maven profile at build time).

### 8.3 Property Placeholder Strategy

Properties are centralized in `data-access.properties`, which:

- References Maven properties (resolved at build time)
- Defers resolution to Spring (at context initialization time)
- Allows system properties to override (via system-properties-mode="OVERRIDE")

This design reduces duplication but creates a two-stage resolution flow that can be confusing during troubleshooting.

### 8.4 Logging

Logback is configured to:

- Log at `DEBUG` level for `org.springframework.samples.petclinic.*` (application code)
- Log at `INFO` level for everything else (frameworks)
- Scan `logback.xml` for changes every 30 seconds (hot reload)

The `scan="true"` setting enables developers to adjust logging levels without restarting.

### 8.5 Caching

Tools configuration enables Caffeine caching with two named caches:

- `default`: General-purpose cache
- `vets`: Veterinarian list cache (likely marked with `@Cacheable("vets")`)

Cache annotations (`@Cacheable`, `@CachePut`, `@CacheEvict`) are detected via `<cache:annotation-driven/>`.

### 8.6 Character Encoding

`PetclinicInitializer` registers a `CharacterEncodingFilter` to handle UTF-8 input, specifically for supporting Chinese character entry in forms (see comment at line 76). This is a legacy requirement retained for compatibility.

### 8.7 Exception Handling

`mvc-core-config.xml` declares a `SimpleMappingExceptionResolver` that:

- Catches all exceptions (default behavior)
- Maps them to the logical view name `exception`
- Renders `/WEB-INF/jsp/exception.jsp`
- Logs exceptions to the `warn` logger

This is a simple catch-all error handler; more specific error handling may exist in controller advice annotations.

### 8.8 Message Localization

Message bundles are loaded via `ResourceBundleMessageSource` with basename `messages/messages`:

- `messages.properties`: Fallback (English)
- `messages_en.properties`: English
- `messages_de.properties`: German
- `messages_es.properties`: Spanish

Spring's view resolvers use these bundles for form labels, validation messages, and UI strings.

### 8.9 Resource Mapping Strategy

The application maps static resources via:

- `/resources/**` → `src/main/webapp/resources/` (application CSS, JS, images)
- `/webjars/**` → Maven WebJars (Bootstrap, FontAwesome, etc.)
- **Default servlet handler** for unmapped requests (fallback to Jetty/Tomcat default)

This allows JSP views to reference resources using `<link href="/resources/css/petclinic.css" />` or `<link href="/webjars/bootstrap/..." />`.

### 8.10 Impedance: CSS Generation

**Critical Design Quirk:** CSS is **generated** from SCSS. The `src/main/webapp/resources/css/petclinic.css` file is auto-generated; editing it directly will be overwritten.

To regenerate CSS after SCSS changes:
```bash
./mvnw generate-resources -P css
```

This invokes the `libsass-maven-plugin` profile to compile SCSS → CSS (see pom.xml, lines 601–649).

---

## 9. Sources Consulted

### Graphify Queries

- Graph Report: `graphify-out/GRAPH_REPORT.md` (architecture overview, communities, god nodes)
- Community: "Database Configuration" (relevant nodes for configuration structure)

### Files Reviewed

- `src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java` — Servlet initialization, profile defaults
- `src/main/resources/spring/business-config.xml` — Persistence layer setup, profile definitions
- `src/main/resources/spring/datasource-config.xml` — DataSource bean, database initialization
- `src/main/resources/spring/mvc-core-config.xml` — Web tier configuration
- `src/main/resources/spring/mvc-view-config.xml` — View resolution
- `src/main/resources/spring/tools-config.xml` — Caching, AOP, monitoring
- `src/main/resources/spring/data-access.properties` — Property placeholders
- `src/main/resources/logback.xml` — Logging configuration
- `pom.xml` (lines 520–651) — Maven profiles for database selection
- `AGENTS.md` — Startup instructions, architecture overview

---

## 10. Open Questions

1. **Persistence Profile Override Scope**: Can the persistence profile (`-Dspring.profiles.active=jdbc`) be changed at runtime, or only at startup? (Inferred: Only at startup, but not explicitly documented.)

2. **CSS Regeneration Automation**: Is there any CI/CD automation to regenerate CSS, or does this always require manual intervention? (Inferred: Manual, based on instructions in AGENTS.md.)

3. **Database Migration Strategy**: How are schema changes managed when switching between database profiles? (No evidence found; likely not supported—each profile's SQL scripts are independent.)

4. **Character Encoding Filter Necessity**: Is the UTF-8 `CharacterEncodingFilter` still needed in modern Spring/Jakarta EE? (Inferred: Legacy requirement, retained for compatibility.)

5. **JMX Monitoring Setup**: Tools configuration exports MBeans via `<context:mbean-export/>`. How is the MBX monitoring console configured? (Not documented in provided files.)

6. **Cache Invalidation Strategy**: Beyond the two named caches (`default`, `vets`), how are cache eviction policies defined? (No evidence found; likely using Caffeine defaults.)

---

## 11. Assumptions

1. **Default Profiles Are Stable**: The `SPRING_PROFILE = "jpa"` default in `PetclinicInitializer.java` is intended to remain unchanged. VM option override (`-Dspring.profiles.active`) is the intended mechanism for switching persistence implementations.

2. **Maven Profiles Are Build-Time Only**: Database profiles (H2, MySQL, PostgreSQL) are baked into the WAR at build time. Switching databases requires a rebuild—no runtime switching mechanism exists.

3. **Property Resolution Order**: System properties (`-Dkey=value`) override Maven properties. This is declared in `datasource-config.xml` via `system-properties-mode="OVERRIDE"`.

4. **Classpath Assumption for Scripts**: SQL initialization scripts (`schema.sql`, `data.sql`) are expected to be on the classpath under `db/{db.script}/`. No fallback mechanism is visible if scripts are missing.

5. **Single Transaction Manager at a Time**: Only one transaction manager bean is active (either `JpaTransactionManager`, `DataSourceTransactionManager`, or implicitly managed by Spring Data JPA). Mixing is not supported.

6. **Logback Hot-Reload is Safe**: The `scan="true"` setting enables hot-reloading of `logback.xml`. Assumed to be safe for development; not recommended for production.

7. **WebJars Always Available**: Bootstrap and FontAwesome WebJars are assumed to be present on the classpath. Missing WebJars would cause 404s on `/webjars/**` requests but would not fail startup.

8. **No Externalized Configuration at Runtime**: There is no externalized configuration system (e.g., Spring Cloud Config, Kubernetes ConfigMaps). All configuration is static (Maven properties, properties files, XML).

---

