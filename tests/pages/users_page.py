"""Users list page object (multi-column sort, pagination, actions)."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base import BasePage

class UsersPage(BasePage):
    path = "/users"
    def open(self):
        self.goto(self.path)
        expect(self.page.get_by_role("heading", name="Users")).to_be_visible()

    def sort_by(self, col_header: str, times: int = 1):
        th = self.page.get_by_role("columnheader", name=col_header).first
        for _ in range(times):
            th.click()

    def get_table_text(self) -> list[list[str]]:
        rows = self.page.locator("table tbody tr")
        data = []
        for i in range(rows.count()):
            row = rows.nth(i).locator("td").all_inner_texts()
            data.append([c.strip() for c in row])
        return data

    def delete_user(self, username: str):
        row = self.page.get_by_role("row", name=username)
        row.get_by_role("button", name="Delete").click()
        self.page.get_by_role("button", name="Confirm delete").click()
        expect(self.page.get_by_text("User deleted")).to_be_visible()
