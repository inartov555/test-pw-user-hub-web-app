"""Users table page object (used for sorting coverage)."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class UsersPage(BasePage):
    path = "/users"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.table = page.locator("table").first

    def assert_loaded(self):
        expect(self.table).to_be_visible()
        return self

    def rows(self) -> int:
        return self.page.locator("table tbody tr").count()
