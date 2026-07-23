# Plan I — Lesson 07 (Modules, packages, imports)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the seventh course lesson — a small `geom` package (`points.py`, `metrics.py`, `__init__.py`) where one module imports another and imports the stdlib `math`, and the learner wires up the `__init__.py` re-exports (red-start) plus two functions.

**Architecture:** Scaffold `lessons/07-modules/` with `new_lesson`, replace the placeholder module with a `geom` sub-package under both `exercises/` and `solutions/`. Absolute imports only (`exercises.geom.` / `solutions.geom.` prefix) — the repo's ruff bans relative imports (TID252), so no ruff change is needed and none is made. Author README + deck. Seventh lesson, so `make test` now spans seven lessons.

**Tech Stack:** Python 3.13, uv workspace, pytest, ruff, mypy, GNU Make, `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored).

---

## Context for the implementer

- **Repo state:** Plans A–H merged (Lesson 06 must be on `main` before this runs — the controller waits for the Lesson 06 PR to merge, then branches off the updated `main`). Lessons `01-hello` … `06-classes` are the pattern; mirror `lessons/06-classes/` for file shapes and deck style.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`). Run it after scaffolding.
- **`make new-lesson NAME=07-modules`** produces `pyproject.toml` (name `lesson-07-modules`, `package=false`, pytest `pythonpath=["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}`. The scaffolder derives the deck title from the slug ("Modules") and emits **absolute** `/shared/reveal/...` asset paths (do not change those).
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("07", "modules", "Modules, packages, imports", …, 1)`. Once `lessons/07-modules/slides/` exists, `build_index` renders it as a link. No catalog change.
- **Package naming:** the lesson package is `geom` (sub-package of `exercises`/`solutions`); module files `points.py`, `metrics.py`; test file `test_geom.py` sits at the lesson's `exercises/` / `solutions/` top level (sibling of `geom/`).
- **Absolute imports only:** internal imports use the full `exercises.geom.` / `solutions.geom.` prefix. Consequence: the exercise and solution copies of `metrics.py` and `geom/__init__.py` differ by that prefix — NOT only the test import line. This is intended.
- **Design spec:** `docs/superpowers/specs/2026-07-08-lesson-07-modules-design.md`.
- **Typing gate:** `make typecheck` is scoped to `tools/` only; lesson code is not a mypy gate yet (starts Lesson 09). Lesson code must be `ruff`-clean.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Branch:** all work on `lesson-07-modules` (created from up-to-date `main` that already contains Lesson 06). Every task's first step confirms the branch.
- **Commit messages:** Conventional Commits. **Do NOT add a `Co-Authored-By` trailer or any AI-attribution line.** Subject (+ optional body) only.
- **Do NOT push** — the controller finishes the branch.
- The package modules replace the scaffold's `main.py`/`test_main.py`.

---

## File Structure

```
lessons/07-modules/                          (NEW — scaffolded then authored)
├── pyproject.toml                           (from scaffold; unchanged)
├── README.md                                (authored — Task 2)
├── slides/
│   ├── index.html                           (from scaffold; <title> fixed — Task 3)
│   ├── slides.md                            (authored — Task 3)
│   └── assets/.gitkeep                       (from scaffold)
├── exercises/
│   ├── __init__.py                          (from scaffold; empty)
│   ├── geom/
│   │   ├── __init__.py                      (authored — red-start comment only)
│   │   ├── points.py                        (authored — Point given, midpoint stub)
│   │   └── metrics.py                       (authored — imports given, distance stub)
│   └── test_geom.py                         (authored — replaces test_main.py)
└── solutions/
    ├── __init__.py                          (from scaffold; empty)
    ├── geom/
    │   ├── __init__.py                      (authored — re-exports)
    │   ├── points.py                        (authored)
    │   └── metrics.py                       (authored)
    └── test_geom.py                         (authored)
```

No catalog / Makefile / ruff changes.

---

## Task 1: Scaffold lesson 07 and author the `geom` package + tests

**Files:** as in the tree above (create the `geom` sub-packages and test files; delete `main.py`/`test_main.py`).

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current` → `lesson-07-modules`. If not, STOP and report.
Also run `git cat-file -e main:lessons/06-classes/solutions/shapes.py 2>/dev/null && echo "L06 present" || echo "L06 MISSING"` — expected `L06 present` (this branch must be based on a `main` that already has Lesson 06). If MISSING, STOP and report.

- [ ] **Step 2: Scaffold**

```bash
make new-lesson NAME=07-modules
make sync
```
Expected: `created lessons/07-modules`; `make sync` installs `lesson-07-modules`.

- [ ] **Step 3: Remove placeholder module/test files**

```bash
git rm -f lessons/07-modules/exercises/main.py lessons/07-modules/exercises/test_main.py \
          lessons/07-modules/solutions/main.py lessons/07-modules/solutions/test_main.py
```
(If untracked, use plain `rm`.) Keep the `exercises/__init__.py` and `solutions/__init__.py`.

- [ ] **Step 4: Create the solution package `solutions/geom/`**

Create `lessons/07-modules/solutions/geom/points.py`:
```python
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


def midpoint(a: Point, b: Point) -> Point:
    """Return the point halfway between a and b."""
    return Point((a.x + b.x) / 2, (a.y + b.y) / 2)
```

Create `lessons/07-modules/solutions/geom/metrics.py`:
```python
import math

from solutions.geom.points import Point


def distance(a: Point, b: Point) -> float:
    """Return the straight-line distance between a and b."""
    return math.hypot(a.x - b.x, a.y - b.y)
```

Create `lessons/07-modules/solutions/geom/__init__.py`:
```python
"""The geom package: points and the distance between them."""

from solutions.geom.metrics import distance
from solutions.geom.points import Point, midpoint

__all__ = ["Point", "distance", "midpoint"]
```

- [ ] **Step 5: Create the exercise package `exercises/geom/` (red-start)**

Create `lessons/07-modules/exercises/geom/points.py`:
```python
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


def midpoint(a: Point, b: Point) -> Point:
    """Return the point halfway between a and b."""
    raise NotImplementedError("implement midpoint() so the tests pass")
```

Create `lessons/07-modules/exercises/geom/metrics.py`:
```python
import math

from exercises.geom.points import Point


def distance(a: Point, b: Point) -> float:
    """Return the straight-line distance between a and b (use math.hypot)."""
    raise NotImplementedError("implement distance() so the tests pass")
```

Create `lessons/07-modules/exercises/geom/__init__.py` (comment only — the learner writes the re-exports):
```python
"""The geom package.

Wire up this file so `from exercises.geom import Point, midpoint, distance`
works: import each name from its module (use ABSOLUTE imports —
`from exercises.geom.points import ...`) and list them in __all__.
See the README.
"""
```
IMPORTANT: leave `exercises/geom/__init__.py` with NO re-exports (this is the red-start). Do not add the imports here.

- [ ] **Step 6: Create `solutions/test_geom.py`**

```python
from solutions.geom import Point, distance, midpoint


def test_point_is_reexported() -> None:
    assert Point(1.0, 2.0) == Point(1.0, 2.0)


def test_midpoint() -> None:
    assert midpoint(Point(0.0, 0.0), Point(4.0, 6.0)) == Point(2.0, 3.0)


def test_midpoint_negative() -> None:
    assert midpoint(Point(-2.0, -4.0), Point(2.0, 4.0)) == Point(0.0, 0.0)


def test_midpoint_same_point() -> None:
    p = Point(3.0, 5.0)
    assert midpoint(p, p) == p


def test_distance() -> None:
    assert distance(Point(0.0, 0.0), Point(3.0, 4.0)) == 5.0


def test_distance_same_point() -> None:
    assert distance(Point(1.0, 1.0), Point(1.0, 1.0)) == 0.0


def test_distance_is_symmetric() -> None:
    a, b = Point(0.0, 0.0), Point(3.0, 4.0)
    assert distance(a, b) == distance(b, a)
```

- [ ] **Step 7: Create `exercises/test_geom.py`**

IDENTICAL to Step 6 EXCEPT line 1 is `from exercises.geom import Point, distance, midpoint`. Everything else byte-for-byte the same.

- [ ] **Step 8: Verify red/green**

```bash
( cd lessons/07-modules && uv run pytest exercises -q )
( cd lessons/07-modules && uv run pytest solutions -q )
```
Expected: exercise → 7 failed (the top-level `from exercises.geom import ...` raises `ImportError` at collection because the exercise `__init__.py` re-exports nothing — pytest reports 7 errors/failures); solution → 7 passed.

- [ ] **Step 9: Confirm the package works end-to-end**

```bash
( cd lessons/07-modules && uv run python -c "from solutions.geom import Point, distance, midpoint; print(distance(Point(0,0), Point(3,4))); print(midpoint(Point(0,0), Point(4,6)))" )
```
Expected:
```
5.0
Point(x=2.0, y=3.0)
```

- [ ] **Step 10: Lint + format**

```bash
make lint
uv run ruff format lessons/07-modules
uv run ruff format --check .
```
Expected: `make lint` → "All checks passed!" (absolute imports satisfy TID252; no relative-import errors); `ruff format --check .` → no diff. If ruff rewrites anything, re-run Step 8.

- [ ] **Step 11: Commit**

```bash
git add lessons/07-modules uv.lock
git commit -m "feat(lesson-07): add the geom package (modules, intra-package imports, __init__ re-exports)"
```
Commits the whole scaffolded lesson (placeholder README/slides ride along; overwritten in Tasks 2/3) plus the authored package and `uv.lock`. No `Co-Authored-By` trailer.

---

## Task 2: Author the lesson README

**Files:** Modify `lessons/07-modules/README.md`.

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-07-modules`. If not, STOP.

- [ ] **Step 2: Overwrite `lessons/07-modules/README.md` with EXACTLY this content**

````markdown
# Lesson 07 — Modules, packages, imports

Group related code into a package: split it across modules, import between them,
and re-export a clean public API.

## Learning goals

- Understand that a `.py` file is a **module** and a directory with `__init__.py` is a
  **package**.
- Use the import forms: `import x`, `from x import y`, and `import x as y`.
- Re-export a clean public API from a package's `__init__.py`.
- Know the difference between absolute and relative imports, and why this repo uses
  absolute.

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md),
  [Lesson 02 — Variables, types, operators](../02-variables/README.md),
  [Lesson 03 — Control flow](../03-control-flow/README.md),
  [Lesson 04 — Functions & tests](../04-functions/README.md),
  [Lesson 05 — Collections](../05-collections/README.md), and
  [Lesson 06 — Classes & dataclasses](../06-classes/README.md).

## Concepts

### A module is a file

Every `.py` file is a **module**. `import math` finds the module, runs its top-level
code once, and binds the name `math` to the module object.

```python
import math

math.hypot(3, 4)   # 5.0
```

### Import forms

```python
import math                     # whole module: math.sqrt(9)
from math import sqrt           # one name: sqrt(9)
from math import sqrt as root   # rename on import
from geom.points import Point   # a name from a package module
```

### What `import` actually does

1. Finds the module on `sys.path` (the list of search directories).
2. Runs its top-level code **once**.
3. Caches the module in `sys.modules` (a second import is free).
4. Binds a name in your namespace.

Because top-level code runs on first import, keep it cheap — guard scripts with
`if __name__ == "__main__":`.

### Packages and `__init__.py`

A **package** is a directory containing an `__init__.py`. Importing the package runs its
`__init__.py`; its modules are `package.module`:

```
geom/
├── __init__.py
├── points.py     # geom.points
└── metrics.py    # geom.metrics
```

### `__init__.py` as the public API

Re-export the good names in `__init__.py` so callers write `from geom import distance`
instead of reaching into `geom.metrics`:

```python
from geom.metrics import distance
from geom.points import Point, midpoint

__all__ = ["Point", "distance", "midpoint"]
```

`__all__` lists the package's public names (and controls `from geom import *`).

### Absolute vs relative imports

```python
from geom.points import Point     # absolute — full path from sys.path
from .points import Point         # relative — "the points module next to me"
```

Relative imports only work **inside** a package. This repo (like many others) prefers
**absolute** imports for clarity, and its linter enforces that — so the exercise uses
absolute imports throughout.

### The standard library

Python ships "batteries included" — a large standard library you can import without
installing anything: `math`, `random`, `pathlib`, `json`, `datetime`, `statistics`,
`collections`, and many more. Import what you need.

### Gotcha: don't shadow stdlib names

If you name your own file `math.py`, then `import math` finds *yours* instead of the
standard library's. Avoid standard-library names for your own modules.

## Exercise

Build the `geom` package in `exercises/geom/` so the tests pass:

1. Implement `midpoint(a, b)` in `points.py` — the point halfway between two points.
2. Implement `distance(a, b)` in `metrics.py` — use `math.hypot`.
3. Wire up `__init__.py` to re-export `Point`, `midpoint`, and `distance` using
   **absolute** imports (`from exercises.geom.points import ...`), so
   `from exercises.geom import Point, midpoint, distance` works.

Until `__init__.py` re-exports them, the test file's top import fails and every test is
red.

## How to run

From the repo root:

```bash
make test-lesson LESSON=07-modules
```

Or directly:

```bash
cd lessons/07-modules
uv run pytest exercises          # your work — fails until implemented
uv run pytest solutions          # the reference — passes
```

Try the finished package from a one-liner (run from `lessons/07-modules/`):

```bash
uv run python -c "from solutions.geom import Point, distance; print(distance(Point(0, 0), Point(3, 4)))"
# 5.0
```

## Going further

- `python -m package` runs a package's `__main__.py`.
- `importlib` imports modules by name at runtime.
- Namespace packages: directories without `__init__.py` that still act as packages.
- Third-party packages: `uv add <name>` pulls from PyPI (Phase 3).
- `if __name__ == "__main__":` lets one file act as both an importable module and a
  runnable script.
````

- [ ] **Step 3: Sanity-check**

```bash
grep -ic todo lessons/07-modules/README.md          # expect 0
grep -c '```' lessons/07-modules/README.md           # expect even
head -1 lessons/07-modules/README.md                 # expect: # Lesson 07 — Modules, packages, imports
```

- [ ] **Step 4: Commit**

```bash
git add lessons/07-modules/README.md
git commit -m "docs(lesson-07): author the README (modules, packages, imports)"
```
(No `Co-Authored-By` trailer.)

---

## Task 3: Author the slide deck

**Files:** Modify `lessons/07-modules/slides/slides.md` and `slides/index.html` (`<title>`).

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-07-modules`. If not, STOP.

- [ ] **Step 2: Overwrite `lessons/07-modules/slides/slides.md` with EXACTLY this content**

````markdown
## Lesson 07
### Modules, packages, imports

Split code across modules, import between them, re-export a clean API.

Note:
Build the geom package: points + metrics + an __init__ that re-exports.

---

## A module is a file

```python
import math

math.hypot(3, 4)   # 5.0
```

- Every `.py` file is a module
- `import` runs it once and binds the name

---

## Import forms

```python
import math                     # whole module
from math import sqrt           # one name
from math import sqrt as root   # rename
from geom.points import Point   # from a package module
```

---

## What `import` does

1. Finds the module on `sys.path`
2. Runs its top-level code **once**
3. Caches it in `sys.modules`
4. Binds a name

- A second import is free (cached)

---

## Packages

```text
geom/
├── __init__.py      # makes geom a package
├── points.py        # geom.points
└── metrics.py       # geom.metrics
```

- A package is a directory with `__init__.py`
- Importing it runs `__init__.py`

---

## `__init__.py` = public API

```python
from geom.metrics import distance
from geom.points import Point, midpoint

__all__ = ["Point", "distance", "midpoint"]
```

- Re-export so callers write `from geom import distance`
- `__all__` lists the public names

---

## Our package

```python
# metrics.py
import math
from geom.points import Point

def distance(a: Point, b: Point) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)
```

- `metrics` imports `points` — one module uses another

---

## Absolute vs relative

```python
from geom.points import Point   # absolute
from .points import Point       # relative
```

- Relative only works inside a package
- This repo prefers absolute (its linter enforces it)

---

## The standard library

- `math`, `random`, `pathlib`, `json`
- `datetime`, `statistics`, `collections`
- "Batteries included" — import what you need

---

## Gotchas

- Top-level code runs on **first import** — keep it cheap
- Don't name a file `math.py` — it shadows the stdlib
- Guard scripts with `if __name__ == "__main__":`

---

## Your turn

- Implement `midpoint` in `points.py`, `distance` in `metrics.py`
- Wire `__init__.py` to re-export `Point`, `midpoint`, `distance`
- `make test-lesson LESSON=07-modules` until green

---

## What's next

**Lesson 08 — Phase 1 capstone (CLI).**
````

- [ ] **Step 3: Fix the deck `<title>` in index.html**

The scaffolder derives the title from the slug, producing `<title>Lesson 07 — Modules</title>`. Edit it to EXACTLY (em-dash U+2014):
```html
  <title>Lesson 07 — Modules, packages, imports</title>
```
Do NOT change the `/shared/reveal/...` asset paths.

- [ ] **Step 4: Build; confirm LINK + absolute asset paths**

```bash
make slides-build
grep -q 'href="lessons/07-modules/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
grep -oE '/shared/reveal|\.\./\.\./shared/reveal' dist/lessons/07-modules/slides/index.html | sort | uniq -c
test -f dist/lessons/07-modules/slides/index.html && test -f dist/lessons/07-modules/slides/slides.md && echo "SLIDES_COPIED"
```
Expected: `LINK_OK`; future-placeholder count `21` (with Lesson 06 also published); asset-path grep shows ONLY `/shared/reveal`; `SLIDES_COPIED`. Then `rm -rf dist`.

- [ ] **Step 5: Dev-server smoke test**

```bash
( uv run python -m slides_dev --lesson 07-modules --repo-root "$(pwd)" --port 8000 & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
kill "$(lsof -ti:8000)" 2>/dev/null || true
lsof -ti:8000 || echo "port clear"
```
Expected: title line `<title>Lesson 07 — Modules, packages, imports</title>`, `slidesmd=200`, `revealcss=200`, `port clear`.

- [ ] **Step 6: Commit**

```bash
git add lessons/07-modules/slides/slides.md lessons/07-modules/slides/index.html
git commit -m "feat(lesson-07): author the slide deck"
```
(No `Co-Authored-By` trailer.)

---

## Task 4: Final verification

- [ ] **Step 1: Confirm branch** — `git branch --show-current` → `lesson-07-modules`. If not, STOP, report BLOCKED.

- [ ] **Step 2: Full quality bar**

```bash
make lint
uv run ruff format --check .
make typecheck
make test
```
Expected: `make lint` → All checks passed!; `ruff format --check .` → no diff; `make typecheck` → Success (tools); `make test` → tools + Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10), 06 (11), 07 (7) solutions all pass; exit 0; no `import file mismatch`.

- [ ] **Step 3: Lesson red/green + package demo**

```bash
make test-lesson LESSON=07-modules
( cd lessons/07-modules && uv run python -c "from solutions.geom import Point, distance, midpoint; print(distance(Point(0,0), Point(3,4))); print(midpoint(Point(0,0), Point(4,6)))" )
```
Expected: exercises FAIL (7; ImportError→then NotImplementedError, tolerated), solutions PASS (7), exit 0; demo prints `5.0` then `Point(x=2.0, y=3.0)`.

- [ ] **Step 4: Landing page link + git hygiene + no co-author trailers**

```bash
make slides-build
grep -q 'href="lessons/07-modules/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
rm -rf dist
git status --porcelain
git ls-files lessons/07-modules | sort
git log --oneline main..HEAD
git log main..HEAD --format='%B' | grep -i 'co-authored\|generated with' && echo "TRAILER FOUND (bad)" || echo "no trailers — good"
```
Expected: `LINK_OK`; future count `21`; clean tree; `git ls-files lessons/07-modules` lists exactly: `pyproject.toml`, `README.md`, `slides/{index.html,slides.md,assets/.gitkeep}`, `exercises/{__init__.py,test_geom.py}`, `exercises/geom/{__init__.py,points.py,metrics.py}`, `solutions/{__init__.py,test_geom.py}`, `solutions/geom/{__init__.py,points.py,metrics.py}` — NO `main.py`/`test_main.py`; 3 commits; `no trailers — good`.

- [ ] **Step 5: Confirm port clear** — `lsof -ti:8000 || echo "port clear"` → `port clear`.

- [ ] **Step 6: Commit only if Steps 1-5 surfaced changes.** If clean, report CLEAN; if a check FAILED, STOP and report BLOCKED.

---

## Notes for execution

- **Three commits** when done: `feat(lesson-07): add the geom package …`, `docs(lesson-07): author the README …`, `feat(lesson-07): author the slide deck`.
- **Mirror Lesson 06** for any shape question.
- **Never** add a `Co-Authored-By` / AI-attribution trailer; **never** push or open a PR.
- The exercise `geom/__init__.py` is intentionally empty of re-exports (red-start). Do not add the imports there.
- Absolute imports only: `metrics.py` and `geom/__init__.py` differ between the exercise (`exercises.geom.`) and solution (`solutions.geom.`) copies — that is expected, not a bug.
- `make typecheck` covers `tools/` only; lesson code isn't a mypy gate but must be `ruff`-clean.
```
