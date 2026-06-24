from config import START
import pandas as pd
import yfinance as yf


def data(tickers):
    """Download historical price data and compute returns.

    Fetches adjusted closing prices from Yahoo Finance starting from the
    configured date. Handles both single and multiple ticker cases.

    Args:
        tickers: List of ticker symbols or single ticker string.

    Returns:
        close: DataFrame (or Series if single ticker) of adjusted closing prices.
        returns: DataFrame (or Series) of daily percentage returns.
    """
    df = yf.download(tickers, start=START, auto_adjust=True)

    close = df['Close'].dropna(how='all')

    if isinstance(close, pd.DataFrame) and close.shape[1] == 1:
        close = close.squeeze('columns')

    returns = close.pct_change(fill_method=None)

    return close, returns