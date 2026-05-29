# Plan C — Lesson 01 (Hello, Python) + multi-lesson make-test fix

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the first course lesson — a `greet(name)` exercise whose file doubles as a runnable interactive greeter — and fix `make test` so each lesson runs in an isolated pytest process (no cross-lesson `solutions` package collision).

**Architecture:** First the harness fix: narrow the root pytest `testpaths` to `["tools"]` and rewrite the lesson test make-targets to `cd` into each lesson and run pytest there (so the lesson's own `pythonpath = ["."]` applies and each lesson is its own process). Then author lesson `lessons/01-hello/` by scaffolding with the existing `new_lesson` tool and replacing the placeholder exercise with `greet`. The lesson appears as a link on the generated landing page automatically because `build_index`'s catalog already lists `01-hello`.

**Tech Stack:** Python 3.13, uv workspace, pytest, ruff, mypy, GNU Make, the existing `new_lesson` / `slides_dev` / `build_index` tools, reveal.js (vendored).

---

## Context for the implementer

- **Repo state:** Plans A and B are merged to `main`. The repo has a uv workspace with three tools under `tools/` (`new_lesson`, `slides_dev`, `build_index`), vendored reveal.js, a Makefile, deploy config, and CI. `lessons/` is currently **empty** — lesson 01 is the first.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`). After scaffolding a lesson (a new workspace member), run `uv sync --all-packages`.
- **The lesson template** (`tools/new_lesson/src/new_lesson/template/`) produces, for `make new-lesson NAME=01-hello`:
  - `lessons/01-hello/pyproject.toml` with `name = "lesson-01-hello"`, `[tool.uv] package = false`, and `[tool.pytest.ini_options] pythonpath = ["."]`.
  - `README.md` (with TODO placeholders), `slides/{index.html, slides.md, assets/.gitkeep}`.
  - `exercises/{__init__.py, main.py, test_main.py}` and `solutions/{__init__.py, main.py, test_main.py}` — the placeholder is a no-arg `hello()`.
  - The scaffolder derives the deck title from the slug: `01-hello` → "Hello". We override prose to "Hello, Python".
- **Catalog already lists the lesson:** `tools/build_index/src/build_index/catalog.py` has `LessonInfo("01", "hello", "Hello, Python", …, 1)`, so `dir_name()` is `01-hello`. Once `lessons/01-hello/slides/` exists on disk, `build_index` renders it as a link instead of a faded placeholder. No catalog change needed.
- **Design spec:** `docs/superpowers/specs/2026-05-29-lesson-01-hello-design.md`.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Commit messages:** Conventional Commits (`fix:`, `feat(lesson-01):`, `docs(lesson-01):`, `ci:`).
- **Do NOT push** — the controller handles branch finishing.
- Recipe lines in the Makefile use real TAB indentation.

---

## File Structure

```
python-training/
├── pyproject.toml                       (MODIFY: testpaths → ["tools"])
├── Makefile                             (MODIFY: test, test-exercises, test-lesson)
├── .github/workflows/ci.yml             (MODIFY: tool-tests step → make test)
└── lessons/
    └── 01-hello/                        (NEW — scaffolded then authored)
        ├── pyproject.toml               (from scaffold; unchanged)
        ├── README.md                    (authored — Task 3)
        ├── slides/
        │   ├── index.html               (from scaffold; <title> tweaked — Task 4)
        │   ├── slides.md                (authored — Task 4)
        │   └── assets/.gitkeep
        ├── exercises/
        │   ├── __init__.py              (from scaffold; kept, empty)
        │   ├── hello.py                 (authored — Task 2; replaces main.py)
        │   └── test_hello.py            (authored — Task 2; replaces test_main.py)
        └── solutions/
            ├── __init__.py              (from scaffold; kept, empty)
            ├── hello.py                 (authored — Task 2)
            └── test_hello.py            (authored — Task 2)
```

---

## Task 1: Harness fix — isolated per-lesson pytest

**Files:**
- Modify: `pyproject.toml` (the `[tool.pytest.ini_options] testpaths` line)
- Modify: `Makefile` (`test`, `test-exercises`, `test-lesson` targets)
- Modify: `.github/workflows/ci.yml` (replace the standalone tool-tests step)

- [ ] **Step 1: Narrow root pytest testpaths**

In `pyproject.toml`, find:

```toml
[tool.pytest.ini_options]
testpaths = ["tools", "lessons"]
```

Change the `testpaths` line to:

```toml
testpaths = ["tools"]
```

Leave the other keys (`python_files`, `python_classes`, `python_functions`) unchanged. Rationale: lessons are tested per-lesson from inside each lesson dir (next step), never collected globally, so a bare `uv run pytest` at the root runs only the tool suite and can never hit the cross-lesson `solutions` collision.

- [ ] **Step 2: Rewrite the `test` target**

In `Makefile`, replace the entire `test` target (currently lines ~14-17):

```makefile
.PHONY: test
test: ## Run tool + lesson-solution tests (the ones that should always pass)
	@dirs=$$(find lessons -type d -name solutions 2>/dev/null); \
	if [ -z "$$dirs" ]; then echo "no solution directories yet"; else uv run pytest tools $$dirs; fi
```

with:

```makefile
.PHONY: test
test: ## Run tool + lesson-solution tests (the ones that should always pass)
	uv run pytest tools
	@for d in $$(find lessons -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort); do \
		if [ -d "$$d/solutions" ]; then \
			echo "== $$d/solutions =="; \
			( cd "$$d" && uv run pytest solutions ) || exit 1; \
		fi; \
	done
```

> Each lesson runs in its own `pytest` process invoked from inside the lesson dir, so pytest uses the lesson's `pyproject.toml` as rootdir and applies its `pythonpath = ["."]`. No cross-lesson collection → no `import file mismatch`.

- [ ] **Step 3: Rewrite the `test-exercises` target**

Replace the `test-exercises` target (currently lines ~19-23):

```makefile
.PHONY: test-exercises
test-exercises: ## Run exercise tests (these fail by design until students complete them)
	-@dirs=$$(find lessons -type d -name exercises 2>/dev/null); \
	if [ -z "$$dirs" ]; then echo "no exercise directories yet"; exit 0; fi; \
	uv run pytest $$dirs
```

with:

```makefile
.PHONY: test-exercises
test-exercises: ## Run exercise tests (these fail by design until students complete them)
	@for d in $$(find lessons -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort); do \
		if [ -d "$$d/exercises" ]; then \
			echo "== $$d/exercises =="; \
			( cd "$$d" && uv run pytest exercises ) || true; \
		fi; \
	done
```

> `|| true` swallows the expected failures (exercise tests are the spec; they fail until students complete them).

- [ ] **Step 4: Rewrite the `test-lesson` target**

Replace the `test-lesson` target (currently lines ~25-29):

```makefile
.PHONY: test-lesson
test-lesson: ## Run tests for one lesson, both exercises and solutions (LESSON=NN-name)
	@test -n "$(LESSON)" || (echo "usage: make test-lesson LESSON=NN-name" && exit 1)
	-uv run pytest lessons/$(LESSON)/exercises
	uv run pytest lessons/$(LESSON)/solutions
```

with:

```makefile
.PHONY: test-lesson
test-lesson: ## Run tests for one lesson, both exercises and solutions (LESSON=NN-name)
	@test -n "$(LESSON)" || (echo "usage: make test-lesson LESSON=NN-name" && exit 1)
	-( cd lessons/$(LESSON) && uv run pytest exercises )
	( cd lessons/$(LESSON) && uv run pytest solutions )
```

> Same `cd`-into-lesson pattern. The leading `-` on the exercises line lets the (expected) exercise failures pass through without aborting the target, so the solutions line still runs.

- [ ] **Step 5: Update CI to run `make test` instead of the standalone tool-tests step**

In `.github/workflows/ci.yml`, find the step:

```yaml
      - name: Tool tests
        run: uv run pytest tools
```

Replace it with:

```yaml
      - name: Tests (tools + lesson solutions)
        run: make test
```

`make test` runs the tool suite plus every lesson's solution tests (isolated per lesson). Exercise tests are not run in CI (they fail by design). Leave the other ci.yml steps unchanged.

- [ ] **Step 6: Verify the tool suite and no-lesson behavior**

`lessons/` is still empty at this point, so the loops are no-ops.

Run: `make test`
Expected: `uv run pytest tools` runs and passes (50 tests); the per-lesson loop prints nothing (no lesson dirs); exit 0.

Run: `uv run pytest` (bare, from repo root)
Expected: collects only `tools` (testpaths) and passes — no attempt to collect `lessons/`.

Run: `make lint` and `uv run ruff format --check .`
Expected: both clean (Makefile/yaml/toml changes don't affect ruff).

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml Makefile .github/workflows/ci.yml
git commit -m "fix: run each lesson's tests in an isolated pytest process (multi-lesson make test)"
```

---

## Task 2: Scaffold lesson 01 and author the exercise + solution

**Files:**
- Create (via scaffold): `lessons/01-hello/` tree
- Create: `lessons/01-hello/exercises/hello.py`, `lessons/01-hello/exercises/test_hello.py`
- Create: `lessons/01-hello/solutions/hello.py`, `lessons/01-hello/solutions/test_hello.py`
- Delete (scaffold placeholders): `lessons/01-hello/{exercises,solutions}/main.py` and `.../test_main.py`

- [ ] **Step 1: Scaffold the lesson with the existing tool**

Run: `make new-lesson NAME=01-hello`
Expected: prints `created lessons/01-hello`. The tree exists with `pyproject.toml`, `README.md`, `slides/{index.html,slides.md,assets/.gitkeep}`, `exercises/{__init__.py,main.py,test_main.py}`, `solutions/{__init__.py,main.py,test_main.py}`.

Run: `uv sync --all-packages`
Expected: uv registers `lesson-01-hello` as a workspace member; exits 0.

- [ ] **Step 2: Remove the placeholder files**

```bash
rm lessons/01-hello/exercises/main.py lessons/01-hello/exercises/test_main.py
rm lessons/01-hello/solutions/main.py lessons/01-hello/solutions/test_main.py
```

(Keep both `__init__.py` files and `slides/assets/.gitkeep`.)

- [ ] **Step 3: Write the solution test (TDD red)**

Create `lessons/01-hello/solutions/test_hello.py`:

```python
from solutions.hello import greet


def test_greets_by_name() -> None:
    assert greet("Aki") == "Hello, Aki!"


def test_greets_anyone() -> None:
    assert greet("world") == "Hello, world!"
```

- [ ] **Step 4: Run the solution test — verify it fails**

Run: `( cd lessons/01-hello && uv run pytest solutions )`
Expected: collection error / `ModuleNotFoundError: No module named 'solutions.hello'` (hello.py doesn't exist yet).

- [ ] **Step 5: Write the solution implementation (TDD green)**

Create `lessons/01-hello/solutions/hello.py`:

```python
def greet(name: str) -> str:
    """Return a friendly greeting, e.g. "Hello, Aki!"."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    who = input("What's your name? ")
    print(greet(who))
```

- [ ] **Step 6: Run the solution test — verify it passes**

Run: `( cd lessons/01-hello && uv run pytest solutions )`
Expected: 2 passed.

- [ ] **Step 7: Write the exercise stub + its test (fails by design)**

Create `lessons/01-hello/exercises/hello.py`:

```python
def greet(name: str) -> str:
    """Return a friendly greeting, e.g. "Hello, Aki!"."""
    raise NotImplementedError("implement greet() so the tests pass")


if __name__ == "__main__":
    who = input("What's your name? ")
    print(greet(who))
```

Create `lessons/01-hello/exercises/test_hello.py`:

```python
from exercises.hello import greet


def test_greets_by_name() -> None:
    assert greet("Aki") == "Hello, Aki!"


def test_greets_anyone() -> None:
    assert greet("world") == "Hello, world!"
```

- [ ] **Step 8: Verify the exercise test fails as designed**

Run: `( cd lessons/01-hello && uv run pytest exercises )`
Expected: 2 failed with `NotImplementedError: implement greet() so the tests pass`. (This is the intended deliverable state — the failing test is the student's spec.)

- [ ] **Step 9: Verify the combined make targets**

Run: `make test-lesson LESSON=01-hello`
Expected: exercises section FAILS (NotImplementedError, tolerated by the leading `-`); solutions section PASSES; overall exit 0.

Run: `make test`
Expected: tool suite passes, then `== lessons/01-hello/solutions ==` runs and passes (2 tests); exit 0.

- [ ] **Step 10: Verify the runnable greeter works (solution)**

Run: `printf 'Aki\n' | ( cd lessons/01-hello && uv run python -m solutions.hello )`
Expected: prints `What's your name? Hello, Aki!` (the prompt then the greeting).

Run: `printf 'Aki\n' | ( cd lessons/01-hello && uv run python -m exercises.hello )`
Expected: prompts, then raises `NotImplementedError` (exercise not implemented — correct).

- [ ] **Step 11: Lint, format, type-check the lesson code**

Run: `make lint`
Expected: All checks passed!

Run: `uv run ruff format --check .`
Expected: all files formatted (no diff). If it reports the new files would be reformatted, run `uv run ruff format lessons/01-hello` and re-check.

Run: `uv run mypy lessons/01-hello/solutions/hello.py lessons/01-hello/exercises/hello.py`
Expected: Success. (Not a CI gate, but the lesson code should be clean — `greet` is fully typed.)

- [ ] **Step 12: Commit**

```bash
git add lessons/01-hello uv.lock
git commit -m "feat(lesson-01): add greet exercise + solution with runnable greeter"
```

---

## Task 3: Author the lesson README

**Files:**
- Modify: `lessons/01-hello/README.md` (replace the scaffold's TODO placeholders)

- [ ] **Step 1: Replace the README with authored content**

Overwrite `lessons/01-hello/README.md` with:

````markdown
# Lesson 01 — Hello, Python

Your first Python program. By the end you will have run Python through
`uv`, written and called a typed function, run it as an interactive
program, and made a failing test pass.

## Learning goals

- Run Python via `uv run` and verify your toolchain
- Understand `python -m module` versus running a script, and the REPL
- Write and call a typed function that returns an f-string (`greet`)
- Use `print()` and `input()` in a runnable program
- Read a `test_*.py` file as the spec and make a failing test pass

## Prereqs

- [`uv`](https://docs.astral.sh/uv/) installed — see the [repo README](../../README.md). No earlier lessons required.

## Concepts

**The toolchain.** `uv` installs Python (per `.python-version`), manages the
project's virtual environment, and runs commands inside it. `uv run python
--version` prints the interpreter version; `uv run pytest …` runs the tests.

**Functions, types, f-strings.** A function is defined with `def`. We annotate
the parameter and return type — `def greet(name: str) -> str:` — and build the
result with an f-string: `f"Hello, {name}!"`. Type hints are optional in early
lessons but we use them from the start.

**`print` and `input`.** `print(x)` writes a line to the screen; `input(prompt)`
shows a prompt and returns what the user typed, as a string.

**Scripts versus modules.** The same `.py` file can be *imported* (the tests do
`from solutions.hello import greet`) or *run* as a program. Code under
`if __name__ == "__main__":` runs only when the file is executed directly
(`python -m solutions.hello`), not when it is imported — so importing the module
for tests does not trigger the interactive prompt.

**Tests are the spec.** Each `test_*.py` file says what "done" means. For now,
treat `pytest` as a magic test runner that checks your work; we explain it
properly in Lesson 04. Your job: make the failing test pass.

## Exercise brief

Open `exercises/hello.py` and implement `greet(name)` so it returns a greeting
like `"Hello, Aki!"`. Both tests in `exercises/test_hello.py` must pass. Then
run the file as a program to greet yourself interactively.

## How to run

Run the tests (exercises fail until you implement `greet`; solutions pass):

```bash
make test-lesson LESSON=01-hello
```

Or directly:

```bash
cd lessons/01-hello && uv run pytest exercises
```

Run the interactive greeter:

```bash
cd lessons/01-hello && uv run python -m exercises.hello
```

## Going further

- Try other f-string tricks: `f"{name!r}"`, `f"{name:>10}"`, `f"{2 + 2 = }"`.
- Run a one-liner without a file: `uv run python -c 'print("hi")'`.
- Open the REPL and call your function: `uv run python`, then `from solutions.hello import greet` and `greet("you")`.
````

- [ ] **Step 2: Verify markdown fences are balanced**

Run: `grep -c '```' lessons/01-hello/README.md`
Expected: an even number (every fence closed).

Run: `grep -q "Hello, Python" lessons/01-hello/README.md && grep -q "make test-lesson LESSON=01-hello" lessons/01-hello/README.md && echo "readme ok"`
Expected: `readme ok`.

- [ ] **Step 3: Commit**

```bash
git add lessons/01-hello/README.md
git commit -m "docs(lesson-01): author the README (goals, concepts, exercise, going further)"
```

---

## Task 4: Author the slide deck

**Files:**
- Modify: `lessons/01-hello/slides/slides.md` (replace the template deck)
- Modify: `lessons/01-hello/slides/index.html` (deck `<title>` only)

- [ ] **Step 1: Replace slides.md with the authored deck**

Overwrite `lessons/01-hello/slides/slides.md` with:

````markdown
## Lesson 01
### Hello, Python

Run Python, write your first function, make a test pass.

Note:
Goal: from zero to a passing test and a runnable greeter.

---

## Why Python

- Readable — looks close to pseudocode
- Batteries included — a large standard library
- Everywhere — scripting, web, data, automation

---

## The toolchain — `uv`

`uv` installs Python, manages the virtual environment, and runs things.

```bash
uv run python --version
uv run pytest
```

Note:
uv reads .python-version and provisions the right interpreter automatically.

---

## Running Python

- `uv run python -m module` runs a module
- `uv run python file.py` runs a script
- `uv run python` opens the REPL (interactive prompt)

---

## Your first function

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

- `def` defines a function
- `name: str -> str` are type hints
- `f"..."` is an f-string — `{name}` is substituted

---

## print() and input()

```python
who = input("What's your name? ")
print(greet(who))
```

- `input` shows a prompt and returns what was typed
- `print` writes a line to the screen

---

## Scripts vs modules

```python
if __name__ == "__main__":
    who = input("What's your name? ")
    print(greet(who))
```

- Runs only when the file is executed directly
- Importing the file (for tests) does **not** run it

---

## Tests are the spec

```python
from exercises.hello import greet

def test_greets_by_name() -> None:
    assert greet("Aki") == "Hello, Aki!"
```

For now, pytest is a magic test runner. Make the failing test pass:

```bash
make test-lesson LESSON=01-hello
```

Note:
We explain pytest properly in Lesson 04.

---

## Your turn

- Implement `greet` in `exercises/hello.py`
- Run `make test-lesson LESSON=01-hello` until green
- Greet yourself: `uv run python -m exercises.hello`

---

## What's next

**Lesson 02 — Variables, types, operators.**
````

- [ ] **Step 2: Fix the deck `<title>` in index.html**

In `lessons/01-hello/slides/index.html`, the scaffolder set the title from the slug. Find the `<title>` line (it reads `<title>Lesson 01 — Hello</title>`) and change it to:

```html
  <title>Lesson 01 — Hello, Python</title>
```

(Only the `<title>` text changes; leave the rest of index.html untouched.)

- [ ] **Step 3: Build the site and confirm the lesson is now a link**

Run: `make slides-build`
Expected: prints `built dist`.

Run:
```bash
grep -q 'href="lessons/01-hello/slides/"' dist/index.html && echo "LINK_OK"
grep -c 'class="lesson future"' dist/index.html
test -f dist/lessons/01-hello/slides/index.html && test -f dist/lessons/01-hello/slides/slides.md && echo "SLIDES_COPIED"
```
Expected: `LINK_OK`; the future-placeholder count is now `27` (lesson 01 is no longer faded); `SLIDES_COPIED`.

Run: `rm -rf dist`

- [ ] **Step 4: Smoke-test the dev server**

Start it in the background and curl it:
```bash
( make slides-dev LESSON=01-hello & ) ; sleep 1.5
curl -s http://127.0.0.1:8000/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "slidesmd=%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
# stop the server
kill "$(lsof -ti:8000)" 2>/dev/null || true
```
Expected: title line `<title>Lesson 01 — Hello, Python</title>`, `slidesmd=200`, `revealcss=200`. Confirm `lsof -ti:8000` is empty afterward.

If `make slides-dev` backgrounding is awkward in your shell, run `uv run python -m slides_dev --lesson 01-hello --repo-root "$(pwd)" --port 8000 &` instead, then the same curls and `kill`.

- [ ] **Step 5: Commit**

```bash
git add lessons/01-hello/slides/slides.md lessons/01-hello/slides/index.html
git commit -m "feat(lesson-01): author the slide deck"
```

---

## Task 5: Final verification

End-to-end check that the lesson + harness fix work together. No new code unless something needs tidying.

- [ ] **Step 1: Full quality bar**

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
- `make test` → tool suite passes (50) AND `== lessons/01-hello/solutions ==` passes (2); exit 0.

- [ ] **Step 2: Lesson-level red/green**

```bash
make test-lesson LESSON=01-hello
```
Expected: exercises FAIL (NotImplementedError, tolerated); solutions PASS; exit 0.

- [ ] **Step 3: Greeter behaves (both packages)**

```bash
printf 'world\n' | ( cd lessons/01-hello && uv run python -m solutions.hello )
```
Expected: `What's your name? Hello, world!`.

- [ ] **Step 4: Landing page link + git hygiene**

```bash
make slides-build
grep -q 'href="lessons/01-hello/slides/"' dist/index.html && echo "LINK_OK"
rm -rf dist
git status --porcelain
git ls-files | grep -E 'dist/|__pycache__|\.pyc$' || echo "no stray artifacts tracked"
```
Expected: `LINK_OK`; clean working tree (no `dist/`); `no stray artifacts tracked` (the `shared/reveal/dist/` vendored files are expected and fine — only a top-level generated `dist/` would be a problem, and it's gitignored).

- [ ] **Step 5: Commit only if Step 1-4 surfaced changes**

```bash
git status
```
If clean, skip. If anything changed (e.g., a `ruff format` tidy), investigate, then commit with an appropriate message.

---

## Notes for execution

- No `gcloud`, no secrets, no push. The deploy pipeline picks the lesson up automatically on the next push to `main` (the catalog already lists it; `build_index` now finds its `slides/`).
- After this plan, `make test` correctly runs tools + the one lesson's solutions in isolated processes. The pattern scales: lesson 02 will Just Work with the same targets, validating the harness fix.
- The exercise tests are *meant* to fail until a student implements `greet`. That is the lesson, not a bug — `make test-lesson` tolerates it and `make test` only gates on solutions.
