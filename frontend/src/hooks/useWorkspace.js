import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import useWorkspaceStore from '../store/workspaceStore'

export function useWorkspaceList() {
  const { workspaces, isLoadingWorkspaces, fetchWorkspaces, createWorkspace, deleteWorkspace } =
    useWorkspaceStore()

  useEffect(() => {
    fetchWorkspaces()
  }, [])

  return { workspaces, isLoadingWorkspaces, createWorkspace, deleteWorkspace }
}

export function useActiveWorkspace(workspaceId) {
  const {
    currentWorkspace,
    files,
    conversations,
    isUploading,
    selectWorkspace,
    fetchFiles,
    uploadFiles,
    removeFile,
    pollFileStatus,
  } = useWorkspaceStore()

  useEffect(() => {
    if (!workspaceId) return
    if (currentWorkspace?.id !== workspaceId) {
      selectWorkspace({ id: workspaceId })
    }
  }, [workspaceId])

  // Poll for file status changes (preprocessing / embedding)
  useEffect(() => {
    if (!workspaceId) return
    const hasProcessing = files.some(f => f.status === 'pending' || f.status === 'processing')
    if (!hasProcessing) return
    const timer = setInterval(() => pollFileStatus(workspaceId), 3000)
    return () => clearInterval(timer)
  }, [workspaceId, files])

  return { currentWorkspace, files, conversations, isUploading, uploadFiles, removeFile }
}
