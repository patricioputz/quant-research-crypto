import numpy as np
from engine.config import COST_BPS


def costs(positions):
    """Calculate transaction costs from position turnover.

    Turnover is measured as the sum of absolute position changes across assets,
    and costs are applied as a fixed basis points fee on turnover.
    """
    turnover = positions.diff().abs().sum(axis=1)
    costs = turnover * (COST_BPS / 10000)
    return costs


def net_pnl(returns, costs):
    """Calculate net P&L by subtracting transaction costs from strategy returns."""
    net_pnl = returns - costs
    return net_pnl


def _compound(returns):
    """Compound a returns series into cumulative growth-of-$1 using log returns.

    Caps losses at -99.99% to prevent cumulative value from hitting zero or
    going negative (which would permanently flatline every day after). Uses
    log returns for numerical stability.
    """
    capped_returns = returns.clip(lower=-0.9999)
    return np.exp(np.log1p(capped_returns).cumsum())


def buy_and_hold(returns):
    """Compute cumulative returns for a buy-and-hold strategy."""
    return _compound(returns)


def compute_cum_returns(returns):
    """Compute cumulative strategy performance from net P&L."""
    return _compound(returns)


def apply_liquidation_threshold(position, returns, threshold):
    """Cap a position's daily P&L contribution at a forced-liquidation threshold.

    Simulates a margin call: if a single position's daily loss exceeds the
    threshold, it's capped there instead of riding to its full (possibly
    unbounded, for a short) loss.
    """
    contribution = position * returns
    return contribution.clip(lower=threshold)
