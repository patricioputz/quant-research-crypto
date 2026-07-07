# --- Universe & data ---
STRAT_MOM_TICKERS = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'ADA-USD',
                     'XRP-USD', 'AVAX-USD', 'DOT-USD', 'LINK-USD', 'DOGE-USD']
EQUITY_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',
                  'NVDA', 'JPM', 'XOM', 'UNH', 'V']  # cross-asset comparison universe: 10 liquid large-caps
COMPARISON_TICK = 'SPY'          # buy-and-hold baseline ticker
START = '2021-01-01'             # data start date

# --- Strategy signal / construction ---
LOOKBACK = 30       # days of trailing momentum to rank on
HOLD = 7            # rebalance every N days
N_LONG = 3          # number of assets to long
N_SHORT = 3         # number of assets to short (set 0 for long-only)
VOL_LOOKBACK = 30   # days of trailing volatility used to scale position sizing

# --- Risk controls ---
GROSS_TARGET = 1.0            # target gross exposure (1.0 = no leverage)
LIQUIDATION_THRESHOLD = -0.5  # forced close-out if a position loses more than 50% in a day

# --- Costs ---
COST_BPS = 10  # transaction cost, in basis points, per unit turnover

# --- Calendar / annualization ---
CRYPTO_C_DAYS = 365    # crypto trades every day
EQUITIES_C_DAYS = 252  # equities trade weekdays only

# --- Walk-forward validation ---
TRAIN_DAYS = 365 * 2         # days used to select best params (in-sample)
TEST_DAYS = 365 // 2         # days used to evaluate those params (out-of-sample)

# --- Sweep ---
LOOKBACK_VALUES = [15, 30, 45, 60]
HOLD_VALUES = [3, 7, 14]