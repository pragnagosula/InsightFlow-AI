"""
Persists chart records and serves chart data.
"""
from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException

from app.config import settings
from app.repositories.chart_repository import chart_repo
from app.schemas.analysis import ChartResponse


async def save_chart(
    workspace_id: str,
    message_id: str,
    chart_type: str,
    title: str,
    plotly_json: dict,
    image_path: str = "",
) -> str:
    now = datetime.utcnow()
    doc = {
        "workspace_id": workspace_id,
        "message_id": message_id,
        "chart_type": chart_type,
        "title": title,
        "image_path": image_path,
        "plotly_json": plotly_json,
        "created_at": now,
    }
    return await chart_repo.insert(doc)


async def list_charts(workspace_id: str) -> list[ChartResponse]:
    docs = await chart_repo.find_by_workspace(workspace_id)
    return [_to_response(d) for d in docs]


async def get_chart(chart_id: str) -> ChartResponse:
    doc = await chart_repo.find_by_id(chart_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Chart not found")
    return _to_response(doc)


def _to_response(doc: dict) -> ChartResponse:
    image_url = None
    image_path = doc.get("image_path", "")
    if image_path:
        from pathlib import Path as _Path
        image_url = f"/storage/charts/{_Path(image_path).name}"
    return ChartResponse(
        id=doc["_id"],
        workspace_id=doc["workspace_id"],
        message_id=doc["message_id"],
        chart_type=doc["chart_type"],
        title=doc["title"],
        plotly_json=doc.get("plotly_json", {}),
        image_url=image_url,
        created_at=str(doc["created_at"]),
    )
