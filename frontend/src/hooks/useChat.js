import { useRef, useEffect } from 'react'
import useWorkspaceStore from '../store/workspaceStore'

export function useChat(workspaceId) {
  const {
    messages,
    currentConversation,
    conversations,
    isSending,
    isLoadingMessages,
    sendMessage,
    selectConversation,
    newChat,
    error,
    clearError,
  } = useWorkspaceStore()

  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isSending])

  const submit = async (text) => {
    if (!text.trim() || isSending) return
    await sendMessage(workspaceId, text)
  }

  return {
    messages,
    currentConversation,
    conversations,
    isSending,
    isLoadingMessages,
    bottomRef,
    submit,
    selectConversation,
    newChat,
    error,
    clearError,
  }
}
