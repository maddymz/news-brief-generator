const DONE_LABELS = {
  location: '📍 Location detected',
  scout:    '🔎 Scout data gathered',
  publisher:'✍️ Article generated',
  done:     '✅ Done',
}

const PENDING_LABELS = {
  location: '📍 Detecting location…',
  scout:    '🔎 Running Scout…',
  publisher:'✍️ Running Publisher…',
}

const ALL_STEPS = ['location', 'scout', 'publisher', 'done']

export default function ProgressLog({ steps, status, error }) {
  const nextStep = ALL_STEPS.find(s => !steps.includes(s))

  return (
    <div className="progress-log">
      {steps.map(step => (
        <div key={step} className="progress-step step-done">
          {DONE_LABELS[step]}
        </div>
      ))}

      {status === 'streaming' && nextStep && nextStep !== 'done' && (
        <div className="progress-step step-pending">
          <span className="spinner" />
          {PENDING_LABELS[nextStep]}
        </div>
      )}

      {status === 'error' && (
        <div className="progress-step step-error">❌ {error}</div>
      )}
    </div>
  )
}
