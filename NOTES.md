# Research Log

Working notes on design decisions, bugs found, and what they actually mean — kept separate from README.md, which is the polished public-facing description. This file is messier on purpose: it's meant to capture reasoning as it happens, including dead ends, so it's easy to reconstruct "why did I do it this way" later (interview prep, future-me, etc.).

---

## 2026-06-23 — Parameter sweep reveals unbounded short-side tail risk (DOGE)

**What happened:** Ran a `LOOKBACK` × `HOLD` grid sweep (`sweep.py`) on the cross-sectional momentum strategy. Most combinations land in a plausible Sharpe range (~0.5–1.05). `LOOKBACK=15` combinations broke badly — negative final portfolio value, max drawdown below -100% (which shouldn't be mathematically possible).

**Root cause:** DOGE moved +355% in a single day while the strategy held it at a -33% short weight. That single position alone contributed roughly -118% to that day's portfolio return. `strat_performance()`/`buy_and_hold()` compound returns via `(1 + r).cumprod()` — this formula is only valid for `r > -1` (a loss can't exceed -100% of capital, in theory). A daily return worse than -100% breaks the compounding math outright: the cumulative product can go negative or collapse to zero permanently (since `0 × anything = 0` for every day after).

**Why this isn't actually a "math bug" to be fixed quietly:** This is the backtest correctly exposing a real, structural risk that the strategy doesn't currently account for — **short positions have theoretically unlimited downside** (unlike longs, capped at -100% when price hits zero). Equal-weighting every asset on the short side, including a famously volatile, sentiment-driven, low-fundamental-value asset like DOGE, means a single news-driven spike can wipe out far more than its allocated weight should "normally" allow.

**Options considered:**
1. **Per-position loss cap / simulated stop-loss** — cap any single position's daily contribution at some realistic liquidation threshold (e.g. -50%), modeling what an exchange's margin system would actually do rather than letting a position ride to -118% unchecked. Most realistic option, not yet implemented.
2. **Filter the short-eligible universe** — exclude low-liquidity / high-volatility / meme-driven assets (DOGE is the obvious example here) from being shortable at all. Mirrors how real funds apply liquidity/volatility screens before including a name in a strategy.
3. **Clip extreme returns as a stopgap** — `net_pnl.clip(lower=-0.9999)`. Prevents the cumulative product from landing exactly on zero (which would permanently flatline the equity curve, since every subsequent day's compounding factor would also be zero) and stops the immediate crash/NaN cascade. **This does not fix the underlying risk** — it only stops the simulation math from breaking when that risk materializes. Implemented for now as a stopgap; the real risk (unbounded short exposure to a single illiquid name) is still unmodeled.

**Current decision:** Using the clip (option 3) to keep the sweep runnable, but treating this as an open item — option 1 (realistic position-level loss cap) is the more correct long-term fix and is on the roadmap.

**Why this matters / interview framing:** Equal weighting silently assumes every asset in the universe carries comparable risk characteristics. It doesn't — and this is a concrete example of where that assumption broke, found via a parameter sweep rather than assumed away. A naive backtest that never tests enough parameter combinations, or never sanity-checks an implausible drawdown number, would have missed this entirely.

---

## Template for future entries

```
## YYYY-MM-DD — Short title of what happened

**What happened:**
**Root cause:**
**Why this matters:**
**Decision / next step:**
```