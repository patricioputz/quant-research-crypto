from config import COST_BPS
    
def costs(positions):
    #real turnover and transac cost

    turnover = positions.diff().abs().sum(axis=1)
    costs = turnover * (COST_BPS / 10000)
    
    return costs