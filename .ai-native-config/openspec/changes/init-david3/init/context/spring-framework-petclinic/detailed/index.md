# Spring Framework Petclinic - Documentation Index

## Project Overview
- **Type:** monolith (single part, repository `spring-framework-petclinic`)
- **Primary Language:** Java 17
- **Architecture:** 3-layer (presentation -> service -> repository), XML-configured Spring Framework MVC, WAR packaging
- **Scan level:** quick (patterns, manifests, directory structure; source files not read)

## Quick Reference
- **Tech Stack:** Spring Framework 7.0.7, Spring MVC + JSP/JSTL, Spring Data JPA 2025.1.5, Hibernate 7.3.2, JDBC, HSQLDB/H2/MySQL/PostgreSQL, Maven
- **Entry Point:** `PetclinicInitializer.java` (servlet container bootstrap) + `src/main/resources/spring/*.xml`
- **Architecture Pattern:** layered monolith, XML context config, selectable repository implementation (JPA / JDBC / Spring Data JPA)

## Generated Documentation
- [Project Overview](./project-overview.md)
- [Architecture](./architecture.md)
- [Source Tree Analysis](./source-tree-analysis.md)
- [Component Inventory](./component-inventory.md)
- [Development Guide](./development-guide.md)
- [Deployment Guide](./deployment-guide.md)
- [API Contracts](./api-contracts.md)
- [Data Models](./data-models.md)

## Existing Documentation
- [readme.md](../../../../../../spring-framework-petclinic/readme.md) - upstream README (run instructions, links)
- `.github/workflows/maven-build-main.yml`, `maven-build-pull-request.yml` - CI definitions
- `.devcontainer/devcontainer.json` - dev container

## Getting Started
`./mvnw jetty:run-war` then open http://localhost:8080/. See the [Development Guide](./development-guide.md).
