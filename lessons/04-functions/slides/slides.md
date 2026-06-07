## Lesson 04
### Functions & tests

Arguments, defaults, *args/**kwargs, tuples — and how pytest works.

Note:
Two threads: function calling conventions, then pytest demystified.

---

## Defining functions

```python
def power(base: float, exp: float) -> float:
    return base ** exp
```

- We've written functions since Lesson 01
- `def name(params) -> return_type:`

---

## Positional & keyword args

```python
power(2.0, 3.0)        # positional
power(2.0, exp=3.0)    # keyword
```

- Position order matters; keywords name the parameter
- Keywords can make a call clearer

---

## Default arguments

```python
def power(base: float, exp: float = 2.0) -> float:
    return base ** exp

power(5.0)   # 25.0  — exp defaults to 2
```

- Omit an argument to use its default
- Defaults are evaluated once — never use a mutable default

---

## *args

```python
def total(*numbers: float) -> float:
    return sum(numbers)

total(1.0, 2.0, 3.0)   # 6.0
```

- `*args` collects extra positional args into a **tuple**

---

## **kwargs

```python
def tally(**counts: int) -> int:
    return sum(counts.values())

tally(apples=3, pears=2)   # 5
```

- `**kwargs` collects extra keyword args into a **dict**

---

## Returning tuples

```python
def divmod_pair(a: int, b: int) -> tuple[int, int]:
    return a // b, a % b

q, r = divmod_pair(17, 5)   # q=3, r=2
```

- Commas build a tuple; the caller can unpack it

---

## The magic, explained

```bash
uv run pytest
```

- pytest finds `test_*.py` files and `test_*` functions
- runs each and reports pass/fail

---

## assert

```python
def test_power_squares() -> None:
    assert power(5.0) == 25.0
```

- A failing `assert` prints both sides — you see what went wrong

---

## parametrize

```python
@pytest.mark.parametrize("base, exp, expected", [
    (3.0, 2.0, 9.0),
    (2.0, 3.0, 8.0),
])
def test_power(base, exp, expected) -> None:
    assert power(base, exp) == expected
```

- One test body, many cases (`pytest -v` lists each)

---

## fixtures

```python
@pytest.fixture
def sample_numbers() -> tuple[float, ...]:
    return (1.0, 2.0, 3.0, 4.0)

def test_total(sample_numbers) -> None:
    assert total(*sample_numbers) == 10.0
```

- pytest injects a fixture into any test that names it

---

## Your turn

- Implement the four functions in `exercises/functions.py`
- `make test-lesson LESSON=04-functions` until green
- Read `test_functions.py` — that's pytest, no longer magic

---

## What's next

**Lesson 05 — Collections.**
