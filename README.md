# Quant Research Crypto

Systematic trading strategy research — backtesting framework for evaluating signal-driven strategies against honest baselines, with rigor on lookahead bias, transaction costs, and risk-adjusted performance.

This isn't a single strategy repo. It's the start of an ongoing research environment: a place to test ideas, validate them properly, and only keep what survives scrutiny.

## Current Strategy: Cross-Sectional Momentum

A long/short strategy that ranks assets against each other by trailing return and rotates into relative winners, away from relative losers.

- **Universe:** 10 liquid cryptocurrencies (BTC, ETH, SOL, BNB, ADA, XRP, AVAX, DOT, LINK, DOGE)
- **Signal:** `LOOKBACK`-day trailing return, ranked cross-sectionally each rebalance
- **Construction:** Long top-N, short bottom-N, equal-weighted within each side
- **Rebalance:** Every `HOLD` days
- **Costs:** Modeled via turnover × assumed bps per trade (not free — every rotation has a price)

All parameters live in `engine/config.py` — no magic numbers buried in logic.

## Why Three Baselines, Not One

A strategy's raw return means nothing without honest comparison points. This framework checks the result against:

| Comparison | What it isolates |
|---|---|
| **SPY buy-and-hold** | Did this beat the equities market at all? |
| **Equal-weight crypto buy-and-hold** | Did the *signal* add value, or did it just ride the crypto asset class? |
| **The strategy itself** | Sharpe and max drawdown, not just total return — risk-adjusted, not vanity metrics |

A strategy that beats SPY by riding a crypto bull run isn't skill. A strategy that beats *naive crypto exposure* on a risk-adjusted basis is a real signal. This repo is built to never confuse the two.

## Methodology Commitments

- **No lookahead bias.** Every signal is computed on data available *as of the prior day's close* (`.shift(1)` on all ranking logic) before being acted on.
- **Costs are real.** Turnover is computed explicitly; returns are reported net of an assumed transaction cost, not gross.
- **Sharpe is annualized correctly per asset class** — √365 for crypto (trades every day), √252 for equities (trades weekdays only).
- **Every number is sanity-checked against intuition** before being trusted — implausibly high Sharpe is treated as a bug signal, not a result to celebrate.

## Architecture

```
engine/                   — shared backtest machinery, used by every strategy
  config.py               — all strategy parameters and constants, single source of truth
  data.py                 — data download + cleaning (yfinance), shape-normalized for 1 or N tickers
  backtest.py             — turnover, transaction costs, net P&L, cumulative performance, liquidation cap
  metrics.py              — Sharpe ratio, max drawdown
  reporting.py            — comparison table across any number of strategies/baselines

strategies/               — the actual signals (the edge)
  momentum.py             — cross-sectional momentum: signal generation + position construction

research/                 — validation tooling, not part of the runtime path
  sweep.py                — grid search over LOOKBACK/HOLD, returns the best combo by Sharpe
  validation.py           — walk-forward validation: params picked on train, scored on held-out test
  NOTES.md                — research log — design decisions, bugs found, what they mean

tests/                    — unit tests (planned)
main.py                   — wires it all together, runs the full pipeline
```

Each file has exactly one job. Adding a new strategy means adding a new file to `strategies/` in the same shape as `momentum.py` and a new entry in `main.py` — the rest of the pipeline (costs, metrics, reporting) doesn't change.

## Running It

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py                    # full pipeline: strategy vs baselines, sweep, walk-forward
python3 -m research.sweep          # sweep only
python3 -m research.validation     # walk-forward only
```

`research/` scripts are packages, not standalone scripts — run them with `-m` from the project root (not `python3 research/sweep.py`), so the `engine`/`strategies` imports resolve.

## Roadmap

This repo is meant to grow. In rough priority order:

- [ ] **Parameter robustness sweep** — grid search over `LOOKBACK`/`HOLD`/`N_LONG`, confirm Sharpe is stable across nearby parameter choices rather than a lucky single configuration
- [ ] **Walk-forward validation** — split history into in-sample (parameter selection) and out-of-sample (true test) windows, rather than testing on the same data used to tune
- [ ] **Equity curve visualization** — plot strategy vs. both baselines over time, not just final summary numbers, to show *when* the edge showed up or disappeared
- [ ] **Cross-asset comparison** — run the identical signal logic on an equities universe, compare whether momentum behaves differently by asset class (and why)
- [ ] **Second independent strategy** — likely mean-reversion or pairs trading, to start reasoning about a multi-strategy portfolio rather than a single signal
- [ ] **Live paper trading integration** — same `strategy.py` logic reused against live data (Alpaca paper account), proving the signal function generalizes beyond historical backtest to a live decision loop

