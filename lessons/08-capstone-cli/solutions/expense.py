"""What an expense is, plus the pure functions that summarise a list of them.

Nothing in here touches the disk or the terminal, which is why every function
is a one-liner to test.
"""

from dataclasses import dataclass


@dataclass
class Expense:
    """One spending record.

    The date is a plain string like "2026-09-21". Real date objects arrive in
    Lesson 14; until then a string is enough, and it keeps the program free of
    a hidden clock.
    """

    date: str
    category: str
    amount: float


def filter_by_category(expenses: list[Expense], category: str) -> list[Expense]:
    """Return the expenses in one category, keeping the original order."""
    return [expense for expense in expenses if expense.category == category]


def totals_by_category(expenses: list[Expense]) -> dict[str, float]:
    """Return {category: sum of that category's amounts}."""
    totals: dict[str, float] = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
    return totals
