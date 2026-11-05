# Deployment Guide

- Artifact: WAR (`spring-framework-petclinic`), servlet container (Jetty 11 for run, Tomcat 11 libraries referenced as provided).
- Docker: Jib plugin builds image on base `jetty:11.0-jdk17`, prefix `springcommunity`; run: `docker run -p 8080:8080 springcommunity/spring-framework-petclinic`.
- CI: GitHub Actions - `maven-build-main.yml` (push to main, Java 17/21 matrix, `./mvnw -B verify` + SonarCloud) and `maven-build-pull-request.yml`.
- Config: DB selected at build time via Maven profile; no Kubernetes/Terraform files detected.
