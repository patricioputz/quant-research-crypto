"""Main entry point for cross-momentum strategy backtesting and comparison."""

from engine.config import (
    CRYPTO_TICKERS, EQUITY_TICKERS, COMPARISON_TICK, CRYPTO_C_DAYS, EQUITIES_C_DAYS,
    LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET,
    LOOKBACK_VALUES, HOLD_VALUES,
)
from engine.data import data
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns, buy_and_hold
from engine.metrics import metrics
from engine.reporting import summary_table
from research.sweep import run_sweep
from research.validation import walk_forward_analysis
from research.cross_asset import run_cross_asset, sweep_equities


def main():
    """Run the cross-momentum strategy with fixed parameters and compare against baselines.

    Executes a single momentum strategy configuration, then benchmarks it against:
    - SPY buy-and-hold (equities baseline)
    - Equal-weight crypto buy-and-hold (cross-sectional skill baseline)
    """
    # Load data
    universe_close, universe_returns = data(CRYPTO_TICKERS)

    # Run strategy with configured parameters
    strat_mom_returns, strat_mom_positions = cross_mom_strat(
        universe_close, universe_returns, LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET
    )
    strat_mom_costs = costs(strat_mom_positions)
    strat_mom_pnl = net_pnl(strat_mom_returns, strat_mom_costs)
    mom_performance = compute_cum_returns(strat_mom_pnl)
    mom_sharpe, mom_mdd = metrics(strat_mom_pnl, CRYPTO_C_DAYS, mom_performance)

    # Baseline 1: SPY buy-and-hold (equities market comparison)
    spy_close, spy_returns = data(COMPARISON_TICK)
    spy_performance = buy_and_hold(spy_returns)
    spy_sharpe, spy_mdd = metrics(spy_returns, EQUITIES_C_DAYS, spy_performance)

    # Baseline 2: Equal-weight crypto buy-and-hold (no stock picking, just market exposure)
    # Takes mean return across all assets for each date
    crypto_bh_returns = universe_returns.mean(axis=1)  # type: ignore[call-overload]
    crypto_bh_performance = buy_and_hold(crypto_bh_returns)
    crypto_bh_sharpe, crypto_bh_mdd = metrics(
        crypto_bh_returns, CRYPTO_C_DAYS, crypto_bh_performance
    )

    def section(title):
        print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")

    # Compare strategy against both baselines
    section(f"1. CRYPTO STRATEGY VS. BASELINES  (primary — LOOKBACK={LOOKBACK}, HOLD={HOLD})")
    table = summary_table([
        ("Momentum", mom_sharpe, mom_mdd, mom_performance.iloc[-1]),
        ("SPY B&H", spy_sharpe, spy_mdd, spy_performance.iloc[-1]),
        ("Crypto B&H", crypto_bh_sharpe, crypto_bh_mdd, crypto_bh_performance.iloc[-1]),
    ])
    print(table.to_string(index=False))

    # Parameter sweep: how sensitive is the result to LOOKBACK/HOLD choice?
    section("2. PARAMETER SWEEP  (LOOKBACK x HOLD grid)")
    run_sweep(universe_close, universe_returns, LOOKBACK_VALUES, HOLD_VALUES, N_LONG, N_SHORT)

    # Walk-forward validation: params picked on train data only, scored on held-out test data
    section("3. WALK-FORWARD VALIDATION  (in-sample params -> out-of-sample test)")
    wf_lookback, wf_hold, wf_train_sharpe, wf_test_sharpe, wf_test_mdd, wf_test_final_value = walk_forward_analysis(
        universe_close, universe_returns, N_LONG, N_SHORT, VOL_LOOKBACK
    )
    print(f"Selected on train:  LOOKBACK={wf_lookback}, HOLD={wf_hold}  (train Sharpe {wf_train_sharpe:.2f})")
    print(f"Out-of-sample:      Sharpe {wf_test_sharpe:.2f}, Max DD {wf_test_mdd:.1%}, Final Value {wf_test_final_value:.2f}x")
    print(f"Overfitting gap:    {wf_train_sharpe - wf_test_sharpe:.2f}  (train Sharpe minus test Sharpe)")

    # Cross-asset check: does the same signal work on equities? Naive first
    # (crypto params, unchanged), then with params tuned to equities' own
    # 3-12mo momentum window instead of crypto's weeks-scale one.
    section("4. CROSS-ASSET CHECK  (secondary — momentum on equities; SPY shown in section 1)")
    equity_close, equity_returns = data(EQUITY_TICKERS)
    print("Naive: crypto params, unchanged")
    run_cross_asset(equity_close, equity_returns)

    print("\nEquities-tuned sweep (2-8mo lookback, monthly hold):")
    best_equity = sweep_equities(equity_close, equity_returns)
    print(f"\nBest equities params: LOOKBACK={best_equity['lookback']}, HOLD={best_equity['hold']} "
          f"(Sharpe {best_equity['sharpe']:.2f})")
    run_cross_asset(equity_close, equity_returns, lookback=best_equity['lookback'], hold=best_equity['hold'])
    print()


if __name__ == "__main__":
    main()