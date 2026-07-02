import { statusColor, fileIcon } from '../../utils/formatters'

export default function TopBar({ workspace, files, onFileClick }) {
  const ready = files.filter(f => f.status === 'complete').length
  const processing = files.filter(f => ['pending', 'processing'].includes(f.status)).length

  return (
    <header className="border-b border-surface-600 bg-surface-800 px-6 py-3 flex items-center justify-between shrink-0">
      <div className="flex items-center gap-3">
        <div>
          <h1 className="text-text-primary font-semibold text-sm">{workspace?.name ?? 'Workspace'}</h1>
          {files.length > 0 && (
            <p className="text-xs text-text-muted mt-0.5">
              {ready} file{ready !== 1 ? 's' : ''} ready
              {processing > 0 && (
                <span className="ml-2 text-yellow-400 animate-pulse">
                  · {processing} processing…
                </span>
              )}
            </p>
          )}
        </div>
      </div>

      {/* Clickable file badges */}
      {files.length > 0 && (
        <div className="flex items-center gap-1.5 flex-wrap justify-end max-w-md">
          {files.slice(0, 6).map(f => (
            <button
              key={f.id}
              onClick={() => onFileClick?.(f)}
              className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-surface-700 border border-surface-600 text-xs transition-colors hover:border-surface-400 ${statusColor(f.status)} ${onFileClick ? 'cursor-pointer' : 'cursor-default'}`}
              title={`${f.filename} — click to inspect`}
            >
              <span>{fileIcon(f.file_type, f.kind)}</span>
              <span className="max-w-[100px] truncate">{f.filename}</span>
            </button>
          ))}
          {files.length > 6 && (
            <span className="text-xs text-text-muted">+{files.length - 6} more</span>
          )}
        </div>
      )}
    </header>
  )
}
