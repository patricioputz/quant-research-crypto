import pandas as pd

def summary_table(mom_sharpe, mom_mdd, mom_final, base_sharpe, base_mdd, base_final):
    rows = [
        {"Strategy": "Momentum", "Final Value": mom_final, "Sharpe": mom_sharpe, "Max DD": mom_mdd},
        {"Strategy": "SPY B&H",  "Final Value": base_final, "Sharpe": base_sharpe, "Max DD": base_mdd},
    ]
    return pd.DataFrame(rows)
