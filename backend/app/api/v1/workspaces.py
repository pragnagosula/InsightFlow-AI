from fastapi import APIRouter
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse, FileEntry
from app.services import workspace_service

router = APIRouter()


@router.post("/", response_model=WorkspaceResponse, status_code=201)
async def create_workspace(data: WorkspaceCreate):
    return await workspace_service.create_workspace(data)


@router.get("/", response_model=list[WorkspaceResponse])
async def list_workspaces():
    return await workspace_service.list_workspaces()


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: str):
    return await workspace_service.get_workspace(workspace_id)


@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(workspace_id: str, data: WorkspaceUpdate):
    return await workspace_service.update_workspace(workspace_id, data)


@router.delete("/{workspace_id}", status_code=204)
async def delete_workspace(workspace_id: str):
    await workspace_service.delete_workspace(workspace_id)


@router.get("/{workspace_id}/files", response_model=list[FileEntry])
async def list_workspace_files(workspace_id: str):
    return await workspace_service.list_workspace_files(workspace_id)
