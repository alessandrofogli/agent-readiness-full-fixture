"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .db import get_session
from .flags import is_enabled
from .models import User
from .privacy import delete_user_data, export_user_data
from .resilience import call_external_service

app = FastAPI(title="Full Fixture API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict:
    return {"status": "ready"}


@app.get("/live")
def live() -> dict:
    return {"status": "alive"}


@app.get("/onboarding")
def onboarding(user_id: int | None = None) -> dict:
    return {"new_onboarding": is_enabled("new_onboarding", user_id)}


@app.get("/users")
def list_users(session: Session = Depends(get_session)) -> list[dict]:
    return [u.as_dict() for u in session.query(User).all()]


@app.get("/external")
def external() -> dict:
    return call_external_service()


@app.post("/privacy/export/{user_id}")
def privacy_export(user_id: int, session: Session = Depends(get_session)) -> dict:
    try:
        return export_user_data(session, user_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/privacy/delete/{user_id}")
def privacy_delete(user_id: int, session: Session = Depends(get_session)) -> dict:
    try:
        return delete_user_data(session, user_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
