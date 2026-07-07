"""Walk-forward validation: roll train/test windows through the full history,
tuning params on each train window and evaluating only on the unseen test window."""

import pandas as pd
from engine.config import TRAIN_DAYS, TEST_DAYS, GROSS_TARGET, CRYPTO_C_DAYS, LOOKBACK_VALUES, HOLD_VALUES
from research.sweep import run_sweep
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns
from engine.metrics import metrics

def walk_forward_analysis(close, returns, n_long, n_short, vol_lookback):
    """Select lookback/hold on a training window, evaluate on the held-out test window.
    """
    #TRAIN WINDOW
    train_close = close.iloc[:TRAIN_DAYS]
    train_returns = returns.iloc[:TRAIN_DAYS]
    test_close = close.iloc[TRAIN_DAYS : TRAIN_DAYS + TEST_DAYS]
    test_returns = returns.iloc[TRAIN_DAYS : TRAIN_DAYS + TEST_DAYS]

    # Run parameter sweep on the training window to find the best lookback/hold combo
    best = run_sweep(train_close, train_returns, LOOKBACK_VALUES, HOLD_VALUES, n_long, n_short)

    # TEST Apply winning PARAMS from train to test
    test_strat_returns, test_strat_positions = cross_mom_strat(
        test_close, test_returns, best['lookback'], best['hold'], n_long, n_short, vol_lookback, GROSS_TARGET
    )
    test_strat_costs = costs(test_strat_positions)
    test_strat_pnl = net_pnl(test_strat_returns, test_strat_costs)
    test_strat_performance = compute_cum_returns(test_strat_pnl)
    test_strat_sharpe, test_strat_mdd = metrics(test_strat_pnl, CRYPTO_C_DAYS, test_strat_performance)

    return best['lookback'], best['hold'], best['sharpe'], test_strat_sharpe, test_strat_mdd, test_strat_performance.iloc[-1]

if __name__ == "__main__":
    from engine.config import STRAT_MOM_TICKERS, N_LONG, N_SHORT, VOL_LOOKBACK
    from engine.data import data

    universe_close, universe_returns = data(STRAT_MOM_TICKERS)
    best_lb, best_hold, train_sharpe, test_sharpe, test_mdd, test_final_value = walk_forward_analysis(
        universe_close, universe_returns, N_LONG, N_SHORT, VOL_LOOKBACK
    )

    print(f"Selected on train: LOOKBACK={best_lb}, HOLD={best_hold} (train Sharpe {train_sharpe:.3f})")
    print(f"Out-of-sample test: Sharpe {test_sharpe:.3f}, Max DD {test_mdd:.3f}")
    print(f"Overfitting gap: {train_sharpe - test_sharpe:.3f}")