# Lesson 07 — Modules, packages, imports — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-07-08
**Owner:** Aki Ristkari

## Summary

The seventh course lesson moves from single files to a **package**. Students build a
small `geom` package — two modules plus an `__init__.py` — where one module imports
another, one module imports from the standard library (`math`), and the `__init__.py`
re-exports a clean public API. This is the exact structural skill Lesson 08's capstone
CLI needs. The graded exercise centres on writing the `__init__.py` re-exports (a
red-start: the exercise `__init__.py` starts empty) and two small functions; the
stdlib tour, import forms, and the absolute-vs-relative distinction are taught on the
slides/README but not graded. Seventh lesson, so `make test` now spans seven lessons.

## Scope (from the course design spec)

Lesson 7: files vs modules, `__init__.py`, absolute vs relative imports, the import
system mental model, stdlib tour.

**Graded:** a `geom` package — `points.py` (`Point` dataclass given + `midpoint` to
implement), `metrics.py` (`distance` to implement, importing `Point` from `points` and
`math` from the stdlib), and `__init__.py` (the learner writes the re-exports).
**Slides/README only (not graded):** import forms, the import-system mental model,
absolute vs relative imports (the repo bans relative imports globally via ruff TID252,
so they are shown but never used in graded code), and the stdlib tour.

## Package naming and layout

The lesson package is **`geom`** (module files `points.py`, `metrics.py`; test file
`test_geom.py`). Continues Lesson 06's geometry theme (`Point`). Layout:

```
lessons/07-modules/
├── exercises/
│   ├── __init__.py            # empty (kept from scaffold)
│   ├── geom/
│   │   ├── __init__.py        # red-start: comment only; learner writes re-exports
│   │   ├── points.py          # Point (given) + midpoint (stub)
│   │   └── metrics.py         # distance (stub); imports points + math
│   └── test_geom.py           # from exercises.geom import Point, midpoint, distance
└── solutions/
    ├── __init__.py            # empty
    ├── geom/
    │   ├── __init__.py        # re-exports Point, midpoint, distance
    │   ├── points.py
    │   └── metrics.py
    └── test_geom.py           # from solutions.geom import ...
```

## Absolute imports only

Per the repo's ruff config (`ban-relative-imports = "all"`, TID252), the package's
internal imports are **absolute**: `metrics.py` uses `from exercises.geom.points import
Point` and `__init__.py` uses `from exercises.geom.points import Point, midpoint` /
`from exercises.geom.metrics import distance`. The solution copies use the
`solutions.geom.` prefix. Consequence: unlike prior lessons, the exercise and solution
copies of `metrics.py` and `__init__.py` differ by the `exercises.`/`solutions.` prefix
(not only the test file's top import). This is accepted — it models the repo's real
absolute-only convention. Relative imports (`from .points import Point`) are shown on
the slides/README as the alternative, with a note that this repo defaults to absolute.

## Exercise — build the `geom` package

### `solutions/geom/points.py`

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

### `solutions/geom/metrics.py`

```python
import math

from solutions.geom.points import Point


def distance(a: Point, b: Point) -> float:
    """Return the straight-line distance between a and b."""
    return math.hypot(a.x - b.x, a.y - b.y)
```

`math.hypot` is used (not a hand-rolled `** 0.5`) both to demonstrate a stdlib import
inside the package and because it is numerically robust.

### `solutions/geom/__init__.py`

```python
"""The geom package: points and the distance between them."""

from solutions.geom.metrics import distance
from solutions.geom.points import Point, midpoint

__all__ = ["Point", "distance", "midpoint"]
```

### `solutions/test_geom.py`

Imports from the package root (so it exercises the `__init__.py` re-exports). Seven
deterministic tests — the distances chosen are exact floats (3-4-5 → 5.0; midpoints of
even coordinates).

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

### `exercises/` stubs (red-start)

`exercises/geom/points.py` — `Point` given (implemented); `midpoint` raises:

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

`exercises/geom/metrics.py` — imports given (worked example to read); `distance` raises:

```python
import math

from exercises.geom.points import Point


def distance(a: Point, b: Point) -> float:
    """Return the straight-line distance between a and b (use math.hypot)."""
    raise NotImplementedError("implement distance() so the tests pass")
```

`exercises/geom/__init__.py` — the red-start; comment only, no re-exports:

```python
"""The geom package.

Wire up this file so `from exercises.geom import Point, midpoint, distance`
works: import each name from its module (use ABSOLUTE imports —
`from exercises.geom.points import ...`) and list them in __all__.
See the README.
"""
```

`exercises/test_geom.py` — identical to the solutions test except line 1 reads
`from exercises.geom import Point, distance, midpoint`.

Because the exercise `__init__.py` re-exports nothing, `from exercises.geom import
Point, distance, midpoint` fails at collection with `ImportError`, so all seven tests
are red until the learner (1) implements `midpoint`, (2) implements `distance`, and
(3) writes the `__init__.py` re-exports.

### `__main__` demo

No `__main__` block inside the package modules (a package is imported, not run as a
script here). The README/How-to-run shows a one-liner:
`uv run python -c "from solutions.geom import Point, distance; print(distance(Point(0,0), Point(3,4)))"`
→ prints `5.0`.

## pyproject / harness

Scaffolded `pyproject.toml` (name `lesson-07-modules`, `package = false`, pytest
`pythonpath = ["."]`) is unchanged. `exercises/` and `solutions/` are packages
(`__init__.py`); the new `geom/` sub-package has its own `__init__.py`. Tests import
`from exercises.geom import ...` / `from solutions.geom import ...`. No new
`import file mismatch` risk — the two `test_geom.py` files sit in distinct
`exercises`/`solutions` packages, exactly as prior lessons' duplicate test basenames do.

## Slides (`slides/slides.md`)

About twelve slides, `---` separated, mirrors Lesson 06 deck style.

1. **Title** — "Lesson 07 — Modules, packages, imports" + one-line goal.
2. **A module is a file** — any `.py` file is a module; `import name` runs it once and
   binds the module object.
3. **Import forms** — `import math`; `from math import hypot`; `import numpy as np`
   (naming only); `from pkg.mod import thing`.
4. **What `import` does** — finds the module on `sys.path`, runs its top-level code
   once, caches it in `sys.modules`, binds a name.
5. **Packages** — a directory with `__init__.py`; importing the package runs its
   `__init__.py`; sub-modules are `package.module`.
6. **`__init__.py` as the public API** — re-export the good names so callers write
   `from geom import distance`, not `from geom.metrics import distance`; `__all__`.
7. **Our package** — the `geom` layout (`points.py`, `metrics.py`, `__init__.py`);
   `metrics` imports `points`.
8. **Absolute vs relative** — absolute `from geom.points import Point` vs relative
   `from .points import Point`; this repo (and many) default to absolute; relative only
   works inside a package.
9. **The standard library** — "batteries included": `math`, `random`, `pathlib`,
   `json`, `datetime`, `statistics`, `collections`; import what you need.
10. **Gotchas** — top-level code runs on first import (keep it cheap / guard with
    `if __name__ == "__main__":`); circular imports; a local file shadowing a stdlib
    name (e.g. naming your file `math.py`).
11. **Your turn** — implement `midpoint` and `distance`, then wire up `__init__.py`;
    `make test-lesson LESSON=07-modules` until green.
12. **What's next** — Lesson 08 — Phase 1 capstone (CLI).

## README (`README.md`)

Four-file-convention sections:

- **Learning goals** — understand that a `.py` file is a module and a directory with
  `__init__.py` is a package; use the import forms; re-export a clean public API from
  `__init__.py`; know absolute vs relative imports and why this repo uses absolute.
- **Prereqs** — Lessons 01–06 (single joined bullet, full titles, matching lessons
  03–06).
- **Concepts** — module = file; import forms (`import x`, `from x import y`, `as`);
  what import does (sys.path, runs once, sys.modules cache, name binding); packages and
  `__init__.py`; `__init__.py` as public API + `__all__`; absolute vs relative imports
  (repo defaults to absolute; relative shown for contrast); a short stdlib tour;
  gotchas (top-level code runs on import; shadowing a stdlib name).
- **Exercise brief** — build the `geom` package: implement `midpoint` in `points.py`
  and `distance` in `metrics.py`, then wire `__init__.py` to re-export `Point`,
  `midpoint`, and `distance` so `from exercises.geom import ...` works.
- **How to run** — `make test-lesson LESSON=07-modules`; the one-liner demo
  (`uv run python -c "from solutions.geom import Point, distance; print(distance(Point(0,0), Point(3,4)))"`).
- **Going further** — `python -m pkg` and `__main__.py`; `importlib`; namespace
  packages (no `__init__.py`); third-party packages via `uv add` (Phase 3);
  `if __name__ == "__main__":` as a script/import guard.

## Verification (success criteria)

- `make test-lesson LESSON=07-modules` → exercise tests FAIL (ImportError at collection
  until `__init__.py` is wired, then `NotImplementedError`); solution tests PASS (7);
  exit 0.
- `make test` → tools + Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10), 06 (11),
  07 (7) solutions all pass, isolated per-lesson processes; no `import file mismatch`.
- `uv run python -c "from solutions.geom import Point, distance; print(distance(Point(0,0), Point(3,4)))"`
  (run from `lessons/07-modules/`) → prints `5.0`.
- `make slides-build` → `dist/index.html` shows `07-modules` as a link; future-
  placeholder count drops to 21 (assumes Lesson 06 already merged); absolute
  `/shared/reveal/...` asset paths; deck renders.
- `make lint` and `uv run ruff format --check .` → clean (absolute imports satisfy
  TID252). `make typecheck` stays scoped to tools; lesson code cleanly typed but not a
  gate yet (strict lesson typing starts at Lesson 09).

## Non-goals

- No third-party packages / `uv add` — stdlib only (third-party arrives in Phase 3).
- No `importlib`, namespace packages, or circular-import deep dive — mentioned in
  going-further at most.
- Relative imports are shown on slides/README but NOT used in graded code (repo bans
  them via ruff TID252).
- No graded stdlib-tour drills — the only stdlib use in graded code is `math.hypot`
  inside `metrics.py`.
- No catalog change — `07-modules` is already listed.
- No tooling/harness changes; no ruff config change (absolute imports avoid needing a
  TID252 exception). No strict mypy gate on lesson code yet.

## Open items deferred to implementation planning

- Exact slide prose and README wording.
- The deck `<title>` is hand-set to "Lesson 07 — Modules, packages, imports" (the slug
  gives "Modules"; the catalog name is longer — edit like Lessons 04/06).
