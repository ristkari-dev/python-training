# Lesson 04 — Functions & tests — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-06-03
**Owner:** Aki Ristkari

## Summary

The fourth course lesson and the first to formally explain `pytest` — which has been a "magic test runner" since Lesson 01. It has two threads woven together: (1) Python's function calling conventions (positional/keyword args, defaults, `*args`, `**kwargs`, returning tuples), taught through four small functions students implement; and (2) pytest demystified (`assert`, `@pytest.mark.parametrize`, `@pytest.fixture`), taught by *showcasing* those features in this lesson's provided test file and walking through it in the slides and README. Students still only implement functions — the course's "provided tests are the spec" model is unchanged; no student-written tests (those can't be auto-verified). Fourth lesson, so `make test` now spans four lessons.

## Scope (from the course design spec)

Lesson 4: positional/keyword args, defaults, `*args`/`**kwargs`, return tuples; `pytest` properly introduced — `assert`, parametrize, fixtures basics. Functions (`def`) have been the exercise format since Lesson 01; this lesson formalizes the calling conventions. List **methods**/building lists are Lesson 05, so the exercise uses only `int`/`float`/`tuple` (and the `dict` that `**kwargs` produces, used read-only via `.values()`).

## Exercise — four calling-convention drills

A `functions.py` module with four functions, each isolating one facet. Bodies are one-liners on purpose — the teaching point is the *signature/calling convention*, not algorithmic complexity.

### Functions

- `power(base: float, exp: float = 2.0) -> float` — default argument + keyword argument. `base ** exp`.
- `total(*numbers: float) -> float` — variadic positional (`*args`); `sum(numbers)`. `total()` → `0.0`.
- `tally(**counts: int) -> int` — variadic keyword (`**kwargs`); `sum(counts.values())`. Demonstrates that `**kwargs` collects into a dict. `tally()` → `0`.
- `divmod_pair(a: int, b: int) -> tuple[int, int]` — returning a tuple, written as the explicit comma form `a // b, a % b` (to *show* tuple construction; the `divmod` builtin is a going-further note).

### Coverage mapping

- **positional args** — all four.
- **keyword args + defaults** — `power` (`exp=2.0`; callable as `power(5.0)` or `power(2.0, exp=3.0)`).
- **`*args`** — `total`.
- **`**kwargs`** — `tally`.
- **returning tuples (+ unpacking)** — `divmod_pair`; unpacking (`q, r = divmod_pair(...)`) shown on slides/README.

### `exercises/functions.py` (stub)

```python
def power(base: float, exp: float = 2.0) -> float:
    """Return base raised to exp. exp defaults to 2 (squaring)."""
    raise NotImplementedError("implement power() so the tests pass")


def total(*numbers: float) -> float:
    """Return the sum of all the numbers (0.0 if none)."""
    raise NotImplementedError("implement total() so the tests pass")


def tally(**counts: int) -> int:
    """Return the sum of all the keyword values (0 if none)."""
    raise NotImplementedError("implement tally() so the tests pass")


def divmod_pair(a: int, b: int) -> tuple[int, int]:
    """Return (quotient, remainder) of a divided by b."""
    raise NotImplementedError("implement divmod_pair() so the tests pass")


if __name__ == "__main__":
    print(power(5.0))                # 25.0
    print(total(1.0, 2.0, 3.0))      # 6.0
    print(tally(apples=3, pears=2))  # 5
    print(divmod_pair(17, 5))        # (3, 2)
```

### `solutions/functions.py`

```python
def power(base: float, exp: float = 2.0) -> float:
    """Return base raised to exp. exp defaults to 2 (squaring)."""
    return base**exp


def total(*numbers: float) -> float:
    """Return the sum of all the numbers (0.0 if none)."""
    return sum(numbers)


def tally(**counts: int) -> int:
    """Return the sum of all the keyword values (0 if none)."""
    return sum(counts.values())


def divmod_pair(a: int, b: int) -> tuple[int, int]:
    """Return (quotient, remainder) of a divided by b."""
    return a // b, a % b


if __name__ == "__main__":
    print(power(5.0))                # 25.0
    print(total(1.0, 2.0, 3.0))      # 6.0
    print(tally(apples=3, pears=2))  # 5
    print(divmod_pair(17, 5))        # (3, 2)
```

Note: `total()` and `tally()` with no arguments return `sum(())` (`0`) and `sum({}.values())` (`0`); `0 == 0.0` is `True`, so the empty-case assertions hold. The `__main__` block is non-interactive; it prints `25.0`, `6.0`, `5`, `(3, 2)` once implemented (running it before implementing raises `NotImplementedError` — expected; the README says run the tests first).

### Tests (`exercises/test_functions.py` / `solutions/test_functions.py`)

Identical except the import line. This file is the lesson's pytest teaching artifact: it deliberately uses a `@pytest.fixture` and `@pytest.mark.parametrize`, plus plain `assert` tests, and the README/slides reference it directly. Values are deterministic and float-exact.

```python
import pytest

from exercises.functions import divmod_pair, power, tally, total


@pytest.fixture
def sample_numbers() -> tuple[float, ...]:
    """A few numbers reused across tests."""
    return (1.0, 2.0, 3.0, 4.0)


@pytest.mark.parametrize(
    "base, exp, expected",
    [
        (3.0, 2.0, 9.0),
        (2.0, 3.0, 8.0),
        (5.0, 0.0, 1.0),
        (2.0, 10.0, 1024.0),
    ],
)
def test_power(base: float, exp: float, expected: float) -> None:
    assert power(base, exp) == expected


def test_power_default_exp_squares() -> None:
    assert power(5.0) == 25.0


def test_power_keyword_arg() -> None:
    assert power(2.0, exp=3.0) == 8.0


def test_total_empty_is_zero() -> None:
    assert total() == 0.0


def test_total_sums_args() -> None:
    assert total(1.0, 2.0, 3.0) == 6.0


def test_total_with_fixture(sample_numbers: tuple[float, ...]) -> None:
    assert total(*sample_numbers) == 10.0


def test_tally_empty_is_zero() -> None:
    assert tally() == 0


def test_tally_sums_keyword_values() -> None:
    assert tally(apples=3, pears=2, plums=5) == 10


def test_divmod_pair_returns_quotient_and_remainder() -> None:
    assert divmod_pair(17, 5) == (3, 2)


def test_divmod_pair_exact_division() -> None:
    assert divmod_pair(10, 2) == (5, 0)
```

The solutions copy is identical except the first import line reads `from solutions.functions import divmod_pair, power, tally, total`. `test_power` is parametrized over 4 cases, so pytest reports **13 test items** (4 + 9 plain). The `sample_numbers` fixture is consumed by `test_total_with_fixture`.

## Files

`lessons/04-functions/` (scaffold with `make new-lesson NAME=04-functions`, then author; replace the placeholder `main.py`/`test_main.py` with `functions.py`/`test_functions.py`):

```
lessons/04-functions/
├── pyproject.toml          # name "lesson-04-functions", package=false, pytest pythonpath=["."]
├── README.md               # authored
├── slides/
│   ├── index.html          # scaffold; <title> set to "Lesson 04 — Functions & tests"; absolute /shared/reveal paths (already correct)
│   ├── slides.md           # authored
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py         # empty (kept)
│   ├── functions.py
│   └── test_functions.py
└── solutions/
    ├── __init__.py         # empty
    ├── functions.py
    └── test_functions.py
```

## Slides (`slides/slides.md`)

About twelve slides, `---` separated, code in fenced `python` blocks, ~15 visible lines max. `Note:` speaker notes where useful. Two threads: functions, then pytest.

1. **Title** — "Lesson 04 — Functions & tests" + one-line goal.
2. **Defining functions** — `def name(params) -> ret:`; we've used them since Lesson 01, now formalize.
3. **Positional & keyword args** — `power(2.0, 3.0)` vs `power(2.0, exp=3.0)`.
4. **Default arguments** — `def power(base, exp=2.0)`; `power(5.0)` squares. (One-line caution: defaults are evaluated once — avoid mutable defaults.)
5. **`*args`** — `def total(*numbers)` collects extra positional args into a **tuple**.
6. **`**kwargs`** — `def tally(**counts)` collects extra keyword args into a **dict**.
7. **Returning tuples** — `return a // b, a % b`; unpack with `q, r = divmod_pair(17, 5)`.
8. **The magic, explained** — pytest finds `test_*.py` files and `test_*` functions and runs them.
9. **`assert`** — `assert power(5.0) == 25.0`; on failure pytest shows both sides.
10. **`parametrize`** — `@pytest.mark.parametrize(...)` runs one test over many inputs.
11. **`fixtures`** — `@pytest.fixture` supplies reusable setup/data to tests that name it.
12. **Your turn + what's next** — implement the four functions; pointer to Lesson 05 — Collections.

## README (`README.md`)

Four-file-convention sections:

- **Learning goals** — call functions with positional, keyword, and default arguments; gather extra arguments with `*args` and `**kwargs`; return and unpack tuples; understand how `pytest` discovers and runs tests, and read `assert`/`parametrize`/`fixtures`.
- **Prereqs** — Lessons 01, 02, 03.
- **Concepts** — function arguments (positional vs keyword; defaults, evaluated once); `*args` (a tuple of the extra positionals) and `**kwargs` (a dict of the extra keywords); returning a tuple and unpacking it; **pytest demystified** — test discovery (`test_*.py`, `test_*` functions), `assert` with rich failure output, `@pytest.mark.parametrize` (one test, many cases), `@pytest.fixture` (reusable setup/data). Point readers at this lesson's `test_functions.py` as a live example of all three.
- **Exercise brief** — implement `power`, `total`, `tally`, and `divmod_pair` in `exercises/functions.py` so the tests pass; then read `exercises/test_functions.py` to see a fixture and a parametrized test in action — that is the machinery that has been checking your work since Lesson 01.
- **How to run** — `make test-lesson LESSON=04-functions` (or `cd lessons/04-functions && uv run pytest exercises`); add `-v` to see each parametrized case listed separately (`cd lessons/04-functions && uv run pytest exercises -v`); run the module `cd lessons/04-functions && uv run python -m exercises.functions`. Run the tests before the module (an unimplemented function raises `NotImplementedError`).
- **Going further** — keyword-only parameters (`def f(*, key)`), positional-only (`def f(x, /)`); the `divmod(a, b)` builtin; the classic mutable-default-argument gotcha (`def f(items=[])`); pytest flags `-k` (select by name) and `-x` (stop on first failure).

## Verification (success criteria)

- `make test-lesson LESSON=04-functions` → exercise tests FAIL with `NotImplementedError`; solution tests PASS (13 items); target exit 0.
- `make test` → tools + Lessons 01 (2), 02 (10), 03 (15), 04 (13) solutions all pass, in isolated per-lesson processes; no `import file mismatch`. (Now spans four lessons.)
- `cd lessons/04-functions && uv run pytest solutions -v` → shows the four parametrized `test_power[...]` cases as separate items.
- `cd lessons/04-functions && uv run python -m solutions.functions` → prints `25.0`, `6.0`, `5`, `(3, 2)`.
- `make slides-build` → `dist/index.html` shows `04-functions` as a link (no longer faded); future-placeholder count drops from 25 to 24; the built deck uses absolute `/shared/reveal/...` asset paths (no `../../`); the deck renders in a browser (multiple slides, no `/shared/reveal` 404s).
- `make lint` and `uv run ruff format --check .` → clean. `make typecheck` stays scoped to tools and remains clean; lesson code is cleanly typed but not a typecheck gate (strict lesson typing starts at Lesson 09).
- The deck renders via `make slides-dev LESSON=04-functions`.

## Non-goals

- No student-written tests — the provided tests remain the spec; pytest features are taught by showcase + materials, not by asking students to author tests (which can't be auto-graded).
- No list construction / `.append` / comprehensions (Lesson 05). The exercise uses `int`/`float`/`tuple` and a read-only `dict` from `**kwargs`.
- No keyword-only/positional-only parameter syntax in the graded exercise — going-further only.
- No catalog change — `04-functions` is already listed in `tools/build_index/src/build_index/catalog.py`.
- No tooling/harness changes. No strict mypy gate on lesson code (starts Lesson 09); the code is nonetheless cleanly typed.

## Open items deferred to implementation planning

- Exact slide prose and README concept wording.
- Whether the deck's `index.html` `<title>` is hand-edited to "Lesson 04 — Functions & tests" (default: yes, matching prior lessons).
