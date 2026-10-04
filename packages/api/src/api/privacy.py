"""GDPR-style data export and deletion (see PRIVACY.md)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from .models import User


def export_user_data(session: Session, user_id: int) -> dict:
    user = session.get(User, user_id)
    if user is None:
        raise KeyError(f"user {user_id} not found")
    return {
        "user_id": user.id,
        "format": "json",
        "data": {
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "orders": [{"id": o.id, "total_cents": o.total_cents} for o in user.orders],
        },
    }


def delete_user_data(session: Session, user_id: int) -> dict:
    user = session.get(User, user_id)
    if user is None:
        raise KeyError(f"user {user_id} not found")
    session.delete(user)
    session.commit()
    return {"user_id": user_id, "deleted": True, "retention_note": "removed within 30 days"}
