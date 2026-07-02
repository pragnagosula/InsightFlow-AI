"""
Handles document uploads and triggers embedding pipeline in background.
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.storage import raw_path, save_upload
from app.core.vector_store import VectorStore
from app.repositories.document_repository import document_repo
from app.schemas.upload import DocumentResponse
from app.services.rag_service import build_index_for_document


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


async def upload_document(workspace_id: str, file: UploadFile) -> DocumentResponse:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    content = await file.read()
    dest = raw_path(workspace_id, file.filename)
    await save_upload(content, dest)

    now = datetime.utcnow()
    doc = {
        "workspace_id": workspace_id,
        "filename": file.filename,
        "file_type": suffix.lstrip("."),
        "path": str(dest),
        "faiss_index_path": "",
        "chunk_count": 0,
        "embedding_status": "pending",
        "created_at": now,
    }
    doc_id = await document_repo.insert(doc)

    asyncio.create_task(_run_embedding(doc_id, dest, suffix))

    return DocumentResponse(
        id=doc_id,
        workspace_id=workspace_id,
        filename=file.filename,
        file_type=suffix.lstrip("."),
        chunk_count=0,
        embedding_status="pending",
        created_at=now,
    )


async def _run_embedding(doc_id: str, path: Path, suffix: str) -> None:
    await document_repo.update_status(doc_id, "processing")
    try:
        chunk_count = await asyncio.to_thread(build_index_for_document, doc_id, path, suffix)
        from app.core.storage import faiss_index_path
        await document_repo.update_status(doc_id, "complete", {
            "faiss_index_path": str(faiss_index_path(doc_id)),
            "chunk_count": chunk_count,
        })
    except Exception as exc:
        await document_repo.update_status(doc_id, "failed", {"error": str(exc)})


async def list_documents(workspace_id: str) -> list[DocumentResponse]:
    docs = await document_repo.find_by_workspace(workspace_id)
    return [_to_response(d) for d in docs]


async def get_document(document_id: str) -> DocumentResponse:
    doc = await document_repo.find_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return _to_response(doc)


async def delete_document(document_id: str) -> None:
    doc = await document_repo.find_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    Path(doc["path"]).unlink(missing_ok=True)
    VectorStore.delete(document_id)
    await document_repo.delete_by_id(document_id)


def _to_response(doc: dict) -> DocumentResponse:
    return DocumentResponse(
        id=doc["_id"],
        workspace_id=doc["workspace_id"],
        filename=doc["filename"],
        file_type=doc["file_type"],
        chunk_count=doc.get("chunk_count", 0),
        embedding_status=doc["embedding_status"],
        created_at=doc["created_at"],
    )
