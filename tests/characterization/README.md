# Characterization Tests — Petclinic

Tests that **pin the exact behaviour** of the Java legacy code
(`src/main/java/org/springframework/samples/petclinic/`) so that any Python
rewrite can be proved equivalent by running the same suite.

> **Golden rule:** the legacy code is the oracle.  
> If the legacy returns `X` and the spec says `Y`, the test asserts `X`
> and the discrepancy is flagged inline with `DISCREPANCY-NNN`.

---

## Directory layout

```
tests/characterization/
  conftest.py                    # shared fixtures & helpers
  test_base_entity.py            # BaseEntity.isNew() / getId()
  test_named_entity.py           # NamedEntity.toString()
  test_owner.py                  # Owner.getPet(), getPets() sort, addPet()
  test_pet.py                    # Pet.getVisits() sort, addVisit()
  test_vet.py                    # Vet.getSpecialties() sort, getNrOfSpecialties()
  test_pet_validator.py          # PetValidator.validate() all branches + supports()
  test_pet_type_formatter.py     # PetTypeFormatter.print() / parse()
  test_entity_utils.py           # EntityUtils.getById() found / not-found / type mismatch
  test_call_monitoring_aspect.py # CallMonitoringAspect state, getCallTime(), reset()
  README.md                      # this file
```

---

## Prerequisites

```bash
python -m pip install pytest
```

The tests import from a `petclinic` package that the modernisation effort
will create.  Until that package exists every test is skipped
(`@pytest.mark.skip("pending RULE-NNN")`).

---

## Running the tests

```bash
# from the project root
pytest tests/characterization/ -v
```

All tests will show `SKIPPED` until the `petclinic` package is implemented.

To run a single file:

```bash
pytest tests/characterization/test_pet_validator.py -v
```

To run only tests that are **not** skipped (i.e. already implemented):

```bash
pytest tests/characterization/ -v -k "not skip"
```

---

## Activating tests as you implement modules

1. Find the `pytestmark` line at the top of the relevant file:
   ```python
   pytestmark = pytest.mark.skip("pending RULE-NNN — ...")
   ```
2. **Remove** (or comment out) that line once the module is implemented.
3. Run the suite — all tests in that file should now pass against your
   Python implementation.

---

## Adding a new test case

1. Open the relevant `test_<module>.py` file.
2. Add a method to the existing class, or create a new class if it covers
   a new behaviour group.
3. Follow the naming convention:  
   `def test_<what_the_input_is>_<expected_outcome>(self):`
4. Use **literal** input values and **literal** expected outputs — no
   "should work correctly" assertions.
5. If the new case requires a pending feature, mark it individually:
   ```python
   @pytest.mark.skip("pending RULE-NNN")
   def test_my_new_case(self):
       ...
   ```

---

## Discrepancy flags

Cases where the legacy behaviour differs from what the spec says are
marked inline:

| ID | Location | Note |
|----|----------|------|
| DISCREPANCY-001 | `test_named_entity.py` | `toString()` returns `"None"` when name is not set — Java returns `null` |
| DISCREPANCY-002 | `test_pet_validator.py` | `PetValidator` accepts blank-only names (`"   "`) — `StringUtils.hasLength` returns `True` for whitespace |

Fixing these bugs is a **separate decision** from proving equivalence.

---

## Mapping: test file → Java source

| Test file | Java class |
|-----------|------------|
| `test_base_entity.py` | `model/BaseEntity.java` |
| `test_named_entity.py` | `model/NamedEntity.java` |
| `test_owner.py` | `model/Owner.java` |
| `test_pet.py` | `model/Pet.java` |
| `test_vet.py` | `model/Vet.java` |
| `test_pet_validator.py` | `web/PetValidator.java` |
| `test_pet_type_formatter.py` | `web/PetTypeFormatter.java` |
| `test_entity_utils.py` | `util/EntityUtils.java` |
| `test_call_monitoring_aspect.py` | `util/CallMonitoringAspect.java` |
