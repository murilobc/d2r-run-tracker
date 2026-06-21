from datetime import datetime

from pydantic import BaseModel, Field

from app.models.run import Location
from app.schemas.item import ItemResponse


class RunCreate(BaseModel):
    profile_id: int
    location: Location
    duration_seconds: int = Field(ge=1)
    item_ids: list[int] = []
    terror_zone_note: str | None = None


class RunItemResponse(BaseModel):
    id: int
    item: ItemResponse

    model_config = {"from_attributes": True}


class RunResponse(BaseModel):
    id: int
    profile_id: int
    location: Location
    run_number: int
    duration_seconds: int
    terror_zone_note: str | None
    created_at: datetime
    items: list[RunItemResponse] = []

    model_config = {"from_attributes": True}
