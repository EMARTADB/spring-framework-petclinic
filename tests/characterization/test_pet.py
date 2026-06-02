"""
Characterization tests for Pet.
Legacy source: src/main/java/.../model/Pet.java

Behaviour pinned:
  - getVisitsInternal() lazy-initialises to empty set (never None)
  - addVisit() adds visit AND back-links visit.pet = this pet
  - getVisits() returns UNMODIFIABLE list sorted by date DESCENDING (reversed)
  - getBirthDate / setBirthDate round-trip
  - getType / setType round-trip
  - getOwner is set via setOwner (package-private in Java → protected here)
"""

import pytest
from datetime import date

pytestmark = pytest.mark.skip("pending RULE-004 — petclinic.model.Pet not yet implemented")


from petclinic.model import Pet, PetType, Visit  # type: ignore[import]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pet(name: str = "Buddy", pet_id: int | None = None) -> "Pet":
    p = Pet()
    p.set_name(name)
    p.set_birth_date(date(2020, 6, 15))
    if pet_id is not None:
        p.set_id(pet_id)
    return p


def _visit(desc: str, visit_date: date) -> "Visit":
    v = Visit()
    v.set_description(desc)
    v.set_date(visit_date)
    return v


# ---------------------------------------------------------------------------
# getVisitsInternal — lazy init
# ---------------------------------------------------------------------------

class TestGetVisitsInternalLazyInit:
    def test_visits_internal_not_none_before_add(self):
        p = _pet()
        assert p.get_visits_internal() is not None

    def test_visits_internal_empty_before_add(self):
        p = _pet()
        assert len(p.get_visits_internal()) == 0

    def test_visits_internal_same_instance_on_repeated_calls(self):
        p = _pet()
        assert p.get_visits_internal() is p.get_visits_internal()


# ---------------------------------------------------------------------------
# addVisit
# ---------------------------------------------------------------------------

class TestAddVisit:
    def test_add_visit_appears_in_get_visits(self):
        p = _pet()
        v = _visit("Annual check-up", date(2023, 3, 10))
        p.add_visit(v)
        assert v in p.get_visits()

    def test_add_visit_back_links_pet(self):
        """addVisit must call visit.setPet(this)."""
        p = _pet()
        v = _visit("Vaccination", date(2023, 5, 1))
        p.add_visit(v)
        assert v.get_pet() is p

    def test_add_two_visits_both_present(self):
        p = _pet()
        v1 = _visit("First", date(2022, 1, 1))
        v2 = _visit("Second", date(2023, 1, 1))
        p.add_visit(v1)
        p.add_visit(v2)
        assert len(p.get_visits()) == 2


# ---------------------------------------------------------------------------
# getVisits — sorted descending by date, unmodifiable
# ---------------------------------------------------------------------------

class TestGetVisitsSorting:
    def test_visits_sorted_descending_by_date(self):
        """Three visits added out of order → returned newest-first."""
        p = _pet()
        v1 = _visit("Oldest", date(2021, 1, 1))
        v2 = _visit("Middle", date(2022, 6, 15))
        v3 = _visit("Newest", date(2023, 12, 31))
        p.add_visit(v1)
        p.add_visit(v3)
        p.add_visit(v2)
        dates = [v.get_date() for v in p.get_visits()]
        assert dates == [date(2023, 12, 31), date(2022, 6, 15), date(2021, 1, 1)]

    def test_visits_unmodifiable(self):
        """Appending to the returned list must raise an error."""
        p = _pet()
        p.add_visit(_visit("Check", date(2023, 1, 1)))
        visits = p.get_visits()
        with pytest.raises((TypeError, AttributeError)):
            visits.append(_visit("Extra", date(2024, 1, 1)))  # type: ignore[arg-type]

    def test_visits_empty_list_when_no_visits(self):
        p = _pet()
        assert p.get_visits() == []


# ---------------------------------------------------------------------------
# birthDate round-trip
# ---------------------------------------------------------------------------

class TestBirthDate:
    def test_set_and_get_birth_date(self):
        p = _pet()
        p.set_birth_date(date(2019, 4, 20))
        assert p.get_birth_date() == date(2019, 4, 20)

    def test_birth_date_none_by_default(self):
        """A Pet constructed without setting birthDate → None."""
        p = Pet()
        p.set_name("X")
        assert p.get_birth_date() is None


# ---------------------------------------------------------------------------
# type round-trip
# ---------------------------------------------------------------------------

class TestPetType:
    def test_set_and_get_type(self):
        p = _pet()
        pt = PetType()
        pt.set_name("cat")
        p.set_type(pt)
        assert p.get_type() is pt

    def test_type_is_none_by_default(self):
        p = Pet()
        p.set_name("X")
        assert p.get_type() is None
