import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useWorkspaceList } from '../hooks/useWorkspace'
import WorkspaceCard from '../components/workspace/WorkspaceCard'
import NewWorkspaceModal from '../components/workspace/NewWorkspaceModal'

export default function Home() {
  const navigate = useNavigate()
  const { workspaces, isLoadingWorkspaces, createWorkspace, deleteWorkspace } = useWorkspaceList()
  const [showModal, setShowModal] = useState(false)

  const handleCreate = async (name, description) => {
    const ws = await createWorkspace(name, description)
    navigate(`/workspace/${ws.id}`)
    setShowModal(false)
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this workspace and all its data?')) return
    await deleteWorkspace(id)
  }

  return (
    <div className="flex-1 overflow-y-auto">
      {/* Hero */}
      <div className="border-b border-surface-600 bg-surface-800 px-8 py-10">
        <div className="max-w-2xl">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-xl bg-accent flex items-center justify-center">
              <span className="text-white font-bold">IF</span>
            </div>
            <h1 className="text-2xl font-bold text-text-primary">InsightFlow AI</h1>
          </div>
          <p className="text-text-secondary text-sm leading-relaxed">
            Upload CSVs, Excel files, PDFs, and documents into a workspace.
            Ask questions in plain English — the AI automatically selects the right files,
            runs analysis, and delivers business insights.
          </p>
          <button
            onClick={() => setShowModal(true)}
            className="btn-primary mt-5 flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Workspace
          </button>
        </div>
      </div>

      {/* Capability pills */}
      <div className="px-8 py-5 border-b border-surface-600 flex flex-wrap gap-2">
        {[
          { icon: '📊', label: 'CSV & Excel Analysis' },
          { icon: '📄', label: 'PDF & Document Q&A' },
          { icon: '🔀', label: 'Hybrid Queries' },
          { icon: '📈', label: 'Auto Charts' },
          { icon: '🧹', label: 'Auto Preprocessing' },
          { icon: '🧠', label: 'Multi-Agent AI' },
        ].map(cap => (
          <span key={cap.label} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-surface-700 border border-surface-600 rounded-full text-xs text-text-secondary">
            <span>{cap.icon}</span>{cap.label}
          </span>
        ))}
      </div>

      {/* Workspaces grid */}
      <div className="px-8 py-6">
        {isLoadingWorkspaces ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-28 bg-surface-700 border border-surface-600 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : workspaces.length === 0 ? (
          <div className="text-center py-16">
            <div className="w-12 h-12 rounded-xl bg-surface-700 border border-surface-600 flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
            </div>
            <p className="text-text-secondary font-medium">No workspaces yet</p>
            <p className="text-text-muted text-sm mt-1">Create your first workspace to get started.</p>
            <button onClick={() => setShowModal(true)} className="btn-primary mt-4">
              Create Workspace
            </button>
          </div>
        ) : (
          <>
            <h2 className="text-text-secondary text-xs font-semibold uppercase tracking-wider mb-4">
              Your Workspaces
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {workspaces.map(ws => (
                <WorkspaceCard key={ws.id} workspace={ws} onDelete={handleDelete} />
              ))}
            </div>
          </>
        )}
      </div>

      {showModal && (
        <NewWorkspaceModal onClose={() => setShowModal(false)} onCreate={handleCreate} />
      )}
    </div>
  )
}
