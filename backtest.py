from config import COST_BPS

#costs
def costs(positions):
    #real turnover and transac cost

    turnover = positions.diff().abs().sum(axis=1)
    costs = turnover * (COST_BPS / 10000)
    
    return costs

# net pnl 
def net_pnl(returns, costs):
    net_pnl = returns - costs
    return net_pnl

#Perfomance Calculating
def buy_and_hold(returns):
    cum_returns = (1 + returns).cumprod()
    return cum_returns

def strat_performance(net_pnl):
    cum_returns_strat = (1 + net_pnl).cumprod()
    return cum_returns_strat