from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, async_session
from app.routers import profiles, items, runs, export, stats
from app.seed.seed_items import seed_items


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session() as session:
        await seed_items(session)
    yield
    await engine.dispose()


app = FastAPI(title="D2R MF Run Tracker", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://frontend:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profiles.router)
app.include_router(items.router)
app.include_router(runs.router)
app.include_router(export.router)
app.include_router(stats.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
