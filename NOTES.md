# Research Notes

## What I built

A cross-sectional momentum strategy: rank assets by trailing return, long the top N, short the bottom N, rebalance periodically. Started equal-weighted, then added real risk controls — inverse-volatility position sizing (so one high-vol asset like DOGE can't dominate the book), a gross exposure cap (100%, no leverage), and a per-position liquidation threshold (caps any single day's loss at -50%, replacing an earlier stopgap that just clipped extreme returns without addressing the underlying risk).

## The parameter sweep looked great — that was the problem

Grid-searching LOOKBACK (15-60 days) × HOLD (3-14 days) on the full history found a best combo of LOOKBACK=15, HOLD=7, Sharpe 1.55 average across the search. Reporting that number alone would have been the mistake — it's exactly the kind of in-sample-fit number that falls apart under a follow-up question.

## Walk-forward, first attempt: unstable

Split the data into one training window and one held-out test window — tune parameters on train, score once on test. First run: train Sharpe 1.60, test Sharpe -0.03. Second run (same method, slightly different data window as more days accumulated): train Sharpe 1.60, test Sharpe -1.12. Same method, wildly different answer. A single train/test split is too noisy to trust on its own — the walk-forward "result" depended entirely on which 6 months happened to be the test window.

## Rolling walk-forward: the real number

Fixed it by rolling the train/test window forward through the whole history — 7 non-overlapping windows from 2021 to 2024, tuning fresh each time and testing only on unseen data. Results:

| Window start | LOOKBACK | HOLD | Train Sharpe | Test Sharpe |
|---|---|---|---|---|
| 2021-01 | 30 | 3 | 1.60 | -1.12 |
| 2021-07 | 15 | 7 | 1.25 | 2.67 |
| 2021-12 | 30 | 7 | 1.15 | -0.89 |
| 2022-07 | 45 | 14 | 1.72 | 0.96 |
| 2022-12 | 45 | 14 | 1.57 | 1.23 |
| 2023-06 | 15 | 7 | 1.94 | 0.82 |
| 2023-12 | 15 | 7 | 1.61 | -0.14 |

Average test Sharpe: 0.50. Stitched continuous out-of-sample Sharpe (concatenating every window's actual daily P&L into one series): 0.60. Standard deviation of test Sharpe across windows: 1.32 — larger than the mean.

**What this means:** the two single-split runs weren't wrong, they were unlucky/lucky draws from a distribution that actually centers around a modest positive Sharpe. The strategy has a real, if inconsistent, edge — not the 1.55 the naive sweep suggested, and not the near-zero either single split implied on its own. Performance is highly regime-dependent: strongly positive in some 6-month windows (2021 H2: 2.67), strongly negative in others (2021 H1: -1.12).

## Does it generalize to equities?

Ran the identical signal, unchanged crypto parameters (LOOKBACK=30, HOLD=7), on a 50-name equities universe. Sharpe: -0.22. Made sense once I checked the horizon — crypto-tuned parameters sit in equities' short-term reversal zone (1 week to 1 month), not the momentum zone (3-12 months) that actually works for equities, per the standard momentum literature (Jegadeesh-Titman).

Re-swept LOOKBACK/HOLD specifically for equities (3-12 month windows, monthly-ish holds), with the annualization bug fixed (had been using 365 days for equities, which only trade ~252/year — a real bug that overstated Sharpe by roughly 20%). Best: LOOKBACK=252, HOLD=21, Sharpe 0.64. Direction flipped from negative to positive once tuned to the right horizon — still trails equal-weight buy-and-hold (1.11) in this sample, which makes sense: a market-neutral long/short book gives up beta exposure that pure buy-and-hold benefits from in a strong bull run.

## What I still don't know

- Whether the crypto universe's correlation structure (most alts move with BTC) is diluting the "cross-sectional" signal into something closer to a leveraged BTC-beta bet — flagged, not yet measured.
- Whether the liquidation threshold is capping the right thing (per-asset contribution before summing) — needs one more direct check.
- Whether 7 windows is enough to trust the variance estimate, or if it needs a longer history / more granular windows to be conclusive.

## Why this is the actual finding

Most backtests report the best in-sample number and stop. The real finding here isn't "Sharpe 1.55" or "Sharpe 0.60" — it's that naive parameter selection substantially inflates apparent performance, and that inflation is only visible once you validate out-of-sample properly. That gap, and being honest about it, is the point.

## Two refactor bugs that would've crashed silently

Restructured the codebase into `engine/`/`strategies/`/`research/` packages partway through, and refactoring introduced a couple of call-site bugs that only surfaced when I actually ran the full pipeline end-to-end instead of eyeballing the diff:

- `main.py` was calling `sweep_equities(equity_close, equity_returns, N_LONG_EQUITY, N_SHORT_EQUITY)` — but after I'd rewritten `sweep_equities` to take just `(close, returns)`, that call still had two extra positional args left over from an earlier version. Would've been a `TypeError` on the first real run.
- Similarly, `run_cross_asset` was being called with a `spy_returns` Series landing in the `lookback` argument slot (which expects an int) — leftover from before I removed the SPY comparison from that function.

Neither was caught by just reading the code — both only showed up by running `main.py` and watching it fail. Take-away: no type checking on function boundaries and no tests means refactors are only as safe as your last full run. This is basically the argument for the unit tests item still sitting on the roadmap.

## Position count now scales with universe size

Originally `N_LONG`/`N_SHORT` were hardcoded (3 and 3) regardless of how many tickers were in the universe. Once I expanded the equities universe to 50 names, that stopped making sense — 3 long / 3 short out of 50 is a much thinner slice than 3/3 out of 10 crypto names.

Fixed by introducing `SELECTION_PCT = 0.20` and deriving `N_LONG`/`N_SHORT` (and the equities equivalents `N_LONG_EQUITY`/`N_SHORT_EQUITY`) as `max(1, int(len(universe) * SELECTION_PCT))`. Now crypto selects 2 long/2 short out of 10, equities selects 10 long/10 short out of 50 — the position count is always proportional to the universe, not a magic number that only made sense for the original 10-crypto setup.