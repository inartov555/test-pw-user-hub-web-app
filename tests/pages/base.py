"""Base page object with common helpers."""
from __future__ import annotations
from playwright.sync_api import Page, expect

class BasePage:
    """Base class for all page objects."""
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str):
        self.page.goto(self.base_url.rstrip("/") + path)

    def assert_url_contains(self, fragment: str):
        expect(self.page).to_have_url(lambda url: fragment in url)

    def set_local_storage(self, key: str, value: str):
        self.page.evaluate("(k,v)=>localStorage.setItem(k,v)", key, value)

    def get_local_storage(self, key: str) -> str|None:
        return self.page.evaluate("k=>localStorage.getItem(k)", key)

    def reload(self):
        self.page.reload()
