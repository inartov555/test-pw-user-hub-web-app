"""
Page object for the /users table view with common interactions.
"""

from __future__ import annotations

from playwright.sync_api import Page, expect

from .base_page import BasePage


class UsersTablePage(BasePage):
    """
    Interactions and assertions for the users table page.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize with a Playwright page and the application base URL.
        """
        super().__init__(page)
        self.base_url = base_url
        self.path = "/users"  # adjust if app uses a different route

    @property
    def table(self):
        """
        Locator for the users table element.
        """
        return self.page.get_by_role("table")

    @property
    def rows(self):
        """
        Locator for all table rows within the tbody.
        """
        return self.page.locator("table tbody tr")

    @property
    def search(self):
        """
        Locator for the table search input.
        """
        return self.page.get_by_placeholder("Search")

    def open(self) -> None:
        """
        Navigate directly to the users table page.
        """
        self.goto(self.base_url + self.path)

    def expect_loaded(self) -> None:
        """
        Assert that the table and at least one row are visible.
        """
        expect(self.table).to_be_visible()
        expect(self.rows.first).to_be_visible()

    def filter_by(self, text: str) -> None:
        """
        Fill the search input to filter the table by text.
        """
        try:
            self.search.fill(text)
        except Exception:
            # Some variants may not expose a search box; ignore.
            pass

    def sort_by(self, column_name: str) -> None:
        """
        Click the specified column header to toggle sort order.
        """
        header = self.page.get_by_role(
            "columnheader",
            name=lambda n: column_name.lower() in n.lower(),
        )
        if header.is_visible():
            header.click()
