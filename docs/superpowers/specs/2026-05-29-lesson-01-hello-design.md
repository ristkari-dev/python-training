# Lesson 01 — Hello, Python — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-05-29
**Owner:** Aki Ristkari

## Summary

The first course lesson plus a small harness fix that lets `make test` work once the repo holds more than one lesson. Lesson 01 ("Hello, Python") is the gentlest possible introduction: students implement a single `greet(name) -> str` function to make a failing pytest pass, and the same file doubles as a runnable interactive greeter that demonstrates `print`/`input` and the scripts-vs-modules distinction. This is the first real lesson built on the Plan A foundation + Plan B slide pipeline, so it doubles as an end-to-end validation of the lesson workflow (scaffold → author → test → build → publish).

## Part A — Harness fix: `make test` for multiple lessons

### Problem

Every scaffolded lesson's `solutions/` directory is a Python package named `solutions` (and `exercises/` is named `exercises`). pytest's default prepend import mode cannot collect two packages of the same name in one session — it raises `import file mismatch`. So the moment a second lesson exists, a single `pytest` invocation spanning lessons aborts before running. The current `make test` recipe (`uv run pytest tools $dirs`, concatenating all `solutions/` dirs into one invocation) hits exactly this. It was documented as a Phase 1 prerequisite during Plan A's review.

### Approach: per-lesson isolated pytest processes

Run each lesson's tests in its own pytest process, invoked from inside the lesson directory so the lesson's own pytest config applies. This sidesteps the collision entirely (no cross-lesson collection) and makes each lesson a self-contained mini-project.

- **Root `pyproject.toml`:** change `[tool.pytest.ini_options] testpaths` from `["tools", "lessons"]` to `["tools"]`. Lessons are never collected globally; a bare `uv run pytest` from the repo root runs only the tool suite, cleanly. (Lesson tests are reached via `make`.)
- **Makefile** — every lesson test target `cd`s into the lesson directory before invoking pytest, so pytest resolves the lesson's `pyproject.toml` as its rootdir and applies its `[tool.pytest.ini_options] pythonpath = ["."]` (already present in the lesson template from Plan A). Each lesson runs in a separate process:
  - `test` — runs `uv run pytest tools`, then loops over `lessons/*/` and, for each that has a `solutions/` dir, runs `( cd lessons/<name> && uv run pytest solutions )`. Any failure fails the target.
  - `test-exercises` — same per-lesson loop running `exercises`; failures are tolerated (a leading `-`), because exercise tests fail by design until students complete them.
  - `test-lesson LESSON=<name>` — `cd` into the named lesson, run `exercises` (tolerated) then `solutions` (must pass).
- **`.github/workflows/ci.yml`:** add a "Lesson solution tests" step that runs the per-lesson solutions loop (e.g. via `make test`), so every lesson's reference solution is gated green in CI. Exercise tests are not a CI gate (they are expected to fail).

### Decisions

- **Keep the template's `exercises/__init__.py` and `solutions/__init__.py`.** With per-lesson isolation they are harmless, and `from solutions.hello import greet` resolves whether `solutions` is a regular package (with `__init__.py`) or a namespace package (without). Removing them would force changes to the `new_lesson` scaffolder's tests (which assert those files exist) for no correctness or safety gain under this approach. The supported test entry point is `make test`; running a bare `pytest lessons/` that collects all lessons at once is explicitly unsupported.
- **No change to the `new_lesson` scaffolder or its template** beyond what Part B's lesson authoring requires (lesson 01 is hand-authored after scaffolding; the template stays generic).

## Part B — Lesson 01 — Hello, Python

### Learning goals

1. Install/verify the toolchain with `uv`; run Python via `uv run`.
2. Understand `python -m module` vs running a script, and the REPL.
3. Write and call a typed function with an f-string return (`greet`).
4. Use `print()` and `input()` in a runnable program.
5. Read a `*_test.py` file as the spec and make a failing test pass with pytest.

### Files

Lesson directory `lessons/01-hello/` (scaffolded via `make new-lesson NAME=01-hello`, then hand-authored):

```
lessons/01-hello/
├── pyproject.toml          # workspace member: name "lesson-01-hello", [tool.uv] package=false,
│                           #   [tool.pytest.ini_options] pythonpath = ["."]
├── README.md
├── slides/
│   ├── index.html          # reveal.js bootstrap (unchanged from scaffold)
│   ├── slides.md           # the deck (authored)
│   └── assets/.gitkeep
├── exercises/
│   ├── __init__.py         # empty (kept; see Part A decision)
│   ├── hello.py            # greet() stub + runnable __main__
│   └── test_hello.py       # failing tests for greet()
└── solutions/
    ├── __init__.py         # empty
    ├── hello.py            # greet() implemented + runnable __main__
    └── test_hello.py       # identical tests, pass
```

The scaffolder emits `main.py`/`test_main.py` with a no-arg `hello()`; lesson 01 replaces these with `hello.py`/`test_hello.py` and the `greet` exercise below. Meaningful file names match the sibling courses' convention (rust used `lib.rs`/`greet`, elixir used `greet.ex`).

### `exercises/hello.py`

```python
def greet(name: str) -> str:
    """Return a friendly greeting, e.g. "Hello, Aki!"."""
    raise NotImplementedError("implement greet() so the tests pass")


if __name__ == "__main__":
    who = input("What's your name? ")
    print(greet(who))
```

### `exercises/test_hello.py`

```python
from exercises.hello import greet


def test_greets_by_name() -> None:
    assert greet("Aki") == "Hello, Aki!"


def test_greets_anyone() -> None:
    assert greet("world") == "Hello, world!"
```

### `solutions/hello.py`

```python
def greet(name: str) -> str:
    """Return a friendly greeting, e.g. "Hello, Aki!"."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    who = input("What's your name? ")
    print(greet(who))
```

### `solutions/test_hello.py`

Identical to the exercises test except the import line:

```python
from solutions.hello import greet


def test_greets_by_name() -> None:
    assert greet("Aki") == "Hello, Aki!"


def test_greets_anyone() -> None:
    assert greet("world") == "Hello, world!"
```

### The dual nature of `hello.py`

The same file is both **importable** and **runnable**:

- **Importable:** `test_hello.py` does `from exercises.hello import greet`. With the lesson's `pythonpath = ["."]` and pytest run from the lesson directory, `exercises` is importable and `exercises.hello.greet` resolves.
- **Runnable:** `cd lessons/01-hello && uv run python -m exercises.hello` runs the `if __name__ == "__main__":` block — an interactive greeter that prompts for a name and prints the greeting. The `__main__` block is not part of the graded tests.

This is the scripts-vs-modules concept demonstrated rather than merely described: importing the module runs no I/O; running it as `__main__` does.

### Slides (`slides/slides.md`)

Roughly nine slides, `---` separated, code in fenced `python` blocks, ~15 visible lines max per code slide. `Note:` speaker notes where useful.

1. **Title** — "Lesson 01 — Hello, Python" + one-line goal.
2. **Why Python** — readable, batteries-included, ubiquitous (brief).
3. **The toolchain — `uv`** — installs Python, manages the venv, runs things; `uv run python --version`.
4. **Running Python** — `uv run python -m <module>`, the REPL, scripts vs modules.
5. **Your first function** — `def greet(name: str) -> str: return f"Hello, {name}!"`; covers `def`, type hints, f-strings.
6. **`print()` and `input()`** — the interactive greeter.
7. **Scripts vs modules** — `if __name__ == "__main__":`; same file imported (tests) vs run (`python -m`).
8. **Tests are the spec** — show `test_hello.py`, `assert`, "pytest is a magic test runner for now"; `make test-lesson LESSON=01-hello`.
9. **The exercise + what's next** — make the failing test pass; pointer to Lesson 02 (Variables, types, operators).

### README (`README.md`)

Sections per the four-file convention:

- **Learning goals** — the five bullets above.
- **Prereqs** — `uv` installed (link to the repo root README); no prior lessons.
- **Concepts** — 1–3 short paragraphs mirroring the deck: the `uv` toolchain; `def` + type hints + f-strings; `print`/`input`; scripts vs modules and `if __name__ == "__main__"`; pytest as the spec ("magic test runner" framing, explained properly in Lesson 04).
- **Exercise brief** — implement `greet` in `exercises/hello.py` so both tests pass; run the interactive greeter to see it work.
- **How to run:**
  - Tests: `make test-lesson LESSON=01-hello` (or `cd lessons/01-hello && uv run pytest exercises`).
  - Greeter: `cd lessons/01-hello && uv run python -m exercises.hello`.
- **Going further** — f-string formatting tricks, `python -c '...'`, exploring the REPL; kept light, no new graded work.

## Verification (success criteria)

- `make test-lesson LESSON=01-hello` → exercise tests FAIL with `NotImplementedError`; solution tests PASS; target exit 0 (exercise failure tolerated).
- `make test` → tools suite passes and the `01-hello` solution passes, in isolated per-lesson processes (no `import file mismatch`).
- `cd lessons/01-hello && uv run python -m exercises.hello` → prompts for a name and prints `Hello, <name>!` (run against `solutions/` it greets; against `exercises/` it raises until implemented).
- `make slides-build` → `dist/index.html` shows `01-hello` as a **link** (no longer a faded "future" placeholder); `dist/lessons/01-hello/slides/index.html` exists.
- `make lint` and `uv run ruff format --check .` → clean (these run repo-wide, so they cover the lesson code). `make typecheck` stays scoped to the tools and remains clean; lesson 01 code is cleanly typed but is not a typecheck gate (strict lesson typing starts at Lesson 09).
- The deck renders locally via `make slides-dev LESSON=01-hello`.

## Non-goals

- No `argparse`/`sys.argv` (deferred to Lesson 08).
- No control flow / `if`-`elif` in the exercise (deferred to Lesson 03).
- No formal pytest teaching (fixtures/parametrize) — that is Lesson 04; here pytest is a "magic test runner".
- No changes to the `new_lesson` scaffolder, `slides_dev`, or `build_index` tools beyond what's listed.
- No type-checking enforcement of lesson code beyond what `make typecheck` already does (strict typing for lessons starts at Lesson 09); lesson 01 code is nonetheless cleanly typed.

## Open items deferred to implementation planning

- Exact wording/voice of slide prose and README concepts paragraphs.
- Whether `make typecheck` should include `lessons/01-hello` paths now or wait until Lesson 09 (default: leave `make typecheck` scoped to tools for now; lesson 01 is trivially typed and not a gate).
- Exact shape of the `ci.yml` lesson-solutions step (reuse `make test` vs a dedicated loop).
