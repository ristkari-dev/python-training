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
    print(r)  # Rectangle(width=3, height=4)
    print(r.area())  # 12
    print(r == Rectangle(3, 4))  # True
    p = Point(1.0, 2.0)
    print(p)  # Point(x=1.0, y=2.0)
    print(p.translate(2.0, 3.0))  # Point(x=3.0, y=5.0)
    print(Point.from_tuple((5.0, 6.0)))  # Point(x=5.0, y=6.0)
