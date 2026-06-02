"""
Characterization tests for NamedEntity.
Legacy source: src/main/java/.../model/NamedEntity.java

Behaviour pinned:
  - getName() / setName() round-trip
  - toString() delegates to getName() — returns the name string directly
  - toString() when name is None → returns the string "None" / "null"
    (Java returns null from getName(); Python equivalent is None → str(None))
"""

import pytest

pytestmark = pytest.mark.skip("pending RULE-002 — petclinic.model.NamedEntity not yet implemented")


from petclinic.model import NamedEntity  # type: ignore[import]


class TestNamedEntityName:
    """getName/setName round-trip."""

    def test_set_and_get_name(self):
        entity = NamedEntity()
        entity.set_name("Buddy")
        assert entity.get_name() == "Buddy"

    def test_name_is_none_before_set(self):
        entity = NamedEntity()
        assert entity.get_name() is None


class TestNamedEntityToString:
    """toString() returns getName() — mirrors Java's `return this.getName()`."""

    def test_to_string_returns_name(self):
        """Input: name='Labrador' → str(entity) == 'Labrador'."""
        entity = NamedEntity()
        entity.set_name("Labrador")
        assert str(entity) == "Labrador"

    def test_to_string_when_name_is_none(self):
        """Input: name not set → str(entity) == 'None'.
        Java returns null; Python equivalent is the string 'None'.
        Flag: DISCREPANCY-001 — callers must not rely on this value."""
        entity = NamedEntity()
        assert str(entity) == "None"
