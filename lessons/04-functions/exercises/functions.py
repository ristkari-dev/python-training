def power(base: float, exp: float = 2.0) -> float:
    """Return base raised to exp. exp defaults to 2 (squaring)."""
    raise NotImplementedError("implement power() so the tests pass")


def total(*numbers: float) -> float:
    """Return the sum of all the numbers (0.0 if none)."""
    raise NotImplementedError("implement total() so the tests pass")


def tally(**counts: int) -> int:
    """Return the sum of all the keyword values (0 if none)."""
    raise NotImplementedError("implement tally() so the tests pass")


def divmod_pair(a: int, b: int) -> tuple[int, int]:
    """Return (quotient, remainder) of a divided by b."""
    raise NotImplementedError("implement divmod_pair() so the tests pass")


if __name__ == "__main__":
    print(power(5.0))  # 25.0
    print(total(1.0, 2.0, 3.0))  # 6.0
    print(tally(apples=3, pears=2))  # 5
    print(divmod_pair(17, 5))  # (3, 2)
