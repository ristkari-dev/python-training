"""The command line: one parser, one main(), three subcommands.

The three imports below carry a `# noqa: F401` pragma: nothing uses those
names yet, and without it the linter would flag them as unused imports. You
will need every one of them in build_parser() and main() -- delete the
pragmas once you do.
"""

import argparse
import sys

from exercises.expense import Expense, filter_by_category, totals_by_category  # noqa: F401
from exercises.reporting import format_money, format_table  # noqa: F401
from exercises.storage import is_amount, is_field, load_expenses, save_expenses  # noqa: F401

DEFAULT_PATH = "expenses.txt"
NOTHING_FOUND = "No expenses found."
BAD_FIELD = "Date and category must not be empty or contain '|' or a line break."
BAD_AMOUNT = "Amount must be a plain number like 24.50."


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser: a global --file plus three subcommands.

    The parser itself, the global --file option and the subparsers object are
    written out below. Your job is the three subcommands:

      add     three positional arguments -- date, category, amount -- all plain
              strings (main() validates them, so no type= here)
      list    no positionals, one optional --category option
      report  no arguments at all

    Each one starts with `subparsers.add_parser("<name>", help="...")`; the
    README and slide 9 show the `add` block in full. Finish with
    `return parser`.
    """
    parser = argparse.ArgumentParser(
        prog="expenses",
        description="Track expenses in a plain text file.",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_PATH,
        help=f"path to the expenses file (default: {DEFAULT_PATH})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)  # noqa: F841 -- you use it
    raise NotImplementedError("implement build_parser() so the tests pass")


def main(argv: list[str]) -> int:
    """Run one command. Returns the exit code: 0 for success, 1 for a user error.

    argv is the argument list WITHOUT the program name, e.g.
    ["--file", "expenses.txt", "add", "2026-09-21", "groceries", "24.50"].

    The shape:
      1. args = build_parser().parse_args(argv)   (replace the bare call below)
      2. expenses = load_expenses(args.file)
      3. if args.command == "add" / elif "list" / else report
      4. return 0, or 1 when you reject what the user typed

    add     .strip() the date and the category first. print(BAD_FIELD) and
            return 1 when is_field() rejects either of them; print(BAD_AMOUNT)
            and return 1 when is_amount() rejects the amount. Otherwise append
            an Expense to the list you loaded, save the whole list back with
            save_expenses(), and print exactly (the amount goes through
            format_money()):
            Added groceries $24.50 on 2026-09-21.
    list    filter with filter_by_category() when args.category is not None,
            then build one row per expense -- three strings, shaped
            [date, category, format_money(amount)], because format_table only
            aligns strings -- and print(format_table(rows, ["DATE",
            "CATEGORY", "AMOUNT"]))
    report  totals_by_category(), one row per category in `sorted(totals)`
            order, headers ["CATEGORY", "TOTAL"]

    list and report both print(NOTHING_FOUND) when there is nothing to show.
    """
    build_parser().parse_args(argv)
    raise NotImplementedError("implement main() so the tests pass")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
