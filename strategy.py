import numpy as np
import pandas as pd


def cross_mom_strat(close, returns, lookback, hold, n_long, n_short):
    """Cross-sectional momentum strategy with equal-weighted long/short positions.

    Ranks assets by momentum (past returns), goes long the top performers and
    short the worst performers. Rebalances periodically and holds positions
    until the next rebalance date.

    Args:
        close: DataFrame of asset prices, shape (dates, assets).
        returns: DataFrame of daily returns, shape (dates, assets).
        lookback: Number of days for momentum calculation.
        hold: Rebalance frequency in days.
        n_long: Number of assets to hold long.
        n_short: Number of assets to hold short.

    Returns:
        strat_returns: Series of daily strategy returns.
        positions: DataFrame of position weights for each asset over time.
    """
    n_assets = close.shape[1]

    mom_score = close.pct_change(lookback, fill_method=None).shift(1)

    ranks = mom_score.rank(axis=1, ascending=False)

    longs = ranks <= n_long
    shorts = ranks > (n_assets - n_short)

    positions = pd.DataFrame(0.0, index=close.index, columns=close.columns)

    positions[longs] = 1 / n_long
    positions[shorts] = -1 / n_short

    rebalance_days = close.index[::hold]
    is_rebalance_day = positions.index.isin(rebalance_days)

    positions.loc[~is_rebalance_day] = np.nan
    positions = positions.ffill()

    strat_returns = (positions * returns).sum(axis=1)

    return strat_returns, positions