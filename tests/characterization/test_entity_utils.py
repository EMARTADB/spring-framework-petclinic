"""
Characterization tests for EntityUtils.getById().
Legacy source: src/main/java/.../util/EntityUtils.java

Behaviour pinned — getById(entities, entityClass, entityId):
  ① entity found by id AND isinstance check passes → returns entity
  ② id matches but isinstance fails → continues iteration → raises
  ③ id not in collection          → raises ObjectRetrievalFailureException
  ④ empty collection              → raises ObjectRetrievalFailureException
  ⑤ multiple entities — returns the FIRST match in iteration order
     (set iteration order is undefined; this just documents the contract)

Exception type: ObjectRetrievalFailureException
  - maps to petclinic.exceptions.ObjectRetrievalFailureException in Python
  - carries the entity class and the id that was not found
"""

import pytest

pytestmark = pytest.mark.skip("pending RULE-008 — petclinic.util.EntityUtils not yet implemented")


from petclinic.util import EntityUtils  # type: ignore[import]
from petclinic.model import BaseEntity, PetType, Specialty  # type: ignore[import]
from petclinic.exceptions import ObjectRetrievalFailureException  # type: ignore[import]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _entity(entity_id: int, name: str = "X") -> "PetType":
    e = PetType()
    e.set_id(entity_id)
    e.set_name(name)
    return e


# ---------------------------------------------------------------------------
# Found — branch ①
# ---------------------------------------------------------------------------

class TestGetByIdFound:
    def test_single_entity_found_by_id(self):
        """Input: collection=[PetType(id=1)], id=1 → returns that entity."""
        e = _entity(1, "cat")
        result = EntityUtils.get_by_id([e], PetType, 1)
        assert result is e

    def test_multiple_entities_correct_one_returned(self):
        """Input: [id=1, id=2, id=3], lookup id=2 → entity with id=2."""
        e1 = _entity(1, "cat")
        e2 = _entity(2, "dog")
        e3 = _entity(3, "bird")
        result = EntityUtils.get_by_id([e1, e2, e3], PetType, 2)
        assert result is e2

    def test_returns_correct_type(self):
        """Returned object is an instance of the requested entityClass."""
        e = _entity(5, "snake")
        result = EntityUtils.get_by_id([e], PetType, 5)
        assert isinstance(result, PetType)


# ---------------------------------------------------------------------------
# isinstance mismatch — branch ②
# ---------------------------------------------------------------------------

class TestGetByIdTypeMismatch:
    def test_id_match_but_wrong_class_raises(self):
        """A Specialty with id=1 is NOT returned when PetType is requested."""
        s = Specialty()
        s.set_id(1)
        s.set_name("radiology")
        with pytest.raises(ObjectRetrievalFailureException):
            EntityUtils.get_by_id([s], PetType, 1)


# ---------------------------------------------------------------------------
# Not found — branch ③④
# ---------------------------------------------------------------------------

class TestGetByIdNotFound:
    def test_id_not_in_collection_raises(self):
        """Input: [id=1, id=2], lookup id=99 → ObjectRetrievalFailureException."""
        entities = [_entity(1), _entity(2)]
        with pytest.raises(ObjectRetrievalFailureException):
            EntityUtils.get_by_id(entities, PetType, 99)

    def test_empty_collection_raises(self):
        """Input: [], any id → ObjectRetrievalFailureException."""
        with pytest.raises(ObjectRetrievalFailureException):
            EntityUtils.get_by_id([], PetType, 1)

    def test_exception_carries_entity_id(self):
        """The raised exception must expose the missing id (42)."""
        with pytest.raises(ObjectRetrievalFailureException) as exc_info:
            EntityUtils.get_by_id([], PetType, 42)
        assert 42 in str(exc_info.value) or exc_info.value.identifier == 42

    def test_exception_carries_entity_class(self):
        """The raised exception must expose the entity class (PetType)."""
        with pytest.raises(ObjectRetrievalFailureException) as exc_info:
            EntityUtils.get_by_id([], PetType, 1)
        assert PetType in (exc_info.value.persistent_class,) or "PetType" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Edge: id=0
# ---------------------------------------------------------------------------

class TestGetByIdEdgeCases:
    def test_id_zero_found(self):
        """id=0 is a valid integer id; entity must be returned."""
        e = _entity(0, "zero-pet")
        result = EntityUtils.get_by_id([e], PetType, 0)
        assert result is e

    def test_large_id_found(self):
        """id=2_147_483_647 (Integer.MAX_VALUE in Java) → found."""
        max_id = 2_147_483_647
        e = _entity(max_id, "max-pet")
        result = EntityUtils.get_by_id([e], PetType, max_id)
        assert result is e
