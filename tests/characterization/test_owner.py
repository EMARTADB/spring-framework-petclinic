"""
Characterization tests for Owner.
Legacy source: src/main/java/.../model/Owner.java

Behaviour pinned:
  - getPets() returns an UNMODIFIABLE list sorted by name CASE-INSENSITIVELY
  - getPetsInternal() initialises to empty set lazily (never None)
  - addPet() adds the pet AND back-links pet.owner = this owner
  - getPet(name) — case-insensitive lookup, returns None when not found
  - getPet(name, ignoreNew=False) — includes new (id=None) pets
  - getPet(name, ignoreNew=True)  — skips new (id=None) pets
"""

import pytest
from datetime import date

pytestmark = pytest.mark.skip("pending RULE-003 — petclinic.model.Owner not yet implemented")


from petclinic.model import Owner, Pet, PetType  # type: ignore[import]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pet(name: str, pet_id: int | None = None) -> "Pet":
    pt = PetType()
    pt.set_name("dog")
    p = Pet()
    p.set_name(name)
    p.set_birth_date(date(2020, 1, 1))
    p.set_type(pt)
    if pet_id is not None:
        p.set_id(pet_id)
    return p


def _owner() -> "Owner":
    o = Owner()
    o.set_first_name("John")
    o.set_last_name("Doe")
    o.set_address("123 Main St")
    o.set_city("Springfield")
    o.set_telephone("6085551023")
    return o


# ---------------------------------------------------------------------------
# getPetsInternal lazy init
# ---------------------------------------------------------------------------

class TestGetPetsInternalLazyInit:
    def test_pets_internal_is_empty_set_before_any_add(self):
        """getPetsInternal() must return an empty set, never None."""
        o = _owner()
        internal = o.get_pets_internal()
        assert internal is not None
        assert len(internal) == 0

    def test_pets_internal_is_same_object_on_second_call(self):
        """Subsequent calls return the same set instance (lazy init once)."""
        o = _owner()
        first = o.get_pets_internal()
        second = o.get_pets_internal()
        assert first is second


# ---------------------------------------------------------------------------
# addPet
# ---------------------------------------------------------------------------

class TestAddPet:
    def test_add_pet_appears_in_get_pets(self):
        o = _owner()
        p = _pet("Rex", pet_id=1)
        o.add_pet(p)
        assert p in o.get_pets()

    def test_add_pet_back_links_owner(self):
        """addPet must call pet.setOwner(this)."""
        o = _owner()
        p = _pet("Rex", pet_id=1)
        o.add_pet(p)
        assert p.get_owner() is o

    def test_add_two_pets_both_present(self):
        o = _owner()
        p1 = _pet("Alpha", pet_id=1)
        p2 = _pet("Beta", pet_id=2)
        o.add_pet(p1)
        o.add_pet(p2)
        pets = o.get_pets()
        assert len(pets) == 2


# ---------------------------------------------------------------------------
# getPets — sorted, unmodifiable
# ---------------------------------------------------------------------------

class TestGetPetsSorting:
    def test_pets_sorted_case_insensitively(self):
        """Input: ['Zebra', 'apple', 'Mango'] → ['apple', 'Mango', 'Zebra']."""
        o = _owner()
        for name, pid in [("Zebra", 3), ("apple", 1), ("Mango", 2)]:
            o.add_pet(_pet(name, pet_id=pid))
        names = [p.get_name() for p in o.get_pets()]
        assert names == ["apple", "Mango", "Zebra"]

    def test_get_pets_returns_unmodifiable_list(self):
        """Mutating the returned list must raise an error."""
        o = _owner()
        o.add_pet(_pet("Rex", pet_id=1))
        pets = o.get_pets()
        with pytest.raises((TypeError, AttributeError)):
            pets.append(_pet("Extra", pet_id=99))  # type: ignore[arg-type]

    def test_get_pets_empty_when_no_pets(self):
        o = _owner()
        assert o.get_pets() == []


# ---------------------------------------------------------------------------
# getPet(name) — case-insensitive, ignoreNew=False by default
# ---------------------------------------------------------------------------

class TestGetPetByName:
    def test_found_by_exact_name(self):
        o = _owner()
        p = _pet("Rex", pet_id=1)
        o.add_pet(p)
        assert o.get_pet("Rex") is p

    def test_found_case_insensitive_upper(self):
        """Input name 'REX' finds pet named 'Rex'."""
        o = _owner()
        p = _pet("Rex", pet_id=1)
        o.add_pet(p)
        assert o.get_pet("REX") is p

    def test_found_case_insensitive_lower(self):
        """Input name 'rex' finds pet named 'Rex'."""
        o = _owner()
        p = _pet("Rex", pet_id=1)
        o.add_pet(p)
        assert o.get_pet("rex") is p

    def test_not_found_returns_none(self):
        """Input name 'Ghost' when owner has 'Rex' → None."""
        o = _owner()
        o.add_pet(_pet("Rex", pet_id=1))
        assert o.get_pet("Ghost") is None

    def test_no_pets_returns_none(self):
        o = _owner()
        assert o.get_pet("Any") is None

    def test_new_pet_is_included_by_default(self):
        """getPet(name) with ignoreNew=False includes pets without an id."""
        o = _owner()
        p = _pet("NewPet")  # no id → isNew() == True
        o.add_pet(p)
        assert o.get_pet("NewPet") is p


# ---------------------------------------------------------------------------
# getPet(name, ignoreNew=True) — skips pets with id == None
# ---------------------------------------------------------------------------

class TestGetPetByNameIgnoreNew:
    def test_ignore_new_skips_pet_without_id(self):
        """Input: pet 'NewPet' with no id, ignoreNew=True → None."""
        o = _owner()
        o.add_pet(_pet("NewPet"))  # no id
        assert o.get_pet("NewPet", ignore_new=True) is None

    def test_ignore_new_finds_persisted_pet(self):
        """Input: pet 'OldPet' with id=5, ignoreNew=True → found."""
        o = _owner()
        p = _pet("OldPet", pet_id=5)
        o.add_pet(p)
        assert o.get_pet("OldPet", ignore_new=True) is p

    def test_ignore_new_false_includes_new_pet(self):
        """ignoreNew=False (explicit) includes pets without an id."""
        o = _owner()
        p = _pet("NewPet")
        o.add_pet(p)
        assert o.get_pet("NewPet", ignore_new=False) is p
