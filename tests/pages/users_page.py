"""Users table page object (sorting, search, selection)."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class UsersPage(BasePage):
    path = "/users"

    def open(self, base_url: str) -> None:
        self.goto(base_url + self.path)
        expect(self.page.get_by_role("heading", name=lambda n: "Users" in n)).to_be_visible()

    @property
    def searchbox(self):
        return self.page.get_by_placeholder("Search") 

    def header(self, col_text: str):
        return self.page.get_by_role("columnheader", name=lambda n: col_text.lower() in n.lower()).first

    def visible_rows(self):
        return self.page.locator("table tbody tr")

    def cell_texts(self, col_index: int) -> list[str]:
        return [self.page.locator(f"table tbody tr >> td:nth-child({col_index})").nth(i).inner_text().strip() for i in range(self.visible_rows().count())]

    def clear_sort(self):
        self.page.get_by_role("button", name=lambda n: "Clear" in n and "sort" in n.lower()).click()
