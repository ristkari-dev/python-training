from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


def midpoint(a: Point, b: Point) -> Point:
    """Return the point halfway between a and b."""
    raise NotImplementedError("implement midpoint() so the tests pass")
