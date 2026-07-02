"""
Handles CSV/XLSX upload, triggers preprocessing pipeline in background.
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.storage import raw_path, cleaned_path, save_upload
from app.repositories.dataset_repository import dataset_repo
from app.repositories.report_repository import preprocessing_report_repo
from app.schemas.upload import DatasetResponse, PreprocessingReportResponse
from app.services import preprocessing_service


ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


async def upload_dataset(workspace_id: str, file: UploadFile) -> DatasetResponse:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    content = await file.read()
    raw = raw_path(workspace_id, file.filename)
    await save_upload(content, raw)

    now = datetime.utcnow()
    doc = {
        "workspace_id": workspace_id,
        "original_filename": file.filename,
        "original_path": str(raw),
        "cleaned_path": "",
        "file_type": suffix.lstrip("."),
        "columns": [],
        "row_count": 0,
        "preprocessing_status": "pending",
        "quality_score": 0.0,
        "preprocessing_report_id": None,
        "created_at": now,
    }
    dataset_id = await dataset_repo.insert(doc)

    # Kick off preprocessing without blocking the response
    asyncio.create_task(_run_preprocessing(dataset_id, workspace_id, raw, file.filename))

    return DatasetResponse(
        id=dataset_id,
        workspace_id=workspace_id,
        original_filename=file.filename,
        file_type=suffix.lstrip("."),
        columns=[],
        row_count=0,
        preprocessing_status="pending",
        quality_score=0.0,
        preprocessing_report_id=None,
        created_at=now,
    )


async def _run_preprocessing(dataset_id: str, workspace_id: str, raw: Path, filename: str) -> None:
    await dataset_repo.update_status(dataset_id, "processing")
    cleaned = cleaned_path(workspace_id, filename)
    try:
        report = await asyncio.to_thread(preprocessing_service.run_pipeline, raw, cleaned)
        report_doc = {
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            **{k: report[k] for k in (
                "original_rows", "cleaned_rows", "removed_duplicates",
                "null_fills", "type_conversions", "outliers_handled",
                "removed_columns", "quality_score", "detailed_log",
            )},
            "created_at": datetime.utcnow(),
        }
        report_id = await preprocessing_report_repo.insert(report_doc)
        await dataset_repo.update_status(dataset_id, "complete", {
            "cleaned_path": str(cleaned),
            "columns": report["columns"],
            "row_count": report["row_count"],
            "quality_score": report["quality_score"],
            "preprocessing_report_id": report_id,
        })
    except Exception as exc:
        await dataset_repo.update_status(dataset_id, "failed", {"error": str(exc)})


async def list_datasets(workspace_id: str) -> list[DatasetResponse]:
    docs = await dataset_repo.find_by_workspace(workspace_id)
    return [_to_response(d) for d in docs]


async def get_dataset(dataset_id: str) -> DatasetResponse:
    doc = await dataset_repo.find_by_id(dataset_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return _to_response(doc)


async def get_preprocessing_report(dataset_id: str) -> PreprocessingReportResponse:
    doc = await dataset_repo.find_by_id(dataset_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Dataset not found")
    report = await preprocessing_report_repo.find_by_dataset(dataset_id)
    if not report:
        raise HTTPException(status_code=404, detail="Preprocessing report not available yet")
    return PreprocessingReportResponse(
        id=report["_id"],
        dataset_id=report["dataset_id"],
        original_rows=report["original_rows"],
        cleaned_rows=report["cleaned_rows"],
        removed_duplicates=report["removed_duplicates"],
        null_fills=report["null_fills"],
        type_conversions=report["type_conversions"],
        outliers_handled=report["outliers_handled"],
        removed_columns=report["removed_columns"],
        quality_score=report["quality_score"],
        detailed_log=report["detailed_log"],
        created_at=report["created_at"],
    )


async def delete_dataset(dataset_id: str) -> None:
    doc = await dataset_repo.find_by_id(dataset_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Dataset not found")
    for p in (doc.get("original_path"), doc.get("cleaned_path")):
        if p:
            Path(p).unlink(missing_ok=True)
    await preprocessing_report_repo.delete_many({"dataset_id": dataset_id})
    await dataset_repo.delete_by_id(dataset_id)


def _to_response(doc: dict) -> DatasetResponse:
    return DatasetResponse(
        id=doc["_id"],
        workspace_id=doc["workspace_id"],
        original_filename=doc["original_filename"],
        file_type=doc["file_type"],
        columns=doc.get("columns", []),
        row_count=doc.get("row_count", 0),
        preprocessing_status=doc["preprocessing_status"],
        quality_score=doc.get("quality_score", 0.0),
        preprocessing_report_id=doc.get("preprocessing_report_id"),
        created_at=doc["created_at"],
    )
