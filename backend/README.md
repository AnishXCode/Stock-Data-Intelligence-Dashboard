# Stock Data Intelligence Dashboard

A mini financial data platform built with **FastAPI + PostgreSQL + React** that collects, processes, and visualises NSE (National Stock Exchange) stock market data.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.13) |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Source | yfinance, NSE EQUITY_L.csv |
| Data Processing | Pandas |
| Server | Uvicorn |

---

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point & route registration
├── routes.py            # All API endpoint definitions
├── services.py          # Business logic (data fetch, compute metrics, queries)
├── models.py            # SQLAlchemy ORM database models
├── schemas.py           # Pydantic request/response validation schemas
├── db.py                # Database connection and session setup
├── seed.py              # One-time database seeder (NSE company list)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image configuration
├── docker-compose.yml   # Local development environment setup
└── README.md            # This file
```

---

## Setup & Installation

### 1. Prerequisites

- Python 3.10+
- PostgreSQL running locally
- Node.js 18+ (for frontend)

### 2. Create the database

```bash
createdb fintech
```

### 3. Install Python dependencies

```bash
cd backend
python -m venv env
source env/bin/activate        # Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure the database URL

In `db.py`, update the connection string to match your Postgres credentials:

```python
DATABASE_URL = "postgresql://your_user:your_password@localhost:5432/fintech"
```

### 5. Seed the database

Fetches all EQ-series companies from NSE and stores them in Postgres. Run this once:

```bash
python seed.py 
```

### 6. Start the API server

```bash
uvicorn main:app --reload
```

API is now live at `http://localhost:8000`
Swagger UI is at `http://localhost:8000/docs`

---

## Docker Setup

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will:
- Build the FastAPI backend
- Start PostgreSQL database
- Run database migrations and seeding
- Expose API on `http://localhost:8000`

### Environment Variables

Create a `.env` file in the backend directory:

```bash
DATABASE_URL=postgresql://postgres:password@db:5432/fintech
PYTHON_ENV=development
```

---

## API Endpoints

### `GET /`
Health check.

**Response:**
```json
"Welcome to Backend of this Fintech project"
```

---

### `GET /companies?startIdx=0`
Returns 30 NSE-listed companies at a time (paginated).

| Query Param | Type | Default | Description |
|---|---|---|---|
| `startIdx` | int | 0 | Offset for pagination |

**Example:** `GET /companies?startIdx=30`

**Response:**
```json
[
  {
    "id": 31,
    "name": "Infosys Limited",
    "symbol": "INFY",
    "date_listing": "11-06-1993"
  }
]
```

---

### `GET /search/{name}`
Searches for a stock by company name using yfinance and fetches stock data

**Example:** `GET /search/infosys`

**Response:**
```json
[
  {
    "id": 882,
    "name": "Infosys Limited",
    "symbol": "INFY",
    "date_listing": "08-FEB-1995"
  }
]
```

---

### `GET /data/{symbol}`
Returns the last 30 days of OHLCV data + computed metrics for a stock.
Checks the local DB first — fetches from yfinance only if not found.

**Example:** `GET /data/INFY.NS`

**Response:**
```json
[
  {
    "id": 1,
    "symbol": "INFY.NS",
    "date": "2026-03-01",
    "open": 1540.0,
    "close": 1558.25,
    "high": 1562.0,
    "low": 1535.5,
    "volume": 4200000,
    "daily_return": 0.0119,
    "ma_7": 1549.3,
    "high_52w": 1950.0,
    "low_52w": 1220.5,
    "volatility": 0.014,
    "avg_close": 1490.0
  }
]
```

---

### `GET /summary/{symbol}`
Returns 52-week high/low and average close for a stock.

**Example:** `GET /summary/INFY.NS`

**Response:**
```json
[
  {
    "id": 1,
    "symbol": "INFY.NS",
    "high_52w": 1950.0,
    "low_52w": 1220.5,
    "avg_close": 1490.0
  }
]
```

---

### `GET /compare?symbol1=INFY.NS&symbol2=TCS.NS`
Compares two stocks over 1 year. Returns normalised price chart data and a correlation analysis.

| Query Param | Type | Required | Description |
|---|---|---|---|
| `symbol1` | string | yes | First stock symbol e.g. `INFY.NS` |
| `symbol2` | string | yes | Second stock symbol e.g. `TCS.NS` |

**Example:** `GET /compare?symbol1=INFY.NS&symbol2=TCS.NS`

**Response:**
```json
{
  "symbol1": "INFY.NS",
  "symbol2": "TCS.NS",
  "correlation": 0.87,
  "correlation_label": "Strongly Positive",
  "insight": "These stocks move together. Diversification benefit is low.",
  "diversification_score": 0.13,
  "chart_data": [
    { "date": "2025-04-01", "s1": 1.000, "s2": 1.000 },
    { "date": "2025-04-02", "s1": 1.012, "s2": 0.998 }
  ]
}
```

---

## Computed Metrics

| Metric | Formula | Description |
|---|---|---|
| `daily_return` | `(close - open) / open` | Intraday return percentage |
| `ma_7` | 7-day rolling mean of close | Short-term trend indicator |
| `high_52w` | Rolling 252-day max of close | 52-week high |
| `low_52w` | Rolling 252-day min of close | 52-week low |
| `volatility` | 20-day rolling std of daily returns | Risk/volatility score |
| `avg_close` | Mean close over stored period | Average price reference |

---

## Custom Feature — Correlation & Diversification Score

The `/compare` endpoint goes beyond basic price comparison. It computes the **Pearson correlation** between two stocks' closing prices over 1 year and returns:

- A **correlation label** (Strongly Positive → Strongly Negative)
- A plain-English **insight** about what the correlation means for an investor
- A **diversification score** = `1 - |correlation|` — the closer to 1.0, the better the two stocks complement each other in a portfolio

This is the custom analytical feature built on top of the required metrics.

---

## Data Flow

```
NSE EQUITY_L.csv ──► seed.py ──► stocks table (company list)

yfinance API ──► services.py ──► StocksData table (OHLCV + metrics)
                     │
                     └──► FastAPI routes ──► React frontend
```

---

## Notes

- Stock symbols must include the `.NS` suffix for NSE (e.g. `INFY.NS`, `TCS.NS`). The `/summary` endpoint auto-appends `.NS` if missing.
- The seeder filters to `SERIES = EQ` only, excluding bonds, ETFs, and SME-listed instruments.
- Data is cached in Postgres — yfinance is only called when a symbol isn't in the local DB.

---

## Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.135.2 | Web framework |
| `uvicorn` | Latest | ASGI server |
| `sqlalchemy` | Latest | ORM for database |
| `psycopg2-binary` | 2.9.11 | PostgreSQL adapter |
| `yfinance` | Latest | Yahoo Finance API |
| `pandas` | 3.0.1 | Data manipulation |
| `requests` | 2.32.3 | HTTP library (NSE API) |
| `certifi` | 2026.2.25 | SSL certificates |

Run `pip install -r requirements.txt` to install all dependencies.

---

## Troubleshooting

### Database Connection Error
**Problem:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
1. Ensure PostgreSQL is running
2. Verify credentials in `db.py`
3. Create database: `createdb fintech`

### yfinance Rate Limiting
**Problem:** `HTTPError 429: Too Many Requests`

**Solution:**
- Data is cached in PostgreSQL after first fetch
- Wait a few minutes and retry
- Limit concurrent requests

### Port Already in Use
**Problem:** `Address already in use (:8000)`

**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Seed Script Fails
**Problem:** Hash or validation errors during `python seed.py`

**Solution:**
```bash
# Clear any partial data and retry
python seed.py --reset
```

---

## Performance Notes

- **Data Caching**: Stock data is cached in PostgreSQL after first fetch to minimize API calls
- **Pagination**: `/companies` endpoint returns 30 records per page
- **Query Optimization**: Use indexes on `symbol` and `date` columns
- **Batch Operations**: Consider pagination when handling large datasets

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit: `git commit -m 'Add new feature'`
5. Push: `git push origin feature/new-feature`
6. Open a Pull Request

**Code Style:**
- Follow PEP 8 (Python style guide)
- Use type hints for function parameters
- Write docstrings for complex functions
- Test all API endpoints

---

## License

This project is provided for educational purposes.