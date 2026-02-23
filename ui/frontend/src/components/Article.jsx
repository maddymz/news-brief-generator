import { useState, useMemo } from 'react'
import { marked } from 'marked'

marked.setOptions({ breaks: true })

export default function Article({ article }) {
  const [open, setOpen] = useState(true)
  const html = useMemo(() => marked.parse(article || ''), [article])

  return (
    <div className="article-section">
      <h3 className="section-title">📄 Generated Article</h3>
      <div className="nbg-article-container">
        <button className="expander-toggle" onClick={() => setOpen(o => !o)}>
          {open ? '▲' : '▼'} Read full article
        </button>
        {open && (
          <div
            className="article-body"
            dangerouslySetInnerHTML={{ __html: html }}
          />
        )}
      </div>
    </div>
  )
}
