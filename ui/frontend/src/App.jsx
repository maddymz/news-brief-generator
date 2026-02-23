import { useState } from 'react'
import Header from './components/Header'
import TopicInput from './components/TopicInput'
import ProgressLog from './components/ProgressLog'
import ContextTiles from './components/ContextTiles'
import Article from './components/Article'
import ImageDisplay from './components/ImageDisplay'

export default function App() {
  const [status, setStatus] = useState('idle') // idle | streaming | done | error
  const [steps, setSteps] = useState([])
  const [scoutData, setScoutData] = useState(null)
  const [publisherData, setPublisherData] = useState(null)
  const [error, setError] = useState(null)
  const [showMetadata, setShowMetadata] = useState(false)

  async function handleGenerate(topic) {
    setStatus('streaming')
    setSteps([])
    setScoutData(null)
    setPublisherData(null)
    setError(null)

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      })

      if (!res.ok) throw new Error(`Server error: ${res.status}`)

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() // hold incomplete line for next chunk

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              handleEvent(JSON.parse(line.slice(6)))
            } catch {
              // skip malformed lines
            }
          }
        }
      }
    } catch (err) {
      setError(err.message)
      setStatus('error')
    }
  }

  function handleEvent(event) {
    switch (event.step) {
      case 'location':
        setSteps(s => [...s, 'location'])
        break
      case 'scout':
        setScoutData(event.data)
        setSteps(s => [...s, 'scout'])
        break
      case 'publisher':
        setPublisherData(event.data)
        setSteps(s => [...s, 'publisher'])
        break
      case 'done':
        setStatus('done')
        setSteps(s => [...s, 'done'])
        break
      case 'error':
        setError(event.message)
        setStatus('error')
        break
    }
  }

  const context = scoutData?.context || {}
  const fx = context.financial_context || {}
  const weatherStr = context.location?.weather || 'N/A'
  const currency = fx.currency_code || ''
  const rate = fx.rate || ''
  const fxStr = rate ? `1 ${currency} = ${rate} USD` : 'N/A'

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <TopicInput onGenerate={handleGenerate} disabled={status === 'streaming'} />

        {(status === 'streaming' || status === 'error') && (
          <ProgressLog steps={steps} status={status} error={error} />
        )}

        {scoutData && (
          <ContextTiles
            location={scoutData.location || 'N/A'}
            weather={weatherStr}
            fx={fxStr}
          />
        )}

        {publisherData && (
          <>
            <Article article={publisherData.article || ''} />
            <ImageDisplay scoutData={scoutData} />

            <div className="metadata-toggle-row">
              <label className="metadata-toggle">
                <input
                  type="checkbox"
                  checked={showMetadata}
                  onChange={e => setShowMetadata(e.target.checked)}
                />
                🔍 Show metadata
              </label>
            </div>

            {showMetadata && (
              <div className="metadata-section">
                <h3 className="section-title">🔧 Debug Information</h3>
                <details className="metadata-block">
                  <summary>📦 Payload Data</summary>
                  <pre>{JSON.stringify(publisherData.payload, null, 2)}</pre>
                </details>
                {publisherData.signal && !publisherData.signal.ERROR && (
                  <details className="metadata-block">
                    <summary>📡 Signal Data</summary>
                    <pre>{JSON.stringify(publisherData.signal, null, 2)}</pre>
                  </details>
                )}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}
