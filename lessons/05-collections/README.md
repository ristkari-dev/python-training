# Lesson 05 — Collections

Group values with Python's four built-in containers — `list`, `tuple`, `dict`,
and `set` — and build them concisely with comprehensions. By the end you will
have written a list, a dict, and a set, and used `enumerate` and `zip`.

## Learning goals

- Recognise the four built-in containers and when to use each
- Build lists, dicts, and sets with comprehensions
- Filter inside a comprehension (`[x for x in xs if ...]`)
- Use `enumerate` to get index + item, and `zip` to pair iterables

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md),
  [Lesson 02 — Variables, types, operators](../02-variables/README.md),
  [Lesson 03 — Control flow](../03-control-flow/README.md), and
  [Lesson 04 — Functions & tests](../04-functions/README.md).

## Concepts

**The four containers.**

- `list` — an ordered, mutable sequence: `[1, 2, 3]`. Index (`xs[0]`), slice
  (`xs[1:3]`), and append (`xs.append(4)`).
- `tuple` — an ordered, **immutable** sequence: `(1, 2)`. Good for fixed-shape
  records and as `dict` keys. Unpack with `a, b = pair`.
- `dict` — a mapping of keys to values: `{"a": 1}`. Look up with `d["a"]` or the
  safer `d.get("a", default)`; iterate pairs with `d.items()`.
- `set` — an unordered collection of **unique** values: `{1, 2}`. Fast
  membership (`x in s`); set operations (`|` union, `&` intersection, `-`
  difference).

**Comprehensions.** A comprehension builds a collection in one expression:

- list: `[n for n in numbers if n % 2 == 0]` (the `if` filters)
- dict: `{word: len(word) for word in words}`
- set: `{len(w) for w in words}` (deduplicates as it builds)

They can nest (`[x for row in grid for x in row]`) and use a conditional
expression for the value (`[x if x > 0 else 0 for x in xs]`).

**`enumerate`.** `for i, item in enumerate(items)` gives you the index and the
item together — no manual counter.

**`zip`.** `zip(names, scores)` pairs two iterables element by element;
`list(zip(...))` materialises a list of tuples. Pass `strict=True` to require
equal lengths (it raises if they differ) — a good default.

**When to pick which.** Ordered and changing? `list`. Fixed and unchanging?
`tuple`. Looking things up by key? `dict`. Membership or dedup? `set`.

## Exercise brief

Open `exercises/containers.py` and implement five functions so the tests pass:

- `evens(numbers)` — the even numbers, in order (list comprehension).
- `word_lengths(words)` — `{word: len(word)}` (dict comprehension).
- `unique(items)` — the distinct items as a `set`.
- `index_map(items)` — `{item: position}` using `enumerate`.
- `pair_up(names, scores)` — a list of `(name, score)` tuples using `zip`.

Run the tests first to watch them fail, then make them pass.

## How to run

Run the tests (exercises fail until you implement the functions; solutions pass):

```bash
make test-lesson LESSON=05-collections
```

Or directly:

```bash
cd lessons/05-collections && uv run pytest exercises
```

Run the module (prints a demo of all five; implement the functions first, or
it raises `NotImplementedError`):

```bash
cd lessons/05-collections && uv run python -m exercises.containers
```

## Going further

- `collections.Counter(items)` tallies occurrences; `collections.defaultdict`
  gives missing keys a default.
- Full set operations: union `|`, intersection `&`, difference `-`, symmetric
  difference `^`. `frozenset` is an immutable set.
- `zip(a, b, strict=True)` raises if the iterables differ in length — catching
  a common bug where one list is shorter than the other.
- `dict.get(key, default)` and `dict.setdefault(key, default)` handle missing
  keys gracefully.
- Ordering with `sorted(...)` is coming in a later lesson.
