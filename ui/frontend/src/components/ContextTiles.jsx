export default function ContextTiles({ location, weather, fx }) {
  return (
    <div className="context-section">
      <h3 className="section-title">Context Overview</h3>
      <div className="tiles-row">
        <Tile type="location" icon="📍" label="Location"      value={location} />
        <Tile type="weather"  icon="🌤" label="Weather"       value={weather} />
        <Tile type="fx"       icon="💱" label="Exchange Rate" value={fx} />
      </div>
    </div>
  )
}

function Tile({ type, icon, label, value }) {
  return (
    <div className="nbg-tile" data-type={type}>
      <span className="nbg-tile-icon">{icon}</span>
      <div className="nbg-tile-label">{label}</div>
      <div className="nbg-tile-value">{value}</div>
    </div>
  )
}
