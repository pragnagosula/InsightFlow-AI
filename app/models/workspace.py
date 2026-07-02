from datetime import datetime
from typing import Annotated, Any
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field


def _coerce_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError(f"Invalid ObjectId: {v}")


PyObjectId = Annotated[str, BeforeValidator(_coerce_object_id)]


class WorkspaceModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    name: str
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
