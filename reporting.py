import pandas as pd

def summary_table(strategies):
    rows = []
    
    for name, sharpe, mdd, final_val in strategies:
        rows.append({"Strategy": name, "Final Value": final_val, "Sharpe": sharpe, "Max DD": mdd})
    return pd.DataFrame(rows)
