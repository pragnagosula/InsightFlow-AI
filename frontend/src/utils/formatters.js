export const formatDate = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

export const formatTime = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

export const formatRelative = (iso) => {
  if (!iso) return ''
  const diff = Date.now() - new Date(iso).getTime()
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}d ago`
  return formatDate(iso)
}

export const fileIcon = (fileType, kind) => {
  if (kind === 'dataset') return '📊'
  const icons = { pdf: '📄', docx: '📝', txt: '📃', md: '📋' }
  return icons[fileType] ?? '📁'
}

export const statusColor = (status) => {
  const map = {
    complete: 'text-green-400',
    processing: 'text-yellow-400',
    pending: 'text-text-muted',
    failed: 'text-red-400',
  }
  return map[status] ?? 'text-text-muted'
}

export const qualityColor = (score) => {
  if (score >= 0.85) return 'text-green-400'
  if (score >= 0.65) return 'text-yellow-400'
  return 'text-red-400'
}

export const truncate = (str, n = 40) =>
  str && str.length > n ? str.slice(0, n) + '…' : str
