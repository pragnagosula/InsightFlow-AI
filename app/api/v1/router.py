from fastapi import APIRouter
from app.api.v1 import workspaces, upload, chat, datasets, documents, charts, reports

api_router = APIRouter()

api_router.include_router(workspaces.router, prefix="/workspaces", tags=["Workspaces"])
api_router.include_router(upload.router, tags=["Upload"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(datasets.router, tags=["Datasets"])
api_router.include_router(documents.router, tags=["Documents"])
api_router.include_router(charts.router, tags=["Charts"])
api_router.include_router(reports.router, tags=["Reports"])
