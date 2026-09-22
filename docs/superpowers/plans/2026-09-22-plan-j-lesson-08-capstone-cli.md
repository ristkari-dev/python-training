# Plan J — Lesson 08 (Phase 1 capstone: expense tracker CLI)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. `scripts/task-brief` extracts ONLY the `## Task N` section, so paste the **Global Constraints** block into every implementer dispatch alongside the brief path. **Extractor guard:** the Task 5 and Task 6 payloads are 4-backtick fences containing 3-backtick blocks, and `task-brief` flips its fence flag on *any* line starting with three backticks — the parity works out today. After ANY edit to this plan, re-run `scripts/task-brief` for tasks 1-7 and confirm all seven succeed; "task 6 not found" / "task 7 not found" means an edit added or removed a fenced block inside one of those two payloads.

**Goal:** Author the eighth course lesson — the Phase 1 capstone: an expense tracker CLI (`add`, `list --category`, `report`) over a pipe-delimited plain-text ledger. The learner writes 8 functions across `expense.py`, `storage.py` and `cli.py` (~70 lines) and imports a complete `reporting` package they are told not to edit. 4 modules, 4 test files, 28 test functions, 41 collected cases; the first exercise run is `39 failed, 2 passed`.

**Architecture:** Scaffold `lessons/08-capstone-cli/` with `new_lesson`, delete the placeholder `main.py`/`test_main.py`, and author four units per tree: a given `reporting` sub-package (`money.py`, `table.py`, `__init__.py`), `expense.py` (given `Expense` dataclass + 2 graded functions), `storage.py` (given constants/predicates + 4 graded functions) and `cli.py` (given constants, parser head and `__main__` block + 2 graded functions), with one test file per unit. Absolute imports only (`exercises.` / `solutions.` prefix) — the repo's ruff bans relative imports (TID252), so no ruff change is needed and none is made. Author README + deck. Eighth lesson, so `make test` now spans eight lessons and Phase 1 goes fully green on the landing page.

**Tech Stack:** Python 3.13, uv workspace, pytest 9.0.3, ruff 0.15.14, mypy, GNU Make, `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored). Lesson code is stdlib-only: `argparse`, `os.path`, `dataclasses`, `sys`.

**Spec:** docs/superpowers/specs/2026-09-22-lesson-08-capstone-cli-design.md

---

## Global Constraints

Project-wide requirements from the spec. Every one of them applies to every task below.

- **Stdlib only.** No third-party packages, no `uv add`, no new dependencies. Lesson imports are limited to `argparse`, `sys`, `os`, `dataclasses` (+ `pytest` in test files).
- **ruff config is `select = ["E", "W", "F", "I", "UP", "B", "SIM", "TID"]` at `line-length = 100`, `target-version = "py313"`, `quote-style = "double"`** — inherited from the repo root `pyproject.toml`. Do NOT change the ruff config; `SIM108` is already ignored under `lessons/**` and `RUF100` is not selected (so `# noqa` comments do not start failing once the learner finishes).
- **TID252 (`ban-relative-imports = "all"`) means every intra-lesson import is absolute.** Consequence: the exercise and solution copies of `reporting/__init__.py`, `storage.py`, `cli.py` and all four test files differ by the `exercises.` / `solutions.` prefix — that is intended, not a bug. Measured: `reporting/money.py` and `reporting/table.py` are byte-identical between trees; `reporting/__init__.py` and `test_storage.py` differ by 2 import lines each; the other three test files by 1.
- **`make typecheck` is tools-only** (`uv run mypy tools/new_lesson/src tools/slides_dev/src tools/build_index/src`). Lesson code is annotated as house style but is NOT a mypy gate — strict lesson typing starts at Lesson 09. Lesson code must be `ruff`-clean.
- **No `try`/`except` anywhere, including given code.** Lesson 08 is a pure LBYL program: a missing file is `if not os.path.exists(path): return []`, a bad amount is the given `is_amount` string check. `try`/`except` is Lesson 11.
- **No `pathlib`, `json`, `csv`, `datetime` or `decimal.Decimal` in lesson code.** Paths are `str`, dates are `str`. The only `pathlib` in the lesson is `tmp_path / "expenses.txt"` inside two fixtures, wrapped in `str(...)` at the call site.
- **No generators, no decorators (beyond the given `@dataclass`), no `Protocol`/ABC, no writing a context manager.** `with` is consumed, never authored.
- **`with open(...)` is used, and taught as a recipe:** "`with` opens the file and guarantees it gets closed when the block ends — even if something goes wrong inside. That is all you need today. Lesson 13 shows you how `with` works and how to write your own."
- **Commit messages: Conventional Commits. Do NOT add a `Co-Authored-By` trailer or any AI-attribution line.** Subject (+ optional body) only.
- **Do NOT push and do NOT open a PR** — the controller finishes the branch.
- **Branch: `lesson-08-capstone-cli`, created from an up-to-date `main`** (a `main` that already contains Lesson 07). Every task's first step confirms the branch.
- **Files touched outside `lessons/08-capstone-cli/`: exactly two** — `.gitignore` (a two-line block: a `# Lesson 08 capstone: ...` comment plus an unanchored `expenses.txt` pattern, Task 7) and the regenerated `uv.lock` (Task 1). No catalog, Makefile, ruff-config or mypy-scope changes.
- **Working directory:** every command runs from the repo root of the `lesson-08-capstone-cli` branch (a worktree counts), except the ones written `( cd lessons/08-capstone-cli && ... )`, which must run inside the lesson folder — that is where pytest's `pythonpath = ["."]` makes `exercises.` / `solutions.` importable. `uv run pytest exercises` from the repo root gives `ERROR: file or directory not found: exercises`, because the root `testpaths` is `tools`.

---

## Context for the implementer

- **Repo state:** Plans A–I merged; Lessons `01-hello` … `07-modules` are on `main` and are the pattern. Mirror `lessons/06-classes/` and `lessons/07-modules/` for file shapes and deck style.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`, members `lessons/*` + `tools/*`). Run it right after scaffolding; it picks up the new member via the `lessons/*` glob and regenerates `uv.lock` (two `lesson-08-capstone-cli` entries: the workspace-members list and a `[[package]]` stanza, no dependency changes). Commit the lock in Task 1.
- **`make new-lesson NAME=08-capstone-cli`** produces `pyproject.toml` (name `lesson-08-capstone-cli`, `description = "Lesson 08: Capstone Cli"`, `package = false`, pytest `pythonpath = ["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}`. It prints `created lessons/08-capstone-cli`. The scaffolder derives the deck title from the slug ("Capstone Cli") and emits **absolute** `/shared/reveal/...` asset paths (do not change those). Leave `pyproject.toml` unmodified.
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("08", "capstone-cli", "Phase 1 capstone — CLI", "argparse · files · multi-module", 1)`. Once `lessons/08-capstone-cli/slides/` exists, `build_index` renders it as a link and Phase 1 shows fully green. **No catalog change.**
- **The deck `<title>` needs hand-editing.** The scaffolder writes `<title>Lesson 08 — Capstone Cli</title>`; Task 6 replaces it with `<title>Lesson 08 — Phase 1 capstone: expense tracker CLI</title>` (em-dash U+2014), exactly as Lessons 04/06/07 did.
- **Landing page placeholders:** the catalog holds 28 lessons and 7 are published today, so `dist/index.html` currently shows 21 `class="lesson future"` placeholders. After this lesson lands the count is **20**.
- **Typing gate:** `make typecheck` is scoped to `tools/` only; lesson code is not a mypy gate yet (starts Lesson 09). Lesson code must be `ruff`-clean.
- **Package naming:** the given package is `reporting` (a sub-package of `exercises`/`solutions`) with modules `money.py` and `table.py`; the three flat modules `expense.py`, `storage.py`, `cli.py` and the four test files sit at the lesson's `exercises/` / `solutions/` top level, siblings of `reporting/`.
- **Every command runs from `/Users/ristkari/code/private/python-training/`**, except the ones written as `( cd lessons/08-capstone-cli && ... )`, which run inside the lesson folder (that is where `pythonpath = ["."]` makes `exercises.` / `solutions.` importable). Running `uv run pytest exercises` from the repo root gives `ERROR: file or directory not found: exercises` — the root `testpaths` is `tools`.
- **Design spec:** `docs/superpowers/specs/2026-09-22-lesson-08-capstone-cli-design.md`. Every code block in this plan is reproduced from it (and re-verified against a running prototype); you should not need to open it.

## Conventions used by this plan

- **Working directory:** see Global Constraints — the repo root of the `lesson-08-capstone-cli` branch (or its worktree).
- **Branch:** all work on `lesson-08-capstone-cli` (created from up-to-date `main` that already contains Lesson 07). Every task's first step confirms the branch.
- **Commit messages:** Conventional Commits. **No `Co-Authored-By` trailer, no AI-attribution line.**
- **Do NOT push** — the controller finishes the branch.
- The four units replace the scaffold's `main.py`/`test_main.py`, which are deleted in Task 1.
- Tasks 1–4 each end with their own commit; Task 5 and Task 6 commit their own file(s); Task 7 commits only what it changes.

---

## File Structure

```
lessons/08-capstone-cli/                     (NEW — scaffolded then authored)
├── pyproject.toml                           (from scaffold; unchanged)
├── README.md                                (authored — Task 5)
├── slides/
│   ├── index.html                           (from scaffold; <title> fixed — Task 6)
│   ├── slides.md                            (authored, 12 slides — Task 6)
│   └── assets/.gitkeep                      (from scaffold)
├── exercises/
│   ├── __init__.py                          (from scaffold; empty)
│   ├── reporting/
│   │   ├── __init__.py                      (authored — re-exports, Task 1)
│   │   ├── money.py                         (authored — given, Task 1)
│   │   └── table.py                         (authored — given, Task 1)
│   ├── expense.py                           (authored — Expense given + 2 stubs, Task 2)
│   ├── storage.py                           (authored — constants/predicates given + 4 stubs, Task 3)
│   ├── cli.py                               (authored — constants/parser head/__main__ given + 2 stubs, Task 4)
│   ├── test_reporting.py                    (authored — 2 cases, GREEN, Task 1)
│   ├── test_expense.py                      (authored — 4 cases, red, Task 2)
│   ├── test_storage.py                      (authored — 16 cases, red, Task 3)
│   └── test_cli.py                          (authored — 19 cases, red, Task 4)
└── solutions/                               (same shape, fully implemented)
    ├── __init__.py                          (from scaffold; empty)
    ├── reporting/{__init__.py,money.py,table.py}
    ├── expense.py
    ├── storage.py
    ├── cli.py
    └── test_{reporting,expense,storage,cli}.py
```

Deleted in Task 1: `exercises/main.py`, `exercises/test_main.py`, `solutions/main.py`, `solutions/test_main.py`.

Outside the lesson folder: `.gitignore` (a two-line block: comment + pattern, Task 7) and `uv.lock` (regenerated, Task 1). No catalog / Makefile / ruff changes.

---

## Task 1: Scaffold the lesson and add the given `reporting` black box

**Files:** `lessons/08-capstone-cli/` (scaffold), `{exercises,solutions}/reporting/{__init__.py,money.py,table.py}`, `{exercises,solutions}/test_reporting.py`; delete `{exercises,solutions}/main.py` and `{exercises,solutions}/test_main.py`.

**Interfaces:**

- **Consumes:** nothing — this is the first task.
- **Produces for later tasks:**
  - The scaffolded tree: `lessons/08-capstone-cli/pyproject.toml` (pytest `pythonpath = ["."]`), empty `exercises/__init__.py` and `solutions/__init__.py`, placeholder `README.md` (Task 5 overwrites) and `slides/` (Task 6 overwrites).
  - `format_money(amount: float) -> str` and `format_table(rows: list[list[str]], headers: list[str]) -> str`, re-exported from `solutions.reporting` / `exercises.reporting`. Task 4's `cli.py` imports exactly these two names: `from solutions.reporting import format_money, format_table`.
  - `solutions/test_reporting.py` and `exercises/test_reporting.py`: **2 passing cases each** — the only green exercise tests in the lesson. Later tasks must not touch them.
  - The three-line expected table used as `EXPECTED_TABLE` here reappears verbatim as `EXPECTED_REPORT` in Task 4's `test_cli.py`:
    ```
    CATEGORY       TOTAL
    groceries     $34.75
    rent       $1,200.00
    ```

- [ ] **Step 1: Confirm branch and base**

```bash
git branch --show-current
git cat-file -e main:lessons/07-modules/solutions/geom/metrics.py 2>/dev/null && echo "L07 present" || echo "L07 MISSING"
```
Expected: `lesson-08-capstone-cli` and `L07 present`. The controller creates this branch from an up-to-date `main` **before** dispatching this task, so no step here creates it: if `git branch --show-current` prints anything else (including `main`), the dispatch is wrong — STOP and report BLOCKED rather than branching yourself. Same if Lesson 07 is MISSING.

- [ ] **Step 2: Scaffold**

```bash
make new-lesson NAME=08-capstone-cli
make sync
```
Expected: `created lessons/08-capstone-cli`; `make sync` installs `lesson-08-capstone-cli` and updates `uv.lock`.

Expected after scaffolding — `make new-lesson NAME=08-capstone-cli` produces `pyproject.toml` (name `lesson-08-capstone-cli`, `description = "Lesson 08: Capstone Cli"`, `package = false`, pytest `pythonpath = ["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}`. The scaffolder derives the deck title from the slug ("Capstone Cli") and emits **absolute** `/shared/reveal/...` asset paths (do not change those). **Leave `pyproject.toml` unmodified.** `make sync` adds exactly two `lesson-08-capstone-cli` entries to `uv.lock` — the workspace-members list and a `[[package]]` stanza, no dependency changes — and that is the whole lock diff.

- [ ] **Step 3: Remove the placeholder module/test files**

```bash
rm -f lessons/08-capstone-cli/exercises/main.py lessons/08-capstone-cli/exercises/test_main.py \
      lessons/08-capstone-cli/solutions/main.py lessons/08-capstone-cli/solutions/test_main.py
mkdir -p lessons/08-capstone-cli/exercises/reporting lessons/08-capstone-cli/solutions/reporting
```
Keep `exercises/__init__.py` and `solutions/__init__.py` (both empty). Nothing is tracked yet, so plain `rm` is right.

- [ ] **Step 4: Create `lessons/08-capstone-cli/solutions/reporting/money.py`**

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

- [ ] **Step 5: Create `lessons/08-capstone-cli/solutions/reporting/table.py`**

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

The six validation lines are load-bearing (they turn a learner's mistake into a message that names the mistake instead of an `IndexError` inside a file they were told not to open). Do not "simplify" them away.

- [ ] **Step 6: Create `lessons/08-capstone-cli/solutions/reporting/__init__.py`**

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

`__all__` is why ruff's F401 leaves these re-exports alone — same as Lesson 07's `geom/__init__.py`.

- [ ] **Step 7: Create the exercise copies of `money.py` and `table.py` — byte-identical**

These two files contain no intra-lesson imports, so the exercise copies are byte-identical to the solution copies (verified on the prototype). Copy them:

```bash
cp lessons/08-capstone-cli/solutions/reporting/money.py lessons/08-capstone-cli/exercises/reporting/money.py
cp lessons/08-capstone-cli/solutions/reporting/table.py lessons/08-capstone-cli/exercises/reporting/table.py
```

- [ ] **Step 8: Create `lessons/08-capstone-cli/exercises/reporting/__init__.py`**

Same file as Step 6 with the two import lines re-prefixed (the only 2 differing lines):

```python
"""Presentation helpers for the expense tracker.

This package is GIVEN. Treat it as a library someone else wrote and handed to
you: call it through the two names below, read their docstrings, and do not
edit (or even open) the modules underneath.
"""

from exercises.reporting.money import format_money
from exercises.reporting.table import format_table

__all__ = ["format_money", "format_table"]
```

- [ ] **Step 9: Create `lessons/08-capstone-cli/solutions/test_reporting.py`**

```python
"""Tests for the reporting package.

These two tests pass from your very first run. They are not your work: they
are the documentation for the reporting package you were handed. Read them to
see how to call it.
"""

from solutions.reporting import format_money, format_table

EXPECTED_TABLE = """\
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00"""


def test_format_money_shows_two_decimals_and_groups_thousands() -> None:
    assert format_money(24.5) == "$24.50"
    assert format_money(1200) == "$1,200.00"


def test_format_table_left_aligns_all_but_the_last_column() -> None:
    rows = [["groceries", "$34.75"], ["rent", "$1,200.00"]]
    assert format_table(rows, ["CATEGORY", "TOTAL"]) == EXPECTED_TABLE
```

The `EXPECTED_TABLE` alignment is exact: `CATEGORY` + 7 spaces + `TOTAL`; `groceries` + 5 spaces + `$34.75`; `rent` + 7 spaces + `$1,200.00`. Keep it a module-level triple-quoted constant — that is the only form `ruff format` leaves alone.

- [ ] **Step 10: Create `lessons/08-capstone-cli/exercises/test_reporting.py`**

```python
"""Tests for the reporting package.

These two tests pass from your very first run. They are not your work: they
are the documentation for the reporting package you were handed. Read them to
see how to call it.
"""

from exercises.reporting import format_money, format_table

EXPECTED_TABLE = """\
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00"""


def test_format_money_shows_two_decimals_and_groups_thousands() -> None:
    assert format_money(24.5) == "$24.50"
    assert format_money(1200) == "$1,200.00"


def test_format_table_left_aligns_all_but_the_last_column() -> None:
    rows = [["groceries", "$34.75"], ["rent", "$1,200.00"]]
    assert format_table(rows, ["CATEGORY", "TOTAL"]) == EXPECTED_TABLE
```

(The single differing line is the import: `from exercises.reporting import ...`.)

- [ ] **Step 11: Verify both copies are green**

```bash
( cd lessons/08-capstone-cli && uv run pytest solutions/test_reporting.py -q )
( cd lessons/08-capstone-cli && uv run pytest exercises/test_reporting.py -q )
```
Expected: `2 passed` for each. These are the lesson's only green exercise tests — if either is red, STOP and fix before moving on.

- [ ] **Step 12: Confirm the black-box demo used by the README and slide 7**

```bash
( cd lessons/08-capstone-cli && uv run python -c "from solutions.reporting import format_table; help(format_table)" | head -5 )
```
Expected first lines:
```
Help on function format_table in module solutions.reporting.table:

format_table(rows: list[list[str]], headers: list[str]) -> str
    Render rows as a column-aligned text table and return it as one string.
```

- [ ] **Step 13: Lint + format**

```bash
make lint
uv run ruff format lessons/08-capstone-cli
uv run ruff format --check .
```
Expected: `make lint` → `All checks passed!`; `ruff format --check .` → no diff (`N files already formatted`). If ruff rewrites anything, re-run Step 11.

- [ ] **Step 14: Commit**

```bash
git add lessons/08-capstone-cli uv.lock
git commit -m "feat(lesson-08): scaffold the lesson and add the given reporting package"
```
This commits the whole scaffolded lesson (the placeholder README/slides ride along; Tasks 5/6 overwrite them) plus `uv.lock`. No `Co-Authored-By` trailer.

---

## Task 2: `expense.py` — the record and the two summary functions

**Files:** create `lessons/08-capstone-cli/solutions/expense.py`, `lessons/08-capstone-cli/exercises/expense.py`, `lessons/08-capstone-cli/solutions/test_expense.py`, `lessons/08-capstone-cli/exercises/test_expense.py`.

**Interfaces:**

- **Consumes from Task 1:** only the scaffolded tree (`lessons/08-capstone-cli/` with `pythonpath = ["."]`, empty `exercises/__init__.py` / `solutions/__init__.py`). `expense.py` imports nothing from the lesson — it is the bottom of the dependency chain.
- **Produces for later tasks:**
  - `Expense` — a `@dataclass` with exactly three fields in this order: `date: str`, `category: str`, `amount: float`. Task 3's `storage.py` does `from solutions.expense import Expense`; Task 4's `cli.py` constructs `Expense(date, category, amount)` positionally.
  - `filter_by_category(expenses: list[Expense], category: str) -> list[Expense]` — Task 4's `cli.py` calls it for `list --category`.
  - `totals_by_category(expenses: list[Expense]) -> dict[str, float]` — Task 4's `cli.py` calls it for `report`.
  - Stub messages (exact): `implement filter_by_category() so the tests pass`, `implement totals_by_category() so the tests pass`.
  - The three sample expenses, in this order (Task 3 and Task 4 reuse the same three): `Expense("2026-09-21", "rent", 1200.00)`, `Expense("2026-09-21", "groceries", 24.50)`, `Expense("2026-09-22", "groceries", 10.25)`. `rent` comes **first** on purpose: file order is not alphabetical order, which is what makes Task 4's `sorted()` test real.
  - 4 test cases (`solutions/test_expense.py` → 4 passed; `exercises/test_expense.py` → 4 failed).

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-08-capstone-cli`. If not, STOP and report BLOCKED.

- [ ] **Step 2: Create `lessons/08-capstone-cli/solutions/expense.py`**

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

- [ ] **Step 3: Create `lessons/08-capstone-cli/exercises/expense.py`**

Same file with the two bodies replaced by stubs and one technique paragraph appended to each docstring. No import line changes (this module imports nothing from the lesson):

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
```

IMPORTANT: leave both bodies as `raise NotImplementedError(...)`. This is the red start — do not implement them in the exercises tree.

- [ ] **Step 4: Create `lessons/08-capstone-cli/solutions/test_expense.py`**

```python
"""Tests for expense.py: what an expense is, and the summaries over a list."""

import pytest

from solutions.expense import Expense, filter_by_category, totals_by_category


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
```

Every fixture amount is a binary-exact fraction (`.00`, `.25`, `.50`), so `24.50 + 10.25 == 34.75` holds exactly and no test needs `pytest.approx`. Do not add one.

- [ ] **Step 5: Create `lessons/08-capstone-cli/exercises/test_expense.py`**

```python
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
```

(The single differing line is the import: `from exercises.expense import ...`.)

- [ ] **Step 6: Verify red/green**

```bash
( cd lessons/08-capstone-cli && uv run pytest solutions/test_expense.py -q )
( cd lessons/08-capstone-cli && uv run pytest exercises/test_expense.py -q )
( cd lessons/08-capstone-cli && uv run pytest solutions -q )
```
Expected: solutions file → `4 passed`; exercises file → `4 failed` (each failure is `NotImplementedError: implement filter_by_category() so the tests pass` or `... totals_by_category() ...`); whole solutions tree → `6 passed` (2 reporting + 4 expense).

- [ ] **Step 7: Lint + format**

```bash
make lint
uv run ruff format lessons/08-capstone-cli
uv run ruff format --check .
```
Expected: `All checks passed!` and no format diff. (`exercises/expense.py` needs no `# noqa`: the stub bodies use no imports, and ruff counts annotations as usage.)

- [ ] **Step 8: Commit**

```bash
git add lessons/08-capstone-cli
git commit -m "feat(lesson-08): add expense.py (the Expense record, filtering and totals)"
```
(No `Co-Authored-By` trailer.)

---

## Task 3: `storage.py` — the file format, both directions

**Files:** create `lessons/08-capstone-cli/solutions/storage.py`, `lessons/08-capstone-cli/exercises/storage.py`, `lessons/08-capstone-cli/solutions/test_storage.py`, `lessons/08-capstone-cli/exercises/test_storage.py`.

**Interfaces:**

- **Consumes from Task 2:** `Expense` — the `@dataclass` with fields `date: str`, `category: str`, `amount: float`, imported absolutely (`from solutions.expense import Expense` / `from exercises.expense import Expense`). Nothing else.
- **Produces for later tasks:**
  - `SEPARATOR = "|"` and `MAX_DIGITS = 12` (module constants, given).
  - `is_field(text: str) -> bool` and `is_amount(text: str) -> bool` (given predicates) — Task 4's `cli.py` imports both to validate what the user typed **before any write**.
  - `format_line(expense: Expense) -> str`, `parse_line(line: str) -> Expense | None`, `load_expenses(path: str) -> list[Expense]`, `save_expenses(path: str, expenses: list[Expense]) -> None`. Task 4's `cli.py` imports exactly `is_amount, is_field, load_expenses, save_expenses`.
  - Stub messages (exact): `implement format_line() so the tests pass`, `implement parse_line() so the tests pass`, `implement load_expenses() so the tests pass`, `implement save_expenses() so the tests pass`.
  - The `SAMPLE_FILE` constant (three sample lines, `rent` first, trailing newline). Task 4's `test_cli.py` defines its own byte-identical copy under the same name — the files never import from each other.
  - The `expenses_path` fixture shape (`str(tmp_path / "expenses.txt")`, a path that does **not** exist yet). Task 4's `test_cli.py` repeats it and builds `seeded_path` on top of it.
  - 9 test functions / 16 collected cases (`solutions/test_storage.py` → 16 passed; `exercises/test_storage.py` → 16 failed).

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-08-capstone-cli`. If not, STOP and report BLOCKED.

- [ ] **Step 2: Create `lessons/08-capstone-cli/solutions/storage.py`**

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

Deliberate, do not "improve": `isdecimal` not `isdigit` (`"²".isdigit()` is `True` but `float("²")` raises); the digit cap counts the digits **before** the point, which is the half `:.2f` cannot change; `splitlines()` not `split("\n")`; `save_expenses` takes the whole list and uses mode `"w"` (there is no `append_expense`); no `try`/`except` anywhere.

- [ ] **Step 3: Create `lessons/08-capstone-cli/exercises/storage.py`**

Same module with the import prefix changed, an inline `# noqa: F401` on `import os` (nothing uses it until `load_expenses` is written — without the pragma the red start fails `make lint`, exactly as Lesson 07 handled its unused import), and the four bodies replaced by stubs with a technique paragraph appended to each docstring:

```python
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
```

RUFF TRAP #1 (it bites here): `import os` is unused in the red start and trips **F401**. The fix is the inline pragma above — exactly `import os  # noqa: F401 -- os.path.exists() is for load_expenses()` — following Lesson 07's precedent of an inline `# noqa: F401` rather than a config change. `Expense` needs no pragma: ruff counts annotations as usage.

Also: no stub docstring may contain a literal `\n` escape — in a plain (non-raw) docstring it becomes an actual line break. That is why `save_expenses` says "the line break" in prose.

IMPORTANT: leave all four bodies as `raise NotImplementedError(...)` with the exact messages shown. This is the red start — do not implement them in the exercises tree, and do not reword a stub message.

- [ ] **Step 4: Create `lessons/08-capstone-cli/solutions/test_storage.py`**

```python
"""Tests for storage.py: one line of text in, one Expense out, and back again."""

import os

import pytest

from solutions.expense import Expense
from solutions.storage import format_line, load_expenses, parse_line, save_expenses

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
```

Notes that matter: `MALFORMED_FILE` really does start with a blank line (the `"""\` keeps the first stored line empty) and contains an interior blank line — 6 lines, exactly 2 of which survive. The test file reads files back with the learner's own recipe (`with open(path, encoding="utf-8") as f: f.read()`) and checks absence with `os.path.exists`, never `Path.read_text()` / `Path.exists()`, so the "paths are `str`" seam holds and `import os` is genuinely used (no `noqa` here). `tmp_path` is left unannotated on purpose — annotating it would mean naming `pathlib.Path`, which this lesson does not teach.

- [ ] **Step 5: Create `lessons/08-capstone-cli/exercises/test_storage.py`**

```python
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
```

(The two differing lines are the imports: `from exercises.expense import ...` and `from exercises.storage import ...`.)

- [ ] **Step 6: Verify red/green and the case count**

```bash
( cd lessons/08-capstone-cli && uv run pytest solutions/test_storage.py -q )
( cd lessons/08-capstone-cli && uv run pytest exercises/test_storage.py -q )
( cd lessons/08-capstone-cli && uv run pytest solutions -q )
```
Expected: solutions file → `16 passed` (9 test functions; `test_parse_line_rejects_unusable_lines` contributes 8 of the 16); exercises file → `16 failed`; whole solutions tree → `22 passed` (2 + 4 + 16).

- [ ] **Step 7: Check the storage round-trip outside pytest**

```bash
( cd lessons/08-capstone-cli && uv run python -c "
from solutions.expense import Expense
from solutions.storage import format_line, parse_line, load_expenses
print(format_line(Expense('2026-09-21', 'rent', 1200)))
print(parse_line('  2026-09-21 | groceries | 24.50  '))
print(load_expenses('nope.txt'))
" )
```
Expected, exactly:
```
2026-09-21|rent|1200.00
Expense(date='2026-09-21', category='groceries', amount=24.5)
[]
```

- [ ] **Step 8: Lint + format**

```bash
make lint
uv run ruff format lessons/08-capstone-cli
uv run ruff format --check .
```
Expected: `All checks passed!` and no format diff. If ruff reports `F401 os imported but unused` in `exercises/storage.py`, the `# noqa: F401` comment is missing or misspelled — re-do Step 3's `import os` line. Longest line in `test_storage.py` is 96 characters; nothing may exceed 100.

- [ ] **Step 9: Commit**

```bash
git add lessons/08-capstone-cli
git commit -m "feat(lesson-08): add storage.py (the line format, load and save)"
```
(No `Co-Authored-By` trailer.)

---

## Task 4: `cli.py` — the parser, the dispatch and the exit codes

**Files:** create `lessons/08-capstone-cli/solutions/cli.py`, `lessons/08-capstone-cli/exercises/cli.py`, `lessons/08-capstone-cli/solutions/test_cli.py`, `lessons/08-capstone-cli/exercises/test_cli.py`.

**Interfaces:**

- **Consumes from Task 1:** `format_money(amount: float) -> str` and `format_table(rows: list[list[str]], headers: list[str]) -> str` via `from solutions.reporting import format_money, format_table`. `format_table` takes `(rows, headers)` in that order and every cell must already be a string.
- **Consumes from Task 2:** `Expense` (positional `Expense(date, category, amount)`), `filter_by_category(expenses, category)`, `totals_by_category(expenses)` via `from solutions.expense import Expense, filter_by_category, totals_by_category`.
- **Consumes from Task 3:** `is_amount(text)`, `is_field(text)`, `load_expenses(path)`, `save_expenses(path, expenses)` via `from solutions.storage import is_amount, is_field, load_expenses, save_expenses`. Also reuses Task 3's `SAMPLE_FILE` body and `expenses_path` fixture shape — `test_cli.py` defines its own copies; the test files never import from each other.
- **Produces for later tasks:**
  - `DEFAULT_PATH = "expenses.txt"`, `NOTHING_FOUND = "No expenses found."`, `BAD_FIELD = "Date and category must not be empty or contain '|' or a line break."`, `BAD_AMOUNT = "Amount must be a plain number like 24.50."` — Task 5's README and Task 6's slides quote these strings.
  - `build_parser() -> argparse.ArgumentParser` (prog `expenses`, global `--file`, subcommands `add` / `list` / `report`) and `main(argv: list[str]) -> int`.
  - Stub messages (exact): `implement build_parser() so the tests pass`, `implement main() so the tests pass`.
  - The literal terminal transcript (Step 8 below) that Task 5's README "How to run" and Task 6's slide 2 reproduce.
  - The lesson's final counts: solutions `41 passed`; exercises `39 failed, 2 passed`.

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-08-capstone-cli`. If not, STOP and report BLOCKED.

- [ ] **Step 2: Create `lessons/08-capstone-cli/solutions/cli.py`**

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

Deliberate, do not "improve": `amount` is a plain `str` positional (no `type=float`), so `is_amount` is the single validator for both the write and the read path; `--file` is declared once, globally, and is NOT repeated on the subparsers; `main` takes a required `argv` list (no `argv=None` sentinel); the final branch is a bare `else:` (safe because `required=True`).

- [ ] **Step 3: Create `lessons/08-capstone-cli/exercises/cli.py`**

```python
"""The command line: one parser, one main(), three subcommands.

The three imports below carry a `# noqa: F401` pragma: nothing uses those
names yet, and without it the linter would flag them as unused imports. You
will need every one of them in build_parser() and main() -- delete the
pragmas once you do.
"""

import argparse
import sys

from exercises.expense import Expense, filter_by_category, totals_by_category  # noqa: F401
from exercises.reporting import format_money, format_table  # noqa: F401
from exercises.storage import is_amount, is_field, load_expenses, save_expenses  # noqa: F401

DEFAULT_PATH = "expenses.txt"
NOTHING_FOUND = "No expenses found."
BAD_FIELD = "Date and category must not be empty or contain '|' or a line break."
BAD_AMOUNT = "Amount must be a plain number like 24.50."


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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

RUFF TRAP #2 (it bites here): the given parser head assigns `subparsers`, which nothing uses until the learner writes the three `add_parser` blocks — that trips **F841**. The spec's documented pragma is exactly `# noqa: F841 -- you use it` on that line (97 characters, the longest line in the lesson — still under the 100 limit). The three grouped imports each need `# noqa: F401`: line-scoped, so three comments cover nine names. No pragma for `argparse` (used in the return annotation) or `sys` (used in the `__main__` block).

Two more things that are load-bearing and easy to "fix" wrongly:

- `build_parser().parse_args(argv)` in `main` is a **bare expression**, not `args = build_parser().parse_args(argv)` — an assignment would trip F841, while a bare call is ruff-clean (B018 does not flag function calls). It is what makes `python -m exercises.cli --help` work the moment `build_parser` is done, before `main` exists.
- The worked `add` block belongs in the README and on slide 9 as real, copy-pasteable code — NOT as indented prose inside this docstring, which produces an `IndentationError` the moment a beginner pastes it.

IMPORTANT: leave both bodies as `raise NotImplementedError(...)` with the exact messages shown. This is the red start — do not implement them in the exercises tree, and do not reword a stub message.

- [ ] **Step 4: Create `lessons/08-capstone-cli/solutions/test_cli.py`**

```python
"""Tests for cli.py: the parser, the three commands, the exit codes.

Every test calls main() with a list of strings -- no terminal, no subprocess.
That is what makes a CLI testable.
"""

import os

import pytest

from solutions.cli import BAD_AMOUNT, BAD_FIELD, NOTHING_FOUND, build_parser, main

SAMPLE_FILE = """\
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
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


@pytest.fixture
def seeded_path(expenses_path: str) -> str:
    """The three sample expenses, already on disk."""
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_FILE)
    return expenses_path


def test_build_parser_defaults_the_file_and_names_the_command() -> None:
    args = build_parser().parse_args(["report"])
    assert args.file == "expenses.txt"
    assert args.command == "report"


def test_add_keeps_the_earlier_expenses(expenses_path: str, capsys) -> None:
    assert main(["--file", expenses_path, "add", "2026-09-21", "rent", "1200"]) == 0
    capsys.readouterr()
    assert main(["--file", expenses_path, "add", "2026-09-21", "groceries", "24.50"]) == 0
    assert capsys.readouterr().out == "Added groceries $24.50 on 2026-09-21.\n"
    with open(expenses_path, encoding="utf-8") as f:
        assert f.read() == "2026-09-21|rent|1200.00\n2026-09-21|groceries|24.50\n"


def test_add_prints_a_confirmation(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "add", "2026-09-21", "groceries", "24.50"])
    assert code == 0
    assert capsys.readouterr().out == "Added groceries $24.50 on 2026-09-21.\n"


@pytest.mark.parametrize("amount", ["lots", "-5", "nan", "1234567890123"])
def test_add_rejects_an_amount_that_is_not_a_plain_number(
    expenses_path: str, capsys, amount: str
) -> None:
    code = main(["--file", expenses_path, "add", "2026-09-21", "groceries", amount])
    assert code == 1
    assert capsys.readouterr().out == BAD_AMOUNT + "\n"
    assert not os.path.exists(expenses_path)


@pytest.mark.parametrize(
    ("date", "category"),
    [
        ("2026-09-21", "food|drink"),
        ("2026-09-21|x", "groceries"),
        ("2026-09-21", "   "),
    ],
)
def test_add_rejects_a_field_that_would_break_the_file(
    expenses_path: str, capsys, date: str, category: str
) -> None:
    code = main(["--file", expenses_path, "add", date, category, "24.50"])
    assert code == 1
    assert capsys.readouterr().out == BAD_FIELD + "\n"
    assert not os.path.exists(expenses_path)


def test_list_prints_a_table_of_every_expense(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_LIST + "\n"


def test_list_filters_by_category(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list", "--category", "groceries"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_LIST_GROCERIES + "\n"


def test_list_on_a_missing_file_says_nothing_found(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "list"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_list_with_an_unknown_category_says_nothing_found(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list", "--category", "travel"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_report_totals_each_category_in_alphabetical_order(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_REPORT + "\n"


def test_report_on_a_missing_file_says_nothing_found(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_report_ignores_malformed_lines(expenses_path: str, capsys) -> None:
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write("junk\n" + SAMPLE_FILE)
    code = main(["--file", expenses_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_REPORT + "\n"


@pytest.mark.parametrize("argv", [[], ["add", "2026-09-21"]])
def test_a_bad_command_line_exits_with_code_two(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)
    assert exit_info.value.code == 2
```

Exact alignment matters in the three expected tables — they are what the program prints, column for column:
`DATE` + 8 spaces + `CATEGORY` + 6 spaces + `AMOUNT` on the `EXPECTED_LIST` header, and `rent` + 7 spaces + `$1,200.00` on its `rent` row. Copy them character for character; a stray space turns a green test red.

Why it is written this way: the expected tables carry `$1,200.00`, which only `format_money` produces — a learner who inlines `f"${e.amount:.2f}"` writes `$1200.00` and goes red, which is what makes the black box a graded dependency. The fixture stores `rent` **before** `groceries`, so `test_report_totals_each_category_in_alphabetical_order` genuinely pins `sorted()`. No test asserts on argparse's own message wording — only on `exit_info.value.code`, so a CPython wording change cannot break CI. `capsys` and `tmp_path` stay unannotated (annotating them would drag in `pytest.CaptureFixture` / `pathlib.Path`).

- [ ] **Step 5: Create `lessons/08-capstone-cli/exercises/test_cli.py`**

```python
"""Tests for cli.py: the parser, the three commands, the exit codes.

Every test calls main() with a list of strings -- no terminal, no subprocess.
That is what makes a CLI testable.
"""

import os

import pytest

from exercises.cli import BAD_AMOUNT, BAD_FIELD, NOTHING_FOUND, build_parser, main

SAMPLE_FILE = """\
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
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


@pytest.fixture
def seeded_path(expenses_path: str) -> str:
    """The three sample expenses, already on disk."""
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_FILE)
    return expenses_path


def test_build_parser_defaults_the_file_and_names_the_command() -> None:
    args = build_parser().parse_args(["report"])
    assert args.file == "expenses.txt"
    assert args.command == "report"


def test_add_keeps_the_earlier_expenses(expenses_path: str, capsys) -> None:
    assert main(["--file", expenses_path, "add", "2026-09-21", "rent", "1200"]) == 0
    capsys.readouterr()
    assert main(["--file", expenses_path, "add", "2026-09-21", "groceries", "24.50"]) == 0
    assert capsys.readouterr().out == "Added groceries $24.50 on 2026-09-21.\n"
    with open(expenses_path, encoding="utf-8") as f:
        assert f.read() == "2026-09-21|rent|1200.00\n2026-09-21|groceries|24.50\n"


def test_add_prints_a_confirmation(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "add", "2026-09-21", "groceries", "24.50"])
    assert code == 0
    assert capsys.readouterr().out == "Added groceries $24.50 on 2026-09-21.\n"


@pytest.mark.parametrize("amount", ["lots", "-5", "nan", "1234567890123"])
def test_add_rejects_an_amount_that_is_not_a_plain_number(
    expenses_path: str, capsys, amount: str
) -> None:
    code = main(["--file", expenses_path, "add", "2026-09-21", "groceries", amount])
    assert code == 1
    assert capsys.readouterr().out == BAD_AMOUNT + "\n"
    assert not os.path.exists(expenses_path)


@pytest.mark.parametrize(
    ("date", "category"),
    [
        ("2026-09-21", "food|drink"),
        ("2026-09-21|x", "groceries"),
        ("2026-09-21", "   "),
    ],
)
def test_add_rejects_a_field_that_would_break_the_file(
    expenses_path: str, capsys, date: str, category: str
) -> None:
    code = main(["--file", expenses_path, "add", date, category, "24.50"])
    assert code == 1
    assert capsys.readouterr().out == BAD_FIELD + "\n"
    assert not os.path.exists(expenses_path)


def test_list_prints_a_table_of_every_expense(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_LIST + "\n"


def test_list_filters_by_category(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list", "--category", "groceries"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_LIST_GROCERIES + "\n"


def test_list_on_a_missing_file_says_nothing_found(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "list"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_list_with_an_unknown_category_says_nothing_found(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list", "--category", "travel"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_report_totals_each_category_in_alphabetical_order(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_REPORT + "\n"


def test_report_on_a_missing_file_says_nothing_found(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_report_ignores_malformed_lines(expenses_path: str, capsys) -> None:
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write("junk\n" + SAMPLE_FILE)
    code = main(["--file", expenses_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_REPORT + "\n"


@pytest.mark.parametrize("argv", [[], ["add", "2026-09-21"]])
def test_a_bad_command_line_exits_with_code_two(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)
    assert exit_info.value.code == 2
```

(The single differing line is the import: `from exercises.cli import ...`. The constants exist in the stub file, so this import works from the very first run.)

- [ ] **Step 6: Verify the red start and the totals**

```bash
( cd lessons/08-capstone-cli && uv run pytest solutions -q )
( cd lessons/08-capstone-cli && uv run pytest exercises -q )
( cd lessons/08-capstone-cli && uv run pytest exercises solutions -q )
```
Expected, exactly:
- solutions → `41 passed` (2 reporting + 4 expense + 16 storage + 19 cli)
- exercises → `39 failed, 2 passed` — the 2 green are `test_reporting.py`, and every stub fails at **call** time, not at import time (no collection error)
- both trees in one process → `39 failed, 43 passed`, with **no** `import file mismatch`

If exercises reports a collection error instead of `39 failed, 2 passed`, an import is wrong — fix it before moving on.

- [ ] **Step 7: Verify the ladder's case counts (against `solutions`)**

```bash
( cd lessons/08-capstone-cli && uv run pytest solutions/test_cli.py -k build_parser -q )
( cd lessons/08-capstone-cli && uv run pytest solutions/test_cli.py -k add -q )
```
Expected: `1 passed, 18 deselected` and `9 passed, 10 deselected` — these are the numbers the README's feedback ladder quotes (step 5 takes the exercise suite from 20 to 23 passing: the `build_parser` case plus the 2 exit-code cases that reach argparse through `main`'s bare `parse_args`; step 6 adds 9).

- [ ] **Step 8: Reproduce the literal transcript**

```bash
( cd lessons/08-capstone-cli && rm -f expenses.txt \
  && uv run python -m solutions.cli --file expenses.txt add 2026-09-21 rent 1200 \
  && uv run python -m solutions.cli --file expenses.txt add 2026-09-21 groceries 24.50 \
  && uv run python -m solutions.cli --file expenses.txt add 2026-09-22 groceries 10.25 \
  && cat expenses.txt \
  && uv run python -m solutions.cli --file expenses.txt list \
  && uv run python -m solutions.cli --file expenses.txt list --category groceries \
  && uv run python -m solutions.cli --file expenses.txt report )
```
Expected, exactly:
```
Added rent $1,200.00 on 2026-09-21.
Added groceries $24.50 on 2026-09-21.
Added groceries $10.25 on 2026-09-22.
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
2026-09-22|groceries|10.25
DATE        CATEGORY      AMOUNT
2026-09-21  rent       $1,200.00
2026-09-21  groceries     $24.50
2026-09-22  groceries     $10.25
DATE        CATEGORY   AMOUNT
2026-09-21  groceries  $24.50
2026-09-22  groceries  $10.25
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00
```

Then the error paths and exit codes:
```bash
( cd lessons/08-capstone-cli \
  && uv run python -m solutions.cli --file expenses.txt add 2026-09-23 'food|drink' 5.00 ; echo "exit=$?" \
  ; uv run python -m solutions.cli --file expenses.txt add 2026-09-23 refund -5 ; echo "exit=$?" \
  ; uv run python -m solutions.cli --file missing.txt report ; echo "exit=$?" \
  ; uv run python -m solutions.cli --file expenses.txt ; echo "exit=$?" \
  ; uv run python -m solutions.cli list --file expenses.txt ; echo "exit=$?" )
```
Expected, exactly:
```
Date and category must not be empty or contain '|' or a line break.
exit=1
Amount must be a plain number like 24.50.
exit=1
No expenses found.
exit=0
usage: expenses [-h] [--file FILE] {add,list,report} ...
expenses: error: the following arguments are required: command
exit=2
usage: expenses [-h] [--file FILE] {add,list,report} ...
expenses: error: unrecognized arguments: --file expenses.txt
exit=2
```

And the free help:
```bash
( cd lessons/08-capstone-cli && uv run python -m solutions.cli --help )
```
Expected, exactly:
```
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

- [ ] **Step 9: Clean up the demo file**

```bash
rm -f lessons/08-capstone-cli/expenses.txt
git status --porcelain
```
Expected: no `lessons/08-capstone-cli/expenses.txt` in the output. (The `.gitignore` line that covers a learner's own runs lands in Task 7; until then, delete the file by hand — it must never be committed.)

- [ ] **Step 10: Lint + format**

```bash
make lint
uv run ruff format lessons/08-capstone-cli
uv run ruff format --check .
```
Expected: `All checks passed!` and no format diff (the lesson contributes 22 files to `ruff format --check`). If ruff reports F401/F841 in `exercises/cli.py`, a pragma is missing — the red start needs exactly four: three `# noqa: F401` on the grouped imports and one `# noqa: F841 -- you use it` on the `subparsers` line. No line in the lesson may exceed 100 characters (the longest is that 97-character `subparsers` line).

- [ ] **Step 11: Commit**

```bash
git add lessons/08-capstone-cli
git commit -m "feat(lesson-08): add cli.py (argparse subcommands, dispatch, exit codes)"
```
(No `Co-Authored-By` trailer.)

---

## Task 5: Author the lesson README

**Files:** Modify `lessons/08-capstone-cli/README.md` (overwrite the scaffold's TODO placeholders).

**Interfaces:**

- **Consumes from Tasks 1-4:** the module and function names (`reporting.format_money` / `format_table`, `Expense`, `filter_by_category`, `totals_by_category`, `SEPARATOR`, `MAX_DIGITS`, `is_field`, `is_amount`, `format_line`, `parse_line`, `load_expenses`, `save_expenses`, `build_parser`, `main`); the four `cli.py` constants and their exact text; the literal transcript from Task 4 Step 8; the counts `39 failed, 2 passed` (first exercise run) and `41 passed` (solutions); the per-step ladder numbers (Task 4 Step 7 verifies the `build_parser` and `add` rows; every other row is pinned verbatim in the README content below — reproduce it exactly, do not recompute it).
- **Produces for Task 6:** the wording the deck compresses (the module map, the six unusable line shapes, the `add` subparser block, the ladder). `exercises/cli.py`'s `build_parser` docstring promises "the README and slide 9 show the `add` block in full" — this README is one half of that promise; Task 6 is the other.

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-08-capstone-cli`. If not, STOP and report BLOCKED.

- [ ] **Step 2: Overwrite `lessons/08-capstone-cli/README.md` with EXACTLY this content**

````markdown
# Lesson 08 — Phase 1 capstone: expense tracker CLI

Seven lessons of parts, one program. You build an expense tracker you can actually
run: `add` an expense, `list` what you have, `report` the totals — over a plain
text file you can open in any editor.

## Learning goals

- Split a program across modules whose dependencies point one way.
- Read and write a plain text file with `open`, `read`, `write` and `with`.
- Turn text into objects and back, and decide what to do with input that does not fit.
- Build a subcommand CLI with `argparse` and return a meaningful exit code.
- Use a package you did not write by reading its docstrings, not its source.

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md),
  [Lesson 02 — Variables, types, operators](../02-variables/README.md),
  [Lesson 03 — Control flow](../03-control-flow/README.md),
  [Lesson 04 — Functions & tests](../04-functions/README.md),
  [Lesson 05 — Collections](../05-collections/README.md),
  [Lesson 06 — Classes & dataclasses](../06-classes/README.md), and
  [Lesson 07 — Modules, packages, imports](../07-modules/README.md).

## Concepts

### The shape of a program

Four units, four ideas, and the arrows point one way:

```text
expense.py    what an expense is      (imports nothing)
storage.py    where it lives          (imports expense)
reporting/    how it looks            (imports nothing)
cli.py        how you drive it        (imports all three)

expense.py ──┐
storage.py ──┼──▶ cli.py     nothing imports cli.py
reporting/ ──┘
```

`cli.py` is the only file that knows about all of them, and nothing imports `cli.py`.
That is what lets you build one unit at a time — and test one unit at a time, with
one test file per module.

### A line is a record

One expense per line, three fields, `|` between them, and the file ends with a newline:

```text
2026-09-21|groceries|24.50
```

`Expense` is a `@dataclass` (Lesson 06) with three fields: `date`, `category`, `amount`.
The date is a plain `str` — real date objects are Lesson 14, and a string keeps the
program free of a hidden clock, which is also why every test is deterministic.

`SEPARATOR = "|"` is a module constant so the writer and the reader literally cannot
disagree: `format_line` joins with it, `parse_line` splits on it. Not JSON, not CSV —
those are Lesson 14, and a format dumb enough to read with `str.split` is what makes the
parsing visible.

### Strings are objects with methods

The first string methods of the course, and `parse_line` needs all of them:

```python
"a|b|c".split("|")        # ['a', 'b', 'c']
"  x \n".strip()          # 'x'          — whitespace off both ends
"a\nb\n".splitlines()     # ['a', 'b']   — no phantom empty last element
if line.strip():          # truthiness: a non-empty string is True
date, category, amount = parts      # unpack three items into three names
```

### Files

The recipe — read a whole file, then write one:

```python
with open(path, encoding="utf-8") as f:     # read mode is the default
    text = f.read()

with open(path, "w", encoding="utf-8") as f:
    f.write(line + "\n")                     # write() does NOT add the line break
```

- `"w"` replaces the whole file; `"a"` appends to it.
- You write the newline yourself — that is why `save_expenses` does
  `f.write(format_line(expense) + "\n")`.
- Always pass `encoding="utf-8"` on both ends, so a `café` category survives.
- `f"{amount:.2f}"` (Lesson 02) is what makes the file round-trip: `1200` is stored as
  `1200.00`.

`with` opens the file and guarantees it gets closed when the block ends — even if
something goes wrong inside. That is all you need today. Lesson 13 shows you how `with`
works and how to write your own.

### When there is no file

The first time anyone runs the program there is no file yet. That is not an error, it
means "no expenses yet":

```python
if not os.path.exists(path):
    return []
```

Look before you leap: ask whether the file is there, then read it. Lesson 11 shows the
other style — try it and handle the explosion — and rewrites this exact function.

### Lines that are not expenses

Six shapes are unusable, and `parse_line` returns `None` for every one of them:

1. a blank or whitespace-only line
2. too few fields (`2026-09-21|groceries`)
3. too many fields (`2026-09-21|groceries|24.50|extra`)
4. an empty date (`|groceries|24.50`)
5. an empty category (`2026-09-21||24.50`)
6. an amount that is not a plain number (`lots`, `12,50`, `nan`, `-5.00`)

`load_expenses` skips them, so one bad line never stops your report. There is a
consequence, and it is worth a minute of thought: because `add` does **load → append →
save**, a line the parser skipped is *gone* after your next `add`. Is that the right
behaviour? What should a real program do — back the file up, refuse to save, warn you?

### Validating what the user types

The delimiter you chose is now part of your input contract. `add 2026-09-23 "food|drink" 5`
would otherwise be written as a four-field line and silently discarded forever, so `main`
checks the date and the category with `is_field` and the amount with `is_amount`
**before anything is written**, and returns `1` with a message if either fails.

The same two predicates guard the read side inside `parse_line` — one validator, both
directions, which is why what the program writes is always something it can read back.
That is also why `amount` is a plain string argument and not `type=float`: with
`type=float`, argparse would accept `nan`, `inf` and `-0`, print a cheerful
confirmation, write a line, and lose it on the next load. Whose error message should
this be — the library's or yours?

### A black box you did not write

`reporting/` is given, complete, and you should not open `money.py` or `table.py`. Call
it through the two names it exports and read *their* docstrings:

```python
from exercises.reporting import format_money, format_table

format_money(1200)                                   # '$1,200.00'
print(format_table(rows, ["CATEGORY", "TOTAL"]))     # rows first, headers second
```

```bash
uv run python -c "from solutions.reporting import format_table; help(format_table)"
```

Every cell you hand `format_table` must already be a string — that is what
`format_money` is for. It takes `(rows, headers)` in that order, left-aligns every
column except the last, and returns one string with no trailing newline, so you
`print()` it.

If you find yourself needing to open `table.py` to know how to call it, that means the
docstring failed. Say so — noticing that is a real code-review skill.

### Ordering output

`sorted(iterable)` returns a new sorted list, and iterating a dict gives its keys, so
`sorted(totals)` is the categories in alphabetical order:

```python
for name in sorted(totals):
    ...
```

(Lesson 05 promised `sorted(...)` "in a later lesson" — here it is.) `list` shows the
file in the order you wrote it; `report` sorts.

### Building a dict by hand

Lesson 05 built dicts with comprehensions and read them with `.get`. Here you need the
write half, `d[k] = v`, inside a plain `for` loop:

```python
totals[category] = totals.get(category, 0.0) + amount
```

`.get(key, default)` is what saves you from "is this the first time I have seen this
category?" — the default *is* the answer.

### argparse

```python
parser = argparse.ArgumentParser(prog="expenses", description="...")
parser.add_argument("--file", default=DEFAULT_PATH, help="...")
subparsers = parser.add_subparsers(dest="command", required=True)

add = subparsers.add_parser("add", help="record a new expense")
add.add_argument("date", help="the date, e.g. 2026-09-21")          # positional

listing = subparsers.add_parser("list", help="show every expense")
listing.add_argument("--category", help="only show this category")   # option
```

- A **positional** is required and named by position; an `--option` is optional and
  named by its flag. `dest="command"` puts the chosen subcommand name in `args.command`.
- `--file` is global: it is declared once on the top-level parser and goes **before**
  the subcommand (like `git -C path status`).
- `--help` comes free, and argparse exits with code `2` on a bad command line — and
  writes that message to stderr, not stdout.

### `main(argv) -> int`

A CLI is just a function that takes a list of strings and returns a number:

```python
def main(argv: list[str]) -> int:
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

`sys.argv[1:]` is the real command line without the program name. Because `main` takes
the list as an argument, every test can call it directly — no terminal, no subprocess,
no monkeypatching. Exit codes: `0` success (including "No expenses found."), `1` a value
we rejected, `2` a bad command line (argparse's own).

### How to read the test files

All of this is given; you never write it.

- `tmp_path` is a pytest fixture: a fresh empty directory per test. `tmp_path /
  "expenses.txt"` builds a path inside it — that `/` is `pathlib`, which is Lesson 14,
  which is why the fixture wraps it in `str(...)` before your code ever sees it. The
  path does **not** exist yet, on purpose: the missing-file branch is the default state.
- A fixture may ask for another fixture: `seeded_path` asks for `expenses_path`, then
  writes the three sample expenses into it.
- `capsys` captures output: `capsys.readouterr().out` is what your program printed.
  Calling it also drains the buffer, which is why a test that calls `main` twice reads
  it in between.
- `pytest.raises` is not a fixture but a `with` block, for the argparse exits:

  ```python
  with pytest.raises(SystemExit) as exit_info:
      main([])
  assert exit_info.value.code == 2
  ```

The tests pin exact output strings — read them as the spec for what you print.

### One new note on types

`parse_line` returns `Expense | None` — "an `Expense` or `None`". The runtime check is
`if expense is not None:`, never `expense != None` (that passes the tests and then fails
`make lint` with `E711`). Types get taught properly in Lesson 09.

### Gotchas

- `--file` goes **before** the subcommand. Putting it after — `... cli list --file
  expenses.txt` — fails with
  `expenses: error: unrecognized arguments: --file expenses.txt` and exit code 2.
- The `# noqa: F401` / `# noqa: F841` comments in `exercises/` mark names that are
  deliberately unused *for now*. Delete each one once you use the name.
- A `--file` path whose directory does not exist looks fine to `list` and `report` (they
  print "No expenses found." and exit 0) and then crashes on `add`.
- A file the program cannot read at all still crashes with a traceback — an uncaught
  exception also exits 1, so `echo $?` cannot tell a crash from a rejected value.
  Catching that is Lesson 11.
- Run the commands below from `lessons/08-capstone-cli/`. From the repo root
  `uv run pytest exercises` says `ERROR: file or directory not found: exercises`, and
  `python -m exercises.cli` says `No module named exercises`.

## Exercise

Eight functions, about 70 lines, in this order — inside-out, so you never debug two
unknowns at once:

1. `storage.py` — `format_line`, `parse_line`, `load_expenses`, `save_expenses`
2. `expense.py` — `filter_by_category`, then `totals_by_category`
3. `cli.py` — `build_parser`, then `main`

Your first run says `39 failed, 2 passed`. The 2 that pass are the `reporting` package
you were given — they are its documentation, not your work.

**Core** (what we do together): all four `storage.py` functions, `filter_by_category`,
`build_parser`, and the `add` branch of `main`. That already gives you a program that
takes a real expense, writes a real file and prints a real confirmation.
**Stretch** (self-study): the `list` branch, `totals_by_category`, and the `report`
branch — they only display what `add` already writes.

### The feedback ladder

Run these from `lessons/08-capstone-cli/`. Something goes green every few minutes.

| Step | Command | What you get |
|---|---|---|
| 0 | `uv run pytest exercises -q --tb=line` | `39 failed, 2 passed`, one line each. Open `exercises/test_reporting.py` — those 2 green tests are your library. |
| 1 | `uv run pytest exercises/test_storage.py -k format_line` | **One line of code** goes green. First win inside 3 minutes. |
| 2 | `… -k parse_line` | 10 cases. The parametrized list *is* the spec for bad lines. |
| 3 | `… -k "load or save or round_trip"` | 5 more. Then try it outside pytest: `uv run python -c "from exercises.storage import load_expenses; print(load_expenses('nope.txt'))"` → `[]` |
| 4 | `uv run pytest exercises/test_expense.py -k filter` | 2 more. Pure functions, no I/O — the fastest wins in the lesson. |
| 5 | `uv run pytest exercises/test_cli.py -k build_parser`, then `uv run python -m exercises.cli --help` | 3 more — 23 passing — and the thing prints real help while `main` still raises. It is a program now. |
| 6 | `… -k add` | 9 cases. The `add` branch of `main` lights its own tests. |
| 7 | `uv run python -m exercises.cli --file my.txt add 2026-09-21 coffee 4.50` | Run your own program. `cat my.txt`. `echo $?`. |
| 8 | self-study: `main`'s `list` branch, then `totals_by_category`, then `main`'s `report` branch | 4 cases, then 2, then 3 — the last 9, and the lesson is green. |

### The worked example: one subcommand

`build_parser` gives you the parser, the global `--file` and the `subparsers` object.
You write the three subcommands. Here is `add` in full — `list` and `report` are yours:

```python
add = subparsers.add_parser("add", help="record a new expense")
add.add_argument("date", help="the date, e.g. 2026-09-21")
add.add_argument("category", help="the category, e.g. groceries")
add.add_argument("amount", help="the amount, e.g. 24.50")
```

`list` takes no positionals and one optional `--category`; `report` takes nothing at
all. Finish with `return parser` (and delete the `raise NotImplementedError` line).

## How to run

From the repo root:

```bash
make test-lesson LESSON=08-capstone-cli
```

Or directly, from `lessons/08-capstone-cli/`:

```bash
uv run pytest exercises -q --tb=line     # your work — 39 failed, 2 passed at the start
uv run pytest exercises/test_storage.py  # one module at a time
uv run pytest solutions                  # the reference — 41 passed
```

Run the finished program (from `lessons/08-capstone-cli/`):

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

And the exit codes — `echo $?` right after each command:

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

Read the given package's documentation without opening it:

```bash
uv run python -c "from solutions.reporting import format_table; help(format_table)"
```

## Going further

- Add a grand-total row to `report` — the table aligns it for you.
- `open(path, "a")` appends. Make `add` use it, and say what you lose.
- A skipped line disappears on the next `add`. Fix it: back the file up, refuse to save,
  or warn.
- Real CLIs send errors to stderr: `print(msg, file=sys.stderr)`. Why is that better?
- Money in `float` is a lie (`0.1 + 0.2`). Try `add … tip 0.005` and `add … tip 1.005` —
  they are stored as `0.01` and `1.00`, so what you typed is not what comes back. Where
  did your half-cent go, and why did the two round in opposite directions?
  `decimal.Decimal` is the real answer.
- `str.isdigit()` vs `isdecimal()` vs `isnumeric()` — why `is_amount` uses `isdecimal`
  (`"²".isdigit()` is `True`, but `float("²")` raises). Then read the other half of
  `is_amount`: why does it count the digits *before* the point? Delete that check and try
  a 20-digit amount — `float()` reads it, `format_line` writes it, and the next `load`
  refuses it, so your `add` reports success for a line `list` cannot see and your next
  `add` deletes it.
- `format_table` raises `ValueError` on a ragged row — a real library validates its
  input. Catching that is Lesson 11.
- `argparse`: `type=`, `choices=`, `nargs=`, mutually exclusive groups, `%(prog)s`.
- `console_scripts` in `pyproject.toml` turn `main` into a real `expenses` command
  (Lesson 15). Real dates (`datetime`) and real paths (`pathlib`) — Lesson 14.
````

- [ ] **Step 3: Sanity-check the README**

```bash
grep -ic todo lessons/08-capstone-cli/README.md          # expect 0
grep -c '```' lessons/08-capstone-cli/README.md          # expect even
head -1 lessons/08-capstone-cli/README.md                # expect: # Lesson 08 — Phase 1 capstone: expense tracker CLI
grep -c '39 failed, 2 passed' lessons/08-capstone-cli/README.md   # expect 3
```
Expected: `0`; an even number; the title line with the em-dash; `3` (the Exercise line, the ladder step 0 row, and the "How to run" comment).

- [ ] **Step 4: Commit**

```bash
git add lessons/08-capstone-cli/README.md
git commit -m "docs(lesson-08): author the README (files, argparse, the capstone brief)"
```
(No `Co-Authored-By` trailer.)

---

## Task 6: Author the slide deck

**Files:** Modify `lessons/08-capstone-cli/slides/slides.md` and `lessons/08-capstone-cli/slides/index.html` (`<title>` only).

**Interfaces:**

- **Consumes from Tasks 1-5:** the transcript from Task 4 Step 8 (slide 2), the module map (slide 3), the `add` subparser block written verbatim in Task 5's README (slide 9 repeats it — `exercises/cli.py`'s docstring promises "the README and slide 9 show the `add` block in full"), the six unusable line shapes (slide 6), the ladder and the `39 failed, 2 passed` start (slide 12).
- **Produces for Task 7:** `lessons/08-capstone-cli/slides/` on disk, which is what makes `build_index` render the lesson as a link instead of a future placeholder — Task 7 checks the link and the placeholder count of **20**.

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-08-capstone-cli`. If not, STOP and report BLOCKED.

- [ ] **Step 2: Overwrite `lessons/08-capstone-cli/slides/slides.md` with EXACTLY this content (12 slides)**

````markdown
## Lesson 08
### Phase 1 capstone: expense tracker CLI

Seven lessons of parts, one program.

Note:
Demo the finished CLI before building it: one add, one list, one report.

---

## What we're building

```console
$ uv run python -m solutions.cli add 2026-09-21 groceries 24.50
Added groceries $24.50 on 2026-09-21.

$ uv run python -m solutions.cli report
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00
```

- `add`, `list`, `report` over one plain text file
- No database, no dependencies — stdlib only

Note:
Run all three live: add, list, report. The file already holds `rent 1200.00` and
`groceries 10.25` from earlier adds — that is why the report totals more than the
one add on the slide. `exercises.cli` still raises `NotImplementedError` today;
that is what they are about to fix.

---

## The shape of a program

```text
expense.py    what an expense is      (imports nothing)
storage.py    where it lives          (imports expense)
reporting/    how it looks            (imports nothing)
cli.py        how you drive it        (imports all three)

expense.py ──┐
storage.py ──┼──▶ cli.py     nothing imports cli.py
reporting/ ──┘
```

- Four units, four test files — build one at a time

---

## A line is a record

```text
2026-09-21|groceries|24.50
```

```python
SEPARATOR = "|"

# write
f"{e.date}{SEPARATOR}{e.category}{SEPARATOR}{e.amount:.2f}"

# read
parts = [p.strip() for p in line.strip().split(SEPARATOR)]
date, category, amount = parts
```

- One constant, so the writer and the reader cannot disagree
- `Expense` is a `@dataclass`; the date is a `str` — no hidden clock

---

## Files: open, read, write

```python
with open(path, encoding="utf-8") as f:
    text = f.read()

with open(path, "w", encoding="utf-8") as f:
    f.write(line + "\n")
```

- `"w"` replaces the file, `"a"` appends
- `write()` does not add the line break — you do
- `text.splitlines()` — no phantom empty last line
- `with` closes the file even when something goes wrong
- *Lesson 13 shows how `with` actually works*

---

## Lines that aren't expenses

- blank line
- too few fields / too many fields
- empty date / empty category
- an amount that is not a plain number: `lots`, `-5.00`

```python
if not os.path.exists(path):   # no file yet? not an error
    return []
```

- `parse_line` returns `None`; the loader skips it
- A plain `if`, not `try`/`except` — that is Lesson 11
- *The skipped line is gone after your next `add` — is that OK?*

---

## A black box you didn't write

```python
from exercises.reporting import format_money, format_table

format_money(1200)                                # '$1,200.00'
print(format_table(rows, ["CATEGORY", "TOTAL"]))  # rows first!
```

- Read the docstring, not the source: `help(format_table)`
- Every cell must already be a string — that is what `format_money` is for
- Its 2 tests are green from your first run: they are its documentation

---

## Money, dates and order

```python
totals[category] = totals.get(category, 0.0) + amount

for name in sorted(totals):
    ...
```

- Money in `float` is a lie — we only *display* it, via `format_money`
- The date is a `str`, so there is no hidden clock and no flaky test
- `sorted(totals)` walks the keys alphabetically (Lesson 05 promised this)
- `d[k] = v` is the half of dicts Lesson 05 did not show

---

## argparse: three subcommands

```python
parser.add_argument("--file", default=DEFAULT_PATH, help="...")
subparsers = parser.add_subparsers(dest="command", required=True)

add = subparsers.add_parser("add", help="record a new expense")
add.add_argument("date", help="the date, e.g. 2026-09-21")
add.add_argument("category", help="the category, e.g. groceries")
add.add_argument("amount", help="the amount, e.g. 24.50")
```

- Positional = required, by position; `--option` = optional, by name
- `--file` is global and goes **first**, before the subcommand
- `--help` is free; a bad command line exits `2`
- *`amount` is a plain string, not `type=float` — whose error message is it?*

---

## `main(argv)` is just a function

```python
def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- A list of strings in, an exit code out
- That is why every test calls `main([...])` — no terminal, no subprocess
- `tmp_path`, `capsys`, `pytest.raises(SystemExit)`
- `0` success · `1` we rejected your value · `2` argparse rejected your command line

---

## Phase 1 in one program

- 01 `print`, `python -m`
- 02 f-strings and format specs (`:.2f`)
- 03 `if` / `for`
- 04 functions and pytest
- 05 comprehensions and `dict.get`
- 06 `@dataclass`
- 07 a package with `__init__.py` re-exports

All of it, in the program you finish today.

---

## Your turn / What's next

- Start: `uv run pytest exercises -q --tb=line` → `39 failed, 2 passed`
- The 2 that pass are the library you were given
- Ladder: `format_line` → `parse_line` → load/save → filter → `build_parser` → `--help`
- Core: storage, `build_parser`, `add`. Stretch: `list`, totals, `report`
- `make test-lesson LESSON=08-capstone-cli` until green

**Next: Phase 2 — Lesson 09, type hints & mypy.**
````

- [ ] **Step 3: Fix the deck `<title>` in `slides/index.html`**

The scaffolder derives the title from the slug, producing `<title>Lesson 08 — Capstone Cli</title>`. Edit that one line to EXACTLY (em-dash U+2014):
```html
  <title>Lesson 08 — Phase 1 capstone: expense tracker CLI</title>
```
Do NOT change the `/shared/reveal/...` asset paths or anything else in the file.

- [ ] **Step 4: Build; confirm the link, the placeholder count and the asset paths**

```bash
make slides-build
grep -q 'href="lessons/08-capstone-cli/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
grep -oE '/shared/reveal|\.\./\.\./shared/reveal' dist/lessons/08-capstone-cli/slides/index.html | sort | uniq -c
test -f dist/lessons/08-capstone-cli/slides/index.html && test -f dist/lessons/08-capstone-cli/slides/slides.md && echo "SLIDES_COPIED"
grep -c '^---$' lessons/08-capstone-cli/slides/slides.md
rm -rf dist
```
Expected: `LINK_OK`; future-placeholder count **`20`** (28 catalogued lessons minus the 8 now published — Phase 1 is fully green); the asset-path grep shows ONLY `/shared/reveal`; `SLIDES_COPIED`; the separator count is `11` (12 slides).

- [ ] **Step 5: Dev-server smoke test**

```bash
lsof -ti:8000 && echo "PORT 8000 BUSY — do not run the rest of this step"
( uv run python -m slides_dev --lesson 08-capstone-cli --repo-root "$(pwd)" --port 8000 >/dev/null 2>&1 & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
kill $(lsof -ti:8000) 2>/dev/null || true
lsof -ti:8000 || echo "port clear"
```
Expected: nothing from the first `lsof` (if it prints a PID, another server already owns port 8000 — do not run the rest of the step, and report BLOCKED rather than killing it); then the title line `<title>Lesson 08 — Phase 1 capstone: expense tracker CLI</title>`, `slidesmd=200`, `revealcss=200`, `port clear`.

- [ ] **Step 6: Commit**

```bash
git add lessons/08-capstone-cli/slides/slides.md lessons/08-capstone-cli/slides/index.html
git commit -m "feat(lesson-08): author the slide deck"
```
(No `Co-Authored-By` trailer.)

---

## Task 7: Final verification

**Interfaces:**

- **Consumes from Tasks 1-6:** the finished lesson on disk and six commits on the branch.
- **Produces:** the one repo-level change this lesson is allowed outside its own folder — the `.gitignore` block for the learner's generated `expenses.txt` — and the evidence that the whole quality bar is green.
- **Diff under review:** the two-line `.gitignore` hunk, and nothing else. Steps 3-6 change no file — their evidence lives only in this task's report, so the review checks that the report quotes the expected strings (`All checks passed!`, `Success: no issues found in 13 source files`, `39 failed, 2 passed`, `41 passed`, `39 failed, 43 passed`, `LINK_OK`, `20`, the 27-path `git ls-files` listing, `no trailers — good`) rather than re-running them.

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-08-capstone-cli`. If not, STOP and report BLOCKED.

- [ ] **Step 2: Add the `.gitignore` entry (unanchored)**

Append these two lines at the end of the repo-root `.gitignore` (after the `# Editors / OS` block), separated from it by one blank line:

```gitignore
# Lesson 08 capstone: the learner's local expense file
expenses.txt
```

The pattern is deliberately **unanchored** (`expenses.txt`, not `/lessons/08-capstone-cli/expenses.txt`): it must also cover a learner who runs the demo from the repo root or from any other directory. Verify:

```bash
tail -3 .gitignore
git check-ignore -v expenses.txt lessons/08-capstone-cli/expenses.txt
git add .gitignore
git commit -m "chore(lesson-08): ignore the learner's generated expenses.txt"
```
Expected: the two lines above at the end of the file (`tail -3` prints the blank line, the comment and the pattern), `git check-ignore` reporting `.gitignore:NN:expenses.txt` for **both** paths (`NN` is 36 against today's 33-line `.gitignore`), and the commit created (no `Co-Authored-By` trailer). This is the seventh and last commit — Steps 3-6 only verify, they change no file.

- [ ] **Step 3: Full quality bar**

```bash
make lint
uv run ruff format --check .
make typecheck
make test
```
Expected: `make lint` → `All checks passed!` (absolute imports satisfy TID252; the four `# noqa` pragmas in `exercises/` are the only suppressions); `ruff format --check .` → no diff; `make typecheck` → `Success` (tools only — lesson code is not a mypy gate); `make test` → tools (51) plus Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10), 06 (11), 07 (7) and **08 (41)** solutions all passing, each lesson in its own pytest process; exit 0; no `import file mismatch`.

- [ ] **Step 4: Lesson red/green and a run of the real program**

```bash
make test-lesson LESSON=08-capstone-cli
( cd lessons/08-capstone-cli && uv run pytest exercises solutions -q | tail -1 )
( cd lessons/08-capstone-cli && rm -f demo.txt \
  && uv run python -m solutions.cli --file demo.txt add 2026-09-21 coffee 4.50 \
  && uv run python -m solutions.cli --file demo.txt report ; echo "exit=$?" ; rm -f demo.txt )
```
Expected: `make test-lesson` → exercises `39 failed, 2 passed` (the target tolerates the failure), solutions `41 passed`, exit 0; the one-process run → `39 failed, 43 passed` with no `import file mismatch`; the demo prints
```
Added coffee $4.50 on 2026-09-21.
CATEGORY  TOTAL
coffee    $4.50
exit=0
```

- [ ] **Step 5: Landing page, git hygiene, no attribution trailers**

```bash
make slides-build
grep -q 'href="lessons/08-capstone-cli/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
rm -rf dist
git status --porcelain -- lessons/08-capstone-cli .gitignore uv.lock
git ls-files lessons/08-capstone-cli | sort
git diff --stat main..HEAD -- . ':!lessons/08-capstone-cli'
git log --oneline main..HEAD
git log main..HEAD --format='%B' | grep -i 'co-authored\|generated with' && echo "TRAILER FOUND (bad)" || echo "no trailers — good"
```
Expected:
- `LINK_OK`; future-placeholder count `20`.
- Clean tree for everything this lesson owns (the scoped `git status --porcelain` prints nothing — in particular no stray `expenses.txt` or `demo.txt`; `dist/` and `.pytest_cache/` are already ignored by the repo `.gitignore`). Untracked files elsewhere in the repo — notably this plan under `docs/superpowers/plans/` — are expected and are not this branch's business.
- `git ls-files lessons/08-capstone-cli` lists exactly **27** files: `pyproject.toml`, `README.md`, `slides/{index.html,slides.md,assets/.gitkeep}`, and in each of `exercises/` and `solutions/`: `__init__.py`, `expense.py`, `storage.py`, `cli.py`, `test_reporting.py`, `test_expense.py`, `test_storage.py`, `test_cli.py`, `reporting/{__init__.py,money.py,table.py}` — and NO `main.py` / `test_main.py`.
- Outside the lesson folder, the diff touches only `.gitignore` and `uv.lock`.
- 7 commits; `no trailers — good`.

- [ ] **Step 6: Confirm the port is clear** — `lsof -ti:8000 || echo "port clear"` → `port clear`.

- [ ] **Step 7: Report**

If Steps 3-6 surfaced nothing to change, report CLEAN — the `.gitignore` commit from Step 2 is the last one. If any check FAILED, STOP and report BLOCKED with the failing command and its output. (Do NOT push.)

---

## Notes for execution

- **Seven commits** when done, in this order:
  1. `feat(lesson-08): scaffold the lesson and add the given reporting package`
  2. `feat(lesson-08): add expense.py (the Expense record, filtering and totals)`
  3. `feat(lesson-08): add storage.py (the line format, load and save)`
  4. `feat(lesson-08): add cli.py (argparse subcommands, dispatch, exit codes)`
  5. `docs(lesson-08): author the README (files, argparse, the capstone brief)`
  6. `feat(lesson-08): author the slide deck`
  7. `chore(lesson-08): ignore the learner's generated expenses.txt`
- **Mirror Lessons 06/07** for any shape question (file layout, README section order, deck style, `<title>` handling).
- **Never** add a `Co-Authored-By` / AI-attribution trailer; **never** push or open a PR — the controller finishes the branch.
- **Never edit the catalog, the Makefile, the ruff config or the mypy scope.** The only files touched outside `lessons/08-capstone-cli/` are `.gitignore` (Task 7) and `uv.lock` (Task 1).

Deliberate design points an implementer might "fix" by mistake:

- **`test_reporting.py` is green in the exercises tree from minute zero.** Its 2 passing cases are not an oversight and not a bug — they are the documentation for the given `reporting` package. `39 failed, 2 passed` is the correct first result; do not make them red, and do not add more tests for `reporting`'s internals.
- **The eight stubs must stay unimplemented in `exercises/`.** Every stub is importable and raises at **call** time (`raise NotImplementedError("implement <name>() so the tests pass")`), never at import time — an import-time failure would take the whole suite down and hide the progress bar. Do not "helpfully" implement one, and do not change a stub message: the messages are quoted in the spec and in the lesson.
- **The exercise and solution copies differ by more than the test import line.** Absolute imports (TID252) mean `reporting/__init__.py`, `storage.py` and `cli.py` carry the `exercises.` / `solutions.` prefix, and `exercises/` additionally carries four `# noqa` pragmas and the appended stub-docstring paragraphs. Only `reporting/money.py` and `reporting/table.py` are byte-identical.
- **The four `# noqa` pragmas are required, not clutter.** `import os  # noqa: F401 -- os.path.exists() is for load_expenses()` in `exercises/storage.py`; three `# noqa: F401` on the grouped imports in `exercises/cli.py`; `# noqa: F841 -- you use it` on its `subparsers` line. Stripping them gives 11 ruff diagnostics on 5 lines and a red `make lint`. `RUF100` is not selected, so they do not start failing once the learner finishes.
- **`build_parser().parse_args(argv)` in the `main` stub is a bare expression on purpose** — `args = ...` would trip F841. It is what makes `--help` work before `main` exists.
- **Sub-cent rounding is intentional.** `is_amount` validates the string the user typed, not the float it becomes, so `add … tip 0.005` is stored as `0.01`. That is a Going further exercise, not a bug to fix.
- **`float` money, exact-equality assertions, `rent` stored before `groceries`, and `rent 1200.00`** are all load-bearing: binary-exact fractions mean no `pytest.approx`; a non-alphabetical fixture is what makes `sorted()` testable; and four figures force the thousands separator that only `format_money` produces, which is what makes the black box a graded dependency.
- **No `try`/`except`, no `pathlib`/`json`/`csv`/`datetime`, no `type=float` on the `amount` argument, no `argv=None` default, no `--file` on the subparsers.** Each of these was considered and rejected in the spec for a reason the lesson teaches.
