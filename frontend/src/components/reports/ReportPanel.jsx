import { useEffect, useState } from 'react'
import useWorkspaceStore from '../../store/workspaceStore'
import GenerateReportModal from './GenerateReportModal'
import { formatDate } from '../../utils/formatters'

export default function ReportPanel({ workspaceId }) {
  const {
    reports, isFetchingReports, isGeneratingReport,
    fetchReports, generateReport, conversations,
  } = useWorkspaceStore()

  const [showModal, setShowModal] = useState(false)
  const [successId, setSuccessId] = useState(null)

  useEffect(() => {
    if (workspaceId) fetchReports(workspaceId)
  }, [workspaceId])

  const handleGenerate = async (title, conversationId) => {
    try {
      const report = await generateReport(workspaceId, title, conversationId)
      setSuccessId(report.id)
      setShowModal(false)
      setTimeout(() => setSuccessId(null), 3000)
    } catch {
      // error is already in store
    }
  }

  const downloadReport = (report) => {
    window.open(`/api/v1/reports/${report.id}/download`, '_blank', 'noopener')
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Panel header */}
      <div className="px-5 py-3.5 border-b border-surface-600 flex items-center justify-between shrink-0">
        <p className="text-xs text-text-muted">
          {isFetchingReports ? 'Loading…' : `${reports.length} report${reports.length !== 1 ? 's' : ''}`}
        </p>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-accent hover:bg-accent/90 text-white text-xs font-medium transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Generate Report
        </button>
      </div>

      {/* Success toast */}
      {successId && (
        <div className="mx-5 mt-3 px-4 py-2.5 bg-green-900/30 border border-green-700/40 rounded-lg flex items-center gap-2 animate-fade-in shrink-0">
          <svg className="w-3.5 h-3.5 text-green-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <span className="text-green-300 text-xs">Report generated — click Download to save the PDF</span>
        </div>
      )}

      {/* Body */}
      <div className="flex-1 overflow-y-auto">
        {isFetchingReports ? (
          <div className="flex items-center justify-center h-32">
            <div className="w-5 h-5 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          </div>
        ) : reports.length === 0 ? (
          <EmptyState onGenerate={() => setShowModal(true)} />
        ) : (
          <ul className="p-5 space-y-2 max-w-2xl mx-auto">
            {reports.map(report => (
              <ReportRow
                key={report.id}
                report={report}
                isNew={report.id === successId}
                onDownload={() => downloadReport(report)}
              />
            ))}
          </ul>
        )}
      </div>

      {showModal && (
        <GenerateReportModal
          conversations={conversations}
          isGenerating={isGeneratingReport}
          onGenerate={handleGenerate}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  )
}

function ReportRow({ report, isNew, onDownload }) {
  return (
    <li className={`flex items-center gap-3 px-4 py-3.5 bg-surface-700 border rounded-xl transition-colors animate-fade-in ${isNew ? 'border-accent/40 bg-accent/5' : 'border-surface-600'}`}>
      <div className="w-8 h-8 rounded-lg bg-surface-600 flex items-center justify-center shrink-0">
        <svg className="w-4 h-4 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-text-primary text-sm font-medium truncate">{report.title}</p>
        <p className="text-text-muted text-xs mt-0.5">{formatDate(report.created_at)}</p>
      </div>

      <button
        onClick={onDownload}
        title="Download PDF"
        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-surface-500 hover:border-accent text-text-secondary hover:text-accent text-xs transition-colors shrink-0"
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        Download
      </button>
    </li>
  )
}

function EmptyState({ onGenerate }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 text-center p-10 h-full">
      <div className="w-14 h-14 rounded-2xl bg-surface-700 flex items-center justify-center">
        <svg className="w-7 h-7 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <div>
        <p className="text-text-primary font-medium text-sm">No reports yet</p>
        <p className="text-text-muted text-xs mt-1 max-w-xs leading-relaxed">
          Generate a PDF business report with AI-written executive summary, findings, and recommendations
        </p>
      </div>
      <button
        onClick={onGenerate}
        className="px-4 py-2 rounded-lg bg-accent hover:bg-accent/90 text-white text-sm font-medium transition-colors"
      >
        Generate your first report
      </button>
    </div>
  )
}
