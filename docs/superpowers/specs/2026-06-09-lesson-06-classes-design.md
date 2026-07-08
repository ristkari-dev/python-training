# Lesson 06 — Classes & dataclasses — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-06-09
**Owner:** Aki Ristkari

## Summary

The sixth course lesson introduces user-defined types. The whole lesson hangs on one
contrast: students write a `Rectangle` **by hand** — `__init__`, a method, and the
`__repr__`/`__eq__` dunders you would otherwise type yourself — then build a `Point`
with **`@dataclass`** and watch the same machinery (`__init__`, `__repr__`, `__eq__`)
appear for free. A `@classmethod` alternative constructor on the dataclass rounds out
the graded work. The instance/class/static-method distinction and simple inheritance
are taught on the slides/README but **not graded** (the graded exercise touches only
`@classmethod`). Sixth lesson, so `make test` now spans six lessons.

## Scope (from the course design spec)

Lesson 6: `__init__`, methods, `@dataclass`, instance vs class vs static, simple
inheritance, dunder basics (`__repr__`, `__eq__`).

**Graded:** a hand-written class (`__init__`, a method, `__repr__`, `__eq__`), an
equivalent `@dataclass` (fields + a method + a `@classmethod`).
**Slides/README only (not graded):** the instance vs class vs static method trio
(only `@classmethod` is exercised), simple inheritance, and the "going further"
dataclass features (frozen/order/defaults/`__hash__`).

## Module naming

The lesson module is **`shapes.py`** (and tests `test_shapes.py`). A geometry theme
(`Rectangle`, `Point`) makes the hand-written-vs-dataclass contrast concrete, and
`shapes` shadows no standard-library module (a name like `types.py` would). Import
paths: `from exercises.shapes import Point, Rectangle` /
`from solutions.shapes import Point, Rectangle`.

## Exercise — the hand-written-vs-dataclass contrast

Two classes. `Rectangle` shows everything a plain class needs; `Point` shows how
`@dataclass` removes most of it.

### `Rectangle` — written by hand

- `__init__(self, width: float, height: float) -> None` — store both as instance
  attributes.
- `area(self) -> float` — return `width * height`.
- `__repr__(self) -> str` — return `"Rectangle(width=3, height=4)"`.
- `__eq__(self, other: object) -> bool` — equal when `other` is a `Rectangle` with the
  same dimensions. Uses an `isinstance` guard and returns a plain `bool` (the
  `NotImplemented`-return refinement is a "going further" note, not graded).

### `Point` — built with `@dataclass`

- fields `x: float`, `y: float` — `@dataclass` generates `__init__`, `__repr__`, `__eq__`.
- `translate(self, dx: float, dy: float) -> "Point"` — return a **new** shifted `Point`
  (teaches that methods can return fresh instances; the original is unchanged).
- `@classmethod from_tuple(cls, coords: tuple[float, float]) -> "Point"` — an
  alternative constructor that calls `cls(...)` (teaches `classmethod`/`cls`, and that a
  dataclass is still an ordinary class you can add methods to).

### Coverage mapping

- **`class` / `__init__` / `self` / instance attributes** — `Rectangle`.
- **methods** — `Rectangle.area`, `Point.translate`.
- **`__repr__` (hand-written)** — `Rectangle.__repr__`.
- **`__eq__` (hand-written, value equality, `isinstance` guard)** — `Rectangle.__eq__`.
- **`@dataclass` (generated `__init__`/`__repr__`/`__eq__`)** — `Point`.
- **`@classmethod` / `cls` (alternative constructor)** — `Point.from_tuple`.
- **instance vs class vs static methods, simple inheritance** — slides/README only;
  not graded.

### Red-start design (the dataclass field declaration)

In `exercises/shapes.py`, `Point`'s **fields are left for the learner to declare** (a
guiding comment, no fields yet). This keeps the exercise genuinely red — `Point(1.0, 2.0)`
raises `TypeError` (a no-field dataclass `__init__` takes no positional args) until the
learner adds `x: float` / `y: float`. The moment they do, the repr/equality/construct
tests pass with **no method code written** — making "`@dataclass` wrote the boilerplate"
tangible. `Point.translate`, `Point.from_tuple`, and all of `Rectangle`'s methods raise
`NotImplementedError("implement … so the tests pass")` until implemented.

### `exercises/shapes.py` (stub)

```python
from dataclasses import dataclass


class Rectangle:
    """An axis-aligned rectangle, written by hand.

    Implement __init__, area, __repr__, and __eq__ so the tests pass.
    """

    def __init__(self, width: float, height: float) -> None:
        """Store width and height as instance attributes."""
        raise NotImplementedError("implement Rectangle.__init__() so the tests pass")

    def area(self) -> float:
        """Return width * height."""
        raise NotImplementedError("implement Rectangle.area() so the tests pass")

    def __repr__(self) -> str:
        """Return a string like 'Rectangle(width=3, height=4)'."""
        raise NotImplementedError("implement Rectangle.__repr__() so the tests pass")

    def __eq__(self, other: object) -> bool:
        """Two rectangles are equal when both dimensions match."""
        raise NotImplementedError("implement Rectangle.__eq__() so the tests pass")


@dataclass
class Point:
    """A 2-D point built with @dataclass.

    Declare two float fields, x and y. @dataclass then generates __init__,
    __repr__, and __eq__ for you — you write no code for those.
    """

    # Declare the fields here: x: float and y: float

    def translate(self, dx: float, dy: float) -> "Point":
        """Return a NEW Point shifted by (dx, dy)."""
        raise NotImplementedError("implement Point.translate() so the tests pass")

    @classmethod
    def from_tuple(cls, coords: tuple[float, float]) -> "Point":
        """Build a Point from an (x, y) tuple — an alternative constructor."""
        raise NotImplementedError("implement Point.from_tuple() so the tests pass")


if __name__ == "__main__":
    r = Rectangle(3, 4)
    print(r)
    print(r.area())
    print(r == Rectangle(3, 4))
    p = Point(1.0, 2.0)
    print(p)
    print(p.translate(2.0, 3.0))
    print(Point.from_tuple((5.0, 6.0)))
```

### `solutions/shapes.py`

```python
from dataclasses import dataclass


class Rectangle:
    """An axis-aligned rectangle, written by hand to show the machinery a plain
    class needs: __init__, a method, and the __repr__/__eq__ dunders."""

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def __repr__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Rectangle)
            and self.width == other.width
            and self.height == other.height
        )


@dataclass
class Point:
    """A 2-D point built with @dataclass, which generates __init__, __repr__, and
    __eq__ for us. A dataclass is still an ordinary class — we add methods."""

    x: float
    y: float

    def translate(self, dx: float, dy: float) -> "Point":
        return Point(self.x + dx, self.y + dy)

    @classmethod
    def from_tuple(cls, coords: tuple[float, float]) -> "Point":
        return cls(coords[0], coords[1])


if __name__ == "__main__":
    r = Rectangle(3, 4)
    print(r)                              # Rectangle(width=3, height=4)
    print(r.area())                       # 12
    print(r == Rectangle(3, 4))           # True
    p = Point(1.0, 2.0)
    print(p)                              # Point(x=1.0, y=2.0)
    print(p.translate(2.0, 3.0))          # Point(x=3.0, y=5.0)
    print(Point.from_tuple((5.0, 6.0)))   # Point(x=5.0, y=6.0)
```

The `__main__` block is non-interactive; it prints the six demo lines once
implemented. Running the exercise copy before implementing raises `NotImplementedError`
(from `Rectangle.__init__`) — expected; the README says run the tests first.

### Tests (`exercises/test_shapes.py` / `solutions/test_shapes.py`)

Identical except the import line. Eleven tests, all deterministic. The two "is
generated" tests are the payoff: the learner writes no `__repr__`/`__eq__` for `Point`,
yet they pass once the fields are declared.

```python
from solutions.shapes import Point, Rectangle


def test_rectangle_init_stores_dimensions() -> None:
    r = Rectangle(3, 4)
    assert r.width == 3
    assert r.height == 4


def test_rectangle_area() -> None:
    assert Rectangle(3, 4).area() == 12


def test_rectangle_repr() -> None:
    assert repr(Rectangle(3, 4)) == "Rectangle(width=3, height=4)"


def test_rectangle_equal_when_dimensions_match() -> None:
    assert Rectangle(3, 4) == Rectangle(3, 4)


def test_rectangle_not_equal_when_dimensions_differ() -> None:
    assert Rectangle(3, 4) != Rectangle(3, 5)


def test_rectangle_not_equal_to_other_type() -> None:
    assert Rectangle(3, 4) != "rectangle"


def test_point_constructs_with_fields() -> None:
    p = Point(1.0, 2.0)
    assert p.x == 1.0
    assert p.y == 2.0


def test_point_repr_is_generated() -> None:
    assert repr(Point(1.0, 2.0)) == "Point(x=1.0, y=2.0)"


def test_point_equality_is_generated() -> None:
    assert Point(1.0, 2.0) == Point(1.0, 2.0)


def test_point_translate_returns_new_point() -> None:
    original = Point(1.0, 2.0)
    moved = original.translate(2.0, 3.0)
    assert moved == Point(3.0, 5.0)
    assert original == Point(1.0, 2.0)  # original is unchanged


def test_point_from_tuple() -> None:
    assert Point.from_tuple((5.0, 6.0)) == Point(5.0, 6.0)
```

The solutions copy is identical except the first line reads
`from solutions.shapes import Point, Rectangle`.

## Files

`lessons/06-classes/` (scaffold with `make new-lesson NAME=06-classes`, then author;
replace the placeholder `main.py`/`test_main.py` with `shapes.py`/`test_shapes.py`):

```
lessons/06-classes/
├── pyproject.toml          # name "lesson-06-classes", package=false, pytest pythonpath=["."]
├── README.md               # authored
├── slides/
│   ├── index.html          # scaffold; <title> "Lesson 06 — Classes & dataclasses"; absolute /shared/reveal paths
│   ├── slides.md           # authored
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py         # empty (kept)
│   ├── shapes.py
│   └── test_shapes.py
└── solutions/
    ├── __init__.py         # empty
    ├── shapes.py
    └── test_shapes.py
```

## Slides (`slides/slides.md`)

About twelve slides, `---` separated, code in fenced `python` blocks, ~15 visible lines
max. `Note:` speaker notes where useful. Mirrors the Lesson 05 deck style.

1. **Title** — "Lesson 06 — Classes & dataclasses" + one-line goal.
2. **Why classes** — bundle data + behavior; an object has state (attributes) and
   behavior (methods); a class is the blueprint, an instance is one object.
3. **Defining a class** — `class Rectangle:`, `__init__(self, ...)`, what `self` is,
   setting instance attributes.
4. **Methods** — `area(self)`; call as `r.area()`; methods read `self`.
5. **`__repr__`** — a readable representation; without it you get
   `<Rectangle object at 0x…>`; used by the REPL and `print`.
6. **`__eq__`** — value equality vs identity (`==` vs `is`); the `isinstance` guard;
   the default `__eq__` compares identity.
7. **`@dataclass`** — declare fields, get `__init__`/`__repr__`/`__eq__` for free; the
   `Point` example; far less boilerplate than `Rectangle`.
8. **Dataclasses are still classes** — add ordinary methods (`translate` returns a new
   `Point`).
9. **Method kinds** — instance method (takes `self`), `@classmethod` (takes `cls`, e.g.
   the `from_tuple` alternative constructor), `@staticmethod` (takes neither). Only
   `@classmethod` is in the exercise.
10. **Inheritance (in depth, not graded)** — `class Square(Rectangle)`,
    `super().__init__(side, side)`, overriding `__repr__`.
11. **Your turn** — implement `Rectangle` and `Point` in `exercises/shapes.py`;
    `make test-lesson LESSON=06-classes`; run the module.
12. **What's next** — Lesson 07 — Modules, packages, imports.

## README (`README.md`)

Four-file-convention sections:

- **Learning goals** — define a class with `__init__` and methods and understand `self`;
  write `__repr__` and `__eq__` by hand; use `@dataclass` to generate that boilerplate;
  use a `@classmethod` as an alternative constructor.
- **Prereqs** — Lessons 01, 02, 03, 04, 05.
- **Concepts** — classes, `__init__`, `self`, instance attributes; methods; `__repr__`
  (readable representation); `__eq__` (value equality vs identity; `isinstance` guard);
  `@dataclass` (generated dunders, much less boilerplate); dataclasses are still classes
  (add methods/classmethods); the instance vs class vs static method trio (only
  `classmethod` is exercised); simple inheritance (`Square(Rectangle)`, `super()`); a
  short "plain class vs dataclass — when to pick which" note.
- **Exercise brief** — implement `Rectangle` (`__init__`, `area`, `__repr__`, `__eq__`)
  and `Point` (declare the `x`/`y` fields, then `translate` and `from_tuple`) in
  `exercises/shapes.py` so the tests pass.
- **How to run** — `make test-lesson LESSON=06-classes` (or
  `cd lessons/06-classes && uv run pytest exercises`); run the module
  `cd lessons/06-classes && uv run python -m exercises.shapes`. Run the tests before the
  module (an unimplemented method raises `NotImplementedError`).
- **Going further** — `@dataclass(frozen=True)` for immutable values; default field
  values and `field(default_factory=list)`; ordering with `@dataclass(order=True)` /
  `__lt__`; `__hash__` (and why defining `__eq__` drops it); returning `NotImplemented`
  from `__eq__` so the other operand can cooperate; `@dataclass(slots=True)`; using
  `typing.Self` instead of the `"Point"` forward reference.

## Verification (success criteria)

- `make test-lesson LESSON=06-classes` → exercise tests FAIL (`NotImplementedError` for
  `Rectangle`; `TypeError`/`NotImplementedError` for `Point` until fields + methods are
  written); solution tests PASS (11); target exit 0.
- `make test` → tools + Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10), 06 (11)
  solutions all pass, in isolated per-lesson processes; no `import file mismatch`. (Now
  spans six lessons.)
- `cd lessons/06-classes && uv run python -m solutions.shapes` → prints the six demo
  lines (`Rectangle(width=3, height=4)`, `12`, `True`, `Point(x=1.0, y=2.0)`,
  `Point(x=3.0, y=5.0)`, `Point(x=5.0, y=6.0)`).
- `make slides-build` → `dist/index.html` shows `06-classes` as a link (no longer
  faded); future-placeholder count drops from 23 to 22; the built deck uses absolute
  `/shared/reveal/...` asset paths; the deck renders in a browser (multiple slides, no
  `/shared/reveal` 404s).
- `make lint` and `uv run ruff format --check .` → clean. `make typecheck` stays scoped
  to tools and remains clean; lesson code is cleanly typed but not a typecheck gate
  (strict lesson typing starts at Lesson 09).
- The deck renders via `make slides-dev LESSON=06-classes`.

## Non-goals

- No graded inheritance, `@staticmethod`, or full instance/class/static coverage —
  slides/README only; `@classmethod` is the single graded method kind.
- No frozen/ordered dataclasses, default fields, or `__hash__` in the graded exercise —
  going-further only.
- No `@property`, abstract base classes, `Protocol`, `__slots__`, or other dunders
  beyond `__repr__`/`__eq__` — later/out of scope.
- The `__eq__` solution returns a plain `bool` via an `isinstance` guard; returning
  `NotImplemented` is mentioned in "going further" but not used (keeps the beginner
  exercise mypy-trivially-correct).
- No catalog change — `06-classes` is already listed in
  `tools/build_index/src/build_index/catalog.py`.
- No tooling/harness changes. No strict mypy gate on lesson code (starts Lesson 09); the
  code is nonetheless cleanly typed.

## Open items deferred to implementation planning

- Exact slide prose and README concept wording.
- Whether the deck's `index.html` `<title>` is hand-edited to
  "Lesson 06 — Classes & dataclasses" (default: yes, matching prior lessons).
