from fastapi import APIRouter, HTTPException, Query
from services import getStockSummary, getStockDataFormatted, getStocksWithName, getCompanies, getComparision

router = APIRouter()

# Get all companies with index to show page wise
@router.get(
    "/companies",
    tags=["Companies"],
    summary="List all NSE companies (paginated)",
)
def companies( startIdx: int = 0):
    return getCompanies(startIdx)


# Find Stock with name
@router.get(
    "/search/{name}",
    tags=["Companies"],
    summary="Search stock by company name",
)
def findStock(name: str):
    symbol = getStocksWithName(name)
    if not symbol:
        raise HTTPException(status_code=404, detail="Stock not found")
    return symbol

# Get Stock data of last 30 days
@router.get(
    "/data/{symbol}",
    tags=["Stock Data"],
    summary="Get last 30 days of OHLCV + metrics",
)
def getData(symbol: str):
    symbol = symbol.upper()
    data = getStockDataFormatted(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this symbol")
    return data


# Summary
@router.get(
    "/summary/{symbol}",
    tags=["Insights"],
    summary="Get 52-week summary for a stock",
)
def summary(symbol: str):
    symbol = symbol.upper()
    data = getStockSummary(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="Summary not available for this symbol")
    return data


# Compare
@router.get(
    "/compare",
    tags=["Insights"],
    summary="Compare two stocks with correlation analysis",
)
def compareStocks(
    symbol1: str = Query(..., description="First stock symbol e.g. INFY.NS"),
    symbol2: str = Query(..., description="Second stock symbol e.g. TCS.NS"),
):
    symbol1, symbol2 = symbol1.upper(), symbol2.upper()
    result = getComparision(symbol1, symbol2)
    if not result or "error" in result:
        raise HTTPException(status_code=404, detail="Could not compare these symbols")
    return result