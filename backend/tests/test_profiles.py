import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_profile(client: AsyncClient):
    resp = await client.post("/profiles", json={
        "name": "Test Sorc", "game_mode": "ladder", "character_class": "sorceress"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Sorc"
    assert data["game_mode"] == "ladder"
    assert data["character_class"] == "sorceress"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_profiles(client: AsyncClient):
    await client.post("/profiles", json={"name": "P1", "game_mode": "ladder", "character_class": "warlock"})
    await client.post("/profiles", json={"name": "P2", "game_mode": "hardcore", "character_class": "paladin"})
    resp = await client.get("/profiles")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient):
    create = await client.post("/profiles", json={"name": "Old", "game_mode": "ladder", "character_class": "druid"})
    pid = create.json()["id"]
    resp = await client.put(f"/profiles/{pid}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"
    assert resp.json()["game_mode"] == "ladder"  # unchanged


@pytest.mark.asyncio
async def test_delete_profile(client: AsyncClient):
    create = await client.post("/profiles", json={"name": "Del", "game_mode": "non_ladder", "character_class": "amazon"})
    pid = create.json()["id"]
    resp = await client.delete(f"/profiles/{pid}")
    assert resp.status_code == 204
    resp = await client.get(f"/profiles/{pid}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_invalid_enum(client: AsyncClient):
    resp = await client.post("/profiles", json={"name": "X", "game_mode": "invalid", "character_class": "sorceress"})
    assert resp.status_code == 422
