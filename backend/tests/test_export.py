import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_export_profile(client: AsyncClient):
    # Create profile and runs
    p = await client.post("/profiles", json={
        "name": "Export Test", "game_mode": "ladder", "character_class": "warlock"
    })
    pid = p.json()["id"]

    items_resp = await client.get("/items", params={"search": "Ist Rune", "limit": 1})
    item_id = items_resp.json()[0]["id"]

    await client.post("/runs", json={
        "profile_id": pid, "location": "chaos_sanctuary", "duration_seconds": 300, "item_ids": [item_id]
    })
    await client.post("/runs", json={
        "profile_id": pid, "location": "chaos_sanctuary", "duration_seconds": 250, "item_ids": []
    })

    resp = await client.get(f"/export/{pid}")
    assert resp.status_code == 200
    data = resp.json()

    assert data["profile"]["name"] == "Export Test"
    assert data["profile"]["character_class"] == "warlock"
    assert len(data["runs"]) == 2
    assert data["runs"][0]["items"] == ["Ist Rune"]
    assert data["runs"][1]["items"] == []


@pytest.mark.asyncio
async def test_export_nonexistent_profile(client: AsyncClient):
    resp = await client.get("/export/9999")
    assert resp.status_code == 404
