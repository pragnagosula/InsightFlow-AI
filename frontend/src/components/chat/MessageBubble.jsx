import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import ChartRenderer from '../charts/ChartRenderer'
import CitationCard from './CitationCard'
import { formatTime } from '../../utils/formatters'

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  if (isUser) {
    return (
      <div className="flex justify-end px-4 py-2 animate-fade-in">
        <div className="max-w-[75%]">
          <div className="bg-surface-600 border border-surface-500 rounded-2xl rounded-tr-sm px-4 py-3">
            <p className="text-text-primary text-sm whitespace-pre-wrap">{message.content}</p>
          </div>
          <p className="text-right text-xs text-text-muted mt-1 pr-1">{formatTime(message.created_at)}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-start gap-3 px-4 py-3 animate-slide-up">
      {/* Avatar */}
      <div className="w-7 h-7 rounded-full bg-accent/20 flex items-center justify-center shrink-0 mt-0.5">
        <span className="text-accent text-xs font-bold">IF</span>
      </div>

      <div className="flex-1 min-w-0">
        {/* Markdown content */}
        <div className="prose-ai">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
        </div>

        {/* Charts */}
        {message.charts?.length > 0 && (
          <div className="mt-4 space-y-4">
            {message.charts.map(chart => (
              <ChartRenderer key={chart.id} chart={chart} />
            ))}
          </div>
        )}

        {/* Citation cards (rich — have actual snippets) */}
        {message.citation_sources?.length > 0 && (
          <div className="mt-4 space-y-2">
            <p className="text-xs text-text-muted font-medium uppercase tracking-wider">Sources</p>
            {message.citation_sources.map((source, i) => (
              <CitationCard key={i} source={source} />
            ))}
          </div>
        )}

        {/* Fallback citation pills (older messages without snippet data) */}
        {!message.citation_sources?.length && message.citations?.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {message.citations.map((cite, i) => (
              <span
                key={i}
                className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-surface-700 border border-surface-500 text-xs text-text-muted"
              >
                <svg className="w-3 h-3 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {cite}
              </span>
            ))}
          </div>
        )}

        {/* Files used footer */}
        {message.files_used?.length > 0 && (
          <p className="mt-2 text-xs text-text-muted">
            Analysed {message.files_used.length} file{message.files_used.length !== 1 ? 's' : ''}
          </p>
        )}

        <p className="text-xs text-text-muted mt-2">{formatTime(message.created_at)}</p>
      </div>
    </div>
  )
}
