import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class GameMode(str, enum.Enum):
    LADDER = "ladder"
    NON_LADDER = "non_ladder"
    HARDCORE = "hardcore"
    HARDCORE_LADDER = "hardcore_ladder"


class CharacterClass(str, enum.Enum):
    AMAZON = "amazon"
    NECROMANCER = "necromancer"
    BARBARIAN = "barbarian"
    SORCERESS = "sorceress"
    PALADIN = "paladin"
    DRUID = "druid"
    ASSASSIN = "assassin"
    WARLOCK = "warlock"


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    game_mode: Mapped[GameMode] = mapped_column(Enum(GameMode))
    character_class: Mapped[CharacterClass] = mapped_column(Enum(CharacterClass))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    runs: Mapped[list["Run"]] = relationship(back_populates="profile", cascade="all, delete-orphan")
