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
    """Return the expenses in one category, keeping the original order.

    One list comprehension with an `if` filter (Lesson 05).
    """
    raise NotImplementedError("implement filter_by_category() so the tests pass")


def totals_by_category(expenses: list[Expense]) -> dict[str, float]:
    """Return {category: sum of that category's amounts}.

    Start with an empty dict `totals = {}` and loop: read the running total
    with `totals.get(expense.category, 0.0)` (Lesson 05), add this expense's
    amount, and write it back with `totals[expense.category] = ...` -- writing
    a dict key is `d[k] = v`, the half of dicts Lesson 05 did not show.
    """
    raise NotImplementedError("implement totals_by_category() so the tests pass")
