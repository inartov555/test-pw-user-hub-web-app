"""Base page object: common helpers and assertions."""
from __future__ import annotations
from playwright.sync_api import Page, expect

class BasePage:
    """Base class for Page Objects.

    Args:
        page: Playwright Page instance
    """
    path = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self):
        self.page.goto(self.path)
        return self

    def assert_title_contains(self, text: str):
        expect(self.page).to_have_title(lambda t: text in t)

    # Generic table helpers
    def sort_by_columns(self, *headers: str):
        """Click header names with Shift+Click to multi-sort in given order."""
        first = True
        for name in headers:
            locator = self.page.get_by_role("columnheader", name=name)
            if first:
                locator.click()
                first = False
            else:
                locator.click(modifiers=["Shift"])

    def get_table_cells(self, col_name: str) -> list[str]:
        col_index = self.page.get_by_role("columnheader", name=col_name).evaluate(
            "(th) => Array.from(th.parentElement.children).indexOf(th)"
        )
        rows = self.page.locator("table tbody tr")
        count = rows.count()
        values = []
        for i in range(count):
            values.append(rows.nth(i).locator("td").nth(col_index).inner_text().strip())
        return values
