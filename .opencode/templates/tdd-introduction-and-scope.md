# Template: TDD Section 1 — Introduction and Scope

Use this template to generate section **1. Introduction and Scope** of a Technical Design Document.

The output must be written in English and saved as Markdown.

Recommended target file:

`docs/<document-name>/01-introduction-and-scope.md`

# Required Output Structure

## 1. Introduction and Scope

### 1.1 Purpose

Describe the purpose of this Technical Design Document.

The purpose must be based on observable facts from the existing system, such as:
- main modules
- application entry points
- dominant business flows
- visible APIs, services, jobs, or integrations
- domain entities or processes identified in the graph

If the system purpose is not clearly identifiable, write:

`The main business purpose of the system was not explicitly identified in the graph.`

### 1.2 System Overview

Provide a concise overview of the existing system.

Include only information supported by Graphify or direct repository evidence, such as:
- architectural style, if observable
- main modules or layers
- relevant services, controllers, routes, components, or entities
- visible external integrations
- visible persistence or infrastructure dependencies

Do not invent architectural patterns that are not observable.

If the architecture is not clear, write:

`The high-level architecture was only partially identified from the graph.`

### 1.3 Scope of This Document

Describe what this TDD section covers.

The scope may include:
- the application or subsystem analyzed
- the main process or feature area
- code-level structures included in the analysis
- technical areas covered by the document

The scope must be grounded in the user's request and Graphify findings.

### 1.4 Out of Scope

Describe what is not covered.

Use explicit statements for unavailable information.

Common examples:
- runtime behavior not visible in the graph
- production deployment details
- infrastructure configuration
- database contents
- monitoring and observability
- performance characteristics
- security controls not visible in code
- external systems not identified in the graph

Do not claim something is out of scope if the user explicitly requested it and Graphify provides evidence for it.

### 1.5 Assumptions and Constraints

List assumptions and constraints.

Separate them clearly:

- **Observed constraints:** supported by Graphify or repository evidence.
- **Inferred assumptions:** reasonable conclusions based on the graph.
- **Information gaps:** information not identified in the graph.

If no assumptions are needed, write:

`No additional assumptions were required beyond the information identified in the graph.`

### 1.6 Source of Information

State that the section is based primarily on:
- Graphify query results
- direct repository evidence when used
- reasonable inferences explicitly marked as such

Include a short note such as:

`This section is based primarily on the code graph generated under graphify-out/ and queried through graphify query. Information not visible in the graph is explicitly marked as not identified.`

# Optional Diagrams

A Mermaid diagram may be included only if Graphify identifies real relationships between system elements.

Allowed diagram types:
- C4-style context approximation
- module relationship diagram
- high-level flow diagram

Do not include diagrams based on hypothetical components or flows.

# Writing Rules

- Use clear technical language.
- Do not invent unavailable information.
- Mark missing information explicitly.
- Mark inferences explicitly.
- Keep the section ready to be included directly in a Technical Design Document.
- Do not include agent reasoning or execution logs.