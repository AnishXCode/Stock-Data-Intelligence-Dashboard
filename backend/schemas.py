from pydantic import BaseModel
from datetime import date

class StockSchema(BaseModel):
    id: int
    symbol: str
    name: str
    date: date
    close: float
    open: float
    high: float
    low: float
    volume: int
    daily_return: float
    ma_7: float
    high_52w: float
    low_52w: float
    volatility: float


