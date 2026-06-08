def evens(numbers: list[int]) -> list[int]:
    """Return only the even numbers, in order (use a list comprehension)."""
    raise NotImplementedError("implement evens() so the tests pass")


def word_lengths(words: list[str]) -> dict[str, int]:
    """Map each word to its length (use a dict comprehension)."""
    raise NotImplementedError("implement word_lengths() so the tests pass")


def unique(items: list[int]) -> set[int]:
    """Return the distinct items as a set."""
    raise NotImplementedError("implement unique() so the tests pass")


def index_map(items: list[str]) -> dict[str, int]:
    """Map each item to its position, using enumerate."""
    raise NotImplementedError("implement index_map() so the tests pass")


def pair_up(names: list[str], scores: list[int]) -> list[tuple[str, int]]:
    """Pair each name with its score, using zip."""
    raise NotImplementedError("implement pair_up() so the tests pass")


if __name__ == "__main__":
    print(evens([1, 2, 3, 4, 5, 6]))  # [2, 4, 6]
    print(word_lengths(["hi", "world"]))  # {'hi': 2, 'world': 5}
    print(unique([3, 1, 2, 3, 1]))  # {1, 2, 3}
    print(index_map(["a", "b", "c"]))  # {'a': 0, 'b': 1, 'c': 2}
    print(pair_up(["ann", "bo"], [90, 85]))  # [('ann', 90), ('bo', 85)]
