from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.upload import UploadResponse
from app.services import dataset_service, document_service

router = APIRouter()

DATASET_EXTS = {".csv", ".xlsx", ".xls"}
DOCUMENT_EXTS = {".pdf", ".docx", ".txt", ".md"}


@router.post("/workspaces/{workspace_id}/upload", response_model=list[UploadResponse], status_code=201)
async def upload_files(workspace_id: str, files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    results: list[UploadResponse] = []
    for file in files:
        suffix = Path(file.filename).suffix.lower()
        if suffix in DATASET_EXTS:
            resp = await dataset_service.upload_dataset(workspace_id, file)
            results.append(UploadResponse(
                id=resp.id,
                filename=resp.original_filename,
                file_type=resp.file_type,
                kind="dataset",
                status=resp.preprocessing_status,
                workspace_id=resp.workspace_id,
                created_at=resp.created_at,
            ))
        elif suffix in DOCUMENT_EXTS:
            resp = await document_service.upload_document(workspace_id, file)
            results.append(UploadResponse(
                id=resp.id,
                filename=resp.filename,
                file_type=resp.file_type,
                kind="document",
                status=resp.embedding_status,
                workspace_id=resp.workspace_id,
                created_at=resp.created_at,
            ))
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file: {file.filename}")

    return results


@router.delete("/workspaces/{workspace_id}/files/{file_id}", status_code=204)
async def remove_file(workspace_id: str, file_id: str):
    from app.repositories.dataset_repository import dataset_repo
    from app.repositories.document_repository import document_repo

    ds = await dataset_repo.find_by_id(file_id)
    if ds and ds["workspace_id"] == workspace_id:
        await dataset_service.delete_dataset(file_id)
        return

    doc = await document_repo.find_by_id(file_id)
    if doc and doc["workspace_id"] == workspace_id:
        await document_service.delete_document(file_id)
        return

    raise HTTPException(status_code=404, detail="File not found in this workspace")
