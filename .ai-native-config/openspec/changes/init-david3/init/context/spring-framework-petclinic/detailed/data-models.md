# Data Models

Tables (from `db/*/schema.sql`): `vets`, `specialties`, `vet_specialties`, `types`, `owners`, `pets`, `visits`.

JPA entities (`model` package): Vet (`vets`), Specialty (`specialties`), PetType (`types`), Owner (`owners`), Pet (`pets`), Visit (`visits`). Mapped superclasses: BaseEntity, NamedEntity, Person. `Vets` is a collection wrapper (JSON/XML view).

Relationships (inferred from schema layout, not verified by reading source): owner 1..n pet; pet n..1 type; pet 1..n visit; vet n..n specialty via `vet_specialties`.

Migration strategy: none (no Flyway/Liquibase); schema and sample data loaded at startup from `db/<db.script>/schema.sql` and `data.sql`. MySQL and PostgreSQL have setup notes (`petclinic_db_setup_*.txt`).
