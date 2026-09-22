"""Reading and writing the expenses file.

The file is plain text, one expense per line, three fields separated by "|":

    2026-09-21|groceries|24.50

Reading and writing are two halves of one contract: save_expenses writes lines
that parse_line reads back unchanged.
"""

import os

from solutions.expense import Expense

SEPARATOR = "|"
MAX_DIGITS = 12


def is_field(text: str) -> bool:
    """True when text is usable as one stored field.

    Given code. The separator and the line break are what hold the file format
    together, so a field containing either could never be read back -- and an
    empty field would vanish.
    """
    return text != "" and SEPARATOR not in text and "\n" not in text and "\r" not in text


def is_amount(text: str) -> bool:
    """True when text is a plain non-negative number like "24.50", "5" or ".5".

    Given code. It rejects anything float() cannot read, anything with a sign
    or exponent, and anything with more than MAX_DIGITS digits before the
    point, so that what we write is always something we can read back.
    Lesson 11 rewrites this with try/except.
    """
    return text.replace(".", "", 1).isdecimal() and len(text.split(".")[0]) <= MAX_DIGITS


def format_line(expense: Expense) -> str:
    """Render one expense as a storage line, with no trailing newline.

    The amount always gets two decimals so the file round-trips.
    """
    return f"{expense.date}{SEPARATOR}{expense.category}{SEPARATOR}{expense.amount:.2f}"


def parse_line(line: str) -> Expense | None:
    """Turn one storage line into an Expense, or None when the line is unusable.

    Unusable means: blank, not exactly three "|"-separated fields, an empty
    date or category, or an amount that is not a plain decimal number.
    """
    stripped = line.strip()
    if not stripped:
        return None
    parts = [part.strip() for part in stripped.split(SEPARATOR)]
    if len(parts) != 3:
        return None
    date, category, amount = parts
    if not is_field(date) or not is_field(category) or not is_amount(amount):
        return None
    return Expense(date, category, float(amount))


def load_expenses(path: str) -> list[Expense]:
    """Read every usable expense from path.

    A file that does not exist yet means "no expenses yet", not an error.
    Unusable lines are skipped, so one bad line never stops the report.
    """
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    expenses = []
    for line in text.splitlines():
        expense = parse_line(line)
        if expense is not None:
            expenses.append(expense)
    return expenses


def save_expenses(path: str, expenses: list[Expense]) -> None:
    """Write every expense to path, replacing whatever was there before.

    Each line ends with a newline, so the file ends with one the way a text
    file should.
    """
    with open(path, "w", encoding="utf-8") as f:
        for expense in expenses:
            f.write(format_line(expense) + "\n")
