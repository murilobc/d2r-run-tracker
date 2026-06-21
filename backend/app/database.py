from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

# Fly.io internal Postgres doesn't support SSL; Render.com and others do.
_connect_args = {}
if ".flycast" in settings.database_url or ".internal" in settings.database_url:
    _connect_args["ssl"] = False

engine = create_async_engine(settings.database_url, echo=False, connect_args=_connect_args)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
