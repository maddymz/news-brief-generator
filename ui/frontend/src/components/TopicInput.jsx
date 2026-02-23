import { useState } from 'react'

export default function TopicInput({ onGenerate, disabled }) {
  const [topic, setTopic] = useState('Semiconductor factory opening in Japan')

  function submit() {
    if (!disabled && topic.trim()) onGenerate(topic.trim())
  }

  return (
    <div className="topic-section">
      <h3 className="topic-label">🔍 Enter your topic</h3>
      <p className="topic-sub">
        Get comprehensive news reports with live context, weather, and financial data
      </p>
      <div className="topic-row">
        <input
          className="topic-input"
          type="text"
          value={topic}
          onChange={e => setTopic(e.target.value)}
          placeholder="Enter any news topic..."
          disabled={disabled}
          onKeyDown={e => e.key === 'Enter' && submit()}
        />
        <button className="generate-btn" onClick={submit} disabled={disabled || !topic.trim()}>
          {disabled ? 'Generating…' : 'Generate Report'}
        </button>
      </div>
    </div>
  )
}
