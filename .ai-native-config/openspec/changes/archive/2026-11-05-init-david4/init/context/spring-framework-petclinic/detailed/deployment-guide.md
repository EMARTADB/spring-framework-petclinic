# Deployment Guide

- Packaging: WAR (`maven-war-plugin`); deployable to Tomcat 11 / Jetty (plugin `jetty-maven-plugin` 11.0.26, `jetty-web.xml`).
- Docker: Jib plugin (image prefix `springcommunity`); run `docker run -p 8080:8080 springcommunity/spring-framework-petclinic`.
- CI (GitHub Actions): PRs run `./mvnw -B verify`; main runs `verify` plus SonarCloud analysis.
- Dev container: `.devcontainer/devcontainer.json`.
