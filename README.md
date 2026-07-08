# Cross-Sectional Momentum Backtester

**[Live site: cross-sectional-momentum-alpha.vercel.app](https://cross-sectional-momentum-alpha.vercel.app/)**

![Python](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-3.0-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-2.5-013243?logo=numpy&logoColor=white)
![yfinance](https://img.shields.io/badge/data-yfinance-lightgrey)

A crypto and equities momentum strategy, backtested with real risk controls and validated out-of-sample — built to answer one question honestly: does this edge actually exist, or did I just find a good-looking number by accident?

**Key finding:** an in-sample parameter sweep found Sharpe 1.55. Rolling walk-forward validation across 7 windows (2021–2024) showed the real out-of-sample Sharpe averages 0.50, with high variance across regimes. Full writeup: [NOTES.md](NOTES.md).

![Out-of-sample equity curve vs buy-and-hold](research/oos_equity_curve.png)

## What this actually shows

If you look at the chart above and think "buy-and-hold made more money, so the strategy is worse" — that's the natural read, and it's missing the point. Crypto buy-and-hold returned more in this window because crypto went almost straight up for most of 2021–2024; riding that trend with no risk management will beat almost anything in a raw-return contest. But buy-and-hold also had a **-82% max drawdown** along the way (see `main.py` section 1 output) — meaning at some point it lost over four-fifths of its value. Very few people can actually hold through that without selling at the bottom. This strategy's out-of-sample max drawdown was **-22%**, with an average Sharpe of **0.50** (risk-adjusted return — return per unit of volatility taken on). Lower total return, dramatically less pain to get there.

That's the actual comparison: not "which number is bigger" but "which one would you have actually been able to hold, and does the strategy earn its return from a repeatable process rather than from riding one asset class's lucky run." A backtest that just reports the best-looking number and stops (the in-sample sweep here found Sharpe 1.55) is measuring how well you fit noise, not whether the edge is real — that's why every number above is reported out-of-sample, and why the honest answer is "yes, there's a real edge, and it's smaller and choppier than the sweep initially suggested." Full reasoning and every wrong turn: [NOTES.md](NOTES.md).

## What it does

Ranks a universe of assets by trailing momentum, goes long the winners and short the losers, resizes each position by inverse volatility, caps gross exposure at 100%, and force-liquidates any position that blows past a daily loss threshold.

## Architecture
engine/       — shared backtest machinery (data, costs, P&L, metrics)
strategies/   — the actual signal (momentum.py)
research/     — sweep, walk-forward validation, cross-asset testing, NOTES.md
main.py       — runs the full pipeline

## Running it

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Methodology

- No lookahead bias — every signal uses only data available as of the prior day's close
- Costs are real — turnover-based transaction costs, not gross returns
- Sharpe annualized correctly per asset class (√365 crypto, √252 equities)
- Parameters are validated out-of-sample, not just picked off a full-history sweep
- Corrected for multiple testing — the parameter sweep tries 12 combos before picking a winner; deflated Sharpe ratio (Bailey & López de Prado) checks how much of the best in-sample Sharpe (1.12) is separable from the ~0.35 Sharpe you'd expect from noise alone across 12 trials. Result: 96.4% probability the edge is real, not luck from search. See [NOTES.md](NOTES.md).

## Built with

Python · pandas · NumPy · yfinance