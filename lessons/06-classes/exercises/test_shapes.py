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
