from config import STRAT_MOM_TICKERS, COMPARISON_TICK, CRYPTO_C_DAYS, EQUITIES_C_DAYS
from data import data
from strategy import cross_mom_strat
from backtest import costs, net_pnl, strat_performance, buy_and_hold
from metrics import metrics
from reporting import summary_table

def main():
    #strat momentum crossover
    universe_close, universe_returns = data(STRAT_MOM_TICKERS)
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