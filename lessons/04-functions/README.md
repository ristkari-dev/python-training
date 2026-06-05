# Lesson 04 — Functions & tests

Define functions that take positional, keyword, default, and variadic
arguments — and finally see how `pytest`, the "magic test runner" from the
first three lessons, actually works.

## Learning goals

- Pass arguments positionally and by keyword, and give parameters defaults
- Gather extra arguments with `*args` (a tuple) and `**kwargs` (a dict)
- Return multiple values as a tuple, and unpack them
- Understand how `pytest` discovers and runs tests
- Read `assert`, `@pytest.mark.parametrize`, and `@pytest.fixture`

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md),
  [Lesson 02 — Variables, types, operators](../02-variables/README.md), and
  [Lesson 03 — Control flow](../03-control-flow/README.md).

## Concepts

**Arguments.** A call passes arguments to a function's parameters. You can pass
them by position (`power(2, 3)`) or by keyword (`power(2, exp=3)`). A parameter
with a default may be omitted: `def power(base, exp=2.0)` lets `power(5)` mean
"square it". (Defaults are evaluated once, when the function is defined — so
never use a mutable default like `[]`.)

**`*args` and `**kwargs`.** A `*args` parameter collects any extra positional
arguments into a **tuple**: `def total(*numbers)` makes `total(1, 2, 3)` see
`numbers == (1, 2, 3)`. A `**kwargs` parameter collects any extra keyword
arguments into a **dict**: `def tally(**counts)` makes `tally(apples=3)` see
`counts == {"apples": 3}`.

**Returning tuples.** A function can return several values as a tuple just by
separating them with commas: `return a // b, a % b`. The caller can unpack
them: `q, r = divmod_pair(17, 5)`.

**How `pytest` works.** When you run `pytest`, it discovers files named
`test_*.py` and functions named `test_*`, runs each one, and reports the
results. An `assert` that fails stops that test and prints both sides of the
comparison, so you see exactly what went wrong.

**`parametrize`.** `@pytest.mark.parametrize("a, b, expected", [...])` runs the
same test body once per row of inputs — many cases, one function. Run pytest
with `-v` to see each case listed separately.

**`fixtures`.** A function decorated with `@pytest.fixture` provides reusable
setup or data. Any test that names the fixture in its parameter list receives
its return value — pytest injects it automatically, so several tests can share
one definition instead of repeating the setup. This lesson's tests use a
`sample_numbers` fixture.

Open `exercises/test_functions.py` — it uses a fixture and a parametrized test.
That is the machinery that has been checking your work since Lesson 01.

## Exercise brief

Open `exercises/functions.py` and implement four functions so the tests pass:

- `power(base, exp=2.0)` — `base` raised to `exp`; `exp` defaults to 2.
- `total(*numbers)` — the sum of all the numbers (`0.0` if none).
- `tally(**counts)` — the sum of all the keyword values (`0` if none).
- `divmod_pair(a, b)` — the tuple `(a // b, a % b)`.

Run the tests first to watch them fail, then make them pass.

## How to run

Run the tests (exercises fail until you implement the functions; solutions pass):

```bash
make test-lesson LESSON=04-functions
```

Or directly, with `-v` to see each parametrized case:

```bash
cd lessons/04-functions && uv run pytest exercises -v
```

Run the module (prints a demo of all four; implement the functions first, or
it raises `NotImplementedError`):

```bash
cd lessons/04-functions && uv run python -m exercises.functions
```

## Going further

- Keyword-only parameters: `def f(*, key)`. Positional-only: `def f(x, /)`.
- The built-in `divmod(a, b)` returns the same tuple as `divmod_pair`.
- The mutable-default gotcha: `def f(items=[])` reuses one list across calls —
  use `def f(items=None)` and create a new list inside instead.
- pytest flags: `-k name` selects tests by name, `-x` stops on the first
  failure, `-q` is quiet.
