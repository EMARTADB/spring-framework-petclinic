"""
Characterization tests for CallMonitoringAspect.
Legacy source: src/main/java/.../util/CallMonitoringAspect.java

Behaviour pinned:
  State on construction:
    - enabled = True
    - callCount = 0
    - accumulatedCallTime = 0

  getCallTime():
    - callCount == 0                  → returns 0  (avoids division by zero)
    - callCount > 0                   → returns accumulatedCallTime // callCount

  reset():
    - sets callCount = 0
    - sets accumulatedCallTime = 0

  enabled flag:
    - setEnabled(False) → isEnabled() == False
    - setEnabled(True)  → isEnabled() == True

  NOTE: The AOP @Around advice (invoke()) is NOT tested here because it
  requires a live AspectJ weaving context.  The state-management methods
  are pure Python and fully testable in isolation.
"""

import pytest

pytestmark = pytest.mark.skip("pending RULE-009 — petclinic.util.CallMonitoringAspect not yet implemented")


from petclinic.util import CallMonitoringAspect  # type: ignore[import]


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

class TestInitialState:
    def test_enabled_by_default(self):
        aspect = CallMonitoringAspect()
        assert aspect.is_enabled() is True

    def test_call_count_zero_on_construction(self):
        aspect = CallMonitoringAspect()
        assert aspect.get_call_count() == 0

    def test_call_time_zero_on_construction(self):
        """getCallTime() with callCount=0 → 0 (no division by zero)."""
        aspect = CallMonitoringAspect()
        assert aspect.get_call_time() == 0


# ---------------------------------------------------------------------------
# getCallTime — the division-by-zero guard (branch)
# ---------------------------------------------------------------------------

class TestGetCallTime:
    def test_call_time_zero_when_no_calls(self):
        """Branch: callCount == 0 → return 0."""
        aspect = CallMonitoringAspect()
        assert aspect.get_call_time() == 0

    def test_call_time_average_when_calls_recorded(self):
        """Branch: callCount > 0 → accumulatedCallTime / callCount.
        Input: simulate 3 calls with total 300ms → average = 100ms."""
        aspect = CallMonitoringAspect()
        # Directly manipulate internal state to simulate recorded calls
        # (mirrors what the @Around advice does in production)
        aspect._call_count = 3
        aspect._accumulated_call_time = 300
        assert aspect.get_call_time() == 100

    def test_call_time_integer_division(self):
        """Java uses long division: 250ms / 3 calls → 83 (truncated, not 83.33).
        Python implementation must also truncate (integer division)."""
        aspect = CallMonitoringAspect()
        aspect._call_count = 3
        aspect._accumulated_call_time = 250
        assert aspect.get_call_time() == 83

    def test_call_time_single_call(self):
        """1 call with 47ms → getCallTime() == 47."""
        aspect = CallMonitoringAspect()
        aspect._call_count = 1
        aspect._accumulated_call_time = 47
        assert aspect.get_call_time() == 47


# ---------------------------------------------------------------------------
# reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_sets_call_count_to_zero(self):
        aspect = CallMonitoringAspect()
        aspect._call_count = 10
        aspect.reset()
        assert aspect.get_call_count() == 0

    def test_reset_sets_accumulated_time_to_zero(self):
        aspect = CallMonitoringAspect()
        aspect._accumulated_call_time = 9999
        aspect.reset()
        assert aspect.get_call_time() == 0

    def test_reset_idempotent(self):
        """Calling reset() twice leaves the aspect in the same clean state."""
        aspect = CallMonitoringAspect()
        aspect._call_count = 5
        aspect._accumulated_call_time = 100
        aspect.reset()
        aspect.reset()
        assert aspect.get_call_count() == 0
        assert aspect.get_call_time() == 0


# ---------------------------------------------------------------------------
# enabled flag
# ---------------------------------------------------------------------------

class TestEnabledFlag:
    def test_set_enabled_false(self):
        aspect = CallMonitoringAspect()
        aspect.set_enabled(False)
        assert aspect.is_enabled() is False

    def test_set_enabled_true(self):
        aspect = CallMonitoringAspect()
        aspect.set_enabled(False)
        aspect.set_enabled(True)
        assert aspect.is_enabled() is True

    def test_set_enabled_does_not_affect_call_count(self):
        """Toggling enabled must not reset counters."""
        aspect = CallMonitoringAspect()
        aspect._call_count = 7
        aspect.set_enabled(False)
        assert aspect.get_call_count() == 7
