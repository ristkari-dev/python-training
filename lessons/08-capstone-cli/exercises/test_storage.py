"""Tests for storage.py: one line of text in, one Expense out, and back again."""

import os

import pytest

from exercises.expense import Expense
from exercises.storage import format_line, load_expenses, parse_line, save_expenses

SAMPLE_FILE = """\
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
2026-09-22|groceries|10.25
"""

MALFORMED_FILE = """\

2026-09-21|rent|1200.00
NOT AN EXPENSE
2026-09-21|groceries|lots

2026-09-22|groceries|10.25
"""


@pytest.fixture
def expenses_path(tmp_path) -> str:
    """A path inside a fresh directory -- the file does not exist yet."""
    return str(tmp_path / "expenses.txt")


def test_format_line_joins_the_three_fields_with_two_decimals() -> None:
    assert format_line(Expense("2026-09-21", "groceries", 24.5)) == "2026-09-21|groceries|24.50"


def test_parse_line_reads_the_three_fields() -> None:
    assert parse_line("2026-09-21|groceries|24.50") == Expense("2026-09-21", "groceries", 24.50)


def test_parse_line_strips_whitespace_and_the_newline() -> None:
    line = "  2026-09-21 | groceries | 24.50  \n"
    assert parse_line(line) == Expense("2026-09-21", "groceries", 24.50)


@pytest.mark.parametrize(
    "line",
    [
        "",
        "   \n",
        "2026-09-21|groceries",
        "2026-09-21|groceries|24.50|extra",
        "2026-09-21|groceries|lots",
        "2026-09-21||24.50",
        "|groceries|24.50",
        "2026-09-21|refund|-5.00",
    ],
)
def test_parse_line_rejects_unusable_lines(line: str) -> None:
    assert parse_line(line) is None


def test_load_expenses_returns_empty_when_the_file_is_missing(expenses_path: str) -> None:
    assert not os.path.exists(expenses_path)
    assert load_expenses(expenses_path) == []


def test_load_expenses_skips_blank_and_malformed_lines(expenses_path: str) -> None:
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write(MALFORMED_FILE)
    assert load_expenses(expenses_path) == [
        Expense("2026-09-21", "rent", 1200.00),
        Expense("2026-09-22", "groceries", 10.25),
    ]


def test_save_expenses_writes_one_line_per_expense(expenses_path: str) -> None:
    save_expenses(
        expenses_path,
        [
            Expense("2026-09-21", "rent", 1200.00),
            Expense("2026-09-21", "groceries", 24.50),
            Expense("2026-09-22", "groceries", 10.25),
        ],
    )
    with open(expenses_path, encoding="utf-8") as f:
        assert f.read() == SAMPLE_FILE


def test_save_expenses_replaces_the_previous_contents(expenses_path: str) -> None:
    save_expenses(expenses_path, [Expense("2026-09-21", "rent", 1200.00)])
    save_expenses(expenses_path, [Expense("2026-09-22", "groceries", 10.25)])
    with open(expenses_path, encoding="utf-8") as f:
        assert f.read() == "2026-09-22|groceries|10.25\n"


def test_save_then_load_round_trips(expenses_path: str) -> None:
    expenses = [
        Expense("2026-09-21", "rent", 1200.00),
        Expense("2026-09-21", "groceries", 24.50),
        Expense("2026-09-22", "groceries", 10.25),
    ]
    save_expenses(expenses_path, expenses)
    assert load_expenses(expenses_path) == expenses
