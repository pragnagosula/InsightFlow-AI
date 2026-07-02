from datetime import datetime
from typing import Any, Annotated
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field


def _coerce_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError(f"Invalid ObjectId: {v}")


PyObjectId = Annotated[str, BeforeValidator(_coerce_object_id)]


class MessageModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    conversation_id: str
    workspace_id: str
    role: str  # "user" | "assistant"
    content: str
    files_used: list[str] = Field(default_factory=list)
    chart_ids: list[str] = Field(default_factory=list)
    agent_trace: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
