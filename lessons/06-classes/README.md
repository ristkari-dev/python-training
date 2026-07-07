# Lesson 06 — Classes & dataclasses

Define your own types: write a class by hand, then let `@dataclass` write the
boilerplate for you.

## Learning goals

- Define a class with `__init__` and methods, and understand what `self` is.
- Write `__repr__` and `__eq__` by hand to control how objects print and compare.
- Use `@dataclass` to generate `__init__`, `__repr__`, and `__eq__` automatically.
- Use a `@classmethod` as an alternative constructor.

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md),
  [Lesson 02 — Variables, types, operators](../02-variables/README.md),
  [Lesson 03 — Control flow](../03-control-flow/README.md),
  [Lesson 04 — Functions & tests](../04-functions/README.md), and
  [Lesson 05 — Collections](../05-collections/README.md).

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
