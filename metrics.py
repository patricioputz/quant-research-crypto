import numpy as np


def metrics(net_pnl, calendar_days, cum_performance):
    """Compute Sharpe ratio and maximum drawdown from strategy P&L.

    Args:
        net_pnl: Series of daily net P&L returns.
        calendar_days: Number of trading days per year (e.g., 252 for equities, 365 for crypto).
        cum_performance: Series of cumulative strategy value over time.

    Returns:
        sharpe: Annualized Sharpe ratio (excess return per unit of volatility).
        max_dd: Maximum drawdown from peak (negative value, e.g., -0.5 for 50% loss).
    """
    sharpe = net_pnl.mean() / net_pnl.std() * np.sqrt(calendar_days)

    running_max = cum_performance.cummax()
    drawdown = (cum_performance - running_max) / running_max
    max_dd = drawdown.min()

    return sharpe, max_dd