import { useState } from 'react'

export default function CitationCard({ source }) {
  const [expanded, setExpanded] = useState(false)
  const { filename, snippets } = source

  return (
    <div className="border border-surface-500 rounded-lg overflow-hidden text-xs">
      <button
        onClick={() => setExpanded(e => !e)}
        className="w-full flex items-center justify-between px-3 py-2 bg-surface-700 hover:bg-surface-600 transition-colors text-left"
      >
        <div className="flex items-center gap-2 min-w-0">
          <svg className="w-3 h-3 text-accent shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span className="text-text-secondary font-medium truncate">{filename}</span>
          <span className="text-text-muted shrink-0">
            {snippets.length} chunk{snippets.length !== 1 ? 's' : ''}
          </span>
        </div>
        <svg
          className={`w-3 h-3 text-text-muted transition-transform duration-200 shrink-0 ml-2 ${expanded ? 'rotate-180' : ''}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {expanded && (
        <div className="divide-y divide-surface-600 bg-surface-800 animate-fade-in">
          {snippets.map((snippet, i) => (
            <div key={i} className="px-3 py-2.5">
              <p className="text-text-muted text-xs mb-1.5 font-medium">Chunk {i + 1}</p>
              <p className="text-text-secondary leading-relaxed">{snippet}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
