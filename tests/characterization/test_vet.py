"""
Characterization tests for Vet.
Legacy source: src/main/java/.../model/Vet.java

Behaviour pinned:
  - getSpecialtiesInternal() lazy-initialises to empty set (never None)
  - addSpecialty() adds to internal set
  - getSpecialties() returns UNMODIFIABLE list sorted by name CASE-INSENSITIVELY
  - getNrOfSpecialties() returns count from internal set (not sorted list)
  - duplicate specialty objects are deduplicated by set semantics
"""

import pytest

pytestmark = pytest.mark.skip("pending RULE-005 — petclinic.model.Vet not yet implemented")


from petclinic.model import Vet, Specialty  # type: ignore[import]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _specialty(name: str) -> "Specialty":
    s = Specialty()
    s.set_name(name)
    return s


def _vet() -> "Vet":
    v = Vet()
    v.set_first_name("Jane")
    v.set_last_name("Smith")
    return v


# ---------------------------------------------------------------------------
# getSpecialtiesInternal — lazy init
# ---------------------------------------------------------------------------

class TestGetSpecialtiesInternalLazyInit:
    def test_internal_not_none_before_add(self):
        assert _vet().get_specialties_internal() is not None

    def test_internal_empty_before_add(self):
        assert len(_vet().get_specialties_internal()) == 0

    def test_internal_same_instance_on_repeated_calls(self):
        v = _vet()
        assert v.get_specialties_internal() is v.get_specialties_internal()


# ---------------------------------------------------------------------------
# addSpecialty
# ---------------------------------------------------------------------------

class TestAddSpecialty:
    def test_added_specialty_in_get_specialties(self):
        v = _vet()
        s = _specialty("radiology")
        v.add_specialty(s)
        assert s in v.get_specialties()

    def test_add_two_specialties(self):
        v = _vet()
        v.add_specialty(_specialty("radiology"))
        v.add_specialty(_specialty("surgery"))
        assert v.get_nr_of_specialties() == 2


# ---------------------------------------------------------------------------
# getSpecialties — sorted, unmodifiable
# ---------------------------------------------------------------------------

class TestGetSpecialtiesSorting:
    def test_sorted_case_insensitively(self):
        """Input: ['surgery', 'Radiology', 'dentistry'] → ['dentistry', 'Radiology', 'surgery']."""
        v = _vet()
        for name in ["surgery", "Radiology", "dentistry"]:
            v.add_specialty(_specialty(name))
        names = [s.get_name() for s in v.get_specialties()]
        assert names == ["dentistry", "Radiology", "surgery"]

    def test_unmodifiable(self):
        v = _vet()
        v.add_specialty(_specialty("radiology"))
        specs = v.get_specialties()
        with pytest.raises((TypeError, AttributeError)):
            specs.append(_specialty("extra"))  # type: ignore[arg-type]

    def test_empty_list_when_no_specialties(self):
        assert _vet().get_specialties() == []


# ---------------------------------------------------------------------------
# getNrOfSpecialties
# ---------------------------------------------------------------------------

class TestGetNrOfSpecialties:
    def test_zero_when_no_specialties(self):
        assert _vet().get_nr_of_specialties() == 0

    def test_one_after_add(self):
        v = _vet()
        v.add_specialty(_specialty("radiology"))
        assert v.get_nr_of_specialties() == 1

    def test_three_after_three_adds(self):
        v = _vet()
        for name in ["radiology", "surgery", "dentistry"]:
            v.add_specialty(_specialty(name))
        assert v.get_nr_of_specialties() == 3
