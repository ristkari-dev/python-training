# Plan G — Lesson 05 (Collections)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the fifth course lesson — five collection-idiom drills (`evens` list comprehension, `word_lengths` dict comprehension, `unique` set, `index_map` enumerate, `pair_up` zip) with set/nested comprehensions taught on slides/README only.

**Architecture:** Scaffold `lessons/05-collections/` with the existing `new_lesson` tool, replace the placeholder exercise with the five functions (exercise stubs raise `NotImplementedError`; solutions implemented), author the README + slide deck. The module is named `containers.py` (NOT `collections.py`, to avoid shadowing the stdlib `collections` module). No tooling/harness changes. Fifth lesson, so `make test` now spans five lessons.

**Tech Stack:** Python 3.13, uv workspace, pytest, ruff, mypy, GNU Make, the existing `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored).

---

## Context for the implementer

- **Repo state:** Plans A–F merged to `main`. `lessons/01-hello/` … `lessons/04-functions/` exist and are the pattern to mirror. `make test`/`test-lesson` run each lesson in an isolated pytest process by `cd`-ing into the lesson dir.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`). After scaffolding a lesson, run it.
- **`make new-lesson NAME=05-collections`** produces the lesson with `pyproject.toml` (name `lesson-05-collections`, `[tool.uv] package=false`, `[tool.pytest.ini_options] pythonpath=["."]`), `README.md` (TODO placeholders), `slides/{index.html,slides.md,assets/.gitkeep}`, and `exercises/{__init__.py,main.py,test_main.py}` + `solutions/{__init__.py,main.py,test_main.py}` (placeholder no-arg `hello()`). The scaffolder derives the deck title from the slug ("Collections") and emits **absolute** `/shared/reveal/...` asset paths (do not change those).
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("05", "collections", "Collections", …, 1)`, so `dir_name()` is `05-collections`. Once `lessons/05-collections/slides/` exists, `build_index` renders it as a link. No catalog change needed.
- **Module naming:** use `containers.py`/`test_containers.py` — NOT `collections.py` (which would shadow/confuse the stdlib `collections` module).
- **Design spec:** `docs/superpowers/specs/2026-06-07-lesson-05-collections-design.md`.
- **Mirror Lesson 04** at `lessons/04-functions/` for exact file shapes, README structure, and slide style.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Commit messages:** Conventional Commits. **Do NOT add a `Co-Authored-By` trailer or any AI-attribution line to commits** (project rule). Subject + body only.
- **Do NOT push** — the controller handles branch finishing.
- The module file is named `containers.py` (tests `test_containers.py`), replacing the scaffold's `main.py`/`test_main.py`.

---

## File Structure

```
lessons/05-collections/                   (NEW — scaffolded then authored)
├── pyproject.toml                        (from scaffold; unchanged)
├── README.md                             (authored — Task 2)
├── slides/
│   ├── index.html                        (from scaffold; <title> tweaked — Task 3)
│   ├── slides.md                         (authored — Task 3)
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py                       (from scaffold; kept, empty)
│   ├── containers.py                     (authored — Task 1; replaces main.py)
│   └── test_containers.py                (authored — Task 1; replaces test_main.py)
└── solutions/
    ├── __init__.py                       (from scaffold; kept, empty)
    ├── containers.py                     (authored — Task 1)
    └── test_containers.py                (authored — Task 1)
```

---

## Task 1: Scaffold lesson 05 and author the exercise + solution

**Files:**
- Create (via scaffold): `lessons/05-collections/` tree
- Create: `lessons/05-collections/exercises/containers.py`, `.../exercises/test_containers.py`
- Create: `lessons/05-collections/solutions/containers.py`, `.../solutions/test_containers.py`
- Delete (scaffold placeholders): `lessons/05-collections/{exercises,solutions}/main.py` and `.../test_main.py`

- [ ] **Step 1: Scaffold the lesson**

Run: `make new-lesson NAME=05-collections`
Expected: prints `created lessons/05-collections`; the tree exists.

Run: `uv sync --all-packages`
Expected: registers `lesson-05-collections`; exits 0.

- [ ] **Step 2: Remove the placeholder files**

```bash
rm lessons/05-collections/exercises/main.py lessons/05-collections/exercises/test_main.py
rm lessons/05-collections/solutions/main.py lessons/05-collections/solutions/test_main.py
```

(Keep both `__init__.py` files and `slides/assets/.gitkeep`.)

- [ ] **Step 3: Write the solution tests (TDD red)**

Create `lessons/05-collections/solutions/test_containers.py`:

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

- [ ] **Step 4: Run the solution tests — verify RED**

Run: `( cd lessons/05-collections && uv run pytest solutions )`
Expected: collection error / `ModuleNotFoundError: No module named 'solutions.containers'` (containers.py doesn't exist yet).

- [ ] **Step 5: Write the solution (TDD green)**

Create `lessons/05-collections/solutions/containers.py`:

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

- [ ] **Step 6: Run the solution tests — verify GREEN**

Run: `( cd lessons/05-collections && uv run pytest solutions )`
Expected: 10 passed.

- [ ] **Step 7: Write the exercise stub + its (fail-by-design) test**

Create `lessons/05-collections/exercises/containers.py`:

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

Create `lessons/05-collections/exercises/test_containers.py` (identical to the solutions test except the import line):

```python
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
```

- [ ] **Step 8: Verify the exercise tests fail as designed**

Run: `( cd lessons/05-collections && uv run pytest exercises )`
Expected: 10 failed with `NotImplementedError`. (Intended deliverable — the failing tests are the student's spec.)

- [ ] **Step 9: Verify the make targets**

Run: `make test-lesson LESSON=05-collections`
Expected: exercises section FAILS (NotImplementedError, tolerated by the leading `-`); solutions section PASSES (10); overall exit 0.

Run: `make test`
Expected: tool suite passes, then `== lessons/01-hello/solutions ==` (2), `== lessons/02-variables/solutions ==` (10), `== lessons/03-control-flow/solutions ==` (15), `== lessons/04-functions/solutions ==` (13), AND `== lessons/05-collections/solutions ==` (10) all pass; exit 0; no `import file mismatch`.

- [ ] **Step 10: Verify the runnable module (solution)**

Run: `( cd lessons/05-collections && uv run python -m solutions.containers )`
Expected: prints five lines: `[2, 4, 6]`, `{'hi': 2, 'world': 5}`, `{1, 2, 3}`, `{'a': 0, 'b': 1, 'c': 2}`, `[('ann', 90), ('bo', 85)]`.

Run: `( cd lessons/05-collections && uv run python -m exercises.containers )`
Expected: raises `NotImplementedError` (exercise not implemented — correct).

- [ ] **Step 11: Lint, format, type-check**

Run: `make lint`
Expected: All checks passed!

Run: `uv run ruff format --check .`
Expected: all files formatted (no diff). If it reports the new files would be reformatted, run `uv run ruff format lessons/05-collections` and re-check; note it.

Run: `uv run mypy lessons/05-collections/solutions/containers.py lessons/05-collections/exercises/containers.py`
Expected: Success: no issues found. (All five functions are cleanly typed: list/dict/set comprehensions and `list(zip(...))` infer the annotated return types.)

- [ ] **Step 12: Commit**

```bash
git add lessons/05-collections uv.lock
git commit -m "feat(lesson-05): add collection-idiom drills (list/dict/set comps, enumerate, zip)"
```

(No `Co-Authored-By` trailer. After committing, `git log -1 --format='%B'` should contain no co-author/attribution line.)

---

## Task 2: Author the lesson README

**Files:**
- Modify: `lessons/05-collections/README.md` (replace the scaffold's TODO placeholders)

- [ ] **Step 1: Overwrite `lessons/05-collections/README.md`**

````markdown
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
equal lengths.

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
- `zip(a, b, strict=True)` raises if the iterables differ in length.
- `dict.get(key, default)` and `dict.setdefault(key, default)` handle missing
  keys gracefully.
- Ordering with `sorted(...)` is coming in a later lesson.
````

- [ ] **Step 2: Verify**

Run: `grep -c '```' lessons/05-collections/README.md` → expect an EVEN number.
Run: `grep -q "Lesson 05 — Collections" lessons/05-collections/README.md && grep -q "make test-lesson LESSON=05-collections" lessons/05-collections/README.md && grep -q "Run the tests first to watch them fail" lessons/05-collections/README.md && echo "readme ok"` → expect `readme ok`.
Run: `grep -iE 'TODO' lessons/05-collections/README.md && echo "HAS TODO" || echo "no todos"` → expect `no todos`.

- [ ] **Step 3: Commit**

```bash
git add lessons/05-collections/README.md
git commit -m "docs(lesson-05): author the README (containers, comprehensions, enumerate/zip)"
```

(No `Co-Authored-By` trailer.)

---

## Task 3: Author the slide deck

**Files:**
- Modify: `lessons/05-collections/slides/slides.md` (replace the template deck)
- Modify: `lessons/05-collections/slides/index.html` (deck `<title>` only)

- [ ] **Step 1: Overwrite `lessons/05-collections/slides/slides.md`**

````markdown
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
````

- [ ] **Step 2: Fix the deck `<title>` in index.html**

In `lessons/05-collections/slides/index.html`, find the `<title>` line (the scaffolder set it from the slug, e.g. `<title>Lesson 05 — Collections</title>`) and confirm it reads:

```html
  <title>Lesson 05 — Collections</title>
```

(The slug-derived title "Collections" already matches the course name, so this is likely already correct — verify and leave it. Do NOT change the `/shared/reveal/...` asset paths.)

- [ ] **Step 3: Build the site; confirm the lesson is a LINK and uses absolute asset paths**

Run: `make slides-build`
Expected: prints `built dist`.

Run:
```bash
grep -q 'href="lessons/05-collections/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
grep -oE '/shared/reveal|\.\./\.\./shared/reveal' dist/lessons/05-collections/slides/index.html | sort | uniq -c
test -f dist/lessons/05-collections/slides/index.html && test -f dist/lessons/05-collections/slides/slides.md && echo "SLIDES_COPIED"
```
Expected: `LINK_OK`; future-placeholder count is now `23`; the asset-path grep shows only `/shared/reveal` occurrences (NO `../../shared/reveal`); `SLIDES_COPIED`.

Run: `rm -rf dist`

- [ ] **Step 4: Dev-server smoke test**

```bash
( uv run python -m slides_dev --lesson 05-collections --repo-root "$(pwd)" --port 8000 & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
kill "$(lsof -ti:8000)" 2>/dev/null || true
```
Expected: title line `<title>Lesson 05 — Collections</title>`, `slidesmd=200`, `revealcss=200`. Confirm `lsof -ti:8000` is empty afterward.

- [ ] **Step 5: Commit**

```bash
git add lessons/05-collections/slides/slides.md lessons/05-collections/slides/index.html
git commit -m "feat(lesson-05): author the slide deck"
```

(No `Co-Authored-By` trailer. If only `slides.md` changed because the title was already correct, commit just that file.)

---

## Task 4: Final verification

End-to-end check. No new code unless something needs tidying.

- [ ] **Step 1: Confirm branch**

Run: `git branch --show-current`
Expected: `lesson-05-collections`. If not, STOP and report.

- [ ] **Step 2: Full quality bar**

```bash
make lint
uv run ruff format --check .
make typecheck
make test
```
Expected:
- `make lint` → All checks passed!
- `ruff format --check .` → all files formatted (no diff).
- `make typecheck` → Success (tools; 13 source files).
- `make test` → tool suite passes, Lessons 01 (2), 02 (10), 03 (15), 04 (13), 05 (10) solutions all pass; exit 0; no `import file mismatch`.

- [ ] **Step 3: Lesson red/green + module**

```bash
make test-lesson LESSON=05-collections
( cd lessons/05-collections && uv run python -m solutions.containers )
```
Expected: exercises FAIL (NotImplementedError, tolerated), solutions PASS (10), exit 0; module prints the five demo lines (`[2, 4, 6]`, `{'hi': 2, 'world': 5}`, `{1, 2, 3}`, `{'a': 0, 'b': 1, 'c': 2}`, `[('ann', 90), ('bo', 85)]`).

- [ ] **Step 4: Landing page link + git hygiene + no co-author trailers**

```bash
make slides-build
grep -q 'href="lessons/05-collections/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
rm -rf dist
git status --porcelain
git ls-files lessons/05-collections | sort
git log --oneline main..HEAD
git log main..HEAD --format='%B' | grep -i 'co-authored\|generated with' && echo "TRAILER FOUND (bad)" || echo "no trailers — good"
```
Expected: `LINK_OK`; future count `23`; clean working tree (no `dist/`); `lessons/05-collections` has pyproject.toml, README.md, slides/{index.html,slides.md,assets/.gitkeep}, exercises/{__init__.py,containers.py,test_containers.py}, solutions/{__init__.py,containers.py,test_containers.py} — NO main.py/test_main.py; 3 commits; `no trailers — good`.

- [ ] **Step 5: Confirm port clear**

```bash
lsof -ti:8000 || echo "port clear"
```
Expected: `port clear`.

- [ ] **Step 6: Commit only if Steps 1-5 surfaced changes**

If `git status` is clean, report CLEAN. If anything changed, investigate and commit (no co-author trailer); if a check FAILED, STOP and report BLOCKED.

---

## Notes for execution

- No tooling/harness changes, no `gcloud`, no secrets, no push. The deploy pipeline picks the lesson up automatically on the next merge to `main`.
- The module is `containers.py`, NOT `collections.py` (avoid stdlib shadowing). The scaffolded deck already uses absolute `/shared/reveal/...` paths.
- Commits must NOT include `Co-Authored-By` or AI-attribution trailers (project rule).
