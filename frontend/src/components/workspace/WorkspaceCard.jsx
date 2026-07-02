import { useNavigate } from 'react-router-dom'
import { formatRelative } from '../../utils/formatters'

export default function WorkspaceCard({ workspace, onDelete }) {
  const navigate = useNavigate()

  return (
    <div
      onClick={() => navigate(`/workspace/${workspace.id}`)}
      className="group bg-surface-700 border border-surface-600 hover:border-surface-400 rounded-xl p-5 cursor-pointer transition-all duration-150 hover:bg-surface-600 animate-fade-in"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-6 h-6 rounded-md bg-accent/20 flex items-center justify-center shrink-0">
              <span className="text-accent text-xs font-bold">{workspace.name[0].toUpperCase()}</span>
            </div>
            <h3 className="text-text-primary font-semibold text-sm truncate">{workspace.name}</h3>
          </div>
          {workspace.description && (
            <p className="text-text-muted text-xs mt-1 line-clamp-2">{workspace.description}</p>
          )}
        </div>
        <button
          onClick={e => { e.stopPropagation(); onDelete(workspace.id) }}
          className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-surface-500 text-text-muted hover:text-red-400 transition-all ml-2 shrink-0"
          title="Delete"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
      <div className="mt-3 flex items-center gap-3 text-xs text-text-muted">
        <span>Updated {formatRelative(workspace.updated_at)}</span>
        {workspace.file_count > 0 && (
          <span className="flex items-center gap-1">
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
            </svg>
            {workspace.file_count} file{workspace.file_count !== 1 ? 's' : ''}
          </span>
        )}
      </div>
    </div>
  )
}
