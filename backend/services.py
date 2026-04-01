import yfinance as yf
import pandas as pd
import numpy as np
from db import Session
from models import StockData, Stocks

# Function to get All companies
def getCompanies(startIdx):
    with Session() as session:
        data = session.query(Stocks).order_by(Stocks.id).offset(startIdx).limit(30).all()

        return [
            {
                "id": d.id,
                "name": d.name,
                "symbol": d.symbol,
                "date_listing": d.date_listing
            }
            for d in data
        ]

# Function to get searched stock
def getSearchedStock(symbol):
    if "." in symbol:
        symbol = symbol.split(".")[0]

    with Session() as session:
        data = session.query(Stocks).filter_by(symbol=symbol).all()

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
    try:
        search = yf.Search(name)
        for obj in search.quotes:
            if obj.get("exchange") in ['NSI', 'BSE']:
                return obj.get("symbol")
        
        if search.quotes and "symbol" in search.quotes[0]:
            return search.quotes[0]["symbol"]

        return None
    except Exception as e:
        print(f"Error searching stock with name: {e}")
        return None


# Function to download last 30 days of stock data
def getStockData(symbol: str):
    if "." not in symbol:
            symbol = symbol + ".NS"

    try:
        df = yf.download(symbol, period="1y", interval="1d")
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None
    
    if df.empty:
        print("No data found")
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)
    df.dropna(subset=['Close', 'Open'],inplace=True)

    df['daily_return'] = (df['Close'] - df['Open']) / df['Open']
    df['ma_7'] = df['Close'].rolling(7, min_periods=1).mean()
    df['high_52w'] = df['High'].rolling(252, min_periods=1).max()
    df['low_52w'] = df['Low'].rolling(252, min_periods=1).min()
    df['volatility'] = df['daily_return'].rolling(20, min_periods=1).std()
    df['avg_close'] = df['Close'].mean()

    df_copy = df.tail(30)
    rows = []
    for _, row in df_copy.iterrows():
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
            avg_close = round(float(row["avg_close"]), 2)
        ))

    try:
        with Session() as session:
            session.query(StockData).filter_by(symbol=symbol).delete()
            session.bulk_save_objects(rows)
            session.commit()

        print("Saved the stock data")
        return df
    except Exception as e:
        print(f"Error saving data to database: {e}")
        return None

# Function to send last 30 days of stock data in JSON
def getStockDataFormatted(symbol: str):
    if "." not in symbol:
            symbol = symbol + ".NS"
    try:
        with Session() as session:
            data = session.query(StockData).filter_by(symbol=symbol).all()

            if not data:
                print("No data found in DB, moving to internet")
                getStockData(symbol)
                data = session.query(StockData).filter_by(symbol=symbol).all()
            
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
                    "volatility": d.volatility,
                    "avg_close": d.avg_close
                }
                for d in data
            ]
    except Exception as e:
        print(f"Failed to send Stock Data: {e}")

# Function to return summary of stocks
def getStockSummary(symbol: str):
    try:
        if "." not in symbol:
            symbol = symbol + ".NS"

        with Session() as session:
            data = session.query(StockData).filter_by(symbol=symbol).first()

            if not data:
                print("No data found in DB, moving to internet")
                df = getStockData(symbol)

                if df is None or df.empty:
                    return None
                
                last = df.iloc[-1]

                return {
                    "symbol": symbol,
                    "high_52w": round(float(last["high_52w"]), 2),
                    "low_52w": round(float(last["low_52w"]), 2),
                    "avg_close": round(float(df["Close"].mean()), 2)
                }

            
            return {
                "id": data.id,
                "symbol": data.symbol,
                "high_52w": data.high_52w,
                "low_52w": data.low_52w,
                "avg_close": data.avg_close,
            }

    except Exception as e:
        print(f"Error fetching summary of the stock: {e}")
        return None

# function to interpret correlation between 2 stocks
def interpretCorr(corr):
    if corr > 0.7:
        return "Strongly Positive", "These stocks move together. Diversification benefit is low."
    elif corr > 0.3:
        return "Moderately Positive", "Stocks show some correlation."
    elif corr > -0.3:
        return "Weak / No Correlation", "Stocks behave independently. Good for diversification."
    elif corr > -0.7:
        return "Moderately Negative", "Stocks often move in opposite directions."
    else:
        return "Strongly Negative", "Stocks strongly move opposite. Useful hedge." 
     
# Function to compare 2 stocks
def getComparision(symbol1: str, symbol2: str):
    if "." not in symbol1:
            symbol1 = symbol1 + ".NS"
    if "." not in symbol2:
            symbol2 = symbol2 + ".NS"

    try:
        stock1 = yf.download(symbol1, period="1y")
        stock2 = yf.download(symbol2, period="1y")
    except Exception as e:
        print(f"Error downloading data of the stocks: {e}")
        return None

    if isinstance(stock1.columns, pd.MultiIndex):
        stock1.columns = stock1.columns.get_level_values(0)

    if isinstance(stock2.columns, pd.MultiIndex):
        stock2.columns = stock2.columns.get_level_values(0)

    stock1 = stock1[['Close']]
    stock2 = stock2[['Close']]

    merged = pd.merge(
        stock1,
        stock2,
        left_index=True,
        right_index=True,
        suffixes=('_1', '_2')
    )

    if merged.empty:
        return {"error": "No overlapping data"}

    corr = merged['Close_1'].corr(merged['Close_2'])

    label, insight = interpretCorr(corr)

    merged['norm_1'] = merged['Close_1'] / merged['Close_1'].iloc[0]
    merged['norm_2'] = merged['Close_2'] / merged['Close_2'].iloc[0]

    chart_data = [
        {
            "date": str(idx.date()),
            "s1": round(row['norm_1'], 3),
            "s2": round(row['norm_2'], 3)
        }
        for idx, row in merged.iterrows()
    ]

    return {
        "symbol1": symbol1,
        "symbol2": symbol2,
        "correlation": round(float(corr), 3),
        "correlation_label": label,
        "insight": insight,
        "diversification_score": round(1 - abs(corr), 3),
        "chart_data": chart_data
    }


# getComparision("INFY.NS", "ICICIBANK.NS")
