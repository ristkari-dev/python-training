# Plan E — Lesson 03 (Control flow)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the third course lesson — three single-construct control-flow drills (`letter_grade` = if/elif/else, `count_vowels` = for-loop, `collatz_steps` = while-loop) with `match`/comprehensions as slides-only teasers.

**Architecture:** Scaffold `lessons/03-control-flow/` with the existing `new_lesson` tool, replace the placeholder exercise with the three functions (exercise stubs raise `NotImplementedError`; solutions implemented), author the README and slide deck. No tooling/harness changes. Third lesson, so `make test` now spans three lessons.

**Tech Stack:** Python 3.13, uv workspace, pytest, ruff, mypy, GNU Make, the existing `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored).

---

## Context for the implementer

- **Repo state:** Plans A–D merged to `main`, plus the deck-asset-path fix (PR #5). `lessons/01-hello/` and `lessons/02-variables/` exist and are the pattern to mirror. `make test`/`test-lesson` run each lesson in an isolated pytest process by `cd`-ing into the lesson dir.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`). After scaffolding a lesson, run it.
- **`make new-lesson NAME=03-control-flow`** produces the lesson with `pyproject.toml` (name `lesson-03-control-flow`, `[tool.uv] package=false`, `[tool.pytest.ini_options] pythonpath=["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}` (placeholder no-arg `hello()`). The scaffolder derives the deck title from the slug ("Control Flow") and now emits **absolute** `/shared/reveal/...` asset paths (fixed in PR #5) — so the scaffolded deck renders correctly when deployed; do not reintroduce relative `../../shared/reveal` paths.
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("03", "control-flow", "Control flow", …, 1)`, so `dir_name()` is `03-control-flow`. Once `lessons/03-control-flow/slides/` exists, `build_index` renders it as a link. No catalog change needed.
- **Design spec:** `docs/superpowers/specs/2026-06-01-lesson-03-control-flow-design.md`.
- **Mirror Lesson 02** at `lessons/02-variables/` for exact file shapes, README structure, and slide style.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Commit messages:** Conventional Commits. **Do NOT add a `Co-Authored-By` trailer or any AI-attribution line to commits** (project rule). Subject + body only.
- **Do NOT push** — the controller handles branch finishing.
- The module file is named `flow.py` (and tests `test_flow.py`), replacing the scaffold's `main.py`/`test_main.py`.

---

## File Structure

```
lessons/03-control-flow/                  (NEW — scaffolded then authored)
├── pyproject.toml                        (from scaffold; unchanged)
├── README.md                             (authored — Task 2)
├── slides/
│   ├── index.html                        (from scaffold; <title> tweaked — Task 3)
│   ├── slides.md                         (authored — Task 3)
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py                       (from scaffold; kept, empty)
│   ├── flow.py                           (authored — Task 1; replaces main.py)
│   └── test_flow.py                      (authored — Task 1; replaces test_main.py)
└── solutions/
    ├── __init__.py                       (from scaffold; kept, empty)
    ├── flow.py                           (authored — Task 1)
    └── test_flow.py                      (authored — Task 1)
```

---

## Task 1: Scaffold lesson 03 and author the exercise + solution

**Files:**
- Create (via scaffold): `lessons/03-control-flow/` tree
- Create: `lessons/03-control-flow/exercises/flow.py`, `.../exercises/test_flow.py`
- Create: `lessons/03-control-flow/solutions/flow.py`, `.../solutions/test_flow.py`
- Delete (scaffold placeholders): `lessons/03-control-flow/{exercises,solutions}/main.py` and `.../test_main.py`

- [ ] **Step 1: Scaffold the lesson**

Run: `make new-lesson NAME=03-control-flow`
Expected: prints `created lessons/03-control-flow`; the tree exists.

Run: `uv sync --all-packages`
Expected: registers `lesson-03-control-flow`; exits 0.

- [ ] **Step 2: Remove the placeholder files**

```bash
rm lessons/03-control-flow/exercises/main.py lessons/03-control-flow/exercises/test_main.py
rm lessons/03-control-flow/solutions/main.py lessons/03-control-flow/solutions/test_main.py
```

(Keep both `__init__.py` files and `slides/assets/.gitkeep`.)

- [ ] **Step 3: Write the solution tests (TDD red)**

Create `lessons/03-control-flow/solutions/test_flow.py`:

```python
from solutions.flow import collatz_steps, count_vowels, letter_grade


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

- [ ] **Step 4: Run the solution tests — verify RED**

Run: `( cd lessons/03-control-flow && uv run pytest solutions )`
Expected: collection error / `ModuleNotFoundError: No module named 'solutions.flow'` (flow.py doesn't exist yet).

- [ ] **Step 5: Write the solution (TDD green)**

Create `lessons/03-control-flow/solutions/flow.py`:

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

- [ ] **Step 6: Run the solution tests — verify GREEN**

Run: `( cd lessons/03-control-flow && uv run pytest solutions )`
Expected: 13 passed.

- [ ] **Step 7: Write the exercise stub + its (fail-by-design) test**

Create `lessons/03-control-flow/exercises/flow.py`:

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

Create `lessons/03-control-flow/exercises/test_flow.py` (identical to the solutions test except the import line):

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

- [ ] **Step 8: Verify the exercise tests fail as designed**

Run: `( cd lessons/03-control-flow && uv run pytest exercises )`
Expected: 13 failed with `NotImplementedError`. (Intended deliverable — the failing tests are the student's spec.)

- [ ] **Step 9: Verify the make targets**

Run: `make test-lesson LESSON=03-control-flow`
Expected: exercises section FAILS (NotImplementedError, tolerated by the leading `-`); solutions section PASSES (13); overall exit 0.

Run: `make test`
Expected: tool suite passes, then `== lessons/01-hello/solutions ==` (2), `== lessons/02-variables/solutions ==` (10), AND `== lessons/03-control-flow/solutions ==` (13) all pass; exit 0; no `import file mismatch`.

- [ ] **Step 10: Verify the runnable module (solution)**

Run: `( cd lessons/03-control-flow && uv run python -m solutions.flow )`
Expected: prints three lines: `B`, `2`, `111`.

Run: `( cd lessons/03-control-flow && uv run python -m exercises.flow )`
Expected: raises `NotImplementedError` (exercise not implemented — correct).

- [ ] **Step 11: Lint, format, type-check**

Run: `make lint`
Expected: All checks passed!

Run: `uv run ruff format --check .`
Expected: all files formatted (no diff). If it reports the new files would be reformatted, run `uv run ruff format lessons/03-control-flow` and re-check; note it.

Run: `uv run mypy lessons/03-control-flow/solutions/flow.py lessons/03-control-flow/exercises/flow.py`
Expected: Success.

- [ ] **Step 12: Commit**

```bash
git add lessons/03-control-flow uv.lock
git commit -m "feat(lesson-03): add control-flow drills (letter_grade, count_vowels, collatz_steps)"
```

(No `Co-Authored-By` trailer. After committing, `git log -1 --format='%B'` should contain no co-author/attribution line.)

---

## Task 2: Author the lesson README

**Files:**
- Modify: `lessons/03-control-flow/README.md` (replace the scaffold's TODO placeholders)

- [ ] **Step 1: Overwrite `lessons/03-control-flow/README.md`**

````markdown
# Lesson 03 — Control flow

Make decisions with `if`/`elif`/`else` and repeat work with `for` and `while`
loops. By the end you will have written a grader, a vowel counter, and a
step-counter for the famous Collatz sequence.

## Learning goals

- Branch with `if`/`elif`/`else` and boolean operators (`and`, `or`, `not`)
- Write `for` loops over iterables (and `range`)
- Write `while` loops without creating an infinite loop
- Use `break`, `continue`, and early returns
- Recognise `match` and comprehensions (covered fully later)

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md) and
  [Lesson 02 — Variables, types, operators](../02-variables/README.md).

## Concepts

**Branching.** `if` runs a block when a condition is true; `elif` and `else`
handle the other cases. Conditions are the comparisons from Lesson 02
(`>=`, `==`, …), and you can combine them with `and`, `or`, and `not`.

**Early returns.** A function can `return` as soon as it knows the answer.
A chain of `if ...: return ...` is often clearer than deep nesting.

**`for` loops.** `for item in iterable:` runs the body once per item. Strings
are iterable (you get one character at a time), and `range(n)` gives the
numbers `0 .. n-1`. The `in` operator also tests membership: `"a" in "cat"`.

**`while` loops.** `while condition:` repeats until the condition becomes
false. Make sure something inside the loop changes toward the exit, or it
runs forever.

**`break` and `continue`.** `break` leaves the loop immediately; `continue`
skips to the next iteration.

**`match` (teaser).** Python's `match`/`case` is a cleaner multi-way branch.
We only glimpse it here.

**Comprehensions (intro).** `[n * 2 for n in numbers]` builds a list in one
line. Full treatment in Lesson 05.

## Exercise brief

Open `exercises/flow.py` and implement three functions so the tests pass:

- `letter_grade(score)` — `A` for `>= 90`, `B` for `>= 80`, `C` for `>= 70`,
  `D` for `>= 60`, otherwise `F` (use `if`/`elif`/`else`).
- `count_vowels(text)` — count the vowels in `text`, any case (use a `for`
  loop).
- `collatz_steps(n)` — count steps to reach 1: if `n` is even, `n // 2`,
  else `3 * n + 1`; `n == 1` takes 0 steps (use a `while` loop).

Run the tests first to watch them fail, then make them pass.

## How to run

Run the tests (exercises fail until you implement the functions; solutions pass):

```bash
make test-lesson LESSON=03-control-flow
```

Or directly:

```bash
cd lessons/03-control-flow && uv run pytest exercises
```

Run the module (prints a demo of all three; implement the functions first, or
it raises `NotImplementedError`):

```bash
cd lessons/03-control-flow && uv run python -m exercises.flow
```

## Going further

- `match`/`case`: rewrite a multi-way branch with structural pattern matching.
- Comprehensions: `[n for n in range(10) if n % 2 == 0]`.
- `enumerate(items)` gives `(index, item)` pairs; `zip(a, b)` pairs two
  iterables.
- The `for ... else` clause runs the `else` block if the loop finished without
  a `break`.
- Fun fact: whether *every* starting number's Collatz sequence reaches 1 is an
  unproven mathematical conjecture.
````

- [ ] **Step 2: Verify**

Run: `grep -c '```' lessons/03-control-flow/README.md` → expect an EVEN number.
Run: `grep -q "Lesson 03 — Control flow" lessons/03-control-flow/README.md && grep -q "make test-lesson LESSON=03-control-flow" lessons/03-control-flow/README.md && grep -q "Run the tests first to watch them fail" lessons/03-control-flow/README.md && echo "readme ok"` → expect `readme ok`.
Run: `grep -iE 'TODO' lessons/03-control-flow/README.md && echo "HAS TODO" || echo "no todos"` → expect `no todos`.

- [ ] **Step 3: Commit**

```bash
git add lessons/03-control-flow/README.md
git commit -m "docs(lesson-03): author the README (branching, loops, early returns)"
```

(No `Co-Authored-By` trailer.)

---

## Task 3: Author the slide deck

**Files:**
- Modify: `lessons/03-control-flow/slides/slides.md` (replace the template deck)
- Modify: `lessons/03-control-flow/slides/index.html` (deck `<title>` only)

- [ ] **Step 1: Overwrite `lessons/03-control-flow/slides/slides.md`**

````markdown
## Lesson 03
### Control flow

Make decisions, repeat work, know when to stop.

Note:
Three drills: a grader (if/elif/else), a vowel counter (for), a Collatz
step-counter (while).

---

## if / elif / else

```python
if score >= 90:
    return "A"
elif score >= 80:
    return "B"
else:
    return "F"
```

- `if` runs when the condition is true
- `elif` / `else` handle the rest

---

## Boolean operators

```python
if score >= 60 and not late:
    return "pass"
```

- `and`, `or`, `not` combine conditions
- Comparisons (`>=`, `==`, …) produce a `bool`

---

## Early returns

```python
def grade(score: int) -> str:
    if score < 60:
        return "F"
    return "pass"
```

- Return as soon as the answer is known
- Often clearer than deep nesting

---

## for loops

```python
for char in "hello":
    print(char)

for i in range(3):   # 0, 1, 2
    print(i)
```

- `for x in iterable:` runs once per item
- strings are iterable; `range(n)` gives `0..n-1`

---

## while loops

```python
steps = 0
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    steps += 1
```

- Repeats until the condition is false
- Something must move toward the exit — or it runs forever

---

## break & continue

```python
for n in range(10):
    if n == 5:
        break      # leave the loop
    if n % 2 == 0:
        continue   # skip to next
    print(n)
```

---

## match (teaser)

```python
match command:
    case "go":
        ...
    case _:
        ...
```

A cleaner multi-way branch — more later.

---

## Comprehensions (intro)

```python
doubled = [n * 2 for n in numbers]
```

Build a list in one line — full treatment in Lesson 05.

---

## Your turn

- Implement the three functions in `exercises/flow.py`
- `make test-lesson LESSON=03-control-flow` until green
- Run it: `uv run python -m exercises.flow`

---

## What's next

**Lesson 04 — Functions & tests.**
````

- [ ] **Step 2: Fix the deck `<title>` in index.html**

In `lessons/03-control-flow/slides/index.html`, find the `<title>` line (the scaffolder set it from the slug, e.g. `<title>Lesson 03 — Control Flow</title>`) and change it to:

```html
  <title>Lesson 03 — Control flow</title>
```

(Only the `<title>` text changes. Note lowercase "flow" to match the course naming. Do NOT change the `/shared/reveal/...` asset paths — they are correct.)

- [ ] **Step 3: Build the site; confirm the lesson is a LINK and uses absolute asset paths**

Run: `make slides-build`
Expected: prints `built dist`.

Run:
```bash
grep -q 'href="lessons/03-control-flow/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
grep -oE '/shared/reveal|\.\./\.\./shared/reveal' dist/lessons/03-control-flow/slides/index.html | sort | uniq -c
test -f dist/lessons/03-control-flow/slides/index.html && test -f dist/lessons/03-control-flow/slides/slides.md && echo "SLIDES_COPIED"
```
Expected: `LINK_OK`; future-placeholder count is now `25`; the asset-path grep shows only `/shared/reveal` occurrences (NO `../../shared/reveal`); `SLIDES_COPIED`.

Run: `rm -rf dist`

- [ ] **Step 4: Dev-server smoke test**

```bash
( uv run python -m slides_dev --lesson 03-control-flow --repo-root "$(pwd)" --port 8000 & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
kill "$(lsof -ti:8000)" 2>/dev/null || true
```
Expected: title line `<title>Lesson 03 — Control flow</title>`, `slidesmd=200`, `revealcss=200`. Confirm `lsof -ti:8000` is empty afterward.

- [ ] **Step 5: Commit**

```bash
git add lessons/03-control-flow/slides/slides.md lessons/03-control-flow/slides/index.html
git commit -m "feat(lesson-03): author the slide deck"
```

(No `Co-Authored-By` trailer.)

---

## Task 4: Final verification

End-to-end check. No new code unless something needs tidying.

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current`
Expected: `lesson-03-control-flow`. If not, STOP and report.

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
- `make test` → tool suite passes, Lessons 01 (2), 02 (10), 03 (13) solutions all pass; exit 0; no `import file mismatch`.

- [ ] **Step 3: Lesson red/green + module**

```bash
make test-lesson LESSON=03-control-flow
( cd lessons/03-control-flow && uv run python -m solutions.flow )
```
Expected: exercises FAIL (NotImplementedError, tolerated), solutions PASS (13), exit 0; module prints `B`, `2`, `111`.

- [ ] **Step 4: Landing page link + git hygiene + no co-author trailers**

```bash
make slides-build
grep -q 'href="lessons/03-control-flow/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
rm -rf dist
git status --porcelain
git ls-files lessons/03-control-flow | sort
git log --oneline main..HEAD
git log main..HEAD --format='%B' | grep -i 'co-authored\|generated with' && echo "TRAILER FOUND (bad)" || echo "no trailers — good"
```
Expected: `LINK_OK`; future count `25`; clean working tree (no `dist/`); `lessons/03-control-flow` has pyproject.toml, README.md, slides/{index.html,slides.md,assets/.gitkeep}, exercises/{__init__.py,flow.py,test_flow.py}, solutions/{__init__.py,flow.py,test_flow.py} — NO main.py/test_main.py; 3 commits; `no trailers — good`.

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
- The scaffolded deck already uses absolute `/shared/reveal/...` paths (PR #5 fix); do not reintroduce relative paths.
- Commits must NOT include `Co-Authored-By` or AI-attribution trailers (project rule).
