import { useEffect } from 'react'
import PreprocessingReport from './PreprocessingReport'
import { fileIcon, statusColor, formatDate } from '../../utils/formatters'

export default function FileDrawer({ file, report, isLoading, onClose }) {
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 z-30 bg-black/50" onClick={onClose} />

      {/* Drawer */}
      <div className="fixed right-0 top-0 bottom-0 z-40 w-80 bg-surface-800 border-l border-surface-600 flex flex-col shadow-2xl animate-slide-in-right">
        {/* Header */}
        <div className="px-5 py-4 border-b border-surface-600 flex items-start gap-3 shrink-0">
          <span className="text-xl mt-0.5">{fileIcon(file.file_type, file.kind)}</span>
          <div className="flex-1 min-w-0">
            <h3 className="text-text-primary font-semibold text-sm truncate" title={file.filename}>
              {file.filename}
            </h3>
            <p className="text-xs text-text-muted mt-0.5">
              <span className="capitalize">{file.kind}</span>
              <span className="mx-1">·</span>
              <span className="uppercase">{file.file_type}</span>
              <span className={`ml-2 ${statusColor(file.status)}`}>· {file.status}</span>
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-text-muted hover:text-text-primary transition-colors shrink-0 mt-0.5"
            title="Close (Esc)"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Meta row */}
        <div className="px-5 py-2.5 border-b border-surface-600 flex items-center gap-4 text-xs text-text-muted shrink-0 flex-wrap">
          <span>Added {formatDate(file.created_at)}</span>
          {file.kind === 'dataset' && file.row_count != null && (
            <span>{file.row_count.toLocaleString()} rows</span>
          )}
          {file.kind === 'document' && file.chunk_count != null && (
            <span>{file.chunk_count} chunks indexed</span>
          )}
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto px-5 py-4 space-y-5">
          {file.kind === 'dataset' ? (
            <>
              {/* Column list — shown before preprocessing details */}
              {file.columns?.length > 0 && (
                <ColumnList columns={file.columns} />
              )}
              <PreprocessingReport file={file} report={report} isLoading={isLoading} />
            </>
          ) : (
            <DocumentInfo file={file} />
          )}
        </div>
      </div>
    </>
  )
}

function ColumnList({ columns }) {
  return (
    <div>
      <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">
        Columns ({columns.length})
      </p>
      <div className="flex flex-wrap gap-1.5">
        {columns.map(col => (
          <span
            key={col}
            className="px-2 py-0.5 bg-surface-700 border border-surface-600 rounded text-xs text-text-secondary font-mono"
          >
            {col}
          </span>
        ))}
      </div>
    </div>
  )
}

function DocumentInfo({ file }) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-2.5">
        <InfoCard label="Status" value={file.status} valueClass={statusColor(file.status)} />
        {file.chunk_count != null && (
          <InfoCard label="Chunks indexed" value={file.chunk_count} />
        )}
      </div>
      <p className="text-xs text-text-muted leading-relaxed">
        Document text was split into overlapping chunks, embedded with a local sentence-transformer
        model, and stored in a FAISS index. Relevant chunks are retrieved per question via
        semantic similarity search.
      </p>
      {file.status === 'complete' && (
        <div className="flex items-center gap-2 px-3 py-2.5 bg-green-900/20 border border-green-700/30 rounded-lg">
          <svg className="w-3.5 h-3.5 text-green-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <span className="text-green-400 text-xs">Ready for semantic search</span>
        </div>
      )}
    </div>
  )
}

function InfoCard({ label, value, valueClass }) {
  return (
    <div className="bg-surface-700 border border-surface-600 rounded-lg px-3 py-2.5">
      <p className="text-text-muted text-xs mb-1">{label}</p>
      <p className={`text-sm font-semibold capitalize ${valueClass ?? 'text-text-primary'}`}>{value}</p>
    </div>
  )
}
