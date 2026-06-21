from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.item import Item, ItemCategory
from app.schemas.item import ItemResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
async def search_items(
    search: str = Query("", min_length=0),
    category: ItemCategory | None = None,
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    query = select(Item)

    if category:
        query = query.where(Item.category == category)

    if search:
        pattern = f"%{search}%"
        query = query.where(
            or_(
                Item.name.ilike(pattern),
                Item.aliases.any(search.lower()),
            )
        )

    query = query.order_by(Item.name).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
