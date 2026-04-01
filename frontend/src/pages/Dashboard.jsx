import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import StockChart from '../components/StockChart';
import SummaryCard from '../components/SummaryCard';
import CompareView from '../components/CompareView';
import DataTable from '../components/DataTable'; 
import { getStockData, getStockSummary } from '../api/routes';

export default function Dashboard() {
  const [selectedStock, setSelectedStock] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [view, setView] = useState('single'); 
  const [isLoading, setIsLoading] = useState(false);

  const handleSelect = async (stock) => {
    setSelectedStock(stock);
    setIsLoading(true); 
    
    try {
      const [d, s] = await Promise.all([
        getStockData(stock.symbol),
        getStockSummary(stock.symbol)
      ]);
      setChartData(d.data);
      setSummary(s.data);
    } catch (error) {
      console.error("Error fetching stock data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const latest = chartData.length > 0 ? chartData[chartData.length - 1] : null;

  return (
    <div className="app-layout">
      <Sidebar onSelect={handleSelect} activeSymbol={selectedStock?.symbol} />
      
      <main className="main-content">
        {selectedStock ? (
          <div className="content-inner">
            <header className="content-header">
              <div className="stock-title">
                <h1>{selectedStock.name}</h1>
                <div className="symbol-row">
                  <span className="badge">NSE</span>
                  <span className="symbol-txt">{selectedStock.symbol}</span>
                  {!isLoading && latest && (
                    <span className={`price-change ${latest.daily_return >= 0 ? 'pos' : 'neg'}`}>
                      {latest.daily_return >= 0 ? '▲' : '▼'} {Math.abs(latest.daily_return)}% Most Recent
                    </span>
                  )}
                </div>
              </div>
              <div className="view-tabs">
                <button className={view === 'single' ? 'active' : ''} onClick={() => setView('single')}>Analysis</button>
                <button className={view === 'compare' ? 'active' : ''} onClick={() => setView('compare')}>Comparison Lab</button>
              </div>
            </header>

            {isLoading ? (
              <div className="loading-state">
                <div className="loader"></div>
                <p>Retrieving market intelligence for {selectedStock.symbol}...</p>
                <small>The backend may take a moment to wake up on Render.</small>
              </div>
            ) : view === 'single' ? (
              <>
                <div className="section-label">Yearly Performance</div>
                <div className="metrics-grid">
                  <SummaryCard label="52W High" value={summary?.high_52w} />
                  <SummaryCard label="52W Low" value={summary?.low_52w} />
                  <SummaryCard label="Avg Close" value={summary?.avg_close} />
                  <SummaryCard label="Volatility" value={latest?.volatility + '%'} />
                </div>

                <div className="section-label">Most Recent Snapshot</div>
                <div className="snapshot-grid">
                   <div className="snap-item"><label>Open</label><span>₹{latest?.open}</span></div>
                   <div className="snap-item"><label>High</label><span>₹{latest?.high}</span></div>
                   <div className="snap-item"><label>Low</label><span>₹{latest?.low}</span></div>
                   <div className="snap-item"><label>Volume</label><span>{latest?.volume?.toLocaleString()}</span></div>
                   <div className="snap-item"><label>7D MA</label><span>₹{latest?.ma_7}</span></div>
                </div>

                <div className="chart-section">
                   <div className="section-label">Price Trajectory</div>
                   <StockChart data={chartData} />
                </div>

                <div className="section-label">Recent History</div>
                <DataTable data={chartData} />
              </>
            ) : (
              <CompareView primarySymbol={selectedStock.symbol} />
            )}
          </div>
        ) : (
          <div className="empty-state">Select a company from the watchlist to view intelligence.</div>
        )}
      </main>
    </div>
  );
}