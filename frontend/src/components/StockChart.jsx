import React from 'react';
import { 
  AreaChart, Area, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, ReferenceLine 
} from 'recharts';

export default function StockChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="chart-placeholder">Loading chart data...</div>;
  }

  const minPrice = Math.min(...data.map(d => d.close)) * 0.98;
  const maxPrice = Math.max(...data.map(d => d.close)) * 1.02;
  const avgClose = data[0]?.avg_close;

  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
          <defs>
            <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#387ed1" stopOpacity={0.2}/>
              <stop offset="95%" stopColor="#387ed1" stopOpacity={0}/>
            </linearGradient>
          </defs>

          <CartesianGrid stroke="#f5f5f5" vertical={false} />

          <XAxis 
            dataKey="date" 
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 10, fill: '#bbb' }}
            minTickGap={30} 
            dy={10}
          />

          <YAxis 
            orientation="right" 
            domain={[minPrice, maxPrice]} 
            tick={{ fontSize: 11, fill: '#999' }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value) => `₹${value}`}
          />

          <Tooltip content={<CustomTooltip />} />

          <ReferenceLine 
            y={avgClose} 
            stroke="#ccc" 
            strokeDasharray="3 3" 
            label={{ position: 'left', value: 'Avg', fill: '#ccc', fontSize: 10 }} 
          />

          <Area 
            type="monotone" 
            dataKey="close" 
            stroke="#387ed1" 
            strokeWidth={2.5}
            fillOpacity={1} 
            fill="url(#colorClose)" 
            animationDuration={1000}
          />

          <Line 
            type="monotone" 
            dataKey="ma_7" 
            stroke="#ff9800" 
            dot={false} 
            strokeWidth={1.5}
            strokeDasharray="5 5"
            name="7-Day MA"
          />
        </AreaChart>
      </ResponsiveContainer>
      
      <div className="chart-legend">
        <div className="legend-item"><span className="dot blue"></span> Price</div>
        <div className="legend-item"><span className="dot orange-dash"></span> 7D Moving Average</div>
      </div>
    </div>
  );
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="custom-tooltip">
        <p className="tooltip-date">{label}</p>
        <p className="tooltip-price">₹{data.close.toLocaleString()}</p>
        <div className="tooltip-details">
          <span className={data.daily_return >= 0 ? 'pos' : 'neg'}>
            {data.daily_return >= 0 ? '+' : ''}{data.daily_return}%
          </span>
          <span className="vol">Vol: {(data.volume / 1000000).toFixed(2)}M</span>
        </div>
      </div>
    );
  }
  return null;
};