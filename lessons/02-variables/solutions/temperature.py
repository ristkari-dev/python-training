FREEZING_F = 32.0  # water freezes at 32°F / 0°C


def to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius."""
    return (fahrenheit - FREEZING_F) * 5 / 9


def to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * 9 / 5 + FREEZING_F


def format_temp(celsius: float) -> str:
    """Format a Celsius temperature to one decimal place, e.g. "20.0°C"."""
    return f"{celsius:.1f}°C"


def is_freezing(celsius: float) -> bool:
    """Return True if the temperature is at or below freezing (0°C)."""
    return celsius <= 0


if __name__ == "__main__":
    # Body temperature: 98.6°F in Celsius, formatted.
    print(format_temp(to_celsius(98.6)))
