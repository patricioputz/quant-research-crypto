"""Main entry point: full research pipeline — strategy vs baselines, sweep,
single-split and rolling walk-forward validation, and a cross-asset check."""

from engine.config import (
    CRYPTO_TICKERS, COMPARISON_TICK, CRYPTO_C_DAYS, EQUITIES_C_DAYS,
    LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET,
    LOOKBACK_VALUES, HOLD_VALUES, TEST_DAYS,
    EQUITY_TICKERS,
)
from engine.data import data
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns
from engine.metrics import metrics
from engine.reporting import summary_table
from research.sweep import run_sweep
from research.validation import walk_forward_analysis
from research.cross_asset import run_cross_asset, sweep_equities


def section(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")


def main():
    universe_close, universe_returns = data(CRYPTO_TICKERS)

    # --- 1. Fixed config vs baselines ---
    section("1. CRYPTO STRATEGY VS. BASELINES  (primary — LOOKBACK={}, HOLD={})".format(LOOKBACK, HOLD))
    strat_returns, strat_positions = cross_mom_strat(
        universe_close, universe_returns, LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET
    )
    strat_costs = costs(strat_positions)
    strat_pnl = net_pnl(strat_returns, strat_costs)
    strat_perf = compute_cum_returns(strat_pnl)
    strat_sharpe, strat_mdd = metrics(strat_pnl, CRYPTO_C_DAYS, strat_perf)

    spy_close, spy_returns = data(COMPARISON_TICK)
    spy_perf = compute_cum_returns(spy_returns)
    spy_sharpe, spy_mdd = metrics(spy_returns, EQUITIES_C_DAYS, spy_perf)

    crypto_bh_returns = universe_returns.mean(axis=1)
    crypto_bh_perf = compute_cum_returns(crypto_bh_returns)
    crypto_bh_sharpe, crypto_bh_mdd = metrics(crypto_bh_returns, CRYPTO_C_DAYS, crypto_bh_perf)

    print(summary_table([
        ("Momentum", strat_sharpe, strat_mdd, strat_perf.iloc[-1]),
        ("SPY B&H", spy_sharpe, spy_mdd, spy_perf.iloc[-1]),
        ("Crypto B&H", crypto_bh_sharpe, crypto_bh_mdd, crypto_bh_perf.iloc[-1]),
    ]))

    # --- 2. Parameter sweep ---
    section("2. PARAMETER SWEEP  (LOOKBACK x HOLD grid)")
    best = run_sweep(universe_close, universe_returns, LOOKBACK_VALUES, HOLD_VALUES, N_LONG, N_SHORT)
    print(f"Best in-sample: LOOKBACK={best['lookback']}, HOLD={best['hold']}, Sharpe={best['sharpe']:.3f}")

    # --- 3 & 4. Walk-forward: rolling only (single-split is a special case, skip duplicating) ---
    section("3. ROLLING WALK-FORWARD VALIDATION  (multiple train/test windows)")
    windows, oos_sharpe, oos_mdd = walk_forward_analysis(
        universe_close, universe_returns, N_LONG, N_SHORT, VOL_LOOKBACK
    )
    print(windows.to_string(index=False))
    print(f"\nNumber of windows:    {len(windows)}")
    print(f"Average train Sharpe: {windows['train_sharpe'].mean():.3f}")
    print(f"Average test Sharpe:  {windows['test_sharpe'].mean():.3f}")
    print(f"Test Sharpe std dev:  {windows['test_sharpe'].std():.3f}")
    print(f"Stitched OOS Sharpe:  {oos_sharpe:.3f}")
    print(f"Stitched OOS Max DD:  {oos_mdd:.3f}")
    print(f"In-sample vs OOS gap: {best['sharpe'] - oos_sharpe:.3f}  (this IS the overfitting)")

    # --- 5. Cross-asset check ---
    section("4. CROSS-ASSET CHECK  (momentum on equities)")
    equity_close, equity_returns = data(EQUITY_TICKERS)

    print("Naive: crypto params, unchanged")
    run_cross_asset(equity_close, equity_returns)

    print("\nEquities-tuned sweep (re-tuned lookback/hold):")
    sweep_equities(equity_close, equity_returns)


if __name__ == "__main__":
    main()