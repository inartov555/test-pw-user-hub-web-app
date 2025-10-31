
from __future__ import annotations
import logging, requests
from config.settings import cfg

log = logging.getLogger("qa")

class ApiClient:
    def __init__(self, api_url: str | None = None):
        self.base = api_url or cfg.api_url
        self._access = None

    def login(self, username: str, password: str) -> str:
        r = requests.post(f"{self.base}/auth/jwt/create/", json={"username": username, "password": password}, timeout=20)
        r.raise_for_status()
        data = r.json()
        self._access = data["access"]
        log.info("Logged in as %s", username)
        return self._access

    def auth_headers(self):
        if not self._access:
            raise RuntimeError("Login first")
        return {"Authorization": f"Bearer {self._access}"}

    def create_user(self, username: str, email: str, first: str="", last: str=""):
        r = requests.post(f"{self.base}/users/", json={
            "username": username, "email": email, "first_name": first, "last_name": last, "password": "Test12345!"
        }, headers=self.auth_headers(), timeout=20)
        r.raise_for_status()
        return r.json()

    def delete_user(self, user_id: int):
        r = requests.delete(f"{self.base}/users/{user_id}/", headers=self.auth_headers(), timeout=20)
        r.raise_for_status()

    def get_settings(self):
        r = requests.get(f"{self.base}/system/settings/", headers=self.auth_headers(), timeout=20)
        r.raise_for_status()
        return r.json()

    def update_settings(self, payload):
        r = requests.patch(f"{self.base}/system/settings/", json=payload, headers=self.auth_headers(), timeout=20)
        r.raise_for_status()
        return r.json()
