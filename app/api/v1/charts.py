from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import HTTPException

from app.schemas.analysis import ChartResponse
from app.services import chart_service

router = APIRouter()


@router.get("/workspaces/{workspace_id}/charts", response_model=list[ChartResponse])
async def list_charts(workspace_id: str):
    return await chart_service.list_charts(workspace_id)


@router.get("/charts/{chart_id}", response_model=ChartResponse)
async def get_chart(chart_id: str):
    return await chart_service.get_chart(chart_id)


@router.get("/charts/{chart_id}/image")
async def get_chart_image(chart_id: str):
    from app.config import settings
    path = settings.CHARTS_DIR / f"{chart_id}.png"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Chart image not found")
    return FileResponse(str(path), media_type="image/png")
