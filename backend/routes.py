from fastapi import APIRouter, HTTPException
from services import getStockSummary, getStockDataFormatted, getStocksWithName, getCompanies, getComparision

router = APIRouter()

# Get all companies
@router.get("/companies")
def companies(startIndx: int = 0):
    return getCompanies(startIndx)


# Find Stock with name
@router.get("/data/{name}")
def findStock(name: str):
    symbol = getStocksWithName(name)

    if not symbol:
        raise HTTPException(404, "Stock not found")

    return symbol

# Get Stock data of last 30 days
@router.get("/data/{symbol}")
def getData(symbol: str):
    data = getStockDataFormatted(symbol)

    if not data:
        raise HTTPException(404, "No Data found")

    return data


# Summary
@router.get("/summary/{symbol}")
def summary(symbol: str):
    data = getStockSummary(symbol)

    return data


# Compare
@router.get("/compare?symbol1={symbol1}&symbol2={symbol2}")
def compare_stocks(symbol1: str, symbol2: str):
    return getComparision(symbol1, symbol2)