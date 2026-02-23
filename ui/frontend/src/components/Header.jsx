export default function Header() {
  return (
    <div className="nbg-header">
      <div className="nbg-header-row">
        <div className="nbg-header-icon">📰</div>
        <div className="nbg-header-content">
          <div className="nbg-header-title">News Brief Generator</div>
          <div className="nbg-header-subtitle">
            AI-powered contextual reports with live data
          </div>
        </div>
        <div className="nbg-header-badge">
          <span className="live-dot" />
          Live Data
        </div>
      </div>
    </div>
  )
}
