"""Tests for cli.py: the parser, the three commands, the exit codes.

Every test calls main() with a list of strings -- no terminal, no subprocess.
That is what makes a CLI testable.
"""

import os

import pytest

from exercises.cli import BAD_AMOUNT, BAD_FIELD, NOTHING_FOUND, build_parser, main

SAMPLE_FILE = """\
2026-09-21|rent|1200.00
2026-09-21|groceries|24.50
2026-09-22|groceries|10.25
"""

EXPECTED_LIST = """\
DATE        CATEGORY      AMOUNT
2026-09-21  rent       $1,200.00
2026-09-21  groceries     $24.50
2026-09-22  groceries     $10.25"""

EXPECTED_LIST_GROCERIES = """\
DATE        CATEGORY   AMOUNT
2026-09-21  groceries  $24.50
2026-09-22  groceries  $10.25"""

EXPECTED_REPORT = """\
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00"""


@pytest.fixture
def expenses_path(tmp_path) -> str:
    """A path inside a fresh directory -- the file does not exist yet."""
    return str(tmp_path / "expenses.txt")


@pytest.fixture
def seeded_path(expenses_path: str) -> str:
    """The three sample expenses, already on disk."""
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_FILE)
    return expenses_path


def test_build_parser_defaults_the_file_and_names_the_command() -> None:
    args = build_parser().parse_args(["report"])
    assert args.file == "expenses.txt"
    assert args.command == "report"


def test_add_keeps_the_earlier_expenses(expenses_path: str, capsys) -> None:
    assert main(["--file", expenses_path, "add", "2026-09-21", "rent", "1200"]) == 0
    capsys.readouterr()
    assert main(["--file", expenses_path, "add", "2026-09-21", "groceries", "24.50"]) == 0
    assert capsys.readouterr().out == "Added groceries $24.50 on 2026-09-21.\n"
    with open(expenses_path, encoding="utf-8") as f:
        assert f.read() == "2026-09-21|rent|1200.00\n2026-09-21|groceries|24.50\n"


def test_add_prints_a_confirmation(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "add", "2026-09-21", "groceries", "24.50"])
    assert code == 0
    assert capsys.readouterr().out == "Added groceries $24.50 on 2026-09-21.\n"


@pytest.mark.parametrize("amount", ["lots", "-5", "nan", "1234567890123"])
def test_add_rejects_an_amount_that_is_not_a_plain_number(
    expenses_path: str, capsys, amount: str
) -> None:
    code = main(["--file", expenses_path, "add", "2026-09-21", "groceries", amount])
    assert code == 1
    assert capsys.readouterr().out == BAD_AMOUNT + "\n"
    assert not os.path.exists(expenses_path)


@pytest.mark.parametrize(
    ("date", "category"),
    [
        ("2026-09-21", "food|drink"),
        ("2026-09-21|x", "groceries"),
        ("2026-09-21", "   "),
    ],
)
def test_add_rejects_a_field_that_would_break_the_file(
    expenses_path: str, capsys, date: str, category: str
) -> None:
    code = main(["--file", expenses_path, "add", date, category, "24.50"])
    assert code == 1
    assert capsys.readouterr().out == BAD_FIELD + "\n"
    assert not os.path.exists(expenses_path)


def test_list_prints_a_table_of_every_expense(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_LIST + "\n"


def test_list_filters_by_category(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list", "--category", "groceries"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_LIST_GROCERIES + "\n"


def test_list_on_a_missing_file_says_nothing_found(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "list"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_list_with_an_unknown_category_says_nothing_found(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "list", "--category", "travel"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_report_totals_each_category_in_alphabetical_order(seeded_path: str, capsys) -> None:
    code = main(["--file", seeded_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_REPORT + "\n"


def test_report_on_a_missing_file_says_nothing_found(expenses_path: str, capsys) -> None:
    code = main(["--file", expenses_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == NOTHING_FOUND + "\n"


def test_report_ignores_malformed_lines(expenses_path: str, capsys) -> None:
    with open(expenses_path, "w", encoding="utf-8") as f:
        f.write("junk\n" + SAMPLE_FILE)
    code = main(["--file", expenses_path, "report"])
    assert code == 0
    assert capsys.readouterr().out == EXPECTED_REPORT + "\n"


@pytest.mark.parametrize("argv", [[], ["add", "2026-09-21"]])
def test_a_bad_command_line_exits_with_code_two(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)
    assert exit_info.value.code == 2
