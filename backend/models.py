from sqlalchemy import Column, Integer, String, Date, Float
from db import Base

class Stocks(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    symbol = Column(String)
    series = Column(String)
    date_listing = Column(String)

class StockData(Base):
    __tablename__ = "StocksData"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    date = Column(Date)
    close = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    daily_return = Column(Float)
    ma_7 = Column(Float)
    high_52w = Column(Float)
    low_52w = Column(Float)
    volatility = Column(Float)