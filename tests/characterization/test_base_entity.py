"""
Characterization tests for BaseEntity.
Legacy source: src/main/java/.../model/BaseEntity.java

Behaviour pinned:
  - id is None on construction  → isNew() returns True
  - id set to an integer        → isNew() returns False
  - id set back to None         → isNew() returns True again
  - getId() / setId() round-trip
"""

import pytest

pytestmark = pytest.mark.skip("pending RULE-001 — petclinic.model.BaseEntity not yet implemented")


from petclinic.model import BaseEntity  # type: ignore[import]


class TestBaseEntityIsNew:
    """BaseEntity.isNew() — branch: id is None vs id is not None."""

    def test_is_new_when_id_is_none(self):
        """A freshly constructed entity has no id → isNew() == True."""
        entity = BaseEntity()
        assert entity.is_new() is True

    def test_is_new_false_when_id_set_to_positive_integer(self):
        """After setId(1), isNew() == False."""
        entity = BaseEntity()
        entity.set_id(1)
        assert entity.is_new() is False

    def test_is_new_false_when_id_is_zero(self):
        """id=0 is a valid (non-null) id → isNew() == False.
        NOTE: Java getId() returns Integer (boxed); 0 != null."""
        entity = BaseEntity()
        entity.set_id(0)
        assert entity.is_new() is False

    def test_is_new_true_after_id_reset_to_none(self):
        """Resetting id to None makes the entity 'new' again."""
        entity = BaseEntity()
        entity.set_id(42)
        entity.set_id(None)
        assert entity.is_new() is True

    def test_get_id_returns_set_value(self):
        """getId() round-trip: set 99 → get 99."""
        entity = BaseEntity()
        entity.set_id(99)
        assert entity.get_id() == 99

    def test_get_id_returns_none_before_set(self):
        """getId() returns None before any setId() call."""
        entity = BaseEntity()
        assert entity.get_id() is None
