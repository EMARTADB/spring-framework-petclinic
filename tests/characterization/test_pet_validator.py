"""
Characterization tests for PetValidator.
Legacy source: src/main/java/.../web/PetValidator.java

Behaviour pinned — validate() branches:
  ① name empty / blank / None  → rejects field "name" with code "required"
  ② name present               → no name error
  ③ pet.isNew() AND type==None → rejects field "type" with code "required"
  ④ pet.isNew() AND type set   → no type error
  ⑤ NOT isNew() AND type==None → no type error (existing pets not re-validated)
  ⑥ birthDate == None          → rejects field "birthDate" with code "required"
  ⑦ birthDate set              → no birthDate error
  
  supports():
  ⑧ Pet subclass  → True
  ⑨ other class   → False

Error code used: "required" (both as code AND as default message).
"""

import pytest
from datetime import date
from unittest.mock import MagicMock

pytestmark = pytest.mark.skip("pending RULE-006 — petclinic.web.PetValidator not yet implemented")


from petclinic.web import PetValidator  # type: ignore[import]
from petclinic.model import Pet, PetType  # type: ignore[import]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _errors():
    """Return a mock Errors-like object that records rejectValue calls."""
    errors = MagicMock()
    errors.rejected = []

    def reject(field, code, default_msg=None):
        errors.rejected.append((field, code))

    errors.reject_value = MagicMock(side_effect=reject)
    return errors


def _new_pet(name: str | None = "Buddy",
             pet_type: "PetType | None" = None,
             birth_date: "date | None" = date(2020, 1, 1)) -> "Pet":
    """Return a new Pet (id=None → isNew()==True)."""
    p = Pet()
    if name is not None:
        p.set_name(name)
    p.set_type(pet_type)
    p.set_birth_date(birth_date)
    return p


def _existing_pet(name: str = "Buddy",
                  pet_type: "PetType | None" = None,
                  birth_date: "date | None" = date(2020, 1, 1)) -> "Pet":
    """Return an existing Pet (id=5 → isNew()==False)."""
    p = _new_pet(name=name, pet_type=pet_type, birth_date=birth_date)
    p.set_id(5)
    return p


def _type(name: str = "dog") -> "PetType":
    pt = PetType()
    pt.set_name(name)
    return pt


# ---------------------------------------------------------------------------
# Name validation (branch ①②)
# ---------------------------------------------------------------------------

class TestNameValidation:
    def test_empty_string_name_is_rejected(self):
        """Input: name='' → error on 'name' with code 'required'."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="")
        pet.set_type(_type())
        validator.validate(pet, errors)
        errors.reject_value.assert_any_call("name", "required", "required")

    def test_none_name_is_rejected(self):
        """Input: name=None → error on 'name' with code 'required'."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name=None)
        pet.set_type(_type())
        validator.validate(pet, errors)
        errors.reject_value.assert_any_call("name", "required", "required")

    def test_whitespace_only_name_is_rejected(self):
        """Input: name='   ' — StringUtils.hasLength returns false for blank.
        NOTE: Java StringUtils.hasLength(' ') returns True (has chars).
        This test asserts the LEGACY behaviour: blank passes name check.
        DISCREPANCY-002: spec may intend to reject blanks — separate decision."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="   ")
        pet.set_type(_type())
        validator.validate(pet, errors)
        # Java StringUtils.hasLength("   ") == True → name NOT rejected
        calls = [call[0][0] for call in errors.reject_value.call_args_list]
        assert "name" not in calls

    def test_valid_name_not_rejected(self):
        """Input: name='Buddy' → no error on 'name'."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="Buddy")
        pet.set_type(_type())
        validator.validate(pet, errors)
        calls = [call[0][0] for call in errors.reject_value.call_args_list]
        assert "name" not in calls


# ---------------------------------------------------------------------------
# Type validation (branch ③④⑤)
# ---------------------------------------------------------------------------

class TestTypeValidation:
    def test_new_pet_with_no_type_is_rejected(self):
        """Input: isNew=True, type=None → error on 'type' with code 'required'."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="Buddy", pet_type=None)
        validator.validate(pet, errors)
        errors.reject_value.assert_any_call("type", "required", "required")

    def test_new_pet_with_type_not_rejected(self):
        """Input: isNew=True, type set → no error on 'type'."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="Buddy", pet_type=_type())
        validator.validate(pet, errors)
        calls = [call[0][0] for call in errors.reject_value.call_args_list]
        assert "type" not in calls

    def test_existing_pet_with_no_type_not_rejected(self):
        """Input: isNew=False, type=None → NO error on 'type'.
        The legacy validator only checks type for new pets."""
        validator = PetValidator()
        errors = _errors()
        pet = _existing_pet(name="Buddy", pet_type=None)
        validator.validate(pet, errors)
        calls = [call[0][0] for call in errors.reject_value.call_args_list]
        assert "type" not in calls


# ---------------------------------------------------------------------------
# BirthDate validation (branch ⑥⑦)
# ---------------------------------------------------------------------------

class TestBirthDateValidation:
    def test_none_birth_date_is_rejected(self):
        """Input: birthDate=None → error on 'birthDate' with code 'required'."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="Buddy", pet_type=_type(), birth_date=None)
        validator.validate(pet, errors)
        errors.reject_value.assert_any_call("birthDate", "required", "required")

    def test_valid_birth_date_not_rejected(self):
        """Input: birthDate=2020-01-01 → no error on 'birthDate'."""
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="Buddy", pet_type=_type(), birth_date=date(2020, 1, 1))
        validator.validate(pet, errors)
        calls = [call[0][0] for call in errors.reject_value.call_args_list]
        assert "birthDate" not in calls


# ---------------------------------------------------------------------------
# All fields valid — no errors at all
# ---------------------------------------------------------------------------

class TestNoErrorsWhenAllValid:
    def test_fully_valid_new_pet_produces_no_errors(self):
        validator = PetValidator()
        errors = _errors()
        pet = _new_pet(name="Buddy", pet_type=_type(), birth_date=date(2020, 6, 15))
        validator.validate(pet, errors)
        errors.reject_value.assert_not_called()


# ---------------------------------------------------------------------------
# supports() (branch ⑧⑨)
# ---------------------------------------------------------------------------

class TestSupports:
    def test_supports_pet_class(self):
        """supports(Pet) → True."""
        assert PetValidator().supports(Pet) is True

    def test_supports_pet_subclass(self):
        """supports(subclass of Pet) → True (isAssignableFrom)."""
        class SpecialPet(Pet):
            pass
        assert PetValidator().supports(SpecialPet) is True

    def test_does_not_support_object(self):
        """supports(object) → False."""
        assert PetValidator().supports(object) is False

    def test_does_not_support_str(self):
        """supports(str) → False."""
        assert PetValidator().supports(str) is False
