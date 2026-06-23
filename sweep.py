from itertools import product
from config import STRAT_MOM_TICKERS, CRYPTO_C_DAYS
from data import data
from strategy import cross_mom_strat
from backtest import costs, net_pnl, strat_performance
from metrics import metrics
from reporting import summary_table

def run_sweep():
    universe_close, universe_returns = data(STRAT_MOM_TICKERS)
    
    lookback_values = [15, 30, 45, 60]
    hold_values = [3, 7, 14]
    n_long = 3
    n_short = 3

    results = []
    
    for lb, h in product(lookback_values, hold_values):
        strat_mom_returns, strat_mom_positions = cross_mom_strat(universe_close, universe_returns, LOOKBACK, HOLD, N_LONG, N_SHORT)
    