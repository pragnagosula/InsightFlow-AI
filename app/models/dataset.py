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

PreprocessingStatus = str  # "pending" | "processing" | "complete" | "failed"


class DatasetModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    workspace_id: str
    original_filename: str
    original_path: str
    cleaned_path: str = ""
    file_type: str  # "csv" | "xlsx"
    columns: list[str] = Field(default_factory=list)
    row_count: int = 0
    preprocessing_status: PreprocessingStatus = "pending"
    quality_score: float = 0.0
    preprocessing_report_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
