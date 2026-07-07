"""Cross-asset check: does the momentum signal generalize beyond crypto?

Reuses cross_mom_strat unchanged, just pointed at an equities universe with
the equities trading calendar (252 days/year instead of 365).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.config import (
    EQUITY_TICKERS, EQUITIES_C_DAYS, LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET,
    EQUITY_LOOKBACK_VALUES, EQUITY_HOLD_VALUES,
)
from engine.data import data
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns, buy_and_hold
from engine.metrics import metrics
from engine.reporting import summary_table
from research.sweep import run_sweep


def run_cross_asset(close, returns, lookback=LOOKBACK, hold=HOLD):
    """Run the momentum strategy on an equities universe, compare to equal-weight buy-and-hold.

    Defaults to the crypto LOOKBACK/HOLD so a naive "same signal, unchanged"
    check is still possible — but pass equities-tuned params (see
    sweep_equities below) for a fair comparison instead of just reusing
    crypto's faster settings. (SPY is omitted here since it's already shown
    as a baseline in the main crypto comparison.)
    """
    strat_returns, strat_positions = cross_mom_strat(
        close, returns, lookback, hold, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET
    )
    strat_costs = costs(strat_positions)
    strat_pnl = net_pnl(strat_returns, strat_costs)
    strat_performance = compute_cum_returns(strat_pnl)
    strat_sharpe, strat_mdd = metrics(strat_pnl, EQUITIES_C_DAYS, strat_performance)

    equity_bh_returns = returns.mean(axis=1)
    equity_bh_performance = buy_and_hold(equity_bh_returns)
    equity_bh_sharpe, equity_bh_mdd = metrics(equity_bh_returns, EQUITIES_C_DAYS, equity_bh_performance)

    table = summary_table([
        (f"Momentum (equities, LB={lookback}/HOLD={hold})", strat_sharpe, strat_mdd, strat_performance.iloc[-1]),
        ("Equity B&H (equal-weight)", equity_bh_sharpe, equity_bh_mdd, equity_bh_performance.iloc[-1]),
    ])
    print(table.to_string(index=False))
    return table


def sweep_equities(close, returns):
    """Grid-search LOOKBACK/HOLD on equities-appropriate horizons (months, not weeks).

    Crypto's LOOKBACK_VALUES/HOLD_VALUES are weeks-scale and sit in equities'
    short-term reversal zone, not its momentum zone — this sweeps
    EQUITY_LOOKBACK_VALUES/EQUITY_HOLD_VALUES (3-12 months, monthly rebalance)
    instead, with Sharpe annualized on the 252-day equities calendar.
    """
    return run_sweep(close, returns, EQUITY_LOOKBACK_VALUES, EQUITY_HOLD_VALUES, N_LONG, N_SHORT, EQUITIES_C_DAYS)


if __name__ == "__main__":
    equity_close, equity_returns = data(EQUITY_TICKERS)

    print("Naive: crypto params, unchanged")
    run_cross_asset(equity_close, equity_returns)

    print("\nEquities-tuned sweep (3-12mo lookback, monthly hold):")
    best = sweep_equities(equity_close, equity_returns)

    print(f"\nBest equities params: LOOKBACK={best['lookback']}, HOLD={best['hold']} (Sharpe {best['sharpe']:.2f})")
    run_cross_asset(equity_close, equity_returns, lookback=best['lookback'], hold=best['hold'])
