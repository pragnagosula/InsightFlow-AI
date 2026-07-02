from datetime import datetime
from typing import Any, Annotated
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field


def _coerce_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError(f"Invalid ObjectId: {v}")


PyObjectId = Annotated[str, BeforeValidator(_coerce_object_id)]


class ChartModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    workspace_id: str
    message_id: str
    chart_type: str
    title: str
    image_path: str = ""
    plotly_json: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
