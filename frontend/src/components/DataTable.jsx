import React from 'react';

export default function DataTable({ data }) {
  const recentData = [...data].reverse().slice(0, 10);

  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Open</th>
            <th>Close</th>
            <th>Daily Return</th>
            <th>Volume</th>
          </tr>
        </thead>
        <tbody>
          {recentData.map((row, i) => (
            <tr key={i}>
              <td>{row.date}</td>
              <td>₹{row.open}</td>
              <td>₹{row.close}</td>
              <td className={row.daily_return >= 0 ? 'pos' : 'neg'}>
                {row.daily_return}%
              </td>
              <td>{row.volume.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}