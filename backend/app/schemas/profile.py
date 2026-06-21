from datetime import datetime

from pydantic import BaseModel, Field

from app.models.profile import CharacterClass, GameMode


class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    game_mode: GameMode
    character_class: CharacterClass


class ProfileUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    game_mode: GameMode | None = None
    character_class: CharacterClass | None = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    game_mode: GameMode
    character_class: CharacterClass
    created_at: datetime

    model_config = {"from_attributes": True}
