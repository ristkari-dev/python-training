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
- `name: str` and `-> str` are type hints — parameter and return type
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
