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


class ReportModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    workspace_id: str
    title: str
    path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}


class PreprocessingReportModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    dataset_id: str
    workspace_id: str
    original_rows: int = 0
    cleaned_rows: int = 0
    removed_duplicates: int = 0
    null_fills: dict = Field(default_factory=dict)
    type_conversions: list[dict] = Field(default_factory=list)
    outliers_handled: int = 0
    removed_columns: list[str] = Field(default_factory=list)
    quality_score: float = 0.0
    detailed_log: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
