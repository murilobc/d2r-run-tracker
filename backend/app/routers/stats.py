from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.run import Run, RunItem
from app.models.item import Item

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/{profile_id}")
async def get_stats(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await db.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")

    # Runs per location with avg time
    loc_stats = await db.execute(
        select(
            Run.location,
            func.count(Run.id).label("total_runs"),
            func.sum(Run.duration_seconds).label("total_time"),
            func.avg(Run.duration_seconds).label("avg_time"),
        )
        .where(Run.profile_id == profile_id)
        .group_by(Run.location)
    )

    locations = {}
    for row in loc_stats:
        locations[row.location.value] = {
            "total_runs": row.total_runs,
            "total_time_seconds": row.total_time,
            "avg_time_seconds": round(float(row.avg_time), 1),
        }

    # Top items
    top_items = await db.execute(
        select(Item.name, func.count(RunItem.id).label("count"))
        .join(RunItem, RunItem.item_id == Item.id)
        .join(Run, Run.id == RunItem.run_id)
        .where(Run.profile_id == profile_id)
        .group_by(Item.name)
        .order_by(func.count(RunItem.id).desc())
        .limit(20)
    )

    # Totals
    totals = await db.execute(
        select(
            func.count(Run.id),
            func.coalesce(func.sum(Run.duration_seconds), 0),
        ).where(Run.profile_id == profile_id)
    )
    total_runs, total_time = totals.one()

    total_items = await db.execute(
        select(func.count(RunItem.id))
        .join(Run, Run.id == RunItem.run_id)
        .where(Run.profile_id == profile_id)
    )

    return {
        "total_runs": total_runs,
        "total_time_seconds": total_time,
        "total_items_found": total_items.scalar(),
        "locations": locations,
        "top_items": [{"name": row.name, "count": row.count} for row in top_items],
    }
