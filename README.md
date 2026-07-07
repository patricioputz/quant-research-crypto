# Quant Research Engine

A personal research engine for testing systematic trading signals against honest baselines, with rigor on lookahead bias, transaction costs, and risk-adjusted performance.

It's not a single strategy repo — it's a shared backtest/validation harness (`engine/`) that any strategy (`strategies/`) can plug into, so testing a new idea means writing the signal, not rebuilding the pipeline. Roadmap and status are tracked outside this file (not published).

## What's Been Tested So Far

**Strategy: Cross-Sectional Momentum** (`strategies/momentum.py`) — ranks assets against each other by trailing return, goes long the relative winners and short the relative losers, vol-scaled and gross-capped for risk control.

- **Crypto** (10 liquid names: BTC, ETH, SOL, BNB, ADA, XRP, AVAX, DOT, LINK, DOGE) — baselined against SPY buy-and-hold and equal-weight crypto buy-and-hold.
- **Equities** (10 large-caps) — same signal, unchanged parameters, baselined against SPY buy-and-hold and equal-weight equity buy-and-hold. Result: doesn't generalize as-is — crypto-speed params are too fast for how equities momentum actually behaves.
- **Walk-forward validated** — parameters are selected on a training window and scored once, out-of-sample, on a held-out test window, so results aren't just an in-sample-fit artifact.

All parameters live in `engine/config.py` — no magic numbers buried in logic.

## Why Multiple Baselines, Not One

A strategy's raw return means nothing without honest comparison points. Every run checks the result against:

| Comparison | What it isolates |
|---|---|
| **SPY buy-and-hold** | Did this beat the broad equities market at all? |
| **Equal-weight buy-and-hold (same universe)** | Did the *signal* add value, or did it just ride the asset class? |
| **The strategy itself, out-of-sample** | Sharpe and max drawdown on data the parameter selection never saw |

A strategy that beats SPY by riding a bull run isn't skill. A strategy that beats naive buy-and-hold on the same universe, out-of-sample, on a risk-adjusted basis, is a real signal. This repo is built to never confuse the two.

## Methodology Commitments

- **No lookahead bias.** Every signal is computed on data available *as of the prior day's close* (`.shift(1)` on all ranking logic) before being acted on.
- **Costs are real.** Turnover is computed explicitly; returns are reported net of an assumed transaction cost, not gross.
- **Sharpe is annualized correctly per asset class** — √365 for crypto (trades every day), √252 for equities (trades weekdays only).
- **Parameters are validated out-of-sample**, not just picked by eyeballing a full-history sweep.
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
  cross_asset.py          — runs a strategy, unchanged, on a different asset class
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
python3 main.py                    # full pipeline: strategy vs baselines, sweep, walk-forward, cross-asset
python3 -m research.sweep          # sweep only
python3 -m research.validation     # walk-forward only
python3 -m research.cross_asset    # cross-asset check only
```

`research/` scripts are packages, not standalone scripts — run them with `-m` from the project root (not `python3 research/sweep.py`), so the `engine`/`strategies` imports resolve.
