import { fileIcon, statusColor, truncate } from '../../utils/formatters'

export default function FileChip({ file, onRemove, onClick }) {
  return (
    <span
      onClick={onClick ? () => onClick(file) : undefined}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-600 border border-surface-500 text-xs group transition-colors hover:border-surface-400 ${onClick ? 'cursor-pointer' : ''}`}
    >
      <span>{fileIcon(file.file_type, file.kind)}</span>
      <span className={statusColor(file.status)}>{truncate(file.filename, 22)}</span>

      {(file.status === 'processing' || file.status === 'pending') && (
        <span className="w-1.5 h-1.5 rounded-full bg-yellow-400 animate-pulse" title="Processing…" />
      )}
      {file.status === 'failed' && (
        <span className="text-red-400 text-xs" title="Failed">✕</span>
      )}

      {onRemove && (
        <button
          onClick={(e) => { e.stopPropagation(); onRemove(file.id) }}
          className="ml-0.5 text-text-muted hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
          title="Remove file"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </span>
  )
}
