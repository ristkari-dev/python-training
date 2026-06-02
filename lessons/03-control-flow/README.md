# Lesson 03 — Control flow

Make decisions with `if`/`elif`/`else` and repeat work with `for` and `while`
loops. By the end you will have written a grader, a vowel counter, and a
step-counter for the famous Collatz sequence.

## Learning goals

- Branch with `if`/`elif`/`else` and boolean operators (`and`, `or`, `not`)
- Write `for` loops over iterables (and `range`)
- Write `while` loops without creating an infinite loop
- Use `break`, `continue`, and early returns
- Recognise `match` and comprehensions (covered fully later)

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md) and
  [Lesson 02 — Variables, types, operators](../02-variables/README.md).

## Concepts

**Branching.** `if` runs a block when a condition is true; `elif` and `else`
handle the other cases. Conditions are the comparisons from Lesson 02
(`>=`, `==`, …), and you can combine them with `and`, `or`, and `not`.

**Early returns.** A function can `return` as soon as it knows the answer.
A chain of `if ...: return ...` is often clearer than deep nesting.

**`for` loops.** `for item in iterable:` runs the body once per item. Strings
are iterable (you get one character at a time), and `range(n)` gives the
numbers `0 .. n-1`. The `in` operator also tests membership: `"a" in "cat"`.

**`while` loops.** `while condition:` repeats until the condition becomes
false. Make sure something inside the loop changes toward the exit, or it
runs forever.

**`break` and `continue`.** `break` leaves the loop immediately; `continue`
skips to the next iteration.

**`match` (teaser).** Python's `match`/`case` is a cleaner multi-way branch.
We only glimpse it here.

**Comprehensions (intro).** `[n * 2 for n in numbers]` builds a list in one
line. Full treatment in Lesson 05.

## Exercise brief

Open `exercises/flow.py` and implement three functions so the tests pass:

- `letter_grade(score)` — `A` for `>= 90`, `B` for `>= 80`, `C` for `>= 70`,
  `D` for `>= 60`, otherwise `F` (use `if`/`elif`/`else`).
- `count_vowels(text)` — count the vowels in `text`, any case (use a `for`
  loop).
- `collatz_steps(n)` — count steps to reach 1: if `n` is even, `n // 2`,
  else `3 * n + 1`; `n == 1` takes 0 steps (use a `while` loop).

Run the tests first to watch them fail, then make them pass.

## How to run

Run the tests (exercises fail until you implement the functions; solutions pass):

```bash
make test-lesson LESSON=03-control-flow
```

Or directly:

```bash
cd lessons/03-control-flow && uv run pytest exercises
```

Run the module (prints a demo of all three; implement the functions first, or
it raises `NotImplementedError`):

```bash
cd lessons/03-control-flow && uv run python -m exercises.flow
```

## Going further

- `match`/`case`: rewrite a multi-way branch with structural pattern matching.
- Comprehensions: `[n for n in range(10) if n % 2 == 0]`.
- `enumerate(items)` gives `(index, item)` pairs; `zip(a, b)` pairs two
  iterables.
- The `for ... else` clause runs the `else` block if the loop finished without
  a `break`.
- Fun fact: whether *every* starting number's Collatz sequence reaches 1 is an
  unproven mathematical conjecture.
