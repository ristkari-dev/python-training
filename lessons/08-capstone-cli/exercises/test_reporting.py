"""Tests for the reporting package.

These two tests pass from your very first run. They are not your work: they
are the documentation for the reporting package you were handed. Read them to
see how to call it.
"""

from exercises.reporting import format_money, format_table

EXPECTED_TABLE = """\
CATEGORY       TOTAL
groceries     $34.75
rent       $1,200.00"""


def test_format_money_shows_two_decimals_and_groups_thousands() -> None:
    assert format_money(24.5) == "$24.50"
    assert format_money(1200) == "$1,200.00"


def test_format_table_left_aligns_all_but_the_last_column() -> None:
    rows = [["groceries", "$34.75"], ["rent", "$1,200.00"]]
    assert format_table(rows, ["CATEGORY", "TOTAL"]) == EXPECTED_TABLE
