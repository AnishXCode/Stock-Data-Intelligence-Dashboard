import yfinance as yf
import pandas as pd
import numpy as np
from db import Session
from models import StockData, Stocks

def getCompanies(startIndx: int = 0):
    with Session() as session:
        data = session.query(Stocks).order_by(Stocks.id).offset(startIndx).limit(30).all()

        return [
            {
                "id": d.id,
                "name": d.name,
                "symbol": d.symbol,
                "date_listing": d.date_listing
            }
            for d in data
        ]

# Function to search for stocks with name
def getStocksWithName(name: str):
    search = yf.Search(name)
    for obj in search.quotes:
        if obj.get("exchange") == 'NSI':
            return obj["symbol"]

    return search.quotes[0] if search.quotes else None

# Function to download last 30 days of stock data
def getStockData(symbol: str):
    try:
        df = yf.download(symbol, period="1y", interval="1d")
    except:
        print("Error downloading data")
        return None
    
    if df.empty:
        print("No data found")
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)
    df.dropna(subset=['Close', 'Open'],inplace=True)

    df.columns = df.columns.get_level_values(0)
    df['daily_return'] = (df['Close'] - df['Open']) / df['Open']
    df['ma_7'] = df['Close'].rolling(7, min_periods=1).mean()
    df['high_52w'] = df['High'].rolling(252, min_periods=1).max()
    df['low_52w'] = df['Low'].rolling(252, min_periods=1).min()
    df['volatility'] = df['daily_return'].rolling(20, min_periods=1).std()

    df = df.tail(30)

    rows = []

    for _, row in df.iterrows():
        rows.append(StockData(
            symbol = symbol,
            date = row["Date"].date(),
            open = round(float(row["Open"]), 2),
            close = round(float(row["Close"]), 2),
            high = round(float(row["High"]), 2),
            low = round(float(row["Low"]), 2),
            volume = int(row["Volume"]),
            daily_return = round(float(row["daily_return"]), 2),
            ma_7 = round(float(row["ma_7"]), 2),
            high_52w = round(float(row["high_52w"]), 2),
            low_52w = round(float(row["low_52w"]), 2),
            volatility = round(float(row["volatility"]), 2),
        ))
    
    with Session() as session:
        session.query(StockData).filter_by(symbol=symbol).delete()
        session.bulk_save_objects(rows)
        session.commit()

    print("Saved the stock data")
    return df

# Function to send last 30 days of stock data in JSON
def getStockDataFormatted(symbol: str):
    try:
        with Session() as session:
            data = session.query(StockData).filter_by(symbol).all()

            if not data:
                print("No data found in DB, moving to internet")
                data = getStockData(symbol)
            
            return [
                {
                    "id": d.id,
                    "symbol": d.symbol,
                    "date": d.date,
                    "close": d.close,
                    "open": d.open,
                    "high": d.high,
                    "low": d.low,
                    "volume": d.volume,
                    "daily_return": d.daily_return,
                    "ma_7": d.ma_7,
                    "high_52w": d.high_52w,
                    "low_52w": d.low_52w,
                    "volatility": d.volatility
                }
                for d in data
            ]
        
    except:
        print("Failed to send Stock Data")

# Function to return summary of stocks
def getStockSummary(symbol: str):
    try:
        updatedSymbol = False
        for letter in symbol:
            if letter == ".":
                updatedSymbol = True

        if not updatedSymbol:
            symbol = symbol + ".NS"

        with Session() as session:
            data = session.query(StockData).filter_by(symbol=symbol).all()

            if not data:
                print("No data found in DB, moving to internet")
                data = getStockData(symbol)
            
            return [
                {
                    "id": d.id,
                    "symbol": d.symbol,
                    "daily_return": d.daily_return,
                    "ma_7": d.ma_7,
                    "high_52w": d.high_52w,
                    "low_52w": d.low_52w,
                    "volatility": d.volatility
                }
                for d in data
            ]
    except:
        print("Error fetching summary of the stock")
        return None
    
# Function to compare 2 stocks
def getComparision(symbol1: str, symbol2: str):
    stock1 = getStockSummary(symbol1)
    stock2 = getStockSummary(symbol2)

    
            
print(getStockSummary("INFY.NS"))

