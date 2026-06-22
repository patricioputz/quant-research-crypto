from config import START
import pandas as pd
import yfinance as yf


def data(tickers):
    '''
    downloading data
    '''
    #data download
    df = yf.download(tickers, start=START, auto_adjust=True)
     
    close = df['Close'].dropna(how='all')
     
    if isinstance(close, pd.DataFrame) and close.shape[1] == 1:
        close = close.squeeze('columns')
         
    returns = close.pct_change(fill_method=None)
    
    return close, returns