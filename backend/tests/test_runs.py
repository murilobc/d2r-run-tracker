import pytest
from httpx import AsyncClient


async def _create_profile(client: AsyncClient) -> int:
    resp = await client.post("/profiles", json={
        "name": "Test", "game_mode": "ladder", "character_class": "sorceress"
    })
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_run_sequential_number(client: AsyncClient):
    pid = await _create_profile(client)

    r1 = await client.post("/runs", json={
        "profile_id": pid, "location": "mephisto", "duration_seconds": 120, "item_ids": []
    })
    assert r1.status_code == 201
    assert r1.json()["run_number"] == 1

    r2 = await client.post("/runs", json={
        "profile_id": pid, "location": "mephisto", "duration_seconds": 100, "item_ids": []
    })
    assert r2.json()["run_number"] == 2

    # Different location starts at 1
    r3 = await client.post("/runs", json={
        "profile_id": pid, "location": "pit", "duration_seconds": 90, "item_ids": []
    })
    assert r3.json()["run_number"] == 1


@pytest.mark.asyncio
async def test_create_run_with_items(client: AsyncClient):
    pid = await _create_profile(client)

    # Get some item IDs
    items_resp = await client.get("/items", params={"search": "Ber Rune", "limit": 1})
    item_id = items_resp.json()[0]["id"]

    resp = await client.post("/runs", json={
        "profile_id": pid, "location": "travincal", "duration_seconds": 200, "item_ids": [item_id]
    })
    assert resp.status_code == 201
    assert len(resp.json()["items"]) == 1
    assert resp.json()["items"][0]["item"]["name"] == "Ber Rune"


@pytest.mark.asyncio
async def test_list_runs_filter_by_location(client: AsyncClient):
    pid = await _create_profile(client)
    await client.post("/runs", json={"profile_id": pid, "location": "mephisto", "duration_seconds": 100, "item_ids": []})
    await client.post("/runs", json={"profile_id": pid, "location": "pit", "duration_seconds": 80, "item_ids": []})

    resp = await client.get("/runs", params={"profile_id": pid, "location": "mephisto"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["location"] == "mephisto"


@pytest.mark.asyncio
async def test_delete_run(client: AsyncClient):
    pid = await _create_profile(client)
    r = await client.post("/runs", json={"profile_id": pid, "location": "andariel", "duration_seconds": 60, "item_ids": []})
    run_id = r.json()["id"]

    resp = await client.delete(f"/runs/{run_id}")
    assert resp.status_code == 204

    resp = await client.delete(f"/runs/{run_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_next_run_number(client: AsyncClient):
    pid = await _create_profile(client)

    resp = await client.get("/runs/next-number", params={"profile_id": pid, "location": "cows"})
    assert resp.json()["next_run_number"] == 1

    await client.post("/runs", json={"profile_id": pid, "location": "cows", "duration_seconds": 300, "item_ids": []})

    resp = await client.get("/runs/next-number", params={"profile_id": pid, "location": "cows"})
    assert resp.json()["next_run_number"] == 2


@pytest.mark.asyncio
async def test_terror_zone_note(client: AsyncClient):
    pid = await _create_profile(client)
    resp = await client.post("/runs", json={
        "profile_id": pid, "location": "terror_zone", "duration_seconds": 150,
        "item_ids": [], "terror_zone_note": "Tal Rasha's Tombs"
    })
    assert resp.json()["terror_zone_note"] == "Tal Rasha's Tombs"
