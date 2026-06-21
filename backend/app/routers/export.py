from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.profile import Profile, GameMode, CharacterClass
from app.models.item import Item
from app.models.run import Run, RunItem, Location

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/{profile_id}")
async def export_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await db.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")

    result = await db.execute(
        select(Run)
        .where(Run.profile_id == profile_id)
        .options(selectinload(Run.items).selectinload(RunItem.item))
        .order_by(Run.created_at)
    )
    runs = result.scalars().all()

    return {
        "profile": {
            "name": profile.name,
            "game_mode": profile.game_mode.value,
            "character_class": profile.character_class.value,
        },
        "runs": [
            {
                "location": r.location.value,
                "run_number": r.run_number,
                "duration_seconds": r.duration_seconds,
                "terror_zone_note": r.terror_zone_note,
                "created_at": r.created_at.isoformat(),
                "items": [ri.item.name for ri in r.items],
            }
            for r in runs
        ],
    }


class ImportRun(BaseModel):
    location: str
    run_number: int
    duration_seconds: int
    terror_zone_note: str | None = None
    items: list[str] = []


class ImportPayload(BaseModel):
    profile: dict
    runs: list[ImportRun]


@router.post("/import")
async def import_profile(payload: ImportPayload, db: AsyncSession = Depends(get_db)):
    # Create profile
    profile = Profile(
        name=payload.profile["name"],
        game_mode=GameMode(payload.profile["game_mode"]),
        character_class=CharacterClass(payload.profile["character_class"]),
    )
    db.add(profile)
    await db.flush()

    # Build item name -> id lookup
    item_names = set()
    for r in payload.runs:
        item_names.update(r.items)

    item_map: dict[str, int] = {}
    if item_names:
        result = await db.execute(select(Item).where(Item.name.in_(item_names)))
        for item in result.scalars():
            item_map[item.name] = item.id

    # Create runs
    for r in payload.runs:
        run = Run(
            profile_id=profile.id,
            location=Location(r.location),
            run_number=r.run_number,
            duration_seconds=r.duration_seconds,
            terror_zone_note=r.terror_zone_note,
        )
        db.add(run)
        await db.flush()

        for item_name in r.items:
            if item_name in item_map:
                db.add(RunItem(run_id=run.id, item_id=item_map[item_name]))

    await db.commit()
    return {"profile_id": profile.id, "runs_imported": len(payload.runs)}
