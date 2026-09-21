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
import statistics as stats      # rename a module
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
from exercises.geom.points import Point

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
- Don't name a file `random.py` — it shadows the stdlib
- Circular imports (a imports b imports a) can fail — keep dependencies one-way
- Guard scripts with `if __name__ == "__main__":`

---

## Your turn

- Implement `midpoint` in `exercises/geom/points.py`, `distance` in `exercises/geom/metrics.py`
- Wire `exercises/geom/__init__.py` to re-export `Point`, `midpoint`, `distance` (absolute: `from exercises.geom.points import ...`)
- `make test-lesson LESSON=07-modules` until green

---

## What's next

**Lesson 08 — Phase 1 capstone (CLI).**
