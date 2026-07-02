from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse, ConversationResponse, MessageResponse
from app.services import chat_service

router = APIRouter()


@router.post("/workspaces/{workspace_id}/chat", response_model=ChatResponse)
async def send_message(workspace_id: str, request: ChatRequest):
    return await chat_service.send_message(workspace_id, request)


@router.get("/workspaces/{workspace_id}/conversations", response_model=list[ConversationResponse])
async def list_conversations(workspace_id: str):
    return await chat_service.list_conversations(workspace_id)


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_messages(conversation_id: str):
    return await chat_service.get_messages(conversation_id)
