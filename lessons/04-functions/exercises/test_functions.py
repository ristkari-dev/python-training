import pytest

from exercises.functions import divmod_pair, power, tally, total


@pytest.fixture
def sample_numbers() -> tuple[float, ...]:
    """A few numbers reused across tests."""
    return (1.0, 2.0, 3.0, 4.0)


@pytest.mark.parametrize(
    "base, exp, expected",
    [
        (3.0, 2.0, 9.0),
        (2.0, 3.0, 8.0),
        (5.0, 0.0, 1.0),
        (2.0, 10.0, 1024.0),
    ],
)
def test_power(base: float, exp: float, expected: float) -> None:
    assert power(base, exp) == expected


def test_power_default_exp_squares() -> None:
    assert power(5.0) == 25.0


def test_power_keyword_arg() -> None:
    assert power(2.0, exp=3.0) == 8.0


def test_total_empty_is_zero() -> None:
    assert total() == 0.0


def test_total_sums_args() -> None:
    assert total(1.0, 2.0, 3.0) == 6.0


def test_total_with_fixture(sample_numbers: tuple[float, ...]) -> None:
    assert total(*sample_numbers) == 10.0


def test_tally_empty_is_zero() -> None:
    assert tally() == 0


def test_tally_sums_keyword_values() -> None:
    assert tally(apples=3, pears=2, plums=5) == 10


def test_divmod_pair_returns_quotient_and_remainder() -> None:
    assert divmod_pair(17, 5) == (3, 2)


def test_divmod_pair_exact_division() -> None:
    assert divmod_pair(10, 2) == (5, 0)
