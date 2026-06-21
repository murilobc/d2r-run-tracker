from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("", response_model=ProfileResponse, status_code=201)
async def create_profile(data: ProfileCreate, db: AsyncSession = Depends(get_db)):
    profile = Profile(**data.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("", response_model=list[ProfileResponse])
async def list_profiles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).order_by(Profile.created_at.desc()))
    return result.scalars().all()


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await db.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile


@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(profile_id: int, data: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    profile = await db.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=204)
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await db.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    await db.delete(profile)
    await db.commit()
