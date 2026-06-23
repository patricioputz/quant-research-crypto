import numpy as np
import pandas as pd

def cross_mom_strat(close, returns, lookback, hold, n_long, n_short):
    n_assets = close.shape[1]

    #signal
    mom_score = close.pct_change(lookback, fill_method=None).shift(1)

    #ranking
    ranks = mom_score.rank(axis=1, ascending=False)

    #create the mask 
    longs = ranks <= n_long
    shorts = ranks > (n_assets - n_short)

    #df for masks
    positions = pd.DataFrame(0.0, index=close.index, columns=close.columns)

    #add the weights for each
    positions[longs] = 1 / n_long
    positions[shorts] = - 1 / n_short

    #days to take action
    rebalance_days = close.index[::hold]

    # setting dates in positions True when rebalance
    is_rebalance_day = positions.index.isin(rebalance_days)

    #creating an inverse mask and setting non-rebalance days as nan
    positions.loc[~is_rebalance_day] = np.nan

    #forward fill so positions are kept after rebalncing up till next rebalance date
    positions = positions.ffill()

    #returns across each row
    strat_returns = (positions * returns).sum(axis=1)

    return strat_returns, positions