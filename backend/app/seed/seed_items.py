import asyncio
import json
from pathlib import Path

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item, ItemCategory

SEED_DIR = Path(__file__).parent

DATA_FILES = [
    "data_runes.json",
    "data_runewords.json",
    "data_uniques_weapons_armor_helms.json",
    "data_uniques_gear.json",
    "data_uniques_accessories.json",
    "data_sets.json",
    "data_charms.json",
    "data_jewels.json",
    "data_bases.json",
    "data_magic_rare_consumables.json",
]


async def seed_items(session: AsyncSession) -> int:
    count = (await session.execute(select(func.count(Item.id)))).scalar()
    if count and count > 0:
        return 0

    items = []
    for filename in DATA_FILES:
        filepath = SEED_DIR / filename
        with open(filepath) as f:
            data = json.load(f)
        for entry in data:
            items.append(Item(
                name=entry["name"],
                category=ItemCategory(entry["category"]),
                subcategory=entry.get("subcategory", ""),
                aliases=entry.get("aliases", []),
                is_rotw=entry.get("is_rotw", False),
                is_ladder_only=entry.get("is_ladder_only", False),
            ))

    session.add_all(items)
    await session.commit()
    return len(items)


if __name__ == "__main__":
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from app.config import settings

    async def main():
        engine = create_async_engine(settings.database_url)
        factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with factory() as session:
            inserted = await seed_items(session)
            print(f"Seeded {inserted} items." if inserted else "Items already populated.")
        await engine.dispose()

    asyncio.run(main())
