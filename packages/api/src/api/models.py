"""Database models (SQLAlchemy)."""

from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str]
    phone: Mapped[str | None]

    orders: Mapped[list[Order]] = relationship(back_populates="user")

    def as_dict(self) -> dict:
        return {"id": self.id, "email": self.email, "full_name": self.full_name}


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_cents: Mapped[int]

    user: Mapped[User] = relationship(back_populates="orders")
