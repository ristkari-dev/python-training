def letter_grade(score: int) -> str:
    """Return the letter grade for a score: A>=90, B>=80, C>=70, D>=60, else F."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def count_vowels(text: str) -> int:
    """Count the vowels (a, e, i, o, u — any case) in text."""
    count = 0
    for char in text:
        if char in "aeiouAEIOU":
            count += 1
    return count


def collatz_steps(n: int) -> int:
    """Count steps to reach 1 under the Collatz rule. n == 1 returns 0."""
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


if __name__ == "__main__":
    print(letter_grade(85))  # B
    print(count_vowels("hello"))  # 2
    print(collatz_steps(27))  # 111
