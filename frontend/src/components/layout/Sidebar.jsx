import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useWorkspaceList } from '../../hooks/useWorkspace'
import useWorkspaceStore from '../../store/workspaceStore'
import NewWorkspaceModal from '../workspace/NewWorkspaceModal'
import { formatRelative, truncate } from '../../utils/formatters'

export default function Sidebar() {
  const { workspaceId } = useParams()
  const navigate = useNavigate()
  const { workspaces, isLoadingWorkspaces, createWorkspace, deleteWorkspace } = useWorkspaceList()
  const { conversations, currentConversation, selectConversation, newChat } = useWorkspaceStore()
  const [showModal, setShowModal] = useState(false)
  const [hoveredId, setHoveredId] = useState(null)

  const handleCreate = async (name, description) => {
    const ws = await createWorkspace(name, description)
    navigate(`/workspace/${ws.id}`)
    setShowModal(false)
  }

  const handleDelete = async (e, id) => {
    e.stopPropagation()
    if (!confirm('Delete this workspace and all its data?')) return
    await deleteWorkspace(id)
    if (workspaceId === id) navigate('/')
  }

  return (
    <>
      <aside className="w-64 bg-surface-800 border-r border-surface-600 flex flex-col shrink-0">
        {/* Logo */}
        <div className="px-4 pt-5 pb-4 border-b border-surface-600">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-accent flex items-center justify-center shrink-0">
              <span className="text-white text-xs font-bold">IF</span>
            </div>
            <span className="text-text-primary font-semibold text-sm tracking-tight">InsightFlow AI</span>
          </div>
        </div>

        {/* New workspace */}
        <div className="px-3 pt-3 pb-2">
          <button
            onClick={() => setShowModal(true)}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg border border-surface-500 hover:border-accent hover:bg-surface-700 text-text-secondary hover:text-text-primary text-sm transition-colors duration-150 group"
          >
            <svg className="w-4 h-4 group-hover:text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Workspace
          </button>
        </div>

        {/* Workspace list */}
        <div className="flex-1 overflow-y-auto px-2 py-1 space-y-0.5">
          {isLoadingWorkspaces ? (
            <div className="px-3 py-6 text-center text-text-muted text-xs">Loading…</div>
          ) : workspaces.length === 0 ? (
            <div className="px-3 py-6 text-center text-text-muted text-xs">No workspaces yet</div>
          ) : (
            workspaces.map(ws => (
              <div key={ws.id} className="group relative">
                <button
                  onClick={() => navigate(`/workspace/${ws.id}`)}
                  onMouseEnter={() => setHoveredId(ws.id)}
                  onMouseLeave={() => setHoveredId(null)}
                  className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-colors duration-100 ${
                    workspaceId === ws.id
                      ? 'bg-surface-600 text-text-primary'
                      : 'text-text-secondary hover:bg-surface-700 hover:text-text-primary'
                  }`}
                >
                  <div className="font-medium truncate pr-6">{ws.name}</div>
                  <div className="text-xs text-text-muted mt-0.5">{formatRelative(ws.updated_at)}</div>
                </button>
                {hoveredId === ws.id && (
                  <button
                    onClick={e => handleDelete(e, ws.id)}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1 rounded hover:bg-surface-500 text-text-muted hover:text-red-400 transition-colors"
                    title="Delete workspace"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                )}
              </div>
            ))
          )}
        </div>

        {/* Conversations for current workspace */}
        {workspaceId && conversations.length > 0 && (
          <div className="border-t border-surface-600 px-2 py-2 max-h-52 overflow-y-auto">
            <p className="px-3 py-1 text-xs text-text-muted font-medium uppercase tracking-wider">History</p>
            <button
              onClick={newChat}
              className="w-full text-left px-3 py-1.5 rounded-lg text-xs text-accent hover:bg-surface-700 transition-colors"
            >
              + New chat
            </button>
            {conversations.map(conv => (
              <button
                key={conv.id}
                onClick={() => selectConversation(conv)}
                className={`w-full text-left px-3 py-1.5 rounded-lg text-xs truncate transition-colors ${
                  currentConversation?.id === conv.id
                    ? 'bg-surface-600 text-text-primary'
                    : 'text-text-secondary hover:bg-surface-700 hover:text-text-primary'
                }`}
              >
                {truncate(conv.title, 36)}
              </button>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="px-4 py-3 border-t border-surface-600 text-xs text-text-muted">
          InsightFlow AI v1.0
        </div>
      </aside>

      {showModal && (
        <NewWorkspaceModal onClose={() => setShowModal(false)} onCreate={handleCreate} />
      )}
    </>
  )
}
