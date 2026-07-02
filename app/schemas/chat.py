from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: str | None = None


class ChartInfo(BaseModel):
    id: str
    chart_type: str
    title: str
    plotly_json: dict
    image_url: str | None = None


class CitationSource(BaseModel):
    filename: str
    snippets: list[str]


class ChatResponse(BaseModel):
    message_id: str
    conversation_id: str
    content: str
    charts: list[ChartInfo] = Field(default_factory=list)
    files_used: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    citation_sources: list[CitationSource] = Field(default_factory=list)
    created_at: datetime


class ConversationResponse(BaseModel):
    id: str
    workspace_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    chart_ids: list[str] = Field(default_factory=list)
    files_used: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    citation_sources: list[CitationSource] = Field(default_factory=list)
    created_at: datetime
