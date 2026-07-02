import asyncio
from datetime import datetime
from fastapi import HTTPException

from app.repositories.workspace_repository import workspace_repo
from app.repositories.dataset_repository import dataset_repo
from app.repositories.document_repository import document_repo
from app.repositories.conversation_repository import conversation_repo
from app.repositories.message_repository import message_repo
from app.repositories.chart_repository import chart_repo
from app.repositories.report_repository import report_repo, preprocessing_report_repo
from app.core.storage import delete_workspace_files
from app.core.vector_store import VectorStore
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse, FileEntry


async def create_workspace(data: WorkspaceCreate) -> WorkspaceResponse:
    now = datetime.utcnow()
    doc = {"name": data.name, "description": data.description, "created_at": now, "updated_at": now}
    id_ = await workspace_repo.insert(doc)
    return WorkspaceResponse(
        id=id_, name=data.name, description=data.description,
        file_count=0, created_at=now, updated_at=now,
    )


async def list_workspaces() -> list[WorkspaceResponse]:
    docs = await workspace_repo.find_all()
    if not docs:
        return []

    # Parallel file-count queries per workspace
    async def _with_count(d: dict) -> WorkspaceResponse:
        wid = d["_id"]
        ds_count, doc_count = await asyncio.gather(
            dataset_repo.count({"workspace_id": wid}),
            document_repo.count({"workspace_id": wid}),
        )
        return WorkspaceResponse(
            **{**d, "id": wid, "file_count": ds_count + doc_count}
        )

    return await asyncio.gather(*[_with_count(d) for d in docs])


async def get_workspace(workspace_id: str) -> WorkspaceResponse:
    doc = await workspace_repo.find_by_id(workspace_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Workspace not found")
    ds_count, doc_count = await asyncio.gather(
        dataset_repo.count({"workspace_id": workspace_id}),
        document_repo.count({"workspace_id": workspace_id}),
    )
    return WorkspaceResponse(**{**doc, "id": doc["_id"], "file_count": ds_count + doc_count})


async def update_workspace(workspace_id: str, data: WorkspaceUpdate) -> WorkspaceResponse:
    doc = await workspace_repo.find_by_id(workspace_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Workspace not found")
    fields = {k: v for k, v in data.model_dump().items() if v is not None}
    if fields:
        await workspace_repo.set_fields(workspace_id, fields)
    return await get_workspace(workspace_id)


async def delete_workspace(workspace_id: str) -> None:
    doc = await workspace_repo.find_by_id(workspace_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Delete FAISS indexes for all documents before removing DB records
    docs = await document_repo.find_by_workspace(workspace_id)
    for d in docs:
        VectorStore.delete(d["_id"])

    # Delete every collection that carries workspace_id — messages included
    for col_repo in (
        dataset_repo, document_repo, conversation_repo,
        chart_repo, report_repo, preprocessing_report_repo,
        message_repo,
    ):
        await col_repo.delete_many({"workspace_id": workspace_id})

    delete_workspace_files(workspace_id)
    await workspace_repo.delete_by_id(workspace_id)


async def list_workspace_files(workspace_id: str) -> list[FileEntry]:
    datasets = await dataset_repo.find_by_workspace(workspace_id)
    documents = await document_repo.find_by_workspace(workspace_id)

    entries: list[FileEntry] = []
    for d in datasets:
        entries.append(FileEntry(
            id=d["_id"],
            filename=d["original_filename"],
            file_type=d["file_type"],
            kind="dataset",
            status=d["preprocessing_status"],
            row_count=d.get("row_count") or None,
            quality_score=d.get("quality_score") or None,
            columns=d.get("columns") or None,
            created_at=d["created_at"],
        ))
    for d in documents:
        entries.append(FileEntry(
            id=d["_id"],
            filename=d["filename"],
            file_type=d["file_type"],
            kind="document",
            status=d["embedding_status"],
            chunk_count=d.get("chunk_count") or None,
            created_at=d["created_at"],
        ))
    entries.sort(key=lambda e: e.created_at, reverse=True)
    return entries
