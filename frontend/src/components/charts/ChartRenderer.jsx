import { lazy, Suspense, useState } from 'react'

const Plot = lazy(() => import('react-plotly.js'))

export default function ChartRenderer({ chart }) {
  const [expanded, setExpanded] = useState(false)
  const hasPlotly = chart.plotly_json && Object.keys(chart.plotly_json).length > 0

  return (
    <div className="rounded-xl border border-surface-500 bg-surface-800 overflow-hidden">
      {/* Header */}
      <div className="px-4 py-2.5 border-b border-surface-600 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <svg className="w-3.5 h-3.5 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span className="text-text-secondary text-xs font-medium">{chart.title}</span>
          <span className="text-xs text-text-muted px-1.5 py-0.5 bg-surface-700 rounded-full">{chart.chart_type}</span>
        </div>
        <button
          onClick={() => setExpanded(e => !e)}
          className="text-xs text-text-muted hover:text-text-secondary transition-colors"
        >
          {expanded ? 'Collapse' : 'Expand'}
        </button>
      </div>

      {/* Chart body */}
      <div className={`transition-all duration-300 ${expanded ? 'max-h-[600px]' : 'max-h-72'} overflow-hidden`}>
        {hasPlotly ? (
          <Suspense
            fallback={
              chart.image_url
                ? <img src={chart.image_url} alt={chart.title} className="w-full object-contain" />
                : <div className="h-48 flex items-center justify-center text-text-muted text-sm">Loading chart…</div>
            }
          >
            <Plot
              data={chart.plotly_json.data ?? []}
              layout={{
                ...(chart.plotly_json.layout ?? {}),
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: { color: '#ececec', family: 'Inter, sans-serif', size: 11 },
                margin: { l: 50, r: 20, t: 20, b: 50 },
                autosize: true,
              }}
              config={{ responsive: true, displayModeBar: false }}
              style={{ width: '100%', height: expanded ? '520px' : '260px' }}
            />
          </Suspense>
        ) : chart.image_url ? (
          <img src={chart.image_url} alt={chart.title} className="w-full object-contain" />
        ) : (
          <div className="h-32 flex items-center justify-center text-text-muted text-sm">Chart unavailable</div>
        )}
      </div>
    </div>
  )
}
