import { useState, useRef, useEffect } from 'react'
import FileChip from './FileChip'
import UploadButton from '../upload/UploadButton'

export default function PromptInput({ onSend, isSending, files, onRemoveFile, onUpload, onFileClick, isUploading, workspaceId }) {
  const [text, setText] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px'
    }
  }, [text])

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  const submit = () => {
    if (!text.trim() || isSending) return
    onSend(text)
    setText('')
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
  }

  return (
    <div className="border-t border-surface-600 bg-surface-800 px-4 pt-3 pb-4 shrink-0">
      {/* File chips row */}
      {files.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {files.map(f => (
            <FileChip key={f.id} file={f} onRemove={() => onRemoveFile(f.id)} onClick={onFileClick} />
          ))}
          {isUploading && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-600 border border-accent/40 text-xs text-accent animate-pulse">
              Uploading…
            </span>
          )}
        </div>
      )}

      {/* Input area */}
      <div className="flex items-end gap-2 bg-surface-700 border border-surface-500 rounded-xl px-3 py-2.5 focus-within:border-accent transition-colors">
        <UploadButton workspaceId={workspaceId} onUpload={onUpload} />

        <textarea
          ref={textareaRef}
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about your uploaded files…"
          rows={1}
          disabled={isSending}
          className="flex-1 bg-transparent text-text-primary placeholder-text-muted text-sm resize-none outline-none min-h-[24px] max-h-[200px] leading-relaxed disabled:opacity-50"
        />

        <button
          onClick={submit}
          disabled={!text.trim() || isSending}
          className="w-8 h-8 rounded-lg bg-accent hover:bg-accent-hover disabled:bg-surface-500 disabled:cursor-not-allowed flex items-center justify-center shrink-0 transition-colors"
          title="Send (Enter)"
        >
          {isSending ? (
            <svg className="w-4 h-4 text-white animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 100 16 8 8 0 01-8-8z" />
            </svg>
          ) : (
            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          )}
        </button>
      </div>
      <p className="text-center text-xs text-text-muted mt-2">
        Press <kbd className="px-1 py-0.5 bg-surface-600 rounded text-text-muted">Enter</kbd> to send · <kbd className="px-1 py-0.5 bg-surface-600 rounded text-text-muted">Shift+Enter</kbd> for new line
      </p>
    </div>
  )
}
