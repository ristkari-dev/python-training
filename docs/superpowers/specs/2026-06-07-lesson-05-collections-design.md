# Lesson 05 — Collections — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-06-07
**Owner:** Aki Ristkari

## Summary

The fifth course lesson and the first where building `list`/`dict`/`set` values and using comprehensions are fair game (lessons 01–04 deliberately avoided them). Students implement five focused drills, each isolating one collection idiom: a filtering **list comprehension** (`evens`), a **dict comprehension** (`word_lengths`), a **set** dedup (`unique`), **`enumerate`** (`index_map`), and **`zip`** (`pair_up`). Set comprehensions, nested comprehensions, and conditional-in-comprehension forms are taught "in depth" on the slides/README but not graded. Fifth lesson, so `make test` now spans five lessons.

## Scope (from the course design spec)

Lesson 5: `list`/`tuple`/`dict`/`set` — methods, idioms, comprehensions in depth, `enumerate`/`zip`, when to pick which.

## Module naming

The lesson module is **`containers.py`** (and tests `test_containers.py`), NOT `collections.py`. Naming it `collections.py` would invite confusion with the standard library's `collections` module; `containers.py` ("container types") is unambiguous. Import paths: `from exercises.containers import ...` / `from solutions.containers import ...`.

## Exercise — five idiom drills

Each function isolates one collection/iteration idiom. Bodies are one-liners; the teaching point is the idiom, not algorithmic complexity.

### Functions

- `evens(numbers: list[int]) -> list[int]` — a **list comprehension with a filter**: `[n for n in numbers if n % 2 == 0]`. Order-preserving.
- `word_lengths(words: list[str]) -> dict[str, int]` — a **dict comprehension**: `{word: len(word) for word in words}`.
- `unique(items: list[int]) -> set[int]` — the **`set(...)` constructor** for dedup: `set(items)`.
- `index_map(items: list[str]) -> dict[str, int]` — **`enumerate`** inside a dict comprehension: `{item: i for i, item in enumerate(items)}`.
- `pair_up(names: list[str], scores: list[int]) -> list[tuple[str, int]]` — **`zip`**: `list(zip(names, scores))`.

### Coverage mapping

- **list (+ list comprehension + filter)** — `evens`.
- **dict (+ dict comprehension)** — `word_lengths`, `index_map`.
- **set** — `unique`.
- **tuple** — appears as the element type of `pair_up`'s result.
- **`enumerate`** — `index_map`.
- **`zip`** — `pair_up`.
- **set comprehensions, nested comprehensions, conditional expressions in comprehensions, "when to pick which"** — taught on the slides + README; not graded. (`unique` uses the idiomatic `set(...)` constructor; a set comprehension shines for transforming, e.g. `{len(w) for w in words}`, which is a slides example.)

### `exercises/containers.py` (stub)

```python
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
    print(evens([1, 2, 3, 4, 5, 6]))          # [2, 4, 6]
    print(word_lengths(["hi", "world"]))      # {'hi': 2, 'world': 5}
    print(unique([3, 1, 2, 3, 1]))            # {1, 2, 3}
    print(index_map(["a", "b", "c"]))         # {'a': 0, 'b': 1, 'c': 2}
    print(pair_up(["ann", "bo"], [90, 85]))   # [('ann', 90), ('bo', 85)]
```

### `solutions/containers.py`

```python
def evens(numbers: list[int]) -> list[int]:
    """Return only the even numbers, in order (use a list comprehension)."""
    return [n for n in numbers if n % 2 == 0]


def word_lengths(words: list[str]) -> dict[str, int]:
    """Map each word to its length (use a dict comprehension)."""
    return {word: len(word) for word in words}


def unique(items: list[int]) -> set[int]:
    """Return the distinct items as a set."""
    return set(items)


def index_map(items: list[str]) -> dict[str, int]:
    """Map each item to its position, using enumerate."""
    return {item: i for i, item in enumerate(items)}


def pair_up(names: list[str], scores: list[int]) -> list[tuple[str, int]]:
    """Pair each name with its score, using zip."""
    return list(zip(names, scores))


if __name__ == "__main__":
    print(evens([1, 2, 3, 4, 5, 6]))          # [2, 4, 6]
    print(word_lengths(["hi", "world"]))      # {'hi': 2, 'world': 5}
    print(unique([3, 1, 2, 3, 1]))            # {1, 2, 3}
    print(index_map(["a", "b", "c"]))         # {'a': 0, 'b': 1, 'c': 2}
    print(pair_up(["ann", "bo"], [90, 85]))   # [('ann', 90), ('bo', 85)]
```

The `__main__` block is non-interactive; it prints the five demo lines once implemented (running it before implementing raises `NotImplementedError` — expected; the README says run the tests first).

### Tests (`exercises/test_containers.py` / `solutions/test_containers.py`)

Identical except the import line. Ten tests, all deterministic — `dict`/`set` equality is content-based (order-independent), and list/comprehension results preserve order.

```python
from solutions.containers import evens, index_map, pair_up, unique, word_lengths


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
```

The solutions copy is identical except the first line reads `from solutions.containers import evens, index_map, pair_up, unique, word_lengths`.

## Files

`lessons/05-collections/` (scaffold with `make new-lesson NAME=05-collections`, then author; replace the placeholder `main.py`/`test_main.py` with `containers.py`/`test_containers.py`):

```
lessons/05-collections/
├── pyproject.toml          # name "lesson-05-collections", package=false, pytest pythonpath=["."]
├── README.md               # authored
├── slides/
│   ├── index.html          # scaffold; <title> set to "Lesson 05 — Collections"; absolute /shared/reveal paths (already correct)
│   ├── slides.md           # authored
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py         # empty (kept)
│   ├── containers.py
│   └── test_containers.py
└── solutions/
    ├── __init__.py         # empty
    ├── containers.py
    └── test_containers.py
```

## Slides (`slides/slides.md`)

About twelve slides, `---` separated, code in fenced `python` blocks, ~15 visible lines max. `Note:` speaker notes where useful.

1. **Title** — "Lesson 05 — Collections" + one-line goal.
2. **The four containers** — `list` (ordered, mutable), `tuple` (ordered, immutable), `dict` (key → value), `set` (unordered, unique); a one-line "when to pick which".
3. **list** — create, index, slice, `append`; ordered and mutable.
4. **tuple** — immutable; packing/unpacking; good for fixed-shape records and dict keys.
5. **dict** — create, look up, `.get(key, default)`, `.items()`, iterate.
6. **set** — membership (`in`), dedup, operations (`|`, `&`, `-`).
7. **List comprehension** — `[n for n in numbers if n % 2 == 0]` (the `evens` shape).
8. **Dict comprehension** — `{word: len(word) for word in words}` (the `word_lengths` shape).
9. **Set & nested comprehensions** — `{len(w) for w in words}`; a nested `[x for row in grid for x in row]`; a conditional expression `[x if x > 0 else 0 for x in xs]`. (In depth; not in the graded exercise.)
10. **enumerate** — `for i, item in enumerate(items)`; the `index_map` shape.
11. **zip** — `for a, b in zip(xs, ys)`; `list(zip(...))`; mention `zip(xs, ys, strict=True)`.
12. **When to pick which + your turn + what's next** — quick decision guide; implement the five functions; pointer to Lesson 06 — Classes & dataclasses.

## README (`README.md`)

Four-file-convention sections:

- **Learning goals** — recognise the four built-in containers and when to use each; build lists/dicts/sets with comprehensions; use `enumerate` to get indices and `zip` to pair iterables.
- **Prereqs** — Lessons 01, 02, 03, 04.
- **Concepts** — `list` (ordered, mutable; index, slice, `append`); `tuple` (immutable; packing/unpacking; valid dict keys); `dict` (key → value; `.get`, `.items`, iteration); `set` (unordered, unique; membership; `| & -`); comprehensions in depth (list with filter; dict; set; nested; conditional expression); `enumerate` (index + item); `zip` (pair iterables; `strict=True`); a short "when to pick which" guide.
- **Exercise brief** — implement `evens`, `word_lengths`, `unique`, `index_map`, and `pair_up` in `exercises/containers.py` so the tests pass.
- **How to run** — `make test-lesson LESSON=05-collections` (or `cd lessons/05-collections && uv run pytest exercises`); run the module `cd lessons/05-collections && uv run python -m exercises.containers`. Run the tests before the module (an unimplemented function raises `NotImplementedError`).
- **Going further** — `collections.Counter` and `defaultdict`; full set operations (`& | - ^`); `zip(strict=True)` to catch length mismatches; `frozenset`; `dict.get`/`dict.setdefault`; a teaser that ordering (`sorted`) is coming.

## Verification (success criteria)

- `make test-lesson LESSON=05-collections` → exercise tests FAIL with `NotImplementedError`; solution tests PASS (10); target exit 0.
- `make test` → tools + Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10) solutions all pass, in isolated per-lesson processes; no `import file mismatch`. (Now spans five lessons.)
- `cd lessons/05-collections && uv run python -m solutions.containers` → prints the five demo lines (`[2, 4, 6]`, `{'hi': 2, 'world': 5}`, `{1, 2, 3}`, `{'a': 0, 'b': 1, 'c': 2}`, `[('ann', 90), ('bo', 85)]`).
- `make slides-build` → `dist/index.html` shows `05-collections` as a link (no longer faded); future-placeholder count drops from 24 to 23; the built deck uses absolute `/shared/reveal/...` asset paths; the deck renders in a browser (multiple slides, no `/shared/reveal` 404s).
- `make lint` and `uv run ruff format --check .` → clean. `make typecheck` stays scoped to tools and remains clean; lesson code is cleanly typed but not a typecheck gate (strict lesson typing starts at Lesson 09).
- The deck renders via `make slides-dev LESSON=05-collections`.

## Non-goals

- No graded set comprehension or nested comprehension — slides/README only.
- No sorting (`sorted`, `.sort`, `key=`) — teaser only; sorting is not yet a lesson topic.
- No `collections` module types (`Counter`, `defaultdict`) in the graded exercise — going-further only.
- The module is named `containers.py`, never `collections.py` (avoid stdlib shadowing/confusion).
- No catalog change — `05-collections` is already listed in `tools/build_index/src/build_index/catalog.py`.
- No tooling/harness changes. No strict mypy gate on lesson code (starts Lesson 09); the code is nonetheless cleanly typed.

## Open items deferred to implementation planning

- Exact slide prose and README concept wording.
- Whether the deck's `index.html` `<title>` is hand-edited to "Lesson 05 — Collections" (default: yes, matching prior lessons).
