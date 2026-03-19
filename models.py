"""SQLAlchemy ORM models + Pydantic validation schemas."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase


# ─── ORM Base ────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ─── Enums ───────────────────────────────────────────────────────────────────

class TransactionType(str, enum.Enum):
    INCOME  = "income"
    EXPENSE = "expense"
    SAVINGS = "savings"


# ─── ORM Model ───────────────────────────────────────────────────────────────

class Transaction(Base):
    __tablename__ = "transactions"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    type        = Column(Enum(TransactionType), nullable=False)
    amount      = Column(Float,  nullable=False)
    category    = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    date        = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    def __repr__(self) -> str:
        return (
            f"<Transaction id={self.id} type={self.type.value} "
            f"amount={self.amount:.2f} category={self.category!r}>"
        )


# ─── Pydantic Schemas ─────────────────────────────────────────────────────────

class TransactionCreate(BaseModel):
    type:        TransactionType
    amount:      float
    category:    str
    description: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than zero.")
        return round(v, 2)

    @field_validator("category")
    @classmethod
    def category_must_not_be_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Category cannot be blank.")
        return v


class TransactionOut(BaseModel):
    id:          int
    type:        TransactionType
    amount:      float
    category:    str
    description: Optional[str]
    date:        datetime

    model_config = {"from_attributes": True}
