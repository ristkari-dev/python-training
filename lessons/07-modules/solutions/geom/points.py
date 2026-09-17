from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


def midpoint(a: Point, b: Point) -> Point:
    """Return the point halfway between a and b."""
    return Point((a.x + b.x) / 2, (a.y + b.y) / 2)
