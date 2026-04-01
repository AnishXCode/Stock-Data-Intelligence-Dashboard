import React, { useState, useEffect } from 'react';
import { getCompanies, getStock } from '../api/routes';

export default function Sidebar({ onSelect, activeSymbol }) {
  const [stocks, setStocks] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    fetchList(0);
  }, []);

  const fetchList = (idx) => {
    setIsSearching(false);
    getCompanies(idx).then(res => setStocks(res.data));
  };

  const handleSearch = async (e) => {
    const val = e.target.value;
    setSearch(val);

    if (val.trim() === "" || val.length < 3) {
      fetchList(page);
      return;
    }

    if (val.length > 2) {
      setIsSearching(true);
      try {
        const res = await getStock(val);
        setStocks(res.data);
      } catch (err) {
        console.error("Failed to fetch symbol: ", err);
        setStocks([]); 
      }
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <input 
          type="text" 
          placeholder="Search (e.g. Reliance, TCS)" 
          value={search}
          onChange={handleSearch}
        />
      </div>

      <div className="sidebar-list">
        {stocks.length > 0 ? (
          stocks.map(s => (
            <div 
              key={s.symbol} 
              className={`stock-row ${activeSymbol === s.symbol ? 'active' : ''}`}
              onClick={() => onSelect(s)}
            >
              <div className="stock-info">
                <span className="stock-symbol">{s.symbol}</span>
                <span className="stock-name">{s.name}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="no-results">
            <p>No such stock found</p>
            <span>Try searching by symbol or full name</span>
          </div>
        )}
      </div>

      {!isSearching && (
        <div className="pagination">
          <button onClick={() => { 
            const newPage = Math.max(0, page - 30);
            setPage(newPage); 
            fetchList(newPage); 
          }} disabled={page === 0}>Prev</button>
          <span className="page-indicator">Page {(page / 30) + 1}</span>
          <button onClick={() => { 
            const newPage = page + 30;
            setPage(newPage); 
            fetchList(newPage); 
          }}>Next</button>
        </div>
      )}
    </aside>
  );
}