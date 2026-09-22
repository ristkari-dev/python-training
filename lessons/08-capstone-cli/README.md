# Lesson 08 — Phase 1 capstone: expense tracker CLI

Seven lessons of parts, one program. You build an expense tracker you can actually
run: `add` an expense, `list` what you have, `report` the totals — over a plain
text file you can open in any editor.

## Learning goals

- Split a program across modules whose dependencies point one way.
- Read and write a plain text file with `open`, `read`, `write` and `with`.
- Turn text into objects and back, and decide what to do with input that does not fit.
- Build a subcommand CLI with `argparse` and return a meaningful exit code.
- Use a package you did not write by reading its docstrings, not its source.

## Prereqs

- [Lesson 01 — Hello, Python](../01-hello/README.md),
  [Lesson 02 — Variables, types, operators](../02-variables/README.md),
  [Lesson 03 — Control flow](../03-control-flow/README.md),
  [Lesson 04 — Functions & tests](../04-functions/README.md),
  [Lesson 05 — Collections](../05-collections/README.md),
  [Lesson 06 — Classes & dataclasses](../06-classes/README.md), and
  [Lesson 07 — Modules, packages, imports](../07-modules/README.md).

## Concepts

### The shape of a program

Four units, four ideas, and the arrows point one way:

```text
expense.py    what an expense is      (imports nothing)
storage.py    where it lives          (imports expense)
reporting/    how it looks            (imports nothing)
cli.py        how you drive it        (imports all three)

expense.py ──┐
storage.py ──┼──▶ cli.py     nothing imports cli.py
reporting/ ──┘
```

`cli.py` is the only file that knows about all of them, and nothing imports `cli.py`.
That is what lets you build one unit at a time — and test one unit at a time, with
one test file per module.

### A line is a record

One expense per line, three fields, `|` between them, and the file ends with a newline:

```text
2026-09-21|groceries|24.50
```

`Expense` is a `@dataclass` (Lesson 06) with three fields: `date`, `category`, `amount`.
The date is a plain `str` — real date objects are Lesson 14, and a string keeps the
program free of a hidden clock, which is also why every test is deterministic.

`SEPARATOR = "|"` is a module constant so the writer and the reader literally cannot
disagree: `format_line` joins with it, `parse_line` splits on it. Not JSON, not CSV —
those are Lesson 14, and a format dumb enough to read with `str.split` is what makes the
parsing visible.

### Strings are objects with methods

The first string methods of the course, and `parse_line` and `load_expenses` need
all of them:

```python
"a|b|c".split("|")        # ['a', 'b', 'c']
"  x \n".strip()          # 'x'          — whitespace off both ends
"a\nb\n".splitlines()     # ['a', 'b']   — no phantom empty last element
if line.strip():          # truthiness: a non-empty string is True
date, category, amount = parts      # unpack three items into three names
```

### Files

The recipe — read a whole file, then write one:

```python
with open(path, encoding="utf-8") as f:     # read mode is the default
    text = f.read()

with open(path, "w", encoding="utf-8") as f:
    f.write(line + "\n")                     # write() does NOT add the line break
```

- `"w"` replaces the whole file; `"a"` appends to it.
- You write the newline yourself — that is why `save_expenses` does
  `f.write(format_line(expense) + "\n")`.
- Always pass `encoding="utf-8"` on both ends, so a `café` category survives.
- `f"{amount:.2f}"` (Lesson 02) is what makes the file round-trip: `1200` is stored as
  `1200.00`.

`with` opens the file and guarantees it gets closed when the block ends — even if
something goes wrong inside. That is all you need today. Lesson 13 shows you how `with`
works and how to write your own.

### When there is no file

The first time anyone runs the program there is no file yet. That is not an error, it
means "no expenses yet":

```python
if not os.path.exists(path):
    return []
```

Look before you leap: ask whether the file is there, then read it. Lesson 11 shows the
other style — try it and handle the explosion — and rewrites this exact function.

### Lines that are not expenses

Six shapes are unusable, and `parse_line` returns `None` for every one of them:

1. a blank or whitespace-only line
2. too few fields (`2026-09-21|groceries`)
3. too many fields (`2026-09-21|groceries|24.50|extra`)
4. an empty date (`|groceries|24.50`)
5. an empty category (`2026-09-21||24.50`)
6. an amount that is not a plain number (`lots`, `12,50`, `nan`, `-5.00`)

`load_expenses` skips them, so one bad line never stops your report. There is a
consequence, and it is worth a minute of thought: because `add` does **load → append →
save**, a line the parser skipped is *gone* after your next `add`. Is that the right
behaviour? What should a real program do — back the file up, refuse to save, warn you?

### Validating what the user types

The delimiter you chose is now part of your input contract. `add 2026-09-23 "food|drink" 5`
would otherwise be written as a four-field line and silently discarded forever, so `main`
checks the date and the category with `is_field` and the amount with `is_amount`
**before anything is written**, and returns `1` with a message if either fails.

The same two predicates guard the read side inside `parse_line` — one validator, both
directions, which is why an amount with at most two decimals always reads back exactly
as it was written. (`is_amount` checks the text you typed, not the line that gets
written — *Going further* has the one case where those differ.)
That is also why `amount` is a plain string argument and not `type=float`: with
`type=float`, argparse would accept `nan`, `inf` and `-0`, print a cheerful
confirmation, write a line, and lose it on the next load. Whose error message should
this be — the library's or yours?

### A black box you did not write

`reporting/` is given, complete, and you should not open `money.py` or `table.py`. Call
it through the two names it exports and read *their* docstrings:

```python
from exercises.reporting import format_money, format_table

format_money(1200)                                   # '$1,200.00'
print(format_table(rows, ["CATEGORY", "TOTAL"]))     # rows first, headers second
```

```bash
uv run python -c "from exercises.reporting import format_table; help(format_table)"
```

Every cell you hand `format_table` must already be a string — that is what
`format_money` is for. It takes `(rows, headers)` in that order, left-aligns every
column except the last, and returns one string with no trailing newline, so you
`print()` it.

If you find yourself needing to open `table.py` to know how to call it, that means the
docstring failed. Say so — noticing that is a real code-review skill.

### Ordering output

`sorted(iterable)` returns a new sorted list, and iterating a dict gives its keys, so
`sorted(totals)` is the categories in alphabetical order:

```python
for name in sorted(totals):
    ...
```

(Lesson 05 promised `sorted(...)` "in a later lesson" — here it is.) `list` shows the
file in the order you wrote it; `report` sorts.

### Building a dict by hand

Lesson 05 built dicts with comprehensions and read them with `.get`. Here you need the
write half, `d[k] = v`, inside a plain `for` loop:

```python
totals[category] = totals.get(category, 0.0) + amount
```

`.get(key, default)` is what saves you from "is this the first time I have seen this
category?" — the default *is* the answer.

### argparse

```python
parser = argparse.ArgumentParser(prog="expenses", description="...")
parser.add_argument("--file", default=DEFAULT_PATH, help="...")
subparsers = parser.add_subparsers(dest="command", required=True)

add = subparsers.add_parser("add", help="record a new expense")
add.add_argument("date", help="the date, e.g. 2026-09-21")          # positional

listing = subparsers.add_parser("list", help="show every expense")
listing.add_argument("--category", help="only show this category")   # option
```

- A **positional** is required and named by position; an `--option` is optional and
  named by its flag. `dest="command"` puts the chosen subcommand name in `args.command`.
- `--file` is global: it is declared once on the top-level parser and goes **before**
  the subcommand (like `git -C path status`).
- `--help` comes free, and argparse exits with code `2` on a bad command line — and
  writes that message to stderr, not stdout.

### `main(argv) -> int`

A CLI is just a function that takes a list of strings and returns a number:

```python
def main(argv: list[str]) -> int:
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

`sys.argv[1:]` is the real command line without the program name. Because `main` takes
the list as an argument, every test can call it directly — no terminal, no subprocess,
no monkeypatching. Exit codes: `0` success (including "No expenses found."), `1` a value
we rejected, `2` a bad command line (argparse's own).

### How to read the test files

All of this is given; you never write it.

- `tmp_path` is a pytest fixture: a fresh empty directory per test. `tmp_path /
  "expenses.txt"` builds a path inside it — that `/` is `pathlib`, which is Lesson 14,
  which is why the fixture wraps it in `str(...)` before your code ever sees it. The
  path does **not** exist yet, on purpose: the missing-file branch is the default state.
- A fixture may ask for another fixture: `seeded_path` asks for `expenses_path`, then
  writes the three sample expenses into it.
- `capsys` captures output: `capsys.readouterr().out` is what your program printed.
  Calling it also drains the buffer, which is why a test that calls `main` twice reads
  it in between.
- `pytest.raises` is not a fixture but a `with` block, for the argparse exits:

  ```python
  with pytest.raises(SystemExit) as exit_info:
      main([])
  assert exit_info.value.code == 2
  ```

The tests pin exact output strings — read them as the spec for what you print.

### One new note on types

`parse_line` returns `Expense | None` — "an `Expense` or `None`". The runtime check is
`if expense is not None:`, never `expense != None` (that passes the tests and then fails
`make lint` with `E711`). Types get taught properly in Lesson 09.

### Gotchas

- `--file` goes **before** the subcommand. Putting it after — `... cli list --file
  expenses.txt` — fails with
  `expenses: error: unrecognized arguments: --file expenses.txt` and exit code 2.
- The `# noqa: F401` / `# noqa: F841` comments in `exercises/` mark names that are
  deliberately unused *for now*. Delete a pragma once you use every name on that line.
- A `--file` path whose directory does not exist looks fine to `list` and `report` (they
  print "No expenses found." and exit 0) and then crashes on `add`.
- A file the program cannot read at all still crashes with a traceback — an uncaught
  exception also exits 1, so `echo $?` cannot tell a crash from a rejected value.
  Catching that is Lesson 11.
- Run the commands below from `lessons/08-capstone-cli/`. From the repo root
  `uv run pytest exercises` says `ERROR: file or directory not found: exercises`, and
  `python -m exercises.cli` says `No module named exercises`.

## Exercise

Eight functions, about 70 lines, in this order — inside-out, so you never debug two
unknowns at once:

1. `storage.py` — `format_line`, `parse_line`, `load_expenses`, `save_expenses`
2. `expense.py` — `filter_by_category`, then `totals_by_category`
3. `cli.py` — `build_parser`, then `main`

Your first run says `39 failed, 2 passed`. The 2 that pass are the `reporting` package
you were given — they are its documentation, not your work.

**Core** (what we do together): all four `storage.py` functions, `filter_by_category`,
`build_parser`, and the `add` branch of `main`. That already gives you a program that
takes a real expense, writes a real file and prints a real confirmation.
**Stretch** (self-study): the `list` branch, `totals_by_category`, and the `report`
branch — they only display what `add` already writes.

### The feedback ladder

Run these from `lessons/08-capstone-cli/`. Something goes green every few minutes.

| Step | Command | What you get |
|---|---|---|
| 0 | `uv run pytest exercises -q --tb=line` | `39 failed, 2 passed`, one line each. Open `exercises/test_reporting.py` — those 2 green tests are your library. |
| 1 | `uv run pytest exercises/test_storage.py -k format_line` | **One line of code** goes green. First win inside 3 minutes. |
| 2 | `… -k parse_line` | 10 cases. The parametrized list *is* the spec for bad lines. |
| 3 | `… -k "load or save or round_trip"` | 5 more. Then try it outside pytest: `uv run python -c "from exercises.storage import load_expenses; print(load_expenses('nope.txt'))"` → `[]` |
| 4 | `uv run pytest exercises/test_expense.py -k filter` | 2 more. Pure functions, no I/O — the fastest wins in the lesson. |
| 5 | `uv run pytest exercises/test_cli.py -k build_parser`, then `uv run python -m exercises.cli --help` | 3 more — 23 passing (the `build_parser` case, plus the 2 exit-code cases that reach argparse through `main`'s bare `parse_args`) — and the thing prints real help while `main` still raises. It is a program now. |
| 6 | `… -k add` | 9 cases. The `add` branch of `main` lights its own tests. |
| 7 | `uv run python -m exercises.cli --file my.txt add 2026-09-21 coffee 4.50` | Run your own program. `cat my.txt`. `echo $?`. |
| 8 | self-study: `main`'s `list` branch, then `totals_by_category`, then `main`'s `report` branch | 4 cases, then 2, then 3 — the last 9, and the lesson is green. |

### The worked example: one subcommand

`build_parser` gives you the parser, the global `--file` and the `subparsers` object.
You write the three subcommands. Here is `add` in full — `list` and `report` are yours:

```python
add = subparsers.add_parser("add", help="record a new expense")
add.add_argument("date", help="the date, e.g. 2026-09-21")
add.add_argument("category", help="the category, e.g. groceries")
add.add_argument("amount", help="the amount, e.g. 24.50")
```

`list` takes no positionals and one optional `--category`; `report` takes nothing at
all. Finish with `return parser` (and delete the `raise NotImplementedError` line).

## How to run

From the repo root:

```bash
make test-lesson LESSON=08-capstone-cli
```

Or directly, from `lessons/08-capstone-cli/`:

```bash
uv run pytest exercises -q --tb=line     # your work — 39 failed, 2 passed at the start
uv run pytest exercises/test_storage.py  # one module at a time
uv run pytest solutions                  # the reference — 41 passed
```

Run the finished program (from `lessons/08-capstone-cli/`):

```console
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-21 rent 1200
Added rent $1,200.00 on 2026-09-21.
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-21 groceries 24.50
Added groceries $24.50 on 2026-09-21.
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-22 groceries 10.25
Added groceries $10.25 on 2026-09-22.

$ cat expenses.txt
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
2026-09-22|groceries|10.25

$ uv run python -m solutions.cli --file expenses.txt list
DATE        CATEGORY      AMOUNT
2026-09-21  rent       $1,200.00
2026-09-21  groceries     $24.50
2026-09-22  groceries     $10.25

$ uv run python -m solutions.cli --file expenses.txt list --category groceries
DATE        CATEGORY   AMOUNT
2026-09-21  groceries  $24.50
2026-09-22  groceries  $10.25

$ uv run python -m solutions.cli --file expenses.txt report
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00
```

And the exit codes — `echo $?` right after each command:

```console
$ uv run python -m solutions.cli --file expenses.txt add 2026-09-23 'food|drink' 5.00
Date and category must not be empty or contain '|' or a line break.
$ echo $?
1

$ uv run python -m solutions.cli --file expenses.txt add 2026-09-23 refund -5
Amount must be a plain number like 24.50.
$ echo $?
1

$ uv run python -m solutions.cli --file missing.txt report
No expenses found.
$ echo $?
0

$ uv run python -m solutions.cli --file expenses.txt
usage: expenses [-h] [--file FILE] {add,list,report} ...
expenses: error: the following arguments are required: command
$ echo $?
2

$ uv run python -m solutions.cli list --file expenses.txt     # --file in the wrong place
usage: expenses [-h] [--file FILE] {add,list,report} ...
expenses: error: unrecognized arguments: --file expenses.txt
$ echo $?
2
```

Read the given package's documentation without opening it:

```bash
uv run python -c "from solutions.reporting import format_table; help(format_table)"
```

## Going further

- Add a grand-total row to `report` — the table aligns it for you.
- `open(path, "a")` appends. Make `add` use it, and say what you lose.
- A skipped line disappears on the next `add`. Fix it: back the file up, refuse to save,
  or warn.
- Real CLIs send errors to stderr: `print(msg, file=sys.stderr)`. Why is that better?
- Money in `float` is a lie (`0.1 + 0.2`). Try `add … tip 0.005` and `add … tip 1.005` —
  they are stored as `0.01` and `1.00`, so what you typed is not what comes back. Where
  did your half-cent go, and why did the two round in opposite directions?
  `decimal.Decimal` is the real answer.
- `str.isdigit()` vs `isdecimal()` vs `isnumeric()` — why `is_amount` uses `isdecimal`
  (`"²".isdigit()` is `True`, but `float("²")` raises). Then read the other half of
  `is_amount`: it counts the digits *before* the point because `format_line` writes the
  rounded float, so the cap bounds the written field and keeps `float()` nowhere near
  `inf` (`float("9" * 400)` is `inf`, and `f"{inf:.2f}"` writes the literal `inf`, which
  no `load` will take back). But the cap checks the text you *typed*, not the line that
  gets *written* — try `add 2026-09-21 rent 999999999999.999`. It prints
  `Added rent $1,000,000,000,000.00 on 2026-09-21.`, writes thirteen digits, and then
  `list` says `No expenses found.` and your next `add` deletes the line. Where should
  that check go instead?
- `format_table` raises `ValueError` on a ragged row — a real library validates its
  input. Catching that is Lesson 11.
- `argparse`: `type=`, `choices=`, `nargs=`, mutually exclusive groups, `%(prog)s`.
- `console_scripts` in `pyproject.toml` turn `main` into a real `expenses` command
  (Lesson 15). Real dates (`datetime`) and real paths (`pathlib`) — Lesson 14.
