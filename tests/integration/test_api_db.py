"""Integration tests: ORM query-count analysis (N+1 detection)."""

from __future__ import annotations

from api.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def test_list_users_orders_is_not_n_plus_one(seeded, query_counter) -> None:
    stmt = select(User).options(selectinload(User.orders))
    users = seeded.scalars(stmt).all()
    assert len(users) == 10
    # selectinload issues exactly 2 queries (users + orders), not 1 + 10.
    assert query_counter["n"] <= 2, f"possible N+1: {query_counter['n']} queries for 10 users"


def test_lazy_load_would_be_detected(seeded, query_counter) -> None:
    seeded.expire_all()  # force reloads so lazy loading is visible to the counter
    users = seeded.scalars(select(User)).all()
    _ = [len(u.orders) for u in users]
    # Documents the N+1 baseline: 1 + 10 queries. The counter fixture is what lets
    # CI catch regressions if this pattern appears in production code.
    assert query_counter["n"] >= 11
