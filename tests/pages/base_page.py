"""Base PageObject with common helpers."""
from __future__ import annotations
from playwright.sync_api import Page, expect

class BasePage:
    """Base class for all pages."""
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def assert_url_contains(self, path: str) -> None:
        expect(self.page).to_have_url(lambda u: path in u)
