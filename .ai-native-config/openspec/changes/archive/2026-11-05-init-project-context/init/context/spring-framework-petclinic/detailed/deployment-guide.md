# Deployment Guide

- Artifact: WAR (`maven-war-plugin`), deployable to Servlet 6 / Tomcat 11-class containers; Jetty plugin for local runs; `javaee` profile in `datasource-config.xml` for JNDI datasource.
- Container image: Jib (`springcommunity/spring-framework-petclinic`), port 8080.
- CI (GitHub Actions): `maven-build-main.yml` (push to `main`: `./mvnw -B verify` + SonarCloud analysis, JDK matrix), `maven-build-pull-request.yml` (`./mvnw -B verify`). Dependabot in `.github/dependabot.yml`.
- No Kubernetes/Terraform config detected.
