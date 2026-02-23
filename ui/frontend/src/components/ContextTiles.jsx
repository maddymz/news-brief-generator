export default function ContextTiles({ location, weather, fx }) {
  return (
    <div className="context-section">
      <h3 className="section-title">📊 Context Overview</h3>
      <div className="tiles-row">
        <Tile icon="📍" label="Location" value={location} />
        <Tile icon="🌤" label="Weather" value={weather} />
        <Tile icon="💱" label="Exchange Rate" value={fx} />
      </div>
    </div>
  )
}

function Tile({ icon, label, value }) {
  return (
    <div className="nbg-tile">
      <div className="nbg-tile-icon">{icon}</div>
      <div className="nbg-tile-label">{label}</div>
      <div className="nbg-tile-value">{value}</div>
    </div>
  )
}
