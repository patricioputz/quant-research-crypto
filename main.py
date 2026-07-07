"""Main entry point for cross-momentum strategy backtesting and comparison."""

from config import (
    STRAT_MOM_TICKERS, COMPARISON_TICK, CRYPTO_C_DAYS, EQUITIES_C_DAYS,
    LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK
)
from data import data
from strategy import cross_mom_strat
from backtest import costs, net_pnl, strat_performance, buy_and_hold
from metrics import metrics
from reporting import summary_table


def main():
    """Run the cross-momentum strategy with fixed parameters and compare against baselines.

    Executes a single momentum strategy configuration, then benchmarks it against:
    - SPY buy-and-hold (equities baseline)
    - Equal-weight crypto buy-and-hold (cross-sectional skill baseline)
    """
    # Load data
    universe_close, universe_returns = data(STRAT_MOM_TICKERS)

    # Run strategy with configured parameters
    strat_mom_returns, strat_mom_positions = cross_mom_strat(
        universe_close, universe_returns, LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK
    )
    strat_mom_costs = costs(strat_mom_positions)
    strat_mom_pnl = net_pnl(strat_mom_returns, strat_mom_costs)
    mom_performance = strat_performance(strat_mom_pnl)
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

    # Compare strategy against both baselines
    table = summary_table([
        ("Momentum", mom_sharpe, mom_mdd, mom_performance.iloc[-1]),
        ("SPY B&H", spy_sharpe, spy_mdd, spy_performance.iloc[-1]),
        ("Crypto B&H", crypto_bh_sharpe, crypto_bh_mdd, crypto_bh_performance.iloc[-1]),
    ])

    print(table)


if __name__ == "__main__":
    main()