"""The command line: one parser, one main(), three subcommands."""

import argparse
import sys

from solutions.expense import Expense, filter_by_category, totals_by_category
from solutions.reporting import format_money, format_table
from solutions.storage import is_amount, is_field, load_expenses, save_expenses

DEFAULT_PATH = "expenses.txt"
NOTHING_FOUND = "No expenses found."
BAD_FIELD = "Date and category must not be empty or contain '|' or a line break."
BAD_AMOUNT = "Amount must be a plain number like 24.50."


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser: a global --file plus three subcommands."""
    parser = argparse.ArgumentParser(
        prog="expenses",
        description="Track expenses in a plain text file.",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_PATH,
        help=f"path to the expenses file (default: {DEFAULT_PATH})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="record a new expense")
    add.add_argument("date", help="the date, e.g. 2026-09-21")
    add.add_argument("category", help="the category, e.g. groceries")
    add.add_argument("amount", help="the amount, e.g. 24.50")

    listing = subparsers.add_parser("list", help="show every expense")
    listing.add_argument("--category", help="only show this category")

    subparsers.add_parser("report", help="show totals per category")

    return parser


def main(argv: list[str]) -> int:
    """Run one command. Returns the exit code: 0 for success, 1 for a user error."""
    args = build_parser().parse_args(argv)
    expenses = load_expenses(args.file)

    if args.command == "add":
        date = args.date.strip()
        category = args.category.strip()
        if not is_field(date) or not is_field(category):
            print(BAD_FIELD)
            return 1
        if not is_amount(args.amount):
            print(BAD_AMOUNT)
            return 1
        amount = float(args.amount)
        expenses.append(Expense(date, category, amount))
        save_expenses(args.file, expenses)
        print(f"Added {category} {format_money(amount)} on {date}.")
    elif args.command == "list":
        if args.category is not None:
            expenses = filter_by_category(expenses, args.category)
        if expenses:
            rows = [[e.date, e.category, format_money(e.amount)] for e in expenses]
            print(format_table(rows, ["DATE", "CATEGORY", "AMOUNT"]))
        else:
            print(NOTHING_FOUND)
    else:
        totals = totals_by_category(expenses)
        if totals:
            rows = [[name, format_money(totals[name])] for name in sorted(totals)]
            print(format_table(rows, ["CATEGORY", "TOTAL"]))
        else:
            print(NOTHING_FOUND)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
