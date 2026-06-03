# Plan F — Lesson 04 (Functions & tests)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the fourth course lesson — four calling-convention drills (`power` default/keyword args, `total` `*args`, `tally` `**kwargs`, `divmod_pair` tuple return) whose provided test file showcases `@pytest.mark.parametrize` and a `@pytest.fixture`, formally introducing pytest.

**Architecture:** Scaffold `lessons/04-functions/` with the existing `new_lesson` tool, replace the placeholder exercise with the four functions (exercise stubs raise `NotImplementedError`; solutions implemented), and author the README + slide deck. The provided `test_functions.py` is deliberately written with a fixture + parametrize so the README/slides can demystify pytest. No tooling/harness changes. Fourth lesson, so `make test` now spans four lessons.

**Tech Stack:** Python 3.13, uv workspace, pytest, ruff, mypy, GNU Make, the existing `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored).

---

## Context for the implementer

- **Repo state:** Plans A–E merged to `main`. `lessons/01-hello/`, `lessons/02-variables/`, `lessons/03-control-flow/` exist and are the pattern to mirror. `make test`/`test-lesson` run each lesson in an isolated pytest process by `cd`-ing into the lesson dir.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`). After scaffolding a lesson, run it.
- **`make new-lesson NAME=04-functions`** produces the lesson with `pyproject.toml` (name `lesson-04-functions`, `[tool.uv] package=false`, `[tool.pytest.ini_options] pythonpath=["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}` (placeholder no-arg `hello()`). The scaffolder derives the deck title from the slug ("Functions") and emits **absolute** `/shared/reveal/...` asset paths (do not change those).
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("04", "functions", "Functions & tests", …, 1)`, so `dir_name()` is `04-functions`. Once `lessons/04-functions/slides/` exists, `build_index` renders it as a link. No catalog change needed.
- **Design spec:** `docs/superpowers/specs/2026-06-03-lesson-04-functions-design.md`.
- **Mirror Lesson 03** at `lessons/03-control-flow/` for exact file shapes, README structure, and slide style.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Commit messages:** Conventional Commits. **Do NOT add a `Co-Authored-By` trailer or any AI-attribution line to commits** (project rule). Subject + body only.
- **Do NOT push** — the controller handles branch finishing.
- The module file is named `functions.py` (and tests `test_functions.py`), replacing the scaffold's `main.py`/`test_main.py`.

---

## File Structure

```
lessons/04-functions/                     (NEW — scaffolded then authored)
├── pyproject.toml                        (from scaffold; unchanged)
├── README.md                             (authored — Task 2)
├── slides/
│   ├── index.html                        (from scaffold; <title> tweaked — Task 3)
│   ├── slides.md                         (authored — Task 3)
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py                       (from scaffold; kept, empty)
│   ├── functions.py                      (authored — Task 1; replaces main.py)
│   └── test_functions.py                 (authored — Task 1; replaces test_main.py)
└── solutions/
    ├── __init__.py                       (from scaffold; kept, empty)
    ├── functions.py                      (authored — Task 1)
    └── test_functions.py                 (authored — Task 1)
```

---

## Task 1: Scaffold lesson 04 and author the exercise + solution

**Files:**
- Create (via scaffold): `lessons/04-functions/` tree
- Create: `lessons/04-functions/exercises/functions.py`, `.../exercises/test_functions.py`
- Create: `lessons/04-functions/solutions/functions.py`, `.../solutions/test_functions.py`
- Delete (scaffold placeholders): `lessons/04-functions/{exercises,solutions}/main.py` and `.../test_main.py`

- [ ] **Step 1: Scaffold the lesson**

Run: `make new-lesson NAME=04-functions`
Expected: prints `created lessons/04-functions`; the tree exists.

Run: `uv sync --all-packages`
Expected: registers `lesson-04-functions`; exits 0.

- [ ] **Step 2: Remove the placeholder files**

```bash
rm lessons/04-functions/exercises/main.py lessons/04-functions/exercises/test_main.py
rm lessons/04-functions/solutions/main.py lessons/04-functions/solutions/test_main.py
```

(Keep both `__init__.py` files and `slides/assets/.gitkeep`.)

- [ ] **Step 3: Write the solution tests (TDD red)**

Create `lessons/04-functions/solutions/test_functions.py`:

```python
import pytest

from solutions.functions import divmod_pair, power, tally, total


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

- [ ] **Step 4: Run the solution tests — verify RED**

Run: `( cd lessons/04-functions && uv run pytest solutions )`
Expected: collection error / `ModuleNotFoundError: No module named 'solutions.functions'` (functions.py doesn't exist yet).

- [ ] **Step 5: Write the solution (TDD green)**

Create `lessons/04-functions/solutions/functions.py`:

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

- [ ] **Step 6: Run the solution tests — verify GREEN**

Run: `( cd lessons/04-functions && uv run pytest solutions )`
Expected: 13 passed (the parametrized `test_power` expands to 4 items).

- [ ] **Step 7: Write the exercise stub + its (fail-by-design) test**

Create `lessons/04-functions/exercises/functions.py`:

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

Create `lessons/04-functions/exercises/test_functions.py` (identical to the solutions test except the import line):

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

- [ ] **Step 8: Verify the exercise tests fail as designed**

Run: `( cd lessons/04-functions && uv run pytest exercises )`
Expected: 13 failed with `NotImplementedError`. (Intended deliverable — the failing tests are the student's spec.)

- [ ] **Step 9: Verify the make targets**

Run: `make test-lesson LESSON=04-functions`
Expected: exercises section FAILS (NotImplementedError, tolerated by the leading `-`); solutions section PASSES (13); overall exit 0.

Run: `make test`
Expected: tool suite passes, then `== lessons/01-hello/solutions ==` (2), `== lessons/02-variables/solutions ==` (10), `== lessons/03-control-flow/solutions ==` (15), AND `== lessons/04-functions/solutions ==` (13) all pass; exit 0; no `import file mismatch`.

- [ ] **Step 10: Verify the parametrized cases show individually, and the module runs**

Run: `( cd lessons/04-functions && uv run pytest solutions -v )`
Expected: output lists `test_power[3.0-2.0-9.0]`, `test_power[2.0-3.0-8.0]`, `test_power[5.0-0.0-1.0]`, `test_power[2.0-10.0-1024.0]` as separate items (confirming parametrize works).

Run: `( cd lessons/04-functions && uv run python -m solutions.functions )`
Expected: prints four lines: `25.0`, `6.0`, `5`, `(3, 2)`.

Run: `( cd lessons/04-functions && uv run python -m exercises.functions )`
Expected: raises `NotImplementedError` (exercise not implemented — correct).

- [ ] **Step 11: Lint, format, type-check**

Run: `make lint`
Expected: All checks passed!

Run: `uv run ruff format --check .`
Expected: all files formatted (no diff). If it reports the new files would be reformatted, run `uv run ruff format lessons/04-functions` and re-check; note it.

Run: `uv run mypy lessons/04-functions/solutions/functions.py lessons/04-functions/exercises/functions.py`
Expected: Success. (If mypy raises a note about `sum(numbers)`'s return type, report it — lesson code is not a CI gate, but capture the exact message; do NOT add `# type: ignore` without reporting first.)

- [ ] **Step 12: Commit**

```bash
git add lessons/04-functions uv.lock
git commit -m "feat(lesson-04): add functions exercise + pytest-showcase tests"
```

(No `Co-Authored-By` trailer. After committing, `git log -1 --format='%B'` should contain no co-author/attribution line.)

---

## Task 2: Author the lesson README

**Files:**
- Modify: `lessons/04-functions/README.md` (replace the scaffold's TODO placeholders)

- [ ] **Step 1: Overwrite `lessons/04-functions/README.md`**

````markdown
# Lesson 04 — Functions & tests

Define functions that take positional, keyword, default, and variadic
arguments — and finally see how `pytest`, the "magic test runner" from the
first three lessons, actually works.

## Learning goals

- Pass arguments positionally and by keyword, and give parameters defaults
- Gather extra arguments with `*args` (a tuple) and `**kwargs` (a dict)
- Return multiple values as a tuple, and unpack them
- Understand how `pytest` discovers and runs tests
- Read `assert`, `@pytest.mark.parametrize`, and `@pytest.fixture`

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md),
  [Lesson 02 — Variables, types, operators](../02-variables/README.md), and
  [Lesson 03 — Control flow](../03-control-flow/README.md).

## Concepts

**Arguments.** A call passes arguments to a function's parameters. You can pass
them by position (`power(2, 3)`) or by keyword (`power(2, exp=3)`). A parameter
with a default may be omitted: `def power(base, exp=2.0)` lets `power(5)` mean
"square it". (Defaults are evaluated once, when the function is defined — so
never use a mutable default like `[]`.)

**`*args` and `**kwargs`.** A `*args` parameter collects any extra positional
arguments into a **tuple**: `def total(*numbers)` makes `total(1, 2, 3)` see
`numbers == (1, 2, 3)`. A `**kwargs` parameter collects any extra keyword
arguments into a **dict**: `def tally(**counts)` makes `tally(apples=3)` see
`counts == {"apples": 3}`.

**Returning tuples.** A function can return several values as a tuple just by
separating them with commas: `return a // b, a % b`. The caller can unpack
them: `q, r = divmod_pair(17, 5)`.

**How `pytest` works.** When you run `pytest`, it discovers files named
`test_*.py` and functions named `test_*`, runs each one, and reports the
results. An `assert` that fails stops that test and prints both sides of the
comparison, so you see exactly what went wrong.

**`parametrize`.** `@pytest.mark.parametrize("a, b, expected", [...])` runs the
same test body once per row of inputs — many cases, one function. Run pytest
with `-v` to see each case listed separately.

**`fixtures`.** A function decorated with `@pytest.fixture` provides reusable
setup or data. A test that names the fixture in its parameters receives its
return value. This lesson's tests use a `sample_numbers` fixture.

Open `exercises/test_functions.py` — it uses a fixture and a parametrized test.
That is the machinery that has been checking your work since Lesson 01.

## Exercise brief

Open `exercises/functions.py` and implement four functions so the tests pass:

- `power(base, exp=2.0)` — `base` raised to `exp`; `exp` defaults to 2.
- `total(*numbers)` — the sum of all the numbers (`0.0` if none).
- `tally(**counts)` — the sum of all the keyword values (`0` if none).
- `divmod_pair(a, b)` — the tuple `(a // b, a % b)`.

Run the tests first to watch them fail, then make them pass.

## How to run

Run the tests (exercises fail until you implement the functions; solutions pass):

```bash
make test-lesson LESSON=04-functions
```

Or directly, with `-v` to see each parametrized case:

```bash
cd lessons/04-functions && uv run pytest exercises -v
```

Run the module (prints a demo of all four; implement the functions first, or
it raises `NotImplementedError`):

```bash
cd lessons/04-functions && uv run python -m exercises.functions
```

## Going further

- Keyword-only parameters: `def f(*, key)`. Positional-only: `def f(x, /)`.
- The built-in `divmod(a, b)` returns the same tuple as `divmod_pair`.
- The mutable-default gotcha: `def f(items=[])` reuses one list across calls —
  use `def f(items=None)` and create a new list inside instead.
- pytest flags: `-k name` selects tests by name, `-x` stops on the first
  failure, `-q` is quiet.
````

- [ ] **Step 2: Verify**

Run: `grep -c '```' lessons/04-functions/README.md` → expect an EVEN number.
Run: `grep -q "Lesson 04 — Functions & tests" lessons/04-functions/README.md && grep -q "make test-lesson LESSON=04-functions" lessons/04-functions/README.md && grep -q "Run the tests first to watch them fail" lessons/04-functions/README.md && echo "readme ok"` → expect `readme ok`.
Run: `grep -iE 'TODO' lessons/04-functions/README.md && echo "HAS TODO" || echo "no todos"` → expect `no todos`.

- [ ] **Step 3: Commit**

```bash
git add lessons/04-functions/README.md
git commit -m "docs(lesson-04): author the README (args, *args/**kwargs, tuples, pytest)"
```

(No `Co-Authored-By` trailer.)

---

## Task 3: Author the slide deck

**Files:**
- Modify: `lessons/04-functions/slides/slides.md` (replace the template deck)
- Modify: `lessons/04-functions/slides/index.html` (deck `<title>` only)

- [ ] **Step 1: Overwrite `lessons/04-functions/slides/slides.md`**

````markdown
## Lesson 04
### Functions & tests

Arguments, defaults, *args/**kwargs, tuples — and how pytest works.

Note:
Two threads: function calling conventions, then pytest demystified.

---

## Defining functions

```python
def power(base: float, exp: float) -> float:
    return base ** exp
```

- We've written functions since Lesson 01
- `def name(params) -> return_type:`

---

## Positional & keyword args

```python
power(2.0, 3.0)        # positional
power(2.0, exp=3.0)    # keyword
```

- Position order matters; keywords name the parameter
- Keywords can make a call clearer

---

## Default arguments

```python
def power(base: float, exp: float = 2.0) -> float:
    return base ** exp

power(5.0)   # 25.0  — exp defaults to 2
```

- Omit an argument to use its default
- Defaults are evaluated once — never use a mutable default

---

## *args

```python
def total(*numbers: float) -> float:
    return sum(numbers)

total(1.0, 2.0, 3.0)   # 6.0
```

- `*args` collects extra positional args into a **tuple**

---

## **kwargs

```python
def tally(**counts: int) -> int:
    return sum(counts.values())

tally(apples=3, pears=2)   # 5
```

- `**kwargs` collects extra keyword args into a **dict**

---

## Returning tuples

```python
def divmod_pair(a: int, b: int) -> tuple[int, int]:
    return a // b, a % b

q, r = divmod_pair(17, 5)   # q=3, r=2
```

- Commas build a tuple; the caller can unpack it

---

## The magic, explained

```bash
uv run pytest
```

- pytest finds `test_*.py` files and `test_*` functions
- runs each and reports pass/fail

---

## assert

```python
def test_power_squares() -> None:
    assert power(5.0) == 25.0
```

- A failing `assert` prints both sides — you see what went wrong

---

## parametrize

```python
@pytest.mark.parametrize("base, exp, expected", [
    (3.0, 2.0, 9.0),
    (2.0, 3.0, 8.0),
])
def test_power(base, exp, expected) -> None:
    assert power(base, exp) == expected
```

- One test body, many cases (`pytest -v` lists each)

---

## fixtures

```python
@pytest.fixture
def sample_numbers() -> tuple[float, ...]:
    return (1.0, 2.0, 3.0, 4.0)

def test_total(sample_numbers) -> None:
    assert total(*sample_numbers) == 10.0
```

- A fixture supplies reusable setup/data to tests that name it

---

## Your turn

- Implement the four functions in `exercises/functions.py`
- `make test-lesson LESSON=04-functions` until green
- Read `test_functions.py` — that's pytest, no longer magic

---

## What's next

**Lesson 05 — Collections.**
````

- [ ] **Step 2: Fix the deck `<title>` in index.html**

In `lessons/04-functions/slides/index.html`, find the `<title>` line (the scaffolder set it from the slug, e.g. `<title>Lesson 04 — Functions</title>`) and change it to:

```html
  <title>Lesson 04 — Functions & tests</title>
```

(Only the `<title>` text changes. Do NOT change the `/shared/reveal/...` asset paths — they are correct.)

- [ ] **Step 3: Build the site; confirm the lesson is a LINK and uses absolute asset paths**

Run: `make slides-build`
Expected: prints `built dist`.

Run:
```bash
grep -q 'href="lessons/04-functions/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
grep -oE '/shared/reveal|\.\./\.\./shared/reveal' dist/lessons/04-functions/slides/index.html | sort | uniq -c
test -f dist/lessons/04-functions/slides/index.html && test -f dist/lessons/04-functions/slides/slides.md && echo "SLIDES_COPIED"
```
Expected: `LINK_OK`; future-placeholder count is now `24`; the asset-path grep shows only `/shared/reveal` occurrences (NO `../../shared/reveal`); `SLIDES_COPIED`.

Run: `rm -rf dist`

- [ ] **Step 4: Dev-server smoke test**

```bash
( uv run python -m slides_dev --lesson 04-functions --repo-root "$(pwd)" --port 8000 & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
kill "$(lsof -ti:8000)" 2>/dev/null || true
```
Expected: title line `<title>Lesson 04 — Functions & tests</title>`, `slidesmd=200`, `revealcss=200`. Confirm `lsof -ti:8000` is empty afterward.

- [ ] **Step 5: Commit**

```bash
git add lessons/04-functions/slides/slides.md lessons/04-functions/slides/index.html
git commit -m "feat(lesson-04): author the slide deck"
```

(No `Co-Authored-By` trailer.)

---

## Task 4: Final verification

End-to-end check. No new code unless something needs tidying.

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current`
Expected: `lesson-04-functions`. If not, STOP and report.

- [ ] **Step 2: Full quality bar**

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
- `make test` → tool suite passes, Lessons 01 (2), 02 (10), 03 (15), 04 (13) solutions all pass; exit 0; no `import file mismatch`.

- [ ] **Step 3: Lesson red/green + parametrize + module**

```bash
make test-lesson LESSON=04-functions
( cd lessons/04-functions && uv run pytest solutions -v )
( cd lessons/04-functions && uv run python -m solutions.functions )
```
Expected: exercises FAIL (NotImplementedError, tolerated), solutions PASS (13), exit 0; `-v` shows four `test_power[...]` items; module prints `25.0`, `6.0`, `5`, `(3, 2)`.

- [ ] **Step 4: Landing page link + git hygiene + no co-author trailers**

```bash
make slides-build
grep -q 'href="lessons/04-functions/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
rm -rf dist
git status --porcelain
git ls-files lessons/04-functions | sort
git log --oneline main..HEAD
git log main..HEAD --format='%B' | grep -i 'co-authored\|generated with' && echo "TRAILER FOUND (bad)" || echo "no trailers — good"
```
Expected: `LINK_OK`; future count `24`; clean working tree (no `dist/`); `lessons/04-functions` has pyproject.toml, README.md, slides/{index.html,slides.md,assets/.gitkeep}, exercises/{__init__.py,functions.py,test_functions.py}, solutions/{__init__.py,functions.py,test_functions.py} — NO main.py/test_main.py; 3 commits; `no trailers — good`.

- [ ] **Step 5: Confirm port clear**

```bash
lsof -ti:8000 || echo "port clear"
```
Expected: `port clear`.

- [ ] **Step 6: Commit only if Steps 1-5 surfaced changes**

If `git status` is clean, report CLEAN. If anything changed, investigate and commit (no co-author trailer); if a check FAILED, STOP and report BLOCKED.

---

## Notes for execution

- No tooling/harness changes, no `gcloud`, no secrets, no push. The deploy pipeline picks the lesson up automatically on the next merge to `main`.
- The scaffolded deck already uses absolute `/shared/reveal/...` paths; do not reintroduce relative paths.
- This lesson's `test_functions.py` is a teaching artifact (fixture + parametrize) — keep both features in it; they are referenced by the README and slides.
- Commits must NOT include `Co-Authored-By` or AI-attribution trailers (project rule).
