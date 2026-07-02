from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.schemas.analysis import ReportResponse, ReportCreate
from app.services import report_service

router = APIRouter()


@router.get("/workspaces/{workspace_id}/reports", response_model=list[ReportResponse])
async def list_reports(workspace_id: str):
    return await report_service.list_reports(workspace_id)


@router.post("/workspaces/{workspace_id}/reports", response_model=ReportResponse, status_code=201)
async def create_report(workspace_id: str, data: ReportCreate):
    from app.agents import report_agent
    content = await report_agent.generate_report_content(data.title, "", data.title)
    return await report_service.create_report(workspace_id, data, content)


@router.get("/reports/{report_id}/download")
async def download_report(report_id: str):
    path = await report_service.get_report_path(report_id)
    return FileResponse(str(path), filename=path.name, media_type="application/pdf")
