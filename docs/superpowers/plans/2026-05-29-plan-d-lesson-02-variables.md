# Plan D — Lesson 02 (Variables, types, operators)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the second course lesson — a temperature-converter module (`to_celsius`, `to_fahrenheit`, `format_temp`, `is_freezing`) that exercises Python's primitive types, operators, conversions, f-strings, and a `FREEZING_F` constant.

**Architecture:** Scaffold `lessons/02-variables/` with the existing `new_lesson` tool, replace the placeholder exercise with the four temperature functions (exercise stubs raise `NotImplementedError`; solutions implemented), author the README and slide deck. No tooling or harness changes — Plan C already made `make test` multi-lesson-safe, and this lesson is the first real two-lesson exercise of that fix.

**Tech Stack:** Python 3.13, uv workspace, pytest, ruff, mypy, GNU Make, the existing `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored).

---

## Context for the implementer

- **Repo state:** Plans A, B, C merged to `main`. `lessons/01-hello/` exists and is the pattern to mirror. The `make test` / `test-lesson` targets run each lesson in an isolated pytest process (Plan C). `lessons/` currently holds only `01-hello`.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`). After scaffolding a lesson, run it.
- **`make new-lesson NAME=02-variables`** produces `lessons/02-variables/` with `pyproject.toml` (name `lesson-02-variables`, `[tool.uv] package=false`, `[tool.pytest.ini_options] pythonpath=["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}` (placeholder no-arg `hello()`). The scaffolder derives the deck title from the slug ("Variables").
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("02", "variables", "Variables, types, operators", …, 1)`, so `dir_name()` is `02-variables`. Once `lessons/02-variables/slides/` exists, `build_index` renders it as a link. No catalog change needed.
- **Test invocation:** run a lesson's tests from inside the lesson dir, e.g. `( cd lessons/02-variables && uv run pytest solutions )`, OR via `make test-lesson LESSON=02-variables`. This is what makes `from solutions.temperature import …` resolve (the lesson's `pythonpath=["."]`).
- **Design spec:** `docs/superpowers/specs/2026-05-29-lesson-02-variables-design.md`.
- **Mirror Lesson 01** at `lessons/01-hello/` for exact file shapes, README structure, and slide style.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Commit messages:** Conventional Commits. **Do NOT add a `Co-Authored-By` trailer or any AI-attribution line to commits** (project rule). Subject + body only.
- **Do NOT push** — the controller handles branch finishing.
- The module file is named `temperature.py` (and tests `test_temperature.py`), replacing the scaffold's `main.py`/`test_main.py`.

---

## File Structure

```
lessons/02-variables/                    (NEW — scaffolded then authored)
├── pyproject.toml                       (from scaffold; unchanged)
├── README.md                            (authored — Task 2)
├── slides/
│   ├── index.html                       (from scaffold; <title> tweaked — Task 3)
│   ├── slides.md                        (authored — Task 3)
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py                      (from scaffold; kept, empty)
│   ├── temperature.py                   (authored — Task 1; replaces main.py)
│   └── test_temperature.py              (authored — Task 1; replaces test_main.py)
└── solutions/
    ├── __init__.py                      (from scaffold; kept, empty)
    ├── temperature.py                   (authored — Task 1)
    └── test_temperature.py              (authored — Task 1)
```

---

## Task 1: Scaffold lesson 02 and author the exercise + solution

**Files:**
- Create (via scaffold): `lessons/02-variables/` tree
- Create: `lessons/02-variables/exercises/temperature.py`, `.../exercises/test_temperature.py`
- Create: `lessons/02-variables/solutions/temperature.py`, `.../solutions/test_temperature.py`
- Delete (scaffold placeholders): `lessons/02-variables/{exercises,solutions}/main.py` and `.../test_main.py`

- [ ] **Step 1: Scaffold the lesson**

Run: `make new-lesson NAME=02-variables`
Expected: prints `created lessons/02-variables`; the tree exists with the scaffold files.

Run: `uv sync --all-packages`
Expected: registers `lesson-02-variables`; exits 0.

- [ ] **Step 2: Remove the placeholder files**

```bash
rm lessons/02-variables/exercises/main.py lessons/02-variables/exercises/test_main.py
rm lessons/02-variables/solutions/main.py lessons/02-variables/solutions/test_main.py
```

(Keep both `__init__.py` files and `slides/assets/.gitkeep`.)

- [ ] **Step 3: Write the solution tests (TDD red)**

Create `lessons/02-variables/solutions/test_temperature.py`:

```python
from solutions.temperature import (
    format_temp,
    is_freezing,
    to_celsius,
    to_fahrenheit,
)


def test_to_celsius_freezing() -> None:
    assert to_celsius(32.0) == 0.0


def test_to_celsius_boiling() -> None:
    assert to_celsius(212.0) == 100.0


def test_to_fahrenheit_freezing() -> None:
    assert to_fahrenheit(0.0) == 32.0


def test_to_fahrenheit_boiling() -> None:
    assert to_fahrenheit(100.0) == 212.0


def test_round_trip_is_exact_for_boiling() -> None:
    assert to_fahrenheit(to_celsius(212.0)) == 212.0


def test_format_temp_one_decimal() -> None:
    assert format_temp(37.0) == "37.0°C"


def test_format_temp_negative() -> None:
    assert format_temp(-12.5) == "-12.5°C"


def test_is_freezing_at_zero() -> None:
    assert is_freezing(0.0) is True


def test_is_freezing_below() -> None:
    assert is_freezing(-5.0) is True


def test_is_freezing_above() -> None:
    assert is_freezing(10.0) is False
```

- [ ] **Step 4: Run the solution tests — verify RED**

Run: `( cd lessons/02-variables && uv run pytest solutions )`
Expected: collection error / `ModuleNotFoundError: No module named 'solutions.temperature'` (temperature.py doesn't exist yet).

- [ ] **Step 5: Write the solution (TDD green)**

Create `lessons/02-variables/solutions/temperature.py`:

```python
FREEZING_F = 32.0  # water freezes at 32°F / 0°C


def to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius."""
    return (fahrenheit - FREEZING_F) * 5 / 9


def to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * 9 / 5 + FREEZING_F


def format_temp(celsius: float) -> str:
    """Format a Celsius temperature to one decimal place, e.g. "20.0°C"."""
    return f"{celsius:.1f}°C"


def is_freezing(celsius: float) -> bool:
    """Return True if the temperature is at or below freezing (0°C)."""
    return celsius <= 0


if __name__ == "__main__":
    # Body temperature: 98.6°F in Celsius, formatted.
    print(format_temp(to_celsius(98.6)))
```

- [ ] **Step 6: Run the solution tests — verify GREEN**

Run: `( cd lessons/02-variables && uv run pytest solutions )`
Expected: 10 passed.

- [ ] **Step 7: Write the exercise stub + its (fail-by-design) test**

Create `lessons/02-variables/exercises/temperature.py`:

```python
FREEZING_F = 32.0  # water freezes at 32°F / 0°C


def to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius."""
    raise NotImplementedError("implement to_celsius() so the tests pass")


def to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    raise NotImplementedError("implement to_fahrenheit() so the tests pass")


def format_temp(celsius: float) -> str:
    """Format a Celsius temperature to one decimal place, e.g. "20.0°C"."""
    raise NotImplementedError("implement format_temp() so the tests pass")


def is_freezing(celsius: float) -> bool:
    """Return True if the temperature is at or below freezing (0°C)."""
    raise NotImplementedError("implement is_freezing() so the tests pass")


if __name__ == "__main__":
    # Body temperature: 98.6°F in Celsius, formatted.
    print(format_temp(to_celsius(98.6)))
```

Create `lessons/02-variables/exercises/test_temperature.py` (identical to the solutions test except the import line):

```python
from exercises.temperature import (
    format_temp,
    is_freezing,
    to_celsius,
    to_fahrenheit,
)


def test_to_celsius_freezing() -> None:
    assert to_celsius(32.0) == 0.0


def test_to_celsius_boiling() -> None:
    assert to_celsius(212.0) == 100.0


def test_to_fahrenheit_freezing() -> None:
    assert to_fahrenheit(0.0) == 32.0


def test_to_fahrenheit_boiling() -> None:
    assert to_fahrenheit(100.0) == 212.0


def test_round_trip_is_exact_for_boiling() -> None:
    assert to_fahrenheit(to_celsius(212.0)) == 212.0


def test_format_temp_one_decimal() -> None:
    assert format_temp(37.0) == "37.0°C"


def test_format_temp_negative() -> None:
    assert format_temp(-12.5) == "-12.5°C"


def test_is_freezing_at_zero() -> None:
    assert is_freezing(0.0) is True


def test_is_freezing_below() -> None:
    assert is_freezing(-5.0) is True


def test_is_freezing_above() -> None:
    assert is_freezing(10.0) is False
```

- [ ] **Step 8: Verify the exercise tests fail as designed**

Run: `( cd lessons/02-variables && uv run pytest exercises )`
Expected: 10 failed with `NotImplementedError`. (Intended deliverable — the failing tests are the student's spec.)

- [ ] **Step 9: Verify the make targets**

Run: `make test-lesson LESSON=02-variables`
Expected: exercises section FAILS (NotImplementedError, tolerated by the leading `-`); solutions section PASSES (10); overall exit 0.

Run: `make test`
Expected: tool suite passes (50), then `== lessons/01-hello/solutions ==` passes (2) AND `== lessons/02-variables/solutions ==` passes (10); exit 0. **This is the first time `make test` spans two lessons — confirm there is NO `import file mismatch` error.**

- [ ] **Step 10: Verify the runnable module (solution)**

Run: `( cd lessons/02-variables && uv run python -m solutions.temperature )`
Expected: prints `37.0°C`.

Run: `( cd lessons/02-variables && uv run python -m exercises.temperature )`
Expected: raises `NotImplementedError` (exercise not implemented — correct).

- [ ] **Step 11: Lint, format, type-check**

Run: `make lint`
Expected: All checks passed!

Run: `uv run ruff format --check .`
Expected: all files formatted (no diff). If it reports the new files would be reformatted, run `uv run ruff format lessons/02-variables` and re-check; note it in your report.

Run: `uv run mypy lessons/02-variables/solutions/temperature.py lessons/02-variables/exercises/temperature.py`
Expected: Success. (Not a CI gate, but the lesson code should be cleanly typed.)

- [ ] **Step 12: Commit**

```bash
git add lessons/02-variables uv.lock
git commit -m "feat(lesson-02): add temperature-converter exercise + solution"
```

(No `Co-Authored-By` trailer.)

---

## Task 2: Author the lesson README

**Files:**
- Modify: `lessons/02-variables/README.md` (replace the scaffold's TODO placeholders)

- [ ] **Step 1: Overwrite `lessons/02-variables/README.md`**

````markdown
# Lesson 02 — Variables, types, operators

Store values in variables, work with Python's core types, and combine them
with operators. By the end you will have built a small temperature converter
and learned why `1 / 2` is `0.5` but `1 // 2` is `0`.

## Learning goals

- Assign values to variables and name them well (`snake_case`)
- Recognise the core built-in types: `int`, `float`, `str`, `bool`, `None`
- Use arithmetic and comparison operators, including `/` versus `//`
- Format values with f-strings (`f"{x:.1f}"`)
- Understand truthiness and "constants by convention"

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md).

## Concepts

**Variables.** A variable is a name bound to a value: `freezing = 32.0`. Names
use `snake_case`. Assignment binds the name; it does not copy.

**The core types.** `int` (whole numbers), `float` (decimals), `str` (text),
`bool` (`True`/`False`), and `None` (the "no value" value). `type(x)` tells you
which one you have.

**Operators.** Arithmetic: `+ - * / // % **`. Note that `/` always produces a
`float` (`6 / 2` is `3.0`), `//` floors to an `int`-like result (`7 // 2` is
`3`), `%` is the remainder, and `**` is power. Comparisons (`== != < <= > >=`)
produce a `bool`.

**Conversions.** Convert between types explicitly: `int("3")`, `float(3)`,
`str(3)`. Reading user input (`input()`) always gives a `str`, so you convert
when you need a number.

**f-strings.** Build strings from values: `f"Hello, {name}!"`. A format spec
after a colon controls the display: `f"{value:.1f}"` shows one decimal place.

**Truthiness.** Any value can be tested for truth. Falsy values include `0`,
`0.0`, `""`, `None`, and empty collections; almost everything else is truthy.
Comparisons already return a real `bool`.

**Constants by convention.** Python has no `const` keyword. A name in
`UPPER_CASE` (like `FREEZING_F = 32.0`) signals "treat this as a constant" —
the language won't stop you reassigning it, but you shouldn't.

**Immutability intuition.** `int` and `str` values are immutable: `x = x + 1`
makes a new number and rebinds the name `x` — it does not change the original
object. (Mutable types like lists arrive in Lesson 05.)

## Exercise brief

Open `exercises/temperature.py` and implement four functions so the tests pass:
`to_celsius`, `to_fahrenheit`, `format_temp` (one decimal place, like
`"20.0°C"`), and `is_freezing` (at or below 0°C). A `FREEZING_F = 32.0` constant
is provided for you to use. Run the tests first to watch them fail, then make
them pass.

## How to run

Run the tests (exercises fail until you implement the functions; solutions pass):

```bash
make test-lesson LESSON=02-variables
```

Or directly:

```bash
cd lessons/02-variables && uv run pytest exercises
```

Run the module (prints a composed conversion; implement the functions first, or
it raises `NotImplementedError`):

```bash
cd lessons/02-variables && uv run python -m exercises.temperature
```

## Going further

- `divmod(17, 5)` returns `(3, 2)` — quotient and remainder at once.
- Floats are approximate: try `0.1 + 0.2` in the REPL (`uv run python`) — it is
  not exactly `0.3`. For exact money math, look at `decimal.Decimal`.
- Explore more f-string format specs: `f"{1234567:,}"`, `f"{0.25:.0%}"`,
  `f"{42:>6}"` (width and alignment).
````

- [ ] **Step 2: Verify**

Run: `grep -c '```' lessons/02-variables/README.md` → expect an EVEN number.
Run: `grep -q "Variables, types, operators" lessons/02-variables/README.md && grep -q "make test-lesson LESSON=02-variables" lessons/02-variables/README.md && echo "readme ok"` → expect `readme ok`.
Run: `grep -iE 'TODO' lessons/02-variables/README.md && echo "HAS TODO" || echo "no todos"` → expect `no todos`.

- [ ] **Step 3: Commit**

```bash
git add lessons/02-variables/README.md
git commit -m "docs(lesson-02): author the README (types, operators, conversions, f-strings)"
```

(No `Co-Authored-By` trailer.)

---

## Task 3: Author the slide deck

**Files:**
- Modify: `lessons/02-variables/slides/slides.md` (replace the template deck)
- Modify: `lessons/02-variables/slides/index.html` (deck `<title>` only)

- [ ] **Step 1: Overwrite `lessons/02-variables/slides/slides.md`**

````markdown
## Lesson 02
### Variables, types, operators

Store values, pick the right type, combine them with operators.

Note:
We build a small temperature converter in the exercise.

---

## Variables

```python
freezing = 32.0
name = "Aki"
```

- A variable is a name bound to a value
- Names use `snake_case`
- Assignment binds the name; it does not copy

---

## The core types

- `int` — whole numbers: `42`
- `float` — decimals: `3.14`
- `str` — text: `"hello"`
- `bool` — `True` / `False`
- `None` — the "no value" value

`type(x)` tells you which one you have.

---

## Operators

```python
7 + 2    # 9
7 / 2    # 3.5   (always a float)
7 // 2   # 3     (floor division)
7 % 2    # 1     (remainder)
2 ** 10  # 1024  (power)
```

Comparisons (`== != < <= > >=`) return a `bool`.

---

## Conversions

```python
int("3")    # 3
float(3)    # 3.0
str(3)      # "3"
```

- Convert between types explicitly
- `input()` always returns a `str` — convert to compute

---

## f-strings

```python
celsius = 20.0
f"{celsius:.1f}°C"   # "20.0°C"
```

- `f"..."` builds a string from values
- A format spec after `:` controls display — `.1f` is one decimal

---

## bool & truthiness

- Comparisons return a real `bool`
- Falsy: `0`, `0.0`, `""`, `None`, empty collections
- Almost everything else is truthy

```python
bool(0)    # False
bool("hi") # True
```

---

## Constants by convention

```python
FREEZING_F = 32.0
```

- No `const` keyword in Python
- `UPPER_CASE` means "treat as constant"
- The language won't stop you — it's a convention

---

## Immutability intuition

```python
x = 1
x = x + 1   # new number, name rebound
```

- `int` and `str` are immutable
- Rebinding a name is not the same as mutating an object
- Mutable types (lists) arrive in Lesson 05

---

## Your turn

- Implement the four functions in `exercises/temperature.py`
- `make test-lesson LESSON=02-variables` until green
- Run it: `uv run python -m exercises.temperature`

---

## What's next

**Lesson 03 — Control flow.**
````

- [ ] **Step 2: Fix the deck `<title>` in index.html**

In `lessons/02-variables/slides/index.html`, find the `<title>` line (the scaffolder set it from the slug, e.g. `<title>Lesson 02 — Variables</title>`) and change it to:

```html
  <title>Lesson 02 — Variables, types, operators</title>
```

(Only the `<title>` text changes.)

- [ ] **Step 3: Build the site; confirm the lesson is a LINK**

Run: `make slides-build`
Expected: prints `built dist`.

Run:
```bash
grep -q 'href="lessons/02-variables/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
test -f dist/lessons/02-variables/slides/index.html && test -f dist/lessons/02-variables/slides/slides.md && echo "SLIDES_COPIED"
```
Expected: `LINK_OK`; future-placeholder count is now `26` (lessons 01 and 02 are both links); `SLIDES_COPIED`.

Run: `rm -rf dist`

- [ ] **Step 4: Dev-server smoke test**

```bash
( uv run python -m slides_dev --lesson 02-variables --repo-root "$(pwd)" --port 8000 & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
kill "$(lsof -ti:8000)" 2>/dev/null || true
```
Expected: title line `<title>Lesson 02 — Variables, types, operators</title>`, `slidesmd=200`, `revealcss=200`. Confirm `lsof -ti:8000` is empty afterward.

- [ ] **Step 5: Commit**

```bash
git add lessons/02-variables/slides/slides.md lessons/02-variables/slides/index.html
git commit -m "feat(lesson-02): author the slide deck"
```

(No `Co-Authored-By` trailer.)

---

## Task 4: Final verification

End-to-end check. No new code unless something needs tidying.

- [ ] **Step 1: Full quality bar**

```bash
make lint
uv run ruff format --check .
make typecheck
make test
```
Expected:
- `make lint` → All checks passed!
- `ruff format --check .` → all files formatted (no diff).
- `make typecheck` → Success (tools; 13 source files).
- `make test` → tool suite passes (50), Lesson 01 solutions pass (2), Lesson 02 solutions pass (10); exit 0; **no `import file mismatch`**.

- [ ] **Step 2: Lesson red/green**

```bash
make test-lesson LESSON=02-variables
```
Expected: exercises FAIL (NotImplementedError, tolerated); solutions PASS (10); exit 0.

- [ ] **Step 3: Module runs (solution)**

```bash
( cd lessons/02-variables && uv run python -m solutions.temperature )
```
Expected: prints `37.0°C`.

- [ ] **Step 4: Landing page link + git hygiene**

```bash
make slides-build
grep -q 'href="lessons/02-variables/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
rm -rf dist
git status --porcelain
git ls-files lessons/02-variables | sort
git log --oneline main..HEAD
```
Expected: `LINK_OK`; future count `26`; clean working tree (no `dist/`); `lessons/02-variables` has pyproject.toml, README.md, slides/{index.html,slides.md,assets/.gitkeep}, exercises/{__init__.py,temperature.py,test_temperature.py}, solutions/{__init__.py,temperature.py,test_temperature.py} — NO main.py/test_main.py; the log shows 3 commits (exercise+solution, README, slides).

- [ ] **Step 5: Confirm port clear**

```bash
lsof -ti:8000 || echo "port clear"
```
Expected: `port clear`.

- [ ] **Step 6: Commit only if Steps 1-5 surfaced changes**

```bash
git status
```
If clean, report CLEAN. If anything changed (e.g., a ruff format tidy), investigate and commit (no co-author trailer).

---

## Notes for execution

- No tooling/harness changes, no `gcloud`, no secrets, no push. The deploy pipeline picks the lesson up automatically on the next merge to `main` (catalog already lists it).
- This lesson is the first real two-lesson `make test` run — it validates the Plan C harness fix at 2+ lessons. If `make test` ever shows `import file mismatch`, STOP and report (it would mean the harness fix regressed).
- Commits must NOT include `Co-Authored-By` or AI-attribution trailers (project rule).
