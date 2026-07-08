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
