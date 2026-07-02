"""
PDF report generation and retrieval.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi import HTTPException
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from app.config import settings
from app.repositories.report_repository import report_repo
from app.schemas.analysis import ReportResponse, ReportCreate


async def create_report(workspace_id: str, data: ReportCreate, content: str) -> ReportResponse:
    now = datetime.utcnow()
    doc_meta = {"workspace_id": workspace_id, "title": data.title, "path": "", "created_at": now}
    report_id = await report_repo.insert(doc_meta)

    path = settings.REPORTS_DIR / f"{report_id}.pdf"
    await _generate_pdf(path, data.title, content)
    await report_repo.set_fields(report_id, {"path": str(path)})

    return ReportResponse(
        id=report_id,
        workspace_id=workspace_id,
        title=data.title,
        download_url=f"/api/v1/reports/{report_id}/download",
        created_at=str(now),
    )


async def list_reports(workspace_id: str) -> list[ReportResponse]:
    docs = await report_repo.find_by_workspace(workspace_id)
    return [_to_response(d) for d in docs]


async def get_report_path(report_id: str) -> Path:
    doc = await report_repo.find_by_id(report_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Report not found")
    p = Path(doc["path"])
    if not p.exists():
        raise HTTPException(status_code=404, detail="Report file not found")
    return p


async def _generate_pdf(path: Path, title: str, body: str) -> None:
    import asyncio
    await asyncio.to_thread(_write_pdf, path, title, body)


def _write_pdf(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 20),
    ]
    for line in body.split("\n"):
        story.append(Paragraph(line or "&nbsp;", styles["Normal"]))
        story.append(Spacer(1, 4))
    doc.build(story)


def _to_response(doc: dict) -> ReportResponse:
    return ReportResponse(
        id=doc["_id"],
        workspace_id=doc["workspace_id"],
        title=doc["title"],
        download_url=f"/api/v1/reports/{doc['_id']}/download",
        created_at=str(doc["created_at"]),
    )
