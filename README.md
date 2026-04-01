# Stock Data Intelligence Dashboard

A comprehensive financial data platform that collects, processes, and visualizes NSE (National Stock Exchange) stock market data with real-time charts, stock comparisons, and advanced analytics.

**Live Demo:** [View Dashboard](#) | **API Docs:** [Swagger UI](#)

---

## Overview

This full-stack application provides a complete solution for analyzing Indian stock market data (NSE). Users can:

- **Search** for companies from the NSE listing
- **View** interactive price charts with historical data
- **Analyze** stock metrics (52-week high/low, volatility, moving averages)
- **Compare** multiple stocks to analyze correlation and diversification benefits
- **Explore** detailed stock data in interactive tables

---

## Tech Stack

### Backend
| Component | Technology |
|---|---|
| Framework | FastAPI (Python 3.13) |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Sources | yfinance, NSE API |
| Data Processing | Pandas |
| Server | Uvicorn |

### Frontend
| Component | Technology |
|---|---|
| Framework | React 19 |
| Build Tool | Vite |
| UI Charts | Recharts |
| HTTP Client | Axios |
| Icons | Lucide React |
| Linting | ESLint |

---

## Project Structure

```
.
├── README.md                 # This file
├── docker-compose.yml        # Docker setup
├── render.yaml              # Render.com deployment config
│
├── backend/                 # FastAPI backend
│   ├── main.py             # App entry point
│   ├── routes.py           # API routes
│   ├── services.py         # Business logic
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic response schemas
│   ├── db.py               # Database configuration
│   ├── seed.py             # NSE data seeder
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Docker image
│   ├── docker-compose.yml  # Local dev environment
│   └── README.md           # Backend documentation
│
└── frontend/                # React frontend
    ├── src/
    │   ├── components/     # React components
    │   ├── pages/         # Page components
    │   ├── api/           # API integration
    │   ├── App.jsx        # Root component
    │   ├── main.jsx       # React entry
    │   └── index.css      # Global styles
    ├── public/            # Static assets
    ├── package.json       # Node dependencies
    ├── vite.config.js     # Vite configuration
    └── README.md          # Frontend documentation
```

---

## Quick Start

### Prerequisites

- **Backend:** Python 3.10+, PostgreSQL
- **Frontend:** Node.js 18+

### Option 1: Docker (Backend) + Manual Frontend (Recommended)

**Backend & Database (Docker):**
```bash
cd backend
docker-compose up --build
```

**Frontend (in a new terminal):**
```bash
cd frontend
npm install
npm run dev
```

**Access:**
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Swagger UI: `http://localhost:8000/docs`
- Database: `localhost:5433` (PostgreSQL)

### Option 2: Manual Setup (Everything Locally)

**Backend:**
```bash
cd backend
python -m venv env
source env/bin/activate              # Windows: env\Scripts\activate
pip install -r requirements.txt
# Update DB credentials in db.py
python seed.py                         # Seed NSE companies
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Documentation

- **[Backend README](./backend/README.md)** - API endpoints, data models, setup details
- **[Frontend README](./frontend/README.md)** - Components, features, deployment guide

---

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/companies?startIdx=0` | GET | List NSE companies (paginated) |
| `/search/{name}` | GET | Search stock by company name |
| `/data/{symbol}` | GET | Historical OHLCV + computed metrics |
| `/summary/{symbol}` | GET | 52-week stats and averages |
| `/compare?symbol1=X&symbol2=Y` | GET | Compare two stocks |

See [Backend README](./backend/README.md) for complete API documentation.

---

## Key Features

### 1. Stock Search & Discovery
- Paginated company listing from NSE
- Real-time search with autocomplete
- Company details and listing dates

### 2. Interactive Charts
- Line charts with Recharts
- Responsive design for all devices
- Real-time price data from yfinance

### 3. Stock Analytics
- **Daily Return**: Intraday percentage change
- **Moving Average (MA-7)**: 7-day trend
- **52-Week High/Low**: Year performance bounds
- **Volatility**: 20-day rolling standard deviation
- **Average Close**: Historical price reference

### 4. Stock Comparison
- **Correlation Analysis**: Pearson correlation between two stocks
- **Diversification Score**: 1 - |correlation| (0-1 scale)
- **Insight Labels**: Plain-English interpretation
- **1-Year Chart Data**: Normalized price comparison

### 5. Responsive UI
- Mobile-first design
- Sidebar navigation
- Summary cards with key metrics
- Sortable data tables

---

## 💾 Data Model

### Stocks Table
```sql
id, symbol, name, date_listing
```

### StockData Table
```sql
id, symbol, date, open, close, high, low, volume,
daily_return, ma_7, high_52w, low_52w, volatility, avg_close
```

---

## Data Flow

```
NSE EQUITY_L.csv ──→ seed.py ──→ PostgreSQL (stocks table)
                                      ↓
                              services.py (queries + compute)
                                      ↓
                    yfinance API ──→ StockData table
                                      ↓
                                FastAPI routes
                                      ↓
                                React Frontend
```

---

## Development

### Run Tests
```bash
cd backend
pytest
```

### Lint Code
```bash
cd frontend
npm run lint
```

### Build Frontend
```bash
cd frontend
npm run build
```

---

## Deployment

### Docker
```bash
docker-compose up --build
```

### Render.com
Push to GitHub and Render automatically deploys via `render.yaml`:
```bash
git push origin main
```

### Manual Deployment
- Backend: Python hosting (Render, Railway, Heroku)
- Frontend: Static hosting (Vercel, Netlify, GitHub Pages)
- Database: Managed PostgreSQL (AWS RDS, Render)

---

## Computed Metrics

| Metric | Formula | Use Case |
|---|---|---|
| `daily_return` | `(close - open) / open` | Intraday volatility |
| `ma_7` | 7-day rolling mean | Short-term trend |
| `high_52w` | 252-day rolling max | Annual performance peak |
| `low_52w` | 252-day rolling min | Annual performance trough |
| `volatility` | 20-day rolling std dev | Risk assessment |
| `avg_close` | Mean close price | Price baseline |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open a Pull Request

**Code Guidelines:**
- Follow PEP 8 (Python) and ES6+ (JavaScript)
- Run linting before committing
- Add comments for complex logic
- Test changes thoroughly

---

## Known Limitations

- Stock symbols must include `.NS` suffix (NSE convention)
- Data limited to EQ-series stocks (excludes bonds, ETFs, SMEs)
- yfinance may rate-limit requests during peak hours
- Historical data cached in local database

---

## License

This project is provided as-is for educational and personal use.

---

## Acknowledgments

- **yfinance**: Yahoo Finance data API
- **NSE**: National Stock Exchange of India
- **FastAPI**: Modern Python web framework
- **React**: UI library
- **Recharts**: Charting library

---

## GitHub Checklist

- [x] Complete project structure
- [x] API documentation
- [x] Frontend components documented
- [x] Setup instructions included
- [x] Docker configuration ready
- [x] .gitignore properly configured
- [x] Requirements/dependencies cleaned
- [x] README files comprehensive
- [x] Both backend and frontend READMEs
- [x] Contributing guidelines included

---

## Quick Links

- **Issues**: [Report bugs or request features](../../issues)
- **Pull Requests**: [Contribute code improvements](../../pulls)
- **Discussions**: [Ask questions and share ideas](../../discussions)

---

**Last Updated:** February 2026

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
Searches for a stock by company name using yfinance. Returns the Stock Data.

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