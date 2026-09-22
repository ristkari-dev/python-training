"""Plain-text table rendering.

Given code: you do not need to read or change this file. Call it through
``reporting.format_table`` and read that function's docstring.
"""


def format_table(rows: list[list[str]], headers: list[str]) -> str:
    """Render rows as a column-aligned text table and return it as one string.

    ``rows`` is a list of rows; every row is a list of already-formatted
    strings. ``headers`` is a single row of column titles and fixes the column
    count: every row must have exactly as many cells as there are headers, and
    every cell must already be a string (that is what format_money is for).

    Columns are separated by two spaces. Every column is left-aligned except
    the last, which is right-aligned so amounts line up on the decimal point.
    The result has no trailing newline, so ``print()`` it.

        print(format_table([["rent", "$1,200.00"]], ["CATEGORY", "TOTAL"]))
        CATEGORY      TOTAL
        rent      $1,200.00
    """
    for row in [headers, *rows]:
        if len(row) != len(headers):
            raise ValueError(
                f"row {row!r} has {len(row)} cells, but there are {len(headers)} headers"
            )
        for cell in row:
            if not isinstance(cell, str):
                raise ValueError(f"every cell must already be a string, but {cell!r} is not")

    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    last = len(widths) - 1
    lines = []
    for row in [headers, *rows]:
        cells = []
        for index, cell in enumerate(row):
            if index == last:
                cells.append(cell.rjust(widths[index]))
            else:
                cells.append(cell.ljust(widths[index]))
        lines.append("  ".join(cells))
    return "\n".join(lines)
