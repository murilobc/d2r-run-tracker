from pydantic import BaseModel

from app.models.item import ItemCategory


class ItemResponse(BaseModel):
    id: int
    name: str
    category: ItemCategory
    subcategory: str
    aliases: list[str]
    is_rotw: bool
    is_ladder_only: bool

    model_config = {"from_attributes": True}
