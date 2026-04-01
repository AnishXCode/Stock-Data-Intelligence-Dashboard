export default function SummaryCard({ label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value ? `₹${value}` : '--'}</div>
    </div>
  );
}