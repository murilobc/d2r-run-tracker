import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_by_name(client: AsyncClient):
    resp = await client.get("/items", params={"search": "Harlequin", "limit": 5})
    assert resp.status_code == 200
    items = resp.json()
    assert any(i["name"] == "Harlequin Crest" for i in items)


@pytest.mark.asyncio
async def test_search_by_alias(client: AsyncClient):
    resp = await client.get("/items", params={"search": "shako", "limit": 5})
    assert resp.status_code == 200
    items = resp.json()
    assert any(i["name"] == "Harlequin Crest" for i in items)


@pytest.mark.asyncio
async def test_filter_by_category(client: AsyncClient):
    resp = await client.get("/items", params={"category": "rune", "limit": 50})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 33
    assert all(i["category"] == "rune" for i in items)


@pytest.mark.asyncio
async def test_search_rotw_items(client: AsyncClient):
    resp = await client.get("/items", params={"search": "Ars Al", "limit": 10})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) >= 1
    assert all(i["is_rotw"] for i in items)


@pytest.mark.asyncio
async def test_empty_search_returns_items(client: AsyncClient):
    resp = await client.get("/items", params={"limit": 10})
    assert resp.status_code == 200
    assert len(resp.json()) == 10
