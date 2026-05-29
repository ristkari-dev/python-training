from solutions.temperature import (
    format_temp,
    is_freezing,
    to_celsius,
    to_fahrenheit,
)


def test_to_celsius_freezing() -> None:
    assert to_celsius(32.0) == 0.0


def test_to_celsius_boiling() -> None:
    assert to_celsius(212.0) == 100.0


def test_to_fahrenheit_freezing() -> None:
    assert to_fahrenheit(0.0) == 32.0


def test_to_fahrenheit_boiling() -> None:
    assert to_fahrenheit(100.0) == 212.0


def test_round_trip_is_exact_for_boiling() -> None:
    assert to_fahrenheit(to_celsius(212.0)) == 212.0


def test_format_temp_one_decimal() -> None:
    assert format_temp(37.0) == "37.0°C"


def test_format_temp_negative() -> None:
    assert format_temp(-12.5) == "-12.5°C"


def test_is_freezing_at_zero() -> None:
    assert is_freezing(0.0) is True


def test_is_freezing_below() -> None:
    assert is_freezing(-5.0) is True


def test_is_freezing_above() -> None:
    assert is_freezing(10.0) is False
