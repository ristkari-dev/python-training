"""Tests for expense.py: what an expense is, and the summaries over a list."""

import pytest

from exercises.expense import Expense, filter_by_category, totals_by_category


@pytest.fixture
def sample_expenses() -> list[Expense]:
    """The three sample expenses, in file order -- rent first, two categories."""
    return [
        Expense("2026-09-21", "rent", 1200.00),
        Expense("2026-09-21", "groceries", 24.50),
        Expense("2026-09-22", "groceries", 10.25),
    ]


def test_filter_by_category_keeps_only_matches(sample_expenses: list[Expense]) -> None:
    kept = filter_by_category(sample_expenses, "groceries")
    assert kept == [sample_expenses[1], sample_expenses[2]]


def test_filter_by_category_unknown_category_is_empty(sample_expenses: list[Expense]) -> None:
    assert filter_by_category(sample_expenses, "travel") == []


def test_totals_by_category_sums_each_category(sample_expenses: list[Expense]) -> None:
    assert totals_by_category(sample_expenses) == {"rent": 1200.00, "groceries": 34.75}


def test_totals_by_category_empty_list_is_empty_dict() -> None:
    assert totals_by_category([]) == {}
