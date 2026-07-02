from pydantic import BaseModel, Field


class ChartResponse(BaseModel):
    id: str
    workspace_id: str
    message_id: str
    chart_type: str
    title: str
    plotly_json: dict
    image_url: str | None = None
    created_at: str


class ReportResponse(BaseModel):
    id: str
    workspace_id: str
    title: str
    download_url: str
    created_at: str


class ReportCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    conversation_id: str | None = None
