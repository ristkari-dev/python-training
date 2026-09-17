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
import statistics as stats      # rename a module: stats.mean([1, 2])
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

In this lesson the lesson folder (`lessons/07-modules/`) is on `sys.path`, so the full
absolute path is `exercises.geom.points` (or `solutions.geom.points`); the examples
above shorten it to `geom`.

### The standard library

Python ships "batteries included" — a large standard library you can import without
installing anything: `math`, `random`, `pathlib`, `json`, `datetime`, `statistics`,
`collections`, and many more. Import what you need.

### Gotcha: don't shadow stdlib names

If you name your own file `random.py`, then `import random` finds *yours* instead of
the standard library's. Avoid standard-library names for your own modules.

## Exercise

Build the `geom` package in `exercises/geom/` so the tests pass:

1. Implement `midpoint(a, b)` in `points.py` — the point halfway between two points.
2. Implement `distance(a, b)` in `metrics.py` — use `math.hypot`.
3. Wire up `__init__.py` to re-export `Point`, `midpoint`, and `distance` using
   **absolute** imports (`from exercises.geom.points import ...`), so
   `from exercises.geom import Point, midpoint, distance` works.

Until `__init__.py` re-exports them, the test file's top import fails and every test is
red.

Tip: you can wire `__init__.py` first — the stubs already define all three names, so
the tests then collect and report `midpoint` and `distance` separately as you
implement them.

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

Try the finished package from a one-liner:

```bash
cd lessons/07-modules
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
