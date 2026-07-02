import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'

export default function ChatWindow({ messages, isSending, isLoading, bottomRef }) {
  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center text-text-muted text-sm">
        Loading conversation…
      </div>
    )
  }

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-4 px-8 text-center">
        <div className="w-14 h-14 rounded-2xl bg-accent/10 border border-accent/20 flex items-center justify-center">
          <svg className="w-7 h-7 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1 1 .03 2.699-1.347 2.699H4.145c-1.377 0-2.347-1.7-1.347-2.699L4.2 15.3" />
          </svg>
        </div>
        <div>
          <h2 className="text-text-primary font-semibold text-base">Ask anything about your data</h2>
          <p className="text-text-muted text-sm mt-1 max-w-sm">
            Upload CSV, Excel, PDFs, or documents — then ask questions in plain English.
            The AI automatically selects the right files.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-2 mt-2 text-left max-w-md w-full">
          {[
            'Show monthly sales trend',
            'Summarize the strategy document',
            'Compare salaries with HR policy',
            'What are the top 5 products?',
          ].map(hint => (
            <div
              key={hint}
              className="px-3 py-2.5 bg-surface-700 border border-surface-600 rounded-lg text-xs text-text-secondary cursor-default hover:border-surface-400 transition-colors"
            >
              "{hint}"
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto py-4 space-y-1">
      {messages.map(msg => (
        <MessageBubble key={msg.id} message={msg} />
      ))}
      {isSending && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  )
}
