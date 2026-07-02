import { useRef } from 'react'

const ACCEPTED = '.csv,.xlsx,.xls,.pdf,.docx,.txt,.md'

export default function UploadButton({ workspaceId, onUpload }) {
  const inputRef = useRef(null)

  const handleChange = async (e) => {
    if (e.target.files?.length) {
      await onUpload(e.target.files)
      e.target.value = ''
    }
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={ACCEPTED}
        className="hidden"
        onChange={handleChange}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        className="w-7 h-7 rounded-lg hover:bg-surface-600 flex items-center justify-center text-text-muted hover:text-accent transition-colors shrink-0"
        title="Upload files (CSV, Excel, PDF, DOCX, TXT, MD)"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </>
  )
}
