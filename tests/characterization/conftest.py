"""
Shared fixtures for Petclinic characterization tests.

These tests pin the *exact* behaviour of the Java legacy code so that
any Python rewrite can be proved equivalent by running the same suite
against the new implementation.

Import convention:
  All production models are expected under the `petclinic` package that
  the modernisation effort will create.  Until a module is implemented
  the relevant test file marks its tests with:
      @pytest.mark.skip("pending RULE-NNN")

Legacy oracle: src/main/java/org/springframework/samples/petclinic/
"""

import pytest


# ---------------------------------------------------------------------------
# Tiny helper to build model objects without a real DB / Spring context.
# Tests instantiate models directly; repositories are mocked where needed.
# ---------------------------------------------------------------------------

def make_pet_type(name: str, type_id: int | None = None):
    """Return a PetType-like object usable in tests."""
    from petclinic.model import PetType  # type: ignore[import]
    pt = PetType()
    pt.set_name(name)
    if type_id is not None:
        pt.set_id(type_id)
    return pt


def make_pet(name: str, pet_id: int | None = None, birth_date=None, pet_type=None):
    """Return a Pet configured with the supplied values."""
    from petclinic.model import Pet  # type: ignore[import]
    from datetime import date

    p = Pet()
    p.set_name(name)
    if pet_id is not None:
        p.set_id(pet_id)
    p.set_birth_date(birth_date or date(2020, 1, 1))
    if pet_type is not None:
        p.set_type(pet_type)
    return p


def make_visit(description: str, visit_date=None, visit_id: int | None = None):
    """Return a Visit configured with the supplied values."""
    from petclinic.model import Visit  # type: ignore[import]
    from datetime import date

    v = Visit()
    v.set_description(description)
    if visit_date is not None:
        v.set_date(visit_date)
    if visit_id is not None:
        v.set_id(visit_id)
    return v


def make_specialty(name: str):
    from petclinic.model import Specialty  # type: ignore[import]
    s = Specialty()
    s.set_name(name)
    return s
