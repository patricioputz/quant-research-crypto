# --- Universe & data ---
CRYPTO_TICKERS = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'ADA-USD',
                  'XRP-USD', 'AVAX-USD', 'DOT-USD', 'LINK-USD', 'DOGE-USD']
EQUITY_TICKERS = [
    # Tech (7)
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META', 'ADBE', 'CRM',
    # Financials (7)
    'JPM', 'BAC', 'GS', 'MS', 'V', 'MA', 'BRK-B',
    # Healthcare (6)
    'UNH', 'JNJ', 'LLY', 'PFE', 'ABBV', 'MRK',
    # Energy (5)
    'XOM', 'CVX', 'COP', 'SLB', 'OXY',
    # Consumer Discretionary (6)
    'AMZN', 'TSLA', 'HD', 'NKE', 'MCD', 'SBUX',
    # Consumer Staples (5)
    'WMT', 'PG', 'KO', 'PEP', 'COST',
    # Industrials (5)
    'BA', 'CAT', 'HON', 'UPS', 'GE',
    # Materials (3)
    'LIN', 'FCX', 'NEM',
    # Utilities (3)
    'NEE', 'DUK', 'SO',
    # Communication Services (3)
    'DIS', 'NFLX', 'CMCSA',
]
COMPARISON_TICK = 'SPY'          # buy-and-hold baseline ticker
START = '2021-01-01'             # data start date

# --- Strategy signal / construction ---
LOOKBACK = 30       # days of trailing momentum to rank on
HOLD = 7            # rebalance every N days
SELECTION_PCT = 0.20  # fraction of the universe held long, and separately held short (0.20 = top/bottom 20%)
N_LONG = max(1, int(len(CRYPTO_TICKERS) * SELECTION_PCT))    # number of crypto assets to long
N_SHORT = max(1, int(len(CRYPTO_TICKERS) * SELECTION_PCT))   # number of crypto assets to short (0 for long-only)
N_LONG_EQUITY = max(1, int(len(EQUITY_TICKERS) * SELECTION_PCT))   # number of equity assets to long
N_SHORT_EQUITY = max(1, int(len(EQUITY_TICKERS) * SELECTION_PCT))  # number of equity assets to short
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
LOOKBACK_VALUES = [15, 30, 45, 60]        # crypto: weeks-scale, matches its faster momentum/reversal cycle
HOLD_VALUES = [3, 7, 14]

EQUITY_LOOKBACK_VALUES = [63, 126, 189, 252]  # equities: 3-12 months, the standard academic momentum window
EQUITY_HOLD_VALUES = [21, 42, 63]             # monthly-ish rebalance — 1-3 month hold, not weekly