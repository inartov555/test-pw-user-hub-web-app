from __future__ import annotations

from playwright.sync_api import Page, expect

from .base_page import BasePage


class UsersTablePage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.path = "/users"  # adjust if app uses a different route

    @property
    def table(self):
        return self.page.get_by_role("table")

    @property
    def rows(self):
        return self.page.locator("table tbody tr")

    @property
    def search(self):
        return self.page.get_by_placeholder("Search")

    def open(self) -> None:
        self.goto(self.base_url + self.path)

    def expect_loaded(self) -> None:
        expect(self.table).to_be_visible()
        expect(self.rows.first).to_be_visible()

    def filter_by(self, text: str) -> None:
        try:
            self.search.fill(text)
        except Exception:
            pass

    def sort_by(self, column_name: str) -> None:
        header = self.page.get_by_role("columnheader", name=lambda n: column_name.lower() in n.lower())
        if header.is_visible():
            header.click()
