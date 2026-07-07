"""Parameter sweep for cross-momentum strategy across lookback and hold periods."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from itertools import product
from engine.config import CRYPTO_TICKERS, N_LONG, N_SHORT, LOOKBACK_VALUES, HOLD_VALUES, VOL_LOOKBACK, GROSS_TARGET, CRYPTO_C_DAYS
from engine.data import data
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns
from engine.metrics import metrics
from engine.reporting import summary_table


def run_sweep(close, returns, lookback_values, hold_values, n_long, n_short, calendar_days=CRYPTO_C_DAYS):
    """Execute a grid search over lookback and hold period parameters.

    Tests all combinations of lookback (momentum calculation period) and hold
    (rebalance frequency) values. For each combination, computes strategy metrics
    including Sharpe ratio, max drawdown, and final portfolio value.

    calendar_days controls Sharpe annualization (365 for crypto, 252 for
    equities) — defaults to crypto since that's the primary universe, but
    must be passed explicitly for any other asset class.

    Return the single best combo by Sharpe.
    """
    results = []
    table_rows = []

    for lb, h in product(lookback_values, hold_values):
        strat_mom_returns, strat_mom_positions = cross_mom_strat(
            close, returns, lb, h, n_long, n_short, VOL_LOOKBACK, GROSS_TARGET
        )
        strat_mom_costs = costs(strat_mom_positions)
        strat_mom_pnl = net_pnl(strat_mom_returns, strat_mom_costs)
        mom_performance = compute_cum_returns(strat_mom_pnl)
        mom_sharpe, mom_mdd = metrics(strat_mom_pnl, calendar_days, mom_performance)

        label = f"LB={lb}, HOLD={h}"
        table_rows.append((label, mom_sharpe, mom_mdd, mom_performance.iloc[-1])) # for printing a table of results
        
        results.append({
            'lookback': lb,
            'hold': h,
            'sharpe': mom_sharpe,
            'mdd': mom_mdd,
            'final_value': mom_performance.iloc[-1],
        })


    table = summary_table(table_rows)
    print(table.to_string(index=False))

    # Find the best combination by Sharpe ratio
    best_combo = max(results, key=lambda x: x['sharpe'])
    return best_combo

if __name__ == "__main__":
    universe_close, universe_returns = data(CRYPTO_TICKERS)
    best_params = run_sweep(universe_close, universe_returns, LOOKBACK_VALUES, HOLD_VALUES, N_LONG, N_SHORT)