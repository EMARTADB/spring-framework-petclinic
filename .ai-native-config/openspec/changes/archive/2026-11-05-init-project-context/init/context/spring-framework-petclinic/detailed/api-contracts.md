# API / Route Contracts (quick scan, from mapping annotations)

HTML (JSP) routes unless noted. Controllers in `web/`.

| Method | Path | Notes |
|---|---|---|
| GET | `/owners/find` | search form |
| GET | `/owners` | search results |
| GET | `/owners/new` | new owner form |
| POST | `/owners/new` | create owner |
| GET | `/owners/{ownerId}` | owner details |
| GET | `/owners/{ownerId}/edit` | edit form |
| POST | `/owners/{ownerId}/edit` | update owner |
| GET | `/pets/new` | new pet form (as mapped in `PetController`; class-level `/owners/{ownerId}` prefix applies) |
| POST | `/pets/new` | create pet |
| GET | `/pets/{petId}/edit` | edit pet |
| POST | `/pets/{petId}/edit` | update pet |
| GET | `/owners/*/pets/{petId}/visits/new` | new visit form |
| POST | `/owners/{ownerId}/pets/{petId}/visits/new` | create visit |
| GET | `/owners/*/pets/{petId}/visits` | list visits |
| GET | `/vets` | vet list (JSP) |
| GET | `/vets.json` | JSON vets |
| GET | `/vets.xml` | XML vets |
| GET | `/oups` | `CrashController`, deliberate error page |

Authentication: none detected. Request/response schemas not analysed (quick scan).
