import numpy as np

def metrics(net_pnl, calendar_days, cum_performance):
    #sharpe
    sharpe = net_pnl.mean() / net_pnl.std() * np.sqrt(calendar_days)

    #max DD
    running_max = cum_performance.cummax()
    drawdown = (cum_performance - running_max) / running_max
    max_dd = drawdown.min()
    return sharpe, max_dd