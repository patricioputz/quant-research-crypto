"""One-off: generate real equity-curve.csv for the showcase site from actual
backtest output (not illustrative placeholder data). Run with:
  python3 -m research.export_site_data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import csv
from engine.config import (
    CRYPTO_TICKERS, COMPARISON_TICK, LOOKBACK, HOLD, N_LONG, N_SHORT,
    VOL_LOOKBACK, GROSS_TARGET, CRYPTO_C_DAYS, EQUITIES_C_DAYS,
)
from engine.data import data
from strategies.momentum import cross_mom_strat
from engine.backtest import costs, net_pnl, compute_cum_returns, buy_and_hold
from engine.metrics import metrics

universe_close, universe_returns = data(CRYPTO_TICKERS)
strat_returns, strat_positions = cross_mom_strat(
    universe_close, universe_returns, LOOKBACK, HOLD, N_LONG, N_SHORT, VOL_LOOKBACK, GROSS_TARGET
)
strat_pnl = net_pnl(strat_returns, costs(strat_positions))
strat_perf = compute_cum_returns(strat_pnl)
strat_sharpe, strat_mdd = metrics(strat_pnl, CRYPTO_C_DAYS, strat_perf)

spy_close, spy_returns = data(COMPARISON_TICK)
spy_perf = buy_and_hold(spy_returns)

crypto_bh_returns = universe_returns.mean(axis=1)
crypto_bh_perf = buy_and_hold(crypto_bh_returns)

# drawdown series for the strategy
running_max = strat_perf.cummax()
strat_dd = (strat_perf - running_max) / running_max

# align everything to the strategy's dates, forward-filling SPY over weekends
df = strat_perf.to_frame("strategy")
df["cryptoEw"] = crypto_bh_perf
df["spy"] = spy_perf.reindex(df.index).ffill().bfill()
df["strategyDrawdown"] = strat_dd
df = df.dropna()

out_path = Path(__file__).parent.parent / "site" / "data" / "equity-curve.csv"
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "strategy", "cryptoEw", "spy", "strategyDrawdown"])
    for idx, row in df.iterrows():
        writer.writerow([
            idx.strftime("%Y-%m-%d"),
            round(row["strategy"], 4),
            round(row["cryptoEw"], 4),
            round(row["spy"], 4),
            round(row["strategyDrawdown"], 4),
        ])

print(f"wrote {len(df)} rows to {out_path}")
print(f"strategy: Sharpe {strat_sharpe:.3f}, MaxDD {strat_mdd:.3f}, final {strat_perf.iloc[-1]:.2f}x")
print(f"crypto B&H: final {crypto_bh_perf.iloc[-1]:.2f}x")
print(f"SPY: final {spy_perf.iloc[-1]:.2f}x")
