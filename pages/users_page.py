
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class UsersPage(BasePage):
    path = "/users"
    def expect_loaded(self):
        self.goto()
        expect(self.page.get_by_role("heading", name="Users")).to_be_visible()
    def header(self, name: str):
        return self.page.get_by_role("button", name=name)
    def sort_by(self, col_header: str, times: int = 1):
        for _ in range(times):
            self.header(col_header).click()
    def get_column_values(self, index: int):
        return [c.inner_text().strip() for c in self.page.locator(f"table tbody tr td:nth-child({index})").all()]
