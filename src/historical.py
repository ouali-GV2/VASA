import pandas as pd
import yfinance as yf
import talib
from config import THRESHOLDS

def update_historical(tickers):
    if not tickers:  # Fallback if empty
        return pd.DataFrame()

    df = yf.download(tickers, period='1y', group_by='ticker')

    # Loop over tickers to calculate ATR per ticker
    for ticker in tickers:
        if ticker in df.columns.levels[0]:
            high = df[ticker, 'High'].values
            low = df[ticker, 'Low'].values
            close = df[ticker, 'Close'].values
            df[ticker, 'ATR_day'] = talib.ATR(high, low, close, timeperiod=14)

            # Weekly resample per ticker
            df_ticker = df[ticker].copy()
            df_week = df_ticker.resample('W').agg({'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
            df_week['ATR_week'] = talib.ATR(df_week['High'].values, df_week['Low'].values, df_week['Close'].values, timeperiod=14)
            df_ticker = df_ticker.merge(df_week[['ATR_week']], left_index=True, right_index=True, how='left')
            df_ticker['RVOL'] = df_ticker['Volume'] / df_ticker['Volume'].rolling(20).mean()

            # Filter thresholds
            df_ticker = df_ticker[(df_ticker['RVOL'] > THRESHOLDS['rvol']) & (df_ticker['ATR_day'] > THRESHOLDS['atr']) & (df_ticker['ATR_week'] > THRESHOLDS['atr'] * 1.5)]

            # Update main df
            for col in df_ticker.columns:
                df[ticker, col] = df_ticker[col]

    df.to_csv('data/historical.csv')
    return df




