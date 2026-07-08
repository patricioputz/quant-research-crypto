// Single source of truth for every figure rendered on the page.
// Generated from real backtest output — see research/export_site_data.py
// and main.py. Regenerate after any strategy/config change.

export const strategy = {
  eyebrow: "Quant Research",
  name: "Cross-Sectional Momentum",
  oneLiner:
    "A long/short crypto strategy that ranks assets against each other and rotates into relative winners.",
  period: { start: "2021", end: "2026" },
  stats: {
    sharpe: 1.059, // fixed-config, full-history, crypto
    maxDrawdown: -0.327,
    oosSharpeAvg: 0.5, // rolling walk-forward, 7 windows
    oosSharpeStitched: 0.6,
    oosMaxDrawdown: -0.218,
    lookbackDays: 30,
    holdDays: 7,
    costBps: 10,
  },
  universe: [
    "BTC",
    "ETH",
    "SOL",
    "BNB",
    "ADA",
    "XRP",
    "AVAX",
    "DOT",
    "LINK",
    "DOGE",
  ],
  construction: { nLong: 2, nShort: 2 }, // SELECTION_PCT = 0.20 of a 10-name universe
  finding:
    "Crypto buy-and-hold returned more in this window — it also drew down -82%. This strategy's out-of-sample drawdown was -22%, with an average Sharpe of 0.50 across 7 rolling walk-forward windows. Lower total return, dramatically less pain to get there.",
  illustrativeData: false,
  github: "https://github.com/patricioputz/quant-research-crypto",
  author: "Patricio Putz",
} as const;

// Example rebalance snapshot used by the construction diagram (illustrative
// — a representative rebalance shape, not a specific historical date).
export const exampleRanking = [
  { rank: 1, ticker: "SOL", ret: 38.2 },
  { rank: 2, ticker: "AVAX", ret: 24.6 },
  { rank: 3, ticker: "LINK", ret: 19.1 },
  { rank: 4, ticker: "ETH", ret: 11.4 },
  { rank: 5, ticker: "BTC", ret: 8.7 },
  { rank: 6, ticker: "BNB", ret: 3.2 },
  { rank: 7, ticker: "XRP", ret: -2.9 },
  { rank: 8, ticker: "DOT", ret: -8.8 },
  { rank: 9, ticker: "ADA", ret: -14.5 },
  { rank: 10, ticker: "DOGE", ret: -21.4 },
] as const;

// Rolling walk-forward results — 7 non-overlapping windows, 2021-2024.
// Source: research/validation.py::walk_forward_analysis
export const walkForwardWindows = [
  { windowStart: "2021-01", lookback: 30, hold: 3, trainSharpe: 1.6, testSharpe: -1.12 },
  { windowStart: "2021-07", lookback: 15, hold: 7, trainSharpe: 1.25, testSharpe: 2.67 },
  { windowStart: "2021-12", lookback: 30, hold: 7, trainSharpe: 1.15, testSharpe: -0.89 },
  { windowStart: "2022-07", lookback: 45, hold: 14, trainSharpe: 1.72, testSharpe: 0.96 },
  { windowStart: "2022-12", lookback: 45, hold: 14, trainSharpe: 1.57, testSharpe: 1.23 },
  { windowStart: "2023-06", lookback: 15, hold: 7, trainSharpe: 1.94, testSharpe: 0.82 },
  { windowStart: "2023-12", lookback: 15, hold: 7, trainSharpe: 1.61, testSharpe: -0.14 },
] as const;

// Cross-asset check — same signal on a 50-name equities universe.
export const crossAsset = {
  naiveSharpe: -0.22, // crypto params, unchanged
  tunedSharpe: 0.64, // re-swept for equities' 3-12mo momentum horizon
  tunedLookback: 252,
  tunedHold: 21,
  equityBuyHoldSharpe: 1.11,
} as const;

// Multiple testing correction — accounts for testing 12 parameter combos
export const deflatedSharpe = {
  probability: 0.964, // probability observed Sharpe exceeds expected-max-under-null
  trials: 12, // 4 LOOKBACK x 3 HOLD values
  note: "Corrects for 12 independent trials (4 LOOKBACK × 3 HOLD values) before selecting best params — the probability this edge beats what you'd see from noise alone, not just luck from searching multiple combos.",
} as const;
