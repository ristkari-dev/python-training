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
like `"Hello, Aki!"`. Both tests in `exercises/test_hello.py` must pass. Run the
tests first to see them fail, implement `greet`, then run the tests again until
they pass. Once the tests are green, run the file as a program to greet yourself
interactively (running the greeter before you implement `greet` will raise a
`NotImplementedError` — that is expected).

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
