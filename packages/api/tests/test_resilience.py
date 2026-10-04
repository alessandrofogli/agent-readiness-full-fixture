import pybreaker
import pytest


def test_circuit_breaker_opens_after_failures() -> None:
    calls = {"n": 0}
    breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=60)

    @breaker
    def flaky() -> None:
        calls["n"] += 1
        raise RuntimeError("boom")

    for _ in range(3):
        try:
            flaky()
        except (RuntimeError, pybreaker.CircuitBreakerError):
            pass

    assert breaker.current_state == "open"
    executed = calls["n"]
    with pytest.raises(pybreaker.CircuitBreakerError):
        flaky()
    assert calls["n"] == executed  # short-circuited while open
