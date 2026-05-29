from exercises.hello import greet


def test_greets_by_name() -> None:
    assert greet("Aki") == "Hello, Aki!"


def test_greets_anyone() -> None:
    assert greet("world") == "Hello, world!"
