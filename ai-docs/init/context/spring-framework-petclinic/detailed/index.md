# Project Documentation Index — spring-framework-petclinic

### Project Overview
- **Type:** monolith (single part, `web`)
- **Primary Language:** Java 17
- **Architecture:** 3-layer (web → service → repository), XML/Java-config Spring Framework (no Spring Boot)
- **Scan level:** quick (patterns/config only; no source reading)

### Quick Reference
- **Tech Stack:** Spring Framework 7.0.7, Spring MVC + JSP/JSTL, Spring Data JPA, Hibernate 7.3, JDBC, H2 (default), Maven WAR
- **Entry Point:** `PetclinicInitializer.java` (servlet container initializer)
- **Pattern:** Layered MVC with swappable repository implementations (JPA / JDBC / Spring Data JPA)

### Generated Documentation
- [Project Overview](./project-overview.md)
- [Architecture](./architecture.md)
- [Source Tree Analysis](./source-tree-analysis.md)
- [Component Inventory](./component-inventory.md)
- [Development Guide](./development-guide.md)
- [Deployment Guide](./deployment-guide.md)
- [API Contracts](./api-contracts.md)
- [Data Models](./data-models.md)

### Existing Documentation
- `readme.md` — run instructions, DB profiles
- `.github/workflows/` — CI definitions
- `.devcontainer/devcontainer.json`

### Getting Started
`./mvnw jetty:run-war` then open http://localhost:8080/
