# Key Contextualization Points for Archivist Agent in spring-framework-petclinic

Below are the critical points contextualized for this project (workspace root contains the `openspec` directory; repository: `./spring-framework-petclinic`).

## 1. Directory Structure & Paths

| Generic Reference | Description |
|-------------------|------------------------|
| `openspec/changes/` | Active changes directory location (workspace root) |
| `openspec/changes/archive/` | Archive destination path |
| `openspec/specs/` | Main specifications directory |
| `openspec/changes/<name>/specs/` | Delta specs location within a change |

---

## 2. CLI Tool & Commands

Run OpenSpec commands from the workspace root.

| Generic Reference | Description |
|-------------------|------------------------|
| `openspec list --json` | Command to list available changes |
| `openspec status --change "<name>" --json` | Command to check change status |

---

## 3. Schema & Workflow Definition

| Generic Reference       | Description                                                                                      |
|-------------------------|--------------------------------------------------------------------------------------------------|
| Schema list             | Any of the schemas present in openspec: `openspec schemas --json` |
| Schema location         | `openspec/schemas/{schema}/schema.yaml`                                                          |
| Valid artifact statuses | `proposal`, `specs`, `design`, `tasks`, `test-plan`, `validation-results`, `done`, ...           |
| Task tracking syntax    | Markdown checkboxes: `- [ ]` (incomplete), `- [x]` (complete)                                    |
| Tasks file              | Located at path from `openspec status --json` output                                             |

---

## 4. Specification Sync Rules

| Aspect | Description                                               |
|--------|-----------------------------------------------------------|
| Delta spec location | `openspec/changes/<name>/specs/<capability>/spec.md`      |
| Main spec location | `openspec/specs/<capability>/spec.md` |
| Capability definition | A functional module or bounded context of the application |
| Sync behavior | Delta specs are compared with the main specs (adds, modifications, removals, renames) and synced via the sync skill |

---

## 5. Archive Naming & Organization

| Generic Reference | Description                                      |
|-------------------|--------------------------------------------------|
| `YYYY-MM-DD-<name>` | Archive naming pattern                           |
| Date format | Local date in `YYYY-MM-DD` format                |
| Archive structure | Flat directory under `openspec/changes/archive/` |

---

## 6. Completion Criteria

| Aspect | Description |
|--------|------------------------|
| Artifact completion | All artifacts must have `status: "done"` in `openspec status --json` output |
| Incomplete handling | Warn user but allow archiving with confirmation |
