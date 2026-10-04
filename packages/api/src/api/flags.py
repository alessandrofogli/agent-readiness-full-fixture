"""Custom feature flag system with deterministic percentage rollout."""

from __future__ import annotations

import hashlib

FLAGS: dict[str, dict] = {
    "new_onboarding": {
        "description": "New onboarding flow for first-time users",
        "owner": "team-growth",
        "created": "2026-09-01",
        "rollout": 10,
        "default": False,
    },
    "beta_dashboard": {
        "description": "Beta dashboard for the nightly digest",
        "owner": "team-core",
        "created": "2026-08-15",
        "rollout": 50,
        "default": False,
    },
}


def is_enabled(name: str, user_id: int | None = None) -> bool:
    """Evaluate a flag; deterministic per user when user_id is given."""
    flag = FLAGS.get(name)
    if flag is None:
        return False
    if user_id is None:
        return bool(flag["default"])
    bucket = int(hashlib.sha256(f"{name}:{user_id}".encode()).hexdigest(), 16) % 100
    return bucket < flag["rollout"]
