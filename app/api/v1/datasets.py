from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.schemas.upload import DatasetResponse, PreprocessingReportResponse
from app.services import dataset_service

router = APIRouter()


@router.get("/workspaces/{workspace_id}/datasets", response_model=list[DatasetResponse])
async def list_datasets(workspace_id: str):
    return await dataset_service.list_datasets(workspace_id)


@router.get("/datasets/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: str):
    return await dataset_service.get_dataset(dataset_id)


@router.get("/datasets/{dataset_id}/download/raw")
async def download_raw(dataset_id: str):
    ds = await dataset_service.get_dataset(dataset_id)
    from pathlib import Path
    path = Path(ds.original_filename)
    # Resolve actual stored path
    from app.repositories.dataset_repository import dataset_repo
    doc = await dataset_repo.find_by_id(dataset_id)
    raw = Path(doc["original_path"])
    return FileResponse(str(raw), filename=doc["original_filename"], media_type="application/octet-stream")


@router.get("/datasets/{dataset_id}/download/cleaned")
async def download_cleaned(dataset_id: str):
    from pathlib import Path
    from app.repositories.dataset_repository import dataset_repo
    from fastapi import HTTPException
    doc = await dataset_repo.find_by_id(dataset_id)
    if not doc or not doc.get("cleaned_path"):
        raise HTTPException(status_code=404, detail="Cleaned file not available yet")
    cleaned = Path(doc["cleaned_path"])
    if not cleaned.exists():
        raise HTTPException(status_code=404, detail="Cleaned file not found on disk")
    return FileResponse(
        str(cleaned),
        filename=f"cleaned_{doc['original_filename']}",
        media_type="text/csv",
    )


@router.get("/datasets/{dataset_id}/report", response_model=PreprocessingReportResponse)
async def get_report(dataset_id: str):
    return await dataset_service.get_preprocessing_report(dataset_id)
