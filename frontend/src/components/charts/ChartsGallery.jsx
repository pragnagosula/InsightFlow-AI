import { useEffect } from 'react'
import useWorkspaceStore from '../../store/workspaceStore'
import ChartRenderer from './ChartRenderer'
import { formatRelative } from '../../utils/formatters'

export default function ChartsGallery({ workspaceId }) {
  const { charts, isFetchingCharts, fetchCharts } = useWorkspaceStore()

  useEffect(() => {
    if (workspaceId) fetchCharts(workspaceId)
  }, [workspaceId])

  if (isFetchingCharts) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-6 h-6 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          <p className="text-text-muted text-sm">Loading charts…</p>
        </div>
      </div>
    )
  }

  if (charts.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-4 text-center p-10">
        <div className="w-14 h-14 rounded-2xl bg-surface-700 flex items-center justify-center">
          <svg className="w-7 h-7 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <div>
          <p className="text-text-primary font-medium text-sm">No charts yet</p>
          <p className="text-text-muted text-xs mt-1 max-w-xs leading-relaxed">
            Charts are generated automatically when you ask analytical questions in the Chat tab
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="p-5 space-y-4 max-w-3xl mx-auto">
        <div className="flex items-center justify-between">
          <p className="text-xs text-text-muted">
            {charts.length} chart{charts.length !== 1 ? 's' : ''} generated
          </p>
          <button
            onClick={() => fetchCharts(workspaceId)}
            className="text-xs text-text-muted hover:text-accent transition-colors flex items-center gap-1.5"
          >
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>

        {charts.map(chart => (
          <div key={chart.id} className="animate-fade-in">
            <p className="text-xs text-text-muted mb-2">{formatRelative(chart.created_at)}</p>
            <ChartRenderer chart={chart} />
          </div>
        ))}
      </div>
    </div>
  )
}
