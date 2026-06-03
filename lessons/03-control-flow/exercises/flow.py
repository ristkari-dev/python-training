def letter_grade(score: int) -> str:
    """Return the letter grade for a score: A>=90, B>=80, C>=70, D>=60, else F."""
    raise NotImplementedError("implement letter_grade() so the tests pass")


def count_vowels(text: str) -> int:
    """Count the vowels (a, e, i, o, u — any case) in text."""
    raise NotImplementedError("implement count_vowels() so the tests pass")


def collatz_steps(n: int) -> int:
    """Count steps to reach 1 under the Collatz rule. n == 1 returns 0."""
    raise NotImplementedError("implement collatz_steps() so the tests pass")


if __name__ == "__main__":
    print(letter_grade(85))  # B
    print(count_vowels("hello"))  # 2
    print(collatz_steps(27))  # 111
