import os
import time as _time

import httpx

BASE_URL = os.getenv("API_URL", "https://d2r-run-tracker-api.fly.dev")
TIMEOUT = 60.0
MAX_RETRIES = 2


class ApiError(Exception):
    def __init__(self, message: str):
        self.message = message


def _url(path: str) -> str:
    return f"{BASE_URL}{path}"


def _request(method: str, url: str, **kwargs) -> httpx.Response:
    """Make an HTTP request with retry on timeout (handles Fly.io cold starts)."""
    kwargs.setdefault("timeout", TIMEOUT)
    for attempt in range(MAX_RETRIES + 1):
        try:
            return getattr(httpx, method)(url, **kwargs)
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.ConnectError):
            if attempt == MAX_RETRIES:
                raise
            _time.sleep(2)


def _handle(resp: httpx.Response) -> dict | list:
    if resp.status_code >= 400:
        detail = resp.json().get("detail", resp.text) if resp.headers.get("content-type", "").startswith("application/json") else resp.text
        raise ApiError(f"Erro na API ({resp.status_code}): {detail}")
    if resp.status_code == 204:
        return {}
    return resp.json()


def list_profiles() -> list[dict]:
    return _handle(_request("get", _url("/profiles")))


def create_profile(name: str, game_mode: str, character_class: str) -> dict:
    return _handle(_request("post", _url("/profiles"), json={
        "name": name, "game_mode": game_mode, "character_class": character_class
    }))


def delete_profile(profile_id: int):
    _handle(_request("delete", _url(f"/profiles/{profile_id}")))


def search_items(search: str = "", category: str | None = None, limit: int = 50) -> list[dict]:
    params = {"search": search, "limit": limit}
    if category:
        params["category"] = category
    return _handle(_request("get", _url("/items"), params=params))


def get_next_run_number(profile_id: int, location: str) -> int:
    resp = _handle(_request("get", _url("/runs/next-number"), params={
        "profile_id": profile_id, "location": location
    }))
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
    return _handle(_request("post", _url("/runs"), json=payload))


def list_runs(profile_id: int, location: str | None = None, page: int = 1, size: int = 50) -> list[dict]:
    params = {"profile_id": profile_id, "page": page, "size": size}
    if location:
        params["location"] = location
    return _handle(_request("get", _url("/runs"), params=params))


def get_stats(profile_id: int) -> dict:
    return _handle(_request("get", _url(f"/stats/{profile_id}")))


def export_profile(profile_id: int) -> dict:
    return _handle(_request("get", _url(f"/export/{profile_id}")))


def import_profile(data: dict) -> dict:
    return _handle(_request("post", _url("/export/import"), json=data))
