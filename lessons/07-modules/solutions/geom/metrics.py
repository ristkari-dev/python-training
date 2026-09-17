import math

from solutions.geom.points import Point


def distance(a: Point, b: Point) -> float:
    """Return the straight-line distance between a and b."""
    return math.hypot(a.x - b.x, a.y - b.y)
