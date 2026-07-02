import api from './api'

export const uploadFiles = (workspaceId, files) => {
  const form = new FormData()
  Array.from(files).forEach(f => form.append('files', f))
  return api.post(`/workspaces/${workspaceId}/upload`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(r => r.data)
}

export const removeFile = (workspaceId, fileId) =>
  api.delete(`/workspaces/${workspaceId}/files/${fileId}`)

export const downloadRaw = (datasetId) =>
  `/api/v1/datasets/${datasetId}/download/raw`

export const downloadCleaned = (datasetId) =>
  `/api/v1/datasets/${datasetId}/download/cleaned`
