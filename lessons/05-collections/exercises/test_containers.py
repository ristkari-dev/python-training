from exercises.containers import evens, index_map, pair_up, unique, word_lengths


def test_evens_filters_odds() -> None:
    assert evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]


def test_evens_empty() -> None:
    assert evens([]) == []


def test_evens_preserves_order() -> None:
    assert evens([6, 5, 4, 3, 2, 1]) == [6, 4, 2]


def test_word_lengths() -> None:
    assert word_lengths(["hi", "world"]) == {"hi": 2, "world": 5}


def test_word_lengths_empty() -> None:
    assert word_lengths([]) == {}


def test_unique_dedups() -> None:
    assert unique([3, 1, 2, 3, 1]) == {1, 2, 3}


def test_unique_empty() -> None:
    assert unique([]) == set()


def test_index_map() -> None:
    assert index_map(["a", "b", "c"]) == {"a": 0, "b": 1, "c": 2}


def test_pair_up() -> None:
    assert pair_up(["ann", "bo"], [90, 85]) == [("ann", 90), ("bo", 85)]


def test_pair_up_empty() -> None:
    assert pair_up([], []) == []
