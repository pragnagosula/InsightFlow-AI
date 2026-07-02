"""
Chat service: persists messages and delegates to agent orchestrator.
"""
from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException

from app.repositories.conversation_repository import conversation_repo
from app.repositories.message_repository import message_repo
from app.repositories.workspace_repository import workspace_repo
from app.schemas.chat import ChatRequest, ChatResponse, ConversationResponse, MessageResponse


async def send_message(workspace_id: str, request: ChatRequest) -> ChatResponse:
    ws = await workspace_repo.find_by_id(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")

    conversation_id = request.conversation_id
    if not conversation_id:
        conversation_id = await _create_conversation(workspace_id, request.message)
    else:
        conv = await conversation_repo.find_by_id(conversation_id)
        if not conv or conv["workspace_id"] != workspace_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

    now = datetime.utcnow()
    user_msg_doc = {
        "conversation_id": conversation_id,
        "workspace_id": workspace_id,
        "role": "user",
        "content": request.message,
        "files_used": [],
        "chart_ids": [],
        "agent_trace": {},
        "created_at": now,
    }
    await message_repo.insert(user_msg_doc)

    history = await message_repo.get_recent(conversation_id, n=10)

    from app.agents.orchestrator import run_pipeline
    result = await run_pipeline(
        workspace_id=workspace_id,
        question=request.message,
        conversation_id=conversation_id,
        history=history,
    )

    ai_msg_doc = {
        "conversation_id": conversation_id,
        "workspace_id": workspace_id,
        "role": "assistant",
        "content": result["content"],
        "files_used": result.get("files_used", []),
        "chart_ids": [c["id"] for c in result.get("charts", [])],
        "citations": result.get("citations", []),
        "citation_sources": result.get("citation_sources", []),
        "agent_trace": result.get("agent_trace", {}),
        "created_at": datetime.utcnow(),
    }
    msg_id = await message_repo.insert(ai_msg_doc)

    await conversation_repo.set_fields(conversation_id, {"updated_at": datetime.utcnow()})

    from app.schemas.chat import ChartInfo, CitationSource
    return ChatResponse(
        message_id=msg_id,
        conversation_id=conversation_id,
        content=result["content"],
        charts=[ChartInfo(**c) for c in result.get("charts", [])],
        files_used=result.get("files_used", []),
        citations=result.get("citations", []),
        citation_sources=[CitationSource(**s) for s in result.get("citation_sources", [])],
        created_at=datetime.utcnow(),
    )


async def list_conversations(workspace_id: str) -> list[ConversationResponse]:
    docs = await conversation_repo.find_by_workspace(workspace_id)
    return [
        ConversationResponse(
            id=d["_id"],
            workspace_id=d["workspace_id"],
            title=d["title"],
            created_at=d["created_at"],
            updated_at=d["updated_at"],
        )
        for d in docs
    ]


async def get_messages(conversation_id: str) -> list[MessageResponse]:
    docs = await message_repo.find_by_conversation(conversation_id)
    return [
        MessageResponse(
            id=d["_id"],
            role=d["role"],
            content=d["content"],
            chart_ids=d.get("chart_ids", []),
            files_used=d.get("files_used", []),
            citations=d.get("citations", []),
            citation_sources=d.get("citation_sources", []),
            created_at=d["created_at"],
        )
        for d in docs
    ]


async def _create_conversation(workspace_id: str, first_message: str) -> str:
    title = first_message[:60] + ("…" if len(first_message) > 60 else "")
    now = datetime.utcnow()
    return await conversation_repo.insert({
        "workspace_id": workspace_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
    })
