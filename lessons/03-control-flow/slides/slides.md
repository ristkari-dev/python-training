## Lesson 03
### Control flow

Make decisions, repeat work, know when to stop.

Note:
Three drills: a grader (if/elif/else), a vowel counter (for), a Collatz
step-counter (while).

---

## if / elif / else

```python
if score >= 90:
    return "A"
elif score >= 80:
    return "B"
else:
    return "F"
```

- `if` runs when the condition is true
- `elif` / `else` handle the rest

---

## Boolean operators

```python
if score >= 60 and not late:
    return "pass"
```

- `and`, `or`, `not` combine conditions
- Comparisons (`>=`, `==`, …) produce a `bool`

---

## Early returns

```python
def grade(score: int) -> str:
    if score < 60:
        return "F"
    return "pass"
```

- Return as soon as the answer is known
- Often clearer than deep nesting

---

## for loops

```python
for char in "hello":
    print(char)

for i in range(3):   # 0, 1, 2
    print(i)
```

- `for x in iterable:` runs once per item
- strings are iterable; `range(n)` gives `0..n-1`

---

## while loops

```python
steps = 0
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    steps += 1
```

- Repeats until the condition is false
- Something must move toward the exit — or it runs forever

---

## break & continue

```python
for n in range(10):
    if n == 5:
        break      # leave the loop
    if n % 2 == 0:
        continue   # skip to next
    print(n)
```

---

## match (teaser)

```python
match command:
    case "go":
        ...
    case _:
        ...
```

A cleaner multi-way branch — more later.

---

## Comprehensions (intro)

```python
doubled = [n * 2 for n in numbers]
```

Build a list in one line — full treatment in Lesson 05.

---

## Your turn

- Implement the three functions in `exercises/flow.py`
- `make test-lesson LESSON=03-control-flow` until green
- Run it: `uv run python -m exercises.flow`

---

## What's next

**Lesson 04 — Functions & tests.**
