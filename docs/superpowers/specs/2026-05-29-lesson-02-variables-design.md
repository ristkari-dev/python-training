# Lesson 02 — Variables, types, operators — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-05-29
**Owner:** Aki Ristkari

## Summary

The second course lesson. Students implement a small temperature-converter module — four functions that exercise Python's primitive types, arithmetic and comparison operators, type conversions, and f-string formatting. A module-level `FREEZING_F` constant demonstrates "constants by convention". The lesson follows the four-file convention established by Lesson 01 and is the first lesson to exercise the multi-lesson `make test` harness fix (Plan C) with two lessons present.

## Scope (from the course design spec)

Lesson 2 covers: `int`/`float`/`str`/`bool`/`None`, truthiness, f-strings, immutability-vs-mutability intuition, and constants by convention. Control flow (`if`/`elif`) is Lesson 03, so the exercise must not require branching — comparison operators that return `bool` are fine; `if` statements are not.

## Exercise — temperature converter

A cohesive four-function module, `temperature.py`, with a provided `FREEZING_F = 32.0` constant.

### Functions

- `to_celsius(fahrenheit: float) -> float` — `(fahrenheit - FREEZING_F) * 5 / 9`. Float arithmetic, operator precedence, the provided constant.
- `to_fahrenheit(celsius: float) -> float` — `celsius * 9 / 5 + FREEZING_F`.
- `format_temp(celsius: float) -> str` — `f"{celsius:.1f}°C"`. f-string formatting / format spec; int/float→str.
- `is_freezing(celsius: float) -> bool` — `celsius <= 0`. Covers the `bool` type via a comparison operator.

`FREEZING_F = 32.0` is provided in both the exercise stub and the solution (it is not something the student implements; it demonstrates the UPPER_CASE constant convention and is used by the conversion functions).

### Coverage mapping

- **int/float/str** — conversion functions take/return floats; `format_temp` returns a str.
- **bool** — `is_freezing` returns a bool via `<=`.
- **operators** — `-`, `*`, `/`, `+`, and `<=` across the four functions.
- **f-strings** — `format_temp`'s `f"{celsius:.1f}°C"`.
- **constants by convention** — `FREEZING_F`.
- **None, truthiness, immutability-vs-mutability** — taught on the slides + README only (not graded). Truthiness is exercised for real in Lesson 03 (control flow). `None` and immutability are conceptual at this stage; lists/tuples (mutability) arrive in Lesson 05.

### `exercises/temperature.py` (stub)

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

### `solutions/temperature.py`

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

The `if __name__ == "__main__":` block is non-interactive (no `input()`); it prints `37.0°C` once implemented and demonstrates function composition. Running it before implementing raises `NotImplementedError` — expected; the README says run the tests first.

### Tests (`exercises/test_temperature.py` / `solutions/test_temperature.py`)

Identical except the import line (`exercises.temperature` vs `solutions.temperature`). Ten tests, all chosen so the expected values are exactly representable in float — no rounding-dependent assertions, so the suite is not flaky.

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

The solutions copy is byte-identical except the first import line reads `from solutions.temperature import (...)`.

**Float-pitfall avoidance (deliberate):** round-trip is asserted only on 212.0 (where `to_celsius`→100.0 and `to_fahrenheit`→212.0 are both exact); `format_temp` is asserted only on values whose one-decimal form is exact (`37.0`, `-12.5`). Values like `to_fahrenheit(to_celsius(98.6))` or `f"{20.05:.1f}"` are intentionally NOT asserted because float representation makes them surprising — that surprise is surfaced as a "going further" note, not a graded test. `is_freezing` uses `is True`/`is False` to pin that a real `bool` is returned (a comparison returns an actual `bool`).

## Files

`lessons/02-variables/` (scaffold with `make new-lesson NAME=02-variables`, then author; replace the placeholder `main.py`/`test_main.py` with `temperature.py`/`test_temperature.py`):

```
lessons/02-variables/
├── pyproject.toml          # name "lesson-02-variables", package=false, pytest pythonpath=["."]
├── README.md               # authored
├── slides/
│   ├── index.html          # scaffold; <title> set to "Lesson 02 — Variables, types, operators"
│   ├── slides.md           # authored
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py         # empty (kept)
│   ├── temperature.py
│   └── test_temperature.py
└── solutions/
    ├── __init__.py         # empty
    ├── temperature.py
    └── test_temperature.py
```

## Slides (`slides/slides.md`)

About ten slides, `---` separated, code in fenced `python` blocks, ~15 visible lines max. `Note:` speaker notes where useful.

1. **Title** — "Lesson 02 — Variables, types, operators" + one-line goal.
2. **Variables & assignment** — `x = 5`; names are labels; `snake_case`.
3. **The core types** — `int`, `float`, `str`, `bool`, `None`; `type(x)`.
4. **Operators** — arithmetic `+ - * / // % **`; comparison `== != < <= > >=`.
5. **Conversions** — `int("3")`, `float(3)`, `str(3)`; note `/` always yields `float`, `//` floors.
6. **f-strings & format specs** — `f"{c:.1f}°C"`, a couple of format-spec examples.
7. **bool & truthiness** — comparisons return `bool`; falsy values (`0`, `0.0`, `""`, `None`, empty); `bool(x)`.
8. **Constants by convention** — `FREEZING_F = 32.0`; UPPER_CASE; "Python won't enforce it — it's a convention."
9. **Immutability intuition** — `int`/`str` are immutable; `x = x + 1` rebinds the name, it doesn't mutate the object (intuition only; mutability proper arrives with lists in Lesson 05).
10. **Your turn + what's next** — implement the four functions; pointer to Lesson 03 — Control flow.

## README (`README.md`)

Four-file-convention sections:

- **Learning goals** — variables & assignment + naming; the core built-in types and when each is used; arithmetic and comparison operators (incl. `/` vs `//`); f-string formatting; `bool`, truthiness, and constants by convention.
- **Prereqs** — Lesson 01.
- **Concepts** — short paragraphs mirroring the deck: variables/assignment/naming; the five core types; operators (note `/` is float division, `//` floors, `%` remainder, `**` power); conversions; f-string format specs; truthiness (which values are falsy) and that comparisons return `bool`; constants by convention (UPPER_CASE); immutability intuition (rebinding vs mutating).
- **Exercise brief** — implement the four functions in `exercises/temperature.py` so the tests pass; run the module to see a composed conversion.
- **How to run** — `make test-lesson LESSON=02-variables` (or `cd lessons/02-variables && uv run pytest exercises`); run the module `cd lessons/02-variables && uv run python -m exercises.temperature`. Run the tests before running the module (an unimplemented function raises `NotImplementedError`).
- **Going further** — `divmod(a, b)`; `round()` and the classic `0.1 + 0.2 != 0.3` float surprise; a `decimal.Decimal` teaser for exact money math; more f-string format specs (`,`, `%`, width/alignment).

## Verification (success criteria)

- `make test-lesson LESSON=02-variables` → exercise tests FAIL with `NotImplementedError`; solution tests PASS (10); target exit 0.
- `make test` → tools + Lesson 01 solutions + Lesson 02 solutions all pass, in isolated per-lesson processes. **This is the first time `make test` spans two lessons — it confirms the Plan C harness fix works at 2+ lessons (no `import file mismatch`).**
- `cd lessons/02-variables && uv run python -m solutions.temperature` → prints `37.0°C`.
- `make slides-build` → `dist/index.html` shows `02-variables` as a link (no longer faded); future-placeholder count drops from 27 to 26; `dist/lessons/02-variables/slides/index.html` exists.
- `make lint` and `uv run ruff format --check .` → clean. `make typecheck` stays scoped to tools and remains clean; lesson code is cleanly typed but not a typecheck gate (strict lesson typing starts at Lesson 09).
- The deck renders via `make slides-dev LESSON=02-variables`.

## Non-goals

- No `if`/`elif`/`else` or loops (Lesson 03+). Comparison operators returning `bool` are fine; branching is not.
- No graded truthiness or `None` exercise (slides/README only); no mutability exercise (lists arrive Lesson 05).
- No catalog change — `02-variables` is already listed in `tools/build_index/src/build_index/catalog.py`.
- No changes to the tools or harness — Plan C already made `make test` multi-lesson-safe.
- No strict mypy gate on lesson code (starts Lesson 09); the code is nonetheless cleanly typed.

## Open items deferred to implementation planning

- Exact slide prose and README concept wording.
- Whether the deck's `index.html` `<title>` is hand-edited or left as the scaffolder's slug-derived value (default: hand-edit to "Lesson 02 — Variables, types, operators", matching Lesson 01's polish).
