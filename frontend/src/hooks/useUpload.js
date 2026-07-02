import { useRef } from 'react'
import useWorkspaceStore from '../store/workspaceStore'

export function useUpload(workspaceId) {
  const { isUploading, uploadFiles } = useWorkspaceStore()
  const inputRef = useRef(null)

  const openPicker = () => inputRef.current?.click()

  const handleFiles = async (fileList) => {
    if (!fileList?.length) return
    await uploadFiles(workspaceId, fileList)
    if (inputRef.current) inputRef.current.value = ''
  }

  const handleInputChange = (e) => handleFiles(e.target.files)

  const handleDrop = (e) => {
    e.preventDefault()
    handleFiles(e.dataTransfer.files)
  }

  return { isUploading, inputRef, openPicker, handleInputChange, handleDrop }
}
