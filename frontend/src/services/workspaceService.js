import api from './api'

export const getWorkspaces = () =>
  api.get('/workspaces/').then(r => r.data)

export const createWorkspace = (data) =>
  api.post('/workspaces/', data).then(r => r.data)

export const getWorkspace = (id) =>
  api.get(`/workspaces/${id}`).then(r => r.data)

export const updateWorkspace = (id, data) =>
  api.put(`/workspaces/${id}`, data).then(r => r.data)

export const deleteWorkspace = (id) =>
  api.delete(`/workspaces/${id}`)

export const getWorkspaceFiles = (id) =>
  api.get(`/workspaces/${id}/files`).then(r => r.data)

export const getConversations = (id) =>
  api.get(`/workspaces/${id}/conversations`).then(r => r.data)

export const getDatasets = (id) =>
  api.get(`/workspaces/${id}/datasets`).then(r => r.data)

export const getPreprocessingReport = (datasetId) =>
  api.get(`/datasets/${datasetId}/report`).then(r => r.data)

export const getWorkspaceCharts = (id) =>
  api.get(`/workspaces/${id}/charts`).then(r => r.data)

export const getWorkspaceReports = (id) =>
  api.get(`/workspaces/${id}/reports`).then(r => r.data)

export const createReport = (workspaceId, data) =>
  api.post(`/workspaces/${workspaceId}/reports`, data).then(r => r.data)
