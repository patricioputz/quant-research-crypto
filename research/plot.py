"""Plot the stitched out-of-sample equity curve from rolling walk-forward
against equal-weight buy-and-hold, over the same date range."""

import matplotlib.pyplot as plt
from engine.config import CRYPTO_TICKERS, N_LONG, N_SHORT, VOL_LOOKBACK
from engine.data import data
from engine.backtest import compute_cum_returns
from research.validation import walk_forward_analysis

def plot_oos_vs_buy_and_hold(close, returns, n_long, n_short, vol_lookback):
    """Run rolling walk-forward validation and plot the stitched out-of-sample
    equity curve against equal-weight buy-and-hold.
    """
    windows, oos_sharpe, oos_mdd, oos_performance = walk_forward_analysis(
        close, returns, n_long, n_short, vol_lookback
    )

    bh_returns = returns.mean(axis=1)
    bh_performance = compute_cum_returns(bh_returns)

    plt.figure(figsize=(10, 5))
    plt.plot(oos_performance.index, oos_performance.values, label=f"Strategy (OOS, Sharpe {oos_sharpe:.2f})")
    plt.plot(bh_performance.index, bh_performance.values, label="Equal-Weight Buy & Hold")
    plt.title("Out-of-Sample Strategy Performance vs. Buy & Hold")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Value")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("research/oos_equity_curve.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    universe_close, universe_returns = data(CRYPTO_TICKERS)
    plot_oos_vs_buy_and_hold(universe_close, universe_returns, N_LONG, N_SHORT, VOL_LOOKBACK)