## Lesson 02
### Variables, types, operators

Store values, pick the right type, combine them with operators.

Note:
We build a small temperature converter in the exercise.

---

## Variables

```python
freezing = 32.0
name = "Aki"
```

- A variable is a name bound to a value
- Names use `snake_case`
- Assignment binds the name; it does not copy

---

## The core types

- `int` — whole numbers: `42`
- `float` — decimals: `3.14`
- `str` — text: `"hello"`
- `bool` — `True` / `False`
- `None` — the "no value" value

`type(x)` tells you which one you have.

---

## Operators

```python
7 + 2    # 9
7 / 2    # 3.5   (always a float)
7 // 2   # 3     (floor division)
7 % 2    # 1     (remainder)
2 ** 10  # 1024  (power)
```

Comparisons (`== != < <= > >=`) return a `bool`.

---

## Conversions

```python
int("3")    # 3
float(3)    # 3.0
str(3)      # "3"
```

- Convert between types explicitly
- `input()` always returns a `str` — convert to compute

---

## f-strings

```python
celsius = 20.0
f"{celsius:.1f}°C"   # "20.0°C"
```

- `f"..."` builds a string from values
- A format spec after `:` controls display — `.1f` is one decimal

---

## bool & truthiness

- Comparisons return a real `bool`
- Falsy: `0`, `0.0`, `""`, `None`, empty collections
- Almost everything else is truthy

```python
bool(0)    # False
bool("hi") # True
```

---

## Constants by convention

```python
FREEZING_F = 32.0
```

- No `const` keyword in Python
- `UPPER_CASE` means "treat as constant"
- The language won't stop you — it's a convention

---

## Immutability intuition

```python
x = 1
x = x + 1   # new number, name rebound
```

- `int` and `str` are immutable
- Rebinding a name is not the same as mutating an object
- Mutable types (lists) arrive in Lesson 05

---

## Your turn

- Implement the four functions in `exercises/temperature.py`
- `make test-lesson LESSON=02-variables` until green
- Run it: `uv run python -m exercises.temperature`

---

## What's next

**Lesson 03 — Control flow.**
