import { useState } from 'react'

export default function NewWorkspaceModal({ onClose, onCreate }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim()) { setError('Name is required'); return }
    setLoading(true)
    try {
      await onCreate(name.trim(), description.trim())
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-surface-700 border border-surface-500 rounded-xl shadow-2xl w-full max-w-md mx-4 animate-slide-up">
        <div className="px-6 py-5 border-b border-surface-600">
          <h2 className="text-text-primary font-semibold">New Workspace</h2>
          <p className="text-text-muted text-xs mt-0.5">Upload multiple files and ask questions in one place.</p>
        </div>
        <form onSubmit={handleSubmit} className="px-6 py-5 space-y-4">
          <div>
            <label className="text-text-secondary text-xs font-medium block mb-1.5">Workspace Name</label>
            <input
              autoFocus
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. Q4 Sales Analysis"
              className="input-base w-full"
              maxLength={200}
            />
          </div>
          <div>
            <label className="text-text-secondary text-xs font-medium block mb-1.5">Description <span className="text-text-muted">(optional)</span></label>
            <textarea
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="What are you analyzing?"
              rows={2}
              className="input-base w-full resize-none"
              maxLength={500}
            />
          </div>
          {error && <p className="text-red-400 text-xs">{error}</p>}
          <div className="flex gap-3 pt-1">
            <button type="button" onClick={onClose} className="btn-ghost flex-1">Cancel</button>
            <button type="submit" disabled={loading || !name.trim()} className="btn-primary flex-1">
              {loading ? 'Creating…' : 'Create Workspace'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
