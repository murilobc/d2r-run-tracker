import os
import sys

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import Base
from app.main import app
from app.database import get_db
from app.seed.seed_items import seed_items

TEST_DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://d2r_tracker:d2r_tracker_pass@db:5432/d2r_run_tracker")


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DB_URL, pool_size=5)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        await seed_items(session)

    async def override():
        async with session_factory() as s:
            yield s

    app.dependency_overrides[get_db] = override
    yield
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
