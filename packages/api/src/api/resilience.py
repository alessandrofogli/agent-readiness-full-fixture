"""Resilience patterns for external calls: retry + circuit breaker."""

from __future__ import annotations

import urllib.request

import pybreaker
from tenacity import retry, stop_after_attempt, wait_exponential

# Circuit breaker: open after 5 consecutive failures, half-open after 30s.
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)


@breaker
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=2), reraise=True)
def fetch_remote_status(url: str, timeout: float = 3.0) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return {"status": resp.status}


def call_external_service() -> dict:
    """Call the external service with a fallback if the breaker is open."""
    try:
        return {"remote": fetch_remote_status("https://example.com")}
    except Exception as exc:  # noqa: BLE001 - fallback is deliberate
        return {"remote": "unavailable", "fallback": True, "error": type(exc).__name__}
