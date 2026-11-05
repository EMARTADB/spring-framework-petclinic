# API Contracts (MVC routes, from annotations)

| Method | Path | Controller |
|---|---|---|
| GET | /oups | CrashController |
| GET | /owners/find | OwnerController |
| GET | /owners | OwnerController |
| GET/POST | /owners/new | OwnerController |
| GET | /owners/{ownerId} | OwnerController |
| GET/POST | /owners/{ownerId}/edit | OwnerController |
| GET/POST | /owners/{ownerId}/pets/new | PetController |
| GET/POST | /owners/{ownerId}/pets/{petId}/edit | PetController |
| GET/POST | /owners/{ownerId}/pets/{petId}/visits/new | VisitController |
| GET | /owners/*/pets/{petId}/visits | VisitController |
| GET | /vets | VetController (HTML) |
| GET | /vets.json | VetController (JSON) |
| GET | /vets.xml | VetController (XML) |

Request/response schemas and authentication not determined (quick scan); no auth config detected by filename.
