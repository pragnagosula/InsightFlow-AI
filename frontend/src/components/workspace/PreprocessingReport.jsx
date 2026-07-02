import { qualityColor } from '../../utils/formatters'

export default function PreprocessingReport({ file, report, isLoading }) {
  if (file.status === 'pending' || file.status === 'processing') {
    return (
      <div className="text-center py-10">
        <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-text-muted text-sm">Preprocessing in progress…</p>
        <p className="text-text-muted text-xs mt-1">The file will be ready in a moment.</p>
      </div>
    )
  }

  if (file.status === 'failed') {
    return (
      <div className="px-3 py-3 bg-red-900/30 border border-red-700/40 rounded-lg">
        <p className="text-red-400 text-sm font-medium">Preprocessing failed</p>
        <p className="text-red-300/70 text-xs mt-1">Try removing and re-uploading the file.</p>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="space-y-3 animate-pulse">
        {[80, 60, 100, 70].map((w, i) => (
          <div key={i} className="h-5 bg-surface-600 rounded" style={{ width: `${w}%` }} />
        ))}
      </div>
    )
  }

  if (!report) {
    return <p className="text-text-muted text-sm">Report not available.</p>
  }

  const qualityPct = Math.round(report.quality_score * 100)
  const retentionPct = report.original_rows > 0
    ? Math.round((report.cleaned_rows / report.original_rows) * 100)
    : 100
  const barColor = qualityPct >= 85 ? 'bg-green-400' : qualityPct >= 65 ? 'bg-yellow-400' : 'bg-red-400'

  return (
    <div className="space-y-5">
      {/* Quality score */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-xs text-text-muted font-medium uppercase tracking-wider">Data Quality</span>
          <span className={`text-sm font-bold ${qualityColor(report.quality_score)}`}>{qualityPct}%</span>
        </div>
        <div className="h-2 bg-surface-600 rounded-full overflow-hidden">
          <div className={`h-full rounded-full transition-all duration-700 ${barColor}`} style={{ width: `${qualityPct}%` }} />
        </div>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 gap-2.5">
        <StatCard label="Original rows" value={report.original_rows.toLocaleString()} />
        <StatCard label="Cleaned rows" value={report.cleaned_rows.toLocaleString()} />
        <StatCard
          label="Duplicates removed"
          value={report.removed_duplicates}
          accent={report.removed_duplicates > 0 ? 'yellow' : null}
        />
        <StatCard
          label="Outliers capped"
          value={report.outliers_handled}
          accent={report.outliers_handled > 0 ? 'yellow' : null}
        />
      </div>

      {/* Row retention bar */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-xs text-text-muted">Row retention</span>
          <span className="text-xs text-text-secondary">{retentionPct}%</span>
        </div>
        <div className="h-1.5 bg-surface-600 rounded-full overflow-hidden">
          <div className="h-full bg-accent rounded-full" style={{ width: `${retentionPct}%` }} />
        </div>
      </div>

      {/* Null fills */}
      {Object.keys(report.null_fills).length > 0 && (
        <Section title={`Null fills (${Object.keys(report.null_fills).length})`}>
          {Object.entries(report.null_fills).map(([col, method]) => (
            <KV key={col} left={col} right={method} />
          ))}
        </Section>
      )}

      {/* Type conversions */}
      {report.type_conversions.length > 0 && (
        <Section title={`Type conversions (${report.type_conversions.length})`}>
          {report.type_conversions.map((tc, i) => (
            <KV key={i} left={tc.column} right={`${tc.from} → ${tc.to}`} />
          ))}
        </Section>
      )}

      {/* Removed columns */}
      {report.removed_columns.length > 0 && (
        <Section title="Constant columns removed">
          <div className="flex flex-wrap gap-1.5">
            {report.removed_columns.map(c => (
              <span key={c} className="px-2 py-0.5 bg-surface-700 rounded text-xs text-text-muted line-through">{c}</span>
            ))}
          </div>
        </Section>
      )}

      {/* Processing log */}
      <Section title="Processing log">
        <div className="max-h-48 overflow-y-auto space-y-1 pr-1">
          {report.detailed_log.map((line, i) => (
            <p key={i} className="text-xs text-text-muted leading-relaxed">· {line}</p>
          ))}
        </div>
      </Section>
    </div>
  )
}

function StatCard({ label, value, accent }) {
  const valueClass =
    accent === 'yellow' ? 'text-yellow-400' :
    accent === 'green' ? 'text-green-400' :
    'text-text-primary'

  return (
    <div className="bg-surface-700 border border-surface-600 rounded-lg px-3 py-2.5">
      <p className="text-text-muted text-xs mb-1">{label}</p>
      <p className={`text-sm font-semibold ${valueClass}`}>{value}</p>
    </div>
  )
}

function Section({ title, children }) {
  return (
    <div>
      <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">{title}</p>
      <div className="space-y-1.5">{children}</div>
    </div>
  )
}

function KV({ left, right }) {
  return (
    <div className="flex items-center justify-between gap-3 text-xs py-0.5">
      <span className="text-text-secondary font-mono truncate">{left}</span>
      <span className="text-text-muted shrink-0 text-right">{right}</span>
    </div>
  )
}
