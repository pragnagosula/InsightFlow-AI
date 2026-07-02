import { useState, useEffect, useRef } from 'react'

export default function GenerateReportModal({ conversations, isGenerating, onGenerate, onClose }) {
  const [title, setTitle] = useState('')
  const [conversationId, setConversationId] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    inputRef.current?.focus()
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!title.trim()) return
    onGenerate(title.trim(), conversationId || null)
  }

  return (
    <>
      <div className="fixed inset-0 z-50 bg-black/60" onClick={onClose} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div
          className="bg-surface-800 border border-surface-600 rounded-2xl shadow-2xl w-full max-w-md pointer-events-auto animate-slide-up"
          onClick={e => e.stopPropagation()}
        >
          {/* Header */}
          <div className="px-6 py-5 border-b border-surface-600 flex items-center justify-between">
            <div>
              <h2 className="text-text-primary font-semibold text-sm">Generate Report</h2>
              <p className="text-text-muted text-xs mt-0.5">Create a PDF business report with AI</p>
            </div>
            <button onClick={onClose} className="text-text-muted hover:text-text-primary transition-colors">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="px-6 py-5 space-y-4">
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1.5">
                Report title <span className="text-red-400">*</span>
              </label>
              <input
                ref={inputRef}
                type="text"
                value={title}
                onChange={e => setTitle(e.target.value)}
                placeholder="e.g. Q3 Sales Analysis, Customer Churn Report"
                maxLength={200}
                className="w-full bg-surface-700 border border-surface-500 rounded-lg px-3 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent transition-colors"
              />
            </div>

            {conversations.length > 0 && (
              <div>
                <label className="block text-xs font-medium text-text-secondary mb-1.5">
                  Base on conversation <span className="text-text-muted font-normal">(optional)</span>
                </label>
                <select
                  value={conversationId}
                  onChange={e => setConversationId(e.target.value)}
                  className="w-full bg-surface-700 border border-surface-500 rounded-lg px-3 py-2.5 text-sm text-text-primary focus:outline-none focus:border-accent transition-colors"
                >
                  <option value="">— None —</option>
                  {conversations.map(c => (
                    <option key={c.id} value={c.id}>{c.title}</option>
                  ))}
                </select>
              </div>
            )}

            <p className="text-xs text-text-muted leading-relaxed">
              The AI will generate a structured PDF report with executive summary, key findings, analysis, and recommendations based on the title you provide.
            </p>

            <div className="flex gap-2 pt-1">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-2.5 rounded-lg border border-surface-500 text-text-secondary hover:text-text-primary hover:border-surface-400 text-sm transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={!title.trim() || isGenerating}
                className="flex-1 px-4 py-2.5 rounded-lg bg-accent hover:bg-accent/90 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium transition-colors flex items-center justify-center gap-2"
              >
                {isGenerating ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Generating…
                  </>
                ) : (
                  <>
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Generate PDF
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  )
}
