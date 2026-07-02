from fastapi import APIRouter
from app.schemas.upload import DocumentResponse
from app.services import document_service

router = APIRouter()


@router.get("/workspaces/{workspace_id}/documents", response_model=list[DocumentResponse])
async def list_documents(workspace_id: str):
    return await document_service.list_documents(workspace_id)


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    return await document_service.get_document(document_id)
