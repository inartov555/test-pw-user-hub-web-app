from __future__ import annotations

from playwright.sync_api import Page, expect


class Toast:
    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_message(self, text: str) -> None:
        toast = self.page.get_by_role("status")
        expect(toast).to_contain_text(text)
