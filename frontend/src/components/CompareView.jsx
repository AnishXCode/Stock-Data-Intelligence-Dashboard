import React, { useState } from 'react';
import { getStock, getComparision } from '../api/routes';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, ReferenceLine, Legend 
} from 'recharts';

export default function CompareView({ primarySymbol }) {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [targetStock, setTargetStock] = useState(null);
  const [compareData, setCompareData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    const val = e.target.value;
    setQuery(val);
    if (val.length > 2) {
      try {
        const res = await getStock(val);
        setSearchResults(res.data || []);
      } catch (err) { setSearchResults([]); }
    } else { setSearchResults([]); }
  };

  const selectAndCompare = async (stock) => {
    setTargetStock(stock);
    setSearchResults([]);
    setQuery("");
    setLoading(true);
    try {
      const res = await getComparision(primarySymbol, stock.symbol);
      setCompareData(res.data);
    } catch (err) {
      alert("Comparison failed. Symbols must be active on NSE.");
    } finally { setLoading(false); }
  };

  return (
    <div className="compare-lab">
      <div className="compare-header-box">
        <div className="compare-selector">
          <div className="stock-pill primary">{primarySymbol}</div>
          <span className="vs-text">vs</span>
          <div className="search-container">
            <input 
              type="text" 
              placeholder="Search target stock..." 
              value={targetStock ? targetStock.name : query}
              onChange={handleSearch}
              className="compare-input"
            />
            {targetStock && (
              <button className="clear-btn" onClick={() => {setTargetStock(null); setCompareData(null);}}>✕</button>
            )}
            {searchResults.length > 0 && (
              <div className="compare-results-dropdown">
                {searchResults.map(s => (
                  <div key={s.symbol} className="result-item" onClick={() => selectAndCompare(s)}>
                    <span className="res-sym">{s.symbol}</span>
                    <span className="res-name">{s.name}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {loading && <div className="loading-placeholder">Calculating Correlation...</div>}

      {compareData && !loading && (
        <div className="comparison-content">
          <div className="insight-row">
            <div className="insight-card">
              <label>Correlation Strength</label>
              <div className="val">{compareData.correlation_label}</div>
              <p className="desc">{compareData.insight}</p>
            </div>
            <div className="insight-card">
              <label>Diversification</label>
              <div className="val">{compareData.diversification_score}</div>
              <p className="desc">Score closer to 1.0 means better risk spread.</p>
            </div>
          </div>

          <div className="compare-chart-container">
            <div className="section-label">Normalized Performance Comparison</div>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={compareData.chart_data} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid stroke="#f5f5f5" vertical={false} />
                
                <XAxis 
                  dataKey="date" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{fontSize: 10, fill: '#bbb'}} 
                  minTickGap={40}
                  dy={10}
                />
                
                <YAxis 
                  orientation="right" 
                  tick={{fontSize: 11, fill: '#999'}} 
                  axisLine={false} 
                  tickLine={false}
                  tickFormatter={(v) => `${v > 1 ? '+' : ''}${((v - 1) * 100).toFixed(0)}%`}
                />

                <ReferenceLine 
                  y={1} 
                  stroke="#333" 
                  strokeDasharray="3 3" 
                  label={{ position: 'left', value: '0% (Start)', fill: '#999', fontSize: 10, fontWeight: 700 }} 
                />

                <Legend verticalAlign="top" align="right" height={36} iconType="circle" />

                <Tooltip content={<CompareTooltip />} />

                <Line 
                  type="monotone" 
                  dataKey="s1" 
                  stroke="#387ed1" 
                  name={compareData.symbol1} 
                  dot={false} 
                  strokeWidth={3} 
                  animationDuration={1500}
                />
                <Line 
                  type="monotone" 
                  dataKey="s2" 
                  stroke="#f43f5e" 
                  name={compareData.symbol2} 
                  dot={false} 
                  strokeWidth={3} 
                  animationDuration={1500}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

const CompareTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length === 2) {
    return (
      <div className="custom-tooltip compare">
        <p className="tooltip-date">{label}</p>
        <div className="compare-items">
          {payload.map((item, index) => {
            const percentChange = ((item.value - 1) * 100).toFixed(2);
            const isPositive = percentChange >= 0;

            return (
              <div key={index} className="tooltip-item">
                <span className={`dot ${index === 0 ? 'blue' : 'red'}`}></span>
                <span className="name">{item.name}</span>
                <span className={`val ${isPositive ? 'pos' : 'neg'}`}>
                  {isPositive ? '+' : ''}{percentChange}%
                </span>
              </div>
            );
          })}
        </div>
      </div>
    );
  }
  return null;
};