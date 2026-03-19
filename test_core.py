"""Tests for core business logic using an in-memory SQLite database."""

from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use in-memory DB for all tests
os.environ["FINANCE_DB_URL"] = "sqlite:///:memory:"

from finance_tracker.core import (
    add_transaction,
    delete_transaction,
    get_category_breakdown,
    get_summary,
    list_transactions,
    search_transactions,
)
from finance_tracker.database import init_db
from finance_tracker.models import Base, TransactionCreate, TransactionType

# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


def _income(session, amount=1000.0, category="Salary"):
    return add_transaction(session, TransactionCreate(
        type=TransactionType.INCOME, amount=amount, category=category
    ))


def _expense(session, amount=200.0, category="Groceries", description=None):
    return add_transaction(session, TransactionCreate(
        type=TransactionType.EXPENSE, amount=amount, category=category,
        description=description,
    ))


def _savings(session, amount=100.0, category="Emergency Fund"):
    return add_transaction(session, TransactionCreate(
        type=TransactionType.SAVINGS, amount=amount, category=category
    ))


# ─── TransactionCreate validation ────────────────────────────────────────────

class TestTransactionCreate:
    def test_valid(self):
        t = TransactionCreate(type=TransactionType.INCOME, amount=500, category="Test")
        assert t.amount == 500.0

    def test_amount_rounded(self):
        t = TransactionCreate(type=TransactionType.EXPENSE, amount=9.999, category="X")
        assert t.amount == 10.0

    def test_negative_amount_raises(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            TransactionCreate(type=TransactionType.INCOME, amount=-50, category="X")

    def test_zero_amount_raises(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            TransactionCreate(type=TransactionType.INCOME, amount=0, category="X")

    def test_blank_category_raises(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            TransactionCreate(type=TransactionType.EXPENSE, amount=10, category="   ")


# ─── CRUD ─────────────────────────────────────────────────────────────────────

class TestAddTransaction:
    def test_creates_row(self, session):
        tx = _income(session)
        assert tx.id is not None
        assert tx.type == TransactionType.INCOME
        assert tx.amount == 1000.0

    def test_description_optional(self, session):
        tx = _expense(session)
        assert tx.description is None

    def test_description_stored(self, session):
        tx = _expense(session, description="Weekly shop")
        assert tx.description == "Weekly shop"


class TestListTransactions:
    def test_returns_all(self, session):
        _income(session)
        _expense(session)
        _savings(session)
        results = list_transactions(session)
        assert len(results) == 3

    def test_filter_by_type(self, session):
        _income(session)
        _expense(session)
        results = list_transactions(session, tx_type=TransactionType.INCOME)
        assert len(results) == 1
        assert results[0].type == TransactionType.INCOME

    def test_filter_by_category(self, session):
        _income(session, category="Freelance")
        _income(session, category="Salary")
        results = list_transactions(session, category="free")
        assert len(results) == 1

    def test_limit(self, session):
        for _ in range(10):
            _income(session)
        results = list_transactions(session, limit=3)
        assert len(results) == 3

    def test_ordered_desc(self, session):
        t1 = _income(session, amount=100)
        t2 = _income(session, amount=200)
        results = list_transactions(session)
        assert results[0].id >= results[-1].id


class TestDeleteTransaction:
    def test_delete_existing(self, session):
        tx = _income(session)
        ok = delete_transaction(session, tx.id)
        assert ok is True
        assert list_transactions(session) == []

    def test_delete_nonexistent(self, session):
        ok = delete_transaction(session, 9999)
        assert ok is False


# ─── Summary ──────────────────────────────────────────────────────────────────

class TestGetSummary:
    def test_empty(self, session):
        s = get_summary(session)
        assert s.total_income == 0
        assert s.net == 0

    def test_net(self, session):
        _income(session, 1000)
        _expense(session, 300)
        s = get_summary(session)
        assert s.total_income == 1000
        assert s.total_expenses == 300
        assert s.net == 700

    def test_savings_rate(self, session):
        _income(session, 1000)
        _savings(session, 200)
        s = get_summary(session)
        assert s.savings_rate == pytest.approx(20.0)

    def test_savings_rate_zero_income(self, session):
        s = get_summary(session)
        assert s.savings_rate == 0.0


# ─── Category breakdown ───────────────────────────────────────────────────────

class TestCategoryBreakdown:
    def test_aggregates_same_category(self, session):
        _expense(session, 100, "Food")
        _expense(session, 50, "Food")
        bd = get_category_breakdown(session, tx_type=TransactionType.EXPENSE)
        assert bd["Food"] == 150.0

    def test_sorted_descending(self, session):
        _expense(session, 10, "Cheap")
        _expense(session, 500, "Expensive")
        bd = get_category_breakdown(session, tx_type=TransactionType.EXPENSE)
        keys = list(bd.keys())
        assert keys[0] == "Expensive"


# ─── Search ───────────────────────────────────────────────────────────────────

class TestSearch:
    def test_search_category(self, session):
        _income(session, category="Freelance Python")
        _expense(session, category="Rent")
        results = search_transactions(session, "python")
        assert len(results) == 1

    def test_search_description(self, session):
        _expense(session, description="Amazon Prime subscription")
        results = search_transactions(session, "amazon")
        assert len(results) == 1

    def test_search_no_results(self, session):
        results = search_transactions(session, "zzznomatch")
        assert results == []
