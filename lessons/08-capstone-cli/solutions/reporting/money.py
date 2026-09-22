"""Money formatting.

Given code: you do not need to read or change this file. Call it through
``reporting.format_money`` and read that function's docstring.
"""


def format_money(amount: float) -> str:
    """Format an amount as US dollars with exactly two decimal places.

    Thousands are grouped with commas.

        format_money(24.5)   -> '$24.50'
        format_money(1200)   -> '$1,200.00'
        format_money(0)      -> '$0.00'
    """
    return f"${amount:,.2f}"
