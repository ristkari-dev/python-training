# Lesson 02 — Variables, types, operators

Store values in variables, work with Python's core types, and combine them
with operators. By the end you will have built a small temperature converter
and learned why `1 / 2` is `0.5` but `1 // 2` is `0`.

## Learning goals

- Assign values to variables and name them well (`snake_case`)
- Recognise the core built-in types: `int`, `float`, `str`, `bool`, `None`
- Use arithmetic and comparison operators, including `/` versus `//`
- Format values with f-strings (`f"{x:.1f}"`)
- Understand truthiness and "constants by convention"

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md).

## Concepts

**Variables.** A variable is a name bound to a value: `freezing = 32.0`. Names
use `snake_case`. Assignment binds the name; it does not copy.

**The core types.** `int` (whole numbers), `float` (decimals), `str` (text),
`bool` (`True`/`False`), and `None` (the "no value" value). `type(x)` tells you
which one you have.

**Operators.** Arithmetic: `+ - * / // % **`. Note that `/` always produces a
`float` (`6 / 2` is `3.0`), `//` floors to an `int`-like result (`7 // 2` is
`3`), `%` is the remainder, and `**` is power. Comparisons (`== != < <= > >=`)
produce a `bool`.

**Conversions.** Convert between types explicitly: `int("3")`, `float(3)`,
`str(3)`. Reading user input (`input()`) always gives a `str`, so you convert
when you need a number.

**f-strings.** Build strings from values: `f"Hello, {name}!"`. A format spec
after a colon controls the display: `f"{value:.1f}"` shows one decimal place.

**Truthiness.** Any value can be tested for truth. Falsy values include `0`,
`0.0`, `""`, `None`, and empty collections; almost everything else is truthy.
Comparisons already return a real `bool`.

**Constants by convention.** Python has no `const` keyword. A name in
`UPPER_CASE` (like `FREEZING_F = 32.0`) signals "treat this as a constant" —
the language won't stop you reassigning it, but you shouldn't.

**Immutability intuition.** `int` and `str` values are immutable: `x = x + 1`
makes a new number and rebinds the name `x` — it does not change the original
object. (Mutable types like lists arrive in Lesson 05.)

## Exercise brief

Open `exercises/temperature.py` and implement four functions so the tests pass:
`to_celsius`, `to_fahrenheit`, `format_temp` (one decimal place, like
`"20.0°C"`), and `is_freezing` (at or below 0°C). A `FREEZING_F = 32.0` constant
is provided for you to use. Run the tests first to watch them fail, then make
them pass.

## How to run

Run the tests (exercises fail until you implement the functions; solutions pass):

```bash
make test-lesson LESSON=02-variables
```

Or directly:

```bash
cd lessons/02-variables && uv run pytest exercises
```

Run the module (prints a composed conversion; implement the functions first, or
it raises `NotImplementedError`):

```bash
cd lessons/02-variables && uv run python -m exercises.temperature
```

## Going further

- `divmod(17, 5)` returns `(3, 2)` — quotient and remainder at once.
- Floats are approximate: try `0.1 + 0.2` in the REPL (`uv run python`) — it is
  not exactly `0.3`. For exact money math, look at `decimal.Decimal`.
- Explore more f-string format specs: `f"{1234567:,}"`, `f"{0.25:.0%}"`,
  `f"{42:>6}"` (width and alignment).
