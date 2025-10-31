"""Backend API helpers for admin-only operations (settings, etc.)."""
from __future__ import annotations
import requests
from typing import Optional
from .config import Settings

class BackendApi:
    """Tiny REST helper that logs in via JWT and calls admin endpoints."""
    def __init__(self, base_url: str) -> None:
        # The frontend is at :5173; the API is reverse-proxied at /api under the same origin by the app.
        # The SPA uses relative /auth/... and /users/... so we do the same (assuming dev reverse-proxy).
        # If your backend is on a different port/host, adjust BASE here (e.g. http://localhost:8000).
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base = base_url  # for tests we hit the SPA origin and relative API paths
        self.jwt: Optional[str] = None

    def login(self, username: str, password: str) -> None:
        r = requests.post(f"{self.base}/auth/jwt/create/", json={"username": username, "password": password})
        r.raise_for_status()
        self.jwt = r.json()["access"]

    def set_idle_timeout(self, seconds: int) -> dict:
        assert self.jwt, "Call login() first"
        h = {"Authorization": f"Bearer {self.jwt}"}
        r = requests.patch(f"{self.base}/settings/", json={"IDLE_TIMEOUT_SECONDS": seconds, "ACCESS_TOKEN_LIFETIME": 3600, "JWT_RENEW_AT_SECONDS": 300}, headers=h)
        r.raise_for_status()
        return r.json()
