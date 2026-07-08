"""Walk-forward validation: roll train/test windows through the full history,
tuning params on each train window and evaluating only on the unseen test window."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from engine.config import TRAIN_DAYS, TEST_DAYS, GROSS_TARGET, CRYPTO_C_DAYS, LOOKBACK_VALUES, HOLD_VALUES
from research.sweep import run_sweep
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns
from engine.metrics import metrics

def walk_forward_analysis(close, returns, n_long, n_short, vol_lookback) -> tuple[pd.DataFrame, float, float]:
    """Select lookback/hold on a training window, evaluate on the held-out test window.
    """
    window_results = []
    all_test_pnl = []
    start = 0

    while start + TRAIN_DAYS + TEST_DAYS <= len(close):
        train_close = close.iloc[start : start + TRAIN_DAYS]
        train_returns = returns.iloc[start : start + TRAIN_DAYS]
        test_close = close.iloc[start + TRAIN_DAYS : start + TRAIN_DAYS + TEST_DAYS]
        test_returns = returns.iloc[start + TRAIN_DAYS : start + TRAIN_DAYS + TEST_DAYS]

        best = run_sweep(train_close, train_returns, LOOKBACK_VALUES, HOLD_VALUES, n_long, n_short, verbose=False)

        test_strat_returns, test_strat_positions = cross_mom_strat(
            test_close, test_returns, best['lookback'], best['hold'], n_long, n_short, vol_lookback, GROSS_TARGET
        )
        test_strat_costs = costs(test_strat_positions)
        test_strat_pnl = net_pnl(test_strat_returns, test_strat_costs)
        test_strat_performance = compute_cum_returns(test_strat_pnl)
        test_strat_sharpe, test_strat_mdd = metrics(test_strat_pnl, CRYPTO_C_DAYS, test_strat_performance)

        window_results.append({
            'window_start': close.index[start],
            'lookback': best['lookback'],
            'hold': best['hold'],
            'train_sharpe': best['sharpe'],
            'test_sharpe': test_strat_sharpe,
            'test_mdd': test_strat_mdd,
        })
        all_test_pnl.append(test_strat_pnl)
        start += TEST_DAYS

    oos_pnl = pd.concat(all_test_pnl)
    oos_performance = compute_cum_returns(oos_pnl)
    oos_sharpe, oos_mdd = metrics(oos_pnl, CRYPTO_C_DAYS, oos_performance)

    return pd.DataFrame(window_results), oos_sharpe, oos_mdd, oos_performance

if __name__ == "__main__":
    from engine.config import CRYPTO_TICKERS, N_LONG, N_SHORT, VOL_LOOKBACK
    from engine.data import data

    universe_close, universe_returns = data(CRYPTO_TICKERS)

    windows, oos_sharpe, oos_mdd, oos_performance = walk_forward_analysis(
        universe_close, universe_returns, N_LONG, N_SHORT, VOL_LOOKBACK
    )

    print(windows.to_string(index=False))
    print(f"\nNumber of windows:    {len(windows)}")
    print(f"Average train Sharpe: {windows['train_sharpe'].mean():.3f}")
    print(f"Average test Sharpe:  {windows['test_sharpe'].mean():.3f}")
    print(f"Test Sharpe std dev:  {windows['test_sharpe'].std():.3f}")
    print(f"Stitched OOS Sharpe:  {oos_sharpe:.3f}")
    print(f"Stitched OOS Max DD:  {oos_mdd:.3f}")