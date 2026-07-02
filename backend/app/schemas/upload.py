from datetime import datetime
from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    kind: str  # "dataset" | "document"
    status: str
    workspace_id: str
    created_at: datetime


class DatasetResponse(BaseModel):
    id: str
    workspace_id: str
    original_filename: str
    file_type: str
    columns: list[str]
    row_count: int
    preprocessing_status: str
    quality_score: float
    preprocessing_report_id: str | None
    created_at: datetime


class DocumentResponse(BaseModel):
    id: str
    workspace_id: str
    filename: str
    file_type: str
    chunk_count: int
    embedding_status: str
    created_at: datetime


class PreprocessingReportResponse(BaseModel):
    id: str
    dataset_id: str
    original_rows: int
    cleaned_rows: int
    removed_duplicates: int
    null_fills: dict
    type_conversions: list[dict]
    outliers_handled: int
    removed_columns: list[str]
    quality_score: float
    detailed_log: list[str]
    created_at: datetime
