## Lesson 05
### Collections

list, tuple, dict, set — and comprehensions to build them.

Note:
Five drills: a list comp, a dict comp, a set, enumerate, and zip.

---

## The four containers

- `list` — ordered, mutable: `[1, 2, 3]`
- `tuple` — ordered, immutable: `(1, 2)`
- `dict` — key → value: `{"a": 1}`
- `set` — unordered, unique: `{1, 2}`

Pick: changing→list, fixed→tuple, lookup→dict, dedup→set.

---

## list

```python
xs = [1, 2, 3]
xs[0]        # 1
xs[1:3]      # [2, 3]
xs.append(4) # [1, 2, 3, 4]
```

- Ordered and mutable

---

## tuple

```python
point = (2, 3)
x, y = point   # unpack: x=2, y=3
```

- Immutable — can't be changed after creation
- Good for fixed records and as dict keys

---

## dict

```python
ages = {"ann": 30, "bo": 25}
ages["ann"]            # 30
ages.get("zoe", 0)     # 0  (safe default)
for k, v in ages.items():
    ...
```

---

## set

```python
s = {1, 2, 2, 3}   # {1, 2, 3}
2 in s             # True
{1, 2} | {2, 3}    # {1, 2, 3}  (union)
```

- Unordered, unique; fast membership

---

## List comprehension

```python
[n for n in numbers if n % 2 == 0]
```

- Build a list in one expression
- The trailing `if` filters

---

## Dict comprehension

```python
{word: len(word) for word in words}
```

- Build a dict in one expression — `key: value`

---

## Set & nested comprehensions

```python
{len(w) for w in words}              # set comp
[x for row in grid for x in row]     # nested
[x if x > 0 else 0 for x in xs]      # conditional value
```

---

## enumerate

```python
for i, item in enumerate(items):
    ...

{item: i for i, item in enumerate(items)}
```

- Index and item together — no manual counter

---

## zip

```python
list(zip(names, scores))   # [(n, s), ...]

for name, score in zip(names, scores):
    ...
```

- Pairs iterables; `zip(a, b, strict=True)` checks lengths

---

## Your turn

- Implement the five functions in `exercises/containers.py`
- `make test-lesson LESSON=05-collections` until green
- Run it: `uv run python -m exercises.containers`

---

## What's next

**Lesson 06 — Classes & dataclasses.**
