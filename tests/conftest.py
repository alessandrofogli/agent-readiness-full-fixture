"""Shared fixtures: SQLite engine, session, and a query counter for N+1 analysis."""

from __future__ import annotations

import pytest
from api.models import Base, Order, User
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture()
def engine():
    eng = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture()
def session(engine) -> Session:
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as s:
        yield s


@pytest.fixture()
def query_counter(engine):
    """Count SQL statements executed against the engine (N+1 detection)."""
    counts = {"n": 0}

    def _count(conn, cursor, statement, parameters, context, executemany):
        counts["n"] += 1

    event.listen(engine, "before_cursor_execute", _count)
    yield counts
    event.remove(engine, "before_cursor_execute", _count)


@pytest.fixture()
def seeded(session) -> Session:
    for i in range(10):
        user = User(email=f"user{i}@example.com", full_name=f"User {i}", phone=None)
        user.orders = [Order(total_cents=100 * i), Order(total_cents=200 * i)]
        session.add(user)
    session.commit()
    return session
