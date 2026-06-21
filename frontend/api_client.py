import os

import httpx

BASE_URL = os.getenv("API_URL", "http://api:8000")
TIMEOUT = 10.0


class ApiError(Exception):
    def __init__(self, message: str):
        self.message = message


def _url(path: str) -> str:
    return f"{BASE_URL}{path}"


def _handle(resp: httpx.Response) -> dict | list:
    if resp.status_code >= 400:
        detail = resp.json().get("detail", resp.text) if resp.headers.get("content-type", "").startswith("application/json") else resp.text
        raise ApiError(f"Erro na API ({resp.status_code}): {detail}")
    if resp.status_code == 204:
        return {}
    return resp.json()


def list_profiles() -> list[dict]:
    return _handle(httpx.get(_url("/profiles"), timeout=TIMEOUT))


def create_profile(name: str, game_mode: str, character_class: str) -> dict:
    return _handle(httpx.post(_url("/profiles"), json={
        "name": name, "game_mode": game_mode, "character_class": character_class
    }, timeout=TIMEOUT))


def delete_profile(profile_id: int):
    _handle(httpx.delete(_url(f"/profiles/{profile_id}"), timeout=TIMEOUT))


def search_items(search: str = "", category: str | None = None, limit: int = 50) -> list[dict]:
    params = {"search": search, "limit": limit}
    if category:
        params["category"] = category
    return _handle(httpx.get(_url("/items"), params=params, timeout=TIMEOUT))


def get_next_run_number(profile_id: int, location: str) -> int:
    resp = _handle(httpx.get(_url("/runs/next-number"), params={
        "profile_id": profile_id, "location": location
    }, timeout=TIMEOUT))
    return resp["next_run_number"]


def create_run(profile_id: int, location: str, duration_seconds: int,
               item_ids: list[int], terror_zone_note: str | None = None) -> dict:
    payload = {
        "profile_id": profile_id,
        "location": location,
        "duration_seconds": duration_seconds,
        "item_ids": item_ids,
    }
    if terror_zone_note:
        payload["terror_zone_note"] = terror_zone_note
    return _handle(httpx.post(_url("/runs"), json=payload, timeout=TIMEOUT))


def list_runs(profile_id: int, location: str | None = None, page: int = 1, size: int = 50) -> list[dict]:
    params = {"profile_id": profile_id, "page": page, "size": size}
    if location:
        params["location"] = location
    return _handle(httpx.get(_url("/runs"), params=params, timeout=TIMEOUT))


def get_stats(profile_id: int) -> dict:
    return _handle(httpx.get(_url(f"/stats/{profile_id}"), timeout=TIMEOUT))


def export_profile(profile_id: int) -> dict:
    return _handle(httpx.get(_url(f"/export/{profile_id}"), timeout=TIMEOUT))


def import_profile(data: dict) -> dict:
    return _handle(httpx.post(_url("/export/import"), json=data, timeout=TIMEOUT))
