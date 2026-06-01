# Lesson 03 — Control flow — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-06-01
**Owner:** Aki Ristkari

## Summary

The third course lesson and the first where branching and loops are allowed in the exercise. Students implement three small functions, each isolating one control-flow construct: `letter_grade` (if/elif/else), `count_vowels` (for-loop), and `collatz_steps` (while-loop). `match` and comprehensions are introduced as slides/README teasers only — they receive full treatment later (comprehensions in Lesson 05). Follows the four-file convention; third lesson, so `make test` now spans three lessons.

## Scope (from the course design spec)

Lesson 3 covers: `if`/`elif`/`else`, `for` over iterables, `while`, a `match` teaser, early returns, and a comprehensions intro. Functions (`def`) have been the exercise format since Lesson 01, so writing functions is fine; the *formal* treatment of functions (args, `*args`/`**kwargs`, pytest) is Lesson 04. List **methods** and building lists (`.append`, comprehensions as the primary tool) are Lesson 05, so the exercise uses only `int` and `str` — no list construction.

## Exercise — three single-construct drills

A `flow.py` module with three functions, each cleanly mapping to one construct. No list-building, no float.

### Functions

- `letter_grade(score: int) -> str` — `if`/`elif`/`else`. `A` for `>= 90`, `B` for `>= 80`, `C` for `>= 70`, `D` for `>= 60`, else `F`. The solution uses an `if`/`elif`/`else` chain with `return`s, which also models early-return style.
- `count_vowels(text: str) -> int` — `for` loop over a string with `in` membership. Counts vowels (`aeiouAEIOU`).
- `collatz_steps(n: int) -> int` — `while` loop. Counts steps to reach 1 under the Collatz rule (even → `n // 2`, odd → `3 * n + 1`); `n == 1` returns `0`. Uses `%` and `//` from Lesson 02.

### Coverage mapping

- **if/elif/else + early returns** — `letter_grade`.
- **for over iterables + `in`** — `count_vowels` (a string is the cleanest iterable available before lists arrive in Lesson 05).
- **while** — `collatz_steps`.
- **match teaser, comprehensions intro, `range`, `break`/`continue`, boolean operators (`and`/`or`/`not`)** — taught on the slides + README; not graded. `match` and comprehensions are deliberately teasers (comprehensions are Lesson 05's core topic).

### `exercises/flow.py` (stub)

```python
def letter_grade(score: int) -> str:
    """Return the letter grade for a score: A>=90, B>=80, C>=70, D>=60, else F."""
    raise NotImplementedError("implement letter_grade() so the tests pass")


def count_vowels(text: str) -> int:
    """Count the vowels (a, e, i, o, u — any case) in text."""
    raise NotImplementedError("implement count_vowels() so the tests pass")


def collatz_steps(n: int) -> int:
    """Count steps to reach 1 under the Collatz rule. n == 1 returns 0."""
    raise NotImplementedError("implement collatz_steps() so the tests pass")


if __name__ == "__main__":
    print(letter_grade(85))        # B
    print(count_vowels("hello"))   # 2
    print(collatz_steps(27))       # 111
```

### `solutions/flow.py`

```python
def letter_grade(score: int) -> str:
    """Return the letter grade for a score: A>=90, B>=80, C>=70, D>=60, else F."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def count_vowels(text: str) -> int:
    """Count the vowels (a, e, i, o, u — any case) in text."""
    count = 0
    for char in text:
        if char in "aeiouAEIOU":
            count += 1
    return count


def collatz_steps(n: int) -> int:
    """Count steps to reach 1 under the Collatz rule. n == 1 returns 0."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


if __name__ == "__main__":
    print(letter_grade(85))        # B
    print(count_vowels("hello"))   # 2
    print(collatz_steps(27))       # 111
```

The `__main__` block is non-interactive; it prints `B`, `2`, `111` once implemented. Running it before implementing raises `NotImplementedError` — expected; the README says run the tests first.

### Tests (`exercises/test_flow.py` / `solutions/test_flow.py`)

Identical except the import line. Thirteen tests, all deterministic (ints/strings; no float).

```python
from exercises.flow import collatz_steps, count_vowels, letter_grade


def test_grade_a() -> None:
    assert letter_grade(95) == "A"


def test_grade_a_boundary() -> None:
    assert letter_grade(90) == "A"


def test_grade_b_boundary() -> None:
    assert letter_grade(80) == "B"


def test_grade_c() -> None:
    assert letter_grade(72) == "C"


def test_grade_d_boundary() -> None:
    assert letter_grade(60) == "D"


def test_grade_f() -> None:
    assert letter_grade(40) == "F"


def test_count_vowels_basic() -> None:
    assert count_vowels("hello") == 2


def test_count_vowels_mixed_case() -> None:
    assert count_vowels("AEIOU xyz") == 5


def test_count_vowels_none() -> None:
    assert count_vowels("rhythm") == 0


def test_collatz_one() -> None:
    assert collatz_steps(1) == 0


def test_collatz_two() -> None:
    assert collatz_steps(2) == 1


def test_collatz_three() -> None:
    assert collatz_steps(3) == 7


def test_collatz_sixteen() -> None:
    assert collatz_steps(16) == 4
```

The solutions copy is identical except the first line reads `from solutions.flow import collatz_steps, count_vowels, letter_grade`.

Boundary coverage: `letter_grade` pins the 90/80/60 thresholds; `count_vowels` covers a basic case, an all-vowels-mixed-case case, and a no-vowels case; `collatz_steps` covers the base case (1→0) and three known values (2→1, 3→7, 16→4).

## Files

`lessons/03-control-flow/` (scaffold with `make new-lesson NAME=03-control-flow`, then author; replace the placeholder `main.py`/`test_main.py` with `flow.py`/`test_flow.py`):

```
lessons/03-control-flow/
├── pyproject.toml          # name "lesson-03-control-flow", package=false, pytest pythonpath=["."]
├── README.md               # authored
├── slides/
│   ├── index.html          # scaffold; <title> set to "Lesson 03 — Control flow"
│   ├── slides.md           # authored
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py         # empty (kept)
│   ├── flow.py
│   └── test_flow.py
└── solutions/
    ├── __init__.py         # empty
    ├── flow.py
    └── test_flow.py
```

## Slides (`slides/slides.md`)

About eleven slides, `---` separated, code in fenced `python` blocks, ~15 visible lines max. `Note:` speaker notes where useful.

1. **Title** — "Lesson 03 — Control flow" + one-line goal.
2. **if / elif / else** — the `letter_grade` shape.
3. **Boolean operators** — `and`, `or`, `not` to combine conditions.
4. **Early returns** — guard-clause style; return as soon as the answer is known.
5. **for loops** — `for x in iterable`; iterating a string; `range(n)`.
6. **while loops** — loop until a condition; the Collatz example; beware infinite loops.
7. **break & continue** — exit early / skip an iteration.
8. **match (teaser)** — a `match`/`case` glimpse; "a cleaner multi-way branch — more later."
9. **Comprehensions (intro)** — `[n * 2 for n in numbers]` glimpse; "full treatment in Lesson 05."
10. **Your turn** — implement the three functions; `make test-lesson LESSON=03-control-flow`.
11. **What's next** — Lesson 04 — Functions & tests.

## README (`README.md`)

Four-file-convention sections:

- **Learning goals** — branch with `if`/`elif`/`else` and boolean operators; write `for` loops over iterables (and `range`); write `while` loops safely; use `break`/`continue` and early returns; recognise `match` and comprehensions (deeper later).
- **Prereqs** — Lessons 01 and 02.
- **Concepts** — branching (`if`/`elif`/`else`, comparisons from Lesson 02, `and`/`or`/`not`, early returns / guard clauses); `for` loops (iterables, iterating a string, `range`); `while` loops (loop-until-condition, the infinite-loop trap); `break`/`continue`; a `match` teaser; a comprehension intro (pointer to Lesson 05).
- **Exercise brief** — implement `letter_grade`, `count_vowels`, and `collatz_steps` in `exercises/flow.py` so the tests pass; run the module to see all three.
- **How to run** — `make test-lesson LESSON=03-control-flow` (or `cd lessons/03-control-flow && uv run pytest exercises`); run the module `cd lessons/03-control-flow && uv run python -m exercises.flow`. Run the tests before the module (an unimplemented function raises `NotImplementedError`).
- **Going further** — `match`/`case` properly; comprehensions; `enumerate` and `zip`; the `for ... else` clause; fun fact: whether every Collatz sequence reaches 1 is an unproven conjecture.

## Verification (success criteria)

- `make test-lesson LESSON=03-control-flow` → exercise tests FAIL with `NotImplementedError`; solution tests PASS (13); target exit 0.
- `make test` → tools + Lessons 01, 02, 03 solutions all pass, in isolated per-lesson processes; no `import file mismatch`. (Now spans three lessons.)
- `cd lessons/03-control-flow && uv run python -m solutions.flow` → prints `B`, `2`, `111` (one per line).
- `make slides-build` → `dist/index.html` shows `03-control-flow` as a link (no longer faded); future-placeholder count drops from 26 to 25; `dist/lessons/03-control-flow/slides/index.html` exists.
- `make lint` and `uv run ruff format --check .` → clean. `make typecheck` stays scoped to tools and remains clean; lesson code is cleanly typed but not a typecheck gate (strict lesson typing starts at Lesson 09).
- The deck renders via `make slides-dev LESSON=03-control-flow`.

## Non-goals

- No list construction / `.append` / comprehensions as the primary tool (Lesson 05). The exercise uses only `int` and `str`.
- No graded `match` or comprehension function — slides/README teasers only.
- No formal functions material (args/`*args`/`**kwargs`, pytest internals) — that is Lesson 04.
- No catalog change — `03-control-flow` is already listed in `tools/build_index/src/build_index/catalog.py`.
- No tooling/harness changes. No strict mypy gate on lesson code (starts Lesson 09); the code is nonetheless cleanly typed.

## Open items deferred to implementation planning

- Exact slide prose and README concept wording.
- Whether the deck's `index.html` `<title>` is hand-edited to "Lesson 03 — Control flow" (default: yes, matching prior lessons' polish).
