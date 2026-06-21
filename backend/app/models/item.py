import enum

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class ItemCategory(str, enum.Enum):
    BASE = "base"
    MAGIC_RARE = "magic_rare"
    CHARM = "charm"
    JEWEL = "jewel"
    SET = "set"
    UNIQUE = "unique"
    RUNEWORD = "runeword"
    RUNE = "rune"
    CONSUMABLE = "consumable"


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    category: Mapped[ItemCategory] = mapped_column(Enum(ItemCategory), index=True)
    subcategory: Mapped[str] = mapped_column(String(100), default="")
    aliases: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    is_rotw: Mapped[bool] = mapped_column(Boolean, default=False)
    is_ladder_only: Mapped[bool] = mapped_column(Boolean, default=False)
