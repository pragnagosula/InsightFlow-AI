from datetime import datetime
from pydantic import BaseModel, Field


class WorkspaceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: str
    file_count: int = 0
    created_at: datetime
    updated_at: datetime


class FileEntry(BaseModel):
    id: str
    filename: str
    file_type: str
    kind: str  # "dataset" | "document"
    status: str
    row_count: int | None = None
    chunk_count: int | None = None
    quality_score: float | None = None
    columns: list[str] | None = None
    created_at: datetime
