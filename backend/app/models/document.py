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

EmbeddingStatus = str  # "pending" | "processing" | "complete" | "failed"


class DocumentModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    workspace_id: str
    filename: str
    file_type: str  # "pdf" | "docx" | "txt" | "md"
    path: str
    faiss_index_path: str = ""
    chunk_count: int = 0
    embedding_status: EmbeddingStatus = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
