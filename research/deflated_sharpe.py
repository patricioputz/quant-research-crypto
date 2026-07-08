"""Deflated Sharpe ratio: corrects in-sample sweep's best Sharpe for
multiple testing (Bailey & López de Prado, 2014). No external dependencies."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import math
import numpy as np

from engine.config import (
    CRYPTO_TICKERS, LOOKBACK_VALUES, HOLD_VALUES, N_LONG, N_SHORT,
    VOL_LOOKBACK, GROSS_TARGET, CRYPTO_C_DAYS,
)
from engine.data import data
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl
from research.sweep import run_sweep


def norm_ppf(p):
    """Approximate inverse normal CDF."""
    if p < 0 or p > 1:
        raise ValueError(f"p must be in [0, 1], got {p}")
    if p == 0:
        return -10.0
    if p == 1:
        return 10.0
    t = math.sqrt(-2 * math.log(p)) if p < 0.5 else math.sqrt(-2 * math.log(1 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    num = c0 + c1 * t + c2 * t ** 2
    den = 1 + d1 * t + d2 * t ** 2 + d3 * t ** 3
    z = t - num / den
    return -z if p < 0.5 else z


def norm_cdf(z):
    """Approximate normal CDF using error function."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def expected_max_sharpe(trial_sharpes):
    """Expected maximum Sharpe under null of zero skill."""
    n = len(trial_sharpes)
    if n <= 1:
        return 0.0
    sigma = np.std(trial_sharpes, ddof=1)
    gamma = 0.5772156649
    return sigma * ((1 - gamma) * norm_ppf(1 - 1/n) + gamma * norm_ppf(1 - 1/(n*math.e)))


def deflated_sharpe_ratio(obs_daily_sr, trial_sharpes_annualized, n_obs, calendar_days):
    """DSR: probability the true daily Sharpe exceeds the benchmark implied
    by testing multiple parameter combos. trial_sharpes_annualized are
    converted to daily scale so they're comparable to obs_daily_sr —
    mixing annualized and per-period Sharpes silently breaks the z-score."""
    trial_sharpes_daily = [s / math.sqrt(calendar_days) for s in trial_sharpes_annualized]
    benchmark = expected_max_sharpe(trial_sharpes_daily)
    denom = math.sqrt(n_obs - 1)
    z = (obs_daily_sr - benchmark) * denom
    psr = norm_cdf(z)
    return psr, benchmark


def run():
    close, returns = data(CRYPTO_TICKERS)
    best, results = run_sweep(
        close, returns, LOOKBACK_VALUES, HOLD_VALUES, N_LONG, N_SHORT,
        CRYPTO_C_DAYS, verbose=False, return_all=True,
    )
    trial_sharpes = [r['sharpe'] for r in results]

    best_returns, best_positions = cross_mom_strat(
        close, returns, best['lookback'], best['hold'], N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET
    )
    best_pnl = net_pnl(best_returns, costs(best_positions))
    daily_sr = best_pnl.mean() / best_pnl.std()

    psr, benchmark_daily = deflated_sharpe_ratio(daily_sr, trial_sharpes, len(best_pnl), CRYPTO_C_DAYS)
    benchmark_annualized = benchmark_daily * math.sqrt(CRYPTO_C_DAYS)

    print(f"Best in-sample: LOOKBACK={best['lookback']}, HOLD={best['hold']}, Sharpe={best['sharpe']:.3f}")
    print(f"Trials tested: {len(trial_sharpes)}")
    print(f"Expected max Sharpe from noise alone (12 trials): {benchmark_annualized:.3f}")
    print(f"Observed Sharpe clears the noise benchmark by: {best['sharpe'] - benchmark_annualized:.3f}")
    print(f"Deflated Sharpe Ratio (probability real edge > noise benchmark): {psr:.1%}")


if __name__ == "__main__":
    run()
