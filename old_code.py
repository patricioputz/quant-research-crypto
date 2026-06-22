import numpy as np
import pandas as pd
import yfinance as yf
 
#constants
LOOKBACK = 30  # days of trailing momentum to rank on
HOLD     = 7   # rebalance every N days
N_LONG = 3     # number of assets to long
N_SHORT = 3    # number of assets to short (set 0 for long-only)
COST_BPS = 10
START = '2024-01-01'
COMPARISON_TICK = 'SPY'
CRYPTO_C_DAYS = 365
EQUITIES_C_DAYS = 252

# UNIVERSE (Established liquid cryptos)
strat_mom_tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'ADA-USD',
           'XRP-USD', 'AVAX-USD', 'DOT-USD', 'LINK-USD', 'DOGE-USD']

def data(tickers):
    #data download
    df = yf.download(tickers, start=START, auto_adjust=True)

    #data cleaning
    close = df['Close'].dropna(how='all')

    if isinstance(close, pd.DataFrame) and close.shape[1] == 1:
        close = close.squeeze("columns")

    returns = close.pct_change(fill_method=None)
    
    return(close, returns)


def cross_mom_strat(close, returns):
    n_assets = close.shape[1]

    #signal
    mom_score = close.pct_change(LOOKBACK, fill_method=None).shift(1)

    #ranking
    ranks = mom_score.rank(axis=1, ascending=False)

    #create the mask 
    longs = ranks <= N_LONG
    shorts = ranks > (n_assets - N_SHORT)

    #df for masks
    positions = pd.DataFrame(0.0, index=close.index, columns=close.columns)

    #add the weights for each
    positions[longs] = 1 / N_LONG
    positions[shorts] = - 1 / N_SHORT

    #days to take action
    rebalance_days = close.index[::HOLD]

    # setting dates in positions True when rebalance
    is_rebalance_day = positions.index.isin(rebalance_days)

    #creating an inverse mask and setting non-rebalance days as nan
    positions.loc[~is_rebalance_day] = np.nan

    #forward fill so positions are kept after rebalncing up till next rebalance date
    positions = positions.ffill()

    #returns across each row
    strat_returns = (positions * returns).sum(axis=1)

    return strat_returns, positions

def costs(positions):
    #real turnover and transac cost

    turnover = positions.diff().abs().sum(axis=1)
    costs = turnover * (COST_BPS / 10000)
    
    return costs

def net_pnl(returns, costs):
    net_pnl = returns - costs
    return net_pnl


def strat_performance(net_pnl):
    #perfomance 
    cum_returns_strat = (1 + net_pnl).cumprod()

    return cum_returns_strat

def buy_and_hold(returns):

    #comparison
    cum_returns = (1 + returns).cumprod()

    return cum_returns

def metrics(net_pnl, calendar_days, cum_performance):
    #sharpe
    sharpe = net_pnl.mean() / net_pnl.std() * np.sqrt(calendar_days)

    #max DD
    running_max = cum_performance.cummax()
    drawdown = (cum_performance - running_max) / running_max
    max_dd = drawdown.min()
    return sharpe, max_dd

def summary_table(mom_sharpe, mom_mdd, mom_final, base_sharpe, base_mdd, base_final):
    rows = [
        {"Strategy": "Momentum", "Final Value": mom_final, "Sharpe": mom_sharpe, "Max DD": mom_mdd},
        {"Strategy": "SPY B&H",  "Final Value": base_final, "Sharpe": base_sharpe, "Max DD": base_mdd},
    ]
    return pd.DataFrame(rows)


def main():
    #strat momentum crossover
    universe_close, universe_returns = data(strat_mom_tickers)
    strat_mom_returns, strat_mom_positions = cross_mom_strat(universe_close, universe_returns)
    strat_mom_costs = costs(strat_mom_positions)
    strat_mom_pnl = net_pnl(strat_mom_returns, strat_mom_costs)
    mom_performance = strat_performance(strat_mom_pnl)

    
    baseline_close, baseline_returns = data(COMPARISON_TICK)
    baseline_performance = buy_and_hold(baseline_returns)

    mom_sharpe, mom_mdd = metrics(strat_mom_pnl, CRYPTO_C_DAYS, mom_performance)
    base_sharpe, base_mdd = metrics(baseline_returns, EQUITIES_C_DAYS, baseline_performance)
    
    #prints

    table = summary_table(mom_sharpe, mom_mdd, mom_performance.iloc[-1],
                       base_sharpe, base_mdd, baseline_performance.iloc[-1])
    print(table)
    return


    
if __name__ == "__main__": 
    main()