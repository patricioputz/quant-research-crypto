#CONSTANTS

LOOKBACK = 30  # days of trailing momentum to rank on
HOLD     = 7   # rebalance every N days
N_LONG = 3     # number of assets to long
N_SHORT = 3    # number of assets to short (set 0 for long-only)
COST_BPS = 10  # cost basis points
START = '2021-01-01' # data start date
COMPARISON_TICK = 'SPY' # buy and hold ticker baseline
CRYPTO_C_DAYS = 365 # crypto trading days
EQUITIES_C_DAYS = 252 # equities trading days
VOL_LOOKBACK = 30 # days of trailing volatility to scale positions by
 
STRAT_MOM_TICKERS = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'ADA-USD',
                     'XRP-USD', 'AVAX-USD', 'DOT-USD', 'LINK-USD', 'DOGE-USD']