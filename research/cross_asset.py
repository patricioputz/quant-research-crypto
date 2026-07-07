"""Cross-asset check: does the momentum signal generalize beyond crypto?

Reuses cross_mom_strat unchanged, just pointed at an equities universe with
the equities trading calendar (252 days/year instead of 365).
"""

import sys
from pathlib import Path

# Let this run directly (python research/cross_asset.py) as well as via
# `python -m research.cross_asset` — direct execution doesn't put the
# project root on sys.path, so `engine`/`strategies` won't resolve otherwise.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.config import EQUITY_TICKERS, COMPARISON_TICK, EQUITIES_C_DAYS, LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET
from engine.data import data
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns, buy_and_hold
from engine.metrics import metrics
from engine.reporting import summary_table


def run_cross_asset(close, returns, spy_returns):
    """Run the momentum strategy on an equities universe, compare to SPY buy-and-hold.

    Same LOOKBACK/HOLD/N_LONG/N_SHORT/VOL_LOOKBACK/GROSS_TARGET as the crypto
    run — the point is to see how the identical signal behaves on a different
    asset class, not to re-tune it for equities.
    """
    strat_returns, strat_positions = cross_mom_strat(
        close, returns, LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET
    )
    strat_costs = costs(strat_positions)
    strat_pnl = net_pnl(strat_returns, strat_costs)
    strat_performance = compute_cum_returns(strat_pnl)
    strat_sharpe, strat_mdd = metrics(strat_pnl, EQUITIES_C_DAYS, strat_performance)

    spy_performance = buy_and_hold(spy_returns)
    spy_sharpe, spy_mdd = metrics(spy_returns, EQUITIES_C_DAYS, spy_performance)

    equity_bh_returns = returns.mean(axis=1) 
    equity_bh_performance = buy_and_hold(equity_bh_returns)
    equity_bh_sharpe, equity_bh_mdd = metrics(equity_bh_returns, EQUITIES_C_DAYS, equity_bh_performance)

    table = summary_table([
        ("Momentum (equities)", strat_sharpe, strat_mdd, strat_performance.iloc[-1]),
        ("SPY B&H", spy_sharpe, spy_mdd, spy_performance.iloc[-1]),
        ("Equity B&H (equal-weight)", equity_bh_sharpe, equity_bh_mdd, equity_bh_performance.iloc[-1]),
    ])
    print(table)
    return table


if __name__ == "__main__":
    equity_close, equity_returns = data(EQUITY_TICKERS)
    _, spy_returns = data(COMPARISON_TICK)
    run_cross_asset(equity_close, equity_returns, spy_returns)
