"""
Characterization tests for PetTypeFormatter.
Legacy source: src/main/java/.../web/PetTypeFormatter.java

Behaviour pinned:
  print():
    - Returns petType.getName() — locale is ignored
  parse():
    - Iterates clinicService.findPetTypes(); returns FIRST match by name
      using exact equals (case-SENSITIVE)
    - No match → raises ParseException with message "type not found: <text>"
      and error offset == 0
"""

import pytest
from unittest.mock import MagicMock

pytestmark = pytest.mark.skip("pending RULE-007 — petclinic.web.PetTypeFormatter not yet implemented")


from petclinic.web import PetTypeFormatter  # type: ignore[import]
from petclinic.model import PetType  # type: ignore[import]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pet_type(name: str) -> "PetType":
    pt = PetType()
    pt.set_name(name)
    return pt


def _service(*type_names: str) -> MagicMock:
    """Return a mock ClinicService whose findPetTypes() returns the named types."""
    svc = MagicMock()
    svc.find_pet_types.return_value = [_pet_type(n) for n in type_names]
    return svc


# ---------------------------------------------------------------------------
# print()
# ---------------------------------------------------------------------------

class TestPrint:
    def test_print_returns_name(self):
        """Input: PetType(name='cat') → 'cat'."""
        formatter = PetTypeFormatter(_service("cat", "dog"))
        pt = _pet_type("cat")
        assert formatter.print(pt, locale=None) == "cat"

    def test_print_locale_ignored(self):
        """Locale parameter has no effect on the returned string."""
        formatter = PetTypeFormatter(_service("dog"))
        pt = _pet_type("dog")
        import locale as loc_module
        assert formatter.print(pt, locale=loc_module.getlocale()) == "dog"


# ---------------------------------------------------------------------------
# parse() — found
# ---------------------------------------------------------------------------

class TestParseFound:
    def test_parse_exact_match(self):
        """Input: text='cat', types=['cat','dog'] → PetType named 'cat'."""
        formatter = PetTypeFormatter(_service("cat", "dog"))
        result = formatter.parse("cat", locale=None)
        assert result.get_name() == "cat"

    def test_parse_returns_correct_object_instance(self):
        """parse() returns the object from the service collection, not a copy."""
        cat = _pet_type("cat")
        svc = MagicMock()
        svc.find_pet_types.return_value = [cat, _pet_type("dog")]
        formatter = PetTypeFormatter(svc)
        assert formatter.parse("cat", locale=None) is cat

    def test_parse_returns_first_match(self):
        """If two types have the same name, the first one is returned."""
        first = _pet_type("cat")
        second = _pet_type("cat")
        svc = MagicMock()
        svc.find_pet_types.return_value = [first, second]
        formatter = PetTypeFormatter(svc)
        assert formatter.parse("cat", locale=None) is first


# ---------------------------------------------------------------------------
# parse() — case sensitive (no match on wrong case)
# ---------------------------------------------------------------------------

class TestParseCaseSensitive:
    def test_parse_case_sensitive_uppercase_not_found(self):
        """Input: text='CAT', types=['cat'] → ParseException (exact equals)."""
        formatter = PetTypeFormatter(_service("cat"))
        with pytest.raises(Exception) as exc_info:
            formatter.parse("CAT", locale=None)
        assert "CAT" in str(exc_info.value)

    def test_parse_case_sensitive_mixed_not_found(self):
        """Input: text='Cat', types=['cat'] → ParseException."""
        formatter = PetTypeFormatter(_service("cat"))
        with pytest.raises(Exception):
            formatter.parse("Cat", locale=None)


# ---------------------------------------------------------------------------
# parse() — not found
# ---------------------------------------------------------------------------

class TestParseNotFound:
    def test_parse_raises_on_unknown_type(self):
        """Input: text='fish', types=['cat','dog'] → exception."""
        formatter = PetTypeFormatter(_service("cat", "dog"))
        with pytest.raises(Exception) as exc_info:
            formatter.parse("fish", locale=None)
        assert "fish" in str(exc_info.value)

    def test_parse_error_message_contains_type_not_found_prefix(self):
        """Exception message matches 'type not found: <text>'."""
        formatter = PetTypeFormatter(_service("cat"))
        with pytest.raises(Exception) as exc_info:
            formatter.parse("bird", locale=None)
        assert "type not found: bird" in str(exc_info.value)

    def test_parse_raises_on_empty_type_list(self):
        """Empty collection → exception for any input."""
        formatter = PetTypeFormatter(_service())
        with pytest.raises(Exception):
            formatter.parse("cat", locale=None)

    def test_parse_raises_on_empty_text(self):
        """Input: text='' with types present → exception (no type named '')."""
        formatter = PetTypeFormatter(_service("cat", "dog"))
        with pytest.raises(Exception):
            formatter.parse("", locale=None)
