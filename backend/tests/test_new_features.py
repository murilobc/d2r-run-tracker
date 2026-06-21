import pytest
from httpx import AsyncClient


async def _create_profile_with_run(client: AsyncClient):
    p = await client.post("/profiles", json={
        "name": "Stat Test", "game_mode": "ladder", "character_class": "sorceress"
    })
    pid = p.json()["id"]
    items = await client.get("/items", params={"search": "Ber Rune", "limit": 1})
    item_id = items.json()[0]["id"]
    await client.post("/runs", json={
        "profile_id": pid, "location": "mephisto", "duration_seconds": 200, "item_ids": [item_id]
    })
    await client.post("/runs", json={
        "profile_id": pid, "location": "mephisto", "duration_seconds": 100, "item_ids": []
    })
    return pid


@pytest.mark.asyncio
async def test_stats_endpoint(client: AsyncClient):
    pid = await _create_profile_with_run(client)
    resp = await client.get(f"/stats/{pid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_runs"] == 2
    assert data["total_time_seconds"] == 300
    assert data["total_items_found"] == 1
    assert "mephisto" in data["locations"]
    assert data["locations"]["mephisto"]["avg_time_seconds"] == 150.0


@pytest.mark.asyncio
async def test_import_export_roundtrip(client: AsyncClient):
    pid = await _create_profile_with_run(client)
    export_resp = await client.get(f"/export/{pid}")
    exported = export_resp.json()

    import_resp = await client.post("/export/import", json=exported)
    assert import_resp.status_code == 200
    result = import_resp.json()
    assert result["runs_imported"] == 2
    new_pid = result["profile_id"]
    assert new_pid != pid

    # Verify imported data
    runs = await client.get("/runs", params={"profile_id": new_pid})
    assert len(runs.json()) == 2


@pytest.mark.asyncio
async def test_create_run_invalid_profile(client: AsyncClient):
    resp = await client.post("/runs", json={
        "profile_id": 9999, "location": "pit", "duration_seconds": 60, "item_ids": []
    })
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_run_invalid_items(client: AsyncClient):
    p = await client.post("/profiles", json={
        "name": "T", "game_mode": "ladder", "character_class": "druid"
    })
    pid = p.json()["id"]
    resp = await client.post("/runs", json={
        "profile_id": pid, "location": "pit", "duration_seconds": 60, "item_ids": [99999]
    })
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_create_run_zero_duration_rejected(client: AsyncClient):
    p = await client.post("/profiles", json={
        "name": "T", "game_mode": "ladder", "character_class": "druid"
    })
    pid = p.json()["id"]
    resp = await client.post("/runs", json={
        "profile_id": pid, "location": "pit", "duration_seconds": 0, "item_ids": []
    })
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_profile_empty_name_rejected(client: AsyncClient):
    resp = await client.post("/profiles", json={
        "name": "", "game_mode": "ladder", "character_class": "sorceress"
    })
    assert resp.status_code == 422
