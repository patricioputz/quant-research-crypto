import pandas as pd


def summary_table(strategies):
    """Format strategy results into a comparison table.

    Args:
        strategies: List of tuples (name, sharpe, max_dd, final_value).

    Returns:
        DataFrame with columns: Strategy, Final Value, Sharpe, Max DD.
    """
    rows = []

    for name, sharpe, mdd, final_val in strategies:
        rows.append({
            "Strategy": name,
            "Final Value": round(final_val, 2),
            "Sharpe": round(sharpe, 2),
            "Max DD": f"{mdd:.1%}",
        })

    return pd.DataFrame(rows)
