from solutions.geom import Point, distance, midpoint


def test_point_is_reexported() -> None:
    assert Point(1.0, 2.0) == Point(1.0, 2.0)


def test_midpoint() -> None:
    assert midpoint(Point(0.0, 0.0), Point(4.0, 6.0)) == Point(2.0, 3.0)


def test_midpoint_negative() -> None:
    assert midpoint(Point(-2.0, -4.0), Point(2.0, 4.0)) == Point(0.0, 0.0)


def test_midpoint_same_point() -> None:
    p = Point(3.0, 5.0)
    assert midpoint(p, p) == p


def test_distance() -> None:
    assert distance(Point(0.0, 0.0), Point(3.0, 4.0)) == 5.0


def test_distance_same_point() -> None:
    assert distance(Point(1.0, 1.0), Point(1.0, 1.0)) == 0.0


def test_distance_is_symmetric() -> None:
    a, b = Point(0.0, 0.0), Point(3.0, 4.0)
    assert distance(a, b) == distance(b, a)
