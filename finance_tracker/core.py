"""Core business logic — decoupled from CLI and database session management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from finance_tracker.models import Transaction, TransactionCreate, TransactionType


# ─── Summary dataclass ───────────────────────────────────────────────────────

@dataclass
class FinanceSummary:
    total_income:   float
    total_expenses: float
    total_savings:  float

    @property
    def net(self) -> float:
        return self.total_income - self.total_expenses

    @property
    def balance(self) -> float:
        return self.net - self.total_savings

    @property
    def savings_rate(self) -> float:
        """Savings as a percentage of income."""
        if self.total_income == 0:
            return 0.0
        return (self.total_savings / self.total_income) * 100


# ─── CRUD ─────────────────────────────────────────────────────────────────────

def add_transaction(session: Session, data: TransactionCreate) -> Transaction:
    tx = Transaction(
        type=data.type,
        amount=data.amount,
        category=data.category,
        description=data.description,
    )
    session.add(tx)
    session.flush()   # populate tx.id before commit
    return tx


def list_transactions(
    session: Session,
    tx_type:  Optional[TransactionType] = None,
    category: Optional[str] = None,
    limit:    Optional[int] = None,
) -> List[Transaction]:
    q = session.query(Transaction).order_by(Transaction.date.desc())
    if tx_type:
        q = q.filter(Transaction.type == tx_type)
    if category:
        q = q.filter(Transaction.category.ilike(f"%{category}%"))
    if limit:
        q = q.limit(limit)
    return q.all()


def delete_transaction(session: Session, tx_id: int) -> bool:
    tx = session.query(Transaction).filter(Transaction.id == tx_id).first()
    if tx is None:
        return False
    session.delete(tx)
    return True


def get_summary(
    session: Session,
    since:   Optional[datetime] = None,
) -> FinanceSummary:
    q = session.query(Transaction)
    if since:
        q = q.filter(Transaction.date >= since)

    income   = sum(t.amount for t in q if t.type == TransactionType.INCOME)
    expenses = sum(t.amount for t in q if t.type == TransactionType.EXPENSE)
    savings  = sum(t.amount for t in q if t.type == TransactionType.SAVINGS)
    return FinanceSummary(income, expenses, savings)


def get_category_breakdown(
    session:  Session,
    tx_type:  Optional[TransactionType] = None,
) -> dict[str, float]:
    """Return {category: total_amount} sorted descending."""
    q = session.query(Transaction)
    if tx_type:
        q = q.filter(Transaction.type == tx_type)
    breakdown: dict[str, float] = {}
    for tx in q:
        breakdown[tx.category] = breakdown.get(tx.category, 0.0) + tx.amount
    return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))


def search_transactions(session: Session, keyword: str) -> List[Transaction]:
    return (
        session.query(Transaction)
        .filter(
            Transaction.category.ilike(f"%{keyword}%")
            | Transaction.description.ilike(f"%{keyword}%")
        )
        .order_by(Transaction.date.desc())
        .all()
    )
