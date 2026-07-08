# Plan H — Lesson 06 (Classes & dataclasses)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the sixth course lesson — define a `Rectangle` by hand (`__init__`, `area`, `__repr__`, `__eq__`), then a `Point` with `@dataclass` (fields + `translate` + a `from_tuple` classmethod), so learners feel how `@dataclass` generates the boilerplate.

**Architecture:** Scaffold `lessons/06-classes/` with the existing `new_lesson` tool, replace the placeholder exercise with `shapes.py` (exercise stubs raise `NotImplementedError`; the dataclass fields are left for the learner to declare so the exercise starts red; solutions implemented), author the README + slide deck. The module is named `shapes.py` (geometry theme; shadows no stdlib module). No tooling/harness changes. Sixth lesson, so `make test` now spans six lessons.

**Tech Stack:** Python 3.13, uv workspace, pytest, ruff, mypy, GNU Make, the existing `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored).

---

## Context for the implementer

- **Repo state:** Plans A–G merged to `main`; lessons `01-hello` … `05-collections` exist and are the pattern to mirror. `make test`/`test-lesson` run each lesson in an isolated pytest process by `cd`-ing into the lesson dir.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`). After scaffolding a lesson, run it.
- **`make new-lesson NAME=06-classes`** produces the lesson with `pyproject.toml` (name `lesson-06-classes`, `[tool.uv] package=false`, `[tool.pytest.ini_options] pythonpath=["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}` (placeholder no-arg `hello()`). The scaffolder derives the deck title from the slug ("Classes") and emits **absolute** `/shared/reveal/...` asset paths (do not change those).
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("06", "classes", "Classes & dataclasses", …, 1)`, so `dir_name()` is `06-classes`. Once `lessons/06-classes/slides/` exists, `build_index` renders it as a link. No catalog change needed.
- **Module naming:** use `shapes.py`/`test_shapes.py` — NOT `classes.py` or `types.py`. The geometry theme (`Rectangle`, `Point`) carries the hand-written-vs-dataclass contrast, and `shapes` shadows no stdlib module.
- **Design spec:** `docs/superpowers/specs/2026-06-09-lesson-06-classes-design.md`.
- **Mirror Lesson 05** at `lessons/05-collections/` for exact file shapes, README structure, and slide style.
- **Typing gate:** `make typecheck` is scoped to `tools/` only; lesson code is NOT a mypy gate yet (strict lesson typing starts at Lesson 09). Lesson code must still be `ruff`-clean and cleanly typed.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Branch:** all work happens on `lesson-06-classes` (created from up-to-date `main`). Every task's first step confirms the branch.
- **Commit messages:** Conventional Commits. **Do NOT add a `Co-Authored-By` trailer or any AI-attribution line to commits** (project rule). Subject + optional body only.
- **Do NOT push** — the controller handles branch finishing.
- The module file is named `shapes.py` (tests `test_shapes.py`), replacing the scaffold's `main.py`/`test_main.py`.

---

## File Structure

```
lessons/06-classes/                       (NEW — scaffolded then authored)
├── pyproject.toml                        (from scaffold; unchanged)
├── README.md                             (authored — Task 2)
├── slides/
│   ├── index.html                        (from scaffold; <title> verified — Task 3)
│   ├── slides.md                         (authored — Task 3)
│   └── assets/.gitkeep                   (from scaffold)
├── exercises/
│   ├── __init__.py                       (from scaffold; empty)
│   ├── shapes.py                         (authored — Task 1; replaces main.py)
│   └── test_shapes.py                    (authored — Task 1; replaces test_main.py)
└── solutions/
    ├── __init__.py                       (from scaffold; empty)
    ├── shapes.py                         (authored — Task 1)
    └── test_shapes.py                    (authored — Task 1)
```

No other files change. No catalog edit, no Makefile edit, no tooling change.

---

## Task 1: Scaffold lesson 06 and author the exercise + solution

**Files:**
- Create (via scaffold): `lessons/06-classes/` tree
- Delete: `lessons/06-classes/exercises/main.py`, `lessons/06-classes/exercises/test_main.py`, `lessons/06-classes/solutions/main.py`, `lessons/06-classes/solutions/test_main.py`
- Create: `lessons/06-classes/exercises/shapes.py`, `lessons/06-classes/exercises/test_shapes.py`, `lessons/06-classes/solutions/shapes.py`, `lessons/06-classes/solutions/test_shapes.py`

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current`
Expected: `lesson-06-classes`. If it prints anything else, STOP and report — do not scaffold on the wrong branch.

- [ ] **Step 2: Scaffold the lesson**

Run:
```bash
make new-lesson NAME=06-classes
make sync
```
Expected: `make new-lesson` prints `created lessons/06-classes`; `make sync` (uv sync --all-packages) succeeds and installs `lesson-06-classes` as a workspace member.

- [ ] **Step 3: Remove the placeholder module/test files**

Run:
```bash
git rm -f lessons/06-classes/exercises/main.py lessons/06-classes/exercises/test_main.py \
          lessons/06-classes/solutions/main.py lessons/06-classes/solutions/test_main.py
```
(If `git rm` complains they are untracked, use plain `rm`.) Expected: the four placeholder files are gone; `__init__.py` files remain.

- [ ] **Step 4: Write `lessons/06-classes/solutions/shapes.py`**

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

- [ ] **Step 5: Write `lessons/06-classes/exercises/shapes.py` (stub)**

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

Note: the exercise's `Point` deliberately has **no fields** so the exercise starts red (`Point(1.0, 2.0)` raises `TypeError`). Keep the `# Declare the fields here` comment as the learner's cue.

- [ ] **Step 6: Write `lessons/06-classes/solutions/test_shapes.py`**

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

- [ ] **Step 7: Write `lessons/06-classes/exercises/test_shapes.py`**

Identical to the solutions test file EXCEPT the import line. The full content:

```python
from exercises.shapes import Point, Rectangle


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

- [ ] **Step 8: Verify exercise fails, solution passes**

Run:
```bash
( cd lessons/06-classes && uv run pytest exercises -q )
( cd lessons/06-classes && uv run pytest solutions -q )
```
Expected: exercise run → 11 failed (the `Rectangle` tests raise `NotImplementedError`; the `Point` tests raise `TypeError`/`NotImplementedError`); solution run → 11 passed.

- [ ] **Step 9: Run the solution module**

Run: `( cd lessons/06-classes && uv run python -m solutions.shapes )`
Expected (six lines):
```
Rectangle(width=3, height=4)
12
True
Point(x=1.0, y=2.0)
Point(x=3.0, y=5.0)
Point(x=5.0, y=6.0)
```

- [ ] **Step 10: Lint + format**

Run:
```bash
make lint
uv run ruff format lessons/06-classes
uv run ruff format --check .
```
Expected: `make lint` → "All checks passed!"; `ruff format` reports the lesson files already-formatted or formats them; `ruff format --check .` → no diff. If `ruff` rewrites anything, re-run Step 8 to confirm tests still pass.

- [ ] **Step 11: Commit**

```bash
git add lessons/06-classes uv.lock
git commit -m "feat(lesson-06): add class & dataclass drills (Rectangle by hand, Point via @dataclass)"
```
This commits the whole scaffolded lesson — including the placeholder `README.md` and `slides/` (with `slides/assets/.gitkeep`) — plus the authored `shapes.py`/`test_shapes.py` and the `uv.lock` workspace-member addition. The placeholder `README.md` and `slides/slides.md` ride along here and are **overwritten** in Tasks 2 and 3 (this mirrors Lesson 05 and keeps `assets/.gitkeep` and `index.html` tracked from the start). No `Co-Authored-By` trailer.

---

## Task 2: Author the lesson README

**Files:**
- Modify: `lessons/06-classes/README.md` (replace scaffold placeholder)

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current` → must be `lesson-06-classes`. If not, STOP.

- [ ] **Step 2: Overwrite `lessons/06-classes/README.md` with EXACTLY this content**

````markdown
# Lesson 06 — Classes & dataclasses

Define your own types: write a class by hand, then let `@dataclass` write the
boilerplate for you.

## Learning goals

- Define a class with `__init__` and methods, and understand what `self` is.
- Write `__repr__` and `__eq__` by hand to control how objects print and compare.
- Use `@dataclass` to generate `__init__`, `__repr__`, and `__eq__` automatically.
- Use a `@classmethod` as an alternative constructor.

## Prereqs

- [Lesson 01 — Hello](../01-hello/README.md)
- [Lesson 02 — Variables](../02-variables/README.md)
- [Lesson 03 — Control flow](../03-control-flow/README.md)
- [Lesson 04 — Functions](../04-functions/README.md)
- [Lesson 05 — Collections](../05-collections/README.md)

## Concepts

### Classes, `__init__`, and `self`

A **class** is a blueprint for objects that bundle **data** (attributes) with
**behavior** (methods). An **instance** is one object built from the class.

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
```

`__init__` runs when you call `Rectangle(3, 4)`. `self` is the instance being built;
`self.width = width` stores a value on it. Each instance has its own attributes.

### Methods

A **method** is a function defined in the class; its first parameter is `self`.

```python
    def area(self) -> float:
        return self.width * self.height
```

Call it on an instance: `Rectangle(3, 4).area()` is `12`.

### `__repr__`

Without `__repr__`, printing an object shows something like
`<Rectangle object at 0x10a…>`. Define it for a readable representation:

```python
    def __repr__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"
```

`repr(r)` and the REPL now show `Rectangle(width=3, height=4)`.

### `__eq__`

By default `==` compares **identity** (are these the same object?). Define `__eq__`
for **value** equality. Guard with `isinstance` so comparing to other types is safe:

```python
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Rectangle)
            and self.width == other.width
            and self.height == other.height
        )
```

Now `Rectangle(3, 4) == Rectangle(3, 4)` is `True`, and `Rectangle(3, 4) == "x"` is
`False`.

### `@dataclass`

Writing `__init__`/`__repr__`/`__eq__` by hand is repetitive. `@dataclass` generates
them from field declarations:

```python
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float
```

That is the whole class — `Point(1.0, 2.0)` works, `repr` gives `Point(x=1.0, y=2.0)`,
and two points with equal fields compare equal. Compare that to all of `Rectangle`
above.

### Dataclasses are still classes

A dataclass is an ordinary class — add methods and classmethods:

```python
    def translate(self, dx: float, dy: float) -> "Point":
        return Point(self.x + dx, self.y + dy)
```

`translate` returns a **new** `Point`; the original is untouched.

### Instance, class, and static methods

```python
class Point:
    def translate(self, dx, dy): ...        # instance method — takes self

    @classmethod
    def from_tuple(cls, coords):            # class method — takes cls
        return cls(coords[0], coords[1])

    @staticmethod
    def describe():                         # static method — takes neither
        return "a 2-D point"
```

A **`@classmethod`** receives the class as `cls` and is the usual way to write an
**alternative constructor**. A **`@staticmethod`** is just a function that lives in the
class's namespace. In the exercise you write the `from_tuple` classmethod.

### Simple inheritance

A class can build on another. A `Square` is a `Rectangle` with one side:

```python
class Square(Rectangle):
    def __init__(self, side: float) -> None:
        super().__init__(side, side)
```

`super().__init__(...)` calls the parent's `__init__`. `Square` inherits `area`,
`__repr__`, and `__eq__`. (Inheritance is shown here for understanding; it is not part
of the exercise.)

### Plain class vs dataclass — when to pick which

Reach for a **`@dataclass`** when the type is mostly a bundle of values (records,
configuration, results). Write a **plain class** when construction or behavior is
involved enough that the generated dunders would not fit.

## Exercise

Implement two classes in `exercises/shapes.py` so the tests pass:

- **`Rectangle`** — `__init__(width, height)`, `area()`, `__repr__`, and `__eq__`.
- **`Point`** — a `@dataclass`: declare the `x` and `y` float fields, then implement
  `translate(dx, dy)` (return a new `Point`) and the `from_tuple(coords)` classmethod.

The `Point` fields are left for you to declare — until you add them, `Point(1.0, 2.0)`
raises `TypeError`. Once declared, `@dataclass` gives you `__init__`/`__repr__`/`__eq__`
for free.

## How to run

From the repo root:

```bash
make test-lesson LESSON=06-classes
```

Or directly:

```bash
cd lessons/06-classes
uv run pytest exercises          # your work — fails until implemented
uv run pytest solutions          # the reference — passes
```

Run the module to see the demos (run the tests first — an unimplemented method raises
`NotImplementedError`):

```bash
cd lessons/06-classes
uv run python -m exercises.shapes
```

## Going further

- `@dataclass(frozen=True)` makes instances immutable (and hashable).
- Default field values: `count: int = 0`; for mutable defaults use
  `field(default_factory=list)`.
- `@dataclass(order=True)` generates `<`, `>`, … so instances sort; or write `__lt__`.
- Defining `__eq__` sets `__hash__` to `None` (the object becomes unhashable) unless you
  also define `__hash__` or use a frozen dataclass.
- Returning `NotImplemented` (not `False`) from `__eq__` lets the *other* operand try the
  comparison — the fully robust pattern.
- `@dataclass(slots=True)` stores fields in `__slots__` for lower memory use.
- `typing.Self` (Python 3.11+) can replace the `"Point"` forward-reference return type.
````

- [ ] **Step 3: Sanity-check the README**

Run:
```bash
grep -ic todo lessons/06-classes/README.md          # expect 0
grep -c '```' lessons/06-classes/README.md           # expect an even number (balanced fences)
```
Expected: `0` TODOs; an even fence count.

- [ ] **Step 4: Commit**

```bash
git add lessons/06-classes/README.md
git commit -m "docs(lesson-06): author the README (classes, dunders, @dataclass, classmethod)"
```
(No `Co-Authored-By` trailer.)

---

## Task 3: Author the slide deck

**Files:**
- Modify: `lessons/06-classes/slides/slides.md` (replace the template deck)
- Modify: `lessons/06-classes/slides/index.html` (deck `<title>` only — likely already correct)

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current` → must be `lesson-06-classes`. If not, STOP.

- [ ] **Step 2: Overwrite `lessons/06-classes/slides/slides.md` with EXACTLY this content**

````markdown
## Lesson 06
### Classes & dataclasses

Write a class by hand — then let `@dataclass` write the boilerplate.

Note:
Build Rectangle by hand, then Point with @dataclass and watch __init__/__repr__/__eq__ appear for free.

---

## Why classes

- An **object** bundles data (attributes) and behavior (methods)
- A **class** is the blueprint; an **instance** is one object
- You've used objects all along (`str`, `list`) — now you define your own

---

## Defining a class

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
```

- `__init__` runs on `Rectangle(3, 4)`
- `self` is the instance; `self.width = ...` stores an attribute

---

## Methods

```python
    def area(self) -> float:
        return self.width * self.height
```

```python
Rectangle(3, 4).area()   # 12
```

- A method is a function that takes `self`

---

## `__repr__`

```python
    def __repr__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"
```

- Without it: `<Rectangle object at 0x10a...>`
- With it: `Rectangle(width=3, height=4)`

---

## `__eq__`

```python
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Rectangle)
            and self.width == other.width
            and self.height == other.height
        )
```

- Default `==` compares identity; this compares values
- The `isinstance` guard keeps cross-type compares safe

---

## `@dataclass`

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

- Generates `__init__`, `__repr__`, `__eq__` for you
- All of Rectangle's boilerplate — for free

---

## Dataclasses are still classes

```python
    def translate(self, dx: float, dy: float) -> "Point":
        return Point(self.x + dx, self.y + dy)
```

- Add ordinary methods
- `translate` returns a NEW Point; the original is unchanged

---

## Method kinds

```python
    def translate(self, dx, dy): ...     # instance — takes self

    @classmethod
    def from_tuple(cls, coords):         # class — takes cls
        return cls(coords[0], coords[1])

    @staticmethod
    def describe(): ...                  # static — takes neither
```

- `@classmethod` → alternative constructor (you write this one)

---

## Inheritance

```python
class Square(Rectangle):
    def __init__(self, side: float) -> None:
        super().__init__(side, side)
```

- `Square` inherits `area`, `__repr__`, `__eq__`
- `super()` calls the parent (shown for understanding; not in the exercise)

---

## Your turn

- Implement `Rectangle` and `Point` in `exercises/shapes.py`
- Declare Point's `x`/`y` fields, then `translate` + `from_tuple`
- `make test-lesson LESSON=06-classes` until green
- Run it: `uv run python -m exercises.shapes`

---

## What's next

**Lesson 07 — Modules, packages, imports.**
````

- [ ] **Step 3: Fix the deck `<title>` in index.html**

The scaffolder derives the title from the **slug**, so it produces
`<title>Lesson 06 — Classes</title>`. Edit it to match the catalog name and the deck's
title slide — exactly:

```html
  <title>Lesson 06 — Classes & dataclasses</title>
```

Use a **literal `&`** (not `&amp;`) and an em-dash `—` (U+2014), matching Lesson 04's
`<title>Lesson 04 — Functions & tests</title>`. Do NOT change the `/shared/reveal/...`
asset paths.

- [ ] **Step 4: Build the site; confirm the lesson is a LINK and uses absolute asset paths**

Run: `make slides-build`
Expected: prints `built dist`.

Run:
```bash
grep -q 'href="lessons/06-classes/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
grep -oE '/shared/reveal|\.\./\.\./shared/reveal' dist/lessons/06-classes/slides/index.html | sort | uniq -c
test -f dist/lessons/06-classes/slides/index.html && test -f dist/lessons/06-classes/slides/slides.md && echo "SLIDES_COPIED"
```
Expected: `LINK_OK`; future-placeholder count is now `22`; the asset-path grep shows only `/shared/reveal` occurrences (NO `../../shared/reveal`); `SLIDES_COPIED`.

Run: `rm -rf dist`

- [ ] **Step 5: Dev-server smoke test**

```bash
( uv run python -m slides_dev --lesson 06-classes --repo-root "$(pwd)" --port 8000 & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
kill "$(lsof -ti:8000)" 2>/dev/null || true
```
Expected: the title line is `<title>Lesson 06 — Classes & dataclasses</title>`, `slidesmd=200`, `revealcss=200`. Confirm `lsof -ti:8000` is empty afterward.

- [ ] **Step 6: Commit**

```bash
git add lessons/06-classes/slides/slides.md lessons/06-classes/slides/index.html
git commit -m "feat(lesson-06): author the slide deck"
```
(No `Co-Authored-By` trailer. If only `slides.md` changed because the title was already correct, commit just that file.)

---

## Task 4: Final verification

End-to-end check. No new code unless something needs tidying.

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current`
Expected: `lesson-06-classes`. If not, STOP and report.

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
- `make typecheck` → Success (tools only).
- `make test` → tool suite passes; Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10), 06 (11) solutions all pass; exit 0; no `import file mismatch`.

- [ ] **Step 3: Lesson red/green + module**

```bash
make test-lesson LESSON=06-classes
( cd lessons/06-classes && uv run python -m solutions.shapes )
```
Expected: exercises FAIL (11; `NotImplementedError`/`TypeError`, tolerated), solutions PASS (11), exit 0; module prints the six demo lines (`Rectangle(width=3, height=4)`, `12`, `True`, `Point(x=1.0, y=2.0)`, `Point(x=3.0, y=5.0)`, `Point(x=5.0, y=6.0)`).

- [ ] **Step 4: Landing page link + git hygiene + no co-author trailers**

```bash
make slides-build
grep -q 'href="lessons/06-classes/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
rm -rf dist
git status --porcelain
git ls-files lessons/06-classes | sort
git log --oneline main..HEAD
git log main..HEAD --format='%B' | grep -i 'co-authored\|generated with' && echo "TRAILER FOUND (bad)" || echo "no trailers — good"
```
Expected: `LINK_OK`; future count `22`; clean working tree (no `dist/`); `lessons/06-classes` has `pyproject.toml`, `README.md`, `slides/{index.html,slides.md,assets/.gitkeep}`, `exercises/{__init__.py,shapes.py,test_shapes.py}`, `solutions/{__init__.py,shapes.py,test_shapes.py}` — NO `main.py`/`test_main.py`; 3 commits; `no trailers — good`.

- [ ] **Step 5: Confirm port clear**

```bash
lsof -ti:8000 || echo "port clear"
```
Expected: `port clear`.

- [ ] **Step 6: Commit only if Steps 1-5 surfaced changes**

If `git status` is clean, report CLEAN. If anything changed, investigate and commit (no co-author trailer); if a check FAILED, STOP and report BLOCKED.

---

## Notes for execution

- **Three commits** when done: `feat(lesson-06): add class & dataclass drills …`, `docs(lesson-06): author the README …`, `feat(lesson-06): author the slide deck`.
- **Mirror Lesson 05** for any shape question (`lessons/05-collections/`).
- **Never** add a `Co-Authored-By` / AI-attribution trailer.
- **Never** push or open a PR — the controller (subagent-driven-development) does branch finishing.
- The exercise's `Point` has no fields on purpose (red-start). Do not "fix" it by adding fields to the exercise.
- `make typecheck` covers `tools/` only; lesson code is not a mypy gate yet but must be `ruff`-clean.
```
