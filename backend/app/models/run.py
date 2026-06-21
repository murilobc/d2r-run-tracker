import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class Location(str, enum.Enum):
    ANDARIEL = "andariel"
    COUNTESS = "countess"
    PIT = "pit"
    COWS = "cows"
    STONY_TOMBS = "stony_tombs"
    ARCANE_SANCTUARY = "arcane_sanctuary"
    ANCIENT_TUNNELS = "ancient_tunnels"
    LOWER_KURAST = "lower_kurast"
    TRAVINCAL = "travincal"
    MEPHISTO = "mephisto"
    CHAOS_SANCTUARY = "chaos_sanctuary"
    ELDRITCH_SHENK = "eldritch_shenk"
    PINDLESKIN = "pindleskin"
    WORLDSTONE_KEEP = "worldstone_keep"
    TERROR_ZONE = "terror_zone"
    COLOSSAL_ANCIENTS = "colossal_ancients"


class Run(Base):
    __tablename__ = "runs"
    __table_args__ = (
        Index("ix_runs_profile_location", "profile_id", "location"),
        Index("uq_runs_profile_location_number", "profile_id", "location", "run_number", unique=True),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"))
    location: Mapped[Location] = mapped_column(Enum(Location))
    run_number: Mapped[int] = mapped_column(Integer)
    duration_seconds: Mapped[int] = mapped_column(Integer)
    terror_zone_note: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    profile: Mapped["Profile"] = relationship(back_populates="runs")
    items: Mapped[list["RunItem"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class RunItem(Base):
    __tablename__ = "run_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))

    run: Mapped["Run"] = relationship(back_populates="items")
    item: Mapped["Item"] = relationship()
