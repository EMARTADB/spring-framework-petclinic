# Data Models (quick scan)

Tables (from `db/h2/schema.sql`; equivalents for hsqldb/mysql/postgresql): `vets`, `specialties`, `vet_specialties`, `types`, `owners`, `pets`, `visits`.

JPA/domain classes in `model/`: `BaseEntity` → `NamedEntity` (`PetType`, `Specialty`, `Pet`), `Person` (`Owner`, `Vet`), `Visit`, `Vets` (XML/JSON wrapper).

Seed data: `db/<vendor>/data.sql`. MySQL/PostgreSQL setup notes: `petclinic_db_setup_*.txt`. Schema is script-based (no migration tool detected). Relationships/columns not analysed in detail.
