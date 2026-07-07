import numpy as np
import pandas as pd
from config import LIQUIDATION_THRESHOLD


def cross_mom_strat(close, returns, lookback, hold, n_long, n_short, vol_lookback):
    """Cross-sectional momentum strategy with vol-scaled long/short positions.

    Ranks assets by momentum (past returns), goes long the top performers and
    short the worst performers, sized inversely to rolling volatility so each
    position contributes roughly equal risk instead of equal dollar exposure.
    Rebalances periodically and holds positions until the next rebalance date.

    Args:
        close: DataFrame of asset prices, shape (dates, assets).
        returns: DataFrame of daily returns, shape (dates, assets).
        lookback: Number of days for momentum calculation.
        hold: Rebalance frequency in days.
        n_long: Number of assets to hold long.
        n_short: Number of assets to hold short.
        vol_lookback: Number of days for rolling volatility used in sizing.

    Returns:
        strat_returns: Series of daily strategy returns.
        positions: DataFrame of position weights for each asset over time.
    """
    n_assets = close.shape[1]

    mom_score = close.pct_change(lookback, fill_method=None).shift(1)

    ranks = mom_score.rank(axis=1, ascending=False)

    longs = ranks <= n_long
    shorts = ranks > (n_assets - n_short)

    vol = returns.rolling(vol_lookback).std().shift(1)
    inv_vol = 1 / vol

    long_inv_vol = inv_vol.where(longs, 0)
    short_inv_vol = inv_vol.where(shorts, 0)

    long_weights = long_inv_vol.div(long_inv_vol.sum(axis=1), axis=0)
    short_weights = short_inv_vol.div(short_inv_vol.sum(axis=1), axis=0)

    positions = long_weights.fillna(0) - short_weights.fillna(0)

    rebalance_days = close.index[::hold]
    is_rebalance_day = positions.index.isin(rebalance_days)

    positions.loc[~is_rebalance_day] = np.nan
    positions = positions.ffill()

    position_returns = positions * returns
    position_returns_capped = position_returns.clip(lower=LIQUIDATION_THRESHOLD)
    strat_returns = position_returns_capped.sum(axis=1)

    return strat_returns, positions