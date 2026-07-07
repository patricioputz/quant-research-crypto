"""Parameter sweep for cross-momentum strategy across lookback and hold periods."""

from itertools import product
from config import STRAT_MOM_TICKERS, CRYPTO_C_DAYS, VOL_LOOKBACK
from data import data
from strategy import cross_mom_strat
from backtest import costs, net_pnl, strat_performance
from metrics import metrics
from reporting import summary_table


def run_sweep():
    """Execute a grid search over lookback and hold period parameters.

    Tests all combinations of lookback (momentum calculation period) and hold
    (rebalance frequency) values. For each combination, computes strategy metrics
    including Sharpe ratio, max drawdown, and final portfolio value.
    """
    universe_close, universe_returns = data(STRAT_MOM_TICKERS)

    lookback_values = [15, 30, 45, 60]
    hold_values = [3, 7, 14]
    n_long = 3
    n_short = 3

    results = []

    for lb, h in product(lookback_values, hold_values):
        strat_mom_returns, strat_mom_positions = cross_mom_strat(
            universe_close, universe_returns, lb, h, n_long, n_short, VOL_LOOKBACK
        )
        strat_mom_costs = costs(strat_mom_positions)
        strat_mom_pnl = net_pnl(strat_mom_returns, strat_mom_costs)
        mom_performance = strat_performance(strat_mom_pnl)
        mom_sharpe, mom_mdd = metrics(strat_mom_pnl, CRYPTO_C_DAYS, mom_performance)

        label = f"LB={lb}, HOLD={h}"
        results.append((label, mom_sharpe, mom_mdd, mom_performance.iloc[-1]))

    table = summary_table(results)
    print(table)


if __name__ == "__main__":
    run_sweep()