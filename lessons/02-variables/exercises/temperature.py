FREEZING_F = 32.0  # water freezes at 32°F / 0°C


def to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius."""
    raise NotImplementedError("implement to_celsius() so the tests pass")


def to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    raise NotImplementedError("implement to_fahrenheit() so the tests pass")


def format_temp(celsius: float) -> str:
    """Format a Celsius temperature to one decimal place, e.g. "20.0°C"."""
    raise NotImplementedError("implement format_temp() so the tests pass")


def is_freezing(celsius: float) -> bool:
    """Return True if the temperature is at or below freezing (0°C)."""
    raise NotImplementedError("implement is_freezing() so the tests pass")


if __name__ == "__main__":
    # Body temperature: 98.6°F in Celsius, formatted.
    print(format_temp(to_celsius(98.6)))
