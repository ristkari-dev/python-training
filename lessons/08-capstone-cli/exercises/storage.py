"""Reading and writing the expenses file.

The file is plain text, one expense per line, three fields separated by "|":

    2026-09-21|groceries|24.50

Reading and writing are two halves of one contract: save_expenses writes lines
that parse_line reads back unchanged.
"""

import os  # noqa: F401 -- os.path.exists() is for load_expenses()

from exercises.expense import Expense

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

    One f-string: date, category and amount joined by SEPARATOR, with the
    format spec `:.2f` on the amount so 1200 is written as 1200.00.
    """
    raise NotImplementedError("implement format_line() so the tests pass")


def parse_line(line: str) -> Expense | None:
    """Turn one storage line into an Expense, or None when the line is unusable.

    Unusable means: blank, not exactly three "|"-separated fields, an empty
    date or category, or an amount that is not a plain decimal number.

    Start with `line.strip()` and return None when nothing is left. Cut the
    rest with `.split(SEPARATOR)`, strip each field (a list comprehension does
    both in one line), and return None unless there are exactly 3. Then check
    the date and the category with is_field() and the amount with is_amount()
    before returning `Expense(date, category, float(amount))`.
    """
    raise NotImplementedError("implement parse_line() so the tests pass")


def load_expenses(path: str) -> list[Expense]:
    """Read every usable expense from path.

    A file that does not exist yet means "no expenses yet", not an error.
    Unusable lines are skipped, so one bad line never stops the report.

    A missing file is not an error: check with `os.path.exists(path)` first and
    return []. Otherwise read the whole file with
    `with open(path, encoding="utf-8") as f: text = f.read()`, cut it into
    lines with `text.splitlines()`, and keep every line parse_line() accepts --
    it returns None for the ones it rejects, so the check is
    `if expense is not None:`.
    """
    raise NotImplementedError("implement load_expenses() so the tests pass")


def save_expenses(path: str, expenses: list[Expense]) -> None:
    """Write every expense to path, replacing whatever was there before.

    Each line ends with a newline, so the file ends with one the way a text
    file should.

    Open it with `with open(path, "w", encoding="utf-8") as f:` -- mode "w"
    replaces the whole file -- then f.write() one format_line() per expense.
    write() does not add the line break at the end; you do.
    """
    raise NotImplementedError("implement save_expenses() so the tests pass")
