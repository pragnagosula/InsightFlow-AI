import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useActiveWorkspace } from '../hooks/useWorkspace'
import { useChat } from '../hooks/useChat'
import TopBar from '../components/layout/TopBar'
import ChatWindow from '../components/chat/ChatWindow'
import PromptInput from '../components/chat/PromptInput'
import FileDrawer from '../components/workspace/FileDrawer'
import ChartsGallery from '../components/charts/ChartsGallery'
import ReportPanel from '../components/reports/ReportPanel'
import useWorkspaceStore from '../store/workspaceStore'
import { getPreprocessingReport } from '../services/workspaceService'

const TABS = [
  {
    id: 'chat',
    label: 'Chat',
    icon: (
      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    ),
  },
  {
    id: 'charts',
    label: 'Charts',
    icon: (
      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
  },
  {
    id: 'reports',
    label: 'Reports',
    icon: (
      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
  },
]

export default function WorkspacePage() {
  const { workspaceId } = useParams()
  const { currentWorkspace, files, isUploading, uploadFiles, removeFile } = useActiveWorkspace(workspaceId)
  const { messages, isSending, isLoadingMessages, bottomRef, submit } = useChat(workspaceId)
  const { error, clearError, charts, reports } = useWorkspaceStore()

  const [activeTab, setActiveTab] = useState('chat')
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileReport, setFileReport] = useState(null)
  const [isLoadingReport, setIsLoadingReport] = useState(false)

  const openFile = async (file) => {
    setSelectedFile(file)
    setFileReport(null)
    if (file.kind === 'dataset' && file.status === 'complete') {
      setIsLoadingReport(true)
      try {
        const report = await getPreprocessingReport(file.id)
        setFileReport(report)
      } catch {
        // drawer shows graceful fallback
      } finally {
        setIsLoadingReport(false)
      }
    }
  }

  const closeFile = () => {
    setSelectedFile(null)
    setFileReport(null)
  }

  const tabBadge = { charts: charts.length, reports: reports.length }

  return (
    <div className="flex flex-col h-full overflow-hidden relative">
      <TopBar workspace={currentWorkspace} files={files} onFileClick={openFile} />

      {/* Tab bar */}
      <div className="border-b border-surface-600 px-4 flex items-center gap-0 shrink-0 bg-surface-900">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-1.5 px-4 py-2.5 text-xs font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-accent text-accent'
                : 'border-transparent text-text-muted hover:text-text-secondary hover:border-surface-500'
            }`}
          >
            {tab.icon}
            {tab.label}
            {tabBadge[tab.id] > 0 && (
              <span className={`ml-0.5 px-1.5 py-0.5 rounded-full text-[10px] leading-none ${
                activeTab === tab.id ? 'bg-accent/20 text-accent' : 'bg-surface-600 text-text-muted'
              }`}>
                {tabBadge[tab.id]}
              </span>
            )}
          </button>
        ))}
      </div>

      {error && (
        <div className="mx-4 mt-3 px-4 py-2.5 bg-red-900/40 border border-red-700/50 rounded-lg flex items-center justify-between animate-fade-in shrink-0">
          <span className="text-red-300 text-sm">{error}</span>
          <button onClick={clearError} className="text-red-400 hover:text-red-200 ml-3">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {/* Tab content */}
      {activeTab === 'chat' && (
        <>
          <ChatWindow
            messages={messages}
            isSending={isSending}
            isLoading={isLoadingMessages}
            bottomRef={bottomRef}
          />
          <PromptInput
            onSend={submit}
            isSending={isSending}
            files={files}
            onRemoveFile={(id) => removeFile(workspaceId, id)}
            onUpload={(fileList) => uploadFiles(workspaceId, fileList)}
            onFileClick={openFile}
            isUploading={isUploading}
            workspaceId={workspaceId}
          />
        </>
      )}

      {activeTab === 'charts' && (
        <ChartsGallery workspaceId={workspaceId} />
      )}

      {activeTab === 'reports' && (
        <ReportPanel workspaceId={workspaceId} />
      )}

      {selectedFile && (
        <FileDrawer
          file={selectedFile}
          report={fileReport}
          isLoading={isLoadingReport}
          onClose={closeFile}
        />
      )}
    </div>
  )
}
