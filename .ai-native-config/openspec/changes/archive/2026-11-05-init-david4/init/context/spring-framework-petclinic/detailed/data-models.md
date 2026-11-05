# Data Models

Tables (from `db/h2/schema.sql`; equivalents for hsqldb, mysql, postgresql): `vets`, `specialties`, `vet_specialties`, `types`, `owners`, `pets`, `visits`.

Entities (`model`): BaseEntity → NamedEntity (PetType, Specialty), Person (Owner, Vet), Pet, Visit; `Vets` wrapper for JSON/XML.
Likely relations (inferred from table names): owner 1-N pet, pet 1-N visit, pet N-1 type, vet N-N specialty.
Migrations: none; schema/data scripts loaded at startup via `data-access.properties` (`jdbc.initLocation`, `jdbc.dataLocation`).
