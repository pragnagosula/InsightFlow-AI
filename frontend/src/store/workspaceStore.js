import { create } from 'zustand'
import * as workspaceService from '../services/workspaceService'
import * as chatService from '../services/chatService'
import * as uploadService from '../services/uploadService'

const useWorkspaceStore = create((set, get) => ({
  // ── State ──────────────────────────────────────────────────
  workspaces: [],
  currentWorkspace: null,
  files: [],
  conversations: [],
  currentConversation: null,
  messages: [],
  charts: [],
  reports: [],

  isLoadingWorkspaces: false,
  isLoadingMessages: false,
  isSending: false,
  isUploading: false,
  isFetchingCharts: false,
  isFetchingReports: false,
  isGeneratingReport: false,
  error: null,

  // ── Workspaces ─────────────────────────────────────────────
  fetchWorkspaces: async () => {
    set({ isLoadingWorkspaces: true, error: null })
    try {
      const workspaces = await workspaceService.getWorkspaces()
      set({ workspaces, isLoadingWorkspaces: false })
    } catch (err) {
      set({ error: err.message, isLoadingWorkspaces: false })
    }
  },

  createWorkspace: async (name, description = '') => {
    const workspace = await workspaceService.createWorkspace({ name, description })
    set(s => ({ workspaces: [workspace, ...s.workspaces] }))
    return workspace
  },

  deleteWorkspace: async (id) => {
    await workspaceService.deleteWorkspace(id)
    set(s => ({
      workspaces: s.workspaces.filter(w => w.id !== id),
      currentWorkspace: s.currentWorkspace?.id === id ? null : s.currentWorkspace,
      files: s.currentWorkspace?.id === id ? [] : s.files,
      messages: s.currentWorkspace?.id === id ? [] : s.messages,
      currentConversation: s.currentWorkspace?.id === id ? null : s.currentConversation,
    }))
  },

  selectWorkspace: async (workspace) => {
    // Use the full object from the local list when available (avoids an extra fetch
    // when the user clicks a workspace in the sidebar). Fall back to the API when
    // navigating directly to /workspace/:id with no local state (e.g. page refresh).
    const existing = get().workspaces.find(w => w.id === workspace.id)
    const full = existing ?? await workspaceService.getWorkspace(workspace.id)
    set({ currentWorkspace: full, messages: [], currentConversation: null, charts: [], reports: [] })
    await Promise.all([
      get().fetchFiles(full.id),
      get().fetchConversations(full.id),
    ])
  },

  // ── Files ──────────────────────────────────────────────────
  fetchFiles: async (workspaceId) => {
    const files = await workspaceService.getWorkspaceFiles(workspaceId)
    set({ files })
  },

  uploadFiles: async (workspaceId, fileList) => {
    set({ isUploading: true, error: null })
    try {
      await uploadService.uploadFiles(workspaceId, fileList)
      await get().fetchFiles(workspaceId)
    } catch (err) {
      set({ error: err.message })
      throw err
    } finally {
      set({ isUploading: false })
    }
  },

  removeFile: async (workspaceId, fileId) => {
    await uploadService.removeFile(workspaceId, fileId)
    set(s => ({ files: s.files.filter(f => f.id !== fileId) }))
  },

  pollFileStatus: async (workspaceId) => {
    const files = await workspaceService.getWorkspaceFiles(workspaceId)
    set({ files })
  },

  // ── Conversations ──────────────────────────────────────────
  fetchConversations: async (workspaceId) => {
    const conversations = await workspaceService.getConversations(workspaceId)
    set({ conversations })
  },

  selectConversation: async (conversation) => {
    set({ currentConversation: conversation, isLoadingMessages: true, messages: [] })
    try {
      const messages = await chatService.getMessages(conversation.id)
      set({ messages, isLoadingMessages: false })
    } catch {
      set({ isLoadingMessages: false })
    }
  },

  newChat: () => set({ currentConversation: null, messages: [] }),

  // ── Chat ───────────────────────────────────────────────────
  sendMessage: async (workspaceId, text) => {
    const { currentConversation } = get()
    set({ isSending: true, error: null })

    const tempId = `temp-${Date.now()}`
    set(s => ({
      messages: [
        ...s.messages,
        { id: tempId, role: 'user', content: text, chart_ids: [], files_used: [], created_at: new Date().toISOString() },
      ],
    }))

    try {
      const res = await chatService.sendMessage(workspaceId, {
        message: text,
        conversation_id: currentConversation?.id ?? null,
      })

      if (!currentConversation) {
        const conversations = await workspaceService.getConversations(workspaceId)
        set({
          conversations,
          currentConversation: { id: res.conversation_id, title: text.slice(0, 60) },
        })
      }

      set(s => {
        // Merge new charts into gallery state so Charts tab updates immediately
        const newGalleryCharts = (res.charts ?? []).map(c => ({
          ...c,
          workspace_id: workspaceId,
          message_id: res.message_id,
          created_at: res.created_at,
          image_url: null,
        }))
        return {
          messages: [
            ...s.messages,
            {
              id: res.message_id,
              role: 'assistant',
              content: res.content,
              charts: res.charts ?? [],
              chart_ids: res.charts?.map(c => c.id) ?? [],
              files_used: res.files_used ?? [],
              citations: res.citations ?? [],
              citation_sources: res.citation_sources ?? [],
              created_at: res.created_at,
            },
          ],
          charts: newGalleryCharts.length > 0 ? [...newGalleryCharts, ...s.charts] : s.charts,
          isSending: false,
        }
      })
    } catch (err) {
      set(s => ({
        messages: s.messages.filter(m => m.id !== tempId),
        isSending: false,
        error: err.message,
      }))
    }
  },

  // ── Charts ─────────────────────────────────────────────────
  fetchCharts: async (workspaceId) => {
    set({ isFetchingCharts: true })
    try {
      const charts = await workspaceService.getWorkspaceCharts(workspaceId)
      set({ charts, isFetchingCharts: false })
    } catch {
      set({ isFetchingCharts: false })
    }
  },

  // ── Reports ────────────────────────────────────────────────
  fetchReports: async (workspaceId) => {
    set({ isFetchingReports: true })
    try {
      const reports = await workspaceService.getWorkspaceReports(workspaceId)
      set({ reports, isFetchingReports: false })
    } catch {
      set({ isFetchingReports: false })
    }
  },

  generateReport: async (workspaceId, title, conversationId = null) => {
    set({ isGeneratingReport: true })
    try {
      const report = await workspaceService.createReport(workspaceId, {
        title,
        conversation_id: conversationId,
      })
      set(s => ({ reports: [report, ...s.reports], isGeneratingReport: false }))
      return report
    } catch (err) {
      set({ isGeneratingReport: false })
      throw err
    }
  },

  clearError: () => set({ error: null }),
}))

export default useWorkspaceStore
