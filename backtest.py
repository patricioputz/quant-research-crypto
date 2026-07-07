import numpy as np
from config import COST_BPS


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


def buy_and_hold(returns):
    """Compute cumulative returns for a buy-and-hold strategy using log returns.

    Caps losses at -99.99% to handle extreme market moves. Uses log returns
    for numerical stability when dealing with leveraged positions.
    """
    capped_returns = returns.clip(lower=-0.9999)
    cum_returns = np.exp(np.log1p(capped_returns).cumsum())
    return cum_returns


def strat_performance(net_pnl):
    """Compute cumulative strategy performance using log returns.

    Caps losses at -99.99% to prevent portfolio value from going negative
    even with leveraged positions. Uses log returns for numerical stability.
    """
    capped_pnl = net_pnl.clip(lower=-0.9999)
    cum_returns_strat = np.exp(np.log1p(capped_pnl).cumsum())
    return cum_returns_strat
