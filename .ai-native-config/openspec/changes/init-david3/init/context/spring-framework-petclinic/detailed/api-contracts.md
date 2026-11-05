# API Contracts

Derived from mapping annotations (quick scan; request/response schemas not read).

| Method | Path | Notes |
|---|---|---|
| GET | `/owners/find` | search form |
| GET | `/owners` | search results |
| GET | `/owners/new`, POST `/owners/new` | create owner |
| GET | `/owners/{ownerId}` | owner details |
| GET | `/owners/{ownerId}/edit`, POST same | update owner |
| GET | `/pets/new`, POST `/pets/new` | create pet (paths under owner scope per controller class mapping `/owners/{ownerId}`) |
| GET | `/pets/{petId}/edit`, POST same | update pet |
| GET | `/owners/*/pets/{petId}/visits/new` | visit form |
| POST | `/owners/{ownerId}/pets/{petId}/visits/new` | add visit |
| GET | `/owners/*/pets/{petId}/visits` | list visits |
| GET | `/vets` | vet list (HTML) |
| GET | `/vets.json` | JSON (application/json) |
| GET | `/vets.xml` | XML (application/xml) |
| GET | `/oups` | deliberate error page |

Authentication: none detected. Note: `@RequestMapping("/owners/{ownerId}")` is on one controller (presumably PetController), so pet paths are prefixed; verify in source.
