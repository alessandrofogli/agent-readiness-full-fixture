"""Background jobs (nightly digest behind a feature flag)."""

from __future__ import annotations

from api.flags import is_enabled
from api.models import User
from sqlalchemy.orm import Session


def nightly_digest(session: Session) -> dict:
    """Build the nightly digest; gated behind the beta_dashboard flag."""
    if not is_enabled("beta_dashboard"):
        return {"skipped": True, "reason": "beta_dashboard disabled"}
    users = session.query(User).all()
    return {"skipped": False, "users": len(users)}
