# Stock Data Intelligence Dashboard - Frontend

A modern React-based frontend for visualizing and comparing NSE (National Stock Exchange) stock market data. This dashboard provides interactive charts, company search, stock comparisons, and detailed data tables.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | React 19.2.4 |
| Build Tool | Vite 8.0.1 |
| HTTP Client | Axios 1.13.6 |
| Charts | Recharts 3.8.1 |
| Icons | Lucide React 1.7.0 |
| Linting | ESLint 9.39.4 |
| Styling | CSS3 |

---

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   └── Dashboard.jsx       # Main dashboard page
│   ├── components/
│   │   ├── Sidebar.jsx         # Company selector sidebar
│   │   ├── StockChart.jsx      # Interactive price chart
│   │   ├── SummaryCard.jsx     # Stock summary statistics
│   │   ├── CompareView.jsx     # Multi-stock comparison
│   │   └── DataTable.jsx       # Detailed stock data table
│   ├── api/
│   │   ├── api.js              # Axios instance configuration
│   │   └── routes.js           # API route functions
│   ├── App.jsx                 # Root component
│   ├── main.jsx                # React DOM entry point
│   └── index.css               # Global styles
├── public/                      # Static assets
├── index.html                  # HTML entry point
├── package.json                # Dependencies and scripts
├── vite.config.js              # Vite configuration
└── eslint.config.js            # ESLint rules
```

---

## Features

### Dashboard
- **Stock Search**: Search and select stocks from the NSE company list
- **Interactive Charts**: Visualize stock price trends with Recharts
- **Summary Cards**: Display key metrics (current price, high, low, change percentage)
- **Data Table**: View detailed historical stock data
- **Compare View**: Compare multiple stocks side-by-side

### Components
- **Sidebar**: Browse companies with pagination
- **StockChart**: Line chart with responsive design
- **SummaryCard**: Key statistics display
- **CompareView**: Multi-stock comparison interface
- **DataTable**: Sortable and filterable stock data

---

## Setup & Installation

### 1. Prerequisites

- Node.js 18+ and npm/yarn installed
- Backend API running (see backend README)

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure API Endpoint

Edit `src/api/api.js` and ensure the API base URL matches your backend:

```javascript
const API_BASE_URL = 'http://localhost:8000/api'; // Adjust as needed
```

---

## Running the Application

### Development Server

Start the development server with hot module reload:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the next available port).

### Build for Production

Create an optimized production build:

```bash
npm run build
```

Output will be in the `dist/` directory.

### Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

### Linting

Check code style and quality:

```bash
npm run lint
```

---

## API Integration

The frontend communicates with the backend API through `src/api/routes.js`:

### Available Endpoints

- `GET /companies?startIdx={index}` - Fetch companies with pagination
- `GET /search/{name}` - Search for a stock
- `GET /data/{symbol}` - Get stock historical data
- `GET /summary/{symbol}` - Get stock summary statistics

---

## Component Hierarchy

```
App
└── Dashboard
    ├── Sidebar
    ├── StockChart
    ├── SummaryCard
    ├── CompareView
    └── DataTable
```

---

## State Management

Uses React hooks (`useState`, `useEffect`) for local state management:

- `selectedStock` - Currently selected stock
- `chartData` - Historical stock price data
- `summary` - Stock summary statistics
- `view` - Current view mode ('single' or 'compare')

---

## Development Notes

- **Hot Reload**: Changes are automatically reflected in the browser
- **ESLint**: Run `npm run lint` before committing
- **Responsive Design**: CSS includes media queries for mobile/tablet/desktop
- **Error Handling**: API calls include try-catch blocks for error management

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Deployment

### Using Vite

Build the project and deploy the `dist/` folder to any static hosting service:

```bash
npm run build
# Deploy dist/ folder to your hosting platform
```

### Popular Platforms

- Vercel
- Netlify
- AWS S3 + CloudFront
- GitHub Pages

---

## Troubleshooting

### CORS Issues

If you encounter CORS errors, ensure the backend is configured to allow requests from your frontend origin.

### API Connection Errors

- Verify the backend is running on the configured API endpoint
- Check the API base URL in `src/api/api.js`
- Ensure network connectivity

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## Contributing

1. Keep code clean with ESLint checks
2. Follow React best practices
3. Add comments for complex logic
4. Test changes in development mode before committing

---

## License

This project is part of the Stock Data Intelligence Platform.
