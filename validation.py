"""Walk-forward validation: pick params in-sample, test them out-of-sample."""

from itertools import product
from config import (
    TRAIN_DAYS, TEST_DAYS, GROSS_TARGET, WF_LOOKBACK_VALUES, WF_HOLD_VALUES,
    CRYPTO_C_DAYS,
)
from strategy import cross_mom_strat
from backtest import costs, net_pnl, strat_performance
from metrics import metrics


def walk_forward_analysis(close, returns, n_long, n_short, vol_lookback):
    """Select lookback/hold on a training window, evaluate on the held-out test window.

    This is the fix for parameter selection overfitting: `main.py`/`sweep.py`
    pick LOOKBACK/HOLD by eyeballing a sweep run on the *entire* dataset, so the
    "winning" params have already seen the data they're judged on. Here the grid
    search only ever touches the training slice; the test slice is scored once,
    with the params already fixed, so it's a genuine out-of-sample result.

    Args:
        close: DataFrame of asset prices, shape (dates, assets).
        returns: DataFrame of daily returns, shape (dates, assets).
        n_long: Number of assets to hold long.
        n_short: Number of assets to hold short.
        vol_lookback: Number of days for rolling volatility used in sizing.

    Returns:
        best_lookback, best_hold: Params selected on the training window.
        train_sharpe: In-sample Sharpe for the selected params (for comparison).
        test_sharpe, test_mdd: Out-of-sample Sharpe and max drawdown.
    """
    train_close = close.iloc[:TRAIN_DAYS]
    train_returns = returns.iloc[:TRAIN_DAYS]
    test_close = close.iloc[TRAIN_DAYS:TRAIN_DAYS + TEST_DAYS]
    test_returns = returns.iloc[TRAIN_DAYS:TRAIN_DAYS + TEST_DAYS]

    # Grid search on the training window only — test window is never touched here.
    best_sharpe = -float("inf")
    best_lookback, best_hold = WF_LOOKBACK_VALUES[0], WF_HOLD_VALUES[0]

    for lb, h in product(WF_LOOKBACK_VALUES, WF_HOLD_VALUES):
        train_strat_returns, train_positions = cross_mom_strat(
            train_close, train_returns, lb, h, n_long, n_short, vol_lookback, GROSS_TARGET
        )
        train_costs = costs(train_positions)
        train_pnl = net_pnl(train_strat_returns, train_costs)
        train_performance = strat_performance(train_pnl)
        train_sharpe, _ = metrics(train_pnl, CRYPTO_C_DAYS, train_performance)

        if train_sharpe > best_sharpe:
            best_sharpe = train_sharpe
            best_lookback, best_hold = lb, h

    # Apply the winning params, unchanged, to the held-out test window.
    test_strat_returns, test_positions = cross_mom_strat(
        test_close, test_returns, best_lookback, best_hold, n_long, n_short, vol_lookback, GROSS_TARGET
    )
    test_costs = costs(test_positions)
    test_pnl = net_pnl(test_strat_returns, test_costs)
    test_performance = strat_performance(test_pnl)
    test_sharpe, test_mdd = metrics(test_pnl, CRYPTO_C_DAYS, test_performance)

    return best_lookback, best_hold, best_sharpe, test_sharpe, test_mdd


if __name__ == "__main__":
    from config import STRAT_MOM_TICKERS, N_LONG, N_SHORT, VOL_LOOKBACK
    from data import data

    universe_close, universe_returns = data(STRAT_MOM_TICKERS)
    lb, h, train_sharpe, test_sharpe, test_mdd = walk_forward_analysis(
        universe_close, universe_returns, N_LONG, N_SHORT, VOL_LOOKBACK
    )
    print(f"Selected on train: LOOKBACK={lb}, HOLD={h} (train Sharpe {train_sharpe:.3f})")
    print(f"Out-of-sample test: Sharpe {test_sharpe:.3f}, Max DD {test_mdd:.3f}")
