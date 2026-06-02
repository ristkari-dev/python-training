from solutions.flow import collatz_steps, count_vowels, letter_grade


def test_grade_a() -> None:
    assert letter_grade(95) == "A"


def test_grade_a_boundary() -> None:
    assert letter_grade(90) == "A"


def test_grade_b_boundary() -> None:
    assert letter_grade(80) == "B"


def test_grade_c() -> None:
    assert letter_grade(72) == "C"


def test_grade_d_boundary() -> None:
    assert letter_grade(60) == "D"


def test_grade_f() -> None:
    assert letter_grade(40) == "F"


def test_count_vowels_basic() -> None:
    assert count_vowels("hello") == 2


def test_count_vowels_mixed_case() -> None:
    assert count_vowels("AEIOU xyz") == 5


def test_count_vowels_none() -> None:
    assert count_vowels("rhythm") == 0


def test_collatz_one() -> None:
    assert collatz_steps(1) == 0


def test_collatz_two() -> None:
    assert collatz_steps(2) == 1


def test_collatz_three() -> None:
    assert collatz_steps(3) == 7


def test_collatz_sixteen() -> None:
    assert collatz_steps(16) == 4
