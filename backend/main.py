from fastapi import FastAPI
import models
from db import engine
from fastapi.middleware.cors import CORSMiddleware
from routes import router

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "General",
        "description": "Health check",
    },
    {
        "name": "Companies",
        "description": "Browse and search NSE-listed companies stored in the local database.",
    },
    {
        "name": "Stock Data",
        "description": "OHLCV price data and computed metrics. Served from PostgreSQL, fetched from yfinance on first request.",
    },
    {
        "name": "Insights",
        "description": "Higher-level analytics — summaries, comparisons, and correlation analysis.",
    },
]

app = FastAPI(
    title="Stock Data Intelligence API",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",     # Swagger UI  → http://localhost:8000/docs
    redoc_url="/redoc",   # ReDoc UI    → http://localhost:8000/redoc
)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stock-frontend-0m9q.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"], summary="Health check")
def greet():
    return "Welcome to Backend of this Fintech project"



