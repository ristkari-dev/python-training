# Lesson 08 — Phase 1 capstone: expense tracker CLI — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-09-22
**Owner:** Aki Ristkari

## Summary

The eighth lesson closes Phase 1 by turning seven lessons of parts into one program a
person can actually run: an **expense tracker CLI** — `add`, `list --category`,
`report` — over a pipe-delimited plain-text ledger. The learner writes two flat modules
plus the argparse wiring and imports a complete `reporting` package they are told not to
edit. Three things carry the lesson:

1. **Four units, four ideas.** `expense.py` (what an expense *is*), `storage.py` (where
   it *lives*), `reporting/` (how it *looks*), `cli.py` (how you *drive* it). The
   dependency arrows point one way; `cli.py` is the only file that imports all three.
2. **A black box you did not write.** `reporting` ships complete; its two tests pass from
   the first run — they are its documentation, not the learner's work.
3. **A feedback ladder, not a cliff.** Something goes green or something runs every 5-10
   minutes. The high point: finishing `build_parser` alone — with `main` still raising —
   makes `python -m exercises.cli --help` print real help and takes the suite from 2 to 5
   passing.

Every code block, transcript, table alignment, exit code and message below was produced
by running the prototype under the repo's toolchain (Python 3.13, pytest 9.0.3,
ruff 0.15.14).

## Scope

**Graded — the learner writes these 8 functions (~70 lines):**

| Module | Function | What it exercises |
|---|---|---|
| `storage.py` | `format_line` | f-string with a `:.2f` format spec (02) |
| `storage.py` | `parse_line` | `str.strip`/`str.split`, list comprehension, tuple unpack, `if` guards |
| `storage.py` | `load_expenses` | `os.path.exists`, `with open`, `read`, `splitlines`, `for` |
| `storage.py` | `save_expenses` | `with open(..., "w")`, `write` |
| `expense.py` | `filter_by_category` | list comprehension with a filter (05) |
| `expense.py` | `totals_by_category` | dict accumulation, `dict.get(k, default)` (05) |
| `cli.py` | `build_parser` | `argparse` subparsers, positionals vs options |
| `cli.py` | `main` | dispatch, validation, exit codes, calling every other unit |

**Given — complete, never edited.** The `reporting` package (`format_money`,
`format_table`); the `Expense` dataclass; `storage.SEPARATOR`, `storage.MAX_DIGITS`,
`storage.is_field`, `storage.is_amount`; the four `cli.py` constants `DEFAULT_PATH`,
`NOTHING_FOUND`, `BAD_FIELD`, `BAD_AMOUNT`; the top-level parser / `--file` /
`add_subparsers` lines inside `build_parser`; and the `if __name__ == "__main__":`
block. The constants are listed explicitly because the tests pin their exact text —
omitting them turns self-study into guess-the-message.

**Taught on slides/README, not graded.** Exit-code conventions; `with` as a recipe;
look-before-you-leap vs the `try/except` of Lesson 11; why money in `float` is a lie; why
the delimiter you choose becomes part of your input contract; the consequence that
`load → save` silently drops a line it could not parse.

**New vocabulary, deliberately small.** `str.strip`/`str.split`/`str.splitlines`,
`open`/`read`/`write`, `with`, `os.path.exists`, `sorted()`, `argparse`,
`sys.argv`/`sys.exit`, two pytest fixtures (`tmp_path`, `capsys`) and one context manager
(`pytest.raises`).
**Every one gets a README Concepts bullet, a slide line, and a named mention in the stub
docstring that needs it.** Verified by grep: none of these appears anywhere in lessons
01-07, and Lesson 05's Going further promises `sorted(...)` "in a later lesson" — this is
that lesson. Everything else is lessons 01-07.

## Two constraint calls — conclusions

**`with open(...)` — used, and taught as a recipe.** Lessons 01-07 contain zero `with`
and zero file I/O, so this is a real call, and the answer is to use it: `f = open(...)` …
`f.close()` is code the learner would have to *unlearn* in five lessons and it leaks the
handle whenever anything raises mid-function, while every real Python file-handling code
they will ever read uses `with open` — a capstone that looks unlike real Python defeats
its own purpose. The course already endorses the move: per the course design spec
`pytest` is used "from lesson 1 — treated as a 'magic test runner' until lesson 4
explains it properly", and Lesson 06 uses `@dataclass` seven lessons before decorators.
The teaching line, one slide and one README paragraph:

> `with` opens the file and guarantees it gets closed when the block ends — even if
> something goes wrong inside. That is all you need today. Lesson 13 shows you how
> `with` works and how to write your own.

**`try/except` — not once.** Two places tempt it; both get a plain `if`: a missing file
(`if not os.path.exists(path): return []`) and a non-numeric amount (the given
`is_amount`, below). Lesson 08 is therefore a **pure LBYL program**. `is_amount` was
verified against `float()` on every shape that matters: it accepts exactly `"5"`,
`"24.50"`, `".5"`, `"5."` (all `float()`-able) and rejects `""`, `"."`, `"-5"`, `"-0"`,
`"nan"`, `"inf"`, `"1e3"`, `"1.2.3"`, `"12,50"`, and anything with more than
`MAX_DIGITS` (12) digits before the point. `isdecimal` not `isdigit`, on purpose:
`"²".isdigit()` is `True` but `float("²")` raises, while `is_amount("²")` is `False`.
The digit cap is on purpose too, and it counts the digits **before the point** rather
than the length of the whole string: `format_line` appends `.00`, so any cap on the raw
typed text would just move the boundary — `"1000000000000"` would be accepted at the
door and written as a 16-character field the reader then refuses. Capping the integer
part makes the write form and the read form agree by construction, and it puts `inf` out
of reach: the largest value `is_amount` can hand to `float()` is under 10 trillion.

### Recommendations to later lessons — non-binding

Suggestions for Lessons 11 and 13 when those lessons are designed. Nothing in Lesson 08
depends on them; they are **not commitments**.

- **Lesson 11 (Errors & exceptions)** could reopen this exact `storage.py` and rewrite
  `load_expenses` and `is_amount` the EAFP way, side by side with the LBYL originals.
- **Lesson 13 (Decorators & context managers)** could open with a one-line callback to
  the `with` recipe above, then explain the machinery it stood in for.

## Layout

```
lessons/08-capstone-cli/
├── pyproject.toml                  # unmodified scaffold: name lesson-08-capstone-cli,
│                                   #   package = false, pytest pythonpath = ["."]
├── README.md
├── slides/{index.html, slides.md, assets/.gitkeep}
├── exercises/
│   ├── __init__.py                 # empty (scaffold)
│   ├── reporting/                  # GIVEN — complete black box
│   │   ├── __init__.py             #   re-exports format_money, format_table
│   │   ├── money.py                #   format_money                    (given)
│   │   └── table.py                #   format_table                    (given)
│   ├── expense.py                  # Expense (given) + 2 stubs
│   ├── storage.py                  # constants + is_field/is_amount (given) + 4 stubs:
│   │                               #   format_line, parse_line, load_expenses,
│   │                               #   save_expenses
│   ├── cli.py                      # constants + parser head + __main__ (given) + 2 stubs
│   ├── test_reporting.py           #  2 cases — GREEN from minute zero
│   ├── test_expense.py             #  4 cases — red
│   ├── test_storage.py             # 16 cases — red
│   └── test_cli.py                 # 19 cases — red
└── solutions/                      # same shape, fully implemented
```

Four units, four test files, 1:1 — that mapping is what lets the learner work one module
at a time (`uv run pytest exercises/test_storage.py`), which is the whole feedback story.
Per TID252 every intra-lesson import is absolute, so the `exercises.`/`solutions.` prefix
differs between the trees: measured on the prototype, `reporting/money.py` and
`reporting/table.py` are **byte-identical**, `reporting/__init__.py` and
`test_storage.py` differ by 2 import lines each, the other three test files by 1.
`reporting/` is a two-module package and not one file on purpose — it is Lesson 07's
`geom` grown up, and it costs the learner nothing.

## The `reporting` black box

Shipped complete, ruff-clean, stdlib-only, and typed — because a real library you depend
on *is* typed even when your own code isn't yet. The `exercises/` copies are identical
apart from the import prefix in `__init__.py`.

### `solutions/reporting/money.py`

```python
"""Money formatting.

Given code: you do not need to read or change this file. Call it through
``reporting.format_money`` and read that function's docstring.
"""


def format_money(amount: float) -> str:
    """Format an amount as US dollars with exactly two decimal places.

    Thousands are grouped with commas.

        format_money(24.5)   -> '$24.50'
        format_money(1200)   -> '$1,200.00'
        format_money(0)      -> '$0.00'
    """
    return f"${amount:,.2f}"
```

One expression. Negative amounts cannot reach it — `is_amount` rejects the minus sign on
both the write and the read path — so the sign-handling branch (and with it the
`$-0.00` / `-$0.00` signed-zero bug) simply does not exist.

### `solutions/reporting/table.py`

```python
"""Plain-text table rendering.

Given code: you do not need to read or change this file. Call it through
``reporting.format_table`` and read that function's docstring.
"""


def format_table(rows: list[list[str]], headers: list[str]) -> str:
    """Render rows as a column-aligned text table and return it as one string.

    ``rows`` is a list of rows; every row is a list of already-formatted
    strings. ``headers`` is a single row of column titles and fixes the column
    count: every row must have exactly as many cells as there are headers, and
    every cell must already be a string (that is what format_money is for).

    Columns are separated by two spaces. Every column is left-aligned except
    the last, which is right-aligned so amounts line up on the decimal point.
    The result has no trailing newline, so ``print()`` it.

        print(format_table([["rent", "$1,200.00"]], ["CATEGORY", "TOTAL"]))
        CATEGORY      TOTAL
        rent      $1,200.00
    """
    for row in [headers, *rows]:
        if len(row) != len(headers):
            raise ValueError(
                f"row {row!r} has {len(row)} cells, but there are {len(headers)} headers"
            )
        for cell in row:
            if not isinstance(cell, str):
                raise ValueError(f"every cell must already be a string, but {cell!r} is not")

    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    last = len(widths) - 1
    lines = []
    for row in [headers, *rows]:
        cells = []
        for index, cell in enumerate(row):
            if index == last:
                cells.append(cell.rjust(widths[index]))
            else:
                cells.append(cell.ljust(widths[index]))
        lines.append("  ".join(cells))
    return "\n".join(lines)
```

API decisions, all in service of "read the docstring, not the source":

- **Signature order is `(rows, headers)`, both required.** Not guessable — you have to
  read the docstring, which is the skill.
- **`rows` holds strings, not floats.** The caller formats money *before* handing it
  over: the renderer aligns text, it does not know what a dollar is.
- **Left-align everything except the last column** makes money line up without the
  library knowing which column is money, and because the last column is `rjust`-ed no
  rendered line ever carries trailing spaces.
- **The six validation lines are load-bearing.** Without them the mistakes a learner
  actually makes either fail *inside the file they were told not to open* or — worse —
  do not fail at all. Verified:

  | Learner's mistake | Without the guard | With it |
  |---|---|---|
  | `rows` built from floats — `[e.date, e.category, e.amount]` | `TypeError: object of type 'float' has no len()` inside `table.py` | `ValueError: every cell must already be a string, but 24.5 is not` |
  | arguments swapped — `format_table(headers, rows)` | `IndexError: list index out of range` inside `table.py` | `ValueError: every cell must already be a string, but ['rent', '$1.00'] is not` |
  | a short row — `format_table([["a"]], ["A", "B"])` | **no error at all** — a silently misaligned table, `'A  B\na'` | `ValueError: row ['a'] has 1 cells, but there are 2 headers` |
  | a long row — `format_table([["a", "b", "c"]], ["A", "B"])` | `IndexError: list index out of range` inside `table.py` | `ValueError: row ['a', 'b', 'c'] has 3 cells, but there are 2 headers` |

  *Raising* is already in the learner's vocabulary — their own stubs raise
  `NotImplementedError`. *Handling* is Lesson 11, and Going further says so.

### `solutions/reporting/__init__.py`

```python
"""Presentation helpers for the expense tracker.

This package is GIVEN. Treat it as a library someone else wrote and handed to
you: call it through the two names below, read their docstrings, and do not
edit (or even open) the modules underneath.
"""

from solutions.reporting.money import format_money
from solutions.reporting.table import format_table

__all__ = ["format_money", "format_table"]
```

`__all__` is why ruff's F401 leaves these re-exports alone — same as Lesson 07's
`geom/__init__.py`.

**Making the box actually black.** Four mechanisms, all cheap: (1) the "Given code"
banner in each module docstring; (2) `test_reporting.py` passes from the first run and
its module docstring says *"They are not your work: they are the documentation for the
`reporting` package you were handed. Read them to see how to call it."*; (3) a live
session move on the deck — `uv run python -c "from solutions.reporting import
format_table; help(format_table)"`, `help()` on a package you did not write, in five
seconds; (4) **the tests make the dependency real** — the sample ledger's `rent 1200.00`
means both expected tables contain `$1,200.00`, so a learner who inlines
`f"${e.amount:.2f}"` produces `$1200.00` and goes red. The black box is a graded
dependency, not an honour system. The README adds the honest framing: *"If you find
yourself needing to open `table.py` to know how to call it, that means the docstring
failed. Say so — noticing that is a real code-review skill."*

## `Expense` and the domain functions

### `solutions/expense.py`

```python
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
```

`dict.get(key, default)` was taught in Lesson 05 and the stub docstring points at it by
name. `@dataclass` gives `__eq__` for free, which is why every test compares whole
`Expense` objects with `==`. The docstring makes **no claim about key order** — nothing
observes it (`report` sorts) and dict `==` would not test it.

**Float money.** Every fixture amount is a binary-exact fraction (`.00`, `.25`, `.50`,
`.75`), so `24.50 + 10.25 == 34.75` holds exactly and no test needs `pytest.approx`.
Slide 8 says out loud that this is a choice, not an accident; Going further points at
`decimal.Decimal`. **No clock:** dates are strings supplied on the command line, so the
program has no hidden input and every test is deterministic by construction.

## The storage module

One expense per line, three `|`-separated fields, file ends with a newline:
`2026-09-21|groceries|24.50`. `SEPARATOR = "|"` is a module constant so the writer and
the reader literally cannot disagree. Not JSON, not CSV — `json` and `csv` are Lesson 14,
and a format dumb enough to read with `str.split` is what makes the parsing lesson
visible.

### `solutions/storage.py`

```python
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
```

**`save_expenses`, not an `append_expense`.** The writer takes the whole list and
rewrites the file with mode `"w"`; `add` therefore does **load → append in memory →
save**. That is what makes the `save → load` round-trip test possible at all, and it is
what the `"w"`-vs-`"a"` mutation proves the suite catches.

**`splitlines()`, not `split("\n")`** — one method that deletes a manufactured edge case:
`"a\nb\n".splitlines()` is `["a", "b"]` with no phantom empty last element, and it
handles `\r\n`/`\r` survivors too. **Paths are `str`, never `Path`** — `pathlib` is
Lesson 14, so no graded function ever sees a `Path`; the test fixtures convert with
`str(...)` at the call site, which makes the seam visible.

**The round-trip invariant, and where it holds.** *Every expense the program writes with
an amount of at most two decimals reads back unchanged.* Verified by brute force: 120,000
random 2-decimal amounts up to $10,000,000 across six category shapes (including
`"eating out"`, `"café"`, a 40-char name) → **0 mismatches**, plus 200,000 more 2-decimal
amounts sampled across the whole accepted range up to `MAX_DIGITS` → **0 mismatches**, and
200,000 random accepted shapes with zero, one or two decimals → **0 cases** where the
written form was anything the reader refuses. It holds because `is_field` and `is_amount`
gate the write side with exactly the predicates `parse_line` uses on the read side — one
validator, both directions — and because `is_amount` counts the digits *before* the point,
which is the half `format_line`'s `:.2f` cannot change. `"9" * 12` is accepted and
round-trips; `"9" * 13` is refused at the door rather than written and silently dropped
later. One shape stays open on purpose and becomes a Going further exercise, because
`is_amount` validates the string the user typed and not the float it becomes: a third
decimal is rounded on the way out (`add … tip 0.005` is stored as `0.01`).

### Edge cases, and where each is handled

| Edge case | Handled by | How |
|---|---|---|
| File does not exist yet | `load_expenses` | `if not os.path.exists(path): return []` |
| Trailing newline at EOF | `load_expenses` | `splitlines()` — no phantom last element |
| Blank / whitespace-only line | `parse_line` | `if not stripped: return None` |
| Too few / too many fields | `parse_line` | `if len(parts) != 3: return None` |
| Empty date or category | `parse_line` | `is_field` |
| Amount not a number (`lots`, `12,50`, `nan`, `-5.00`) | `parse_line` → `is_amount` | string check, no `try/except` |
| Amount with more than 12 digits before the point | `parse_line` → `is_amount` | `len(text.split(".")[0]) <= MAX_DIGITS` — the half `:.2f` cannot change, so write and read agree |
| Human spacing (`" a \| b \| 1.00 "`) | `parse_line` | strip the line, then strip each field |
| `\|` or a line break *typed by the user* | `main` → `is_field` | rejected with exit 1 **before any write** |
| Amount written as `1200` | `format_line` | `f"{amount:.2f}"` → `1200.00` |
| Windows `\r\n` | free | text-mode `open` translates; `splitlines()` catches survivors |
| Non-ASCII category | `open(..., encoding="utf-8")` | explicit encoding on both ends |

**The teachable consequence, stated on purpose.** Because `add` does load → append →
save, a line the parser skipped is *gone* after the next `add`. The deck names it and
asks the room what a real program should do (back it up? refuse to save? warn?), and it
becomes a Going further exercise.

## The CLI

### `solutions/cli.py`

```python
"""The command line: one parser, one main(), three subcommands."""

import argparse
import sys

from solutions.expense import Expense, filter_by_category, totals_by_category
from solutions.reporting import format_money, format_table
from solutions.storage import is_amount, is_field, load_expenses, save_expenses

DEFAULT_PATH = "expenses.txt"
NOTHING_FOUND = "No expenses found."
BAD_FIELD = "Date and category must not be empty or contain '|' or a line break."
BAD_AMOUNT = "Amount must be a plain number like 24.50."


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser: a global --file plus three subcommands."""
    parser = argparse.ArgumentParser(
        prog="expenses",
        description="Track expenses in a plain text file.",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_PATH,
        help=f"path to the expenses file (default: {DEFAULT_PATH})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="record a new expense")
    add.add_argument("date", help="the date, e.g. 2026-09-21")
    add.add_argument("category", help="the category, e.g. groceries")
    add.add_argument("amount", help="the amount, e.g. 24.50")

    listing = subparsers.add_parser("list", help="show every expense")
    listing.add_argument("--category", help="only show this category")

    subparsers.add_parser("report", help="show totals per category")

    return parser


def main(argv: list[str]) -> int:
    """Run one command. Returns the exit code: 0 for success, 1 for a user error."""
    args = build_parser().parse_args(argv)
    expenses = load_expenses(args.file)

    if args.command == "add":
        date = args.date.strip()
        category = args.category.strip()
        if not is_field(date) or not is_field(category):
            print(BAD_FIELD)
            return 1
        if not is_amount(args.amount):
            print(BAD_AMOUNT)
            return 1
        amount = float(args.amount)
        expenses.append(Expense(date, category, amount))
        save_expenses(args.file, expenses)
        print(f"Added {category} {format_money(amount)} on {date}.")
    elif args.command == "list":
        if args.category is not None:
            expenses = filter_by_category(expenses, args.category)
        if expenses:
            rows = [[e.date, e.category, format_money(e.amount)] for e in expenses]
            print(format_table(rows, ["DATE", "CATEGORY", "AMOUNT"]))
        else:
            print(NOTHING_FOUND)
    else:
        totals = totals_by_category(expenses)
        if totals:
            rows = [[name, format_money(totals[name])] for name in sorted(totals)]
            print(format_table(rows, ["CATEGORY", "TOTAL"]))
        else:
            print(NOTHING_FOUND)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

Shape decisions, each load-bearing:

- **`main(argv: list[str]) -> int`, no `argv=None` sentinel.** A required list makes the
  key insight visible: **a CLI is just a function that takes a list of strings and
  returns a number** — which is why the whole program is testable without a terminal,
  without a subprocess, without monkeypatching `sys.argv`.
- **`amount` is a plain `str` positional, not `type=float`.** With `type=float`,
  argparse's validator and `is_amount` disagree, so `add … nan`, `add … inf`, `add … -0`
  all print a success confirmation, write a line, and lose it on the next load. One
  validator for both directions closes all three and removes the
  separate "negative amount" branch (`is_amount("-5")` is already `False`). The cost —
  losing argparse's free exit-2 on a bad number — is bought back as a slide: *who should
  report this error, the library or you?*
- **`is_field` on date and category, before any write.** `add 2026-09-23 "food|drink" 5`
  is otherwise accepted, written as a four-field line, and silently discarded forever.
  Two `if`s, entirely taught vocabulary, and the lesson's sharpest slide: **the delimiter
  you chose is now part of your input contract.** `.strip()` first so a stray space
  normalises instead of being rejected.
- **`--file` is global** (before the subcommand, git-style), declared once. It is also
  what lets every test point at `tmp_path`. Repeating it on the subparsers was rejected:
  the subparser default silently overwrites the top-level value, which is a wrong-file
  write. The natural-but-wrong invocation fails loudly instead, and README Gotchas shows
  the exact error: `expenses: error: unrecognized arguments: --file expenses.txt`.
- **`add_subparsers(dest="command", required=True)` is given.** Pure incantation; giving
  it removes an opaque failure mode (without `required=True` the `[]` case of
  `test_a_bad_command_line_exits_with_code_two` fails with `DID NOT RAISE`, which names
  nothing) *and* makes the final bare `else:` provably safe.
- **One `if`/`elif`/`else` in one function.** At 30 lines the whole behaviour fits on one
  screen, and `args.date` sitting next to `add.add_argument("date")` is the argparse
  mental model in one glance.
- **`sorted(totals)`** makes `report` order-independent of the file — Lesson 05's
  promised "later lesson" for `sorted`, spent on one line.

### Sample data — both properties are load-bearing

The fixture ledger, in this order:

```
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
2026-09-22|groceries|10.25
```

- **`rent` is stored *before* `groceries`.** File order is not alphabetical order, so
  `test_report_totals_each_category_in_alphabetical_order` genuinely pins `sorted()`. An
  alphabetically-ordered fixture lets the `sorted(totals)` mutation survive.
- **`rent` is `1200.00`.** Four figures force a thousands separator, so the expected
  tables contain `$1,200.00`, which only `format_money` produces. A learner who inlines
  `f"${e.amount:.2f}"` writes `$1200.00` and goes red — that is what makes the black box
  a graded dependency.

### Exit codes

| Code | When | Who produces it |
|---|---|---|
| `0` | command succeeded (including "No expenses found.") | `main` returns 0 |
| `1` | a value we rejected: bad amount, or a date/category that would break the file | `main` returns 1 |
| `2` | bad command line: no command, unknown command, missing argument, misplaced `--file` | argparse calls `sys.exit(2)` |
| `1` *(+ traceback)* | the file cannot be read at all (wrong encoding, a directory), or cannot be *written* — `--file nosuchdir/expenses.txt` makes `list`/`report` print "No expenses found." and exit 0, then `add` raises `FileNotFoundError` | Python; an uncaught exception exits 1 too, so `echo $?` cannot tell a crash from a rejected value. **Catching it is Lesson 11**, and the README says so rather than pretending it cannot happen |

`echo $?` in the terminal is a live-demo beat.

### Literal output — captured from the running program

```console
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-21 rent 1200
Added rent $1,200.00 on 2026-09-21.
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-21 groceries 24.50
Added groceries $24.50 on 2026-09-21.
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-22 groceries 10.25
Added groceries $10.25 on 2026-09-22.

$ cat expenses.txt
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
2026-09-22|groceries|10.25

$ uv run python -m solutions.cli --file expenses.txt list
DATE        CATEGORY      AMOUNT
2026-09-21  rent       $1,200.00
2026-09-21  groceries     $24.50
2026-09-22  groceries     $10.25

$ uv run python -m solutions.cli --file expenses.txt list --category groceries
DATE        CATEGORY   AMOUNT
2026-09-21  groceries  $24.50
2026-09-22  groceries  $10.25

$ uv run python -m solutions.cli --file expenses.txt report
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00
```

`list` shows file order; `report` sorts. Errors:

```console
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-23 'food|drink' 5.00
Date and category must not be empty or contain '|' or a line break.
$ echo $?
1

$ uv run python -m solutions.cli --file expenses.txt add 2026-09-23 refund -5
Amount must be a plain number like 24.50.
$ echo $?
1

$ uv run python -m solutions.cli --file missing.txt report
No expenses found.
$ echo $?
0

$ uv run python -m solutions.cli --file expenses.txt
usage: expenses [-h] [--file FILE] {add,list,report} ...
expenses: error: the following arguments are required: command
$ echo $?
2

$ uv run python -m solutions.cli list --file expenses.txt     # --file in the wrong place
usage: expenses [-h] [--file FILE] {add,list,report} ...
expenses: error: unrecognized arguments: --file expenses.txt
$ echo $?
2
```

And the help argparse writes for free:

```console
$ uv run python -m solutions.cli --help
usage: expenses [-h] [--file FILE] {add,list,report} ...

Track expenses in a plain text file.

positional arguments:
  {add,list,report}
    add              record a new expense
    list             show every expense
    report           show totals per category

options:
  -h, --help         show this help message and exit
  --file FILE        path to the expenses file (default: expenses.txt)
```

## The test suite

**28 test functions, 41 collected cases, across 4 files**, all passing against the
reference solution, chunked one file per unit. Isolation and capture:

- **Filesystem:** `tmp_path`. Each of `test_storage.py` and `test_cli.py` defines
  `expenses_path(tmp_path) -> str` returning `str(tmp_path / "expenses.txt")` — a path
  that **does not exist yet**, on purpose, so the missing-file branch is the default
  state rather than a special case. `test_cli.py` adds `seeded_path`, a fixture built on
  a fixture (Lesson 04's fixture basics extended), holding the three sample lines above.
- **stdout:** `capsys.readouterr().out` compared against an exact string; multi-call
  tests drain the buffer with a bare `capsys.readouterr()` first. Every message *our* code
  prints goes to stdout; argparse writes its own usage and error text to stderr, which is
  precisely the Going further hook (`print(..., file=sys.stderr)`). No graded code touches
  `sys.stderr`, and no test asserts on the stderr path — only on the exit code.
- **Determinism:** no clock, no randomness, no network, no CWD dependence (every CLI call
  passes `--file`), `prog="expenses"` pinned so usage text is identical under pytest and
  `python -m`, and **no assertion on argparse's message wording** — only on
  `exit_info.value.code`, so a CPython wording change cannot break CI.
- **Readable expectations:** every expected table and file body is a **module-level
  triple-quoted constant**, so it reads on the page exactly as in the terminal. It is
  also the only form `ruff format` leaves alone — implicit string concatenation gets
  collapsed onto one line and destroys the alignment.

Test bodies read files back with the same recipe the learner writes — `with open(path,
encoding="utf-8") as f: f.read()` — and check absence with `os.path.exists(path)`, never
`Path.read_text()`/`Path.exists()`, so the "paths are `str`" seam holds; `test_storage.py`
and `test_cli.py` therefore `import os` (used, so no `noqa`). The shared constants and
fixtures, verbatim:

```python
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

EXPECTED_LIST = """\
DATE        CATEGORY      AMOUNT
2026-09-21  rent       $1,200.00
2026-09-21  groceries     $24.50
2026-09-22  groceries     $10.25"""

EXPECTED_LIST_GROCERIES = """\
DATE        CATEGORY   AMOUNT
2026-09-21  groceries  $24.50
2026-09-22  groceries  $10.25"""

EXPECTED_REPORT = """\
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00"""


@pytest.fixture
def expenses_path(tmp_path) -> str:
    """A path inside a fresh directory -- the file does not exist yet."""
    return str(tmp_path / "expenses.txt")


@pytest.fixture                                  # test_cli.py only
def seeded_path(expenses_path: str) -> str:
    """The three sample expenses, already on disk."""
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_FILE)
    return expenses_path


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
```

`SAMPLE_FILE` is also the exact body `test_save_expenses_writes_one_line_per_expense`
asserts. `test_load_expenses_skips_blank_and_malformed_lines` writes `MALFORMED_FILE`
(6 lines) and expects exactly `[Expense("2026-09-21", "rent", 1200.00),
Expense("2026-09-22", "groceries", 10.25)]`. `test_report_ignores_malformed_lines`
writes `"junk\n" + SAMPLE_FILE` and expects `EXPECTED_REPORT + "\n"` — byte-identical to
the clean-file report. The absence assertions read `assert not
os.path.exists(expenses_path)`. `test_reporting.py` keeps its own `EXPECTED_TABLE`; the
names differ per file, so nothing collides.

### `test_reporting.py` — 2 functions, 2 cases, **green from the first run**

| Test | Asserts |
|---|---|
| `test_format_money_shows_two_decimals_and_groups_thousands` | `format_money(24.5) == "$24.50"` and `format_money(1200) == "$1,200.00"` — the whole contract |
| `test_format_table_left_aligns_all_but_the_last_column` | an exact three-line table; shows the argument order *and* the alignment rule in one assertion |

```python
EXPECTED_TABLE = """\
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00"""


def test_format_table_left_aligns_all_but_the_last_column() -> None:
    rows = [["groceries", "$34.75"], ["rent", "$1,200.00"]]
    assert format_table(rows, ["CATEGORY", "TOTAL"]) == EXPECTED_TABLE
```

These are the black box's documentation; the module docstring, the README and slide 12
all say so.

### `test_storage.py` — 9 functions, 16 cases (red)

| Test | Asserts / why |
|---|---|
| `test_format_line_joins_the_three_fields_with_two_decimals` | `Expense(…, 24.5)` → `"2026-09-21\|groceries\|24.50"` — the format contract *and* the `:.2f` in one assertion |
| `test_parse_line_reads_the_three_fields` | whole-`Expense` equality (thanks `@dataclass`); also catches forgetting `float()` |
| `test_parse_line_strips_whitespace_and_the_newline` | `"  2026-09-21 \| groceries \| 24.50  \n"` — trailing newline *and* human spacing at once |
| `test_parse_line_rejects_unusable_lines` | **parametrized, 8 cases**: `""`, `"   \n"`, 2 fields, 4 fields, `…\|lots`, empty category, empty date, `…\|refund\|-5.00` — the last pins that `is_amount` rejects the minus sign |
| `test_load_expenses_returns_empty_when_the_file_is_missing` | `[]`, not a crash — the first-run experience |
| `test_load_expenses_skips_blank_and_malformed_lines` | a 6-line hand-written file with a leading blank, a garbage line, a bad amount and an interior blank → exactly 2 survive |
| `test_save_expenses_writes_one_line_per_expense` | exact file bytes, including the final newline |
| `test_save_expenses_replaces_the_previous_contents` | `"w"` truncates — catches using `"a"` |
| `test_save_then_load_round_trips` | the headline invariant the whole format exists to satisfy |

### `test_expense.py` — 4 functions, 4 cases (red)

A `sample_expenses` fixture: the three expenses above, in that order, two categories.

| Test | Asserts |
|---|---|
| `test_filter_by_category_keeps_only_matches` | the two groceries rows, by identity of the fixture items — list `==` is ordered, so this pins order too |
| `test_filter_by_category_unknown_category_is_empty` | `[]` |
| `test_totals_by_category_sums_each_category` | `{"groceries": 34.75, "rent": 1200.00}` — exact float equality by design |
| `test_totals_by_category_empty_list_is_empty_dict` | `{}` — drives the "start with an empty dict" shape |

### `test_cli.py` — 13 functions, 19 cases (red)

| Test | Asserts / why |
|---|---|
| `test_build_parser_defaults_the_file_and_names_the_command` | `parse_args(["report"]).file == "expenses.txt"` and `.command == "report"`; **testable without `main`**, so `build_parser` has its own green light |
| `test_add_keeps_the_earlier_expenses` | two adds → exactly two lines, in order; catches truncating on every add, and the raw file read means a storage bug cannot hide a CLI bug |
| `test_add_prints_a_confirmation` | `"Added groceries $24.50 on 2026-09-21.\n"` — pins the message. `format_money(24.5)` and an inlined `f"${24.5:.2f}"` both give `$24.50`, so it is the expected *tables* (with their `$1,200.00`) that pin the `format_money` call, as the mutation table says |
| `test_add_rejects_an_amount_that_is_not_a_plain_number` | **parametrized, 4 cases**: `"lots"`, `"-5"`, `"nan"`, `"1234567890123"` (13 digits before the point — one past `MAX_DIGITS`) → returns `1`, exact `BAD_AMOUNT`, **and the file still does not exist** |
| `test_add_rejects_a_field_that_would_break_the_file` | **parametrized, 3 cases**: a category with `\|`, a date with `\|`, a whitespace-only category → returns `1`, exact `BAD_FIELD`, file untouched; the third pins the `.strip()` |
| `test_list_prints_a_table_of_every_expense` | the exact 4-line table, in file order |
| `test_list_filters_by_category` | `--category groceries` → header + two rows, column widths re-computed on the filtered set |
| `test_list_on_a_missing_file_says_nothing_found` | `"No expenses found.\n"`, exit 0 — empty is not an error |
| `test_list_with_an_unknown_category_says_nothing_found` | the same message reached through the *filter*, on a non-empty file — catches filtering and then printing a bare header |
| `test_report_totals_each_category_in_alphabetical_order` | exact table; the fixture stores `rent` first, so this is a real `sorted()` test |
| `test_report_on_a_missing_file_says_nothing_found` | the empty-report branch, separate learner code from `list`'s |
| `test_report_ignores_malformed_lines` | a file with `junk` on line 1 still reports — end-to-end proof that the skip policy reaches the user |
| `test_a_bad_command_line_exits_with_code_two` | **parametrized, 2 cases**: `[]` (no subcommand) and `["add", "2026-09-21"]` (missing positionals, so `add` really declares three); `pytest.raises(SystemExit)` and `exit_info.value.code == 2` |

### Mutation results

**15 mutations of the reference solution were applied and the suite re-run; every one was
killed:** (1) `"a"` instead of `"w"`; (2) a dropped `"\n"`; (3) a dropped `:.2f`; (4) a
dropped `os.path.exists` guard; (5) a forgotten `float()`; (6) a dropped per-field
`.strip()`; (7) `parse_line` drops its `is_amount` guard; (8) `parse_line` drops its
`is_field` guards; (9) `main`'s `add` drops `is_amount`; (10) `main`'s `add` drops
`is_field`; (11) an unsorted `report`; (12) `list` drops its empty-check; (13) `report`
drops its empty-check; (14) an ignored `--category`; (15) an inlined `f"${x:.2f}"`.
Two drove design changes rather than being asserted away:

| Mutation that initially survived | Fix |
|---|---|
| `main` iterates `totals` instead of `sorted(totals)` | store `rent` before `groceries` in the fixtures, so file order ≠ alphabetical order |
| `main` inlines `f"${x:.2f}"` instead of calling `format_money` | add the `rent 1200.00` row, so the expected table needs a thousands separator |

## The red start

**First run: `39 failed, 2 passed`.** The 2 green are `test_reporting.py` — deliberately
green, executable documentation for the black box. Every test of learner-written code is
red.

Every stub is *importable* and raises at call time, not at import time — a deliberate
departure from Lesson 07's `ImportError` at collection: with 41 cases, an all-or-nothing
import gate would hide the progress bar that makes a capstone feel finishable. The names
are the to-do list. The eight stub messages:

```
NotImplementedError: implement format_line() so the tests pass
NotImplementedError: implement parse_line() so the tests pass
NotImplementedError: implement load_expenses() so the tests pass
NotImplementedError: implement save_expenses() so the tests pass
NotImplementedError: implement filter_by_category() so the tests pass
NotImplementedError: implement totals_by_category() so the tests pass
NotImplementedError: implement build_parser() so the tests pass
NotImplementedError: implement main() so the tests pass
```

### Stub docstrings name the technique

The repo's most consistent teaching convention (Lesson 05: *"using `enumerate`"*;
Lesson 07: *"use `math.hypot`"*), and it matters more here than anywhere because five of
the eight stubs need an API that has never appeared in this repo.

**Construction rule for six of the eight stubs:** the stub is the solution's signature
and docstring exactly as printed above, with the paragraph below appended to the
docstring and the body replaced by `raise NotImplementedError("implement <name>() so the
tests pass")`. The appended paragraphs, verbatim:

```text
format_line
    One f-string: date, category and amount joined by SEPARATOR, with the
    format spec `:.2f` on the amount so 1200 is written as 1200.00.

parse_line
    Start with `line.strip()` and return None when nothing is left. Cut the
    rest with `.split(SEPARATOR)`, strip each field (a list comprehension does
    both in one line), and return None unless there are exactly 3. Then check
    the date and the category with is_field() and the amount with is_amount()
    before returning `Expense(date, category, float(amount))`.

load_expenses
    A missing file is not an error: check with `os.path.exists(path)` first and
    return []. Otherwise read the whole file with
    `with open(path, encoding="utf-8") as f: text = f.read()`, cut it into
    lines with `text.splitlines()`, and keep every line parse_line() accepts --
    it returns None for the ones it rejects, so the check is
    `if expense is not None:`.

save_expenses
    Open it with `with open(path, "w", encoding="utf-8") as f:` -- mode "w"
    replaces the whole file -- then f.write() one format_line() per expense.
    write() does not add the line break at the end; you do.

filter_by_category
    One list comprehension with an `if` filter (Lesson 05).

totals_by_category
    Start with an empty dict `totals = {}` and loop: read the running total
    with `totals.get(expense.category, 0.0)` (Lesson 05), add this expense's
    amount, and write it back with `totals[expense.category] = ...` -- writing
    a dict key is `d[k] = v`, the half of dicts Lesson 05 did not show.
```

**Note for the implementer:** no stub docstring may contain a literal `\n` escape —
inside a plain (non-raw) docstring it becomes an actual line break. That is why
`save_expenses` says "the line break" in prose.

### `build_parser` — real given code, three subcommands to write

The two non-obvious pieces of argparse here are `dest=`/`required=` (pure incantation)
and the difference between a positional and an option on a subparser (the actual skill).
So the incantation is **given as working code** and the learner writes **all three**
`add_parser` blocks, including the fiddly optional `--category`.

```python
# exercises/cli.py

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser: a global --file plus three subcommands.

    The parser itself, the global --file option and the subparsers object are
    written out below. Your job is the three subcommands:

      add     three positional arguments -- date, category, amount -- all plain
              strings (main() validates them, so no type= here)
      list    no positionals, one optional --category option
      report  no arguments at all

    Each one starts with `subparsers.add_parser("<name>", help="...")`; the
    README and slide 9 show the `add` block in full. Finish with
    `return parser`.
    """
    parser = argparse.ArgumentParser(
        prog="expenses",
        description="Track expenses in a plain text file.",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_PATH,
        help=f"path to the expenses file (default: {DEFAULT_PATH})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)  # noqa: F841 -- you use it
    raise NotImplementedError("implement build_parser() so the tests pass")
```

The worked `add` block lives in the README's Exercise section and on slide 9 as real
copy-pasteable code — *not* as indented prose inside a docstring, which produces an
`IndentationError` the moment a beginner pastes it.

### `main` — skeleton plus the exact strings

```python
# exercises/cli.py

def main(argv: list[str]) -> int:
    """Run one command. Returns the exit code: 0 for success, 1 for a user error.

    argv is the argument list WITHOUT the program name, e.g.
    ["--file", "expenses.txt", "add", "2026-09-21", "groceries", "24.50"].

    The shape:
      1. args = build_parser().parse_args(argv)   (replace the bare call below)
      2. expenses = load_expenses(args.file)
      3. if args.command == "add" / elif "list" / else report
      4. return 0, or 1 when you reject what the user typed

    add     .strip() the date and the category first. print(BAD_FIELD) and
            return 1 when is_field() rejects either of them; print(BAD_AMOUNT)
            and return 1 when is_amount() rejects the amount. Otherwise append
            an Expense to the list you loaded, save the whole list back with
            save_expenses(), and print exactly (the amount goes through
            format_money()):
            Added groceries $24.50 on 2026-09-21.
    list    filter with filter_by_category() when args.category is not None,
            then build one row per expense -- three strings, shaped
            [date, category, format_money(amount)], because format_table only
            aligns strings -- and print(format_table(rows, ["DATE",
            "CATEGORY", "AMOUNT"]))
    report  totals_by_category(), one row per category in `sorted(totals)`
            order, headers ["CATEGORY", "TOTAL"]

    list and report both print(NOTHING_FOUND) when there is nothing to show.
    """
    build_parser().parse_args(argv)
    raise NotImplementedError("implement main() so the tests pass")
```

That bare `build_parser().parse_args(argv)` call is load-bearing, and it is a bare
expression rather than `args = …` on purpose: an assignment would trip ruff F841, while a
bare call is ruff-clean (B018 does not flag function calls). It means **`--help` works
the instant `build_parser` is done**, before `main` exists. Verified: with only
`build_parser` implemented, the suite goes **2 passed → 5 passed** and

```console
$ uv run python -m exercises.cli --help        # main still raises!
usage: expenses [-h] [--file FILE] {add,list,report} ...
...
$ uv run python -m exercises.cli bogus
usage: expenses [-h] [--file FILE] {add,list,report} ...
expenses: error: argument command: invalid choice: 'bogus' (choose from 'add', 'list', 'report')
$ echo $?
2
```

### F401/F841 in the red start

Stripping every `# noqa` and re-running ruff produces **exactly 11 diagnostics on 5
lines**, all handled inline following Lesson 07's precedent — no config change, because
the wart belongs next to the code the learner reads:

```python
# exercises/storage.py
import os  # noqa: F401 -- os.path.exists() is for load_expenses()

# exercises/cli.py
from exercises.expense import Expense, filter_by_category, totals_by_category  # noqa: F401
from exercises.reporting import format_money, format_table  # noqa: F401
from exercises.storage import is_amount, is_field, load_expenses, save_expenses  # noqa: F401
...
    subparsers = parser.add_subparsers(dest="command", required=True)  # noqa: F841 -- you use it
```

`# noqa` is line-scoped, so three grouped imports cover nine names in three comments. No
noqa is needed for `argparse` (used in `build_parser`'s return annotation), `sys` (used
in the shipped `__main__` block), `Expense` in `storage.py` (used in signatures) or
`dataclass` — **ruff counts annotations as usage**. `exercises/cli.py`'s module docstring
explains the pragmas and tells the learner to delete them once every name is used.
Longest of the five lines: 97 chars. RUF100 is not in the repo's select list, so the
comments do not start failing `make lint` once the learner finishes.

## The feedback ladder

The spine of the design; it belongs on slide 12 and in the README, in this order, headed
by its own line `cd lessons/08-capstone-cli` — every command below is relative to the
lesson folder. Run from the repo root (where `make test-lesson` was just run) step 0
gives `ERROR: file or directory not found: exercises`, because the root `testpaths` is
`tools`, and step 5 gives `No module named exercises`.

| Step | Command | What you get |
|---|---|---|
| 0 | `uv run pytest exercises -q --tb=line` | `39 failed, 2 passed`, one line each. `--tb=line` prints one line per *failure*, so open `exercises/test_reporting.py` — those 2 green tests are your library. |
| 1 | `uv run pytest exercises/test_storage.py -k format_line` | **One line of code** goes green. First win inside 3 minutes. |
| 2 | `… -k parse_line` | 10 cases. The parametrized list *is* the spec for bad lines. |
| 3 | `… -k "load or save or round_trip"` | 5 more. Now try it outside pytest: `uv run python -c "from exercises.storage import load_expenses; print(load_expenses('nope.txt'))"` → `[]` |
| 4 | `uv run pytest exercises/test_expense.py -k filter` | 2 more. Pure functions, no I/O, fastest wins in the lesson. |
| 5 | `uv run pytest exercises/test_cli.py -k build_parser`, then **`uv run python -m exercises.cli --help`** | 3 more — 23 passing (the `build_parser` case, plus the 2 exit-code cases that reach argparse through `main`'s bare `parse_args`) — and the thing prints real help. It is a program now. |
| 6 | `… -k add` | 9 cases. The `add` branch of `main` lights its own tests. |
| 7 | `uv run python -m exercises.cli --file my.txt add 2026-09-21 coffee 4.50` | Run your own program. `cat my.txt`. `echo $?`. |
| 8 | self-study: `main`'s `list` branch, then `totals_by_category`, then `main`'s `report` branch | 4 cases, then 2, then 3 — the last 9, and the lesson is green. |

Deliberate ordering: **inside-out.** Storage and domain first (built entirely from
lessons 01-07 vocabulary), CLI last (the one alien API, but by then everything it calls
is proven). The learner never debugs two unknowns at once.

## Session fit (~90 minutes)

Fits, with a pre-declared **core** (storage ×4 and `filter_by_category` ~32 min,
`build_parser` ~16 min live-coded together, `main`'s `add` branch plus running it ~12 min
— ~60 min of working time) / **stretch**, done as self-study (`main`'s `list` branch
~6 min, `totals_by_category` ~7 min, `main`'s `report` branch ~5 min, plus 15-20 min
running it for real and picking up a Going further) split. The stretch tier is everything
purely *additive*: `list` and `report` only display what `add` already writes, so stopping
at the end of the session leaves a program that genuinely runs — it takes a real expense,
writes a real file and prints a real confirmation — rather than a half-wired one. **Every
learner leaves with their own CLI running**, which is the point of the 74-86 block.

| Minutes | Activity |
|---|---|
| 0-8 | Slides 1-2 and a **live demo of the finished CLI** — they see the goal running before they build it |
| 8-26 | Slides 3-8: shape, the record, files, bad lines, the black box, money/dates/order |
| 26-58 | **Hands-on: `storage.py`** (4 functions) **and `filter_by_category`**. Target: `test_storage.py` green, 16 cases, plus the 2 filter cases |
| 58-74 | Slides 9-10 (argparse, `main(argv)`), then **live-code `build_parser` together on the projector**, learners typing along. Run `--help`. Watch 3 more go green — 23 passing |
| 74-86 | **`main`'s `add` branch only.** Everyone runs `add` against their own file, `cat`s it, checks `echo $?` |
| 86-90 | Slides 11-12: the Phase 1 recap, the ladder, `list`/`report` as self-study, what's next |

**The only in-session cut lever**, usable at minute 45 in one sentence: drop `--category`
— skip `filter_by_category` and the `--category` option, and `list` (already self-study)
becomes unconditional. That buys back ~8 minutes of the 26-58 hands-on block, and it is
the only lever left now that `list` itself sits in the stretch tier. It costs four red
tests: the two the room would otherwise have turned green in session
(`test_filter_by_category_keeps_only_matches` and
`test_filter_by_category_unknown_category_is_empty`), plus `test_list_filters_by_category`
and `test_list_with_an_unknown_category_says_nothing_found` in the self-study tier — and
those last two fail with `SystemExit: 2` (argparse rejects the undeclared `--category`
before `main` runs) rather than with a wrong-output diff. Every other cut considered
(shipping `save_expenses`, shipping `build_parser`) requires editing `exercises/`,
`solutions/`, test files and the README mid-session, so it is a pre-session decision, not
a recovery lever.

## README outline

Standard six-section README, Lesson 07 shape (the four-file convention: README, slides,
exercises, solutions).

1. **Learning goals** (5 bullets) — split a program across modules whose dependencies
   point one way; read and write a plain text file with `open`, `read`, `write`, `with`;
   turn text into objects and back, and decide what to do with input that does not fit;
   build a subcommand CLI with `argparse` and return a meaningful exit code; use a
   package you did not write by reading its docstrings, not its source.
2. **Prereqs** — Lessons 01-07, one joined bullet with full titles and relative links
   (matching 03-07).
3. **Concepts**
   - *The shape of a program* — four units, one-way dependencies; `cli.py` is the only
     file that knows about all of them.
   - *A line is a record* — `Expense` as a `@dataclass`; the date as a `str` (no clock);
     the `|` format; `SEPARATOR` as a shared constant; writer and reader are one
     contract; why not JSON or CSV yet (Lesson 14).
   - *Strings are objects with methods* — `"a|b|c".split("|")`, `" x \n".strip()`,
     `"a\nb\n".splitlines()`, `if line.strip():` as a truthiness check, and
     `date, category, amount = parts` to unpack the three pieces into three names. The
     first string methods in the course; their own subsection because `parse_line` needs
     them.
   - *Files* — `with open(path, encoding="utf-8") as f: text = f.read()`; `"w"`
     truncates, `"a"` appends; you write the newline yourself —
     `f.write(format_line(expense) + "\n")`; always pass `encoding`;
     `f"{amount:.2f}"` so the file round-trips; what `with` buys you (recipe now,
     Lesson 13 for the machinery).
   - *When there is no file* — `os.path.exists(path)` and a plain `if` → `[]`;
     look-before-you-leap, with Lesson 11 showing the other style.
   - *Lines that are not expenses* — the six unusable shapes (blank; too few fields; too
     many fields; empty date; empty category; an amount that is not a plain number), the
     same six the 8 parametrized cases cover and the same six slide 6 lists; `parse_line`
     returns `None`; the loader skips; `load → save` drops the skipped line — is that
     right?
   - *Validating what the user types* — the delimiter is part of your input contract;
     `is_field`/`is_amount` gate the write side with the read side's rules; why
     `type=float` was *not* used and who should own an error message.
   - *A black box you did not write* — how to import it, how to read
     `help(format_table)`, the rule not to open `money.py`/`table.py`, and "every cell
     you hand `format_table` must already be a string — that is what `format_money` is
     for".
   - *Ordering output* — `sorted(iterable)` returns a new sorted list; iterating a dict
     gives its keys, so `sorted(totals)` is the categories alphabetically. (Lesson 05
     promised `sorted` "in a later lesson" — here it is.)
   - *Building a dict by hand* — Lesson 05 built dicts with comprehensions and read them
     with `.get`; here you need the write half, `d[k] = v`, in a plain `for` loop:
     `totals[category] = totals.get(category, 0.0) + amount`.
   - *argparse* — parser, `add_subparsers(dest="command", required=True)`, positionals vs
     `--options`, a global `--file`, free `--help`, exit code 2.
   - *`main(argv) -> int`* — a CLI is a function that takes a list of strings and returns
     a number; that is why it is testable; `sys.exit(main(sys.argv[1:]))`.
   - *How to read the test files* — `tmp_path` (a fresh empty directory per test;
     `tmp_path / "expenses.txt"` builds a path inside it — that `/` is `pathlib`,
     Lesson 14, which is why the fixture wraps it in `str(...)` before your code ever
     sees it), `capsys` (`capsys.readouterr().out` is what your program printed), and
     `pytest.raises` — not a fixture but a `with` block:
     `with pytest.raises(SystemExit) as exit_info:` / `main([])` /
     `assert exit_info.value.code == 2`, because argparse ends the program itself. Also:
     a fixture may ask for another fixture (`seeded_path` asks for `expenses_path`). All
     of this is given; you never write it. The tests pin exact output strings — read them
     as the spec.
   - *One new note on types* — `Expense | None` means "an `Expense` or `None`"; the
     runtime check is `if x is not None:`, never `x != None` (that passes the tests and
     then fails `make lint` with `E711`); types get taught properly in Lesson 09.
   - *Gotchas* — `--file` goes **before** the subcommand; the `# noqa: F401` comments
     mark deliberately-unused imports, delete them once everything is used; a `--file`
     path whose directory does not exist looks fine to `list` and `report` (they print
     "No expenses found." and exit 0) and then crashes on `add`; a file the
     program cannot read at all still crashes with a traceback, and catching that is
     Lesson 11.
4. **Exercise** — the 8 functions grouped by module, **in the recommended order**, the
   feedback-ladder table, the `add` subparser written out verbatim as the worked example
   for `build_parser`, the explicit core/stretch split, and the line: *"Your first run
   says `39 failed, 2 passed`. The 2 that pass are the `reporting` package you were
   given."*
5. **How to run** — `make test-lesson LESSON=08-capstone-cli`; the quiet first run
   (`uv run pytest exercises -q --tb=line`); per-file runs; the full terminal transcript
   above using `--file expenses.txt`; `echo $?`;
   `uv run python -c "from solutions.reporting import format_table; help(format_table)"`.
6. **Going further**
   - Add a grand-total row to `report` — the table aligns it for you.
   - `open(path, "a")` appends; make `add` use it, and say what you lose.
   - A skipped line disappears on the next `add`. Fix it: back the file up, refuse to
     save, or warn.
   - Real CLIs send errors to stderr: `print(msg, file=sys.stderr)`. Why is that better?
   - Money in `float` is a lie (`0.1 + 0.2`). Try `add … tip 0.005` and `add … tip 1.005`
     — they are stored as `0.01` and `1.00`, so what you typed is not what comes back.
     Where did your half-cent go, and why did the two round in opposite directions?
     `decimal.Decimal` is the real answer.
   - `str.isdigit()` vs `isdecimal()` vs `isnumeric()` — why `is_amount` uses `isdecimal`
     (`"²".isdigit()` is `True`, but `float("²")` raises). Then read the other half of
     `is_amount`: why does it count the digits *before* the point? Delete that check and
     try a 20-digit amount — `float()` reads it, `format_line` writes it, and the next
     `load` refuses it, so your `add` reports success for a line `list` cannot see and
     your next `add` deletes it.
   - `format_table` raises `ValueError` on a ragged row — a real library validates its
     input. Catching that is Lesson 11.
   - `argparse`: `type=`, `choices=`, `nargs=`, mutually exclusive groups, `%(prog)s`.
   - `console_scripts` in `pyproject.toml` turn `main` into a real `expenses` command
     (Lesson 15). Real dates (`datetime`) and real paths (`pathlib`) — Lesson 14.

## Slides (`slides/slides.md`)

Twelve slides, `---` separated, Lesson 06/07 style (~6 bullets and ≤15 visible code lines
each).

1. **Title** — "Lesson 08 — Phase 1 capstone: expense tracker CLI"; *seven lessons of
   parts, one program.*
2. **What we're building** — live demo first: one `add`, one `list`, one `report` on the
   projector, six lines of transcript on the slide.
3. **The shape of a program** — the module map as a fenced `text` block; four units,
   one-way arrows, nothing imports `cli`.
4. **A line is a record** — `2026-09-21|groceries|24.50`; `format_line` and `parse_line`
   side by side; `SEPARATOR` so writer and reader cannot disagree; `.split`/`.strip`.
5. **Files: open, read, write** — `with open(...)` as a recipe; `"w"` truncates, `"a"`
   appends; you write the newline; `.splitlines()`; *Lesson 13 shows how `with` works.*
6. **Lines that aren't expenses** — the six shapes; `parse_line` returns `None`; missing
   file → `os.path.exists` → `[]`; plain `if`, not `try/except`. *And the skipped line is
   gone after your next `add` — is that OK?*
7. **A black box you didn't write** — import the two names, read the docstring not the
   source, `help(format_table)` live; every cell must already be a string.
8. **Money, dates and order** — money in `float` is a lie, so we only *display* it
   through `format_money`; the date is a `str`, so no clock; `sorted(totals)`; and the
   line that builds the dict, `totals[category] = totals.get(category, 0.0) + amount` —
   `d[k] = v` is the half of dicts Lesson 05 did not show.
9. **argparse: three subcommands** — the parser tree, the `add` block verbatim,
   positionals vs options, `--file` is global and goes first, `--help` free, exit 2.
   *Why `amount` is a plain string and not `type=float`: whose error message is it?*
10. **`main(argv)` is just a function** — a list of strings in, an exit code out; that is
    why it is testable (`tmp_path`, `capsys`, `pytest.raises`); exit codes 0 / 1 / 2.
11. **Phase 1 in one program** — the recap: `print` and `python -m` (01), f-strings and
    format specs (02), `if`/`for`
    (03), functions and pytest (04), comprehensions and `dict.get` (05), `@dataclass`
    (06), a package with `__init__.py` re-exports (07) — all in the file you finish today.
    (The `if __name__ == "__main__":` guard from Lesson 01 is already on screen at the
    bottom of `cli.py`, so it needs no extra exhibit.)
12. **Your turn / What's next** — the ladder; `39 failed, 2 passed` is the correct first
    result and the 2 are the library; next is Phase 2 — Lesson 09, type hints & mypy.

Slide 3's module map is a fenced `text` block (like Lesson 07's package-tree slide), not
an SVG asset:

```text
expense.py    what an expense is      (imports nothing)
storage.py    where it lives          (imports expense)
reporting/    how it looks            (imports nothing)
cli.py        how you drive it        (imports all three)

expense.py ──┐
storage.py ──┼──▶ cli.py     nothing imports cli.py
reporting/ ──┘
```

Deck `<title>` hand-set to "Lesson 08 — Phase 1 capstone: expense tracker CLI" (the slug
gives "Capstone Cli"; edit like Lessons 04/06/07).

## Verification (success criteria)

Already executed against the prototype with the repo's `uv` environment and real root
`pyproject.toml`:

| Check | Expected | Observed |
|---|---|---|
| `uv run pytest solutions` | 41 passed | `41 passed in 0.07s` |
| `uv run pytest exercises` | 39 failed, 2 passed, no collection error | `39 failed, 2 passed in 0.08s` |
| `uv run pytest exercises solutions` (one process) | no `import file mismatch` | `39 failed, 43 passed` |
| `uv run ruff check` (E,W,F,I,UP,B,SIM,TID; line-length 100) | clean on both trees | `All checks passed!` |
| `uv run ruff format --check` | clean on both trees | `22 files already formatted` |
| F401/F841 set with every `noqa` stripped | 5 lines | 11 diagnostics on 5 lines |
| Longest line | < 100 | 97 (an exercise `noqa` line); 96 in `test_storage.py` |
| Full transcript in "Literal output" | reproduces byte for byte | yes |
| With only `build_parser` implemented | `--help` prints usage, exit 0; suite `5 passed` | yes |
| Round-trip: 120,000 random amounts × 6 category shapes | 0 mismatches | `mismatches: 0 of 120000` |
| Round-trip: 200,000 random 2-decimal amounts across the whole accepted range | 0 mismatches | `mismatches: 0 of 200000` |
| Round-trip: 200,000 random accepted shapes with 0, 1 or 2 decimals | every accepted text writes a form the reader also accepts, value preserved | `violations: 0` |
| `is_amount`'s `MAX_DIGITS` cap | `"9" * 12` accepted, `"9" * 13` rejected; `inf` unreachable | yes |
| 15 mutations of the reference solution | every one killed | yes |

Remaining criteria for the implementation PR:

- `make test-lesson LESSON=08-capstone-cli` → exercises `39 failed, 2 passed`; solutions
  41 passed; exit 0.
- `make test` → tools + Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10), 06 (11),
  07 (7), 08 (**41**) all pass in isolated per-lesson processes; no `import file
  mismatch`.
- `make lint` and `uv run ruff format --check .` → clean repo-wide (absolute imports
  satisfy TID252).
- `make typecheck` unchanged — tools only. Lesson code is annotated as house style but is
  not a gate; strict lesson typing starts at Lesson 09.
- `make sync` picks up the new workspace member via the `lessons/*` glob; `uv.lock`
  regenerated and committed.
- `make slides-build` → `dist/index.html` links `08-capstone-cli`; Phase 1 shows fully
  green; the future-placeholder count drops to **20**; absolute `/shared/reveal/...`
  asset paths; deck renders.

### Repo changes outside the lesson folder

One line in `.gitignore`, **unanchored** so it also covers a learner running the demo
from the repo root:

```gitignore
# Lesson 08 capstone: the learner's local expense file
expenses.txt
```

Plus the regenerated `uv.lock`: `make sync` adds two `lesson-08-capstone-cli` entries (the
workspace-members list and a `[[package]]` stanza) and no dependency changes — commit it,
the way Lessons 01-07 are already recorded there. Nothing else. The catalog already lists
`08` / `capstone-cli` / "Phase 1 capstone — CLI"
/ "argparse · files · multi-module", so there is no catalog change, and no ruff config
change is needed (absolute imports satisfy TID252, the five pragmas are inline, and
`SIM108` is already ignored under `lessons/**`).

## Non-goals

- No `json`, `csv`, `pathlib`, `datetime` or `Decimal` in graded code (Lesson 14). Paths
  are `str`, dates are `str`; the only `pathlib` is one `tmp_path / "…"` in two fixtures,
  wrapped in `str(...)`.
- No `try`/`except` anywhere, including given code (Lesson 11).
- No `Protocol`/ABC, no generators, no decorators, no *writing* a context manager
  (Lessons 10, 12, 13). `with` is consumed, never authored.
- No type-hint enforcement — signatures are annotated as house style, as in Lessons
  06/07, but `mypy --strict` on lesson code starts at Lesson 09.
- No third-party packages, no `uv add`.
- No `edit`/`delete` subcommands, date filters, config file, colours, `--json`, or
  interactive mode. No `console_scripts` entry point (Lesson 15), no `__main__.py`, no
  `conftest.py` (Lesson 15), no `set_defaults(func=…)` dispatch.
- No `print(..., file=sys.stderr)` in graded code (argparse's own usage and error text
  does go to stderr). No escaping or quoting of `|` inside a field — it is rejected
  instead, and *why* real formats quote is Lesson 14's opening slide.
- No concurrency, locking, or crash-safe writes; `save_expenses` truncates and rewrites.
- No tests for the `reporting` internals beyond its 2 documentation tests, and no
  assertions on argparse's own message wording — exit codes only.
- No SVG assets — slide 3's module map is a fenced `text` block.
- No tooling, Makefile, ruff-config, mypy-scope or catalog changes. The only files touched
  outside `lessons/08-capstone-cli/` are `.gitignore` and the regenerated `uv.lock`.

## Open items deferred to implementation planning

- Exact slide prose and README wording.
- The deck `<title>` is hand-set (the slug gives "Capstone Cli"; edit like Lessons
  04/06/07).
