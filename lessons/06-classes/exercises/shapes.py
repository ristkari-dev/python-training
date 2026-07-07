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
