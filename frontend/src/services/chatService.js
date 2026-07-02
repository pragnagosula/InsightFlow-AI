import api from './api'

export const sendMessage = (workspaceId, data) =>
  api.post(`/workspaces/${workspaceId}/chat`, data).then(r => r.data)

export const getMessages = (conversationId) =>
  api.get(`/conversations/${conversationId}/messages`).then(r => r.data)

export const getCharts = (workspaceId) =>
  api.get(`/workspaces/${workspaceId}/charts`).then(r => r.data)
