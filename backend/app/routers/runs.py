from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.profile import Profile
from app.models.item import Item
from app.models.run import Location, Run, RunItem
from app.schemas.run import RunCreate, RunResponse

router = APIRouter(prefix="/runs", tags=["runs"])

MAX_RETRIES = 3


@router.post("", response_model=RunResponse, status_code=201)
async def create_run(data: RunCreate, db: AsyncSession = Depends(get_db)):
    # Validate profile exists
    profile = await db.get(Profile, data.profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")

    # Validate item_ids exist
    if data.item_ids:
        result = await db.execute(select(func.count(Item.id)).where(Item.id.in_(data.item_ids)))
        if result.scalar() != len(data.item_ids):
            raise HTTPException(400, "One or more item_ids are invalid")

    # Retry loop for run_number race condition
    for attempt in range(MAX_RETRIES):
        result = await db.execute(
            select(func.coalesce(func.max(Run.run_number), 0))
            .where(Run.profile_id == data.profile_id, Run.location == data.location)
        )
        next_number = result.scalar() + 1

        run = Run(
            profile_id=data.profile_id,
            location=data.location,
            run_number=next_number,
            duration_seconds=data.duration_seconds,
            terror_zone_note=data.terror_zone_note,
        )
        db.add(run)

        try:
            await db.flush()
            break
        except IntegrityError:
            await db.rollback()
            if attempt == MAX_RETRIES - 1:
                raise HTTPException(409, "Could not assign run number, try again")

    for item_id in data.item_ids:
        db.add(RunItem(run_id=run.id, item_id=item_id))

    await db.commit()

    result = await db.execute(
        select(Run).where(Run.id == run.id).options(selectinload(Run.items).selectinload(RunItem.item))
    )
    return result.scalar_one()


@router.get("", response_model=list[RunResponse])
async def list_runs(
    profile_id: int,
    location: Location | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Run)
        .where(Run.profile_id == profile_id)
        .options(selectinload(Run.items).selectinload(RunItem.item))
    )

    if location:
        query = query.where(Run.location == location)

    query = query.order_by(Run.created_at.desc()).offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    return result.scalars().all()


@router.delete("/{run_id}", status_code=204)
async def delete_run(run_id: int, db: AsyncSession = Depends(get_db)):
    run = await db.get(Run, run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    await db.delete(run)
    await db.commit()


@router.get("/next-number")
async def get_next_run_number(
    profile_id: int, location: Location, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(func.coalesce(func.max(Run.run_number), 0))
        .where(Run.profile_id == profile_id, Run.location == location)
    )
    return {"next_run_number": result.scalar() + 1}
