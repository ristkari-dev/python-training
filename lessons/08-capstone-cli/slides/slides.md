## Lesson 08
### Phase 1 capstone: expense tracker CLI

Seven lessons of parts, one program.

Note:
Demo the finished CLI before building it: one add, one list, one report.

---

## What we're building

```console
$ uv run python -m solutions.cli add 2026-09-21 groceries 24.50
Added groceries $24.50 on 2026-09-21.

$ uv run python -m solutions.cli report
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00
```

- `add`, `list`, `report` over one plain text file
- No database, no dependencies — stdlib only

Note:
Run all three live: add, list, report. The file already holds `rent 1200.00` and
`groceries 10.25` from earlier adds — that is why the report totals more than the
one add on the slide. `exercises.cli` still raises `NotImplementedError` today;
that is what they are about to fix.

---

## The shape of a program

```text
expense.py    what an expense is      (imports nothing)
storage.py    where it lives          (imports expense)
reporting/    how it looks            (imports nothing)
cli.py        how you drive it        (imports all three)

expense.py ──┐
storage.py ──┼──▶ cli.py     nothing imports cli.py
reporting/ ──┘
```

- Four units, four test files — build one at a time

---

## A line is a record

```text
2026-09-21|groceries|24.50
```

```python
SEPARATOR = "|"

# write
f"{e.date}{SEPARATOR}{e.category}{SEPARATOR}{e.amount:.2f}"

# read
parts = [p.strip() for p in line.strip().split(SEPARATOR)]
date, category, amount = parts
```

- One constant, so the writer and the reader cannot disagree
- `Expense` is a `@dataclass`; the date is a `str` — no hidden clock

---

## Files: open, read, write

```python
with open(path, encoding="utf-8") as f:
    text = f.read()

with open(path, "w", encoding="utf-8") as f:
    f.write(line + "\n")
```

- `"w"` replaces the file, `"a"` appends
- `write()` does not add the line break — you do
- `text.splitlines()` — no phantom empty last line
- `with` closes the file even when something goes wrong
- *Lesson 13 shows how `with` actually works*

---

## Lines that aren't expenses

- blank line
- too few fields / too many fields
- empty date / empty category
- an amount that is not a plain number: `lots`, `-5.00`

```python
if not os.path.exists(path):   # no file yet? not an error
    return []
```

- `parse_line` returns `None`; the loader skips it
- A plain `if`, not `try`/`except` — that is Lesson 11
- *The skipped line is gone after your next `add` — is that OK?*

---

## A black box you didn't write

```python
from exercises.reporting import format_money, format_table

format_money(1200)                                # '$1,200.00'
print(format_table(rows, ["CATEGORY", "TOTAL"]))  # rows first!
```

- Read the docstring, not the source: `help(format_table)`
- Every cell must already be a string — that is what `format_money` is for
- Its 2 tests are green from your first run: they are its documentation

---

## Money, dates and order

```python
totals[category] = totals.get(category, 0.0) + amount

for name in sorted(totals):
    ...
```

- Money in `float` is a lie — we only *display* it, via `format_money`
- The date is a `str`, so there is no hidden clock and no flaky test
- `sorted(totals)` walks the keys alphabetically (Lesson 05 promised this)
- `d[k] = v` is the half of dicts Lesson 05 did not show

---

## argparse: three subcommands

```python
parser.add_argument("--file", default=DEFAULT_PATH, help="...")
subparsers = parser.add_subparsers(dest="command", required=True)

add = subparsers.add_parser("add", help="record a new expense")
add.add_argument("date", help="the date, e.g. 2026-09-21")
add.add_argument("category", help="the category, e.g. groceries")
add.add_argument("amount", help="the amount, e.g. 24.50")
```

- Positional = required, by position; `--option` = optional, by name
- `--file` is global and goes **first**, before the subcommand
- `--help` is free; a bad command line exits `2`
- *`amount` is a plain string, not `type=float` — whose error message is it?*

---

## `main(argv)` is just a function

```python
def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- A list of strings in, an exit code out
- That is why every test calls `main([...])` — no terminal, no subprocess
- `tmp_path`, `capsys`, `pytest.raises(SystemExit)`
- `0` success · `1` we rejected your value · `2` argparse rejected your command line

---

## Phase 1 in one program

- 01 `print`, `python -m`
- 02 f-strings and format specs (`:.2f`)
- 03 `if` / `for`
- 04 functions and pytest
- 05 comprehensions and `dict.get`
- 06 `@dataclass`
- 07 a package with `__init__.py` re-exports

All of it, in the program you finish today.

---

## Your turn / What's next

- Start: `uv run pytest exercises -q --tb=line` → `39 failed, 2 passed`
- The 2 that pass are the library you were given
- Ladder: `format_line` → `parse_line` → load/save → filter → `build_parser` → `--help`
- Core: storage, `build_parser`, `add`. Stretch: `list`, totals, `report`
- `make test-lesson LESSON=08-capstone-cli` until green

**Next: Phase 2 — Lesson 09, type hints & mypy.**
